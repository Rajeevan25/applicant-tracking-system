from django.db import models
from django.contrib.auth import get_user_model
import uuid

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='%(class)s_created')
    # updated_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='%(class)s_updated')

    class Meta:
        abstract = True