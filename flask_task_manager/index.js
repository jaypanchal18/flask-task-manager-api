import os

# Define the project structure
project_structure = {
    "flask_task_manager": {
        "api": {},
        "models": {},
        "routes": {},
        "tests": {},
        "config.py": "",
        "app.py": "",
        "requirements.txt": "",
        "Dockerfile": "",
        "docker-compose.yml": ""
    }
}

def create_project_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_project_structure(path, content)
        else:
            with open(path, 'w') as f:
                f.write(content)

try:
    create_project_structure(os.getcwd(), project_structure)
    print("Project structure created successfully.")
except Exception as e:
    print(f"Error creating project structure: {e}")