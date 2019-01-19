import json

import sys
import subprocess

from run import app

#subprocess.run(['swagger2markdown', '-i', 'docs/api_docs.json', '-o', 'docs/api_docs.md'])
swagger_docs = app.test_client().get('/api/spec.json').json
with open('docs/api_docs.json', 'w') as fp:
    swagger_docs['info'] = 'Documentation for smart lock'
    json.dump(swagger_docs, fp)

