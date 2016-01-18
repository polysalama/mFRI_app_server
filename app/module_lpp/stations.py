from flask_restful import Resource, reqparse
import json
from app import api
from urllib2 import urlopen, Request


class Stations(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument("entranceStation", type=str, required=True, help='No entrance station provided', location='json')
        self.reqparse.add_argument("busNumber", required=False, type=str, location='json')
        super(Stations, self).__init__()

    def get(self):
       pass

    def post(self):
        args = self.reqparse.parse_args()
        if len(args['busNumber'])> 0:
            str = 'http://www.trola.si/' + args['entranceStation'] +'/'+ args['busNumber']
        else:
            str = 'http://www.trola.si/' + args['entranceStation']
        req = Request(str)
        req.add_header("Accept", "application/json")
        token = json.load(urlopen(req))
        return token




# Bind resources to url
api.add_resource(Stations, '/api/stations')
