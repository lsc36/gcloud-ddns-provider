import os

base_dir = os.path.dirname(os.path.realpath(__file__))

users = {
    'alice': 'foo',
}

zone = 'your-zone-name'

gcloud_project = 'your-project-id'

gcloud_key = os.path.join(base_dir, 'key.json')
