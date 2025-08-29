# AI Security Projects Repository  
#### Updated 06/15/2025 📅   
[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-%E2%9D%A4-red?logo=GitHub&style=for-the-badge)](https://github.com/sponsors/ThiagoMaria-SecurityIT)   

### Welcome to my collection of AI-powered security solutions!  

This collection is a selection of AI-driven solutions I developed for cybersecurity and security intelligence applications, among other use cases. It features AI agents, API integrations, and customizable models designed for seamless compatibility with modern threat management systems.

These projects demonstrate the integration of artificial intelligence with cybersecurity, offering capabilities such as real-time threat detection and advanced analytical tools to strengthen security infrastructure.

This portfolio demonstrates my proven ability and expertise to deliver AI solutions—from design and development to practical real-world implementation.

>[!TIP]  
>**Live Demos Available**  
>Several projects are hosted online—click the badge below to explore them:  
>[![Hugging Face](https://img.shields.io/badge/🤗_HuggingFace-View_Projects-blue)](https://huggingface.co/ThiSecur)  
>  
>**Note for project "E. 🕵️ Security Image & Video Analyzer"**  
>This Python-based solution requires a compatible AI model. Download it here:  
>[Download Model](https://huggingface.co/spaces/ThiSecur/imagedtection-demo/blob/main/model.pt)  
>After downloading, rename the file to `yolo11x.pt` for seamless integration.  

## 📋 Index 🕵️

1. [🌟 Featured Projects](#1--featured-projects)  
A. [🔒 Advanced Threat Video Analyzer](#a-advanced-threat-video-analyzer----will-be-released-soon---updated-15062025)   
B. [📋 AI Compliance Visual Inspector](#b-ai-compliance-visual-inspector----lightweight-object-detection)  
C. [🤖 Security AI Command Center](#c-security-ai-agent-%EF%B8%8F)   
D. [🛠️ Multi-Tool AI Assistant](#d-multi-tool-ai-assistant---%EF%B8%8F-live)  
E. [🕵️ Security Image & Video Analyzer ](#e-security-image--video-analyzer---%EF%B8%8F-python--ttk)  
F. [🐉 Chinese Website Translator - Chrome AI API Extension](chrome_extension_chinese_translator_web)  
G. [📚 Person and Object Detection](#g-person--object-detection-ai-) 
7. [🚀 Getting Started](#%EF%B8%8F-getting-started)     
8. [📂 Repository Structure](#-repository-structure)  
9. [🤝 Contribution & Feedback](#-contribution--feedback)  

---

## 1. 🌟 Featured Projects

### A. Advanced Threat Video Analyzer - 🔒 Will be released soon - Updated: 15/06/2025
[![Status](https://img.shields.io/badge/Status-PrivateDevelopment-red)](https://huggingface.co/spaces/ThiSecur/Image-and-Video-detector)

> 🚧 Expected Release: Q4 2025  
> Next-generation security vision system featuring:
> - Real-time anomaly detection
> - Object, animals and person detection
> - Behavioral pattern analysis
> - Multi-camera threat correlation

*Note: Repository currently contains placeholder documentation*

---

### B. AI Compliance Visual Inspector - 📋 Lightweight object detection
[![Live Demo](https://img.shields.io/badge/🤗-Try_Prototype-blue)](https://huggingface.co/spaces/ThiSecur/Security-AI-Agent-Vision)   
[Try Prototype - Click here](https://huggingface.co/spaces/ThiSecur/Security-AI-Agent-Vision)     


<img width="1542" height="768" alt="image" src="https://github.com/user-attachments/assets/750c74f1-08ee-4c7a-addf-8ff2ff56d9bb" />




**A Vision AI Agent live for security cameras to:**  

- Policy violation detection:
  - Unattended devices (phones, laptops)
  - Clean-desk violations
   - Employees/Visitors without badges
   - Paper, pen, pencil, unathourized devices at production
   - Open or damaged doors/windows
   - Any other clean desk policy your company have
     
*This application adds that context by:*  

- Framing the tool for security and compliance use cases (e.g., detecting unattended devices, clean-desk issues).

- Providing a confidence threshold to help filter out uncertain results, which is critical for making informed decisions.

**_The interpretation of the AI's output is left to the human user_**. For example, if the AI identifies a laptop, monitor, and keyboard on a desk, the user must decide if this scene violates a specific clean-desk policy. This tool acts as a powerful assistant to flag potential issues, not as an autonomous decision-maker.  

>[!Important]  
>- This tool is a prototype and demonstration. It is not a certified compliance auditing tool.  
>- The AI can and will make mistakes—it might miss objects (false negatives) or misidentify (like the example image above that it detected a notebook as a "desktop computer") them (false positives).  
>- Always have a human expert review and validate any findings before making any compliance or security-related decisions.
>- Do not rely solely on this tool's output.  
  
---

### C. Security AI Agent 🛡️   
[![Live Demo](https://img.shields.io/badge/🤗-Try_Beta-blue)](https://huggingface.co/spaces/ThiSecur/AI-Security-Agent)      
Click to test online: [Click Here](https://huggingface.co/spaces/ThiSecur/AI-Security-Agent)      

<img width="1542" height="685" alt="image" src="https://github.com/user-attachments/assets/5e8b3049-9fee-48ff-a18f-c66e28872848" />   

An intelligent security app that uses computer vision to automatically detect and log physical security incidents (the incident log is not implemented yet), with an AI-powered advisor(the advisor will be implemented) to explain the risks based on ISO 27001 principles.  
The live version on Hugging Face is a lightweight demo trained on COCO128 (a general-purpose dataset), while the final version could be a more advanced system trained on security-specific data for real-world threat detection.  

Key Features:
- Real-Time Object Detection: Identifies objects in images/video (e.g., "person," "laptop").  
- Security-Focused: Optimized for Incident Log (e.g., intrusions, unattended items).  
- User-Friendly Interface: Simple upload/click-to-run design.  

**Current Limitations (for the demo):**  
- Training Data: This demo runs on a general-purpose dataset (COCO128), so it may not catch security-specific threats as accurately as our full version (trained on millions of security-optimized images).  
- Video Support: The live video feature isn’t enabled at the Hugging Face demo —but check out my other AI models for real-time object detection in videos and security cameras!  

Interested in the full capabilities? Contact me for details.  

---
 
### D. Multi-Tool AI Assistant - 🛠️ Live 
A Template from Hugging Face Agent Course  
[![Live Demo](https://img.shields.io/badge/🤗-Try_Now-success)](https://huggingface.co/spaces/ThiSecur/First_agent_template)


**Core Capabilities:**
- Time zone conversion engine
- Real-time weather lookups
- Unit conversion system
- Intelligent web search
- Dynamic image generation
- Python code execution

**Example Use Cases:**
```python
"What time is 3pm EST in Tokyo?"
"Show weather in São Paulo"
"Convert 50 miles to kilometers"
"Generate image of secure server room"
```

**Technical Highlights:**
- Qwen2.5-Coder-32B model backbone
- Multi-step reasoning architecture
- Tool chaining capabilities
- Hugging Face optimized deployment  
---  

### E. Security Image & Video Analyzer - 🕵️ Python + TTK    

[![Security Image Analyzer](https://img.shields.io/badge/🔍_Security_Image_Analyzer-Python-4B8BBE?style=for-the-badge&logo=python&logoColor=white&labelColor=1F2430)](https://github.com/ThiagoMaria-SecurityIT/AI-showcase/tree/main/security-image-analyzer)  

A Python-based tool for automated image and video analysis using advanced object detection.  
Designed for security professionals to enhance incident investigation, forensic analysis, and threat detection workflows.  
> [!IMPORTANT]     
> You need a pre-trained model in the same folder of the project to run this code.

---  

### F. Chinese Website Translator - Chrome Extension - 🐉
[![Local Project](https://img.shields.io/badge/Get_The_Code_Here-🐉Python-red)](https://github.com/ThiagoMaria-SecurityIT/AI-showcase/blob/main/chrome_extension_chinese_translator_web/README.md)  

A powerful Chrome AI API browser extension that translates Chinese websites (both simplified and traditional) into English (US) with a stunning dark, futuristic interface design.  

 **Features:**  
 **🌟 Core Functionality**  
- **Dual Translation APIs**: Uses Chrome's built-in **AI** translator with Google Translate fallback  
- **Full Page Translation**: Instantly translate entire Chinese web pages to English  
- **Hover Translation**: Real-time translation tooltips when hovering over Chinese text  
- **Language Detection**: Automatically detects simplified vs traditional Chinese
  
---

### **G. Person & Object Detection AI** 📚  
[![Live Demo](https://img.shields.io/badge/🤗-Try_It_Live-success)](https://huggingface.co/spaces/ThiSecur/imagedtection-demo)  

**What it does:**  
- **Smart Detection**: Identifies people, animals, and everyday objects in images.  
- **Visual Highlights**: 🟨 Draws precise bounding boxes 🟩 around detected targets 🟥—so you *see* exactly what the AI found.  
- **Powered by YOLOv11**: Trained on COCO128 for reliable, real-world performance.  

**Perfect for**: Security checks, wildlife monitoring, retail inventory, or just exploring AI vision!  

🚀 **Try the demo now—upload any image and watch the AI in action!**  

---


## 🛠️ Getting Started

1. For live demos:
   - Click the demo badges above
   - Allow 20-30 seconds for Hugging Face to load
   - Interact with the interfaces

2. For private under development projects:
   - Check back for Q3 2025 release
   - Contact for collaboration opportunities

## 📂 Repository Structure
```
AI-Security-Projects/
├── README.md                                 # Project documentation
├── security-image-analyzer                   # Has 2 images, its a simple AI image detector made with python
└── chrome_extension_chinese_translator_web   # Chrome AI API browser extension
```

## 🤝 Contribution & Feedback
This repository demonstrates practical AI security implementations. Suggestions and use case ideas are welcome!  
[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-%E2%9D%A4-red?logo=GitHub&style=for-the-badge)](https://github.com/sponsors/ThiagoMaria-SecurityIT)  
[![Hugging Face](https://img.shields.io/badge/🤗-All_Projects-blue)](https://huggingface.co/ThiSecur)   

Let's chat:  
💼 LinkedIn: https://www.linkedin.com/in/thiago-cequeira-99202239/  
🧑‍💻 GitHub: https://github.com/ThiagoMaria-SecurityIT/  
🤗 Hugging Face: https://huggingface.co/ThiSecur
