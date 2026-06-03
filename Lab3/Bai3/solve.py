import json
import base64
import struct
import hashlib
import zipfile
import io
import os

CHUNK_SIZE = 384
PAYLOAD_SIZE = 23713
SHA1_SEED = "7465737430322d61706b2d6c6564676572"
MASK_KEY_HEX = "e1782c4510dd53107c0d877735de9304"
SEQ_XOR_KEY = 0x5a

def generate_keystream(real_seq, length):
    mask_key_bytes = bytes.fromhex(MASK_KEY_HEX)
    seq_bytes = struct.pack('<I', real_seq) 
    
    hash_obj = hashlib.sha256(mask_key_bytes + seq_bytes)
    base_hash = hash_obj.digest()
    
    keystream = (base_hash * (length // len(base_hash) + 1))[:length]
    return keystream

def solve():
    fragments = {}
    with open('fragment-ledger.jsonl', 'r') as f:
        for line in f:
            data = json.loads(line.strip())
            if 'noise' in data:
                continue
            fragments[data['prev_sha1']] = data

    print(f"[*] Loaded {len(fragments)} valid fragments.")

    current_sha1 = SHA1_SEED
    recovered_data = bytearray()
    
    print("[*] Rebuilding chain...")
    
    while current_sha1 in fragments and len(recovered_data) < PAYLOAD_SIZE:
        frag = fragments[current_sha1]
        
        real_seq = frag['seq_xor'] ^ SEQ_XOR_KEY
        
        masked_bytes = base64.b64decode(frag['masked_b64'])
        
        bytes_to_process = min(len(masked_bytes), PAYLOAD_SIZE - len(recovered_data))
        masked_bytes = masked_bytes[:bytes_to_process]
        
        keystream = generate_keystream(real_seq, len(masked_bytes))
        unmasked_bytes = bytes([b ^ k for b, k in zip(masked_bytes, keystream)])
        
        recovered_data.extend(unmasked_bytes)
        
        current_sha1 = frag['sha1_after']

    print(f"[+] Reconstructed payload size: {len(recovered_data)} bytes.")

    if len(recovered_data) != PAYLOAD_SIZE:
        print("[-] Warning: Recovered size does not match expected payload_size!")

    zip_filename = "recovered_ledger.zip"
    with open(zip_filename, "wb") as f:
        f.write(recovered_data)
    print(f"[+] Saved recovered archive to {zip_filename}")

    try:
        with zipfile.ZipFile(io.BytesIO(recovered_data)) as z:
            if 'flag.txt' in z.namelist():
                flag_content = z.read('flag.txt').decode('utf-8').strip()
                print("\n" + "="*50)
                print(f"FLAG FOUND: {flag_content}")
                print("="*50 + "\n")
            else:
                print("[-] flag.txt not found inside the ZIP.")
                print("Contents of ZIP:", z.namelist())
    except zipfile.BadZipFile:
        print("[-] Error: Recovered data is not a valid ZIP file. Check decryption logic.")

    print(f"[+] Final SHA-1 (cuối chuỗi): {current_sha1}")

if __name__ == "__main__":
    solve()
