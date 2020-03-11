"""Core models."""

import uuid

from django.db import models


class BaseModel(models.Model):
    """Base model for add create and update time."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_on']
