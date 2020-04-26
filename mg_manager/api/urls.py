from django.urls import path, include

from .views import *
from .anal_views import *

urlpatterns = [
    path('dataset/<int:df_pk>/source/', SampleSourceList.as_view()),

    path('source_/', SourceList.as_view()),
    path('biospecimen/', BiospecimenList.as_view()),

    path('real_sample/', RealSampleList.as_view()),
    path('source/', SampleSourceList.as_view()),
    path('source/<int:pk>/', SourceDetail.as_view()),

    path('entry/', EntryList.as_view()),

    path('schema/', SchemaList.as_view()),
    path('dataset_hard/', DatasetHardList.as_view(), name='dataset-hard-list'),
    path('dataset_hard/<int:pk>/', DatasetHardDetail.as_view(), name='dataset-rud'),

    path('dataset_hard/<int:pk>/mg_sample/', MgSampleFullList.as_view(), name='mg-sample-list-dataset'),
    path('dataset_hard/<int:hdf_pk>/mg_sample/<int:pk>', MgSampleDetail.as_view(), name='mg-sample-hdf-detail'),


    path('mg_sample/', MgSampleList.as_view(), name='mg-sample-list'),
    path('mg_sample_update/', MgSampleUpdate.as_view()),
    path('real_sample_update/', RealSampleUpdate.as_view()),

    path('mg_sample_container/', MgSampleContainerList.as_view(), name='mg-sample-container-list'),
    path('mg_sample_container_file/', MgSampleContainerFileList.as_view(), name='mg-sample-container-file-list'),

    path('mg_sample_lookup/', MgSampleNewList.as_view(), name='mg-sample-lookup'),

    path('dataset_hard_full/', DatasetHardFull.as_view(), name='dataset-hard-full'),


    path('mg_sample/<int:pk>', MgSampleDetail.as_view(), name='mg-sample-detail'),
    path('sample_source/', SampleSourceList.as_view()),

    path('library/', LibraryList.as_view(), name='library-list'),
    path('library/<int:pk>/', LibraryDetail.as_view(), name='library-rud'),

    path('mg_sample_full/', MgSampleFullList.as_view(), name='mg-sample-list'),
    path('', include(('mg_manager.result.urls', 'result'), namespace='result')),

    path('sequencing_run/', SequencingRunList.as_view(), name='SequencingRunList-list'),
    path('fs_samples/', FsContainerList.as_view(), name='SequencingRunList-list'),

    path('import_from_asshole/', ImportFromAsshole.as_view()),

]
