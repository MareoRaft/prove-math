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
const moment = require('moment')
const prop_reader = require('properties-reader')


/////////////////// GLOBALS ///////////////////
const src_scss = 'www/sass/**/*.scss'
const src_js6 = 'www/scripts6/**/*.js'
const src_docs = 'docs/source/**/*'

const log_standard = function(event) {
	console.log('File ' + event.path + ' was ' + event.type + ', running tasks...')
}


///////////////////// MAIN /////////////////////
gulp.task('css', function() {
	gulp.src(src_scss)
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

gulp.task('js', function() {
	gulp.src(src_js6)
		.pipe(babel({
			presets: ['es2015'], // Specifies which ECMAScript standard to follow.  This is necessary.
		}))
		.pipe(gulp.dest('www/scripts'))
})

gulp.task('docs', function(cb) {
	// generate docs/build/html from docs/source using sphinx's `sphinx-build` command
	var command = 'cd docs && sphinx-build -b html source build/html'
	exec(command, function (err, stdout, stderr) {
		console.log(stdout)
		console.log(stderr)
		cb(err)
	})
})

gulp.task('minify', function(cb) {
	// so using config.js as the mainConfigFile doesn't work, so we have to use main.js instead.  But that means the 'paths' option in the config file is missing, so I had to create symlinks in the www/scripts/lib directory to point to all the correct JS files :(
	var command = 'node build/r.js -o build/rbuild.js && echo \'REMEMBER to switch "config" to "config-optimized.min" in config.py!\''
	exec(command, function (err, stdout, stderr) {
		console.log(stdout)
		console.log(stderr)
		cb(err)
	})
})

gulp.task('search', function(cb) {
	var command = 'mongo provemath build/mongo-create-search-index.js'
	exec(command, function (err, stdout, stderr) {
		console.log(stdout)
		console.log(stderr)
		cb(err)
	})
})

gulp.task('dump', function(cb) {
	// Dump a backup of the current database contents into the mongo-dumps folder.
	var props = prop_reader('local-config.ini')
	var location = props.get('computer_name')
	var date = moment().format()
	var command = 'DUMPDIR="server/data/mongo-dumps/'+location+'.'+date+'" && mkdir "$DUMPDIR" && mongodump --db provemath --out "$DUMPDIR"'
	exec(command, function (err, stdout, stderr) {
		console.log(stdout)
		console.log(stderr)
		cb(err)
	})
})

gulp.task('mongo-config', function(cb) {
	// Write the mongod config file. (meant for the SERVER) See issue #43
	var command = 'cp -nv build/mongod.conf /usr/local/etc/mongodb.conf && echo \'You can run "use admin" and then "db.runCommand({ getCmdLineOpts: 1 })" in the mongo interactive prompt to see which config file mongo is actually using.\''
	exec(command, function (err, stdout, stderr) {
		console.log(stdout)
		console.log(stderr)
		cb(err)
	})
})

gulp.task('watch', function() {
	// css watcher
	var watch_css = gulp.watch(src_scss, ['css'])
	watch_css.on('change', log_standard)
	// js watcher
	var watch_js = gulp.watch(src_js6, ['js'])
	watch_js.on('change', log_standard)
	// docs watcher
	var watch_docs = gulp.watch(src_docs, ['docs'])
	watch_docs.on('change', log_standard)
})

gulp.task('default', ['js', 'css', 'docs', 'watch'])
// The 'deploy' task is what the server should run when updating ProveMath for real users.
gulp.task('deploy', ['search', 'js', 'css', 'docs', 'minify', 'watch'])
// The 'setup' task is for setting up a new server (which is rare).
gulp.task('setup', ['mongo-config'])
