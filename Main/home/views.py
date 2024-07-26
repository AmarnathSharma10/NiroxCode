from django.shortcuts import render
from django.shortcuts import render,redirect
from home.forms import CodeRunnerForm
from django.conf import settings
from django.template import loader
from django.http import HttpResponse
from home.models import Problem,TestCase,Submission
from django.contrib.auth.decorators import login_required# Create your views here.
import os
import uuid
from pathlib import Path
import subprocess
@ login_required
def all_problems(request):
    all_problems = Problem.objects.filter(for_contest=False)


    context = {
        'all_problems':all_problems,
    }
    template = loader.get_template('all_problems.html')

    return HttpResponse(template.render(context,request))
# Create your views here.
@login_required
def problem_desc(request,problem_id):
    problem=Problem.objects.get(id=problem_id)
    submission_result=None
    if request.method == "POST":
        form = CodeRunnerForm(request.POST)
        action=request.POST.get('action')
        if form.is_valid():
            run = form.save(commit=False)
            if action=="run_code":


                op = run_code(run.language, run.code, run.input_data)
                run.output_data = op

                run.save()

                # context = {
                #     'problem': problem,
                #     'Run': run,
                #     'form': form,
                # }
                form = CodeRunnerForm(instance=run)
            elif action=="submit_code":

                submission_result = Submit(run.language, run.code, problem_id,request.user.id)
                run.verdict=submission_result

                run.save()
                form = CodeRunnerForm(instance=run)
    else:
        form = CodeRunnerForm()

    context = {
        'problem': problem,
        'form': form,
        'submission result':submission_result
    }
    return render(request, "problem.html", context)

@login_required
def my_submissions(request):
    user_submissions = Submission.objects.filter(user_id=request.user.id)
    context = {
        'submissions': user_submissions
    }
    return render(request, 'my_submissions.html', context)




def run_code(language, code, input_data):
    project_path = Path(settings.BASE_DIR)
    directories = ["codes", "inputs", "outputs"]

    for directory in directories:
        dir_path = project_path / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)

    codes_dir = project_path / "codes"
    inputs_dir = project_path / "inputs"
    outputs_dir = project_path / "outputs"

    unique = str(uuid.uuid4())
    if language=="java":
        jc=codes_dir/"javaC"
        code_folder=jc/unique
        if not code_folder.exists():
            code_folder.mkdir(parents=True, exist_ok=True)
        code_file_name="Main.java"
        code_file_path=code_folder/code_file_name

    else:
        code_file_name = f"{unique}.{language}"
        code_file_path = codes_dir / code_file_name
    input_file_name = f"{unique}.txt"
    output_file_name = f"{unique}.txt"

    input_file_path = inputs_dir / input_file_name
    output_file_path = outputs_dir / output_file_name

    with open(code_file_path, "w") as code_file:
        code_file.write(code)

    with open(input_file_path, "w") as input_file:
        input_file.write(input_data)


    with open(output_file_path, "w") as output_file:
        pass

    if language == "cpp":
        executable_path = codes_dir / unique
        compile_result = subprocess.run(
            ["g++", str(code_file_path), "-o", str(executable_path)]
        )
        if compile_result.returncode == 0:
            with open(input_file_path, "r") as input_file:
                with open(output_file_path, "w") as output_file:
                    subprocess.run(
                        [str(executable_path)],
                        stdin=input_file,
                        stdout=output_file,
                    )
    elif language == "c":
        executable_path = codes_dir / unique
        compile_result = subprocess.run(
            ["gcc", str(code_file_path), "-o", str(executable_path)]
        )
        if compile_result.returncode == 0:
            with open(input_file_path, "r") as input_file:
                with open(output_file_path, "w") as output_file:
                    subprocess.run(
                        [str(executable_path)],
                        stdin=input_file,
                        stdout=output_file,
                    )

    elif language == "py":
        # Code for executing Python script
        with open(input_file_path, "r") as input_file:
            with open(output_file_path, "w") as output_file:
                subprocess.run(
                    ["python", str(code_file_path)],
                    stdin=input_file,
                    stdout=output_file,
                )
    elif language == "java":


            compile_result = subprocess.run(
                ["javac", str(code_file_path)]
            )
            if compile_result.returncode == 0:
                with open(input_file_path, "r") as input_file:
                    with open(output_file_path, "w") as output_file:

                        subprocess.run(
                            ["java", str(code_file_path)],
                            stdin=input_file,
                            stdout=output_file,
                        )
            else:
                output_data="compilation error"
                return output_data

    # Read the output from the output file
    with open(output_file_path, "r") as output_file:
        output_data = output_file.read()

    return output_data
def Submit(language,code,p_id,u_id):
    try:
        problem = Problem.objects.get(id=p_id)
    except Problem.DoesNotExist:
        return "________________Problem with given ID does not exist________________."
    print(f"{problem}")
    result=""
    tests=TestCase.objects.filter(problem=problem)
    if not tests.exists():
        return "No test cases available for this problem."

    for test in tests:
        Testinput=test.input
        TestOutput=test.output
        runOutput=run_code(language,code,Testinput)
        if runOutput.strip()!=TestOutput.strip():
            verdict="Rejected"
            result+=f"Input: {Testinput}"
            result+=f"Expected output: {TestOutput} \n"
            result+=f"received  output: {runOutput} "

            submission=Submission(problem=problem,language=language,code=code,verdict=verdict,user_id=u_id)
            submission.save()
            return result

    verdict="Accepted"
    submission = Submission(problem=problem, language=language, code=code, verdict=verdict,user_id=u_id)
    submission.save()
    result+="ACCEPTED for all test cases"
    return result
