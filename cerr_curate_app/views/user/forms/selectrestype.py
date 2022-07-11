"""
This module provides widgets for selecting the resource type
"""
from django import forms
from django.forms import widgets

TMPL8S = "cerr_curate_app/user/forms/"


class ResourceSelect(widgets.ChoiceWidget):
    template_name = TMPL8S + "restype.html"
    # group_template_name = TMPL8S + 'selectGroup.html'

    def __init__(self, allow_multiple=False, resources=(), attrs=None):
        self._allow_multiple = allow_multiple
        self.input_type = "checkbox" if allow_multiple else "radio"
        #        self.template_name = forms.CheckboxSelectMultiple.template_name \
        #                                        if allow_multiple \
        #                                        else forms.RadioSelect.template_name
        self.option_template_name = (
            forms.CheckboxSelectMultiple.option_template_name
            if allow_multiple
            else forms.RadioSelect.option_template_name
        )

        choices = []
        for group, subs in resources:
            choices.append(
                (group, [(group, group)] + [("%s: %s" % (group, s), s) for s in subs])
            )

        super().__init__(attrs, choices)

    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        out = super().create_option(
            name, value, label, selected, index, subindex, attrs
        )
        if subindex is not None:
            out["subindex"] = subindex
        return out

    def use_required_attribute(self, initial):
        # Don't use the 'required' attribute because browser validation would
        # require all checkboxes to be checked instead of at least one.
        if self._allow_multiple:
            return False
        return super().use_required_attribute(initial)

    def value_omitted_from_data(self, data, files, name):
        # HTML checkboxes don't appear in POST data if not checked, so it's
        # never known if the value is actually omitted.
        if self._allow_multiple:
            return False
        return super().use_required_attribute(initial)

    def id_for_label(self, id_, index=None):
        """
        Don't include for="field_0" in <label> because clicking such a label
        would toggle the first checkbox.
        """
        if self._allow_multiple and index is None:
            return ""
        return super().id_for_label(id_, index)


class ResourceTypeChoice:
    """
    a container for a resource type choice and its sub-choices, used to configure a ResourceChoiceField
    """

    def __init__(self, value, label, subchoice_field=None):
        self.value = value
        self.label = label
        self.subchoices = subchoice_field

    def to_tuple(self):
        return (self.value, self.label, self.sub_choices)

    @classmethod
    def to_choices(cls, choice_seq):
        return tuple([c.to_tuple() for c in choice_seq])


class ResourceTypeChoiceField(forms.MultipleChoiceField):
    """
    A choice of a resource type (role)
    """

    def __init__(self, allow_multiple=False, **kwargs):
        self._allow_multiple = allow_multiple

        resources = (
            ("Organization", ("Project", "Trade Association", "Consortium")),
            ("Collection", ("Repository", "Project Archive")),
            ("Dataset", ("Database",)),
            ("Literature", ("Article", "Journal", "Report", "Proceedings")),
            ("Web Site", ("Portal", "Informational")),
            ("Tool", ("Desktop App", "Web App", "Software Library")),
        )

        widget = ResourceSelect(allow_multiple, resources)
        super(ResourceTypeChoiceField, self).__init__(
            choices=widget.choices, widget=widget, **kwargs
        )

    def to_python(self, value):
        if not isinstance(value, (list, tuple)):
            value = [value]
        return super().to_python(value)


class ProductTypeChoiceField(forms.MultipleChoiceField):
    """
    A choice of a resource type (role)
    """

    def __init__(self, allow_multiple=False, **kwargs):
        self._allow_multiple = allow_multiple

        resources = (("batteries", "electronics ", "packaging", "textiles"),)

        widget = ResourceSelect(allow_multiple, resources)
        super(ProductTypeChoiceField, self).__init__(
            choices=widget.choices, widget=widget, **kwargs
        )

    def to_python(self, value):
        if not isinstance(value, (list, tuple)):
            value = [value]
        return super().to_python(value)
