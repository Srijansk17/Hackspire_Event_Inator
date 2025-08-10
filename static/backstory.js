const container = document.getElementById('sceneContainer');
const backstoryImage = document.getElementById('backstoryImage');
const splashCount = 15;
const screenWidth = window.innerWidth;
const screenHeight = window.innerHeight;

for (let i = 0; i < splashCount; i++) {
  const splash = document.createElement('div');
  splash.classList.add('splash');
  const x = Math.random() * (screenWidth - 150);
  const y = Math.random() * (screenHeight - 150);
  splash.style.left = `${x}px`;
  splash.style.top = `${y}px`;
  container.appendChild(splash);
}

// Wait 5 seconds, then fade in the background
setTimeout(() => {
  backstoryImage.style.opacity = 1;
}, 5000);
