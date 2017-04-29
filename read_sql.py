#!flask/bin/python
import MySQLdb
import json
from datetime import datetime
import rm_summary as rs

def get_req():
    request = {'query': ['select', 'from', 'where','limit']}
    return request

def config_sql():
    # host = config['host']
    # user = config['user']
    # passwd = config['pass']
    # schema = config['schema']
    host = '127.0.0.1'
    user = 'root'
    passwd = ''
    schema = 'bruce-ui_production'

    db = MySQLdb.connect(host,user,passwd,schema)
    return db

def man_read_sql():
    response = {}
    response['data_type'] = 'json'
    response['field'] = ['select','from','where','limit']
    return json.dumps(response)

def read_sql(request):
    db = config_sql()
    cursor = db.cursor()

    select = request['select']
    table = request['from']
    where = request['where']
    limit = request['limit']

    sql = "SELECT %s FROM %s" % (select, table)
    sql += " WHERE %s" % (where) if where != None else ""
    sql += " LIMIT %i" % (limit) if limit != None else ""

    cursor.execute(sql)
    results = [[x.strip() for x in select.split(',')]]
    results += cursor.fetchall()
    response = json.dumps(results, default=json_serial)
    print(response)
    return response

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = datetime.strftime(obj,"%Y-%m-%d %H:%M:%S")
        return serial
    raise TypeError ("Type not serializable")
