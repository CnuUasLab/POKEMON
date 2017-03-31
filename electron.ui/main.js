'use strict';

// Sample code

var electron = require('electron');
var path = require('path');
var url = require('url');



var app = electron.app;
var browserWindow = electron.BrowserWindow;

var mainWindow = null;

//when we close.
app.on('window-on-closed', () => {
	if (process.platfor != 'darwin') {
		app.quit();
	}
});

// Create Browser window
app.on('ready', () => {
	mainWindow = new browserWindow({width: 1200, height: 800});
	mainWindow.loadURL(url.format({
		pathname: path.join(__dirname, 'views/index.html'),
		protocol: 'file:',
		slashes: true
	}));
	mainWindow.on('closed', () => {
		mainWindow = null;
	});
});



