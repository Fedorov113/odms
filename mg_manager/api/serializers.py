import json

import requests
from rest_framework import serializers

from odms import settings
from ..models import *


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'


class BiospecimenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biospecimen
        fields = '__all__'





class MetaSchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaSchema
        fields = '__all__'

class SchemaCollectionOrderSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='schema.id')
    name = serializers.ReadOnlyField(source='schema.name')
    class Meta:
        model = SchemaCollectionOrder
        fields = ('id', 'name', 'order', )

class SchemaCollectionSerializer(serializers.ModelSerializer):
    schemas = SchemaCollectionOrderSerializer(source='schemacollectionorder_set', many=True)
    class Meta:
        model = SchemaCollection
        fields = '__all__'

class SchemaCollectionEntrySerializer(serializers.ModelSerializer):
    # schemas = SchemaCollectionOrderSerializer(source='schemacollectionorder_set', many=True)
    class Meta:
        model = CollectionEntry
        fields = '__all__'



class SourceSerializer(serializers.ModelSerializer):
    entries = EntrySerializer(many=True)
    collection_entries = SchemaCollectionEntrySerializer(many=True)
    biospecimens = BiospecimenSerializer(many=True)

    class Meta:
        model = SampleSource
        fields = '__all__'
        # extra_fields = ['entries']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(SourceSerializer, self).get_field_names(
            declared_fields, info)
        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields



class StudySerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
        fields = '__all__'

    def validate_df_name(self, value):
        qs = Study.objects.filter(df_name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Study name must be unique")
        return value


class BiospecimenIdSerializer(serializers.ModelSerializer):
    # source = serializers.PrimaryKeyRelatedField(required=False, queryset=SampleSource.objects.all())

    class Meta:
        model = Biospecimen
        fields = ['pk']


class SampleSourceSerializer(serializers.ModelSerializer):
    biospecimens = BiospecimenIdSerializer(many=True)

    class Meta:
        model = SampleSource
        fields = '__all__'
        extra_fields = ['biospecimens']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(SampleSourceSerializer,
                                self).get_field_names(declared_fields, info)
        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class StudyFullSerializer(serializers.ModelSerializer):

    class Meta:
        model = Study
        fields = '__all__'

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(StudyFullSerializer, self).get_field_names(
            declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields
