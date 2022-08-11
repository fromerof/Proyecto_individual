from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class Comment:
    def __init__(self,data):
        self.id = data['id']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def saveComment(cls,data):
        query = "INSERT INTO comments (comment,created_at,updated_at,user_id) VALUES (%(comment)s,NOW(),NOW(),%(user_id)s)"
        results = connectToMySQL("register_login").query_db(query,data)
        return results

    @classmethod
    def get_allcomments(cls):
        query = "SELECT * FROM comments ORDER BY comment DESC"
        results = connectToMySQL("register_login").query_db(query)
        comments = []
        for comment in results:
            comments.append(cls(comment))
        return comments
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM comments WHERE id = %(user_id)s;"
        results = connectToMySQL("register_login").query_db(query,data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE comments SET comment=%(comment)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL("register_login").query_db(query,data)

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM comments WHERE id = %(id)s;"
        return connectToMySQL("register_login").query_db(query,data)