from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
from app import app, db, login_manager
from models import User, Doctor, Patient, Department, Appointment, Treatment

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def init_admin():
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@hospital.com',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()

def init_departments():
    departments_list = [
        {'name': 'Cardiology', 'description': 'Heart and cardiovascular system'},
        {'name': 'Neurology', 'description': 'Brain and nervous system'},
        {'name': 'Orthopedics', 'description': 'Bones, joints, and muscles'},
        {'name': 'Pediatrics', 'description': 'Children healthcare'},
        {'name': 'Dermatology', 'description': 'Skin conditions'},
        {'name': 'General Medicine', 'description': 'General health consultation'}
    ]
    
    for dept_data in departments_list:
        dept = Department.query.filter_by(name=dept_data['name']).first()
        if not dept:
            dept = Department(name=dept_data['name'], description=dept_data['description'])
            db.session.add(dept)
    
    db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        dob = request.form.get('date_of_birth')
        gender = request.form.get('gender')
        address = request.form.get('address')
        blood_group = request.form.get('blood_group')
        emergency_contact = request.form.get('emergency_contact')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role='patient'
        )
        db.session.add(user)
        db.session.flush()
        
        patient = Patient(
            user_id=user.id,
            full_name=full_name,
            phone=phone,
            date_of_birth=datetime.strptime(dob, '%Y-%m-%d').date() if dob else None,
            gender=gender,
            address=address,
            blood_group=blood_group,
            emergency_contact=emergency_contact
        )
        db.session.add(patient)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif current_user.role == 'doctor':
        return redirect(url_for('doctor_dashboard'))
    elif current_user.role == 'patient':
        return redirect(url_for('patient_dashboard'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    total_doctors = Doctor.query.count()
    total_patients = Patient.query.count()
    total_appointments = Appointment.query.count()
    
    recent_appointments = Appointment.query.order_by(Appointment.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html', 
                         total_doctors=total_doctors,
                         total_patients=total_patients,
                         total_appointments=total_appointments,
                         recent_appointments=recent_appointments)

@app.route('/admin/doctors')
@login_required
def admin_doctors():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    search_query = request.args.get('search', '')
    
    if search_query:
        doctors = Doctor.query.filter(
            (Doctor.full_name.contains(search_query)) |
            (Department.name.contains(search_query))
        ).join(Department).all()
    else:
        doctors = Doctor.query.all()
    
    return render_template('admin/doctors.html', doctors=doctors, search_query=search_query)

@app.route('/admin/doctor/add', methods=['GET', 'POST'])
@login_required
def admin_add_doctor():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        department_id = request.form.get('department_id')
        qualifications = request.form.get('qualifications')
        experience_years = request.form.get('experience_years')
        available_days = request.form.get('available_days')
        consultation_fee = request.form.get('consultation_fee')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('admin_add_doctor'))
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role='doctor'
        )
        db.session.add(user)
        db.session.flush()
        
        doctor = Doctor(
            user_id=user.id,
            full_name=full_name,
            phone=phone,
            department_id=department_id,
            qualifications=qualifications,
            experience_years=experience_years,
            available_days=available_days,
            consultation_fee=consultation_fee
        )
        db.session.add(doctor)
        db.session.commit()
        
        flash('Doctor added successfully!', 'success')
        return redirect(url_for('admin_doctors'))
    
    departments = Department.query.all()
    return render_template('admin/add_doctor.html', departments=departments)

@app.route('/admin/doctor/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_doctor(id):
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    doctor = Doctor.query.get_or_404(id)
    
    if request.method == 'POST':
        doctor.full_name = request.form.get('full_name')
        doctor.phone = request.form.get('phone')
        doctor.department_id = request.form.get('department_id')
        doctor.qualifications = request.form.get('qualifications')
        doctor.experience_years = request.form.get('experience_years')
        doctor.available_days = request.form.get('available_days')
        doctor.consultation_fee = request.form.get('consultation_fee')
        
        email = request.form.get('email')
        if email != doctor.user.email:
            if User.query.filter_by(email=email).first():
                flash('Email already in use', 'error')
                return redirect(url_for('admin_edit_doctor', id=id))
            doctor.user.email = email
        
        db.session.commit()
        flash('Doctor updated successfully!', 'success')
        return redirect(url_for('admin_doctors'))
    
    departments = Department.query.all()
    return render_template('admin/edit_doctor.html', doctor=doctor, departments=departments)

@app.route('/admin/doctor/delete/<int:id>')
@login_required
def admin_delete_doctor(id):
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    doctor = Doctor.query.get_or_404(id)
    user = doctor.user
    
    db.session.delete(doctor)
    db.session.delete(user)
    db.session.commit()
    
    flash('Doctor removed successfully!', 'success')
    return redirect(url_for('admin_doctors'))

@app.route('/admin/patients')
@login_required
def admin_patients():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    search_query = request.args.get('search', '')
    
    if search_query:
        patients = Patient.query.filter(
            (Patient.full_name.contains(search_query)) |
            (Patient.phone.contains(search_query)) |
            (Patient.id == int(search_query) if search_query.isdigit() else False)
        ).all()
    else:
        patients = Patient.query.all()
    
    return render_template('admin/patients.html', patients=patients, search_query=search_query)

@app.route('/admin/patient/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_patient(id):
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    patient = Patient.query.get_or_404(id)
    
    if request.method == 'POST':
        patient.full_name = request.form.get('full_name')
        patient.phone = request.form.get('phone')
        patient.gender = request.form.get('gender')
        patient.address = request.form.get('address')
        patient.blood_group = request.form.get('blood_group')
        patient.emergency_contact = request.form.get('emergency_contact')
        
        dob = request.form.get('date_of_birth')
        if dob:
            patient.date_of_birth = datetime.strptime(dob, '%Y-%m-%d').date()
        
        db.session.commit()
        flash('Patient updated successfully!', 'success')
        return redirect(url_for('admin_patients'))
    
    return render_template('admin/edit_patient.html', patient=patient)

@app.route('/admin/patient/delete/<int:id>')
@login_required
def admin_delete_patient(id):
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    patient = Patient.query.get_or_404(id)
    user = patient.user
    
    db.session.delete(patient)
    db.session.delete(user)
    db.session.commit()
    
    flash('Patient removed successfully!', 'success')
    return redirect(url_for('admin_patients'))

@app.route('/admin/appointments')
@login_required
def admin_appointments():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    appointments = Appointment.query.order_by(Appointment.appointment_date.desc()).all()
    return render_template('admin/appointments.html', appointments=appointments)

@app.route('/doctor/dashboard')
@login_required
def doctor_dashboard():
    if current_user.role != 'doctor':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    
    today = date.today()
    next_week = today + timedelta(days=7)
    
    upcoming_appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.appointment_date >= today,
        Appointment.appointment_date <= next_week,
        Appointment.status == 'Booked'
    ).order_by(Appointment.appointment_date, Appointment.appointment_time).all()
    
    patients_list = Patient.query.join(Appointment).filter(
        Appointment.doctor_id == doctor.id
    ).distinct().all()
    
    return render_template('doctor/dashboard.html', 
                         doctor=doctor,
                         upcoming_appointments=upcoming_appointments,
                         patients=patients_list)

@app.route('/doctor/appointments')
@login_required
def doctor_appointments():
    if current_user.role != 'doctor':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).order_by(
        Appointment.appointment_date.desc()
    ).all()
    
    return render_template('doctor/appointments.html', appointments=appointments)

@app.route('/doctor/appointment/<int:id>/complete', methods=['GET', 'POST'])
@login_required
def doctor_complete_appointment(id):
    if current_user.role != 'doctor':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    appointment = Appointment.query.get_or_404(id)
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    
    if appointment.doctor_id != doctor.id:
        flash('Access denied', 'error')
        return redirect(url_for('doctor_dashboard'))
    
    if request.method == 'POST':
        diagnosis = request.form.get('diagnosis')
        prescription = request.form.get('prescription')
        notes = request.form.get('notes')
        
        appointment.status = 'Completed'
        
        treatment = Treatment(
            appointment_id=appointment.id,
            diagnosis=diagnosis,
            prescription=prescription,
            notes=notes
        )
        db.session.add(treatment)
        db.session.commit()
        
        flash('Appointment completed successfully!', 'success')
        return redirect(url_for('doctor_appointments'))
    
    return render_template('doctor/complete_appointment.html', appointment=appointment)

@app.route('/doctor/appointment/<int:id>/cancel')
@login_required
def doctor_cancel_appointment(id):
    if current_user.role != 'doctor':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    appointment = Appointment.query.get_or_404(id)
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    
    if appointment.doctor_id != doctor.id:
        flash('Access denied', 'error')
        return redirect(url_for('doctor_dashboard'))
    
    appointment.status = 'Cancelled'
    db.session.commit()
    
    flash('Appointment cancelled', 'success')
    return redirect(url_for('doctor_appointments'))

@app.route('/doctor/patient/<int:id>/history')
@login_required
def doctor_patient_history(id):
    if current_user.role != 'doctor':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    patient = Patient.query.get_or_404(id)
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    
    appointments = Appointment.query.filter_by(
        patient_id=patient.id,
        doctor_id=doctor.id,
        status='Completed'
    ).order_by(Appointment.appointment_date.desc()).all()
    
    return render_template('doctor/patient_history.html', patient=patient, appointments=appointments)

@app.route('/patient/dashboard')
@login_required
def patient_dashboard():
    if current_user.role != 'patient':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    departments = Department.query.all()
    
    today = date.today()
    upcoming_appointments = Appointment.query.filter(
        Appointment.patient_id == patient.id,
        Appointment.appointment_date >= today,
        Appointment.status == 'Booked'
    ).order_by(Appointment.appointment_date, Appointment.appointment_time).all()
    
    return render_template('patient/dashboard.html', 
                         patient=patient,
                         departments=departments,
                         upcoming_appointments=upcoming_appointments)

@app.route('/patient/doctors')
@login_required
def patient_doctors():
    if current_user.role != 'patient':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    search_query = request.args.get('search', '')
    department_id = request.args.get('department', '')
    
    query = Doctor.query
    
    if search_query:
        query = query.filter(
            (Doctor.full_name.contains(search_query)) |
            (Department.name.contains(search_query))
        ).join(Department)
    
    if department_id:
        query = query.filter_by(department_id=department_id)
    
    doctors = query.all()
    departments = Department.query.all()
    
    return render_template('patient/doctors.html', 
                         doctors=doctors, 
                         departments=departments,
                         search_query=search_query,
                         selected_department=department_id)

@app.route('/patient/book/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
def patient_book_appointment(doctor_id):
    if current_user.role != 'patient':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    doctor = Doctor.query.get_or_404(doctor_id)
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        appointment_date = request.form.get('appointment_date')
        appointment_time = request.form.get('appointment_time')
        symptoms = request.form.get('symptoms')
        
        appt_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
        
        existing = Appointment.query.filter_by(
            doctor_id=doctor.id,
            appointment_date=appt_date,
            appointment_time=appointment_time
        ).filter(Appointment.status != 'Cancelled').first()
        
        if existing:
            flash('This time slot is already booked. Please choose another time.', 'error')
            return redirect(url_for('patient_book_appointment', doctor_id=doctor_id))
        
        appointment = Appointment(
            patient_id=patient.id,
            doctor_id=doctor.id,
            appointment_date=appt_date,
            appointment_time=appointment_time,
            symptoms=symptoms,
            status='Booked'
        )
        db.session.add(appointment)
        db.session.commit()
        
        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('patient_appointments'))
    
    today = date.today()
    available_dates = [today + timedelta(days=i) for i in range(1, 8)]
    
    return render_template('patient/book_appointment.html', 
                         doctor=doctor, 
                         available_dates=available_dates)

@app.route('/patient/appointments')
@login_required
def patient_appointments():
    if current_user.role != 'patient':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    
    upcoming = Appointment.query.filter(
        Appointment.patient_id == patient.id,
        Appointment.appointment_date >= date.today()
    ).order_by(Appointment.appointment_date, Appointment.appointment_time).all()
    
    past = Appointment.query.filter(
        Appointment.patient_id == patient.id,
        Appointment.appointment_date < date.today()
    ).order_by(Appointment.appointment_date.desc()).all()
    
    return render_template('patient/appointments.html', 
                         upcoming_appointments=upcoming,
                         past_appointments=past)

@app.route('/patient/appointment/<int:id>/cancel')
@login_required
def patient_cancel_appointment(id):
    if current_user.role != 'patient':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    appointment = Appointment.query.get_or_404(id)
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    
    if appointment.patient_id != patient.id:
        flash('Access denied', 'error')
        return redirect(url_for('patient_dashboard'))
    
    appointment.status = 'Cancelled'
    db.session.commit()
    
    flash('Appointment cancelled successfully', 'success')
    return redirect(url_for('patient_appointments'))

@app.route('/patient/profile', methods=['GET', 'POST'])
@login_required
def patient_profile():
    if current_user.role != 'patient':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    patient = Patient.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        patient.full_name = request.form.get('full_name')
        patient.phone = request.form.get('phone')
        patient.gender = request.form.get('gender')
        patient.address = request.form.get('address')
        patient.blood_group = request.form.get('blood_group')
        patient.emergency_contact = request.form.get('emergency_contact')
        patient.medical_history = request.form.get('medical_history')
        
        dob = request.form.get('date_of_birth')
        if dob:
            patient.date_of_birth = datetime.strptime(dob, '%Y-%m-%d').date()
        
        email = request.form.get('email')
        if email != current_user.email:
            if User.query.filter_by(email=email).first():
                flash('Email already in use', 'error')
                return redirect(url_for('patient_profile'))
            current_user.email = email
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('patient_profile'))
    
    return render_template('patient/profile.html', patient=patient)
