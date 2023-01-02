from app.determine_preferred_item import determine_preferred_item
from app import models, schemas


item_schema = schemas.ItemSchema()


def resolve_preferred_item(_, info, brickIds):
    try:
        bricks = models.Brick.query.filter(models.Brick.id.in_(brickIds)).all()
        preferred_item = determine_preferred_item(bricks)
        if preferred_item:
            return {"item": item_schema.dump(preferred_item)}
        else:
            return {"item": None}
    except Exception as e:
        return {"item": None, "errors": [str(e)]}
