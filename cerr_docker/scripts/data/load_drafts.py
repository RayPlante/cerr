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


username = "admin"
# nmrr_user = "admin"
password = "qusIx0u6S@@7"
# nmrr_pass = 'admin'
nmrr_url = "https://ce-i.nist.gov/"
# nmrr_url = "http://192.168.40.111/"


template_id = cdcs.get_template(
    username, password, cert="", url=nmrr_url, title="res-md.xsd"
)["id"]

#### GET DRAfTS:
# GET sur http://ce-i.nist.gov/curate/rest/admin/draft/
# SAVE AS DRAfTS.JSON

# Opening JSON file
f = open("drafts.json")

# returns JSON object as
# a dictionary
data = json.load(f)

# Iterating through the json
# list
for draft in data:
    print(draft["template"])
    draft["template"] = template_id
    # set to new template !!!
    # post draft

    # print(draft)
    # Upload resource
    print(f'**** Uploading new resource: {draft["name"]}:')
    response = requests.post(
        f"{nmrr_url}curate/rest/admin/draft/",
        data=draft,
        verify=False,
        auth=(username, password),
    )
    print(response.json())
    # response = requests.post( "http://192.168.40.111/curate/rest/admin/draft/", data=draft, verify=False, auth=(username, password))
    # res = cdcs.upload_data(nmrr_user, nmrr_pass, cert='',
    #                 url=nmrr_url, filen=xml_fname,
    #                 template_id=template_id)


# Closing file
f.close()
