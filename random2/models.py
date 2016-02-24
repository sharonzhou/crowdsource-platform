from __future__ import unicode_literals

from django.contrib.postgres.fields import JSONField
from django.db import models

from crowdsourcing.models import Project


class Group(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)
    min_sequence = models.IntegerField(default=1)
    max_sequence = models.IntegerField()
    tasks_per_project = models.IntegerField(default=1)
    exclusive = models.BooleanField(default=False)


class ProjectGroup(models.Model):
    group = models.ForeignKey(Group, related_name='projects')
    project = models.ForeignKey(Project, related_name='groups')
    aux_attrib = JSONField(null=True)
