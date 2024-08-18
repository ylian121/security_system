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
