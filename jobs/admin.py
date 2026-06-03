from django.contrib import admin
from .models import Job,Application

admin.site.register(Job)
admin.site.register(Application)
from .models import (
    AIInterviewSession,
    AIQuestion,
    AIAnswer,
    CallLog
)

admin.site.register(AIInterviewSession)
admin.site.register(AIQuestion)
admin.site.register(AIAnswer)
admin.site.register(CallLog)
# Register your models here.
