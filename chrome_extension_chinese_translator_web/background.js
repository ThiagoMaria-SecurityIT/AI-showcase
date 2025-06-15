
// background.js

chrome.runtime.onInstalled.addListener(() => {
  console.log("Chinese Website Translator extension installed.");
});

chrome.action.onClicked.addListener((tab) => {
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    files: ["content.js"],
  });
});

