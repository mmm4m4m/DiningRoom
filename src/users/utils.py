from passlib.context import CryptContext

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def check_password(password, hashed_password):
    return password_context.verify(password, hashed_password)


def get_hashed_password(password):
    return password_context.hash(password) 
