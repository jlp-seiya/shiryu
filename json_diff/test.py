import mydiff
import json

x = json.loads('{ "a":"b", "c": { "c":1}, "d":[1] }')
y = json.loads('{ "a":1, "b":[1,2], "d":[1,3,2],}')
mydiff.diff(x,y)

print("")
print("")
print("")
output = mydiff.diff_html(x,y)
print(output)
