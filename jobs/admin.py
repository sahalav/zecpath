from .models import (
    AIInterviewSession,
    AIQuestion,
    AIAnswer,
    CallLog
)
from django.contrib import admin
from .models import Job, Application
from .models import Subscription


admin.site.register(Job)
admin.site.register(Application)

admin.site.register(AIInterviewSession)
admin.site.register(AIQuestion)
admin.site.register(AIAnswer)
admin.site.register(CallLog)
admin.site.register(Subscription)
# Register your models here.
