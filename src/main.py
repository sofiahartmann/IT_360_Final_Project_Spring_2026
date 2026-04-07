from PIL import Image
from PIL.ExifTags import TAGS
import os
import csv
import hashlib
from datetime import datetime

OUTPUT_FILE = "output.csv"

def get_file_hash(file_path):
    try:
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        return "ERROR"

def get_file_metadata(file_path):
    try:
        stats = os.stat(file_path)

        created = datetime.fromtimestamp(stats.st_ctime)
        modified = datetime.fromtimestamp(stats.st_mtime)
        size = stats.st_size

        return created, modified, size
    except Exception as e:
        return None, None, None

def detect_anomaly(created, modified):
    try:
        if created is None or modified is None:
            return "UNKNOWN"

        if modified < created:
            return "MODIFIED_BEFORE_CREATED"

        if created > datetime.now() or modified > datetime.now():
            return "FUTURE_TIMESTAMP"

        return "NORMAL"
    except:
        return "UNKNOWN"

def scan_directory(directory):
    results = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)

            created, modified, size = get_file_metadata(file_path)
            file_hash = get_file_hash(file_path)
            anomaly = detect_anomaly(created, modified)

extra_metadata = ""

# Check if file is an image
if file.lower().endswith((".jpg", ".jpeg", ".png")):
    img_meta = get_image_metadata(file_path)

    if "DateTime" in img_meta:
        extra_metadata = f"EXIF_DateTime: {img_meta['DateTime']}"

results.append([
    file,
    file_path,
    size,
    created,
    modified,
    file_hash,
    anomaly,
    extra_metadata
])
            ])

    return results

def save_to_csv(data):
   headers = [
    "File Name",
    "Path",
    "Size",
    "Created Time",
    "Modified Time",
    "SHA256 Hash",
    "Anomaly",
    "Extra Metadata"
]
    with open(OUTPUT_FILE, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)

def main():
    directory = input("Enter path to evidence folder: ")

    if not os.path.exists(directory):
        print("Invalid directory.")
        return

    print("Scanning directory...")
    data = scan_directory(directory)

    save_to_csv(data)

    print(f"Scan complete. Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
    
def get_image_metadata(file_path):
    metadata = {}

    try:
        image = Image.open(file_path)
        exif_data = image._getexif()

        if exif_data is not None:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                metadata[tag_name] = value

        return metadata
    except:
        return {}

