from marshmallow import (
    fields,
)
from app import models, ma


class BrickSchema(ma.SQLAlchemySchema):
    class Meta:
        model = models.Brick

        fields = ("id", "design_id", "color_ids")

    id = fields.Integer(dump_only=True)
    design_id = fields.Integer(required=True)
    color_ids = fields.List(fields.Integer())


class MasterDataSchema(ma.SQLAlchemySchema):
    class Meta:
        model = models.MasterData

        fields = ("id", "price", "status")

    id = fields.Integer(dump_only=True)
    price = fields.Integer(required=True)
    status = fields.String(required=True)


class ItemSchema(ma.SQLAlchemySchema):
    class Meta:
        model = models.Item

        fields = ("id", "bricks", "master_data")

    id = fields.Integer(dump_only=True)
    bricks = fields.Nested(BrickSchema, many=True)
    master_data = fields.Nested(MasterDataSchema)
