import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));

// Démarrage du serveur Flask
const flaskProcess = spawn('python', ['app.py'], {
  stdio: 'inherit',
  cwd: __dirname
});

// Démarrage du serveur Vite
const viteProcess = spawn('npm', ['run', 'dev'], {
  stdio: 'inherit',
  cwd: __dirname
});

// Gestion de la fermeture propre
process.on('SIGINT', () => {
  flaskProcess.kill();
  viteProcess.kill();
  process.exit();
});