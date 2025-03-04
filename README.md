# Django PostgreSQL API

A RESTful API built with Django and PostgreSQL, containerized with Docker.

## Features

- Custom User model
- Authentication endpoints (login, logout, signup)
- User profile endpoint
- PostgreSQL database
- Docker Compose setup

## Quick Start

1. Clone the repository
2. Run `docker-compose up`
3. Access the API at http://localhost:8000/api/
4. Access the admin interface at http://localhost:8000/admin/ (Username: admin, Password: adminpassword)

## API Endpoints

- `POST /api/signup/`: Create a new user account
- `POST /api/login/`: Login with username and password
- `POST /api/logout/`: Logout (requires authentication)
- `GET/PUT /api/profile/`: Get or update user profile (requires authentication)
