# Digital Forensics Metadata Tool
### IT360 Final Project — Spring 2026
**Illinois State University**

A Python centered digital forensics tool that scans a directory of evidence files, automatically extracts file system and embedded metadata, and uses AI analysis to detect anomalies and support timeline reconstructions. 

---

## Demo Video

REPLACEEEEE

---

## Project Overview

This tool is designed to assist digital forensic investigators by automating the collection and analysis of file metadata. Instead of manually inspecting files one by one, investigators can point this tool at a folder of evidence files and instantly receive a structured report. This project is expected to save time and aid investigators in the long run. 

The tool will:
- Recursively scan a directory and process every file inside it
- Extract file system metadata. 
- Extract embedded metadata from images, PDFs, and documents. 
- Use AI-assisted logic to flag timestamp inconsistencies and suspicious file patterns.
- Export all collected data to output.csv for easy review and sorting.

Supported Operating Systems: macOS, Linux, Windows

---

## Project Structure (For the Github) 

```
IT_360_Final_Project_Spring_2026/
|-- src/
|   |-- main.py
|   |-- module1.py
|   |-- (other source code files)
|-- docs/
|   |-- final_report.pdf
|   |-- (any other supporting documents or images)
|-- data/
|   |-- sample_evidence.dd
|   |-- (any sample files needed to run the demo)
|-- .gitignore
|-- LICENSE
|-- README.md
|-- requirements.txt
```

---

## Prerequisites

Before running the tool, make sure you have the following installed:

- Python 3.8 or higher
  - Check your version: `python3 --version`
  - Download from: https://www.python.org/downloads/
- pip (Python's package manager — usually included with Python)
  - Check your version: `pip3 --version`
- The repository cloned or downloaded to your machine

---

## Setup Instructions

### macOS Setup

1. Open Terminal
   - Press Command + Space, type Terminal, and hit Enter

2. Navigate to your project folder:
   ```bash
   cd ~/Desktop/IT_360_Final_Project_Spring_2026
   ```

3. Install dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```

4. Run the tool:
   ```bash
   python3 src/main.py
   ```

5. When prompted, enter the folder path:
   ```
   data
   ```

6. The tool will generate output.csv in your project folder. Open it with any spreadsheet application such as Excel, Google Sheets, or Numbers.

---

### Ubuntu / Linux Setup (Proxmox)

1. Open Terminal

2. Navigate to your project folder:
   ```bash
   cd ~/Desktop/IT_360_Final_Project_Spring_2026
   ```

3. Install pip (if needed):
   ```bash
   sudo apt update
   sudo apt install python3-pip -y
   ```

4. Set up Python environment:
   ```bash
   python3 -m venv venv
   ```

5. Activate it:
   ```bash
   source venv/bin/activate
   ```

6. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

7. Run the tool:
   ```bash
   python src/main.py
   ```

8. When prompted, enter the folder path:
   ```
   data
   ```

9. After it runs, type:
   ```bash
   ls
   ```

10. The tool generates a file named output.csv. Open it by entering:
    ```bash
    xdg-open output.csv
    ```

---

## Output

The tool generates a file named output.csv in your project folder after each run.

| Field | Description |
|-------|-------------|
| File Name | Name of the scanned file |
| File Path | Full path to the file on your system |
| File Size | Size of the file in bytes |
| Created Timestamp | When the file was originally created |
| Modified Timestamp | When the file was last modified |
| SHA256 Hash | Unique cryptographic fingerprint of the file |
| Anomaly Detection Result | AI flag for suspicious patterns or timestamp issues |
| Extra Metadata (EXIF) | Embedded metadata such as camera info, GPS, author, etc. |

---

## AI-Assisted Anomaly Detection

This tool uses AI-assisted logic to help investigators identify suspicious file activity. The AI component analyzes the extracted metadata and flags:

- Timestamp inconsistencies — Files where the modified date is earlier than the created date, or where timestamps seem out of place
- Unusual file activity — Files that were accessed or changed outside of normal patterns
- Suspicious patterns — Repeated hashes (duplicate files), unexpected file types, or metadata mismatches

Results appear in the Anomaly Detection Result column of the CSV output. Flagged files are not automatically evidence of wrongdoing — they are starting points for further human investigation.

---

## Troubleshooting

**python3: command not found**
> Python is not installed or not configured correctly. Download and install it from https://www.python.org/downloads/

**pip: command not found or pip3: command not found (Linux)**
> Run the following to install pip:
> ```bash
> sudo apt update && sudo apt install python3-pip -y
> ```

**ModuleNotFoundError: No module named '...'**
> You likely skipped the install step. Run the following and try again:
> ```bash
> pip install -r requirements.txt
> ```

**No such file or directory: 'data'**
> Make sure your evidence files are placed inside the data/ folder in the project directory before running the tool.

**output.csv is empty or missing**
> The data/ folder may be empty or contain unsupported file types. Make sure you have image, PDF, or document files inside it before running.

**Permission denied**
> Try running the command with sudo in front, or check that you have read access to the files in your data/ folder.

---

## Known Limitations

- Supports macOS and Linux only (Proxmox Ubuntu was used for our Linux demo)
- EXIF metadata extraction is most reliable for JPEG images — other file types may return limited embedded metadata
- The AI anomaly detection uses logic and may produce false positives — all flagged results should be reviewed by a human investigator and not be relied on AI. 
- Very large directories may take longer to process. 

---

## Contributors

| Name | 
|------|
| Sophia Criollo |
| Sarah Beyer | 
| Sofia Hartmann | 

---

## Course Info:

**Course** IT360
---

**Semester** Spring 2026
---
**Institution** Illinois State University
---
