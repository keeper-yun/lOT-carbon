

import csv
import requests

headers = {
    'User-Agent': ')Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0\
     Safari/537.36 Edg/120.0.0.0'
}

url = f'http://localhost:8181/monitoring/find'



resp = requests.get(url, headers=headers)
data = resp.json()

def writedata(num):
    with open(f'factory{num}.csv', 'w', encoding='utf-8', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([ u'recordId',u'co2_Level',u'n2o_Level', u'ch4_Level', u'co2_Flow', u'co2_Output', u'n2o_Output', u'ch4_Output',u'factoryId',  u'timestamp'])

        for i in data:
            if i.get('factoryId') == num:
                data_list = []
                recordId = i.get('recordId')
                co2_Level = i.get('co2_Level')
                n2o_Level = i.get('n2o_Level')
                ch4_Level = i.get('ch4_Level')
                co2_Flow = i.get('co2_Flow')
                co2_Output = i.get('co2_Output')
                n2o_Output = i.get('n2o_Output')
                ch4_Output = i.get('ch4_Output')
                factoryId = i.get('factoryId')
                timestamp = i.get('timestamp')

                data_list.append(recordId)
                data_list.append(co2_Level)
                data_list.append(n2o_Level)
                data_list.append(ch4_Level)
                data_list.append(co2_Flow)
                data_list.append(co2_Output)
                data_list.append(n2o_Output)
                data_list.append(ch4_Output)
                data_list.append(factoryId)
                data_list.append(timestamp)

                csv_writer.writerow(data_list)

for a in range(1,5):
    writedata(a)


