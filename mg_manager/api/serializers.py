import json

import requests
from rest_framework import serializers

from odms import settings
from ..models import *

from rest_framework.utils.serializer_helpers import ReturnDict


class DictSerializer(serializers.ListSerializer):
    """
    Overrides default ListSerializer to return a dict with a custom field from
    each item as the key. Makes it easier to normalize the data so that there
    is minimal nesting. dict_key defaults to 'id' but can be overridden.
    """
    dict_key = 'id'

    @property
    def data(self):
        """
        Overriden to return a ReturnDict instead of a ReturnList.
        """
        ret = super(serializers.ListSerializer, self).data
        return ReturnDict(ret, serializer=self)

    def to_representation(self, data):
        """
        Converts the data from a list to a dictionary.
        """
        items = super(DictSerializer, self).to_representation(data)
        return {item[self.dict_key]: item for item in items}


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'
        list_serializer_class = DictSerializer


class BiospecimenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biospecimen
        fields = '__all__'



class MetaSchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaSchema
        fields = '__all__'
        list_serializer_class = DictSerializer


class SchemaCollectionOrderSerializer(serializers.HyperlinkedModelSerializer):
    schema_id = serializers.ReadOnlyField(source='schema.id')
    id = serializers.ReadOnlyField(source='schema.id')
    # schema = MetaSchemaSerializer()

    class Meta:
        model = SchemaCollectionOrder
        fields = ('id', 'schema_id', 'order', )


class SchemaCollectionSerializer(serializers.ModelSerializer):
    schemas = SchemaCollectionOrderSerializer(
        source='schemacollectionorder_set', many=True)
    num_schemas_in_collection = serializers.SerializerMethodField(
        read_only=True)

    def get_num_schemas_in_collection(self, schema_collection):
        return schema_collection.schemas.count()

    class Meta:
        model = SchemaCollection
        fields = '__all__'


class CollectionEntrySerializer(serializers.ModelSerializer):
    collection_entries = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)

    class Meta:
        model = CollectionEntry
        fields = '__all__'
        list_serializer_class = DictSerializer


class SourceSerializer(serializers.ModelSerializer):
    entries = EntrySerializer(many=True)
    collection_entries = CollectionEntrySerializer(many=True)
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
    collection_entries = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)
    entries = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = SampleSource
        fields = '__all__'
    #     extra_fields = ['biospecimens']

    # def get_field_names(self, declared_fields, info):
    #     expanded_fields = super(SampleSourceSerializer,
    #                             self).get_field_names(declared_fields, info)
    #     if getattr(self.Meta, 'extra_fields', None):
    #         return expanded_fields + self.Meta.extra_fields
    #     else:
    #         return expanded_fields


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
