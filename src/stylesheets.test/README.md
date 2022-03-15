# Introduction
This is a QSS files generator for Qt framework (https://www.qt.io/). Instead of writing qss files on your own,
you use Stylus (http://stylus-lang.com/) and with Node.js (https://nodejs.org/en/), and mainly Grunt (https://gruntjs.com/),
a watch task will be running on background and your qss will be generated just by saving of your source *.styl files to disk!

Using Stylus for the job solves bunch of issues in Qt (probably caused by taking Web's CSS technology and breaking it so badly):
* variables
* functions
* overrides
* nested selectors
* parent referencing
* and more!

By default there is /styl folder containing your Stylus source files which is being watched and compiled into /qss directory. 
Mainly the /styl/skin.styl is being compiled ingo /qss/skin.qss.

If you want to setup different files, just modify the Gruntfile.js for yourself and re-run the grunt watch task.

Happy coding! ;)


# Instalation

You need to have nodejs installed. You can donwload it from https://nodejs.org.
Then install all he dependencies from package.json by typing: 

```cmd
npm install 
```


# Run
The default grunt task is also registered to start watching for changes in any sources in styl/ directory. 
So you can just type:
```cmd
grunt
```

Now, when your grunt watch is running, qss/skin.qss will be generated after you save any change in styl/*.styl file

## Demo Application
By running
```cmd
python main.py
```

there will be a simple Qt window with full of Qt widgets opened for you. The purpose of this app is the live reload of qss/skin.qss,
which will show you the currently editing skin on the fly. Feel free to override the test_window.py or create whatever widgets you 
want to do styling for.

Happy coding! ;)