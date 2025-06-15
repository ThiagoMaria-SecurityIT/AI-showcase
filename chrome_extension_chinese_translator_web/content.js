// content.js

// Function to detect Chinese characters (both simplified and traditional)
function isChinese(text) {
  // Unicode ranges for Chinese characters:
  // \u4E00-\u9FFF: CJK Unified Ideographs (most common Chinese characters)
  // \u3400-\u4DBF: CJK Extension A
  // \uF900-\uFAFF: CJK Compatibility Ideographs
  // \u3000-\u303F: CJK Symbols and Punctuation
  return /[\u4E00-\u9FFF\u3400-\u4DBF\uF900-\uFAFF\u3000-\u303F]/.test(text);
}

// Function to translate text using Google Translate API (fallback method)
async function translateWithGoogleAPI(text) {
  try {
    const response = await fetch(`https://translate.googleapis.com/translate_a/single?client=gtx&sl=zh&tl=en&dt=t&q=${encodeURIComponent(text)}`);
    const data = await response.json();
    return data[0][0][0];
  } catch (error) {
    console.error('Google Translate API error:', error);
    return null;
  }
}

// Function to translate text using Chrome's built-in AI API (if available)
async function translateWithChromeAI(text) {
  try {
    if (typeof chrome !== 'undefined' && chrome.ai && chrome.ai.translator) {
      const translator = await chrome.ai.translator.create({
        sourceLanguage: 'zh',
        targetLanguage: 'en'
      });
      return await translator.translate(text);
    }
    return null;
  } catch (error) {
    console.error('Chrome AI translation error:', error);
    return null;
  }
}

// Main translation function with fallback
async function translateText(text) {
  // Try Chrome AI first, then fallback to Google API
  let translatedText = await translateWithChromeAI(text);
  if (!translatedText) {
    translatedText = await translateWithGoogleAPI(text);
  }
  return translatedText;
}

// Function to create translation overlay
function createTranslationOverlay(originalElement, translatedText) {
  const overlay = document.createElement('div');
  overlay.className = 'chinese-translator-overlay';
  overlay.style.cssText = `
    position: absolute;
    background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%);
    color: #00d4ff;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 12px;
    font-family: 'Segoe UI', sans-serif;
    box-shadow: 0 4px 20px rgba(0, 212, 255, 0.3);
    border: 1px solid #00d4ff;
    z-index: 10000;
    max-width: 300px;
    word-wrap: break-word;
    opacity: 0;
    transform: translateY(-10px);
    transition: all 0.3s ease;
    pointer-events: none;
  `;
  overlay.textContent = translatedText;
  
  document.body.appendChild(overlay);
  
  // Position the overlay
  const rect = originalElement.getBoundingClientRect();
  overlay.style.left = rect.left + 'px';
  overlay.style.top = (rect.bottom + window.scrollY + 5) + 'px';
  
  // Animate in
  setTimeout(() => {
    overlay.style.opacity = '1';
    overlay.style.transform = 'translateY(0)';
  }, 10);
  
  return overlay;
}

// Function to handle hover translation
function setupHoverTranslation() {
  let currentOverlay = null;
  let hoverTimeout = null;
  
  document.addEventListener('mouseover', async (e) => {
    const element = e.target;
    const text = element.textContent?.trim();
    
    if (text && isChinese(text) && text.length > 0 && text.length < 200) {
      hoverTimeout = setTimeout(async () => {
        const translatedText = await translateText(text);
        if (translatedText && translatedText !== text) {
          // Remove existing overlay
          if (currentOverlay) {
            currentOverlay.remove();
          }
          
          currentOverlay = createTranslationOverlay(element, translatedText);
        }
      }, 500); // 500ms delay before showing translation
    }
  });
  
  document.addEventListener('mouseout', () => {
    if (hoverTimeout) {
      clearTimeout(hoverTimeout);
      hoverTimeout = null;
    }
    
    if (currentOverlay) {
      currentOverlay.style.opacity = '0';
      currentOverlay.style.transform = 'translateY(-10px)';
      setTimeout(() => {
        if (currentOverlay) {
          currentOverlay.remove();
          currentOverlay = null;
        }
      }, 300);
    }
  });
}

// Function to translate entire page
async function translatePage() {
  const walker = document.createTreeWalker(
    document.body,
    NodeFilter.SHOW_TEXT,
    {
      acceptNode: function(node) {
        // Skip script and style elements
        const parent = node.parentElement;
        if (parent && (parent.tagName === 'SCRIPT' || parent.tagName === 'STYLE')) {
          return NodeFilter.FILTER_REJECT;
        }
        return NodeFilter.FILTER_ACCEPT;
      }
    },
    false
  );
  
  let node;
  const textNodesToTranslate = [];
  
  while ((node = walker.nextNode())) {
    const text = node.nodeValue.trim();
    if (text.length > 0 && isChinese(text)) {
      textNodesToTranslate.push(node);
    }
  }
  
  // Show progress indicator
  const progressIndicator = document.createElement('div');
  progressIndicator.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%);
    color: #00d4ff;
    padding: 15px 20px;
    border-radius: 10px;
    font-family: 'Segoe UI', sans-serif;
    box-shadow: 0 4px 20px rgba(0, 212, 255, 0.3);
    border: 1px solid #00d4ff;
    z-index: 10001;
    font-size: 14px;
  `;
  progressIndicator.textContent = `Translating... 0/${textNodesToTranslate.length}`;
  document.body.appendChild(progressIndicator);
  
  // Translate nodes in batches to avoid overwhelming the API
  const batchSize = 5;
  for (let i = 0; i < textNodesToTranslate.length; i += batchSize) {
    const batch = textNodesToTranslate.slice(i, i + batchSize);
    
    await Promise.all(batch.map(async (textNode, index) => {
      const translatedText = await translateText(textNode.nodeValue);
      if (translatedText) {
        textNode.nodeValue = translatedText;
      }
      
      // Update progress
      progressIndicator.textContent = `Translating... ${i + index + 1}/${textNodesToTranslate.length}`;
    }));
    
    // Small delay between batches
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  
  // Remove progress indicator
  setTimeout(() => {
    progressIndicator.remove();
  }, 2000);
}

// Listen for messages from the popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'translate') {
    translatePage();
    sendResponse({ status: 'Translation initiated' });
  } else if (request.action === 'toggleHover') {
    setupHoverTranslation();
    sendResponse({ status: 'Hover translation enabled' });
  }
});

// Initialize hover translation by default
setupHoverTranslation();


