from flask import Flask, json, request
import sqlite3
import pika
from settings import TABLE_NAME, DB_NAME

app = Flask(__name__)
connection = sqlite3.connect(DB_NAME, check_same_thread=False)
cursor = connection.cursor()


@app.route('/')
def index():
    statement = f"SELECT * FROM {TABLE_NAME}"
    cursor.execute(statement)
    result = cursor.fetchall()
    print(result)
    response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/sale/', methods=['POST'])
def sale():
    data = request.form   # приняли словарь который передали в джанго
    phone = data['phone']
    price = data['price']
    is_sale = True
    status = 'DONE'
    statement = f"INSERT INTO {TABLE_NAME}(phone,price,is_sale,status) values (?,?,?,?)"
    cursor.execute(statement, (phone, price, is_sale, status))
    response = app.response_class(
        response=json.dumps({'STATUS': 'OK'}),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/repair/', methods=['POST'])
def repair():
    data = request.form
    phone = data['phone']
    price = data['price']
    is_sale = False
    status = 'IN PROCESS'
    statement = f"INSERT INTO {TABLE_NAME}(phone,price,is_sale,status) values (?,?,?,?)"
    cursor.execute(statement, (phone, price, is_sale, status))

    # Публикуем сообщение; код выполнится только если запущет rabbit
    connection = pika.BlockingConnection(pika.ConnectionParameters(  # подключение к очереди
        'localhost'))
    channel = connection.channel()  # создание канала
    channel.queue_declare(queue='repair')  # создание очереди
    channel.basic_publish(exchange='',  # размещаем сообщения
                          routing_key='repair',
                          body=phone)
    connection.close()  # закрыли подключение; теперь сообщение находится в очереди

    response = app.response_class(
        response=json.dumps({'STATUS': 'OK'}),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/change/', methods=['POST'])
def change_status():
    data = request.form
    phone = data['phone']
    status = data['status']
    print(status)
    statement = f"UPDATE {TABLE_NAME} set status = ? where phone = ?"
    cursor.execute(statement, (status, phone))

    response = app.response_class(
        response=json.dumps({'STATUS': 'OK'}),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run(debug=True)
