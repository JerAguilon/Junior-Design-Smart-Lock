import json

import subprocess
import os

from configparser import ConfigParser

from run import app

env_mode = os.environ.get('SMARTLOCK_MODE', "DEV")
print("Exporting for SMARTLOCK_MODE={}".format(env_mode))

config = ConfigParser()
config.read('env/variables.ini')
if env_mode == 'DEV':
    config = config['DEV_RUNTIME_VARIABLES']
elif env_mode == 'PROD':
    config = config['PROD_RUNTIME_VARIABLES']
else:
    raise Exception("Invalid env_mode: {}".format(env_mode))

swagger_docs = app.test_client().get('/api/spec.json').json
with open('docs/api_docs.json', 'w') as fp:
    json.dump(swagger_docs, fp)

subprocess.run(
    'api-spec-converter --from=swagger_1 --to=swagger_2 --syntax=json ' +
    'docs/api_docs.json > static/api_docs_v2.json',
    shell=True
)
json_data = json.loads(open('static/api_docs_v2.json').read())
json_data['securityDefinitions'] = {
    "Authorization": {
        "type": "apiKey",
        "name": "Authorization",
        "in": "header"
    }
}


json_data['host'] = config['baseUrl']
json_data['info']['title'] = 'Junior Design Smartlock'
json_data['info']['description'] = \
    'Auto-generated API documentation for this project'
for endpoint, endpoint_val in json_data['paths'].items():
    for verb, endpoint_data in endpoint_val.items():
        endpoint_data['security'] = [{'Authorization': []}]

# Terrible hack due to bugs in flask-restful-swagger
json_data['definitions']['LockPasswordsResponse']['properties']['otp'][
    'items'] = {'$ref': '#definitions/LockPasswordResponse'}
json_data['definitions']['LockPasswordsResponse']['properties']['permanent'][
    'items'] = {'$ref': '#definitions/LockPasswordResponse'}

with open('static/api_docs_v2.json', 'w') as fp:
    json.dump(json_data, fp)

subprocess.run(
    'swagger-markdown -i static/api_docs_v2.json -o docs/api_docs.md',
    shell=True
)
subprocess.run(r"find docs/* \! -name 'api_docs.md' -delete", shell=True)

print("API Docs Updated in docs/api_docs.md")
