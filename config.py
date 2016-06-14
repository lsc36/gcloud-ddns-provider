import os

base_dir = os.path.dirname(os.path.realpath(__file__))

flask_params = {
    'host': '127.0.0.1',
    'port': 5000,
    'debug': True,
}

users = {
    'alice': 'foo',
}

zone = 'your-zone-name'

gcloud_project = 'your-project-id'

gcloud_key = os.path.join(base_dir, 'key.json')
