from flask_restful import Resource
from user_db_model import UserStudentModel
from app import api


class User(Resource):

    def get(self, idx):
        user = UserStudentModel.query.get(idx)
        return user.name

    def put(self):
        pass

    def delete(self):
        pass

# Bind resources to url
api.add_resource(User, '/user/<int:idx>', endpoint='user')
