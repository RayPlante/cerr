"""
This provides some base classes for creating modular forms
"""
from collections import OrderedDict

from django import forms as djforms
from django.utils.html import conditional_escape
from django.utils.datastructures import MultiValueDict
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.forms.utils import ErrorList
from django.forms.renderers import get_default_renderer
from django.utils.safestring import mark_safe, SafeString

TMPL8S = "cerr_curate_app/user/base/"
_template_name_fields_first = TMPL8S + "multiform_fields_first.html"
_template_name_fields_last = TMPL8S + "multiform_fields_last.html"


class RenderableMixin:
    """
    a mixin that allows a form to be built into an enclosing composite form.
    """

    # taken from django 4
    def _bound_items(self):
        """Yield (name, bf) pairs, where bf is a BoundField object."""
        for name in self.fields:
            yield name, self[name]

    def get_context(self):
        fields = []
        hidden_fields = []
        top_errors = self.non_field_errors().copy()
        for name, bf in self._bound_items():
            bf_errors = self.error_class(bf.errors)
            if bf.is_hidden:
                if bf_errors:
                    top_errors += [
                        _("(Hidden field %(name)s) %(error)s")
                        % {"name": name, "error": str(e)}
                        for e in bf_errors
                    ]
                hidden_fields.append(bf)
            else:
                errors_str = str(bf_errors)
                # RemovedInDjango50Warning.
                if not isinstance(errors_str, SafeString):
                    warnings.warn(
                        f"Returning a plain string from "
                        f"{self.error_class.__name__} is deprecated. Please "
                        f"customize via the template system instead.",
                        RemovedInDjango50Warning,
                    )
                    errors_str = mark_safe(errors_str)
                fields.append((bf, errors_str))
        return {
            "form": self,
            "fields": fields,
            "hidden_fields": hidden_fields,
            "errors": top_errors,
        }

    def _render(self, template_name=None, context=None, renderer=None):
        return mark_safe(
            (renderer or self.renderer).render(
                template_name or self.template_name,
                context or self.get_context(),
            )
        )


class ComposableForm(djforms.Form, RenderableMixin):
    def __init__(
        self,
        data=None,
        files=None,
        is_top=True,
        show_errors=None,
        template=None,
        **kwargs,
    ):
        """
        Wrap a collection of forms into a single form

        :param data:  the data to bind to the form (as provided by HttpRequest.POST)
        :param files: the file data to bind to the form (as provided by HttpRequest.FILES)
        :param bool is_top:  If True (default), this form is expected to be the top of the
                      form hierarchy.  This is set a property that can be consulted by subclasses
                      as needed, but it also sets the default value for the show_errors property
                      to the same value.
        :param bool show_errors:  If False, the collected errors detected on bound data will be not
                      displayed in this form (assuming the attached template supports
                      this property); however, they will be available for display by the enclosing
                      form.  This does not affect the display of errors close to the input fields
                      where the error was detected.

        In addition, this constructor supports all of the parameters supported by Form; one must
        specify them explicitly using their argument keywords.
        """
        super(ComposableForm, self).__init__(data, files, **kwargs)

        self.is_top = is_top
        self.show_aggregate_errors = show_errors
        if self.show_aggregate_errors is None:
            self.show_aggregate_errors = self.is_top

        if template:
            self.template_name = template
        self.renderer = get_default_renderer()

    def __str__(self):
        return self._render()


class MultiForm(ComposableForm):
    """
    a form composed from multiple, re-usable djforms
    """

    template_name_fields_first = _template_name_fields_first
    template_name_fields_last = _template_name_fields_last
    template_name = _template_name_fields_first

    def __init__(
        self,
        data=None,
        files=None,
        forms=[],
        is_top=True,
        show_errors=None,
        template=None,
        **kwargs,
    ):
        """
        Wrap a collection of forms into a single form

        :param data:  the data to bind to the form (as provided by HttpRequest.POST)
        :param files: the file data to bind to the form (as provided by HttpRequest.FILES)
        :param forms: the forms to wrap.  The best way to provide these is as an OrderedDict
                      as the name will be used to set a unique name for the encosed input
                      fields, and the order will specify the order that the forms are arranged
                      on the output page.  If given as a list, the order determines the
                      arrangement, and unique names will be created from the provided prefix
                      argument.
                      :type forms: {name, Form} or [Form] or Form
        :param bool is_top:  If True (default), this form is expected to be the top of the
                      form hierarchy.  This is set a property that can be consulted by subclasses
                      as needed, but it also sets the default value for the show_errors property
                      to the same value.
        :param bool show_errors:  If False, the collected errors detected on bound data will be not
                      displayed in this form (assuming the attached template supports
                      this property); however, they will be available for display by the enclosing
                      form.  This does not affect the display of errors close to the input fields
                      where the error was detected.

        In addition, this constructor supports all of the parameters supported by Form; one must
        specify them explicitly using their argument keywords.
        """
        prefix = kwargs.get("prefix", "mf")

        if isinstance(forms, dict):
            self.forms = OrderedDict(forms)
        elif isinstance(forms, djforms.Form):
            self.forms = OrderedDict([(forms.prefix or prefix + "0", forms)])
        else:
            # assume a list; make up some names for them (based on prefix)
            self.forms = OrderedDict()
            for i, form in enumerate(forms):
                self.forms[form.prefix or prefix + str(i)] = form

        super(MultiForm, self).__init__(data, files, is_top, show_errors, **kwargs)
        for fname, form in self.forms.items():
            form.prefix = fname
            if data is not None or files is not None:
                form.is_bound = data is not None or files is not None
                form.data = MultiValueDict() if data is None else data
                form.files = MultiValueDict() if files is None else files

    def clean_subforms(self):
        """
        clean the data from each of the enclosed forms.  If there is a method of the form
        clean_<formname>() where <formname> is the name attached to the form at construction
        time, it will be called; the returned value should be a compressed value for the form
        (usually a dictionary).
        """
        for name, form in self.forms.items():
            try:
                form.full_clean()
                self.cleaned_data[name] = form.cleaned_data
                if hasattr(self, "clean_%s" % name):
                    value = getattr(self, "clean_%s" % name)()
                    self.cleaned_data[name] = value
            except ValidationError as ex:
                self.add_error(name, e)
            if form.errors:
                self.add_error(
                    NON_FIELD_ERRORS, "Please correct the errors indicated below"
                )

    def _clean_form(self):
        super(MultiForm, self)._clean_form()
        self.clean_subforms()

    def get_context(self):
        context = super(MultiForm, self).get_context()
        context["subforms"] = self.forms
        return context


class CerrErrorList(ErrorList):
    template_name = TMPL8S + "errorlist.html"
