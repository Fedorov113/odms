from django.db import models
from django.contrib.postgres.fields import JSONField

from django.contrib.auth.models import User

class MetaSchema(models.Model):
    name = models.CharField(max_length=200, unique=True)
    short_name = models.CharField(max_length=30, unique=True,
                                  help_text='Short human readable id of schema. Digits, Letters, _, - allowed.')
    schema = JSONField(blank=True)

    def __str__(self):
        return self.name


class Study(models.Model):
    full_name = models.CharField(max_length=200)
    df_name = models.CharField(max_length=200, unique=True)
    df_description = models.CharField(max_length=2000, default='Empty')

    # comes_from = models.CharField(max_length=256, default='Internal')

    def_source_schema = models.ForeignKey(MetaSchema,
                                          null=True,
                                          blank=True,
                                          on_delete=models.SET_NULL,
                                          related_name='def_source_schema')
    def_biospecimen_schema = models.ForeignKey(MetaSchema,
                                               null=True,
                                               blank=True,
                                               on_delete=models.SET_NULL,
                                               related_name='def_biospecimen_schema')

    # fs_prefix = models.CharField(max_length=1024)


    users = models.ManyToManyField(User, through='Membership')

    def __str__(self):
        return self.df_name

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)

    ADMIN = 'ADMIN'
    PARTICIPANT = 'PARTICIPANT'
    DOCTOR = 'DOCTOR'
    SCIENTIST = 'SCIENTIST'
    GUEST = 'GUEST'
    ROLES_IN_STUDY_CHOICES = [
        (ADMIN, 'ADMIN'),
        (PARTICIPANT, 'PARTICIPANT'),
        (DOCTOR, 'DOCTOR'),
        (SCIENTIST, 'SCIENTIST'),
        (GUEST, 'GUEST'),
    ]
    role = models.CharField(
        max_length=11,
        choices=ROLES_IN_STUDY_CHOICES,
        default=GUEST,
    )

class SampleSource(models.Model):
    df = models.ForeignKey(Study
, on_delete=models.CASCADE)

    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    # this one is for connecting to other services
    ids = models.TextField(blank=True)  # {'service': <identificator>}; {'rcpcm_cdr': 1234dcertr}

    # This needs to be a reference to schema entry
    # or should we have one main schema and then arbitrary references to entries?
    meta_schema = models.ForeignKey(MetaSchema, on_delete=models.CASCADE, blank=True, null=True)
    meta_info = JSONField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    date_of_inclusion = models.DateField(null=True, blank=True)


    def __str__(self):
        return self.name


class Entry(models.Model):
    source = models.ForeignKey(SampleSource, on_delete=models.CASCADE, related_name='entries')

    meta_schema = models.ForeignKey(MetaSchema, on_delete=models.CASCADE, blank=True, null=True)
    meta_info = JSONField(blank=True)

    # date_time_of_entry = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    date_of_entry = models.DateField(null=True, blank=True)


class Biospecimen(models.Model):
    source = models.ForeignKey(SampleSource, on_delete=models.CASCADE, related_name='real_samples')
    description = models.TextField(blank=True)
    name = models.CharField(max_length=200, blank=True)
    date_of_collection = models.DateField(blank=True, null=True)
    time_point = models.PositiveIntegerField(blank=True, null=True)
    meta_schema = models.ForeignKey(MetaSchema, on_delete=models.CASCADE, blank=True, null=True)
    meta_info = JSONField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('source', 'name')

    def __str__(self):
        return self.source.name + '_' + self.name
