import json
from deepdiff import DeepDiff
import sys, getopt, os
import geopy.distance

file1_name = None
file2_name = None
out_name = None
log_file = None
data = {}
data_pos = {}

try:
    opts, args = getopt.getopt(sys.argv[1:],"b:a:o:",["base=", "aux=", "out="])
except getopt.GetoptError as err:
    print(err)
    print('HINT: main.py -t <arq topologia>')
    print('MORE INFO: main.py --help')
    sys.exit(1)
for opt, arg in opts:
    if opt in ("-b", "--base"):
        file1_name = "demo_icarai/rch_"+arg +".json"
        log_file = file1_name.split(".")+"_log.txt"
    elif opt in ("-a", "--aux"):
        file2_name = arg
    elif opt in ("-o", "--out"):
        out_name = arg


if(file1_name == None):
    print("Error: Missing Argument")
    print('HINT: main.py -b <fcd-output file>')
    print("  O parâmetro -b é obrigatório!!!")
    sys.exit(1)


with open(log_file) as log:
    fault_ids = log.read().splitlines()
    print("log loaded")
with open(file1_name) as base_file:
    base_data = json.load(base_file)
    print("base loaded")
with open(file2_name) as fault_file:
    real_data = json.load(fault_file)
    print("real loaded")




for ts in real_data:
    data[ts] = []
    data_pos[ts] = {}
    for line in real_data[ts]:
        if not line["bus_id"] in fault_ids:
            line["class"] = "T"
            data[ts].append(line)
        else:
            data_pos[ts][line["bus_id"]] = (line["lon"], line["lat"])


for ts in base_data:
    for line in base_data[ts]:
        if line["bus_id"] in fault_ids:
            if line["bus_id"] in data_pos[ts]:
                if geopy.distance.geodesic((line["lon"],line["lat"]), data_pos[ts][line["bus_id"]]).m <= 75:
                    line["class"] = "T"
                else:
                    line["class"] = "F"
            else:
                line["class"] = "F"
            data[ts].append(line)



out = open(out_name, 'w')
json.dump(data, out,indent = 4)
out.close()
