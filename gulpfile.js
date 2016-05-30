/*
Run this file by typing 'gulp' in the command line (you must be in the provemath directory).
More info: https://github.com/gulpjs/gulp/blob/master/docs/getting-started.md
*/
/////////////////// IMPORTS ///////////////////
const gulp = require('gulp')

const compass = require('gulp-for-compass')
const autoprefixer = require('gulp-autoprefixer')
const sourcemaps = require('gulp-sourcemaps')
const concat = require('gulp-concat')
const babel = require('gulp-babel')


/////////////////// GLOBALS ///////////////////
const src_compass = 'www/sass/**/*.scss'
const src_babel = 'www/scripts6/**/*.js'

const log_standard = function(event) {
	console.log('File ' + event.path + ' was ' + event.type + ', running tasks...')
}


///////////////////// MAIN /////////////////////
gulp.task('compass', function() {
	gulp.src(src_compass)
		.pipe(compass({
			sassDir: 'www/sass',
			cssDir: 'www/stylesheets',
			force: true,
		}))
})

gulp.task('autoprefixer', ['compass'], function () {
	gulp.src('www/stylesheets/**/*.css')
		// sourcemaps optional
		.pipe(sourcemaps.init())
		.pipe(autoprefixer({
			browsers: ['last 2 versions'],
			cascade: false,
		}))
		.pipe(concat('main.css'))
		.pipe(sourcemaps.write('.'))
		.pipe(gulp.dest('www/stylesheets'))
})

gulp.task('babel', function() {
	gulp.src(src_babel)
		.pipe(babel())
		.pipe(gulp.dest('www/scripts'))
})

gulp.task('watch', function() {
	// compass and autoprefixer watcher
	var watch_autoprefixer = gulp.watch(src_compass, ['autoprefixer'])
	watch_autoprefixer.on('change', log_standard)
	// babel watcher
	var watch_babel = gulp.watch(src_babel, ['babel'])
	watch_babel.on('change', log_standard)
})

gulp.task('default', ['babel', 'autoprefixer', 'watch'])
