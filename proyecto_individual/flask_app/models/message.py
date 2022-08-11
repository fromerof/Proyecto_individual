from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class Message:
    def __init__(self,data):
        self.name = data['name']
        self.email = data['email']
        self.message = data['message']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def message(cls,data):
        query = "INSERT INTO messages (name,email,message,created_at,updated_at) VALUES (%(name)s,%(email)s,%(message)s,NOW(),NOW());"
        result = connectToMySQL("register_login").query_db(query,data)
        return result

    # @staticmethod
    # def validate_message(message):
    #     is_valid = True
    #     if len(message['name']) < 3:
    #         flash("Name must be at least 3 characters")
    #         is_valid = False
    #     return is_valid