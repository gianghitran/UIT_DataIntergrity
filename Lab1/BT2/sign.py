import hashlib

def sha256(data):
    return hashlib.sha256(data).hexdigest()


def read_user_input(prompt):
    try:
        return raw_input(prompt)  
    except NameError:
        return input(prompt)

def sign_file(file_path, secret_key):
    with open(file_path, "rb") as f:
        data = f.read()

    file_hash = sha256(data)
    signature = sha256((file_hash + secret_key).encode())

    with open(file_path + ".sig", "w") as f:
        f.write(signature)

    print("Signature:", signature)
    print("Saved to:", file_path + ".sig")


if __name__ == "__main__":
    file_path = read_user_input("Enter file path: ").strip().strip('"').strip("'")
    secret_key = read_user_input("Enter secret key: ").strip().strip('"').strip("'")

    sign_file(file_path, secret_key)