# home/admin.py

from django.contrib import admin
from home.models import Problem,TestCase,Submission

from home.models import CodeRunner
from home.forms import CodeRunnerForm

class CodeRunnerAdmin(admin.ModelAdmin):
    form = CodeRunnerForm
    list_display = ['language', 'input_data', 'code', 'output_data', 'verdict']
    readonly_fields = ['output_data', 'verdict']

admin.site.register(CodeRunner, CodeRunnerAdmin)

admin.site.register(Problem)
admin.site.register(TestCase)
admin.site.register(Submission)

