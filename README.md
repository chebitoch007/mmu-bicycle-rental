# 🚲 MMU Bicycle Rental System

A complete Django web application for managing bicycle rentals at Multimedia University of Kenya (MMU).

## Features

- ✅ Student/Staff registration with university ID verification
- ✅ Browse available bicycles across campus stations
- ✅ 30-minute reservation system
- ✅ Real-time rental tracking with automatic cost calculation
- ✅ Email notifications for reservations and rentals
- ✅ Admin dashboard for bicycle and user management
- ✅ Penalty system for late returns
- ✅ Payment tracking (M-Pesa & PayPal ready)
- ✅ RESTful API for mobile app integration

## Tech Stack

- **Backend:** Django 5.0, Python 3.11+
- **Database:** PostgreSQL (Production) / SQLite (Development)
- **Frontend:** Bootstrap 5, HTMX
- **Email:** SMTP (configurable)
- **API:** Django REST Framework

## Installation

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd mmu_bicycle_rental
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Database Setup

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 6. Load Sample Data (Optional)

```bash
python manage.py loaddata fixtures/stations.json
python manage.py loaddata fixtures/bicycles.json
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit: `http://localhost:8000`

## Project Structure

```
mmu_bicycle_rental/
├── apps/                   # Django applications
│   ├── accounts/          # User authentication
│   ├── bicycles/          # Bicycle management
│   ├── rentals/           # Rental & reservations
│   ├── stations/          # Station management
│   ├── payments/          # Payment processing
│   └── api/               # REST API
├── config/                # Project configuration
│   └── settings/          # Environment-specific settings
├── core/                  # Shared utilities
├── templates/             # HTML templates
├── static/                # Static files (CSS, JS)
└── media/                 # User uploads
```

## Usage

### User Registration

1. Go to `/accounts/register/`
2. Fill in your MMU student/staff details
3. Upload your university ID
4. Wait for admin verification

### Renting a Bicycle

1. Browse available bicycles at `/bicycles/`
2. Click "Reserve" on your chosen bicycle
3. Pick up within 30 minutes from the station
4. Start rental when you collect the bicycle
5. Return to any station when done

### Admin Features

- Verify new users
- Add/edit bicycles
- Manage stations
- View all rentals and reservations
- Handle penalties and refunds

## Configuration

### Email Settings

Update `.env` with your SMTP details:

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Payment Integration

#### M-Pesa (Optional)
```
MPESA_CONSUMER_KEY=your-key
MPESA_CONSUMER_SECRET=your-secret
MPESA_SHORTCODE=174379
MPESA_PASSKEY=your-passkey
```

#### PayPal (Optional)
```
PAYPAL_CLIENT_ID=your-client-id
PAYPAL_CLIENT_SECRET=your-secret
PAYPAL_MODE=sandbox
```

## Testing

Run tests:

```bash
python manage.py test
```

With coverage:

```bash
coverage run --source='.' manage.py test
coverage report
```

## Deployment

### Option 1: Render

1. Create account at render.com
2. Create PostgreSQL database
3. Create Web Service
4. Set environment variables
5. Deploy from GitHub

### Option 2: Railway

```bash
railway login
railway init
railway up
```

### Option 3: VPS (Ubuntu)

```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql

# Setup project
git clone <repo>
cd mmu_bicycle_rental
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure Gunicorn & Nginx
# See deployment docs for detailed steps
```

## API Endpoints (Optional)

```
GET  /api/bicycles/          # List bicycles
GET  /api/bicycles/{id}/     # Bicycle detail
POST /api/reservations/      # Create reservation
GET  /api/rentals/           # User's rentals
POST /api/rentals/{id}/end/  # End rental
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

This project is licensed under the MIT License.

## Support

For support, email support@mmu.ac.ke or create an issue in the repository.

## Authors

- MMU Development Team

## Acknowledgments

- Multimedia University of Kenya
- Django Community
- Bootstrap Team