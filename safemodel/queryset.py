# -*- coding: utf-8 -*-
from django.db.models import query

from .config import SafeVisibility


class SafeModelQueryset(query.QuerySet):
    safe_visibility_policy = None

    def __init__(self, safe_visibility_policy=SafeVisibility.DELETED_INVISIBLE, *args, **kwargs):
        self.safe_visibility_policy = safe_visibility_policy
        super(SafeModelQueryset, self).__init__(*args, **kwargs)

    def delete(self, force_policy=None):
        """
        Deletes the records in the current QuerySet.
        """
        assert self.query.can_filter(), "Cannot use 'limit' or 'offset' with delete."

        if self._fields is not None:
            raise TypeError("Cannot call delete() after .values() or .values_list()")

        for obj in self.all():
            obj.delete(force_policy=force_policy)
        self._result_cache = None

    delete.alters_data = True

    def undelete(self, force_policy=None):
        assert self.query.can_filter(), "Cannot use 'limit' or 'offset' with undelete."
        # TODO: Replace this by bulk update if we can (need to call pre/post-save signal)
        for obj in self.all():
            obj.undelete(force_policy=force_policy)
        self._result_cache = None

    undelete.alters_data = True
