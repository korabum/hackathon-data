from flask import Flask, jsonify

app = Flask(__name__)

HOST = '127.0.0.1'
PORT = 5005

functions = [
    {
        'name': 'test',
        'url': "%s:%d/function/test" % (HOST, PORT)
    }
]

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/functions')
def list_functions():
    return jsonify(functions)

@app.route('/function/<name>', methods = ['GET'])
def get_function(name):
    return 'Manual of ' + name + '\n'

@app.route('/function/<name>', methods = ['POST'])
def do_function(name):
    result = {'result': name}
    return jsonify(result)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
