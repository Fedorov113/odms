from rest_framework import generics, mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework.permissions import IsAuthenticated

from knox.auth import TokenAuthentication
from django.http import HttpResponse
from django.db.models import Q, Sum, Count
from django.core.serializers.json import DjangoJSONEncoder

import os
import glob
import json

from .serializers import *


class StudyList(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Study.objects.all()
    serializer_class = StudySerializer
    # print(self)

    def get_queryset(self, *args, **kwargs):
        return Study.objects.filter(users=self.request.user)


class StudyDetail(generics.RetrieveUpdateDestroyAPIView):  # Detail View
    queryset = Study.objects.all()
    serializer_class = StudySerializer


class StudyFull(generics.ListCreateAPIView):
    serializer_class = StudyFullSerializer
    queryset = Study.objects.all()


class SchemaCollectionList(generics.ListCreateAPIView):
    serializer_class = SchemaCollectionSerializer
    queryset = SchemaCollection.objects.all().annotate(
        numbooks=Count('schemas')
    )


class SourceDetail(generics.RetrieveUpdateDestroyAPIView):  # Detail View
    queryset = SampleSource.objects.all()
    serializer_class = SourceSerializer


class BiospecimenList(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    serializer_class = BiospecimenSerializer

    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(BiospecimenList, self).get_serializer(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        qs = Biospecimen.objects.all()
        if 'source_pk' in self.kwargs:
            source_pk = self.kwargs['source_pk']
            if source_pk is not None:
                qs = qs.filter(
                    Q(source=source_pk)
                ).distinct()
        return qs


class EntryList(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    serializer_class = EntrySerializer

    queryset = Entry.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class SampleSourceList(generics.ListCreateAPIView):
    serializer_class = SampleSourceSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, **kwargs):
        sources_dict = {}
        sources = self.get_queryset()

        for source in sources:
            biospecimens = [rs.id for rs in source.biospecimens.all()]
            sources_dict[source.id] = {'id': source.id,
                                       'df': source.df.id,
                                       'name': source.name,
                                       'description': source.description,
                                       'created': source.created,
                                       'biospecimens': biospecimens,
                                       'date_of_inclusion': source.date_of_inclusion,
                                       }

        return Response(sources_dict)

    def post(self, request, **kwargs):

        data = request.data

        print(data)

        source = SampleSource(df_id=data['df_id'],
                              created_by=self.request.user,
                              name=data['name'],
                              description=data['description'],
                              date_of_inclusion=data['date_of_inclusion']
                              )
        source.save()
        print('======ID===', source.id)

        collection_entry = CollectionEntry(
            source_id=source.id,
            schema_collection_id=data['schema_collection']
        )
        collection_entry.save()

        collection_form_data = data['collection_form_data']
        entries = []
        for form_data in collection_form_data.keys():
            entries.append(
                Entry(source_id=source.id,
                      collection_entry_id=collection_entry.id,
                      meta_schema_id=form_data,
                      date_of_entry=data['date_of_inclusion'],
                      meta_info=collection_form_data[form_data]),
            )
        saved_entries = Entry.objects.bulk_create(entries)
        print(saved_entries)
        return HttpResponse(json.dumps('created'), content_type='application/json', status=201)

    def get_queryset(self):
        qs = None
        if 'df_pk' in self.kwargs:
            hard_df_pk = self.kwargs['df_pk']
            if hard_df_pk is not None:
                qs = SampleSource.objects.filter(
                    Q(df=hard_df_pk)).prefetch_related('biospecimens')
        else:
            qs = SampleSource.objects.all().prefetch_related('biospecimens')

        return qs


# class BiospecimenList(APIView):
#     def get(self, request):
#         samples_dict = {}
#         rsamples = Biospecimen.objects.all().prefetch_related('mg_samples')
#         print(len(rsamples))
#         for sample in rsamples:
#             meta = {}
#             try:
#                 meta = json.loads(sample.meta_info)
#             except:
#                 meta = None
#             mgsamps = [rs.id for rs in sample.mg_samples.all()]
#             samples_dict[sample.id] = {
#                 'id': sample.id,
#                 'source': sample.source_id,
#                 'time_point': sample.time_point,
#                 'name': sample.name,
#                 'description': sample.description,
#                 'meta_info': sample.meta_info,
#                 'created': sample.created,
#                 'date_of_collection': sample.date_of_collection,
#                 'mg_samples': mgsamps,
#             }
#         return HttpResponse(json.dumps(samples_dict, cls=DjangoJSONEncoder), content_type='application/json')

#     def post(self, request):
#         data = request.data
#         real_sample = Biospecimen(**data)
#         real_sample.save()
#         return HttpResponse(json.dumps('created'), content_type='application/json')


# class SchemaList(APIView):
#     def get(self, request):
#         schemas_dict = {}
#         schemas = MetaSchema.objects.all()
#         for schema in schemas:
#             schemas_dict[schema.id] = {
#                 'id': schema.id,
#                 'name': schema.name,
#                 'schema': schema.schema,
#                 'ui_schema': schema.ui_schema
#             }

#         return HttpResponse(json.dumps(schemas_dict), content_type='application/json')

class SchemaList(generics.ListCreateAPIView):
    serializer_class = MetaSchemaSerializer
    queryset = MetaSchema.objects.all()

class BiospecimenUpdate(APIView):
    def put(self, request):
        data = request.data
        print(data)
        for key in data.keys():
            s, created = Biospecimen.objects.update_or_create(
                defaults=data[key], pk=key)

        return HttpResponse(json.dumps('update'), content_type='application/json')
