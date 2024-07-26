# Niroxcode


*Table of Contents*

- What is niroxcode? features of niroxcode
- directory structure
- requirements and Setup
- How to run it on your local host?
  ## What is niroxcode?
  **Niroxcode is a django based online coding platform that supports multiple programming languages . It allows users to write, compile, run and submit code in a web-based interface.Serves the functionality of Online Judge**
  ## features of niroxcode
  


- supports multiple languages(java, python, c and c++)
- easy Administration(test cases and problems can be added and deleted easily via django admin )
- Upon rejection of code for a certain problem user can view test case input, expected output and generated output for a test case
  


### Directory Structure

**There are a total of 3 apps in this project as of now Main,accounts and home**


**Main/**
- `__init__.py`: Indicates that this directory should be treated as a Python package.
- `settings.py`: Contains all the settings and configuration for the Django project.
- `urls.py`: Defines the URL patterns for the Django project.
- `wsgi.py`: Serves as an entry point for WSGI-compatible web servers to serve the project.
- `asgi.py`: Serves as an entry point for ASGI-compatible web servers to serve the project.

**accounts/**
- `migrations/`: Contains migration files for database changes.
- `templates/`: Contains HTML templates for the accounts app.
- `__init__.py`: Indicates that this directory should be treated as a Python package.
- `admin.py`: Registers models to be managed via the Django admin interface.
- `apps.py`: Configuration for the accounts app.
- `models.py`: Defines the data models for the accounts app.
- `tests.py`: Contains test cases for the accounts app.
- `views.py`: Contains view functions that handle requests and return responses for the accounts app.

**home/**
- Similar structure to the `accounts` app, tailored for the main functionality of the project.

**codes/**
- `javaC/`: Directory to store Java-related code submissions.

**inputs/** and **outputs/**
- Directories to store input and output files for code execution.

**manage.py**
- A command-line utility that lets you interact with this Django project in various ways.

**Dockerfile**
- Instructions to build a Docker image for the project.

**requirements.txt**
- A file listing the Python dependencies required for the project.

## Setup
**Make Sure to clone the directory first**
```bash
   git clone https://github.com/yourusername/niroxcode.git
   cd niroxcode
```
### Setup using docker
**Prerequisites** install docker desktop


To build the Docker image, use the following command:
        `docker build -t niroxcode:latest .`

run docker container( and map the ports):
        `docker run -d -p 8000:8000 niroxcode:latest`

Open your web browser and navigate to http://localhost:8000 to access the 
application.

        
