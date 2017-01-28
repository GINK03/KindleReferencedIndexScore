import json

for k, v in json.loads(open('./linker_tags.json').read()).items():
    print(k)
