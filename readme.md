# Evently

### Project Overview
**Evently** is a backend service for creating, managing, and booking events. It is built on **Django** and **Django REST Framework**, using **Docker** for containerization. The project utilizes a microservice-like architecture to ensure scalability and fault tolerance, while also implementing advanced testing and CI/CD practices.

### Key Features
- **Event Management**: CRUD operations for creating, updating, viewing, and deleting events and venues.

- **Tickets and Orders Management:**

    - Users can book tickets for events.
    
    - Implements protection against race conditions during order creation using ```select_for_update()```, which guarantees data integrity.
    
    - Each user can only see their own orders, ensuring data security.
    
- **API Endpoints:** API users can filter and sort lists of orders and events.

- **Testing:** Comprehensive test coverage using Pytest, including parameterized tests for efficient verification of various scenarios.

- **DevOps:**

    - The project is containerized with Docker using ```docker-compose.yml```, making setup and deployment straightforward.

    - GitHub Actions is configured to automatically run tests on every commit, ensuring high code quality.

### Technologies
- **Backend:** Django, Django REST Framework

- **Testing:** Pytest

- **Database:** PostgreSQL

- **Containerization:** Docker, Docker Compose

- **CI/CD:** GitHub Actions

- **Dependencies:** Pipenv

### Installation and Launch
#### Prerequisites:
- Docker and Docker Compose

- Pipenv (for dependency management)

#### Steps:
1. Clone the repository:
```bash
git clone https://github.com/13dashaa/Evently.git
cd Evently
```

2. Create and configure environment variables by copying ```.env.example``` to ```.env``` and filling it out.

3. Run Docker Compose to build and start the services:
```bash
docker-compose up --build
```
4. Create a superuser:

```bash
docker-compose run --rm web pipenv run python manage.py createsuperuser
```
The project will be available at ```http://localhost:8000.```

### Running Tests
To run all tests, use the following command from the project root:

```bash
docker-compose run --rm web pipenv run pytest
```

### API Documentation
The API documentation is currently available at ```http://localhost:8000/api/``` via the standard DRF interface.