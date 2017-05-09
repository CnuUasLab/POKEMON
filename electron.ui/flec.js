'use strict';

// Importing required dependeincies.
var electron 		= require('electron');
var path 		= require('path');
var url 		= require('url');
var http 		= require('http');

// Initializing Application
var app 		= electron.app;
var browserWindow 	= electron.BrowserWindow;

// Initializing windows
var mapWindow 		= null;
var consoleWindow 	= null;
var statusWindow 	= null;

//when we close.
app.on('window-on-closed', () => {
	if (process.platform != 'darwin') {
		app.quit();
	}
});


// Create Browser window
app.on('ready', () => {
	mapWindow = new browserWindow({width: 1200, height: 800});
	statusWindow = new browserWindow({width: 100, height: 300});
	consoleWindow = new browserWindow(width: 1200, height: 90);

	mapWindow.loadURL(url.format({
		pathname: path.join(__dirname, 'views/index.html'),
		protocol: 'file:',
		slashes: true
	}));

	statusWindow.on('closed', () => {
		statusWindow = null;
	});

	consoleWindow.on('closed', () => {
		consoleWindow = null;
	});

	mapWindow.on('closed', () => {
		mainWindow = null;
	});
});
