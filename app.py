import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# 1. Generate a secure 32-byte (256-bit) AES key
# key = get_random_bytes(32)
key = b' \xd3\xfd\xa1R\xcf\x13K\xae\x9cV\xe1a\x89\xe9\xca\x96\xcfFM\xa7J\xe5\xd3\xe2\xc1\x0efdl\x9f\xf9'

# 3. Decrypt the Base64 string back to plaintext
def decrypt_string(encrypted_base64: str, key: bytes) -> str:
    # Decode Base64 string back to raw bytes
    raw_data = base64.b64decode(encrypted_base64.encode('utf-8'))
    
    # Extract the nonce (first 16 bytes), tag (next 16 bytes), and ciphertext
    nonce = raw_data[:16]
    tag = raw_data[16:32]
    ciphertext = raw_data[32:]
    
    # Create cipher with the same key and the extracted nonce
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    
    # Decrypt and verify integrity
    decrypted_bytes = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_bytes.decode('utf-8')


from flask import Flask, render_template, request
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


app = Flask(__name__)
key = b' \xd3\xfd\xa1R\xcf\x13K\xae\x9cV\xe1a\x89\xe9\xca\x96\xcfFM\xa7J\xe5\xd3\xe2\xc1\x0efdl\x9f\xf9'

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        # Get the number from the form and convert it to float or int
        user_input = request.form.get("text")
        if user_input:
            text = user_input
            result = decrypt_string(text, key)
            
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)