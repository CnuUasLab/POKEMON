'use strict';

// Sample code

var electron = require('electron');
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
	mainWindow.loadURL("http://localhost:3333");
	mainWindow.on('closed', () => {
		mainWindow = null;
	});
});



