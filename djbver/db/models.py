from django.db import models


__all__ = [
    'GenericModel',
    'GenericAtiveModel',
]


class GenericModel(models):
    created = models.DateTimeField('생성일', auto_now_add=True)
    updated = models.DateTimeField('수정일', auto_now=True)

    class Meta:
        abstract = True


class GenericActiveModel(models):
    is_active = models.BooleanField('활성화 여부', default=True)
    
    created = models.DateTimeField('생성일', auto_now_add=True)
    updated = models.DateTimeField('수정일', auto_now=True)

    class Meta:
        abstract = True
