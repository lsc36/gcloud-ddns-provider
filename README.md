# gcloud-ddns-provider

Simple Python3 Flask app to provide DynDNS-like (Synology DSM-compatible) API
for updating Google Cloud DNS A records.

## Get Started

Copy `config_sample.py` to `config.py`, setup user accounts, provide Google
Cloud project ID, service account key (`key.json` at repository root by default)
and zone name. Then

    $ pip install -r requirements.txt
    $ ./ddns

Use WSGI for production.

## Usage

    GET /update?username=alice&password=foo&hostname=example.com&myip=192.0.2.1

## License

MIT
