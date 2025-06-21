# Chinese Website Translator - Chrome Extension 

## Overview  
- A powerful Chrome extension that translates Chinese websites (both simplified and traditional) into English (US) with a stunning dark, futuristic interface design.
- Made with Manus AI Playbook 
- Published at Chrome Web Store at June 17, 2025  
- Link: https://chromewebstore.google.com/detail/chinese-website-translato/oaecicbfmchjhfgleciddmpdigcmdpgb  
---
![image](https://github.com/user-attachments/assets/53a9967f-793c-409e-86ea-fb8ad0b8d8e5)
  


## Features

### 🌟 Core Functionality
- **Full Page Translation**: Instantly translate entire Chinese web pages to English
- **Hover Translation**: Real-time translation tooltips when hovering over Chinese text
- **Language Detection**: Automatically detects simplified vs traditional Chinese
- **Dual Translation APIs**: Uses Chrome's built-in AI translator with Google Translate fallback

### 🎨 Design
- **Dark Futuristic UI**: Cyberpunk-inspired interface with neon accents
- **Smooth Animations**: Fluid transitions and micro-interactions
- **Responsive Design**: Optimized for all screen sizes
- **Visual Feedback**: Real-time status indicators and progress tracking

### ⚙️ Advanced Features
- **Settings Persistence**: Remembers your preferences across sessions
- **Translation Statistics**: Tracks translation count and detected languages
- **Keyboard Shortcuts**: Quick access via Ctrl+Enter and Ctrl+H
- **Batch Processing**: Efficient translation of large amounts of text

## Installation

### Method 1: Developer Mode (Recommended)
1. Download and extract the extension files
2. Open Chrome and navigate to `chrome://extensions/`
3. Enable "Developer mode" in the top-right corner
4. Click "Load unpacked" and select the extension folder
5. The extension icon will appear in your toolbar

### Method 2: Chrome Web Store
*Coming soon - extension will be published to the Chrome Web Store*

## Usage

### Basic Translation
1. Visit any Chinese website
2. Click the extension icon in the toolbar
3. Click "TRANSLATE PAGE" to translate the entire page
4. Use the toggle to enable/disable hover translation

### Hover Translation
- Move your mouse over any Chinese text
- A translation tooltip will appear after 500ms
- The tooltip features the same futuristic design as the main interface

### Settings
- **Source Language**: Choose between auto-detect, simplified, or traditional Chinese
- **Hover Toggle**: Enable/disable hover translation feature
- **Statistics**: View translation count and detected language types

## Technical Details

### Architecture
- **Manifest V3**: Uses the latest Chrome extension standards
- **Content Scripts**: Inject translation functionality into web pages
- **Background Service Worker**: Handles extension lifecycle and messaging
- **Popup Interface**: Provides user controls and settings

### Translation Methods
1. **Chrome AI Translator**: Primary method using browser's built-in AI
2. **Google Translate API**: Fallback method for broader compatibility
3. **Batch Processing**: Optimized for translating large amounts of text

### Performance
- **Efficient DOM Traversal**: Smart text node detection and processing
- **Rate Limiting**: Prevents API overuse with intelligent batching
- **Memory Management**: Optimized for minimal resource usage

## File Structure
```
chrome_extension_translator/
├── manifest.json          # Extension configuration
├── background.js          # Service worker
├── content.js            # Content script for translation
├── popup/
│   ├── popup.html        # Popup interface
│   ├── popup.css         # Futuristic styling
│   └── popup.js          # Popup functionality
├── icons/
│   ├── icon16.png        # 16x16 icon
│   ├── icon48.png        # 48x48 icon
│   └── icon128.png       # 128x128 icon
├── images/
│   ├── iamge1.png
│   ├── image2.png
│   └── screen1.png
└── README.md             # Documentation
```
## About the Author   

**Thiago Maria - From Brazil to the World 🌎**  
*Senior Security Information Professional | Passionate Programmer | AI Developer*

With a professional background in security analysis and a deep passion for programming, I created this Chrome Extension to share some knowledge about AI, Google Web UI, and development practices. Most of my work here in my Github focuses on implementing security-first approaches in AI and developer tools while maintaining usability.

Let's Connect:

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/thiago-cequeira-99202239/)  
[![Hugging Face](https://img.shields.io/badge/🤗Hugging_Face-AI_projects-yellow)](https://huggingface.co/ThiSecur)

 
## Ways to Contribute:   
 Want to see more upgrades? Help me keep it updated!    
 [![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-red)](https://github.com/sponsors/ThiagoMaria-SecurityIT) 
