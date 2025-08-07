# Coderr Backend - Django REST API

A Django REST API backend for a freelancer platform with user authentication, profile management, offer system, orders, and reviews.

## Project Structure

```
coderr_backend/
├── coderr_app/         # Main app with models, views, serializers
├── auth_app/           # Authentication app
├── core/               # Django project settings and URLs
├── requirements.txt    # Python dependencies
├── manage.py          # Django management script
└── README.md          # This file
```

## Features

- **User Authentication** with token-based authentication
- **Profile Management** for Business and Customer users
- **Offer Management** with different packages (Basic, Standard, Premium)
- **Order Management** with status tracking
- **Review System** for completed orders
- **File Upload** for profiles and offers
- **Pagination** and filtering for all lists
- **CORS Support** for frontend integration

## Quick Start

### Clone Repository

```bash
git clone https://github.com/WladimirWagner/coderr_backend.git
cd coderr_backend
```

### Setup Environment

1. Create and activate virtual environment:
```bash
# Windows
python -m venv env
.\env\Scripts\activate

# Linux/Mac
python3 -m venv env
source env/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run database migrations:
```bash
python manage.py migrate
```

4. Start server:
```bash
python manage.py runserver
```

The backend server starts at `http://localhost:8000`

## Data Model

### Profile
- Extends Django User model
- Distinguishes between Business and Customer users
- Contains contact data, location and working hours

### Offers
- Service offerings from Business users
- Each offer can have multiple details (Basic, Standard, Premium)
- Automatic calculation of minimum price and delivery time

### OfferDetails
- Detailed offers with different prices and features
- Features stored as JSON list
- Different types: Basic, Standard, Premium

### Orders
- Orders between customers and Business users
- Automatic data copying from OfferDetail
- Status: in_progress, completed, cancelled

### Reviews
- Review system for completed orders
- Rating and description text
- Link between reviewer and Business user

## API Endpoints

### Authentication
- `POST /api/auth/registration/` - Register new user
- `POST /api/auth/login/` - User login
- `GET /api/auth/email-check/` - Check email availability

### Profiles
- `GET /api/profile/<id>/` - Get profile details
- `PATCH /api/profile/<id>/` - Update profile
- `GET /api/profiles/business/` - All business profiles
- `GET /api/profiles/customer/` - All customer profiles

### Offers
- `GET /api/offers/` - List all offers
- `POST /api/offers/` - Create new offer
- `GET /api/offers/<id>/` - Get offer details
- `PATCH /api/offers/<id>/` - Update offer
- `DELETE /api/offers/<id>/` - Delete offer

### Orders
- `GET /api/orders/` - All user orders
- `POST /api/orders/` - Create new order
- `GET /api/orders/<id>/` - Get order details
- `PATCH /api/orders/<id>/` - Update order
- `DELETE /api/orders/<id>/` - Delete order

### Reviews
- `GET /api/reviews/` - List all reviews
- `POST /api/reviews/` - Create new review
- `GET /api/reviews/<id>/` - Get review details
- `PATCH /api/reviews/<id>/` - Update review
- `DELETE /api/reviews/<id>/` - Delete review

## Test Data

The backend contains extensive test data:
- 10 users (5 Business, 5 Customer)
- 10 offers with different categories
- 13 orders with different statuses
- 13 reviews

### Test Accounts
- **Business User:** `max_business` / `asdasd`
- **Customer User:** `john_customer` / `asdasd`

## Technologies

- **Django 5.2** - Web framework
- **Django REST Framework** - API framework
- **SQLite** - Database (development)
- **django-cors-headers** - CORS support
- **django-filter** - Filtering

## Development

### Backend Development
```bash
cd coderr_backend
python manage.py makemigrations
python manage.py migrate
python manage.py shell
```

## Deployment

### Backend (Production)
- PostgreSQL instead of SQLite
- Gunicorn as WSGI server
- Nginx as reverse proxy
- Environment variables for SECRET_KEY

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is part of the Developer Academy training.

## Support

For questions or issues:
1. Create issues on GitHub
2. Check documentation in respective README files
3. Check backend logs under `coderr_backend/` 