from flask import Flask

app = Flask(__name__)

app.config.from_object('config')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/geocode', methods=['GET'])
def geocode():
    return 'geocode'


@app.route('/reverse-geocode', methods=['GET'])
def reverse_geocode():
    return 'reverse geocode'

# @app.route('/tasks')

