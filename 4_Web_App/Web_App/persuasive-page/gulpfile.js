'use strict';

// dependencies
var gulp = require('gulp');
var sass = require('gulp-sass');
var minifyCSS = require('gulp-clean-css');
var uglify = require('gulp-uglify');
var rename = require('gulp-rename');
var changed = require('gulp-changed');
var browserSync = require('browser-sync').create();

  /////////////////
 // -SCSS/CSS- ///
/////////////////

var SCSS_SRC = './src/Assets/scss/**/*.scss';
var SCSS_DEST = './src/Assets/css';


function browser_sync(done) {

	browserSync.init({
		server: {
			baseDir: './src/'
		}
	});

	done();
}

// Compile SCSS after running watch tasks
// the scss will create a 'css' like file, which will be
// minified into a compressed readable CSS file
gulp.task('compile_scss', function(done){

	gulp.src(SCSS_SRC)
	.pipe(sass().on('error', sass.logError))
	.pipe(minifyCSS())
	.pipe(rename({ suffix: '.min' }))
	.pipe(changed(SCSS_DEST))
	.pipe(gulp.dest(SCSS_DEST))
	.pipe(browserSync.stream());

	done();
});



///detect changes in SCSS
gulp.task('watch_scss', function(done){
	gulp.watch(SCSS_SRC, gulp.series('compile_scss'))
});


//Run tasks
gulp.task('default', gulp.series('watch_scss'));