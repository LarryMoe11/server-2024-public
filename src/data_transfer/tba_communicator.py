#!/usr/bin/env python3
# Copyright (c) 2022 FRC Team 1678: Citrus Circuits
"""Sends web requests to The Blue Alliance (TBA) APIv3.

Caches data to prevent duplicate data retrieval from the TBA API.
API documentation: https://www.thebluealliance.com/apidocs/v3.
"""

import requests

from data_transfer import database
import utils
import logging

log = logging.getLogger(__name__)


def tba_request(api_url):
    """Sends a single web request to the TBA API v3 api_url is the suffix of the API request URL

    (the part after '/api/v3').
    """
    log.info(f"tba request from {api_url} started")
    full_url = f"https://www.thebluealliance.com/api/v3/{api_url}"
    request_headers = {"X-TBA-Auth-Key": get_api_key()}
    db = database.Database()
    cached = db.get_tba_cache(api_url)
    # Check if cache exists
    if cached:
        request_headers["If-None-Match"] = cached["etag"]
    print(f"Retrieving data from {full_url}")
    log.info(f"tba request from {api_url} finished")
    try:
        request = requests.get(full_url, headers=request_headers)
    except requests.exceptions.ConnectionError:
        log.warning("Error: No internet connection.")
        return None
    # A 200 status code means the request was successful
    # 304 means that data was not modified since the last timestamp
    # specified in request_headers['If-Modified-Since']
    if request.status_code == 304:
        return cached["data"]
    if request.status_code == 200:
        db.update_tba_cache(request.json(), api_url, request.headers["etag"])
        return request.json()
    raise Warning(f"Request failed with status code {request.status_code}")


def get_api_key() -> str:
    with open(utils.create_file_path("data/api_keys/tba_key.txt")) as file:
        api_key = file.read().rstrip("\n")
    return api_key
