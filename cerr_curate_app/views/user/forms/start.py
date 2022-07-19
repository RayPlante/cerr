"""
a module defining Forms used to start a draft record
"""
import os, pdb
from collections import OrderedDict
from collections.abc import Mapping

from django import forms as forms
from django.utils.html import conditional_escape
from django.forms.utils import ErrorDict

from .base import ComposableForm, MultiForm, CerrErrorList
from .selectrestype import ResourceTypeChoiceField

__all__ = "CreateForm StartForm".split()

TMPL8S = "cerr_curate_app/user/forms/"


class CreateForm(ComposableForm):
    """
    A Form for creating an initial draft of a record.

    It includes:
     * a text field for entering a mnemonic name
     * a URL field for entering the resource's landing page
     * an array of radio buttons for selecting a type
    """

    template_name = TMPL8S + "createform.html"
    name = forms.CharField(required=True)
    homepage = forms.URLField(required=False)
    scrape = forms.BooleanField(initial=True, required=False)
    restype = ResourceTypeChoiceField()

    def __init__(self, data=None, files=None, is_top=True, show_errors=None, **kwargs):
        self.is_top = is_top
        self.show_aggregate_errors = show_errors
        self.disabled = False
        if self.show_aggregate_errors is None:
            self.show_aggregate_errors = self.is_top
        if "error_class" not in kwargs:
            kwargs["error_class"] = CerrErrorList
        super(CreateForm, self).__init__(data, files, **kwargs)

    @property
    def name_errors(self):
        """
        return the errors associated with the name input
        """
        return self.errors.get("name", self.error_class(error_class="errorlist"))

    @property
    def homepage_errors(self):
        """
        return the errors associated with the homepage input
        """
        return self.errors.get("homepage", self.error_class(error_class="errorlist"))

    @property
    def restype_errors(self):
        """
        return the errors associated with the homepage input
        """
        return self.errors.get("restype", self.error_class(error_class="errorlist"))

    def full_clean(self):
        if self.disabled:
            self._errors = ErrorDict()
            self.cleaned_data = {}
        else:
            super(CreateForm, self).full_clean()


class MethodSelect(forms.RadioSelect):
    option_template_name = TMPL8S + "method_option.html"


class StartForm(MultiForm):
    """
    Form that allows a user to create a new record.

    The cleaned_data provides data collected from the form in the following fields:
    :param str start_meth:   either "create" or "upload", indicating whether the user wants
                             create a new draft from scratch or start with an exisitng XML-encoded
                             uploaded document.
    :param file xmlfile:     The uploaded file that should be used as the initial draft.
    :param dict create:      A dictionary with the properties for creating a record from scratch
    :param str  create.name: A mnemonic name given to the draft by the user
    :param str  create.homepage:    the new resource's homepage as a URL.
    """

    template_name = TMPL8S + "startform.html"
    xmlfile = forms.FileField(
        widget=forms.FileInput(attrs={"class": "form-control"}), required=False
    )
    start_meth = forms.ChoiceField(
        widget=MethodSelect,
        required=True,
        choices=[
            ("create", "Create a new record from scratch"),
            ("upload", "Upload an existing XML document"),
        ],
    )

    def __init__(self, data=None, files=None, is_top=True, show_errors=None, **kwargs):
        self.create = CreateForm(data, files, is_top=False)
        if "error_class" not in kwargs:
            kwargs["error_class"] = CerrErrorList
        super(StartForm, self).__init__(
            data, files, {"create": self.create}, is_top, show_errors, **kwargs
        )

    def _clean_form(self):
        if self.cleaned_data.get("start_meth") == "upload":
            self.create.disabled = True
            if not self.files.get("xmlfile"):
                if "xmlfile" not in self._errors:
                    self._errors["xmlfile"] = CerrErrorList([], error_class="errorlist")
                self._errors["xmlfile"].append("Please select an XML file to upload")
        super(StartForm, self)._clean_form()
