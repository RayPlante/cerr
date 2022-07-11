"""
a module defining Forms used to edit an existing draft record
"""
import os, pdb
from collections import OrderedDict
from collections.abc import Mapping

from django import forms as forms
from django.utils.html import conditional_escape
from django.forms.utils import ErrorDict
from cerr_curate_app.utils.fancytree.widget import FancyTreeWidget
from .base import MultiForm, CerrErrorList, ComposableForm
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from cerr_curate_app.components.material.models import Material
from cerr_curate_app.components.productclass.models import ProductClass

from cerr_curate_app.components.lifecycle.models import Lifecycle

from .roles import sequenceForm as sequenceForm

__all__ = ["EditForm"]

TMPL8S = "cerr_curate_app/user/forms/"
from .selectrestype import ResourceTypeChoiceField


class AudienceForm(ComposableForm):
    choices = (
        "researchers",
        "practitioners ",
        "educators",
        "policy makers",
        "general public",
        "communication specialists",
    )
    template_name = TMPL8S + "audienceform.html"
    restype = forms.MultipleChoiceField(choices=choices, widget=forms.RadioSelect)

    def __init__(self, data=None, files=None, is_top=True, show_errors=None, **kwargs):
        self.is_top = is_top
        self.show_aggregate_errors = show_errors
        self.disabled = False
        if self.show_aggregate_errors is None:
            self.show_aggregate_errors = self.is_top
        if "error_class" not in kwargs:
            kwargs["error_class"] = CerrErrorList
        super(AudienceForm, self).__init__(data, files, **kwargs)

    # Override get_context to add choices to context
    def get_context(self, **kwargs):
        context = super(AudienceForm, self).get_context(**kwargs)
        context["choices"] = self.choices
        return context

    @property
    def homepage_errors(self):
        """
        return the errors associated with the homepage input
        """
        return self.errors.get("homepage", self.error_class(error_class="errorlist"))

    def full_clean(self):
        if self.disabled:
            self._errors = ErrorDict()
            self.cleaned_data = {}
        else:
            super(AudienceForm, self).full_clean()


class UrlForm(ComposableForm):
    template_name = TMPL8S + "urlform.html"
    homepage = forms.URLField(label="Home Page URL")

    def __init__(self, data=None, files=None, is_top=True, show_errors=None, **kwargs):
        self.is_top = is_top
        self.show_aggregate_errors = show_errors
        self.disabled = False
        if self.show_aggregate_errors is None:
            self.show_aggregate_errors = self.is_top
        if "error_class" not in kwargs:
            kwargs["error_class"] = CerrErrorList
        super(UrlForm, self).__init__(data, files, **kwargs)

    @property
    def homepage_errors(self):
        """
        return the errors associated with the homepage input
        """
        return self.errors.get("homepage", self.error_class(error_class="errorlist"))

    def full_clean(self):
        if self.disabled:
            self._errors = ErrorDict()
            self.cleaned_data = {}
        else:
            super(UrlForm, self).full_clean()


class KeywordsForm(ComposableForm):
    template_name = TMPL8S + "keywordsform.html"
    keywords = forms.CharField(widget=forms.Textarea, label="Keywords")
    # homepage = forms.URLField(label="Home Page URL")

    def __init__(self, data=None, files=None, is_top=True, show_errors=None, **kwargs):
        self.is_top = is_top
        self.show_aggregate_errors = show_errors
        self.disabled = False
        if self.show_aggregate_errors is None:
            self.show_aggregate_errors = self.is_top
        if "error_class" not in kwargs:
            kwargs["error_class"] = CerrErrorList
        super(KeywordsForm, self).__init__(data, files, **kwargs)

    @property
    def homepage_errors(self):
        """
        return the errors associated with the homepage input
        """
        return self.errors.get("homepage", self.error_class(error_class="errorlist"))

    def full_clean(self):
        if self.disabled:
            self._errors = ErrorDict()
            self.cleaned_data = {}
        else:
            super(KeywordsForm, self).full_clean()


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
    restype = ResourceTypeChoiceField()

    def __init__(self, data=None, is_top=True, show_errors=None, **kwargs):
        self.is_top = is_top
        self.show_aggregate_errors = show_errors
        self.disabled = False
        if self.show_aggregate_errors is None:
            self.show_aggregate_errors = self.is_top
        if "error_class" not in kwargs:
            kwargs["error_class"] = CerrErrorList
        super(CreateForm, self).__init__(data, **kwargs)

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


class EditForm(MultiForm):
    """
    Form that allows a user to create a new record.

    The cleaned_data provides data collected from the form in the following fields:
    :param str homepage:   the resource's home page URL
    """

    template_name = TMPL8S + "editform.html"
    description = forms.CharField(widget=forms.Textarea, label="Description")

    def __init__(
        self, data=None, files=None, title=None, is_top=True, show_errors=None, **kwargs
    ):
        if data.get("homepage"):
            self.urlform = UrlForm(
                data, files, is_top=False, initial={"homepage": data["homepage"]}
            )
        else:
            self.urlform = UrlForm(data, files, is_top=False)
        self.resourcelabel = data.get("restype", "nothing")

        self.restitle = forms.CharField(
            label="Title of " + self.resourcelabel, required=True
        )
        self.publisher = forms.CharField(
            label="Publisher of " + self.resourcelabel, required=True
        )

        self.productform = ProductClassForm()
        self.lifecycle = LifecyclePhaseForm()
        self.audienceform = AudienceForm(data, files, is_top=False)
        self.material = MaterialTypeForm()
        self.roleform = RoleForm()
        self.roles = sequenceForm()
        self.keywordsform = KeywordsForm(data, files, is_top=False)
        self.is_top = is_top
        self.show_aggregate_errors = show_errors
        self.title = title
        if self.show_aggregate_errors is None:
            self.show_aggregate_errors = self.is_top
        if "error_class" not in kwargs:
            kwargs["error_class"] = CerrErrorList
        super(EditForm, self).__init__(
            data,
            {
                "urlform": self.urlform,
                "audienceform": self.audienceform,
                "role": self.roleform,
                "keywordsform": self.keywordsform,
            },
            field_order="title publisher description".split(),
            **kwargs
        )
        self.fields["title"] = self.restitle
        self.fields["publisher"] = self.publisher
        self.order_fields(self.field_order)


class MaterialTypeForm(forms.Form):
    fields = ("name", "categories")
    id = "material_type"
    categories = Material.objects.order_by("tree_id", "lft")
    widget = forms.ModelMultipleChoiceField(
        label="Material Type",
        required=False,
        queryset=categories,
        widget=FancyTreeWidget(attrs={"id": id}, queryset=categories),
    )

    def _clean_form(self):
        super(MaterialTypeForm)._clean_form()


class ProductClassForm(forms.Form):
    fields = ("name", "categories")
    id = "product_class"
    categories = ProductClass.objects.order_by("tree_id", "lft")
    widget = forms.ModelMultipleChoiceField(
        label="Product Class",
        required=False,
        queryset=categories,
        widget=FancyTreeWidget(attrs={"id": id}, queryset=categories),
    )

    def _clean_form(self):
        super(ProductClassForm)._clean_form()


class LifecyclePhaseForm(forms.Form):
    fields = ("name", "categories")
    id = "lifecycle_phase"
    categories = Lifecycle.objects.order_by("tree_id", "lft")
    widget = forms.ModelMultipleChoiceField(
        label="Lifecycle Phase",
        required=False,
        queryset=categories,
        widget=FancyTreeWidget(attrs={"id": id}, queryset=categories),
    )

    def _clean_form(self):
        super(LifecyclePhaseForm)._clean_form()


class RoleForm(ComposableForm):
    role = forms.CharField(max_length=255, required=True, label="Role")
    total_input_fields = forms.CharField(widget=forms.HiddenInput())
    template_name = TMPL8S + "roleform.html"

    def __init__(self, *args, **kwargs):

        extra_fields = kwargs.pop("extra", 0)

        # check if extra_fields exist. If they don't exist assign 0 to them
        if not extra_fields:
            extra_fields = 0

        super(RoleForm, self).__init__(*args, **kwargs)
        self.fields["total_input_fields"].initial = extra_fields

        for index in range(int(extra_fields)):
            # generate extra fields in the number specified via extra_fields
            self.fields["extra_field_{index}".format(index=index)] = forms.CharField()
