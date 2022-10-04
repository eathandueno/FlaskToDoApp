from flask import flash
db = 'mybrain'
from flask_app.config.mysqlconnection import connectToMySQL
class Categories:
    @staticmethod
    def validate_register(form):
        is_valid = True
        if len(form['category']) > 1:
            is_valid = False
        return is_valid

    def __init__(self, data):
        self.id = data['id']
        self.creator_id = data['creator_id']
        self.category = data['category']


    @classmethod
    def get_categories(cls, data):
        query = "SELECT * from categories where creator_id = %(id)s"
        results = connectToMySQL(db).query_db(query, data)
        cats = []
        for result in results:
            cats.append(cls(result))
        return cats

    @classmethod
    def create_category(cls,data):
        query = "INSERT into categories (creator_id, category) values (%(id)s, %(category)s);"
        return connectToMySQL(db).query_db(query, data)

    def delete_category(data):
        query = "DELETE from categories where id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)