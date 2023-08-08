

from flask import Flask, jsonify, request

from app.data_loader import load_data
from models import db, User, Order, Offer

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["RESTS_JSON"] = {"unsure_ascii": False, "indent": 4}

db.init_app(app)




# Маршрут для получения всех пользователей
@app.route("/users", methods=["GET"])
def get_all_users():
    # Получение всех пользователей из базы данных
    users = User.query.all()
    user_list = []
    for user in users:
        # Создание словаря с данными о пользователе
        user_data = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "age": user.age,
            "email": user.email,
            "role": user.role,
            "phone": user.phone
        }
        # Добавление данных о пользователе в список
        user_list.append(user_data)
    # Преобразование списка в формат JSON и возвращение его в ответе
    return jsonify(user_list)


# Маршрут для получения конкретного пользователя по его идентификатору
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    # Поиск пользователя по его идентификатору в базе данных
    user = User.query.get(user_id)
    # Проверка, найден ли пользователь с указанным идентификатором
    if not user:
        # Если пользователь не найден, возвращается сообщение об ошибке 404 Not Found
        return jsonify({"message": "User not found"}), 404

    # Создание словаря с данными о пользователе
    user_data = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "age": user.age,
        "email": user.email,
        "role": user.role,
        "phone": user.phone
    }
    # Преобразование словаря в формат JSON и возвращение его в ответе
    return jsonify(user_data)

    # PUT-запрос для обновления пользователя по идентификатору


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.json  # Получаем данные из тела запроса (JSON)
    user.first_name = data["first_name"]
    user.last_name = data["last_name"]
    user.age = data["age"]
    user.email = data["email"]
    user.role = data["role"]
    user.phone = data["phone"]

    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200

@app.route("/users", methods=["POST"])
def create_user():
    # Получение данных из тела запроса
    data = request.json

    # Создание нового объекта User на основе полученных данных
    new_user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        age=data["age"],
        email=data["email"],
        role=data["role"],
        phone=data["phone"]
    )

    # Добавление нового пользователя в базу данных
    db.session.add(new_user)
    db.session.commit()

    # Возвращение ответа с сообщением об успешном создании
    return jsonify({"message": "User created successfully"}), 201


# DELETE-запрос для удаления пользователя по идентификатору
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200


# GET-запрос для получения всех заказов
@app.route("/orders", methods=["GET"])
def get_all_orders():
    orders = Order.query.all()
    order_list = []
    for order in orders:
        # Создание словаря с данными о пользователе
        order_data = {
            "id": order.id,
            "name": order.name,
            "description": order.description,
            "start_date": order.start_date,
            "end_date": order.end_date,
            "address": order.address,
            "price": order.price
        }
        # Добавление данных о пользователе в список
        order_list.append(order_data)
    # Преобразование списка в формат JSON и возвращение его в ответе
    return jsonify(order_list),200



# GET-запрос для получения заказа по идентификатору
@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order_by_id(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"message": "Order not found"}), 404
        # Создание словаря с данными о пользователе
    order_data = {
            "id": order.id,
            "name": order.name,
            "description": order.description,
            "start_date": order.start_date,
            "end_date": order.end_date,
            "address": order.address,
            "price": order.price
        }
    # Возвращаем данные о заказе и статус 200
    return jsonify(order_data), 200


@app.route("/orders", methods=["POST"])
def create_order():
    data = request.json
    if not data:
        return jsonify({"message": "No data provided"}), 400
    new_order = Order(
        name=data["name"],
        description=data["description"],
        start_date=data["start_date"],
        end_date=data["end_date"],
        address=data["address"],
        price=data["price"]
    )

    # Добавление нового пользователя в базу данных
    db.session.add(new_order)
    db.session.commit()

    # Возвращение ответа с сообщением об успешном создании
    return jsonify({"message": "Order created successfully"}), 201



@app.route("/orders/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"message": "Order not found"}), 404
    data = request.json

    order.name = data["name"],
    order.description = data["description"],
    order.start_date = data["start_date"],
    order.end_date = data["end_date"],
    order.address = data["address"],
    order.price = data["price"]

    db.session.commit()

    return jsonify({"message": "User updated successfully"}), 200

@app.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"message": "Order not found"}), 404

    db.session.delete(order)
    db.session.commit()

    return jsonify({"message": "Order deleted successfully"}), 200


# GET-запрос для получения всех предложений
@app.route("/offers", methods=["GET"])
def get_all_offers():
    offers = Offer.query.all()
    offer_list = []
    for offer in offers:
        offer_data = {
             "id": offer.id,
            "order_id": offer.order_id,
            "executor_id": offer.executor_id
        }

        offer_list.append(offer_data)

    return jsonify(offer_list)


# GET-запрос для получения предложения по идентификатору
@app.route("/offers/<int:offer_id>", methods=["GET"])
def get_offer_by_id(offer_id):
    offer = Offer.query.get(offer_id)
    if not offer:
        return jsonify({"message": "Offer not found"}), 404
    offer_data = {
        "id": offer.id,
        "order_id": offer.order_id,
        "executor_id": offer.executor_id
    }

    return jsonify(offer_data)

@app.route("/offers<int:offer_id>", methods=["PUT"])
def update_offer(offer_id):
    offer = Offer.query.get(offer_id)
    if not offer:
        return jsonify({"message": "Offer not found"}), 404

    data = request.json  # Получаем данные из тела запроса (JSON)
    offer.offer_id = data["offer_id "]
    offer.executor_id = data["executor_id"]
    offer.order_id = data["order_id"]


    db.session.commit()
    return jsonify({"message": "Offer updated successfully"}), 200




@app.route("/offers", methods=["POST"])
def create_offer():
    data = request.json
    if not data:
        return jsonify({"message": "No data provided"}), 400

    new_offer = Offer(
        id=data["id"],
        order_id=data["order_id"],
        executor_id=data["executor_id"]
    )


    db.session.add(new_offer)
    db.session.commit()

    return jsonify({"message": "Offer created successfully"}), 201





@app.route("/offers/<int:offer_id>", methods=["DELETE"])
def delete_offer(offer_id):
    offer = Offer.query.get(offer_id)
    if not offer:
        return jsonify({"message": "Offer not found"}), 404

    db.session.delete(offer)
    db.session.commit()

    return jsonify({"message": "Offer deleted successfully"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Создание таблиц базы данных
        load_data()  # Заполнение таблиц данными
    app.run(debug=True)
