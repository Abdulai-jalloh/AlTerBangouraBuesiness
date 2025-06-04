from flask import Flask
from app.models import db
from flask_migrate import Migrate  # type: ignore
from flask_wtf.csrf import CSRFProtect
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus


csrf = CSRFProtect()
migrate = Migrate()

def create_app():
  base_dir = os.path.abspath(os.path.dirname(__file__))
  project_Folder = os.path.abspath(os.path.join(base_dir))
  app = Flask(__name__, 
  template_folder=os.path.join(project_Folder, '..', 'templates'),
  static_folder=os.path.join(project_Folder, '..', 'static'))
  
  load_dotenv(os.path.join(base_dir, '..', '.env'))

  mysql_Name = os.getenv('MYSQL_USER')
  mysql_Password = quote_plus(os.getenv('MYSQL_PASSWORD'))
  mysql_host = os.getenv('MYSQL_HOST')
  mysql_port = os.getenv('MYSQL_PORT', '3306')
  mysql_db = os.getenv('MY_DATABASE')

  app.config['SQLALCHEMY_DATABASE_URI'] = ( f"mysql+pymysql://{mysql_Name}:{mysql_Password}@{mysql_host}:{mysql_port}/{mysql_db}?charset=utf8mb4" )
  

  app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_secret_fallback')

  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['UPLOAD_FOLDER'] = os.path.join(project_Folder, '..', 'static', 'uploads')
  app.config['IMAGES_FOLDER'] = os.path.join(project_Folder, '..', 'static', 'images')
  app.config['ALLOWED_EXTENSION'] = {'JPG', 'jpeg', 'png'}
  print("MYSQL_USER", mysql_Name)
  print("MYSQL_PASSWORD", mysql_Password)
  print("MYSQL_HOST", mysql_host)
  print("MYSQL_PORT", mysql_port)
  print("MY_DATABASE", mysql_db)

  db.init_app(app)
  csrf.init_app(app)
  migrate.init_app(app, db)


  from app.routes.land_routes import land_bp
  app.register_blueprint(land_bp)
  return app