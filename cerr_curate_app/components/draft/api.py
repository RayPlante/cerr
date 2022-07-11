import logging
import xml.etree.ElementTree as ET
from collections import OrderedDict

from cerr_curate_app.components.draft import api as draft_api
from cerr_curate_app.components.draft.models import Draft
from core_main_app.access_control.api import can_read_id, can_write, AccessControlError
from core_main_app.access_control.decorators import access_control
from core_main_app.components.template import api as template_api
from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)

from xml_to_dict import XMLtoDict

logger = logging.getLogger(__name__)


def get_all_by_user_id(user_id):
    """Returns all drafts with the given user

    Args:
        user:
    Returns:
        Draft:
    """
    return Draft.get_all_by_user_id(user_id)


@access_control(can_read_id)
def get_by_id(draft_id, user):
    """
    Returns the Draft data object with the given ID
    :param str draft_id:  the ID for the desired draft
    :param User user:     the user making the request; used to authorize the
                          creation of the draft.

    :return: the requested Draft object
    :rtype:  Draft
    """
    return Draft.get_by_id(draft_id)


@access_control(can_write)
def upsert(draft, user, id=None):
    """
    Save a draft data object.  If id attribute is set or the id is provided, the object will
    replace the previously-saved draft having that ID.

    :param Draft draft:  the draft object to save
    :param User user:    the user making the request; used to authorize the
                         creation of the draft.
    :param str id:       the ID of the previously saved draft to replace; if None,
                         a new draft object is created with a new ID.

    :return: the saved draft object; if id attribute will be set if the draft is new.
    :rtype:  Draft
    """
    if id:
        # We link the data with the draft then save it
        draft.id = id
    return draft.save_object()


def save_new_draft(draftdoc, name, request):
    """
    save a new draft XML document with the given name
    :param dict draftdoc:   the draft XML document as an "xml_to_dict" dictionary
    :param str      name:   the mnemonic name to save the draft under
    :param HttpRequest request:  the HTTP request that delivered the draft; this is used
                            to authorize the creation of the draft.
    """
    # convert the dictionary to an XML-encoded string
    form_string = render_xml(draftdoc)

    # get the current registry template
    version_manager = TemplateVersionManager.get_all()
    version_manager = version_manager.filter(
        _cls="VersionManager.TemplateVersionManager"
    )
    template = template_api.get(str(version_manager[0].current), request)

    # create the Draft object and save
    draft = Draft(
        user_id=str(request.user.id),
        template=template,
        name=name,
        form_data=form_string,
    )
    upsert(draft, request.user)
    return draft


def save_updated_draft(draftdoc, id, request):
    """
    save a new draft XML document with the given name
    :param dict draftdoc:   the draft XML document as an "xml_to_dict" dictionary
    :param str      name:   the mnemonic name to save the draft under
    :param HttpRequest request:  the HTTP request that delivered the draft; this is used
                            to authorize the creation of the draft.
    """
    # convert the dictionary to an XML-encoded string
    form_string = render_xml(draftdoc)

    # retrieve previous draft object
    draft = get_by_id(id, request.user)
    if not draft:
        return None

    # update the draft
    draft.form_data = form_string
    upsert(draft, request.user)
    return draft


def unrender_xml(xmlstr):
    """
    Convert an XML-formatted string to an "xml_to_dict" dictionary
    """
    return _to_dict(ET.fromstring(xmlstr))


def _to_dict(t):
    # based on xml_to_dict (https://github.com/xthehatterx/xml_to_dict)
    d = OrderedDict([(t.tag, OrderedDict() if t.attrib else None)])
    children = list(t)
    if children:
        dd = OrderedDict()
        for dc in map(_to_dict, children):
            for k, v in dc.items():
                if k not in dd:
                    dd[k] = []
                dd[k].append(v)
        d = OrderedDict(
            [
                (
                    t.tag,
                    OrderedDict(
                        [(k, v[0] if len(v) == 1 else v) for k, v in dd.items()]
                    ),
                )
            ]
        )
    if t.attrib:
        d[t.tag].update(("@" + k, v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]["#text"] = text
        else:
            d[t.tag] = text
    return d


def _render_xml(draftdoc, roottag="Resource"):
    """
    Convert an XML document stored as a "xml_to_dict" dictionary to an XML-formatted string

    :param dict draftdoc:   the XML data dictionary to convert
    :param str  roottag:    the root element tag to use

    :return:  the data as an XML-formatted string
    :rtype: str
    """
    root = ET.Element(roottag)

    # this is a placeholder implementation; to be replaced!
    for key, value in draftdoc:
        child = ET.Element(key)
        if isinstance(value, str):
            child.text = str(val)
            elem.append(child)

    return ET.tostring(elem)


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
