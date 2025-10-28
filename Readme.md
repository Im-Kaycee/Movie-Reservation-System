# mBox - Movie Reservation Platform

A full-featured movie ticket reservation system built with Django REST Framework, featuring real-time seat availability, payment processing, and automated reservation management.

## 🚀 Features

### Core Functionality

- **User Authentication & Authorization** - JWT-based secure authentication
- **Movie Management** - Browse movies with genres, descriptions, and showtimes
- **Showtime Scheduling** - Flexible showtime management with conflict prevention
- **Seat Reservation** - Real-time seat availability checking and booking
- **Payment Processing** - Mock payment integration with expiry handling
- **Reservation Management** - View, cancel, and track reservation status
- **Auditorium Management** - Multiple screens with customizable seating

### Advanced Features

- **Automated Expiry** - Unpaid reservations automatically expire after 10 minutes
- **Real-time Availability** - Live seat availability with conflict prevention
- **Cancellation Policy** - Smart cancellation with time-based restrictions
- **Admin Dashboard** - Jazzmin-powered admin interface
- **API Documentation** - Auto-generated Swagger/Redoc documentation

## 🛠 Tech Stack

### Backend

- **Django** - Web framework
- **Django REST Framework** - API development
- **Simple JWT** - Authentication
- **Celery** - Background tasks
- **Redis** - Message broker & result backend
- **SQLite** - Database (development)

### Frontend & API

- **RESTful API** - Full CRUD operations
- **Swagger/Redoc** - API documentation
- **CORS** - Cross-origin resource sharing

## 🗄 Database Models

### Core Models

- **User** - Extended Django user model
- **Movie** - Movie details with genres
- **Genre** - Movie categories
- **Auditorium** - Theater screens with capacity
- **Seat** - Individual seats per auditorium
- **Showtime** - Movie screening schedules

### Reservation System

- **Reservation** - Booking records with status tracking
- **ReservedSeat** - Seat assignments for reservations

## 🔑 API Endpoints

### Authentication

- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - JWT token obtain
- `POST /api/auth/token/refresh/` - Token refresh

### Movies

- `GET /api/movies/{id}/` - Movie details
- `GET /api/movies/showtimes/` - Showtime listings

### Showtimes

- `GET /api/showtimes/` - List all showtimes (with filters)
- `GET /api/showtimes/{showtime_id}/available-seats/` - Available seats

### Reservations

- `POST /api/reservations/create/` - Create reservation
- `GET /api/reservations/` - User's active reservations
- `GET /api/reservations/cancelled/` - User's cancelled reservations
- `GET /api/reservations/{id}/` - Reservation details
- `PUT /api/reservations/{id}/cancel/` - Cancel reservation
- `PUT /api/reservations/{id}/mock-payment/` - Process payment

### Auditoriums

- `GET /api/showtimes/auditoriums/` - List auditoriums
- `GET /api/showtimes/auditoriums/{id}/` - Auditorium details

## 🚦 Installation & Setup

### Prerequisites

- Python 3.8+
- Redis server
- Virtual environment

### Installation Steps

1. **Clone the repository**

```bash
git clone <repository-url>
cd mApp
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Database setup**

```bash
python manage.py migrate
python manage.py createsuperuser
```

5. **Start Redis (required for Celery)**

```bash
redis-server
```

6. **Run development server**

```bash
python manage.py runserver
```

7. **Start Celery worker and beat**

```bash
celery -A mApp worker --beat -l info
```

## 🔧 Configuration

### Environment Setup

Update `mApp/settings.py` for production:

- Set `DEBUG = False`
- Configure production database
- Set `ALLOWED_HOSTS`
- Update security keys

### Celery Configuration

Tasks run every 5 minutes to:

- Expire unpaid reservations automatically
- Clean up expired reservation data

## 🎯 Usage Examples

### Creating a Reservation

1. Authenticate to get JWT token
2. Browse showtimes: `GET /api/showtimes/?movie=1&date=2024-01-15`
3. Check available seats: `GET /api/showtimes/1/available-seats/`
4. Create reservation:

```json
POST /api/reservations/create/
{
    "showtime_id": 1,
    "seats": [1, 2, 3]
}
```

5. Process payment: `PUT /api/reservations/1/mock-payment/`

### Filtering Showtimes

- By movie: `?movie=1`
- By date: `?date=2024-01-15`
- By date range: `?from=2024-01-15&to=2024-01-20`

## 🔒 Reservation Status Flow

```
pending_payment → paid → cancelled
       ↓
    expired (auto)
```

- **pending_payment**: 10-minute payment window
- **paid**: Confirmed reservation
- **cancelled**: User-cancelled (if >1 hour before showtime)
- **expired**: Auto-cancelled after payment window

## 🐛 Troubleshooting

### Common Issues

- Celery not running: Reservations won't expire automatically
- Redis connection failed: Celery tasks won't execute
- CORS errors: Check `CORS_ALLOW_ALL_ORIGINS` in development

### Debug Tips

- Check Celery worker logs for task execution
- Verify Redis server is running
- Use Django admin for data inspection

## 👥 Admin Access

Access the admin dashboard at `/admin/` with superuser credentials. Features:

- Manage all models
- View reservation analytics
- Monitor system status

## 📝 API Documentation

Interactive API documentation available at:

- Swagger UI: `/api/docs/`
- ReDoc: `/api/schema/redoc/`
