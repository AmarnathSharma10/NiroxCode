# home/admin.py

from django.contrib import admin
from home.models import Problem,TestCase,Submission



admin.site.register(Problem)
admin.site.register(TestCase)
admin.site.register(Submission)

