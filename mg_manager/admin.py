from django.contrib import admin
from .models import *

admin.site.register(Study)
admin.site.register(Membership)
admin.site.register(SampleSource)
admin.site.register(Biospecimen)
admin.site.register(MetaSchema)
admin.site.register(Entry)
admin.site.register(SchemaCollection)
admin.site.register(CollectionEntry)
admin.site.register(SchemaCollectionOrder)

