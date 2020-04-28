from rest_framework import generics, mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework.permissions import IsAuthenticated

from knox.auth import TokenAuthentication

from django.http import HttpResponse
from django.db.models import Q, Sum
from django.core.serializers.json import DjangoJSONEncoder

import os, glob, json

from .serializers import *

class StudyList(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Study.objects.all()
    serializer_class = StudySerializer
    # print(self)
    def get_queryset(self, *args, **kwargs):
        print(self.request.user)
        return Study.objects.filter(users=self.request.user)
        


class StudyDetail(generics.RetrieveUpdateDestroyAPIView):  # Detail View
    queryset = Study.objects.all()
    serializer_class = StudySerializer


class StudyFull(generics.ListCreateAPIView):
    serializer_class = StudyFullSerializer
    queryset = Study.objects.all()
    
class SourceList(generics.ListCreateAPIView):
    serializer_class = SourceSerializer

    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(SourceList, self).get_serializer(*args, **kwargs)

    def get_queryset(self):
        qs = SampleSource.objects.all()
        if 'df_pk' in self.kwargs:
            hard_df_pk = self.kwargs['df_pk']
            print(hard_df_pk)
            if hard_df_pk is not None:
                qs = qs.filter(
                    Q(df=hard_df_pk)
                ).distinct()
        return qs


class SourceDetail(generics.RetrieveUpdateDestroyAPIView):  # Detail View
    queryset = SampleSource.objects.all()
    serializer_class = SourceSerializer


class BiospecimenList(generics.ListCreateAPIView):
    serializer_class = BiospecimenSerializer
    queryset = Biospecimen.objects.all()

    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(BiospecimenList, self).get_serializer(*args, **kwargs)

class EntryList(generics.ListCreateAPIView):
    serializer_class = EntrySerializer
    queryset = Entry.objects.all()


class SampleSourceList(generics.ListCreateAPIView):
    serializer_class = SampleSourceSerializer

    def list(self, request, **kwargs):
        sources_dict = {}
        sources = self.get_queryset()

        for source in sources:
            biospecimens = [rs.id for rs in source.real_samples.all()]
            meta = {}
            try:
                meta = json.loads(source.meta_info)
            except:
                meta = None
            print(source.meta_schema)
            sources_dict[source.id] = {'id': source.id,
                                       'df': source.df.id,
                                       'name': source.name,
                                       'description': source.description,
                                       'meta_info': source.meta_info,
                                       # 'meta_schema': source.meta_schema.id,
                                       'created': source.created,
                                       'real_samples': biospecimens,
                                       'date_of_inclusion': source.date_of_inclusion
                                       }
            if source.meta_schema is not None:
                sources_dict[source.id].update({'meta_schema': source.meta_schema.id})

        return Response(sources_dict)

    def post(self, request, **kwargs):

        print('posting source')
        data = request.data

        source = SampleSource(df_id=data['df_id'],
                              name=data['name'],
                              description=data['description'],
                              meta_info=data['meta_info'],
                              date_of_inclusion = data['date_of_inclusion'],
                              meta_schema=MetaSchema.objects.get(id=data['meta_schema']))
        source.save()
        return HttpResponse(json.dumps('created'), content_type='application/json')

    def get_queryset(self):
        qs = None
        if 'df_pk' in self.kwargs:
            hard_df_pk = self.kwargs['df_pk']
            if hard_df_pk is not None:
                qs = SampleSource.objects.filter(Q(df=hard_df_pk)).prefetch_related('real_samples')
        else:
            qs = SampleSource.objects.all().prefetch_related('real_samples')

        return qs


class RealSampleList(APIView):
    def get(self, request):
        samples_dict = {}
        rsamples = Biospecimen.objects.all().prefetch_related('mg_samples')
        print(len(rsamples))
        for sample in rsamples:
            meta = {}
            try:
                meta = json.loads(sample.meta_info)
            except:
                meta = None
            mgsamps = [rs.id for rs in sample.mg_samples.all()]
            samples_dict[sample.id] = {
                'id': sample.id,
                'source': sample.source_id,
                'time_point': sample.time_point,
                'name': sample.name,
                'description': sample.description,
                'meta_info': sample.meta_info,
                'created': sample.created,
                'date_of_collection': sample.date_of_collection,
                'mg_samples': mgsamps,
            }
        return HttpResponse(json.dumps(samples_dict, cls=DjangoJSONEncoder), content_type='application/json')

    def post(self, request):
        data = request.data
        real_sample = Biospecimen(**data)
        real_sample.save()
        return HttpResponse(json.dumps('created'), content_type='application/json')


class SchemaList(APIView):
    def get(self, request):
        schemas_dict = {}
        schemas = MetaSchema.objects.all()
        for schema in schemas:
            schemas_dict[schema.id] = {
                'id': schema.id,
                'name': schema.name,
                'schema': schema.schema
            }

        return HttpResponse(json.dumps(schemas_dict), content_type='application/json')



class RealSampleUpdate(APIView):
    def put(self, request):
        data = request.data
        print(data)
        for key in data.keys():
            s, created = Biospecimen.objects.update_or_create(defaults=data[key], pk=key)

        return HttpResponse(json.dumps('update'), content_type='application/json')


