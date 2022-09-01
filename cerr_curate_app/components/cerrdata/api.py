from xml.etree.ElementTree import Element, tostring

import core_main_app.access_control.api
import core_main_app.components.workspace.access_control
from cerr_curate_app.components.cerrdata import api as cerrdata_api
from cerr_curate_app.components.cerrdata.models import CerrData
from cerr_curate_app.views.user.forms import EditForm
from core_main_app.access_control.decorators import access_control
from core_main_app.commons import exceptions as exceptions
from core_main_app.components.template import api as template_api
from core_main_app.components.version_manager.models import VersionManager
from core_main_app.utils.xml import validate_xml_data
from xml_utils.xsd_tree.xsd_tree import XSDTree
import logging
import xml.etree.ElementTree as ET
from collections import OrderedDict

from cerr_curate_app.components.curate_data_structure import api as draft_api
from cerr_curate_app.components.curate_data_structure.models import CurateDataStructure
from core_main_app.access_control.api import can_read_id, can_write, AccessControlError
from core_main_app.access_control.decorators import access_control
from core_main_app.components.template import api as template_api
from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)

from xml_to_dict import XMLtoDict


def render_xml(draftdoc):
    roottag = list(draftdoc.keys())[0]
    root = ET.Element(roottag)
    _load_children(root, draftdoc[roottag])
    return ET.tostring(root).decode()


def _load_children(parent, data):
    for key, value in data.items():
        if key.startswith("@"):
            parent.attrib[key[1:]] = str(value)
        elif key == "#text":
            if isinstance(value, (tuple, list)):
                value = " ".join([str(v) for v in value])
            parent.text = str(value)
        else:
            if not isinstance(value, (tuple, list)):
                value = [value]
            for val in value:
                child = ET.SubElement(parent, key)
                if isinstance(val, dict):
                    _load_children(child, val)
                else:
                    child.text = str(val)


def convert_clean_data_to_xml(tag, clean_data, status):
    """
    Convert xml string to clean_data object
    :param tag:
    :param clean_data:
    :param status:
    :return:
    """
    elem = Element(tag)
    elem.set("status", status)
    for key, val in clean_data.items():
        # create an Element
        # class object
        child = Element(key)
        child.text = str(val)
        elem.append(child)

    return tostring(elem)


def draft_to_data(draft):
    """
    Convert a draft object into a data object
    :param draft:
    :return:
    """
    form_string = draft.form_string
    data = CerrData()
    data.title = data.name
    template = draft.template
    data.user_id = draft.user  # process the data in form.cleaned_data as required
    # set content
    data.xml_content = form_string
    data.template = template
    # save data
    data = cerrdata_api.upsert(data)
    return data


def save_as_cerr_data(request):
    """
    Save form as data
    :param request:
    :return:
    """
    form = EditForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        form_string = convert_clean_data_to_xml("Resource", cd, "active")
        data = CerrData()
        data.title = cd["title"]
        version_manager = VersionManager.get_all()
        version_manager = version_manager.filter(
            _cls="VersionManager.TemplateVersionManager"
        )
        template = template_api.get(str(version_manager[0].current), request)
        data.template = template
        data.user_id = str(
            request.user.id
        )  # process the data in form.cleaned_data as required
        # set content
        data.xml_content = form_string
        # save data
        data = cerrdata_api.upsert(data, request)


@access_control(core_main_app.access_control.api.can_request_write)
def upsert(data, request=None):
    """Save or update the data.

    Args:
        data:
        request:

    Returns:

    """
    if data.xml_content is None:
        raise exceptions.ApiError("Unable to save data: xml_content field is not set.")
    ##TODO:REMOVE HERE
 #   data.xml_content = '<Resource xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://schema.nist.gov/xml/ce-res-md/1.0wd2 ce-res-md.xsd" xmlns="http://schema.nist.gov/xml/ce-res-md/1.0wd2" xmlns:rsm="http://schema.nist.gov/xml/ce-res-md/1.0wd2" status="active"><identity><title>Clean record</title></identity><providers><publisher>publisher</publisher></providers><content><description>A record well formed</description><subject>Full record</subject><landingPage>http://www.google.fr</landingPage><primaryAudience>researchers</primaryAudience></content><role><database><database_label>database name</database_label></database></role><applicability><productClass><electronics>electronics</electronics><packaging>packaging: glass</packaging><solar_panels>solar panels</solar_panels></productClass><lifecyclePhase><product_design>product design</product_design><recycling>recycling</recycling><recycling>recycling: chemical</recycling></lifecyclePhase><materialType><glass>glass</glass><concrete>concrete</concrete></materialType></applicability></Resource>'

   # draft_api.unrender_xml(data.xml_content)
    check_xml_file_is_valid(data, request=request)
    return data.cerr_convert_and_save()


def check_xml_file_is_valid(data, request=None):
    """Check if xml data is valid against a given schema.

    Args:
        data:
        request:

    Returns:

    """
    template = data.template

    try:
        xml_tree = XSDTree.build_tree(data.xml_content)
    except Exception as e:
        raise exceptions.XMLError(str(e))
    try:
        xsd_tree = XSDTree.build_tree(template.content)
    except Exception as e:
        raise exceptions.XSDError(str(e))
    error = validate_xml_data(xsd_tree, xml_tree, request=request)
    if error is not None:
        raise exceptions.XMLError(error)
    else:
        return True
