from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from sqlalchemy import Enum


bricks_items_table = db.Table(
    "bricks_items",
    db.Column(
        "brick_id", UUID(as_uuid=True), db.ForeignKey("brick.id"), primary_key=True
    ),
    db.Column(
        "item_id", UUID(as_uuid=True), db.ForeignKey("item.id"), primary_key=True
    ),
)


class ItemStatus(enum.Enum):
    Normal = enum.auto()
    Novelty = enum.auto()
    Outgoing = enum.auto()
    Discontinued = enum.auto()


class Brick(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    design_id = db.Column(db.Integer)
    color_ids = db.Column(db.dialects.postgresql.ARRAY(db.Integer))


class Item(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bricks = db.relationship(
        "Brick",
        secondary=bricks_items_table,
        lazy="dynamic",
        backref=db.backref("items", lazy="dynamic"),
    )


class MasterData(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    price = db.Column(db.Integer)
    status = db.Column(Enum(ItemStatus))
