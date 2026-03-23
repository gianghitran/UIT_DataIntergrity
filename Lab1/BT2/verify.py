import hashlib

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def read_user_input(prompt):
    try:
        return raw_input(prompt) 
    except NameError:
        return input(prompt)

def verify_file(file_path, secret_key):
    with open(file_path, "rb") as f:
        data = f.read()

    with open(file_path + ".sig", "r") as f:
        signature = f.read()

    file_hash = sha256(data)
    new_signature = sha256((file_hash + secret_key).encode())

    if new_signature == signature:
        print(" File is VALID")
    else:
        print(" File has been MODIFIED!!!")


if __name__ == "__main__":
    file_path = read_user_input("Enter file path: ").strip().strip('"').strip("'")
    secret_key = read_user_input("Enter secret key: ").strip().strip('"').strip("'")

    verify_file(file_path, secret_key)