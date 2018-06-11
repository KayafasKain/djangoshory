from django.db import models

import uuid

class Link(models.Model):
    id = models.UUIDField(primary_key = True, default=uuid.uuid4)
    basic_link = models.CharField(max_length=228)
    visited = models.IntegerField(default=0)




