const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let djangoProcess;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
	icon: path.join(__dirname, 'historia/static/eye.ico'),
    webPreferences: {
      nodeIntegration: false, // Security best practice
    },
  });
  
  mainWindow.setMenuBarVisibility(false);

  // Load the Django URL
  setTimeout(() => {
      mainWindow.loadURL('http://127.0.0.1:8000');
  }, 2000); // Wait 2s for Django to boot

  mainWindow.on('closed', function () {
    mainWindow = null;
  });
}

function startDjango() {
  //djangoProcess = spawn('manage.exe', ['runserver', '0.0.0.0:8000', '--noreload'], {
  djangoProcess = spawn('python', ['manage.py', 'runserver', '0.0.0.0:8000', '--noreload'], {
    cd: path.join(__dirname, '.'),
    // THIS LINE HIDES THE PYTHON CONSOLE WINDOW
    windowsHide: true 
  });

  djangoProcess.stdout.on('data', (data) => {
    console.log(`Django: ${data}`);
  });

  djangoProcess.stderr.on('data', (data) => {
    console.error(`Django Error: ${data}`);
  });
}

function killDjango() {
    if (djangoProcess) {
        spawn("taskkill", ["/pid", djangoProcess.pid, '/f', '/t']);
        djangoProcess = null;
    }
}

app.on('ready', () => {
  startDjango();
  createWindow();
});

// QUIT HANDLING: Stop Django when Electron closes
app.on('window-all-closed', () => {
  killDjango();
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('will-quit', () => {
    killDjango();
});