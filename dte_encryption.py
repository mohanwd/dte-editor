from cryptography.fernet import Fernet

#Generates a key and save it into a file
def write_key():
    Dkey = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(Dkey)

#Loads the key from the current directory named `key.key`
def load_key():
    return open("key.key", "rb").read()

#write_key()
# load the previously generated key
Dkey = load_key()
# initialize the Fernet class
f = Fernet(Dkey)

def dte_encrypt(data):
	print("Encrypting Data")
	e_data = f.encrypt(data.encode())
	return e_data

def dte_decrypt(data):
	print("Decrypting Data")
	d_data = f.decrypt(data).decode()
	return d_data