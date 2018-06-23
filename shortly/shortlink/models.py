from django.db import models

import uuid

class Link(models.Model):
    id = models.UUIDField(primary_key = True, default=uuid.uuid4)
    basic_link = models.CharField(max_length=256, blank=False, unique=False)
    visited = models.IntegerField(default=0)




