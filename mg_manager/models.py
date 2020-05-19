from django.db import models
from django.contrib.postgres.fields import JSONField

from django.contrib.auth.models import User


class MetaSchema(models.Model):
    name = models.CharField(max_length=200, unique=True)
    short_name = models.CharField(max_length=30, unique=True,
                                  help_text='Short human readable id of schema. Digits, Letters, _, - allowed.')
    schema = JSONField(blank=True)
    ui_schema = JSONField(blank=True, null=True)

    def __str__(self):
        return self.name


class SchemaCollection(models.Model):
    name = models.CharField(max_length=256)
    schemas = models.ManyToManyField(MetaSchema, through='SchemaCollectionOrder')
    def __str__(self):
        return self.name

class SchemaCollectionOrder(models.Model):
    order = models.PositiveIntegerField()
    schema = models.ForeignKey(MetaSchema, on_delete=models.CASCADE)
    collection = models.ForeignKey(SchemaCollection, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.collection) + ' - ' + str(self.schema) 
    class Meta:
        ordering = ('order',)

class Study(models.Model):
    full_name = models.CharField(max_length=200)
    df_name = models.CharField(max_length=200, unique=True)
    df_description = models.CharField(max_length=2000, default='Empty')

    rich_text = models.TextField(null=True, blank=True)

    schemas_in_study = models.ManyToManyField(MetaSchema)

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

    def __str__(self):
        return str(self.study) + ' - ' + str(self.user)


class SampleSource(models.Model):
    df = models.ForeignKey(Study, on_delete=models.CASCADE)

    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    # this one is for connecting to other services
    # {'service': <identificator>}; {'rcpcm_cdr': 1234dcertr}
    ids = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    date_of_inclusion = models.DateField(null=True, blank=True)

    meta_schema = models.ForeignKey(
        MetaSchema, on_delete=models.CASCADE, blank=True, null=True)
    meta_info = JSONField(blank=True, null=True)

    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name





class CollectionEntry(models.Model):
    source = models.ForeignKey(
        SampleSource, on_delete=models.CASCADE, related_name='collection_entries')
    primary = models.BooleanField(default=False)
    schema_collection = models.ForeignKey(
        MetaSchema, on_delete=models.CASCADE, blank=True, null=True)
    

    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

class Entry(models.Model):
    source = models.ForeignKey(
        SampleSource, on_delete=models.CASCADE, related_name='entries')


    collection_entry = models.ForeignKey(CollectionEntry, on_delete=models.CASCADE, blank=True, null=True)

    primary = models.BooleanField(default=False)
    meta_schema = models.ForeignKey(
        MetaSchema, on_delete=models.CASCADE, blank=True, null=True)
    meta_info = JSONField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    date_of_entry = models.DateField(null=True, blank=True)


class Biospecimen(models.Model):
    source = models.ForeignKey(
        SampleSource, on_delete=models.CASCADE, related_name='biospecimens')

    name = models.CharField(max_length=200, unique=True)
    serial_number = models.PositiveIntegerField()
    biospecimen_type = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    date_of_collection = models.DateField()
    time_of_collection = models.TimeField()

    creation_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name
