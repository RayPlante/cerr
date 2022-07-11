"""
The module that provides the user views for creating and editing a draft record.  
"""
from collections import OrderedDict
from collections.abc import Mapping
import json, re, pdb

from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views.generic import View
from cerr_curate_app.components.material import api as material_api
from .forms import StartForm, EditForm
from ...components.draft import api as draft_api

TMPL8S = "cerr_curate_app/user/draft/"


def start(request):
    """
    Present or handle the starting form for creating a record
    """
    if request.method == "POST":
        form = StartForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                draft = start_to_draftdoc(
                    form.cleaned_data, request.FILES.get("xmlfile")
                )
                name = draft["name"]
                del draft["name"]
                draft_obj = draft_api.save_new_draft(draft, name, request)
                return HttpResponseRedirect(reverse("edit", args=(draft_obj.id,)))
            except DetectedFailure as ex:
                return handleFailure(ex)
            except draft_api.AccessControlError as ex:
                return handleFailure(Http401(message=str(ex)))
    else:
        form = StartForm()

    return render(request, TMPL8S + "start.html", {"startform": form})


class EditView(View):
    """
    present and accept updates from an editable version of a draft
    On GET, retrieve a requested draft and load it into the edit form.
    On POST, accept the updated draft and save it.
    """

    def __init__(self, **kwargs):
        self.assets = self._load_assets()

        super().__init__(**kwargs)

    def get(self, request, **kwargs):
        draft_id = kwargs["draft_id"]
        form = EditForm(request.POST)

        try:
            draft_obj = draft_api.get_by_id(draft_id, request.user)
            draft_doc = draft_api.unrender_xml(draft_obj.form_data)
        except draft_api.AccessControlError as ex:
            return handleFailure(Http401(message=str(ex)))
        form = EditForm(data=draftdoc_to_edit(draft_doc, draft_obj.id))

        restype = _get_restype(draft_doc, Resource.schemauri)

        return render(
            request,
            TMPL8S + "edit.html",
            {
                "editform": form,
                "draft_id": draft_id,
                "recname": draft_obj.name,
                "restype": restype,
            },
        )

    def post(self, request, **kwargs):
        draft_id = kwargs["draft_id"]
        form = EditForm(request.POST)
        if form.is_valid():
            try:
                form = save_widgets(request, form)
                draft = edit_to_draftdoc(form.cleaned_data)
                draft_obj = draft_api.save_updated_draft(draft, draft_id, request)
                return HttpResponseRedirect(reverse("start"))
            except DetectedFailure as ex:
                return handleFailure(ex)
            except draft_api.AccessControlError as ex:
                return handleFailure(Http401(message=str(ex)))

        restype = _get_restype(draft, Resource.schemauri)
        recname = request.POST.get("name", [])
        recname = "unkn" if len(recname) == 0 else recname[0]

        return render(
            request,
            TMPL8S + "edit.html",
            {
                "editform": form,
                "draft_id": draft_id,
                "recname": recname,
                "restype": restype,
            },
        )

    def _load_assets(self):
        """Update assets structure relative to the registry

        Returns:

        """

        # add all assets needed
        assets = {
            "js": [
                {
                    "path": "core_explore_keyword_registry_app/user/js/search/tagit.custom.js",
                    "is_raw": False,
                },
                {
                    "path": "core_explore_keyword_registry_app/user/js/search/fancytree.custom.js",
                    "is_raw": False,
                },
                {
                    "path": "core_explore_keyword_registry_app/user/js/search/resource_type_icons_table.js",
                    "is_raw": False,
                },
                {
                    "path": "core_explore_keyword_registry_app/user/js/search/filters.js",
                    "is_raw": False,
                },
            ],
            "css": [
                "core_explore_keyword_registry_app/user/css/fancytree/fancytree.custom.css",
                "core_main_registry_app/user/css/resource_banner/selection.css",
                "core_main_registry_app/user/css/resource_banner/resource_banner.css",
                "core_explore_keyword_registry_app/user/css/search/filters.css",
                "core_main_registry_app/libs/fancytree/skin-bootstrap/ui.fancytree.css",
                "cerr_curate_app/css/main.css",
            ],
        }

        return assets


def start_to_draftdoc(startdata, file_submission=None):
    """
    Convert the cleaned data from the form into a draft XML document.
    :return:  a dictionary containing an "xml_to_dict" representation of the XML document.
    """

    if file_submission is None or startdata["start_meth"] == "create":
        draft = Resource()
        if startdata["create"].get("homepage"):
            draft.add(
                "Resource/content/landingPage", startdata["create"].get("homepage")
            )
        draft.add("Resource/@status", "active")
        draft.add("name", startdata["create"].get("name"))
        if startdata["create"].get("restype"):
            draft.add_role(startdata["create"]["restype"][0].strip())

        if startdata["create"].get("scrape"):
            hp = startdata["create"].get("homepage")
            if hp and (hp.startswith("doi:") or hp.startswith("https://doi.org/")):
                doi_into_draftdoc(hp, draft)

        out = draft.todict()
        return {"Resource": out["Resource"][0], "name": out["name"][0]}

    elif file_submission:
        draft = load_uploaded_file(file_submission)
        draft["_name"] = file_submission.name
        return draft

    elif startdata["start_meth"] == "upload":
        raise Http400("File upload requested but no file was provided")
    else:
        raise Http400("Illegal start method specified")


def uploaded_file_to_draft(filedata):
    raise Http501("not implemented")


def draftdoc_to_edit(draft_doc, draft_id):
    pfx = "{%s}" % Resource.schemauri
    data = {}
    draft = draft_doc.get(pfx + "Resource", {})
    content = draft.get(pfx + "content", {})
    ident = draft.get(pfx + "identity", {})
    if content:
        data["homepage"] = content.get(pfx + "landingPage", "")
        data["description"] = content.get(pfx + "description", "")
        data["publisher"] = ident.get(pfx + "publisher", "")
    if ident:
        data["title"] = ident.get(pfx + "title", "")
    data["draft_id"] = draft_id
    data["restype"] = _get_restype(draft_doc, pfx)

    return data


def _get_restype(draft, pfx):
    if not pfx.startswith("{"):
        pfx = "{%s}" % pfx
    roles = draft.get(pfx + "Resource", {}).get(pfx + "role", [])
    if roles is None:
        roles = []
    elif not isinstance(roles, (list, tuple)):
        roles = [roles]
    out = "resource"
    if len(roles) > 0:
        out = re.sub(r"[^:]*:\s*", "", roles[0].get(pfx + "type", out))
    return out


def edit_to_draftdoc(data):
    draft = Resource()
    if data.get("homepage"):
        draft.add("Resource/content/landingPage", data.get("homepage", ""))
    if data.get("title"):
        draft.add("Resource/identity/title", data.get("title", ""))
    if data.get("description"):
        draft.add("Resource/content/description", data.get("description", ""))
    if data.get("widget"):
        draft.add("Resource/applicability/materialType", data.get("widget", ""))
    out = draft.todict()
    return {"Resource": out["Resource"][0]}


def save_new_draft(draftdoc, name, request):
    """
    save a new draft XML document with the given name
    :param dict draftdoc:   the draft XML document as an "xml_to_dict" dictionary
    :param str      name:   the mnemonic name to save the draft under
    :param HttpRequest request:  the HTTP request that delivered the draft; this is used
                            to authorize the creation of the draft.
    """
    try:
        return draft_api.save_as_draft(draftdoc, name, request).id
    except draft_api.AccessControlError as ex:
        raise Http401("unauthorized")


class DetectedFailure(Exception):
    """
    a base exception used by this module for failures it detects which should result in an
    HTTP response other than 200 or 404.
    """

    def __init__(self, code, reason=None, message=None):
        if not message:
            message = "%s failure condition detected" % str(code)
            if reason:
                message += ": " + reason
        super(DetectedFailure, self).__init__(message)
        self.status_code = code
        self.reason_phrase = reason


class Http400(DetectedFailure):
    """
    a failure requiring an HTTP response of 400 Bad Request
    """

    def __init__(self, reason=None, message=None):
        super(Http400, self).__init__(400, reason, message)


class Http401(DetectedFailure):
    """
    a failure requiring an HTTP response of 401 Unauthorized
    """

    def __init__(self, reason=None, message=None):
        super(Http401, self).__init__(401, reason, message)


class Http501(DetectedFailure):
    """
    a failure requiring an HTTP response of 501 Not Implemented
    """

    def __init__(self, reason=None, message=None):
        super(Http501, self).__init__(401, reason, message)


def handleFailure(exc):
    if isinstance(exc, DetectedFailure):
        return HttpResponse(status=exc.status_code, reason=exc.reason_phrase)


# TODO HANDLE EMPTY WIDGET
def save_widgets(request, form):
    """
    Retrieves the correct widget data and put it back in the form
    :param request:
    :param form:
    :return: form with appended widget data
    """
    widget_ids = dict(request.POST.lists())["widget"]
    materials = material_api.get_list_by_id(widget_ids)
    object_string = ", ".join([str(x.name) for x in materials])
    form.cleaned_data["widget"] = object_string
    return form


################################

_schema = [
    (
        "Resource",
        [
            ("identity", ["title", "altTitle", "identifier", "logo"]),
            (
                "providers",
                [
                    "publisher",
                    "publicationYear",
                    "creator",
                    "constributor",
                    "date",
                    "contact",
                ],
            ),
            (
                "content",
                [
                    "description",
                    "subject",
                    "landingPage",
                    "reference",
                    "primaryAudience",
                ],
            ),
            ("role", []),
            (
                "applicabilty",
                [
                    "productClass",
                    "materialType",
                    "synthesisProcessing",
                    "circularPathway",
                ],
            ),
            ("@atts", ["localid", "status"]),
        ],
    ),
    ("Organization", ["type"]),
    ("LiteratureResource", ["type"]),
    (
        "ServiceAPI",
        ["type", "baseURL", "documentationURL", "specificationURL", "complianceID"],
    ),
    ("Software", ["type"]),
    (
        "Tool",
        [
            "type",
            "codeLanguae",
            "supportedSystem",
            "licenseName",
            "feature",
            "documentation",
            "validationInfo",
            "exportControlStatement",
            "inputOutputs",
            "useNotes",
        ],
    ),
    ("DataCollection", ["type"]),
    ("Dataset", ["type", "dataOrigin"]),
    ("Database", ["type"]),
    ("WebSite", ["type"]),
]


class Node(Mapping):
    """
    a hierarchical dictionary representation of data destined for XML.  It is instantiated with a
    schema that control the order within a hierachical level that an XML element is inserted.
    This schema is used by the add() function which inserts data deep via an XPath-like key that
    points to the data to be set.
    """

    def __init__(self, elems=[]):
        self._data = OrderedDict()
        self._cmplx = {}
        for el in elems:
            if isinstance(el, (tuple, list)):
                self._cmplx[el[0]] = list(el[1])
                el = el[0]
            self._data[el] = None

    def isempty(self):
        return all([e is None for e in self._data.values()])

    def __getitem__(self, key):
        out = self._data[key]
        if out is None:
            raise KeyError(key)
        return out

    def __contains__(self, key):
        v = self.get(key)
        return v is not None

    def __iter__(self):
        return self.todict().items().__iter__()

    def __len__(self):
        return len([v for v in self._data.values() if v is not None])

    _idxre = re.compile(r"\[(\-?\d+)\]$")

    def add(self, key, val=None):
        """
        insert a value into the hierary.  The input key is interpreted for two XPath-like features:
          * slash (/) delimiters that indicate an element-descension into the XML heirarchy
          * [N] indexes on XML element names indicating which sequential occurrance of the element
            to select.
        :param str key:  the XPath like path
        """
        steps = key.split("/")
        node = self
        while len(steps) > 1:
            first = steps.pop(0)
            idx = -1
            m = self._idxre.search(first)
            if m:
                idx = int(m.group(1))
                first = self._idxre.sub("", first)
            node = node._add(first, idx=idx)

        return node._add(steps[0], val)

    def _add(self, key, val=None, idx=-1):
        vl = self._data.get(key)
        if vl is None:
            vl = []
            self._data[key] = vl

        if val is None:
            if len(vl) > 0:
                return vl[idx]

            # am reaching down into hierarchy
            if key in self._cmplx:
                val = Node(self._cmplx[key])
            else:
                val = Node()
        vl.append(val)
        return val

    def todict(self):
        """
        export the data into an OrderedDict tree
        """
        data = []
        for k, v in self._data.items():
            if not isinstance(v, list):
                if v is not None:
                    data.append((k, v))
            elif k.startswith("@"):
                v = "" if len(v) == 0 else v[-1]
                data.append((k, v))
            else:
                children = []
                data.append((k, children))
                for i, e in enumerate(v):
                    if isinstance(e, Node):
                        e = e.todict()
                    children.append(e)
        return OrderedDict(data)


class Resource(Node):
    """
    a Node for a handling Resource document
    """

    xsiuri = "http://www.w3.org/2001/XMLSchema-instance"
    schemauri = "http://schema.nist.gov/xml/ce-res-md/1.0wd2"
    nspfx = "rsm"

    def __init__(self):
        super(Resource, self).__init__(_schema)
        self.add("Resource/@xmlns", self.schemauri)
        self.add("Resource/@xmlns:" + self.nspfx, self.schemauri)
        self.add("Resource/@xmlns:xsi", self.xsiuri)

    def add_role(self, roletype):
        """
        add a role to this Resource object.
        """
        parts = re.split(r":\s*", roletype, 1)
        self.add(parts[0] + "/type", roletype)
        role = self.get(parts[0])
        role[-1].add("@xsi:type", self.nspfx + ":" + parts[0])
        self.add("Resource/role", role[-1])
        return role


import logging
import nistoar.doi

nistoar.doi.set_client_info(
    "NIST Circular Economy Registry",
    "beta",
    "https://nist.gov",
    "raymond.plante@nist.gov",
)
doilog = logging.getLogger("doi")


def doi_into_draftdoc(doi, draft):
    try:
        md = nistoar.doi.resolve(doi, logger=doilog)
        draft.add("Resource/identity/title", md.data["title"])
        draft.add("Resource/content/reference/@pid", doi)
        draft.add("Resource/content/reference/#text", md.citation_text)

        publisher = md.data.get("publisher")
        if md.data.get("container-title"):
            # this is a journal, most likely
            publisher = "%s (%s)" % (md.data.get("container-title"), publisher)
        draft.add("Resource/identity/publisher", publisher)

        pubdate = md.data.get("published", {}).get("date-parts", [[]])
        if len(pubdate) > 0 and pubdate[0]:
            draft.add("Resource/identity/publicationYear", pubdate[0])

    except Exception as ex:
        pass

    return draft
