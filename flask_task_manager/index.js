import os

# Define the base directory for the project
base_dir = 'flask_task_manager'

# Define the directory structure
directories = [
    'app',
    'app/config',
    'app/models',
    'app/routes',
    'app/tests',
    'app/static',
    'app/templates',
    'migrations',
    'instance'
]

# Create the directories
for directory in directories:
    try:
        os.makedirs(os.path.join(base_dir, directory), exist_ok=True)
    except Exception as e:
        print(f"Error creating directory {directory}: {e}")

# Create __init__.py files to make directories packages
init_files = [
    'app/__init__.py',
    'app/config/__init__.py',
    'app/models/__init__.py',
    'app/routes/__init__.py',
    'app/tests/__init__.py'
]

for init_file in init_files:
    try:
        with open(os.path.join(base_dir, init_file), 'w') as f:
            f.write("# This file is for package initialization\n")
    except Exception as e:
        print(f"Error creating file {init_file}: {e}")

# Create a Dockerfile
dockerfile_content = """FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]
"""

try:
    with open(os.path.join(base_dir, 'Dockerfile'), 'w') as f:
        f.write(dockerfile_content)
except Exception as e:
    print(f"Error creating Dockerfile: {e}")

# Create a requirements.txt file
requirements_content = """Flask==2.0.1
Flask-SQLAlchemy==2.5.1
Flask-JWT-Extended==4.3.1
psycopg2-binary==2.9.1
"""

try:
    with open(os.path.join(base_dir, 'requirements.txt'), 'w') as f:
        f.write(requirements_content)
except Exception as e:
    print(f"Error creating requirements.txt: {e}")