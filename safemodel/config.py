# -*- coding: utf-8 -*-


class SafePolicy(object):
    HARD_DELETE = 0
    SOFT_DELETE = 1
    SOFT_DELETE_CASCADE = 2
    HARD_DELETE_NOCASCADE = 3
    NO_DELETE = 4


class SafeVisibility(object):
    DELETED_INVISIBLE = 1
    DELETED_VISIBLE_BY_FIELD = DELETED_VISIBLE_BY_PK = 2
    DELETED_ONLY_VISIBLE = 3
    DELETED_VISIBLE = 4

