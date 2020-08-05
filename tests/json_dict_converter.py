import json
from collections import OrderedDict


data = json.loads('{"foo":1, "bar": 2}', object_pairs_hook=OrderedDict)
print(data)
print(json.dumps(data, indent=4))

