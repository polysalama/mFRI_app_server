from flask_restful import Resource, reqparse
import json
from user_db_model import UserStudentModel
from app import api, ma, db
from urllib2 import urlopen


class Users(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("email", type=str, required=True, help='No email provided', location='json')
        self.reqparse.add_argument("pass", required=True, type=str, location='json')
        super(Users, self).__init__()

    def get(self):
        users = UserStudentModel.query.all()
        return {"users": user_schema.dump(users, many=True).data}

    def post(self):
        args = self.reqparse.parse_args()
        user = UserStudentModel.query.filter_by(email=args['email']).first()
        # Check if user exists
        if user is None:
            token = json.load(urlopen('https://ucilnica.fri.uni-lj.si/login/token.php?username=' + args['email'] +
                                       '&password=' + args['pass'] + '&service=moodle_mobile_app'))['token'].encode('ascii', 'ignore')
            user_id = json.load(urlopen('https://ucilnica.fri.uni-lj.si/webservice/rest/server.php?wstoken=' + token +
                                '&wsfunction=core_webservice_get_site_info&moodlewsrestformat=json'))['userid']
            moodle_user_data = json.load(urlopen('https://ucilnica.fri.uni-lj.si/webservice/rest/server.php?wstoken='
                                                  + token + '&wsfunction=core_user_get_users_by_id&userids[]=' +
                                                  str(user_id) + '&moodlewsrestformat=json'))[0]
            user = UserStudentModel(name=moodle_user_data['fullname'], vpisna_st=int(moodle_user_data['idnumber']),
                                                                                     email=moodle_user_data['email'],
                                                                                     token=token)
            db.session.add(user)
            db.session.commit()
        return user_schema.dump(user).data


class UserSchema(ma.ModelSchema):

    class Meta:
        model = UserStudentModel

    url = ma.Hyperlinks({
        'self': ma.URLFor('user', idx='<id>'),
    }, dump_only=True)

user_schema = UserSchema()


class User(Resource):

    def get(self, idx):
        user = UserStudentModel.query.get(idx)
        return user_schema.dump(user).data

    def put(self, idx):
        pass

    def delete(self):
        pass


# Bind resources to url
api.add_resource(Users, '/api/users', endpoint='users')
api.add_resource(User, '/api/users/<int:idx>', endpoint='user')
