"""
a module defining Forms used to edit an existing draft record
"""
import os
from collections import OrderedDict
from collections.abc import Mapping

from django import forms as forms
from django.utils.html import conditional_escape
from django.forms.utils import ErrorDict
from cerr_curate_app.utils.fancytree.widget import FancyTreeWidget
from .base import MultiForm, CerrErrorList, ComposableForm
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from mptt.querysets import TreeQuerySet
from cerr_curate_app.components.material.models import Material
from cerr_curate_app.components.productclass.models import ProductClass

from cerr_curate_app.components.lifecycle.models import Lifecycle

from .roles import sequenceForm as sequenceForm

__all__ = ["EditForm"]

TMPL8S = "cerr_curate_app/user/forms/"
from .selectrestype import ResourceTypeChoiceField


class AudienceForm(ComposableForm):
    choices = (
        ("researchers", "researchers"),
        ("practitioners ", "practitioners "),
        ("educators", "educators"),
        ("policy makers", "policy makers"),
        ("general public", "general public"),
        ("communication specialists", "communication specialists"),
    )
    template_name = TMPL8S + "audienceform.html"
    categories = forms.MultipleChoiceField(
        choices=choices, widget=forms.CheckboxSelectMultiple, required=False
    )

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
        context["choices"] = [
            {
                "value": c[0],
                "label": c[1],
                "checked": "checked" if c[0] in self.initial["categories"] else "",
            }
            for c in self.choices
        ]
        context["input_name"] = self["categories"].html_name
        context["max_selected"] = len(self.initial["categories"]) > 1

        return context

    def full_clean(self):
        if self.disabled:
            self._errors = ErrorDict()
            self.cleaned_data = {}
        else:
            super(AudienceForm, self).full_clean()


class HomePageForm(ComposableForm):
    template_name = TMPL8S + "homepageform.html"
    url = forms.URLField(label="Home Page URL")

    def __init__(self, data=None, files=None, is_top=True, show_errors=None, **kwargs):
        self.is_top = is_top
        self.show_aggregate_errors = show_errors
        self.disabled = False
        if self.show_aggregate_errors is None:
            self.show_aggregate_errors = self.is_top
        if "error_class" not in kwargs:
            kwargs["error_class"] = CerrErrorList
        super(HomePageForm, self).__init__(data, files, **kwargs)

    @property
    def url_errors(self):
        """
        return the errors associated with the homepage input
        """
        return self.errors.get("url", self.error_class(error_class="errorlist"))

    def full_clean(self):
        if self.disabled:
            self._errors = ErrorDict()
            self.cleaned_data = {}
        else:
            super(HomePageForm, self).full_clean()


class KeywordsForm(ComposableForm):
    template_name = TMPL8S + "keywordsform.html"
    keywords = forms.CharField(widget=forms.Textarea, label="Keywords", required=False)

    def __init__(self, data=None, files=None, is_top=True, show_errors=None, **kwargs):
        self.is_top = is_top
        self.show_aggregate_errors = show_errors
        self.disabled = False
        self.initial = None
        if self.show_aggregate_errors is None:
            self.show_aggregate_errors = self.is_top
        if "error_class" not in kwargs:
            kwargs["error_class"] = CerrErrorList
        if "initial" in kwargs:
            self.initial = kwargs["initial"]
        super(KeywordsForm, self).__init__(data, files, **kwargs)

    def get_context(self, **kwargs):
        context = super(KeywordsForm, self).get_context(**kwargs)
        if self.initial:
            context["prevKeywords"] = self.initial["keywords"]
        return context

    def full_clean(self):
        if self.disabled:
            self._errors = ErrorDict()
            self.cleaned_data = {}
        else:
            super(KeywordsForm, self).full_clean()


class EditForm(MultiForm):
    """
    Form that allows a user to create a new record.

    The cleaned_data provides data collected from the form in the following fields:
    :param str homepage:   the resource's home page URL
    """

    template_name = TMPL8S + "editform.html"
    description = forms.CharField(widget=forms.Textarea, label="Description")
    pubyear = forms.CharField(widget=forms.HiddenInput, required=False)
    # recname = forms.CharField(widget=forms.HiddenInput)

    def __init__(
        self,
        data=None,
        files=None,
        resource_type="Resource",
        is_top=True,
        show_errors=None,
        initial=None,
        **kwargs
    ):

        self.resourcetype = resource_type
        initial = self._unclean_data(initial)

        self.restitle = forms.CharField(
            label="Title of " + self.resourcetype, required=True
        )
        self.publisher = forms.CharField(
            label="Publisher of " + self.resourcetype, required=True
        )
        self.homepage = HomePageForm(
            data, files, is_top=False, initial=initial.get("homepage")
        )
        self.audience = AudienceForm(
            data, files, is_top=False, initial=initial.get("audience")
        )

        self.productclass = ProductClassForm(initial=initial.get("productClass"))
        self.lifecyclephase = LifecyclePhaseForm(initial=initial.get("lifecyclePhase"))
        self.materialtype = MaterialTypeForm(initial=initial.get("materialType"))

        self.keywords = KeywordsForm(
            data, files, is_top=False, initial=initial.get("keywords")
        )

        self.roleform = RoleForm(data, files, is_top=False, initial=initial.get("role"))
        self.sequence = sequenceForm(
            data, files, is_top=False, initial=initial.get("sequence")
        )
        self.is_top = is_top
        self.show_aggregate_errors = show_errors
        if self.show_aggregate_errors is None:
            self.show_aggregate_errors = self.is_top
        if "error_class" not in kwargs:
            kwargs["error_class"] = CerrErrorList
        super(EditForm, self).__init__(
            data,
            files,
            {
                "homepage": self.homepage,
                "productClass": self.productclass,
                "audience": self.audience,
                "sequence": self.sequence,
                "role": self.roleform,
                "keywords": self.keywords,
                "materialType": self.materialtype,
                "lifecyclePhase": self.lifecyclephase,
            },
            initial=initial,
            field_order="recname title publisher pubyear description".split(),
            **kwargs
        )
        self.fields["title"] = self.restitle
        self.fields["publisher"] = self.publisher
        self.order_fields(self.field_order)

    def full_clean(self):
        super(EditForm, self).full_clean()

    def _post_clean(self):
        # flatten the fancy tree data
        for ft in "productClass materialType lifecyclePhase".split():
            if ft in self.cleaned_data:
                if (
                    isinstance(self.cleaned_data[ft], Mapping)
                    and "ft" in self.cleaned_data[ft]
                ):
                    self.cleaned_data[ft] = self.cleaned_data[ft]["ft"]

        if "homepage" in self.cleaned_data and "url" in self.cleaned_data["homepage"]:
            self.cleaned_data["homepage"] = self.cleaned_data["homepage"].get("url", "")

        if (
            "audience" in self.cleaned_data
            and "categories" in self.cleaned_data["audience"]
        ):
            self.cleaned_data["audience"] = self.cleaned_data["audience"].get(
                "categories", ""
            )

        if (
            "keywords" in self.cleaned_data
            and "keywords" in self.cleaned_data["keywords"]
        ):
            self.cleaned_data["keywords"] = self.cleaned_data["keywords"].get(
                "keywords", []
            )
        if (
            "sequence" in self.cleaned_data
            and "sequence" in self.cleaned_data["sequence"]
        ):
            self.cleaned_data["sequence"]["service"] = self.cleaned_data[
                "sequence"
            ].get("service")
            self.cleaned_data["sequence"]["database"] = self.cleaned_data[
                "sequence"
            ].get("database")
            self.cleaned_data["sequence"]["semanticasset"] = self.cleaned_data[
                "sequence"
            ].get("semanticasset")
            self.cleaned_data["sequence"]["software"] = self.cleaned_data[
                "sequence"
            ].get("software")

        if "role" in self.cleaned_data and "role" in self.cleaned_data["role"]:
            self.cleaned_data["role"] = self.cleaned_data["role"].get("role", [])

    def _unclean_data(self, data):

        if isinstance(data, Mapping):
            for ft in "productClass materialType lifecyclePhase".split():
                if ft in data:
                    data[ft] = {"ft": data[ft]}

            if "homepage" in data and isinstance(data["homepage"], str):
                data["homepage"] = {"url": data["homepage"]}

            if "keywords" in data and isinstance(data["keywords"], str):
                data["keywords-keywords"] = "[dodo,dada]"
                data["keywords"] = {"keywords": data["keywords"]}

            if "audience" in data and isinstance(data["audience"], (list, tuple)):
                data["audience"] = {"categories": data["audience"]}

            if "sequence" in data and isinstance(data["sequence"], (list, tuple)):
                data["sequence"] = {"sequence": data["sequence"]}

            if "role" in data and isinstance(data["role"], (list, tuple)):
                data["role"] = {"role": data["role"]}
        elif not data:
            data = {}

        return data


class FancyTreeForm(forms.Form):
    def __init__(self, data=None, files=None, initial=None, **kwargs):
        initial = self._unclean_data(initial)
        super(FancyTreeForm, self).__init__(data, files, initial=initial, **kwargs)

    def _post_clean(self):
        # resolve fancy tree TreeQuerySets into string values
        if "ft" in self.cleaned_data and isinstance(
            self.cleaned_data["ft"], TreeQuerySet
        ):
            terms = []
            for cat in self.cleaned_data["ft"]:
                terms.append(cat.name)
            self.cleaned_data["ft"] = terms

    def _unclean_data(self, data):
        # convert terms back into fancy tree indicies
        if not isinstance(data, Mapping):
            return data
        if not data:
            data = {}

        if "ft" in data and isinstance(data["ft"], (list, tuple)):
            indicies = []
            for term in self.categories:
                if term.name in data["ft"]:
                    indicies.append(str(term.id))
            data["ft"] = indicies
        return data


class MaterialTypeForm(FancyTreeForm):
    fields = ("name", "categories")
    id = "material_type"
    categories = Material.objects.order_by("tree_id", "lft")
    ft = forms.ModelMultipleChoiceField(
        label="Material Type",
        required=False,
        queryset=categories,
        widget=FancyTreeWidget(attrs={"id": id}, queryset=categories),
    )


class ProductClassForm(FancyTreeForm):
    fields = ("name", "categories")
    id = "product_class"
    categories = ProductClass.objects.order_by("tree_id", "lft")
    ft = forms.ModelMultipleChoiceField(
        label="Product Class",
        required=False,
        queryset=categories,
        widget=FancyTreeWidget(attrs={"id": id}, queryset=categories),
    )


class LifecyclePhaseForm(FancyTreeForm):
    fields = ("name", "categories")
    id = "lifecycle_phase"
    categories = Lifecycle.objects.order_by("tree_id", "lft")
    ft = forms.ModelMultipleChoiceField(
        label="Lifecycle Phase",
        required=False,
        queryset=categories,
        widget=FancyTreeWidget(attrs={"id": id}, queryset=categories),
    )


class RoleForm(ComposableForm):
    role = forms.CharField(max_length=255, required=False, label="Role")
    total_input_fields = forms.CharField(widget=forms.HiddenInput(), required=False)
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
