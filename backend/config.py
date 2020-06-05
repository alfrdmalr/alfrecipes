import os

app_path = os.path.abspath(os.path.dirname(__file__)) # absolute path to dir containing this file

class Config:
  SECRET_KEY = 'super-secret' #set as env variable like os.environ.get('SECRET_KEY') or $fallback
  DATABASE = os.path.join(app_path, 'alfrecipes.sqlite')