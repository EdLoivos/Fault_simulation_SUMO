import json
import xmltodict
import math
import sys, getopt, os
import sumolib

#curl -H "Content-Type: application/json" -d '{"bus_id": "2B_4", "trip_id":"XX;1","lat": -8, "lon": -8,"ts": 1, "ng":["2C_4", "3B_4"]}' http://localhost:3000/submit

#net = sumolib.net.readNet('osm.net.xml')

file_name = None
out_name = None
data = {}

try:
    opts, args = getopt.getopt(sys.argv[1:],"f:o:",["file=", "out="])
except getopt.GetoptError as err:
    print(err)
    print('HINT: main.py -t <arq topologia>')
    print('MORE INFO: main.py --help')
    sys.exit(1)
for opt, arg in opts:
    if opt in ("-f", "--file"):
        file_name = arg
    elif opt in ("-o", "--out"):
        out_name = arg

if(file_name == None):
    print("Error: Missing Argument")
    print('HINT: main.py -f <fcd-output file>')
    print("  O parâmetro -f é obrigatório!!!")
    sys.exit(1)


if(out_name == None):
    print("Error: Missing Argument")
    print('HINT: main.py -o <output file>')
    print("  O parâmetro -o é obrigatório!!!")
    sys.exit(1)



with open(file_name) as xml_file:
    data_dict = xmltodict.parse(xml_file.read())
    for key in data_dict["fcd-export"]["timestep"]:
        data[key["@time"]] = []
        if "vehicle" in key:
            if isinstance(key["vehicle"], list):
                for car in key["vehicle"]:
                    lon = float(car["@x"])
                    lat = float(car["@y"])

                    msg = { "bus_id": car["@id"], "lat": lat, "lon": lon, "spd" : float(car["@speed"])*3.6}
                    data[key["@time"]] .append(msg)
            else:
                lon = float(car["@x"])
                lat = float(car["@y"])

                msg = { "bus_id": key["vehicle"]["@id"], "lat": lat, "lon": lon, "spd" : float(key["vehicle"]["@speed"])*3.6}
                data[key["@time"]] .append(msg)

out = open( out_name, "w")
json.dump(data, out,indent = 4)
out.close()
