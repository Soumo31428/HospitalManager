# Hospital Management System

A web-based Hospital Management System for managing patients, doctors, appointments, and medical treatments.

## Overview
This is a comprehensive Hospital Management System built as a final year university project using Flask, SQLite, Jinja2, HTML, CSS, and Bootstrap as per the project requirements.

## Features

- **Admin Dashboard**: Manage doctors, patients, and view all appointments
- **Doctor Portal**: View appointments, enter diagnoses, and track patient history
- **Patient Portal**: Book appointments, search doctors, and view treatment records

### Three User Roles

#### 1. Admin (Hospital Staff)
**Capabilities**:
- View dashboard with statistics (total doctors, patients, appointments)
- Add new doctors with specialization and credentials
- Edit existing doctor information
- Delete/remove doctors from system
- View all patient records
- Edit patient information
- Delete/remove patients
- Search doctors by name or specialization
- Search patients by name, ID, or contact information
- View all appointments (past and upcoming)

#### 2. Doctor
**Capabilities**:
- View personal dashboard with upcoming appointments (next 7 days)
- See list of assigned patients
- Mark appointments as "Completed" or "Cancelled"
- Enter diagnosis, prescriptions, and treatment notes
- View patient medical history
- Access previous treatment records

#### 3. Patient
**Capabilities**:
- Register with comprehensive profile information
- Login and manage account
- View dashboard with upcoming appointments
- Browse all available departments
- Search doctors by name or specialization
- Filter doctors by department
- Book appointments with available doctors
- View appointment booking for next 7 days
- Cancel booked appointments
- View past appointment history
- Access diagnosis and prescription records
- Update personal profile and medical history

## Installation

1. Install dependencies:
```bash
pip install flask flask-sqlalchemy flask-login werkzeug
```

2. Run the application:
```bash
python app.py
```

3. Access the system at: `http://localhost:5000`

## Default Login

**Admin Account:**
- Username: `admin`
- Password: `admin123`

## Key Features Implemented

### Appointment Management
- **Conflict Prevention**: System checks for duplicate bookings (same doctor, date, time)
- **Status Tracking**: Appointments progress through Booked → Completed → Cancelled
- **7-Day Availability**: Patients can book appointments up to 7 days in advance
- **Multiple Time Slots**: 8 time slots available per day (9 AM - 5 PM)

### Search & Filter
- **Doctor Search**: By name or specialization
- **Patient Search**: By name, ID, or contact information
- **Department Filter**: Filter doctors by medical specialization

### Security
- **Password Hashing**: Werkzeug secure password hashing
- **Session Management**: Flask-Login for user sessions
- **Role-Based Access**: Route protection based on user roles
- **CSRF Protection**: Built into Flask forms

### Treatment Records
- Complete medical history tracking
- Diagnosis documentation
- Prescription management
- Doctor notes for each visit
- Accessible to both doctors and patients

## Technology Used

- Flask
- SQLite
- Bootstrap 5
- Jinja2 Templates
- Flask-SQLAlchemy
- Flask-Login
- Werkzeug

## File Structure

```
hospital-management-system/
│
├── app.py                      # Main application (all models and routes)
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template with navigation
│   ├── index.html             # Landing page
│   ├── login.html             # Login form
│   ├── register.html          # Patient registration
│   │
│   ├── admin/                 # Admin role templates
│   │   ├── dashboard.html
│   │   ├── doctors.html
│   │   ├── add_doctor.html
│   │   ├── edit_doctor.html
│   │   ├── patients.html
│   │   ├── edit_patient.html
│   │   └── appointments.html
│   │
│   ├── doctor/                # Doctor role templates
│   │   ├── dashboard.html
│   │   ├── appointments.html
│   │   ├── complete_appointment.html
│   │   └── patient_history.html
│   │
│   └── patient/               # Patient role templates
│       ├── dashboard.html
│       ├── doctors.html
│       ├── book_appointment.html
│       ├── appointments.html
│       └── profile.html
│
├── static/                    # Static assets
│   └── css/
│       └── style.css         # Custom styles
│
├── instance/                  # Auto-generated
│   └── hospital.db           # SQLite database (created on first run)
│
├── README.md                  # Project documentation
└── replit.md                  # Technical documentation
```

## Pre-populated Data

### Default Admin Account
- Username: `admin`
- Email: `admin@hospital.com`
- Password: `admin123`
- Role: Admin

### Default Departments
1. Cardiology - Heart and cardiovascular system
2. Neurology - Brain and nervous system
3. Orthopedics - Bones, joints, and muscles
4. Pediatrics - Children healthcare
5. Dermatology - Skin conditions
6. General Medicine - General health consultation

## Testing Workflow

### As Admin:
1. Login with `admin` / `admin123`
2. Add a new doctor (choose department, set credentials)
3. View patients list
4. Search for doctors or patients
5. View all appointments

### As Doctor:
1. Login with doctor credentials (created by admin)
2. View upcoming appointments
3. Complete an appointment (enter diagnosis, prescription)
4. View patient history

### As Patient:
1. Register a new account
2. Browse available doctors
3. Book an appointment
4. View upcoming/past appointments
5. Update profile information

## Important Notes

- The database is created automatically on first application run
- No manual database setup required
- All data is stored locally in `instance/hospital.db`
- Application binds to `0.0.0.0:5000` for local access
- Debug mode is enabled for development

---
**Project Created**: November 7, 2025  
**Framework**: Flask 3.1.2  
**Database**: SQLite (SQLAlchemy ORM)  
**Frontend**: Bootstrap 5, Jinja2, HTML5, CSS3