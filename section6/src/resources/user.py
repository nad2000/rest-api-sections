from models.user import User
from flask_restful import Resource, reqparse

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("username",
            type=str,
            required=True,
            help="This field cannot be left blank! It should be string."
    )
    parser.add_argument("password",
            type=str,
            required=True,
            help="This field cannot be left blank! It should be string."
    )

    def post(self):
        data = self.parser.parse_args()
        username, password = data["username"], data["password"]

        if User.find_user(username):
            return {"message": "User '%s' already exists." % username}, 400

        User.insert_user(username, password)

        return {"message": "User '%s' created successfully." % username}, 201

