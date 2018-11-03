# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

from .config import (HARD_DELETE, HARD_DELETE_NOCASCADE, SOFT_DELETE, SOFT_DELETE_CASCADE, NO_DELETE)


class SafeModel(models.Model):
    _safe_policy = SOFT_DELETE
    _soft_cascade_classes = []

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

    def save(self, keep_deleted=False, **kwargs):
        if not keep_deleted:
            self.deleted = False
            self.deleted_on = None
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
            super(SafeModel, self).save(**kwargs)
        elif current_policy == SOFT_DELETE_CASCADE:
            deleted_timestamp = timezone.now()
            for related_field in self.related_fields():
                if related_field.__class__.__name__ in self._soft_cascade_classes:
                    related_field.delete(deleted_on=deleted_timestamp, **kwargs)
            self.delete(force_policy=SOFT_DELETE, deleted_on=deleted_timestamp, **kwargs)
        elif current_policy == NO_DELETE:
            return

    def undelete(self, force_policy=None, deleted_on=None, **kwargs):
        assert self.deleted

        current_policy = force_policy or self._safe_policy

        # Check if the delete was from a cascade of the original delete
        if deleted_on and self.deleted_on != deleted_on:
            return

        if current_policy == SOFT_DELETE_CASCADE:
            for related_field in self.related_fields():
                if related_field.__class__.__name__ in self._soft_cascade_classes and related_field.deleted:
                    related_field.undelete(deleted_on=self.deleted_on, **kwargs)

        self.save(**kwargs)
