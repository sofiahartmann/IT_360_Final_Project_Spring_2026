from PIL import Image
from PIL.ExifTags import TAGS
import os
import csv
import hashlib
from datetime import datetime
from collections import Counter

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
    except:
        return "ERROR"


def get_file_metadata(file_path):
    try:
        stats = os.stat(file_path)
        created = datetime.fromtimestamp(stats.st_ctime)
        modified = datetime.fromtimestamp(stats.st_mtime)
        size = stats.st_size
        return created, modified, size
    except:
        return None, None, None


def get_image_metadata(file_path):
    metadata = {}
    try:
        image = Image.open(file_path)
        exif_data = image._getexif()

        if exif_data:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                metadata[tag_name] = value
    except:
        pass

    return metadata


# ---------- AI / Pattern Analysis ----------

def ai_assisted_analysis(file_records):
    hash_counter = Counter()
    timestamp_counter = Counter()
    results = {}

    # Aggregate
    for r in file_records:
        hash_counter[r["hash"]] += 1
        timestamp_counter[str(r["modified"])] += 1

    # Per file analysis
    for r in file_records:
        flags = []

        created = r["created"]
        modified = r["modified"]
        file_hash = r["hash"]
        path = r["path"]
        exif_time = r["exif_time"]

        if created and modified and modified < created:
            flags.append("Modified before created")

        if modified and modified > datetime.now():
            flags.append("Future timestamp detected")

        if created and modified and abs((modified - created).days) > 365:
            flags.append("Large time gap")

        if modified and modified.hour < 5:
            flags.append("Unusual time (early morning)")

        if hash_counter[file_hash] > 1:
            flags.append("Duplicate file detected")

        if timestamp_counter[str(modified)] > 5:
            flags.append("Batch modification detected")

        if exif_time:
            try:
                exif_dt = datetime.strptime(exif_time, "%Y:%m:%d %H:%M:%S")
                if created and abs((exif_dt - created).days) > 30:
                    flags.append("EXIF mismatch")
            except:
                flags.append("Bad EXIF format")

        results[path] = " | ".join(flags) if flags else "NORMAL"

    return results


# ---------- Main Scan Function ----------

def scan_directory(directory):
    file_records = []

    for root, _, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)

            created, modified, size = get_file_metadata(path)
            file_hash = get_file_hash(path)

            exif_time = ""

            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                img_meta = get_image_metadata(path)
                exif_time = img_meta.get("DateTime", "")

            file_records.append({
                "name": file,
                "path": path,
                "size": size,
                "created": created,
                "modified": modified,
                "hash": file_hash,
                "exif_time": exif_time
            })

    ai_results = ai_assisted_analysis(file_records)

    output = []
    for r in file_records:
        output.append([
            r["name"],
            r["path"],
            r["size"],
            r["created"],
            r["modified"],
            r["hash"],
            ai_results.get(r["path"], "NORMAL"),
            f"EXIF_DateTime: {r['exif_time']}" if r["exif_time"] else ""
        ])

    return output


# ---------- Save CSV ----------

def save_to_csv(data):
    headers = [
        "File Name",
        "Path",
        "Size",
        "Created Time",
        "Modified Time",
        "SHA256 Hash",
        "Anomaly Report",
        "Extra Metadata"
    ]

    with open(OUTPUT_FILE, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)


# ---------- Main ----------

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
