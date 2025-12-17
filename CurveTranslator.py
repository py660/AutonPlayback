import json
fname = input("File path/name? ")
out = []
fin = open(fname, "rb")
data = fin.read().decode('utf-8', errors='ignore')
pathdata = json.loads(data.split("#PATH.JERRYIO-DATA ")[-1].split("#PATH.JERRYIO-DATA\0")[-1])
path = pathdata["paths"][0]["segments"]
for rawsegment in path:
    segment = rawsegment["controls"]
    if len(segment) == 4:
        out.append(f"CURVE: ({segment[0]['x']},{segment[0]['y']}) | ({segment[1]['x']},{segment[1]['y']}) | ({segment[2]['x']},{segment[2]['y']}) | ({segment[3]['x']},{segment[3]['y']})")
    elif len(segment) == 2:
        out.append(f"CURVE: ({segment[0]['x']},{segment[0]['y']}) | ({2*segment[0]['x']/3 + segment[1]['x']/3},{2*segment[0]['y']/3 + segment[1]['y']/3}) | ({segment[0]['x']/3 + 2*segment[1]['x']/3},{segment[0]['y']/3 + 2*segment[1]['y']/3}) | ({segment[1]['x']},{segment[1]['y']})")
    else:
        raise Exception("Path data includes a segment with only one point ?!?!?")
    
fout = open("spline0.txt", "w")
fout.write("\n".join(out))
print("Done!")

""" # Format:
# Comment Blah Blah
CURVE: [START_POINT] | [CTRL_POINT1] | [CTRL_POINT1] | [END_POINT]
# Ex. CURVE: (2.23,0.34) | (3.35,-2) | (2.3,5.4) | (6.5)
CMD: SET_VELOCITY = {1-100 (%)}
CMD: TURN_HEADING = {0-359 (deg)}
CMD: ROUTINE = {PICK_UP, PUT_DOWN, STORE, PUT_TOP, PUT_MIDDLE, STOP_INTAKE}
CMD: DELAY = {0-INF (msec)}
"""