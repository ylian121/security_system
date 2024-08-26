import json
import bcrypt
from cryptography.fernet import Fernet
import os

encryption_key = os.environ['ENCRYPTION_KEY']
cipher_suite = Fernet(encryption_key.encoded())

#Encrypting the data
def encrypt_data(data):
  return cipher_suite.encrypt(data.encode())
  
#Decryting the data
def decrypt_data(data):
  return cipher_suite.decrypt(data).decode()
  
#JSON File
user_info_file = 'user_info.json'

#Load data from JSON and create a new one if it doesn't already exist
def load_user_data():
  is os.path.exists(user_info_file):
    with open(user_info_file, 'r') as file:
      return json.load(file)
  return {}

#save data to JSON
def save user_data(data):
  with open(user_info_file, 'w') as file:
    json.dump(data, file, indent = 4)

user_data = load_user_data()

#load data when program starts

#check password requirements:
def check_password_requirements(password1, password2):

    if len(password1) < 8:
        print("Password must be at least 8 characters long.")
        return False

    if password1 != password2:
        print("Passwords do not match.")
        return False

    print("Password is valid.")
    return True

#check pincode requirements:
def check_pincode_requirements(pincode):
    # Check if the pincode is at most 6 characters long
    if len(pincode) > 6:
        print("Pincode must be at most 6 characters long.")
        return False

    # Check if the pincode contains only numbers
    if not pincode.isdigit():
        print("Pincode must contain only numbers.")
        return False

    # Check for no repeated numbers next to each other
    for i in range(len(pincode) - 1):
        if pincode[i] == pincode[i + 1]:
            print("Pincode must not have repeated numbers next to each other.")
            return False

    print("Pincode is valid.")
    return True
