import json
from models import db, User, Order, Offer

def load_data_from_json(json_file, model_class):
    with open(json_file, "r") as file:
        data = json.load(file)
        for item in data:
            new_entry = model_class(**item)
            db.session.add(new_entry)
    db.session.commit()

def load_data():
    users_file = "..app/Data/users.json"
    orders_file = "..app/Data/orders.json"
    offers_file = "..app/Data/offers.json"

    load_data_from_json(users_file, User)
    load_data_from_json(orders_file, Order)
    load_data_from_json(offers_file, Offer)




