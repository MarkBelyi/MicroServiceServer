import secrets

def __main__():
    secret_key = secrets.token_hex(32)
    print(f"Generated secret key: {secret_key}")

if __name__ == "__main__":
    __main__()