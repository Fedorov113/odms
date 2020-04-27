from django.urls import path, include
from .views import *

urlpatterns = [
    path('dataset_hard/', StudyList.as_view(), name='dataset-hard-list'),
    path('dataset_hard/<int:pk>/', StudyDetail.as_view(), name='dataset-rud'),

    path('dataset/<int:df_pk>/source/', SampleSourceList.as_view()),

    path('source_/', SourceList.as_view()),
    path('biospecimen/', BiospecimenList.as_view()),

    path('real_sample/', RealSampleList.as_view()),
    path('source/', SampleSourceList.as_view()),
    path('source/<int:pk>/', SourceDetail.as_view()),

    path('entry/', EntryList.as_view()),

    path('schema/', SchemaList.as_view()),

    
    path('dataset_hard_full/', StudyFull.as_view(), name='dataset-hard-full'),

    path('sample_source/', SampleSourceList.as_view()),

]
