import os
import warnings

from dotenv import load_dotenv
from fastapi import FastAPI


from src.app.core.config import get_settings


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

# meta = MetaData(naming_convention=convention)
# Base = declarative_base(metadata=meta)
# migrate = Migrate()
# db = SQLAlchemy(metadata=meta)
# settings = None

# spec = APISpec(
#     title="Picture service API",
#     version="1.0.0",
#     openapi_version="3.0.2",
#     plugins=[FlaskPlugin()],
# )

jwt = JWTManager()


def create_app():
    app_config_name:str = get_app_config_from_environ()
    app:FastAPI = FastAPI()
    
    init_settings(app_config_name)
    # init_extensions(app)
    # register_blueprints(app)
    # register_apispec(app, spec)
    # with app.app_context():
    #     init_db()
    # migrate.init_app(app, db)
    return app

def init_settings(app_config_name:str):
    try:
        settings = get_settings(app_config_name)
        print(f'Settings name: {settings.SETTINGS_NAME}')
    except KeyError as err:
        warnings.warn(f".env SETTINGS_NAME error (dev, prod, test): {err}")
        exit(0)
        
# def init_db():
#     db_uri: str = current_app.config["SQLALCHEMY_DATABASE_URI"]
#     engine = create_engine(db_uri)
#     if not database_exists(engine.url):
#         create_database(engine.url)
#     Base.metadata.create_all(engine)

def get_app_config_from_environ() -> str:
    try:
        load_dotenv(".env")
    except FileNotFoundError:
        warnings.warn(".env file not found")
    try:
        app_config = os.environ["SOCIAL_NETWORK_CONFIG"]
    except KeyError as e:
        raise RuntimeError(f"Environ attr '{e.args[0]}' does not exist.")
    return app_config


# def setup_routers(app: FastAPI):
#     app.include_router(api_router, prefix=settings.API_PATH)


# def init_extensions(app: FastAPI):
#     db.init_app(app)
#     jwt.init_app(app=app)



# def register_blueprints(app: FastAPI):
#     from src.app.api import captcha_auth_app

#     swagger_bp = get_swaggerui_blueprint(
#         "/docs",
#         "/captcha_model_docs",
#     )
#     app.register_blueprint(captcha_auth_app)
#     app.register_blueprint(swagger_bp)


# def register_apispec(app: FastAPI, api_spec: APISpec):
#     with app.app_context():
#         for fn_name in app.view_functions:
#             if fn_name == "static":
#                 continue
#             view_fn = app.view_functions[fn_name]
#             api_spec.path(view=view_fn)

#     @app.route("/captcha_model_docs")
#     def create_swagger_spec():
#         return json.dumps(api_spec.to_dict())
