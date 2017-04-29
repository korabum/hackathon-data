import json
import time
from datetime import datetime

def man_rm_summary():
    response = {}
    response['data_type'] = 'json'
    response['field'] = {'data':['bruce_id','blacklist','whitelist','h2o_score','learning_label']}
    return json.dumps(response)

def rm_summary(json_data):
    data = json.loads(json_data)
    pred_table_h2o = {}
    pred_table_bl = {}
    blacklisted = 0
    whitelisted = 0
    bldate = datetime.strptime('2015-09-07 13:29:09', '%Y-%m-%d %H:%M:%S')

    threshold = 0
    while(threshold <= 1000):
        pred_table_h2o[threshold] = [0,0,0,0,0,0,0,0]
        threshold += 5

    loop_time = time.time()
    whole_time = time.time()

    for trx in data:
        black = trx[1]
        white = trx[2]
        h2o_score = trx[3]
        llabel = trx[4]

        if black == 1 or white == 1:
            blacklisted += 1 if black == 1 else 0
            whitelisted += 1 if white == 1 else 0

            threshold = 1000
            while(threshold >= 0):
                pred_table_h2o[threshold][0] += 1 if black == 1 else 0
                pred_table_h2o[threshold][1] += 1 if white == 1 else 0

                threshold -= 5

            continue

        threshold = 1000
        while(threshold >= 0):
            if(h2o_score <= float(threshold)):
                pred_table_h2o[threshold][2] += 1 if llabel == 0 else 0
                pred_table_h2o[threshold][4] += 1 if llabel == 1 else 0
                pred_table_h2o[threshold][6] += 1 if llabel == 2 else 0
            else:
                pred_table_h2o[threshold][3] += 1 if llabel == 0 else 0
                pred_table_h2o[threshold][5] += 1 if llabel == 1 else 0
                pred_table_h2o[threshold][7] += 1 if llabel == 2 else 0

            threshold -= 5

    ret = []

    threshold = 1000

    while(threshold >= 0):
        acceptance_rate = float((pred_table_h2o[threshold][1] + pred_table_h2o[threshold][2] + pred_table_h2o[threshold][4])) / sum(pred_table_h2o[threshold])
        fraud_accuracy = float(pred_table_h2o[threshold][0] + pred_table_h2o[threshold][5]) / float(pred_table_h2o[threshold][0] + pred_table_h2o[threshold][4] + pred_table_h2o[threshold][5])
        tmp = [threshold, pred_table_h2o[threshold][0], pred_table_h2o[threshold][1], pred_table_h2o[threshold][2], pred_table_h2o[threshold][3], pred_table_h2o[threshold][4], pred_table_h2o[threshold][5], "%1.5f" % acceptance_rate, "%1.5f" % fraud_accuracy]
        ret.append(tmp)

        threshold -= 5

    return json.dumps(ret)
