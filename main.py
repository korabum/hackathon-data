from flask import Flask, jsonify, request

# functions
from rm_summary import rm_summary

app = Flask(__name__)

HOST = '127.0.0.1'
PORT = 5005

functions = [
    {
        'name': 'rm_summary',
        'url': "%s:%d/function/rm_summary" % (HOST, PORT)
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
    if name == 'rm_summary':
        return jsonify(rm_summary(request.data))

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
