# Events Management API

This is a Django-based API for managing events, talks, questions, and user roles. The API supports operations for event registration, talk management, user profile management, and question submission.

## Features

- User roles: `Listener`, `Speaker`, and `Organizer`
- Event program management
- Talk scheduling and management
- Question submission for talks
- Event registration for listeners
- Custom user model with extended fields (`telegram_id`, `telegram_username`, etc.)

## Prerequisites

- Python 3.8+
- Django 4.2+
- Django REST Framework (DRF)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Eugene-Bykovsky/PythonMeetupDjango
   cd PythonMeetupDjango
   ```
   
2. Create a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
   
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
   
4. Apply database migrations:
   ```
   python manage.py migrate
   ```
   
5. Create a superuser for accessing the admin panel:
   ```
   python manage.py createsuperuser
   ```
   
6. Run the development server:
   ```
   python manage.py runserver
   ```
   
## API Endpoints

### Users
GET /api/users/: List all users  
POST /api/users/: Register a new user  
GET /api/users/{id}/: Retrieve a user by ID  
PATCH /api/users/{id}/: Update a user  
DELETE /api/users/{id}/: Delete a user  

### Events  
GET /api/event-programs/: List all events  
POST /api/event-programs/: Create a new event  
GET /api/event-programs/{id}/: Retrieve an event by ID  
PATCH /api/event-programs/{id}/: Update an event  
DELETE /api/event-programs/{id}/: Delete an event  

### Talks
GET /api/talks/: List all talks  
POST /api/talks/: Create a new talk  
GET /api/talks/{id}/: Retrieve a talk by ID  
PATCH /api/talks/{id}/: Update a talk  
DELETE /api/talks/{id}/: Delete a talk  

### Questions
GET /api/questions/: List all questions  
POST /api/questions/: Submit a new question  
GET /api/questions/{id}/: Retrieve a question by ID  

###  Event Registration
POST /api/event-registrations/: Register a listener for an event
Role Check  
GET /api/check-role/check-role/: Check user roles by Telegram ID

## Models  

### CustomUser
Extended from AbstractUser with additional fields:  
telegram_id  
telegram_username  
phone_number  
roles  

### SpeakerProfile  
One-to-one relationship with CustomUser.  
Fields: biography, technical_stack.  

### OrganizerProfile  
One-to-one relationship with CustomUser.  
Fields: organization_name.  

### ListenerProfile  
One-to-one relationship with CustomUser.  
Fields: name, event.  

### Talk
Fields: title, start_time, end_time, speaker.  

### EventProgram
Fields: title, description, start_date, end_date, talks.  

### Question
Fields: text, talk, user, created_at.  

### EventRegistration
Fields: listener, event_program, registered_at.  

### Admin Panel
The admin panel is available at /admin/ for managing all models, including users, profiles, events, talks, and registrations.