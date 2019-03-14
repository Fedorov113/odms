from django.contrib import admin
from .models import *
from .result.models import ProfileResult, Mp2Result
# Register your models here.

admin.site.register(DatasetHard)
admin.site.register(DatasetSoft)

admin.site.register(SampleSource)
admin.site.register(Biospecimen)
admin.site.register(MetaSchema)

admin.site.register(Library)

admin.site.register(SequencingRun)
admin.site.register(MgSample)
admin.site.register(MgSampleContainer)
admin.site.register(MgFile)
admin.site.register(ProfileResult)
admin.site.register(Mp2Result)


