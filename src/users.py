from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
from src.database import User, db
import validators
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token, create_refresh_token

# Blueprint

users = Blueprint("users", __name__, url_prefix="/api/users")

# Routes


@users.get("/")
def getAll():
    users = User.objects
    return (jsonify(users), 200)


@users.get("/<id>")
def getUser(id):
    user = User.objects(id=id).first()
    return (jsonify(user), 200)


@users.post('/')
def create():
    # Request body
    email = request.json.get('email', '')
    password = request.json.get('password', '')
    firstName = request.json.get('firstName', '')
    lastName = request.json.get('lastName', '')

    # validations
    if len(password) < 6:
        return jsonify({"error": "Password too short"}), 400

    if not validators.email(email):
        return jsonify({"error": "Email is not valid"}), 400

    # Encrypt password
    password_hash = generate_password_hash(password)

    # Create new document
    try:
        user = User(email=email, password=password_hash,
                    firstName=firstName, lastName=lastName)
        user.save()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return (jsonify({"message": "User created"}), 201)


@users.put('/<id>')
def update(id):
    # Request body
    email = request.json.get('email', '')
    firstName = request.json.get('firstName', '')
    lastName = request.json.get('lastName', '')

    # Find document
    user = User.objects(id=id).first()

    # Update values
    user.email = email
    user.firstName = firstName
    user.lastName = lastName

    user.save()

    return (jsonify(user), 200)


@users.delete('/<id>')
def delete(id):
    try:
        #Return true or false
        result = User.objects(id=id).delete()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return (jsonify({"result": result}), 200)


# Authentication
@users.post('/login')
def login():
    email = request.json.get('email', '')
    password = request.json.get('password', '')

    user = User.objects(email=email).first()
    if user:
        is_match = check_password_hash(user.password, password)
        if is_match:
            userId = str(user.pk)
            print(userId)
            refreshToken = create_refresh_token(identity=userId)
            accessToken = create_access_token(identity=userId)

            return (jsonify({
                "accessToken": accessToken,
                "refreshToken": refreshToken
            }))

    return (jsonify({
        "error": 'Wrong credentials'
    }), 401)


@users.get("/protectedRoute")
@jwt_required()
def protectedRoute():
    userId = get_jwt_identity()

    user = User.objects(id=userId).first()

    return (jsonify(user), 200)
