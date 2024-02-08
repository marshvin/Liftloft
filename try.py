import secrets
import string

secret_key = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
print(secret_key)
