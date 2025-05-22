#Placeholder for validators
from flask import jsonify

def validate_required_fields(data, fields):
    missing = [field for field in fields if field not in data]
    if missing:
        return False, jsonify({'message': f'Missing fields: {", ".join(missing)}'}), 400
    return True, None, None
