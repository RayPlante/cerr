from xml.etree.ElementTree import Element, tostring

import core_main_app.access_control.api
import core_main_app.components.workspace.access_control
from cerr_curate_app.components.cerrdata import api as cerrdata_api
from cerr_curate_app.components.cerrdata.models import CerrData
from cerr_curate_app.views.user.forms import NameForm
from core_main_app.access_control.decorators import access_control
from core_main_app.commons import exceptions as exceptions
from core_main_app.components.template import api as template_api
from core_main_app.components.version_manager.models import VersionManager
from core_main_app.utils.xml import validate_xml_data
from xml_utils.xsd_tree.xsd_tree import XSDTree


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
    form = NameForm(request.POST)

    cd = form.cleaned_data
    form_string = convert_clean_data_to_xml("Resource", cd, "active")
    data = CerrData()
    data.title = cd["name"]
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
