from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from core_main_app.components.template.models import Template
from django_mongoengine import fields
from mongoengine import errors as mongoengine_errors
from core_main_app.commons import exceptions
import logging

logger = logging.getLogger(__name__)


class ProductClass(MPTTModel):
    # schema associated with the draft document
    template = fields.ReferenceField(Template)
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    @staticmethod
    def get_by_id(productclass_id):
        """Return the object with the given id.

        Args:
            productclass_id:

        Returns:
            ProductClass (obj): ProductClass object with the given id

        """
        try:
            return ProductClass.objects.get(pk=str(productclass_id))
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def get_all():
        """Get all ProductClasss

        Returns:

        """
        return ProductClass.objects.all()
