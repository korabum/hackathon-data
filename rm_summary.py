import json
import time
from datetime import datetime

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
        pred_table_bl[threshold] = [0,0,0,0,0,0,0,0]
        threshold += 5

    loop_time = time.time()
    whole_time = time.time()

    for trx in data:
        engine_decision = trx[3]
        engdec = None
        if(engine_decision == 'accept'):
            engdec = 0
        elif(engine_decision == 'challenge'):
            engdec = 1
        elif(engine_decision == 'deny'):
            engdec = 2

        h2o_score = trx[8]
        bl_score = trx[9]

        llabel = None
        if(trx[6] == 0 and trx[7] == 0):
            llabel = 0
        elif trx[6] in [1,3,4] or trx[7] in [1,2,3,4,6]:
            llabel = 1
        else:
            llabel = 2

        black = None
        white = None
        trxdate = datetime.strptime(trx[1], '%Y-%m-%d %H:%M:%S')
        if(trxdate < bldate):
            if(trx[2] != None):
                rules = trx[2][5:]
                split_rules = rules.split('-')
                for j in range(0, len(split_rules)):
    				split_rules[j] = split_rules[j].strip()

                for rule in split_rules:
                    black = 1 if 'CB' in rule and engine_decision == 'deny' else 0
                    white = 1 if 'CB' in rule and engine_decision == 'accept' else 0

        else:
            black = trx[4] and engine_decision == 'deny'
            white = trx[5] and engine_decision == 'accept'

        if black or white:
            blacklisted += 1 if black else 0
            whitelisted += 1 if white else 0

            threshold = 1000
            while(threshold >= 0):
                pred_table_h2o[threshold][0] += 1 if black == 1 else 0
                pred_table_h2o[threshold][1] += 1 if white == 1 else 0

                pred_table_bl[threshold][0] += 1 if black == 1 else 0
                pred_table_bl[threshold][1] += 1 if white == 1 else 0
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

            if(bl_score <= float(threshold)):
                pred_table_bl[threshold][2] += 1 if llabel == 0 else 0
                pred_table_bl[threshold][4] += 1 if llabel == 1 else 0
                pred_table_bl[threshold][6] += 1 if llabel == 2 else 0
            else:
                pred_table_bl[threshold][3] += 1 if llabel == 0 else 0
                pred_table_bl[threshold][5] += 1 if llabel == 1 else 0
                pred_table_bl[threshold][7] += 1 if llabel == 2 else 0

            threshold -= 5

    ret = []

    threshold = 1000

    while(threshold >= 0):
        acceptance_rate = float(pred_table_h2o[threshold][1] + pred_table_h2o[threshold][2] + pred_table_h2o[threshold][4] + pred_table_h2o[threshold][6]) / sum(pred_table_h2o[threshold])
        fraud_accuracy = float(pred_table_h2o[threshold][0] + pred_table_h2o[threshold][5]) / (pred_table_h2o[threshold][0] + pred_table_h2o[threshold][4] + pred_table_h2o[threshold][5])
        tmp = [threshold, pred_table_h2o[threshold][0], pred_table_h2o[threshold][1], pred_table_h2o[threshold][2], pred_table_h2o[threshold][3], pred_table_h2o[threshold][4], pred_table_h2o[threshold][5], pred_table_h2o[threshold][6], pred_table_h2o[threshold][7], acceptance_rate, fraud_accuracy]
        ret.append(tmp)

        threshold -= 5

    return json.dumps(ret)
