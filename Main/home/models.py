from django.db import models
from accounts.models import Profile
# Create your models here.
class Problem(models.Model):
    name=models.CharField(max_length=100)
    difficulty = models.CharField(
        max_length=10,
        blank=True,
        choices=[("Hard", "Hard"), ("Easy", "Easy"), ("Medium", "Medium")],
    )

    description=models.TextField()
    added_at=models.DateTimeField(auto_now_add=True)
    for_contest=models.BooleanField(default=False)
    has_image=models.BooleanField(default=False)
    image = models.ImageField(upload_to='media/images/', blank=True, null=True)
    def __str__(self):
        return self.name

class Submission(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user_id=models.IntegerField(default=1)
    verdict = models.CharField(max_length=50)
    submitted_at = models.DateTimeField(auto_now_add=True)
    code=models.TextField(default="")
    language=models.CharField(  max_length=10,
        blank=True,
        choices=[("Python","py"),("Java","java"),("c++","cpp"),("C","c")])
    def __str__(self):
        return f" submitted {self.problem}                  Verdict   {self.verdict}                            Time:  {self.submitted_at}"


class TestCase(models.Model):
    input = models.TextField(max_length=255)
    output = models.TextField(max_length=255)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.problem} {self.id}"


class CodeRunner(models.Model):
    language = models.CharField(
        max_length=10,
        blank=True,
        choices=[("py", "Python"), ("java", "Java"), ("cpp", "C++"), ("c", "C")]
    )

    code=models.TextField()
    time_stamp=models.DateTimeField(auto_now_add=True)
    input_data=models.TextField(null=True,blank=True)
    output_data=models.TextField(null=True,blank=True)
    verdict=models.TextField(null=True,blank=True)