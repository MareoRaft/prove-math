/*
Run this file by typing 'gulp' in the command line (you must be somewhere in provemath directory).
More info: https://github.com/gulpjs/gulp/blob/master/docs/getting-started.md
syncronous running: http://stackoverflow.com/questions/26715230/gulp-callback-how-to-tell-gulp-to-run-a-task-first-before-another/26715351
*/
/////////////////// IMPORTS ///////////////////
const gulp = require('gulp')

const compass = require('gulp-for-compass')
const autoprefixer = require('gulp-autoprefixer')
const babel = require('gulp-babel')
const exec = require('child_process').exec


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
		.pipe(autoprefixer({
			browsers: ['last 3 versions'],
			cascade: false,
		}))
		.pipe(gulp.dest('www/stylesheets'))
})

gulp.task('babel', function() {
	gulp.src(src_babel)
		.pipe(babel({
			presets: ['es2015'], // Specifies which ECMAScript standard to follow.  This is necessary.
		}))
		.pipe(gulp.dest('www/scripts'))
})

gulp.task('minify', function(cb) {
	// so using config.js as the mainConfigFile doesn't work, so we have to use main.js instead.  But that means the 'paths' option in the config file is missing, so I had to create symlinks in the www/scripts/lib directory to point to all the correct JS files :(
	exec('node build/r.js -o build/rbuild.js && echo \'REMEMBER to switch "config" to "config-optimized.min" in config.py!\'', function (err, stdout, stderr) {
		console.log(stdout)
		console.log(stderr)
		cb(err)
	})
})

gulp.task('watch', function() {
	// compass and autoprefixer watcher
	var watch_compass = gulp.watch(src_compass, ['compass'])
	watch_compass.on('change', log_standard)
	// babel watcher
	var watch_babel = gulp.watch(src_babel, ['babel'])
	watch_babel.on('change', log_standard)
})

gulp.task('default', ['babel', 'compass', 'watch'])
