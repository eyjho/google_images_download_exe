# Product Name

This is a batch downloader for Google images as a Windows executable for anyone who does not want or cannot run a Python script.

[![NPM Version][npm-image]][npm-url]
[![Build Status][travis-image]][travis-url]
[![Downloads Stats][npm-downloads]][npm-url]

This executable provides simple and fast way to search and download Googe images in a simple GUI for users not using Python. The download functionalities come from google-images-download by hardikvasa (https://github.com/hardikvasa/google-images-download/), and this project adds a simple Tkinter GUI and has packaged in PyInstaller executable.

Start by entering your search terms (keywords, colour, specific site, # limit) into the entry boxes in the interface, then click "Search". The program will search Google, automatically download thumbnails (quantity up to the limit), and display the thumbnails in the interface. The images can be downloaded either altogether with the "Download all" button or individually by clicking on the image (work in progress).

![](interface.png)

## Installation


Windows:

Download Semiotics.Engine.v[x.y.z].zip from https://github.com/eyjho/google_images_download_exe/releases. Extract into your working directory, and run using the shortcut. No installation required. All images will be downloaded into the \Pictures directory by default, which will be in the same directory as the shortcut, or the directory above the .exe file.


OS X & Linux:

TBC

## Usage example

A few motivating and useful examples of how your product can be used. Spice this up with code blocks and potentially more screenshots.

_For more examples and usage, please refer to the [Wiki][wiki]._

## Release History

* 0.2.1
    * CHANGE: Update docs (module code remains unchanged)
* 0.2.0
    * CHANGE: Remove `setDefaultXYZ()`
    * ADD: Add `init()`
* 0.1.1
    * FIX: Crash when calling `baz()` (Thanks @GenerousContributorName!)
* 0.1.0
    * The first proper release
    * CHANGE: Rename `foo()` to `bar()`
* 0.0.1
    * Work in progress

## Meta

Eugene (https://github.com/eyjho)

Distributed under the MIT license. See ``LICENSE`` for more information.

https://github.com/eyjho/google_images_download_exe

<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/yourname/yourproject/wiki
