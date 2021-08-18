"""Item API"""
import json

from flask import Blueprint, request

from model.item import Item, db


api = Blueprint("item", __name__, url_prefix="/item")


@api.route("/register", methods=["POST"])
def register():
    """register an item"""
    data = json.loads(request.data)
    new_item = Item(
        title=data["title"],
        price=data["price"],
        thumbnail=data["thumbnail"] if "thumbnail" in data else None,
    )
    db.session.add(new_item)
    db.session.commit()

    return "Registered"


@api.route("/get", methods=["GET"])
def get():
    """get query result of an item"""
    query = json.loads(request.data)
    items = db.session.query(Item).filter(Item.title == query["title"]).all()

    results = []
    for item in items:
        results.append(
            {
                "id": item.id,
                "title": item.title,
                "price": item.price,
                "thumbnail": item.thumbnail,
            }
        )

    return {"result": results}


@api.route("/update", methods=["POST"])
def update():
    """update an item"""

    def update_if_key(data, key, result):
        return data[key] if key in data else getattr(result, key)

    data_ = json.loads(request.data)
    query = data_["query"]
    data = data_["data"]

    item = db.session.query(Item).filter(Item.title == query["title"]).first()

    for key in ["id", "title", "price", "thumbnail"]:
        setattr(item, key, update_if_key(data, key, item))

    db.session.commit()
    return "Updated"


@api.route("/delete", methods=["POST"])
def delete():
    """delete an item"""
    query = json.loads(request.data)

    item = db.session.query(Item).filter(Item.title == query["title"]).first()

    db.session.delete(item)
    db.session.commit()
    return "Deleted"
