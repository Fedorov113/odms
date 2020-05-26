from django.urls import path, include
from .views import *

urlpatterns = [
    path('study/', StudyList.as_view(), name='study-list'),
    path('study/<int:pk>/', StudyDetail.as_view(), name='dataset-rud'),
    path('study/<int:df_pk>/source/', SampleSourceList.as_view()),
    path('study/<int:study_pk>/entry/', EntryList.as_view()),
    path('study/<int:study_pk>/collection_entry/', CollectionEntryList.as_view()),

    path('source/', SampleSourceList.as_view()),
    path('source/<int:pk>/', SourceDetail.as_view()),
    path('source/<int:source_pk>/biospecimen/', BiospecimenList.as_view()),

    path('entry/', EntryList.as_view()),

    path('schema/', SchemaList.as_view()),
    path('schema_collection/', SchemaCollectionList.as_view()),

    path('biospecimen/', BiospecimenList.as_view()),
    
]
