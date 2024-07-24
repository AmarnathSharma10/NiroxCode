from django.urls import path
from home.views import all_problems,problem_desc,my_submissions

urlpatterns = [
    path('all_problems/', all_problems, name='home'),
    path('all_problems/<int:problem_id>/', problem_desc, name='detail'),
    path('submissions/',my_submissions,name='submissions')

]
