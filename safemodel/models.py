# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

from .config import (HARD_DELETE, HARD_DELETE_NOCASCADE, SOFT_DELETE, SOFT_DELETE_CASCADE, NO_DELETE)


class SafeModel(models.Model):
    _safe_policy = SOFT_DELETE
    _safe_relation_classes = []

    deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(editable=False, null=True)

    class Meta:
        abstract = True

    @classmethod
    def related_fields(cls):
        """
        Get all fields that are either Foreign Keys or One-to-One fields. Ignores Many-to-Many relations.
        :return:
        """
        related_fields = []
        for field in cls._meta.get_fields():
            if issubclass(field.__class__, models.ForeignObject):
                related_fields.append(field)
        return related_fields

    @classmethod
    def can_hard_delete(cls):
        if not cls.related_fields():
            return True
        return False

    def save(self, undelete=True, **kwargs):
        if self.deleted and undelete:
            self.undelete()
        super(SafeModel, self).save(**kwargs)

    def delete(self, force_policy=None, deleted_on=None, **kwargs):
        current_policy = self._safe_policy if (force_policy is None) else force_policy

        if current_policy == HARD_DELETE:
            super(SafeModel, self).delete(**kwargs)
        elif current_policy == HARD_DELETE_NOCASCADE:
            if self.can_hard_delete():
                super(SafeModel, self).delete(**kwargs)
            else:
                self.delete(force_policy=SOFT_DELETE)
        elif current_policy == SOFT_DELETE:
            self.deleted = True
            self.deleted_on = timezone.now()
            self.save(undelete=False)
        elif current_policy == SOFT_DELETE_CASCADE:
            deleted_timestamp = timezone.now()
            pass

    def undelete(self, force_policy=None, deleted_on=None, **kwargs):
        pass
