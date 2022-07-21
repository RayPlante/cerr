import logging

from django_mongoengine import Document
from django_mongoengine import fields
from mongoengine import errors as mongoengine_errors
from mongoengine.errors import NotUniqueError
from mongoengine.queryset.base import CASCADE

from core_main_app.commons import exceptions
from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from cerr_curate_app.components.cerrdata.models import CerrData

logger = logging.getLogger(__name__)


class CurateDataStructure(Document):
    """Stores data being entered and not yet curated"""

    user = fields.StringField()

    # schema associated with the draft document
    template = fields.ReferenceField(Template)
    # name of the document
    name = fields.StringField(unique_with=["user", "template"])
    # Whole XML data of the document
    form_string = fields.StringField(blank=True)
    # Reference to the saved CerrData
    data = fields.ReferenceField(CerrData, blank=True, reverse_delete_rule=CASCADE)

    #    meta = {"abstract": True}

    @staticmethod
    def get_all_by_user_id(user_id):
        """Return all drafts by user

        Returns:

        """
        return CurateDataStructure.objects(user=str(user_id)).all()

    @staticmethod
    def get_all():
        """Return all drafts by user

        Returns:

        """
        return CurateDataStructure.objects.all()

    @staticmethod
    def get_by_id(draft_id):
        """Return the object with the given id.

        Args:
            draft_id:

        Returns:
            Draft (obj): Draft object with the given id

        """
        try:
            return CurateDataStructure.objects.get(pk=str(draft_id))
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    def save_object(self):
        """Custom save

        Returns:

        """
        try:
            return self.save()
        except NotUniqueError:
            raise exceptions.ModelError("Unable to save the document: not unique.")
        except Exception as ex:
            raise exceptions.ModelError(str(ex))
