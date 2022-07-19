from django import forms as forms

from .base import MultiForm, CerrErrorList
from django.forms.utils import ErrorDict

TMPL8S = "cerr_curate_app/user/forms/roles/"


class roleForm(MultiForm):
    @staticmethod
    def createForm(chosen_label, data):
        if chosen_label == "Software":
            return softwareRoleForm(data)
        if chosen_label == "Service API":
            return serviceApiForm(data)
        if chosen_label == "Semantic Asset":
            return semanticAssetRoleForm(data)
        if chosen_label == "Database":
            return databaseRoleForm(data)


class softwareRoleForm(roleForm):
    template_name = TMPL8S + "softwareRoleForm.html"
    software_code_language = forms.CharField(label="Code Language Used")
    software_os_name = forms.CharField(label="OS Name", required=True)
    software_os_version = forms.CharField(label="OS Version", required=True)
    software_license_name = forms.CharField(
        label="Name of license applied to the software", required=True
    )
    software_highlighted_feature = forms.CharField(label="Highlighted feature", required=True)

    def __init(self, data, **kwargs):
        super(softwareRoleForm, self).__init(data, **kwargs)


class semanticAssetRoleForm(roleForm):
    """
    form for simple data
    """

    template_name = TMPL8S + "defaultroleform.html"
    semanticasset_label = forms.CharField(label="SemanticAsset")

    def __init(self, data, label, **kwargs):
        super(semanticAssetRoleForm, self).__init(data, label, **kwargs)


class databaseRoleForm(roleForm):
    """
    form for simple data
    """

    template_name = TMPL8S + "defaultroleform.html"
    database_label = forms.CharField(label="Database")

    def __init(self, data, label, **kwargs):
        super(databaseRoleForm, self).__init(data, label, **kwargs)


class serviceApiForm(roleForm):
    template_name = TMPL8S + "serviceApiForm.html"
    service_tool_choices = [("1", "Service: API"), ("2", "Tool")]
    service_tool = forms.CharField(
        label="Tool", widget=forms.Select(choices=service_tool_choices)
    )
    service_base_url = forms.URLField(required=False)
    service_api_url = forms.URLField(required=False)
    service_specification_url = forms.URLField(
        label="Specification URL", required=False
    )
    service_compliance_id = forms.CharField(
        label="Name of license applied to the software", required=True
    )

    def __init(self, data=None, **kwargs):
        super(serviceApiForm, self).__init(data, **kwargs)


class sequenceForm(roleForm):
    # template_name = TMPL8S + "sequenceroleform"  # Create a button
    template_name = "cerr_curate_app/user/forms/roles/sequenceroleform.html"
    label_choices = [
        ("Service API", "ServiceApi"),
        ("Software", "Software"),
        ("Semantic Asset", "SemanticAsset"),
        ("Database", "Database"),
    ]
    role_list = forms.CharField(
        label="Chose a role", widget=forms.Select(choices=label_choices)
    )
    form_list = []

    def __init(
        self,
        formclass=None,
        form_list=[],
        labels=[],
        data=None,
        files=None,
        is_top=True,
        show_errors=None,
        **kwargs
    ):
        self.is_top = is_top
        self.initial = None

        # forms = {"forms": forms}
        if data is not None:
            for role in data:

                form = formclass.createForm(role.type, role)
                form_list.append(form)
        # if self.show_aggregate_errors is None:
        #     self.show_aggregate_errors = self.is_top
        if "error_class" not in kwargs:
            kwargs["error_class"] = CerrErrorList
        if "initial" in kwargs:
            self.initial = kwargs["initial"]
        super(sequenceForm, self).__init__(data, files, **kwargs)

    def full_clean(self):
        super(sequenceForm, self).full_clean()

    def get_context(self, **kwargs):
        context = super(sequenceForm, self).get_context(**kwargs)
        if self.initial:
            context["sequence"] = self.initial["sequenceform"]
        return context

    def render(self):
        "loop through the forms and render individually each one"
        for form in self.forms_list():
            form.render()

    def _clean_form(self):
        """"""
        service_values = {
            "service_tool": [],
            "service_tool_url": [],
            "service_base_url": [],
            "service_api_url": [],
            "service_specification_url": [],
            "service_compliance_id": [],
        }
        database_values = {"database_label": []}
        semanticasset_values = {"semanticasset_label": []}
        software_values = {
            "software_code_language": [],
            "software_os_name": [],
            "software_os_version": [],
            "software_license_name": [],
            "software_highlighted_feature": [],
        }

        data = self.data
        if data is not None:
            for item in data:
                if isinstance(item, str):
                    if item.startswith(("service")):
                        service_values[item].append(data[item])
                    if item.startswith(("database")):
                        database_values[item].append(data[item])
                    if item.startswith(("semanticasset")):
                        semanticasset_values[item].append(data[item])
                    if item.startswith(("software")):
                        software_values[item].append(data[item])
        self.cleaned_data.update(
            service=service_values,
            database=database_values,
            semanticasset=semanticasset_values,
            software=software_values,
        )
        super(sequenceForm, self)._clean_form()
