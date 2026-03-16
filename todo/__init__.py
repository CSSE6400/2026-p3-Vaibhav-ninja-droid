from os import environ
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
 
def create_app(config_overrides=None): 
   app = Flask(__name__) 
 
   app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///db.sqlite")
   if config_overrides: 
       app.config.update(config_overrides)
 
   # Load the models 
   from todo.models import db 
   from todo.models.todo import Todo 
   db.init_app(app) 
 
   # Create the database tables 
   with app.app_context(): 
      db.create_all() 
      db.session.commit() 

   @app.route("/")
   def home():
      return {
         "message": "Todo API is running",
         "health": "/api/v1/health",
         "todos": "/api/v1/todos"
      }
 
   # Register the blueprints 
   from todo.views.routes import api 
   app.register_blueprint(api) 
 
   return app