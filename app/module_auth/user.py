from flask_restful import Resource
from user_db_model import UserStudent

class User(Resource):

    def get(self, id):
        user = UserStudent.query.filter_by().first()
        return user.name

    def put(self):
        pass

    def delete(self):
        pass
