# IT_360_Final_Project_Spring_2026

## Team Members
- Sophia Criollo
- Sarah Beyer
- Sofia Hartmann

## Project Idea
This project involves developing a Python based digital forensics tool that scans a directory of evidence files and automatically extracts file system and embedded metadata. The tool outputs the collected metadata in a structured format to assist investigators with timeline reconstruction and evidence analysis. A python based code will allow our tool to be used on Windows, Linux, and MacOS. Availibilty is significant to our idea of success with our forensics tool. 
### Target Selection:
The tool targets local file systems or a specified directory containing digital evidence files collected during an investigation. No matter the OS that the tool is being ran on, file systems can be ran through with the choice of the tool being python based. 
### Artifact Selection:
The tool focuses on extracting file system metadata and embedded metadata from common file types such as images, PDFs, and document files.
### Implementation Language:
The tool is built as a Python script that runs from the terminal. The user starts the program by providing the path to a folder containing evidence files. Python is responsible for controlling the entire workflow. Once the tool starts, Python recursively walks through the provided directory and identifies every file inside it. This allows the tool to automatically process large collections of files without manual selection. At this stage, the tool identifies file paths, ignores folders, prepares each file for analysis.
### Output Format:
The extracted metadata will be exported in CSV format for easy analysis and sorting. The tool will asssist with conversion to a CSV format based on the specific operating system that the tool is ran on. 
