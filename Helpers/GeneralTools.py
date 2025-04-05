import json
from passlib.hash import bcrypt
import jwt
import os
import datetime
from typing import Dict, List
from Utils.CustomException import CustomException

def get_input_data(event: dict) -> dict:
    
    """
    Process the input data according to the HTTP method.

    Args:
        event (dict): The event object containing request data.

    Returns:
        dict: The processed data.
    """
    match event['httpMethod']:
        case 'POST':
            return process_post_data(event)
        case 'GET':
            return process_input_data(event)
        case 'PUT':
            return process_post_data(event)
        case 'DELETE':
            return process_input_data(event)
        
def process_post_data(event: dict) -> dict:
    
    """
    Process the input data for POST requests.

    Args:
        event (dict): The event object containing request data.

    Returns:
        dict: The processed data.
    """
    response = {}
    if event.get('body'):
        response = event.get('body') if isinstance(event.get('body'), dict) else json.loads(event.get('body'))

    return response

def process_input_data(event: dict) -> dict:
    """
    Process the input data for GET and DELETE requests.

    Args:
        event (dict): The event object containing request data.

    Returns:
        dict: The processed data from the query string parameters.
    """

    response = {}
    if event.get('queryStringParameters'):
        response = (event.get('queryStringParameters') 
                    if isinstance(event.get('queryStringParameters'), dict) 
                    else json.loads(event.get('queryStringParameters')))
    return response

def hash_password(password: str) -> str:
    """
    Hash a given password using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    """
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify if a given password matches the hashed password.

    Args:
        password (str): The plaintext password to be verified.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password is correct, raises an exception otherwise.

    Raises:
        CustomException: If the password does not match, with a 401 error code.
    """

    if not bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
        raise CustomException("Incorrect credentials", code=401)


def process_dict_data(key_name: str, value_name:str, data: List[Dict])-> Dict[str, str]:
    """
    Convert a list of dictionaries into a single dictionary.

    Args:
        key_name (str): The key whose value will become the keys of the new dictionary.
        value_name (str): The key whose value will become the values of the new dictionary.
        data (List[Dict]): A list of dictionaries to be processed.

    Returns:
        Dict[str, str]: A dictionary where each key-value pair is derived from the 
        corresponding key-value pair in the list of dictionaries.
    """

    response = {}
    for item in data: response[item[key_name]] = item[value_name]
    return response

def get_token_data(username: str, user_id: int) -> dict:

    """
    Generate a JWT token from a username and user_id.

    Args:
        username (str): The username to be included in the token.
        user_id (int): The user_id to be included in the token.

    Returns:
        dict: A JWT token containing the username and user_id, with an expiration time of 1 hour.

    """
    claims = {
        'username': username,
        'user_id': user_id,
        'exp': (datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp()
    }
    return jwt.encode(claims, os.getenv('JWT_SECRET_KEY'), algorithm='HS256')

def verify_token(token: str) -> dict:
    """
    Verify the authenticity of a JWT token.

    Args:
        token (str): The JWT token to be verified.

    Returns:
        dict: A dictionary containing the claims of the token, if it is valid.

    Raises:
        CustomException: If the token is invalid or expired, with a status code of 401.
    """
    try:
        claims = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
    except Exception as e:
        raise CustomException(str(e), code=401)
    
    return claims 
