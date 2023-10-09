import os
import hashlib


def hash_file(file_path):
    """Calculate SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as file:
        while True:
            data = file.read(65536)  # Read in 64k chunks
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()


def find_duplicate_files(directory):
    """Find duplicate files recursively in a directory."""
    duplicates = {}
    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            # if not "politik" in filename.lower():
            #     continue
            file_path = os.path.join(foldername, filename)
            if ".jpg" in file_path or "jpeg" in file_path:
                continue
            # print(file_path)
            file_hash = hash_file(file_path)
            # print(file_hash)
            if file_hash in duplicates:
                duplicates[file_hash].append(file_path)
            else:
                duplicates[file_hash] = [file_path]
    return {key: value for key, value in duplicates.items() if len(value) > 1}


# Example usage
if __name__ == "__main__":
    directory = "/home/cruz/mnt/synology/music/"
    duplicate_files = find_duplicate_files(directory)

    if duplicate_files:
        print("Duplicate files found:")
        for hash_value, file_paths in duplicate_files.items():
            print(f"Hash: {hash_value}")
            for file_path in file_paths:
                print(f"- {file_path}")

        with open("duplicates.txt", "w") as f:
            for hash_value, file_paths in duplicate_files.items():
                for file_path in file_paths:
                    f.write(f"- {file_path}\n")
    else:
        print("No duplicate files found.")
