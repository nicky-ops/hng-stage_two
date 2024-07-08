def validate_user_data(data):
    errors = []
    if not data.get('first_name'):
        errors.append({"field": "first_name", "message": "First name is required"})
    if not data.get('last_name'):
        errors.append({"field": "last_name", "message": "Last name is required"})
    if not data.get('email'):
        errors.append({"field": "email", "message": "Email is required"})
    if not data.get('password'):
        errors.append({"field": "password", "message": "Password is required"})
    if not data.get('phone'):
        errors.append({"field": "phone", "message": "Phone number is required"})
    return errors