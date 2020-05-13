from flask import Flask, request, jsonify 
from redis import Redis
from services.product_event_handler import emit_product_order

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

@app.route('/create', methods=['POST'])
def create():
    name = request.form['name']
    price = request.form['price']
    redis.mset({name: price})
    return jsonify({'name':name, 'price':price}), 201

@app.route('/buy', methods = ['POST'])
def buy():
    name = request.form['name']
    price = redis.get(name)
    emit_product_order(name)
    return jsonify({'receipt': 'Thanks for ordering! Your total comes to: ' + str(price)}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3002)