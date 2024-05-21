from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Tag)
admin.site.register(Learner)
admin.site.register(Educator)
admin.site.register(Session)
admin.site.register(Review)