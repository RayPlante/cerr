#!/usr/bin/env python3

import re
from tqdm import tqdm
from uuid import uuid4
import requests
from datetime import datetime, date
import cdcs
import base64
import os
import openpyxl
from lxml import etree as ET
import importlib.util
import sys

modules_needed = ["lxml", "openpyxl", "requests", "tqdm"]
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


# https://stackoverflow.com/a/7160778/1435788
url_regex = re.compile(
    r"^(?:http|ftp)s?://"  # http:// or https://
    # domain...
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
    r"localhost|"  # localhost...
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
    r"(?::\d+)?"  # optional port
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)

failed_records = []

nmrr_user = "admin"
# nmrr_user = 'admin'
# nmrr_pass = 'qusIx0u6S@@7'
nmrr_pass = "admin"
# nmrr_url = "https://ce-i.nist.gov/"
nmrr_url = "http://192.168.0.205/"

CE_NAMESPACE = "http://schema.nist.gov/xml/ce-res-md/1.0wd2"
CE = f"{{{CE_NAMESPACE}}}"

XSI_NAMESPACE = "http://www.w3.org/2001/XMLSchema-instance"
XSI = f"{{{XSI_NAMESPACE}}}"
nsmap = {None: CE_NAMESPACE, "xsi": XSI_NAMESPACE, "rsm": CE_NAMESPACE}


def proc_val(val):
    if val is not None:
        return val.strip()
    else:
        return val


def get_public_workspace_id():
    url = f"{nmrr_url}/rest/workspace/"
    r = requests.get(url, auth=(nmrr_user, nmrr_pass), verify=False)
    r.raise_for_status()
    for res in r.json():
        if res["title"] == "Global Public Workspace":
            return res["id"]
    raise ValueError("Could not find global public workspace id")


def make_record_public(record_id, public_workspace_id):
    url = f"{nmrr_url}/rest/data/{record_id}/assign/{public_workspace_id}"
    r = requests.patch(url, auth=(nmrr_user, nmrr_pass), verify=False)
    r.raise_for_status()
    return r.json()


script_path = os.path.dirname(os.path.realpath(__file__))
print(script_path)
xsd_path = os.path.join(script_path, "ce-res-md.xsd")

template_id = cdcs.get_template(
    nmrr_user, nmrr_pass, cert="", url=nmrr_url, title="res-md.xsd"
)["id"]
print("template_id")
print(template_id)
workspace_id = get_public_workspace_id()
print("workspace_id")
print(workspace_id)

with open(xsd_path, "r") as f:
    xmlschema_doc = ET.parse(f)
    xmlschema = ET.XMLSchema(xmlschema_doc)

    for title in os.listdir("./xmls"):
        print(title)
        xml_fname = os.path.join(script_path, "xmls", f"{title}")

        try:
            # Upload resource
            print(f"**** Uploading new resource: {title}:")
            res = cdcs.upload_data(
                nmrr_user,
                nmrr_pass,
                cert="",
                url=nmrr_url,
                filen=xml_fname,
                template_id=template_id,
            )
            print(f'Record "{title}"/{res["id"]} uploaded')
            pub_res = make_record_public(res["id"], workspace_id)
            print(f'Record "{title}"/{res["id"]} published')

        except Exception as e:
            print(f"**** COULD NOT VALIDATE {title}:")
            print(f"     {str(e)}")
            failed_records.append((title, f"Error: {str(e)}"))
            continue

if len(failed_records) > 0:
    for f in failed_records:
        print(f"Row {f[0]}:  {f[1]}  -----  {f[2]}")
    print(f"{len(failed_records)} records could not be uploaded; see above for details")
