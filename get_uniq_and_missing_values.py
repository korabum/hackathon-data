import json

def get_uniq_and_missing_values(json_data):
    data = json.loads(json_data)

    missing = [None, -999999999, -888888888]

    header = data[0]
    del data[0]

    ret = [['column_name', 'unique_values', 'missing_values']]

    for i in range(len(data[0])):
        entries = [rows[i] for rows in data]
        missing_values = sum(entries.count(value) for value in missing)
        unique_values = len(list(set(entries)))
        ret.append([str(header[i]), unique_values, missing_values])

    return ret
