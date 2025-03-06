import jose
from jose import jwt
from datetime import datetime, timezone, timedelta
from functools import wraps
from flask import request, jsonify
# from urllib.request import urlopen # commented out to use with Auth0 later
# import json # commented out to use with Auth0 later
import os

SECRET_KEY = os.getenv("SQLALCHEMY_DATABASE_URI") or "some-random-thing-here-does-not-matter"

def encode_jwt_token(customer_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=1),
        'iat': datetime.now(timezone.utc),
        'sub': str(customer_id)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token 

def jwt_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
            if not token:
                return jsonify({'message': 'missing token'}), 401
            
            # verify valid token & get customer_id
            try:
                data = jwt.decode(token, SECRET_KEY, algorithms="HS256")
                print(data)
                customer_id = data['sub']
            except jose.exceptions.ExpiredSignatureError:
                return jsonify({'message': 'token expired'}), 401
            except jose.exceptions.JWTError:
                return jsonify({'message': 'invalid token'}), 401
            
            # Pass customer_id as a keyword argument to the wrapped route function
            kwargs['customer_id'] = customer_id
        else:
            return jsonify({'message': 'you must be logged in to access this.'}), 401
        return f(*args, **kwargs)
      
    return decorated