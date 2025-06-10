# Security Image & Video Analysis Tool

![Object Detection Example](https://via.placeholder.com/800x400?text=Security+Detection+Demo)

A Python-based tool for automated image and video analysis using advanced object detection. Designed for security professionals to enhance incident investigation, forensic analysis, and threat detection workflows.

## Key Features

- **Automated Detection**: Identify objects in images/videos without manual review
- **Forensic Analysis**: Quickly scan evidence for relevant objects/patterns
- **Incident Response**: Process security footage faster than human review
- **Custom Filtering**: Focus on specific object classes (people, vehicles, devices)
- **Scalable**: Process single images or hours of video footage

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/security-image-analyzer.git
   cd security-image-analyzer
   ```

2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Security Use Cases

### Incident Investigation
- Automatically flag frames with objects in security footage
- Track movement patterns of persons-of-interest across multiple cameras

### Forensic Analysis
- Bulk-process scene photos for evidence cataloging
- Detect "not so obvious" objects in photos

### Threat Detection
- Monitor live feeds for unauthorized objects in secure areas
- Identify left-behind items in sensitive locations

## Usage Guide

1. **Image Analysis**:
   - Select "Image Detection" tab
   - Choose image file (JPG/PNG)
   - Filter results by object type/confidence

2. **Video Processing**:
   - Select "Video Detection" tab
   - Load video file (MP4/MOV)
   - Play/pause to analyze frames

## Security Best Practices

- **Data Handling**: All processing occurs locally - no images/videos are uploaded
- **Chain of Custody**: Results include timestamps for evidentiary purposes
- **False Positive Management**: Adjust confidence thresholds to balance sensitivity/specificity
- **Audit Trail**: Detection logs are automatically generated

## Model Information

This tool utilizes the YOLOv11 object detection model through Ultralytics' implementation. The model provides real-time detection capabilities while maintaining high accuracy for security-relevant objects.

## License

This project is released under AGPL-3.0 license as required by Ultralytics. See [LICENSE.txt](LICENSE.txt) for complete terms.

---

*For security professionals by security professional Thiago de Maria - enhancing human analysis with AI assistance*
* _Thiago de Maria_  
🤵🏽[in/thiago-cequeira-99202239](https://www.linkedin.com/in/thiago-cequeira-99202239/) \
🤗https://huggingface.co/settings/profile
