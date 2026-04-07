import os

def get_files(directory):
    files = []
    for root, dirs, filenames in os.walk(directory):
        for f in filenames:
            files.append(os.path.join(root, f))
    return files

folder_path = input("Enter the path to the evidence folder: ")
all_files = get_files(folder_path)

print(f"Found {len(all_files)} files:")
for file in all_files:
    print(file)
