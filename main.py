from flask import Flask, jsonify, request

# functions
from rm_summary import *
from get_uniq_and_missing_values import *
# from read_sql import *
from super_rel_summary import *
from master_summary import *

app = Flask(__name__)

HOST = '127.0.0.1'
PORT = 5005

functions = [
    {
        'name': 'rm_summary',
        'url': "%s:%d/function/rm_summary" % (HOST, PORT)
    },
    #{
    #    'name': 'read_sql',
    #    'url': "%s:%d/function/read_sql" % (HOST, PORT)
    #},
    {
        'name': 'master_summary',
        'url': "%s:%d/function/master_summary" % (HOST, PORT)
    },
    {
        'name': 'super_rel_summary',
        'url': "%s:%d/function/super_rel_summary" % (HOST, PORT)
    },
    {
        'name': 'get_uniq_and_missing_values',
        'url': "%s:%d/function/get_uniq_and_missing_values" % (HOST, PORT)
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
    # TODO
    return 'Manual of ' + name + '\n'

@app.route('/function/<name>', methods = ['POST'])
def do_function(name):
    if name == 'rm_summary':
        return jsonify(rm_summary(request.data))
    elif name == 'get_uniq_and_missing_values':
        return jsonify((request.data))
    #elif name == 'read_sql':
    #    return jsonify(read_sql(request.data))
    elif name == 'master_summary':
        return jsonify(master_summary(request.data))
    elif name == 'super_rel_summary':
        return jsonify(super_rel_summary(request.data))

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
