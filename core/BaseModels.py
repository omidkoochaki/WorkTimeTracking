from datetime import datetime

from django.db import models


class BaseManager(models.Manager):
    """
    Manager is overwritten to handle the logical delete functionality
    """

    def get_queryset(self):
        """
        overwrite get_queryset for personalization this for logical delete
        """
        return super().get_queryset().filter(deleted=False)

    def archive(self):
        """
        rewrite get_queryset for access to all objects and data in this project
        """
        return super().get_queryset()


class BaseModel(models.Model):
    """
    Base Model is overwritten to handle logical delete and some modify time records
    """
    deleted = models.BooleanField(default=False)
    create_timestamp = models.FloatField(default=datetime.now().timestamp())
    modify_timestamp = models.FloatField(default=None, null=True, blank=True, editable=False)
    delete_timestamp = models.FloatField(default=None, null=True, blank=True, editable=False)

    objects = BaseManager()

    class Meta:
        abstract = True

    def logic_delete(self):
        """
        method for logical delete for this project
        """
        self.deleted = True
        self.delete_timestamp = datetime.now().timestamp()
        self.save()

    def delete(self, using=None, keep_parents=False):
        return super().delete(using, keep_parents)
