# Wikipedia Explorer

A modern web application that helps users discover, search, and interact with Wikipedia articles. The system provides personalized article recommendations based on user preferences, trending articles, and search functionality.

Wikipedia Explorer

## Features

- 🔍 Search for Wikipedia articles through MediaWiki API
- 💫 Personalized article recommendations
- 🔥 Trending articles section
- ❤️ Like/unlike functionality for articles
- 👤 User authentication and profiles
- 🌐 Responsive design for all devices
- ∞ Infinite scrolling for articles

## Tech Stack

### Backend
- Django 4.2+ (Python web framework)
- Django REST Framework (API)
- PostgreSQL (Database)
- MediaWiki API integration

### Frontend
- React 18 (JavaScript library)
- React Router (Routing)
- Axios (API requests)
- Bootstrap 5 (CSS framework)

### Infrastructure
- Docker & Docker Compose
- Nginx (Frontend serving)
- Gunicorn (WSGI server)

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Installation & Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/django_postgres_api.git
cd django_postgres_api
```

2. Create a `.env` file in the root directory with the following contents:
```
# Django settings
DEBUG=True
SECRET_KEY=django-insecure-development-key-change-me-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,web
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://localhost:3000

# Database settings
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DATABASE_URL=postgres://postgres:postgres@db:5432/postgres

# Other settings
PYTHONUNBUFFERED=1
```

3. Build and start the Docker containers
```bash
docker-compose build
docker-compose up
```

4. Access the application
   - Frontend: http://localhost:3000
   - API: http://localhost:8000/api/
   - Admin interface: http://localhost:8000/admin/

## Project Architecture

The application follows a modern architecture with a decoupled frontend and backend:

- **Django Backend**: Provides RESTful API endpoints, handles database operations, user authentication, and article recommendations
- **React Frontend**: Delivers a dynamic single-page application with responsive UI components
- **PostgreSQL**: Stores user data, article metadata, and interaction history
- **Docker**: Containerizes all components for easy development and deployment

## API Endpoints

### Authentication
- `POST /api/auth/token/` - Obtain authentication token
- `GET /api/csrf/` - Get CSRF token for secure form submission

### Users
- `POST /api/users/` - Register new user
- `GET /api/users/profile/` - Get current user profile

### Articles
- `GET /api/articles/recommended/` - Get personalized article recommendations
- `GET /api/articles/trending/` - Get trending articles
- `GET /api/articles/search/?q={query}` - Search for articles
- `POST /api/articles/{id}/like/` - Like/unlike an article

## Project Structure

```
django_postgres_api/
│
├── articles/                    # Django app for article management
│   ├── migrations/              # Database migrations
│   ├── services/                # Service classes for external APIs
│   ├── models.py                # Article data models
│   ├── serializers.py          # DRF serializers
│   ├── views.py                # API views
│   └── urls.py                 # API URL routing
│
├── users/                      # Django app for user management
│   ├── migrations/             
│   ├── models.py
│   └── views.py
│
├── frontend/                   # React frontend
│   ├── public/                 # Static assets
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── pages/              # Page components
│   │   ├── services/           # API service modules
│   │   ├── styles/             # CSS files
│   │   ├── App.js              # Main React component
│   │   └── index.js            # React entry point
│   ├── Dockerfile              # Frontend Docker configuration
│   └── nginx.conf              # Nginx configuration
│
├── django_postgres_api/        # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── .env                        # Environment variables
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Backend Docker configuration
├── manage.py                   # Django management script
└── README.md                   # Project documentation
```

## Development Workflow

### Running in Development Mode

The Docker Compose setup provides a development environment with hot-reloading:

- Backend changes are automatically applied
- Frontend changes trigger React hot-reloading

### Useful Commands

```bash
# Start all containers
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Run Django management commands
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# Rebuild containers after dependency changes
docker-compose build
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
