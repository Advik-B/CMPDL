module.exports = function(grunt) {

    // configuration
    grunt.initConfig({

        // watch cmd
        watch: {
            styl: {
                files: ['styl/*.styl', 'styl/**'],
                tasks: [
                    'copy:to_build',
                    'replace:pre',
                    'stylus:compile',
                    'replace:post',
                    'copy:to_dist'
                ],
            },
        },

        // copy cmd
        copy: {
            to_build: {
                files: [{
                    cwd: 'styl',
                    dest: 'build/',
                    src: ['**'],
                    expand: true,
                }]
            },
            to_dist: {
                files: [{
                    cwd: '.',
                    dest: './dist/',
                    src: [
                        // here put your existing files to copy them to `dest`
                        //'qss/nodeeditor.qss',
                        //'qss/skin.qss'
                    ],
                    expand: false,
                }]
            }
        },

        // replace cmd
        replace: {
            pre: {
                overwrite: true,
                src: [
                    // source files
                    'build/*.styl',
                    'build/dark/*.styl',
                    // add more here if you want...
                ],
                replacements: [
                    // string replacement
                    {from: ':!', to: ':~'},
                    {from: 'x1:', to: 'x1\\:'},
                    {from: 'x1 :', to: 'x1\\:'},
                    {from: 'y1:', to: 'y1\\:'},
                    {from: 'y1 :', to: 'y1\\:'},
                    {from: 'x2:', to: 'x2\\:'},
                    {from: 'x2 :', to: 'x2\\:'},
                    {from: 'y2:', to: 'y2\\:'},
                    {from: 'y2 :', to: 'y2\\:'},
                    {from: 'stop:', to: 'stop\\:'},
                    {from: 'stop :', to: 'stop\\:'},
                ]
            },

            post: {
                overwrite: true,
                src: [      // source files array
                    'qss/skin.qss',
                    'qss/nodeeditor.qss',
                    'qss/dark.qss',
                ],
                replacements: [
                    {from: ':~', to: ':!'},
                ]
            },
        },


        stylus: {
            compile: {
                options: {
                    paths: ['styl'],
                    compress: false,
                },
                files: {
                    'qss/skin.qss': 'build/skin.styl',
                    'qss/dark.qss': 'build/dark/skin.styl',
                    'qss/nodeeditor.qss': 'build/nodeeditor.styl',
                }
            }
        },

    });

    grunt.loadNpmTasks('grunt-contrib-stylus');
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-text-replace');
    grunt.loadNpmTasks('grunt-contrib-watch');

    // register default task
    grunt.registerTask('default', [
        'copy:to_build',
        'replace:pre',
        'stylus:compile',
        'replace:post',
        'copy:to_dist',
        'watch'
    ]);
}