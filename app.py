from flask import Flask
from flask_restful import Api, Resource, reqparse
from pymongo import MongoClient
from bson import ObjectId
from flask.json import jsonify


app = Flask(__name__)
api = Api(app)

# MongoDB connection setup
client = MongoClient('mongodb://mongo:27017/')
db = client['mydatabase']

# Define the user resource class
class UserResource(Resource):
    def get(self, id):
        user = db.users.find_one({'_id': ObjectId(id)})
        user['_id'] = str(user['_id'])  # Convert ObjectId to string
        return jsonify({'user': user}) # output showing

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        user_data = parser.parse_args()
        db.users.update_one({'_id': ObjectId(id)}, {'$set': user_data})
        updated_user = db.users.find_one({'_id': ObjectId(id)})
        if not updated_user:
            return jsonify({'message': 'User not found'})
        updated_user['_id'] = str(updated_user['_id'])  # Convert ObjectId to string
        return jsonify({'user': updated_user})

    def delete(self, id):
        user = db.users.find_one({'_id': ObjectId(id)})
        if user:
            db.users.delete_one({'_id': ObjectId(id)})
            return jsonify({'message': 'User deleted successfully'})
        else:
            return jsonify({'message': 'User not found'})


# Define the user list resource class
class UserListResource(Resource):
    def get(self):
        users = []
        for user in list(db.users.find()):
            user['_id'] = str(user['_id'])  # Convert ObjectId to string
            users.append(user)
        return jsonify({'users': users})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        user_data = parser.parse_args()
        user_id = db.users.insert_one(user_data).inserted_id
        new_user = db.users.find_one({'_id': user_id})
        new_user['_id'] = str(new_user['_id'])  # Convert ObjectId to string
        return jsonify({'user': new_user})

# Add the user resource and user list resource to the API
api.add_resource(UserResource, '/users/<id>')
api.add_resource(UserListResource, '/users')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=8080)