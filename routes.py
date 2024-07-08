from flask import Flask, request, jsonify
from models import db, bcrypt, jwt, User, Organisation, user_organisation
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


app = Flask(__name__)
app.config.from_object('config.Config')


db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)

@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    errors = validate_user_data(data)
    if errors:
        return jsonify({"errors": errors}), 422
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"errors": [{"field": "email", "message": "Email already exists"}]}), 422
    
    user = User(**data)
    user.hash_password()

    org_name = f"{user.first_name}'s Organisation"
    organisation = Organisation(name=org_name)

    db.session.add(user)
    db.session.add(organisation)
    db.session.commit()

    user_organisation.insert().values(user_id=user.user_id, org_id=organisation.org_id)
    db.session.commit()

    access_token = create_access_token(identity=user.user_id)

    return jsonify({
        "status": "success",
        "message": "Registration successful",
        "data": {
            "access_token": access_token,
            "user": {
                "user_id": user.user_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone": user.phone
            }
        }
    }), 201

