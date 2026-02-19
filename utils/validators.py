import re

def validate_cpf(cpf):
    # Simple validation
    return len(cpf) == 11 and cpf.isdigit()

def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)