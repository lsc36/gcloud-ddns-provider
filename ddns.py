#!/usr/bin/env python3
import time

from flask import Flask
from flask import request
from gcloud import dns

import config


def list_all(method, *args, **kwargs):
    l, page_token = method(*args, **kwargs)
    while page_token is not None:
        kwargs['page_token'] = page_token
        next_batch, page_token = method(*args, **kwargs)
        l.extend(next_batch)
    return l


def dns_update(hostname, ip):
    # retrieve zone and records
    client = dns.Client.from_service_account_json(
        config.gcloud_key,
        project=config.gcloud_project,
    )
    zones = list_all(client.list_zones)
    zone = [z for z in zones if z.name == config.zone][0]
    rrss = list_all(zone.list_resource_record_sets)

    # build changes
    changes = zone.changes()
    try:
        # find A records of hostname if exists, delete if outdated, return if IP
        # not changed
        rrs_old = [rrs for rrs in rrss
            if (rrs.name, rrs.record_type) == (hostname, 'A')][0]
        if rrs_old.rrdatas[0] == ip:
            return "nochg"
        changes.delete_record_set(rrs_old)
    except:
        pass
    # new record with TTL = 1
    changes.add_record_set(zone.resource_record_set(
        hostname, 'A', 1, [ip],
    ))

    # fire request, wait until done (60s timeout, poll every 5s)
    changes.create()
    timeout = 12
    while changes.status != 'done' and timeout > 0:
        time.sleep(5)
        timeout -= 1
        changes.reload()
    if timeout == 0:
        raise Exception("timeout")
    return "good"


app = Flask(__name__)


@app.route("/update")
def update_handler():
    try:
        username = request.args['username']
        password = request.args['password']
        hostname = request.args['hostname']
        myip = request.args['myip']
    except KeyError:
        return "badparam"
    if not username in config.users or config.users[username] != password:
        return "badauth"

    # FQDN
    if not hostname.endswith('.'):
        hostname += '.'

    try:
        return dns_update(hostname, myip)
    except Exception as e:
        print(e)
        return "911"


if __name__ == "__main__":
    app.run(**config.flask_params)
