from app import models
from flask import jsonify


def resolve_preferred_item(_, info):
    try:
        return {"item": {"id": "test"}}
    except Exception as e:
        return {"errors": [str(e)]}
