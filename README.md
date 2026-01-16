# Flask Task Manager API ![Build Status](https://img.shields.io/badge/build-passing-brightgreen) ![Version](https://img.shields.io/badge/version-1.0.0-blue) ![License](https://img.shields.io/badge/license-MIT-yellowgreen)

## Project Description
A modern RESTful API built with Python Flask for task management, featuring user authentication, CRUD operations, and database integration. This API allows users to create, manage, and prioritize tasks efficiently while ensuring secure access through JWT authentication.

## Features
- 🔒 User authentication with JWT for secure access
- 📋 CRUD operations for tasks (Create, Read, Update, Delete)
- 📂 Task categorization and prioritization
- 👤 User-specific task management with role-based access
- 🗄️ Integration with a PostgreSQL database for persistent storage
- 📖 API documentation using Swagger for easy reference
- ✅ Unit tests for API endpoints to ensure reliability

## Tech Stack
### Backend
- 🐍 Python
- ⚡ Flask
- 🗄️ PostgreSQL
- 🔗 SQLAlchemy
- 🔑 JWT

### DevOps
- 🐳 Docker

## Installation
To set up the project locally, follow these steps:

- Clone the repository
bash
git clone https://github.com/jaypanchal18/flask-task-manager-api.git
- Navigate to the project directory
bash
cd flask-task-manager-api
- Create a virtual environment
bash
python -m venv venv
- Activate the virtual environment
bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
- Install the required packages
bash
pip install -r requirements.txt
- Set up the database
bash
# Create the database
# Ensure PostgreSQL is running and configured
- Run the application
bash
flask run
## Usage
Once the application is running, you can access the API at `http://localhost:5000`. Use tools like Postman or curl to interact with the endpoints.

## API Documentation
API documentation is available using Swagger. After running the application, navigate to `http://localhost:5000/swagger` to explore the available endpoints and their usage.

## Testing
To run the tests for the API, execute the following command:
bash
pytest
## Deployment
For deployment, you can use Docker. Build the Docker image with:
bash
docker build -t flask-task-manager-api .
Run the container with:
bash
docker run -p 5000:5000 flask-task-manager-api
## Contributing
Contributions are welcome! Please follow these steps:
- Fork the repository
- Create a new branch (`git checkout -b feature/YourFeature`)
- Make your changes and commit them (`git commit -m 'Add some feature'`)
- Push to the branch (`git push origin feature/YourFeature`)
- Open a pull request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Thanks to the Flask community for their support and resources.
- Special thanks to contributors and users who provide feedback and improvements.