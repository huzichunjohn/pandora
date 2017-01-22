from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Domain(models.Model):
    name = models.CharField(max_length=50)
    domain_id = models.PositiveIntegerField()
    
class Role(models.Model):
    domain = models.ForeignKey(Domain, related_name='roles', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='roles', on_delete=models.CASCADE)
    can_edit = models.BooleanField(default=False)   
