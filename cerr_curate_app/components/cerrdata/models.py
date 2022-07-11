from django_mongoengine import fields
from mongoengine.queryset.base import NULLIFY

from core_main_app.components.abstract_data.models import AbstractData
from core_main_app.components.template.models import Template
from core_main_app.components.workspace.models import Workspace
from django.db import models


class CerrData(AbstractData):
    """CerrData object"""

    template = fields.ReferenceField(Template, blank=False)
    user_id = fields.StringField()
    workspace = fields.ReferenceField(
        Workspace, reverse_delete_rule=NULLIFY, blank=True
    )

    meta = {"indexes": ["title", "last_modification_date", "template", "user_id"]}

    def cerr_convert_and_save(self):
        """Save Data object and convert the xml to dict if needed.

        Returns:

        """
        self.convert_to_dict()
        self.convert_to_file()

        return self.save_object()
