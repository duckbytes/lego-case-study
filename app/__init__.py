from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)


from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    snake_case_fallback_resolvers,
    ObjectType,
)
from app import queries

query = ObjectType("Query")

query.set_field("preferredItem", queries.resolve_preferred_item)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(type_defs, query, snake_case_fallback_resolvers)

from app import models, routes, determine_preferred_item, schemas
