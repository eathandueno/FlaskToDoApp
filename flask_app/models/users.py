from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
db = 'mybrain'
class User:
    @staticmethod
    def validate_register(form):
        is_valid = True
        if len(form['first_name']) < 1:
            flash("First name must be longer than 2 characters")
            is_valid = False
        if len(form['last_name']) < 2:
            flash("Last name must be longer than 2 characters")
            is_valid = False
        if form['password'] != form['confirmPassword']:
            flash("Passwords do not match")
            is_valid = False
        if not EMAIL_REGEX.match(form['email']):
            flash("Invalid email address")
            is_valid = False
        return is_valid

    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.password = data['password']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_by_username(cls,data):
        query = "SELECT * from user where username = %(username)s"
        results = connectToMySQL(db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    
    def submit_register(data):
        query = "INSERT into user (first_name, last_name, username, password, email) values ( %(first_name)s, %(last_name)s, %(username)s, %(password)s, %(email)s );"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * from user where id = %(id)s"
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])