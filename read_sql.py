#!flask/bin/python
import MySQLdb
import json
from datetime import datetime
import rm_summary as rs

def get_req():
    request = {'query': ['select', 'from', 'where','limit'], 'config': ['host','user','pass','schema']}
    return request

def config_sql(config):
    host = config['host']
    user = config['user']
    passwd = config['pass']
    schema = config['schema']

    db = MySQLdb.connect(host,user,passwd,schema)
    return db

def execute(request):
    db = config_sql(request['config'])
    cursor = db.cursor()

    select = request['query']['select']
    table = request['query']['from']
    where = request['query']['where']
    limit = request['query']['limit']

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
