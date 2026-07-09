const { app, BrowserWindow, globalShortcut, Menu } = require('electron');
const path = require('path');
const { spawn, exec } = require('child_process');

let mainWindow;
const djangoDir = app.isPackaged ? path.join(process.resourcesPath, 'manage') : path.resolve(__dirname, '..');
let djangoProcess;

const icon_path = app.isPackaged ? path.join(process.resourcesPath, 'manage/_internal/historia/static/eye.ico') : path.join(__dirname, '../historia/static/eye.ico');

try { // Load your Django-environ file into process.env to access saved paths
  process.loadEnvFile(path.join(djangoDir, '.env')); 
} catch (err) {
  console.error("Could not load .env file:", err.message);
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1568,
    height: 800,
	icon: icon_path,
    webPreferences: {
      nodeIntegration: false, // Security best practice
    },
  });
  
  mainWindow.setMenuBarVisibility(false);
  mainWindow.setAutoHideMenuBar(true); // Alt key
  console.log('--- App is ready and running! ---');
  
  globalShortcut.register('CommandOrControl+Shift+G', () => {
    mainWindow.isMenuBarVisible() ? mainWindow.setMenuBarVisibility(false) : mainWindow.setMenuBarVisibility(true)
    console.log('--- Shortcut! ---');
  });
  
  globalShortcut.register('CommandOrControl+Shift+E', () => {
    openExplorer(path.join(djangoDir, process.env.BACKUP_LOCATION)); // TODO check if BACKUP_LOCATION is full or relative path
  });

  globalShortcut.register('CommandOrControl+Shift+P', () => {
    launchCmdPython(path.join(djangoDir, "a.py"));
  });

  // Load the Django URL
  setTimeout(() => {
      mainWindow.loadURL('http://127.0.0.1:8000');
  }, 2000); // Wait 2s for Django to boot

  mainWindow.on('closed', function () {
    mainWindow = null;
  });
}

function startDjango() {
  const args = {
		cwd: djangoDir,
		windowsHide: true 
	  }
  if (app.isPackaged) {
	  djangoProcess = spawn('manage.exe', ['runserver', '0.0.0.0:8000', '--noreload'], args);
	} else {
	  djangoProcess = spawn('python', ['manage.py', 'runserver', '0.0.0.0:8000'], args);
	}

  djangoProcess.stderr.on('data', (data) => {
    console.log(`Django: ${data}`);
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


function openExplorer(targetPath) {
  const safePath = path.normalize(targetPath);
  exec(`start "" "${safePath}"`, { shell: true }, (err) => {
    if (err) console.error('Failed to open explorer:', err);
  });
}

function launchCmdPython(scriptPath) {
  const safeScriptPath = path.normalize(scriptPath);
  // Using /k keeps the command prompt window open so you can see errors or output
  const cmdArgs = ['/c', 'start', 'cmd', '/k', `python "${safeScriptPath}"`];
  spawn('cmd.exe', cmdArgs, { shell: true });
}


/*    Open as new window
  const projectDir = path.join(__dirname, '.');
  const commandString = `python manage.py runserver 0.0.0.0:8000 --noreload`;
  const cmdArgs = ['/c', 'start', 'cmd', '/k', commandString];
  const djangoProcess = spawn('cmd.exe', cmdArgs, { 
    shell: true,
    windowsHide: false
  });
*/