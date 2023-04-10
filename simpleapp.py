from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://mongo:27017/db'
# app.config['MONGO_DBNAME'] = 'users'
mongo = PyMongo(app)

# Create a new user
@app.route('/users', methods=['POST'])
def add_user():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    if not name or not email or not password:
        return jsonify({'message': 'Please provide all data'})
    
    user_id = mongo.db.users.insert_one({
        'name': name,
        'email': email,
        'password': password
    }).inserted_id

    new_user = mongo.db.users.find_one({'_id': user_id})
    new_user['_id'] = str(new_user['_id'])  # Convert ObjectId to string

    return jsonify({'user': new_user})

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = []
    for user in mongo.db.users.find():
        user['_id'] = str(user['_id'])  # Convert ObjectId to string
        users.append(user)

    return jsonify({'users': users})

# Get a user by ID
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    if user:
        user['_id'] = str(user['_id'])  # Convert ObjectId to string
        return jsonify({'user': user})
    else:
        return jsonify({'message': 'User not found'})
    

# Update a user by ID
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    # print(user)
    if user:
        # Update the user fields
        name = request.json.get('name')
        if not name:
            name = user['name']
        email = request.json.get('email')
        if not email:
            email = user['email']
        password = request.json.get('password')
        if not password:
            password = user['password']
            
        mongo.db.users.update_one(
            {'_id': ObjectId(id)},
            {'$set': {'name': name, 'email': email, 'password': password}}
        )
        return jsonify({'message': 'User updated successfully'})
    else:
        return jsonify({'message': 'User not found'})

# Delete a user by ID
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    if user:
        mongo.db.users.delete_one({'_id': ObjectId(id)})
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'message': 'User not found'})

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)