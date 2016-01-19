from flask_restful import Resource, reqparse, abort
import json
from user_db_model import UserModel
from app import api, ma, db, MOODLE_URL
from urllib2 import urlopen, URLError, HTTPError
from marshmallow import fields


# Users resource [GET, POST]
class Users(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("email", type=str, required=True, help='No email provided', location='json')
        self.reqparse.add_argument("pass", required=True, type=str, location='json')
        super(Users, self).__init__()

    def get(self):
        users = UserModel.query.all()
        return {"users": users_schema.dump(users).data}

    def post(self):
        args = self.reqparse.parse_args()
        user = UserModel.query.filter_by(email=args['email']).first()
        # Check if user exists
        if user is None:
            try:
                token = json.load(urlopen(MOODLE_URL + '/login/token.php?username=' + args['email'] +
                    '&password=' + args['pass'] + '&service=moodle_mobile_app'))['token'].encode('ascii', 'ignore')

                user_id = json.load(urlopen(MOODLE_URL + '/webservice/rest/server.php?wstoken=' + token +
                                    '&wsfunction=core_webservice_get_site_info&moodlewsrestformat=json'))['userid']

                moodle_user_data = json.load(urlopen(MOODLE_URL + '/webservice/rest/server.php?wstoken='
                                                      + token + '&wsfunction=core_user_get_users_by_id&userids[]=' +
                                                      str(user_id) + '&moodlewsrestformat=json'))[0]
            except KeyError as e:
                if e.message == 'token':
                    return {"Error": "bad username or password"}, 401
            except HTTPError as e:
                return {"Error": "bad moodle url"}, 500
            except URLError as e:
                return {"Error": "bad moodle url"}, 500
            except TypeError as e:
                    abort(500)

            user = UserModel(name=moodle_user_data['fullname'], vpisna_st=int(moodle_user_data['idnumber']),
                             email=moodle_user_data['email'], token=token)
            db.session.add(user)
            db.session.commit()
            sc = UserSchema(extra={"picture": moodle_user_data['profileimageurl']})
            return sc.dump(user).data, 201
        return user_schema.dump(user).data, 200


# User resource [GET, PUT, DELETE]
class User(Resource):

    def get(self, idx):
        user = UserModel.query.get(idx)
        if user is None:
            abort(404)
        return user_schema.dump(user).data

    def put(self, idx):
        pass

    def delete(self, idx):
        if UserModel.query.filter_by(id=idx).delete() != 0:
            db.session.commit()
            return {"Message": "user removed"}, 200
        abort(404)


# Users schema for de/serialization
class UserSchema(ma.ModelSchema):

    class Meta:
        # Use database model
        model = UserModel

    # create url for specific user
    urls = ma.Hyperlinks({
        'self': ma.URLFor('user', idx='<id>'),
    }, dump_only=True)


# create schemas
user_schema = UserSchema()
users_schema = UserSchema(only=('id', 'name', 'urls'), many=True)

# Bind resources to url
api.add_resource(Users, '/api/users', endpoint='users')
api.add_resource(User, '/api/users/<int:idx>', endpoint='user')
