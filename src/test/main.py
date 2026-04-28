from collections import Counter
import time
from PIL import Image
from PIL.ExifTags import TAGS
import os
import csv
import hashlib
from datetime import datetime

OUTPUT_FILE = "output.csv"

# ---------- Utility Functions ----------

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

# ---------- Main Scanning Function ----------

def scan_directory(directory):
    file_records = []

    # --------- FIRST PASS: Collect Raw Metadata ---------
    for root, _, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)

            created, modified, size = get_file_metadata(path)
            file_hash = get_file_hash(path)
            exif_time = ""

            if file.lower().endswith((".jpg", ".jpeg")):
                img_meta = get_image_metadata(path)
                if "DateTime" in img_meta:
                    exif_time = img_meta["DateTime"]

            file_records.append({
                "name": file,
                "path": path,
                "size": size,
                "created": created,
                "modified": modified,
                "hash": file_hash,
                "exif_time": exif_time
            })

    # --------- SECOND PASS: AI-Assisted Analysis ---------
    ai_results = ai_assisted_analysis(file_records)

    # --------- FINAL OUTPUT FORMAT ---------
    results = []
    for r in file_records:
        results.append([
            r["name"],
            r["path"],
            r["size"],
            r["created"],
            r["modified"],
            r["hash"],
            ai_results[r["path"]],
            f"EXIF_DateTime: {r['exif_time']}" if r["exif_time"] else ""
        ])

    return results

# ---------- Save Results ----------

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

# ---------- Main Program ----------

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

# ---------- AI Component ----------


def ai_assisted_analysis(file_records):
    """
    Performs pattern-based AI-style forensic analysis across all files.
    """
    hash_counter = Counter()
    timestamp_counter = Counter()
    flagged_results = {}

    # --------- Aggregate Analysis ---------
    for record in file_records:
        file_hash = record["hash"]
        modified = record["modified"]

        hash_counter[file_hash] += 1
        timestamp_counter(str(modified)) += 1

    # --------- Per-File Analysis ---------
    for record in file_records:
        flags = []

        created = record["created"]
        modified = record["modified"]
        file_hash = record["hash"]
        file_path = record["path"]
        size = record["size"]
        exif_time = record["exif_time"]

        # 1. Timestamp inconsistencies
        if modified < created:
            flags.append("Modified earlier than created")

        if modified > datetime.now():
            flags.append("Future timestamp detected")

        if abs((modified - created).days) > 365:
            flags.append("Large creation/modified gap")

        # 2. Unusual activity times (forensic heuristic)
        if modified.hour < 5:
            flags.append("Unusual modification time (early morning)")

        # 3. Duplicate file detection
        if hash_counter[file_hash] > 1:
            flags.append("Duplicate content detected")

        # 4. Bulk timestamp clustering
        if timestamp_counter[str(modified)] > 5:
            flags.append("Batch-modified files detected")

        # 5. EXIF vs filesystem mismatch
        if exif_time:
            try:
                exif_dt = datetime.strptime(exif_time, "%Y:%m:%d %H:%M:%S")
                if abs((exif_dt - created).days) > 30:
                    flags.append("EXIF metadata mismatch")
            except:
                flags.append("Unreadable EXIF timestamp")

        # 6. Unexpected file extensions
        suspicious_ext = (".exe", ".sh", ".bin", ".ps1")
        if file_path.lower().endswith(suspicious_ext):
            flags.append("Unexpected executable file type")

        flagged_results[file_path] = " | ".join(flags) if flags else "NORMAL"

    return flagged_results
