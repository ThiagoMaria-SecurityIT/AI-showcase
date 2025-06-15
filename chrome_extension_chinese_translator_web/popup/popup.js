// Enhanced popup.js with futuristic functionality

let translatedCount = 0;
let isHoverEnabled = true;

// DOM elements
const translateButton = document.getElementById('translateButton');
const hoverToggle = document.getElementById('hoverToggle');
const sourceLanguage = document.getElementById('sourceLanguage');
const statusIndicator = document.getElementById('statusIndicator');
const translatedCountElement = document.getElementById('translatedCount');
const detectedLanguageElement = document.getElementById('detectedLanguage');

// Initialize popup
document.addEventListener('DOMContentLoaded', () => {
  loadSettings();
  updateUI();
});

// Load saved settings
function loadSettings() {
  chrome.storage.sync.get(['hoverEnabled', 'sourceLanguage', 'translatedCount'], (result) => {
    isHoverEnabled = result.hoverEnabled !== false; // default to true
    hoverToggle.checked = isHoverEnabled;
    sourceLanguage.value = result.sourceLanguage || 'zh';
    translatedCount = result.translatedCount || 0;
    translatedCountElement.textContent = translatedCount;
  });
}

// Save settings
function saveSettings() {
  chrome.storage.sync.set({
    hoverEnabled: isHoverEnabled,
    sourceLanguage: sourceLanguage.value,
    translatedCount: translatedCount
  });
}

// Update UI status
function updateUI() {
  const pulse = statusIndicator.querySelector('.pulse');
  const statusText = statusIndicator.querySelector('span');
  
  if (isHoverEnabled) {
    pulse.style.background = '#00ff88';
    statusText.textContent = 'READY';
    statusText.style.color = '#00ff88';
  } else {
    pulse.style.background = '#ff6b6b';
    statusText.textContent = 'HOVER OFF';
    statusText.style.color = '#ff6b6b';
  }
}

// Animate button during translation
function animateTranslateButton(isTranslating) {
  const btnText = translateButton.querySelector('.btn-text');
  
  if (isTranslating) {
    translateButton.classList.add('loading');
    btnText.textContent = 'TRANSLATING...';
    translateButton.disabled = true;
  } else {
    translateButton.classList.remove('loading');
    btnText.textContent = 'TRANSLATE PAGE';
    translateButton.disabled = false;
  }
}

// Detect language from current tab
async function detectLanguage() {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      function: () => {
        const text = document.body.textContent.slice(0, 100);
        const isSimplified = /[\u4e00-\u9fff]/.test(text);
        const isTraditional = /[\u3400-\u4dbf\uf900-\ufaff]/.test(text);
        
        if (isSimplified && isTraditional) return 'zh-mixed';
        if (isSimplified) return 'zh-cn';
        if (isTraditional) return 'zh-tw';
        return 'unknown';
      }
    }, (results) => {
      if (results && results[0]) {
        const detected = results[0].result;
        let displayText = 'Unknown';
        
        switch (detected) {
          case 'zh-cn': displayText = 'Simplified'; break;
          case 'zh-tw': displayText = 'Traditional'; break;
          case 'zh-mixed': displayText = 'Mixed'; break;
        }
        
        detectedLanguageElement.textContent = displayText;
      }
    });
  } catch (error) {
    console.error('Language detection error:', error);
  }
}

// Event listeners
translateButton.addEventListener('click', async () => {
  animateTranslateButton(true);
  
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    chrome.tabs.sendMessage(tab.id, { action: 'translate' }, (response) => {
      if (response) {
        translatedCount++;
        translatedCountElement.textContent = translatedCount;
        saveSettings();
        
        // Add success animation
        translateButton.style.borderColor = '#00ff88';
        translateButton.style.color = '#00ff88';
        
        setTimeout(() => {
          translateButton.style.borderColor = '#00d4ff';
          translateButton.style.color = '#00d4ff';
        }, 1000);
      }
      
      animateTranslateButton(false);
    });
  } catch (error) {
    console.error('Translation error:', error);
    animateTranslateButton(false);
  }
});

hoverToggle.addEventListener('change', () => {
  isHoverEnabled = hoverToggle.checked;
  updateUI();
  saveSettings();
  
  // Send message to content script
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.tabs.sendMessage(tabs[0].id, { 
      action: isHoverEnabled ? 'enableHover' : 'disableHover' 
    });
  });
});

sourceLanguage.addEventListener('change', () => {
  saveSettings();
  detectLanguage();
});

// Detect language when popup opens
detectLanguage();

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && e.ctrlKey) {
    translateButton.click();
  } else if (e.key === 'h' && e.ctrlKey) {
    hoverToggle.click();
  }
});

// Add visual feedback for interactions
document.querySelectorAll('button, .toggle-label, select').forEach(element => {
  element.addEventListener('mouseenter', () => {
    element.style.transform = 'scale(1.02)';
  });
  
  element.addEventListener('mouseleave', () => {
    element.style.transform = 'scale(1)';
  });
});

