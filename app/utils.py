## utility file for hashing password and verifying password entered by user with hashed password 

from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"],bcrypt__rounds=12)

def hash_password(password:str) ->  str:
    return password_context.hash(password)

def verify_password(plain_password:str, hashed_password:str)->bool:
    return password_context.verify(plain_password, hashed_password)