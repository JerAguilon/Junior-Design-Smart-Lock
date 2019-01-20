import json

import subprocess

from run import app

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
    "api_key": {
        "type": "apiKey",
        "name": "Authorization",
        "in": "header"
    }
}
json_data['host'] = 'localhost:5000'
with open('static/api_docs_v2.json', 'w') as fp:
    json.dump(json_data, fp)

subprocess.run(
    'swagger-markdown -i static/api_docs_v2.json -o docs/api_docs.md',
    shell=True
)
subprocess.run(r"find docs/* \! -name 'api_docs.md' -delete", shell=True)

print("API Docs Updated in docs/api_docs.md")
