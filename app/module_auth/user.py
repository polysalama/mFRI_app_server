from flask_restful import Resource
from user_db_modul import UserStudent


class User(Resource):

    def get(self, id):
        user = UserStudent.query.filter_by(id)
        return {'ime': 'priimek'}

    def put(self):
        pass

    def delete(self):
        pass
