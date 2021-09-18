var gulp = require("gulp")
var cssnano = require("gulp-cssnano")
var sass = require('gulp-sass')(require('sass'))
var rename = require("gulp-rename")
var uglify = require("gulp-uglify")
var watch = require('gulp-watch')
var concat = require("gulp-concat")
var cache = require("gulp-cache")
//var imagemin = require("gulp-imagemin")
var bs = require("browser-sync").create()

//各个文件的路径,方便开发
var path = {
    'html':'./templates/**/',
    'css':'./src/css/',
    'js':'./src/js/',
    'images':'./src/images/',
    'css_dist':'./dist/css/',
    'js_dist':'./dist/js/',
    'images_dist':'./dist/images/'
}

//定义文件处理任务
gulp.task('css',function (){
    gulp.src(path.css+'*.scss')
        .pipe(sass().on('error',sass.logError))
        .pipe(cssnano())
        .pipe(rename({'suffix':'.min'}))
        .pipe(gulp.dest(path.css_dist))
        .pipe(bs.stream())
})

gulp.task('js',function (){
    gulp.src(path.js+'*.js')
        .pipe(uglify())
        .pipe(rename({'suffix':'.min'}))
        .pipe(gulp.dest(path.js_dist))
        .pipe(bs.stream())
})

/*gulp.task('images',function (){
    gulp.src(path.images+'*.*')
        .pipe(cache(imagemin()))
        .pipe(gulp.dest(path.images_dist))
})*/

gulp.task('html',function (){
    gulp.src(path.html+'*.html')
        .pipe(bs.stream())
})

//监听任务
gulp.task('watch',function (){
    watch(path.css+'*.scss',gulp.series('css'))
    watch(path.js+'*.js',gulp.series('js'))
    //gulp.watch(path.images+'*.*',['images'])
    watch(path.html+'*.html',gulp.series('html'))
})

//初始化browser-sync的任务
gulp.task('bs',function (){
    bs.init({
        'server':{
            'baseDir':'./'
        }
    })
})

//创建默认任务
gulp.task('default',gulp.series('watch'))