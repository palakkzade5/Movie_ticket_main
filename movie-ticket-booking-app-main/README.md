# movie-ticket-app
# movie-ticket-booking-app
# Ticket Booking Management System

## Project Overview
This is a Django-based Ticket Booking Management System that allows users to register, login, view available shows, book tickets with seat selection, and view their booking history. The system also includes an admin panel for managing movies, shows, and bookings.

## Features
- User Registration, Login, and Logout (manual data handling, no Django Forms)
- View available shows/events with pagination
- Book tickets with seat selection and confirmation
- Booking history page with pagination
- Admin panel to add, edit, delete movies and shows
- Admin view of all bookings
- Email notifications for booking confirmation
- Responsive UI using Bootstrap
- Docker and Docker Compose for environment setup
- Jenkins CI/CD pipeline for automated build, test, and deploy

## Tech Stack
- Python 3.x
- Django 4.x
- PostgreSQL (or your preferred database)
- Bootstrap 5 for frontend styling
- Docker & Docker Compose
- Jenkins for CI/CD

## Setup & Run Instructions

### Prerequisites
- Docker and Docker Compose installed
- Jenkins installed (for CI/CD)

### Running the Application
1. Clone the repository:
   ```
   git clone <repository-url>
   cd ticket-booking-management-system
   ```

2. Build and start the Docker containers:
   ```
   docker-compose up --build
   ```

3. Apply migrations and create superuser:
   ```
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   ```

4. Access the application:
   - User interface: `http://localhost:8000/`
   - Admin panel: `http://localhost:8000/admin/`

### Running the Management Command to Create Seats
If you add shows manually, run the following command to create seat objects:
```
docker-compose exec web python manage.py create_seats
```

## Docker Usage
- The Dockerfile sets up the Django application environment.
- docker-compose.yml configures the web and database services.
- Use `docker-compose up` to start the application.

## Jenkins Usage
- Jenkinsfile defines the CI/CD pipeline for automated build, test, and deployment.
- Configure Jenkins to use this Jenkinsfile for the project.

## Screenshots


![image](https://github.com/user-attachments/assets/56920501-1196-40be-9f72-18e75605941a)
![image](https://github.com/user-attachments/assets/32fbdb39-3a6c-45de-88b1-298b62d72be0)
![image](https://github.com/user-attachments/assets/6c6d0b15-ade2-4bb4-b77d-fb45e60ce310)
![image](https://github.com/user-attachments/assets/a4b170c3-91bc-4cd3-80c0-dcf69468d9f6)
## Notes
- Seat selection requires JavaScript enabled in the browser.
- Booking confirmation emails are sent upon successful booking.
- Admin panel requires staff user login.
