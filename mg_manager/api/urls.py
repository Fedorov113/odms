from django.urls import path, include
from .views import *

urlpatterns = [
    path('dataset_hard/', StudyList.as_view(), name='study-list'),
    path('dataset_hard/<int:pk>/', StudyDetail.as_view(), name='dataset-rud'),
    path('study/<int:pk>/', StudyDetail.as_view(), name='dataset-rud'),

    path('study/<int:df_pk>/source/', SampleSourceList.as_view()),

    path('biospecimen/', BiospecimenList.as_view()),
    path('source/<int:source_pk>/biospecimen/', BiospecimenList.as_view()),

    path('source/', SampleSourceList.as_view()),
    path('source/<int:pk>/', SourceDetail.as_view()),

    path('entry/', EntryList.as_view()),

    path('schema/', SchemaList.as_view()),
    path('schema_collection/', SchemaCollectionList.as_view()),

    
    path('dataset_hard_full/', StudyFull.as_view(), name='dataset-hard-full'),

    path('sample_source/', SampleSourceList.as_view()),

]
