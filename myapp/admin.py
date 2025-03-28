from django.contrib import admin

# Register your models here.
from myapp.models import CustomUser,CourseOutcome,ProgramOutcome,COPOMap,Assessment
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(CourseOutcome)

admin.site.register(ProgramOutcome)

admin.site.register(COPOMap)
admin.site.register(Assessment)


