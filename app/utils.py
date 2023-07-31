import json

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from models import db, User, Order, Offer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTS_JSON'] = {'unsure_ascii': False, 'indent': 4}


db = SQLAlchemy(app)


def load_data_from_json(json_file, model_class):
    with open(json_file, 'r') as file:
        data = json.load(file)
        for item in data:
            new_entry = model_class(**item)
            db.session.add(new_entry)
    db.session.commit()
    # Создание таблиц в базе данных
    db.create_all()
    # Путь к файлам JSON в директории Data
    users_file = 'Data/users.json'
    orders_file = 'Data/orders.json'
    offers_file = 'Data/offers.json'

    # Загрузка данных из JSON файлов в соответствующие таблицы
    load_data_from_json(users_file, User)
    load_data_from_json(orders_file, Order)
    load_data_from_json(offers_file, Offer)


# Маршрут для получения всех пользователей
@app.route('/users', methods=['GET'])
def get_all_users():
    # Получение всех пользователей из базы данных
    users = User.query.all()
    user_list = []
    for user in users:
        # Создание словаря с данными о пользователе
        user_data = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'age': user.age,
            'email': user.email,
            'role': user.role,
            'phone': user.phone
        }
        # Добавление данных о пользователе в список
        user_list.append(user_data)
    # Преобразование списка в формат JSON и возвращение его в ответе
    return jsonify(user_list)


# Маршрут для получения конкретного пользователя по его идентификатору
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    # Поиск пользователя по его идентификатору в базе данных
    user = User.query.get(user_id)
    # Проверка, найден ли пользователь с указанным идентификатором
    if not user:
        # Если пользователь не найден, возвращается сообщение об ошибке 404 Not Found
        return jsonify({'message': 'User not found'}), 404

    # Создание словаря с данными о пользователе
    user_data = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'age': user.age,
        'email': user.email,
        'role': user.role,
        'phone': user.phone
    }
    # Преобразование словаря в формат JSON и возвращение его в ответе
    return jsonify(user_data)

    # PUT-запрос для обновления пользователя по идентификатору


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.json  # Получаем данные из тела запроса (JSON)
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.age = data['age']
    user.email = data['email']
    user.role = data['role']
    user.phone = data['phone']

    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200


# DELETE-запрос для удаления пользователя по идентификатору
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200


# GET-запрос для получения всех заказов
@app.route('/orders', methods=['GET'])
def get_all_orders():
    orders = Order.query.all()
    return jsonify([order.serialize_order() for order in orders]), 200


# GET-запрос для получения заказа по идентификатору
@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order_by_id(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404
    return jsonify(order.serialize_order()), 200


@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    order = Order()
    order.update_fr

    db.session.add(order)
    db.session.commit()

    return jsonify(order.serialize()), 201


@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    data = request.json
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    order.update_from_json(data)
    db.session.commit()

    return jsonify(order.serialize_order()), 200


@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    db.session.delete(order)
    db.session.commit()

    return jsonify({'message': 'Order deleted successfully'}), 200


# GET-запрос для получения всех предложений
@app.route('/offers', methods=['GET'])
def get_all_offers():
    offers = Offer.query.all()
    return jsonify([offer.serialize_offer() for offer in offers]), 200


# GET-запрос для получения предложения по идентификатору
@app.route('/offers/<int:offer_id>', methods=['GET'])
def get_offer_by_id(offer_id):
    offer = Offer.query.get(offer_id)
    if not offer:
        return jsonify({'message': 'Offer not found'}), 404
    return jsonify(offer.serialize_offer()), 200


# Вспомогательная функция для обновления атрибутов заказа из JSON
def update_order_from_json(order, data):
    if 'name' in data:
        order.name = data['name']
    if 'description' in data:
        order.description = data['description']
    if 'start_date' in data:
        order.start_date = data['start_date']
    if 'end_date' in data:
        order.end_date = data['end_date']
    if 'address' in data:
        order.address = data['address']
    if 'price' in data:
        order.price = data['price']


# Вспомогательная функция для обновления атрибутов предложения из JSON
def update_offer_from_json(offer, data):
    if 'order_id' in data:
        offer.order_id = data['order_id']
    if 'executor_id' in data:
        offer.executor_id = data['executor_id']


@app.route('/offers', methods=['POST'])
def create_offer():
    data = request.json
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    offer = Offer()
    offer.update_from_json(data)

    db.session.add(offer)
    db.session.commit()

    return jsonify(offer.serialize()), 201


@app.route('/offers/<int:offer_id>', methods=['PUT'])
def update_offer(offer_id):
    offer = Offer.query.get(offer_id)
    if not offer:
        return jsonify({'message': 'Offer not found'}), 404

    data = request.json
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    offer.update_from_json(data)
    db.session.commit()

    return jsonify(offer.serialize()), 200


@app.route('/offers/<int:offer_id>', methods=['DELETE'])
def delete_offer(offer_id):
    offer = Offer.query.get(offer_id)
    if not offer:
        return jsonify({'message': 'Offer not found'}), 404

    db.session.delete(offer)
    db.session.commit()

    return jsonify({'message': 'Offer deleted successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)
