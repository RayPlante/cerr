#!/usr/bin/env python3
import re

# from tqdm import tqdm
from uuid import uuid4
import requests
from datetime import datetime, date
import cdcs
import base64
import os

# import openpyxl
from lxml import etree as ET
import importlib.util
import sys

import json


modules_needed = ["lxml", "requests"]
missing_modules = []

for name in modules_needed:
    if importlib.util.find_spec(name) is not None:
        # module was found, so proceed
        pass
    else:
        # module wasn't found, so add to missing
        missing_modules.append(name)

if len(missing_modules) > 0:
    print("The following required modules were not found:")
    print(missing_modules)
    print()
    print("Install them with:")
    print(f"  $ pip install --user {' '.join(missing_modules)}")
    sys.exit(1)


username = "changeme"
password = "CHANGEME"
# nmrr_url = "https://ce-i.nist.gov"
nmrr_url = "https://circular.nist.gov/"


def get_public_workspace_id():
    url = f"{nmrr_url}/rest/workspace/"
    r = requests.get(url, auth=(username, password), verify=False)
    r.raise_for_status()
    for res in r.json():
        if res["title"] == "Global Public Workspace":
            return res["id"]
    raise ValueError("Could not find global public workspace id")


def get_review_workspace_id():
    url = f"{nmrr_url}/rest/workspace/"
    r = requests.get(url, auth=(username, password), verify=False)
    r.raise_for_status()
    for res in r.json():
        if res["title"] == "review":
            return res["id"]
    raise ValueError("Could not find review workspace id")


template_id = cdcs.get_template(
    username, password, cert="", url=nmrr_url, title="res-md.xsd"
)["id"]
workspace_id = get_public_workspace_id()
review_id = get_review_workspace_id()


### GET RECORDS
# GET sur http://ce-i.nist.gov/rest/admin/data/

# Opening JSON file
f = open("0305records.json")

# returns JSON object as
# a dictionary
data = json.load(f)

# Iterating through the json
# list
for record in data:
    # set to new template !!!
    print(record["template"])
    record["template"] = template_id
    ## change PID
    record["xml_content"] = record["xml_content"].replace(
        "https://ce-i.nist.gov/", "https://circular.nist.gov/"
    )
    # )
    ## change global workspace id
    # if record["workspace"]:
    #     record["workspace"] = workspace_id
    # else:
    #     record["workspace"] = review_id

    print(record)

    # post draft

    # print(draft)
    # Upload resource
    print(f'**** Uploading new resource: {record["title"]}:')
    response = requests.post(
        f"{nmrr_url}/rest/admin/data/",
        data=record,
        verify=True,
        auth=(username, password),
    )
    print(response.json())
    record_id = response.json()["id"]
    # print(record_id)
    user_id = record["user_id"]
    # print(user_id)

    ## patch user ID
    print(f'##### patching owner id of record: {record["title"]}: #####')
    # f'**** Uploading new resource: {record["title"]}:'
    response2 = requests.patch(
        f"{nmrr_url}/rest/data/{record_id}/change-owner/{user_id}",
        verify=False,
        auth=(username, password),
    )
    print(response2.json())

    # response = requests.post( "http://192.168.40.111/curate/rest/admin/draft/", data=draft, verify=False, auth=(username, password))
    # res = cdcs.upload_data(nmrr_user, nmrr_pass, cert='',
    #                 url=nmrr_url, filen=xml_fname,
    #                 template_id=template_id)


# Closing file
f.close()
