import hashlib
import os

def calculate_checksum(file_path):
    sha1_hash = hashlib.sha1()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha1_hash.update(byte_block)
        return sha1_hash.hexdigest()
    except Exception as e:
        return f"Error: {e}"

def main():
    right =0
    wrong =0
    miss =0 
    error_files=[]
    folder_to_check = 'ctng_conf_corrupt'
    checksum_file = 'checksum.txt'
    
    expected_checksums = {}
    if os.path.exists(checksum_file):
        with open(checksum_file, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    checksum = parts[0]
                    path = parts[1]
                    expected_checksums[path] = checksum
    else:
        print(f"File not found {checksum_file}")
        return
    for root, dirs, files in os.walk(folder_to_check):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, folder_to_check)
            normalized_path = rel_path.replace("\\", "/") 
            current_checksum = calculate_checksum(full_path)
            
            if normalized_path in expected_checksums:
                if current_checksum == expected_checksums[normalized_path]:
                    right += 1
                else:
                    print(f"==> Wrong  | {normalized_path}")
                    print(f"   ==> Real checksum: {current_checksum}")
                    print(f"   ==> In checksum.txt: {expected_checksums[normalized_path]}")
                    wrong += 1
                    error_files.append(normalized_path)
            else:
                print(f"==> Missing    | {normalized_path} (Không tìm thấy trong checksum.txt)")
                miss += 1

    print(f"\nTotal: {right + wrong + miss}")
    print(f"Match checksum: {right}")
    print(f"Wrong checksum: {wrong}")
    print(f"Missing in txt: {miss}")
    print(f"Error files: {error_files}")
if __name__ == "__main__":
    main()