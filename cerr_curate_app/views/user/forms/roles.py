from django import forms as forms

from .base import MultiForm, CerrErrorList

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
    code_language = forms.CharField(label="Code Language Used")
    os_name = forms.CharField(label="OS Name", required=True)
    os_version = forms.CharField(label="OS Version", required=True)
    license_name = forms.CharField(
        label="Name of license applied to the software", required=True
    )
    highlighted_feature = forms.CharField(label="Highlighted feature", required=True)

    def __init(self, data, **kwargs):
        super(softwareRoleForm, self).__init(data, **kwargs)


class semanticAssetRoleForm(roleForm):
    """
    form for simple data
    """

    template_name = TMPL8S + "defaultroleform.html"
    label = forms.CharField(label="SemanticAsset")

    def __init(self, data, label, **kwargs):
        super(semanticAssetRoleForm, self).__init(data, label, **kwargs)


class databaseRoleForm(roleForm):
    """
    form for simple data
    """

    template_name = TMPL8S + "defaultroleform.html"
    label = forms.CharField(label="Database")

    def __init(self, data, label, **kwargs):
        super(databaseRoleForm, self).__init(data, label, **kwargs)


class serviceApiForm(roleForm):
    template_name = TMPL8S + "serviceApiForm.html"
    tool_choices = [("1", "Service: API"), ("2", "Tool")]
    tool = forms.CharField(label="Tool", widget=forms.Select(choices=tool_choices))
    base_url = forms.URLField(required=False)
    api_url = forms.URLField(required=False)
    specification_url = forms.URLField(label="Specification URL", required=False)
    compliance_id = forms.CharField(
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
        # forms = {"forms": forms}
        if data is not None:
            for role in data:

                form = formclass.createForm(role.type, role)
                form_list.append(form)
        # if self.show_aggregate_errors is None:
        #     self.show_aggregate_errors = self.is_top
        if "error_class" not in kwargs:
            kwargs["error_class"] = CerrErrorList
        super(sequenceForm, self).__init__(data, files, **kwargs)

    def render(self):
        "loop through the forms and render individually each one"
        for form in self.forms_list():
            form.render()

    pass
