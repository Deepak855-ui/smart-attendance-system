from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import pymysql
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import random

from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart



###################### LETS STATRS FOR POSTGRESQL ###########################
app = Flask(__name__)
app.secret_key="name"
app.config['SESSION_TYPE'] = 'filesystem'  # Store session data in a file
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register')
def register():
   return render_template('register_dashboard.html')

@app.route('/teacher_registration')
def teacher_registration():
    return render_template('teacher_registration.html')

@app.route('/student_registration')
def student_registration():
    return render_template('student_registration.html')


# ✅ **Database Configuration**
db = pymysql.connect(
                     host="localhost", 
                     user="root", 
                     password="28oct2004", 
                     database="attendance_system",
                     )
cursor = db.cursor()

# ✅ **Upload Folder for Profile Pictures**
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ✅ Register success 
@app.route('/success_registered')
def success_registered():
    return render_template('success_registered.html')


# teacer registration process with smpt email configuration
def send_otp_teacher(email):
    otp = str(random.randint(100000, 999999))
    expiry_time = (datetime.now() + timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
    session['teacher_otp'] = otp
    session['teacher_otp_expiry'] = expiry_time
    session['teacher_otp_email'] = email
    
    print(f"✅ Debug: Stored OTP -> {session.get('teacher_otp')}, Email -> {session.get('teacher_otp_email')}")  # Debugging

    subject = "Your OTP for Teacher Registration"
    body = f"""
     HELLO, {email}
            
     <div style="font-family: Arial, sans-serif; background-color: #000; padding: 40px; text-align: center;">
        <div style="background-color: #1e1e1e; padding: 20px; border-radius: 8px;">
         <h1 style="color: #ff9900; font-size: 15px; font-family:serif">SHAHEED BHAGAT SINGH STATE UNIVERSITY</h1>
            <p style="color: #fff; font-size: 18px;">Verification code</p>
            <h2 style="color: #fff; font-size: 48px; margin: 20px 0;">{otp}</h2>
            <p style="color: #888; font-size: 14px;">(This code will expire 5 minutes after it was sent.)</p>
            <hr style="border-color: #333; margin: 20px 0;">
            
            <hr style="border-color: #333; margin: 20px 0;">
            <p style="color: #fff; font-size: 12px;">This is a verification code email. Please do not share your code with anyone.</p>
            <p style="color: #fff; font-size: 12px;"> For any assistance, feel free to reach out to our suppurt team. </p>
        </div>
        </div>
    </div>
     
    <br>   
    <p>Thank You,</p>
    <p style="display:inline-block;  background: linear-gradient(90deg,  #002855, #00509E, #87CEFA, #78b1c0); color:red">**Deepak**</p>
    <p>Supoort Team</p>

    <hr style="border-color: #333; margin: 20px 0;">
    <body style="text-align:center">

<p style="color: #888; font-size: 12px; text-align: center;">
    This email was sent by <strong>Shaheed Bhagat Singh State University</strong> for verification purposes. 
    If you didn't request this verification, please ignore this email.
</p>
<p style="color: #ccc; font-size: 12px; text-align: center;">
    Need help? Contact our support team at 
    <a href="mailto:support@sbssu.ac.in" style="color: #00bcd4; text-decoration: none;">support@sbssu.ac.in</a>
</p>
<p style="color: #777; font-size: 12px; text-align: center;">
    Powered by the <strong>Smart Attendance System</strong> – Enhancing attendance management with technology.
</p>

    <hr style="border-color: #333; margin: 20px 40px;">
    
    <p style="color:grey; font-size:8px" >From</p>
    <p style="color:grey; font-size:12px; text-decoration:underline; font-family:fantasy;">Deepak</p>
    <p style="color:grey; font-size:10px ;text-decoration:underline;">imdeep2810@gmail.com</p>
    </body>
 
    """
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    
    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, email, msg.as_string())
        server.quit()
        print(f"✅ OTP Generated: {otp}, Expires at: {session['teacher_otp_expiry']}")  # Debugging
        print(f"✅ OTP Sent Successfully to {email}")
        return True
    except Exception as e:
        print("❌ Email Sending Error:", str(e)) 
        print("Email Error:", e)
        return False

# API to send OTP
@app.route('/send_otp_teacher', methods=['POST'])
def send_otp_teacher_route():
    data = request.get_json()
    email = data.get('email')
    if send_otp_teacher(email):
        return jsonify({"message": "OTP sent successfully!"}), 200
    return jsonify({"error": "Failed to send OTP."}), 500

@app.route('/verify_otp_teacher', methods=['POST'])
def verify_otp_teacher():
    data = request.get_json()
    entered_otp = data.get('otp')
    if 'teacher_otp' in session and session['teacher_otp'] == entered_otp:
        return jsonify({"verified": True})
    return jsonify({"verified": False})

@app.route('/register_teacher', methods=['GET','POST'])
def register_teacher():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    department = request.form['department']
    subjects = request.form['subjects']
    experience = request.form['experience']
    password = request.form['password']
    entered_otp = request.form['otp']
    
    if 'teacher_otp' not in session or session['teacher_otp_email'] != email or session['teacher_otp'] != entered_otp:
        flash("Invalid OTP! Please try again.", "danger")
        return redirect(url_for('teacher_registration'))
    
    hashed_password = generate_password_hash(password)
    file = request.files['profile_picture']
    filename = secure_filename(file.filename) if file.filename else 'default.png'
    if file.filename:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
    
    sql = "INSERT INTO teachers (name, email, phone, department, subjects, experience, profile_pic, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (name, email, phone, department, subjects, experience, filename, hashed_password))
    db.commit()
    session.pop('teacher_otp', None)
    session.pop('teacher_otp_email', None)
    flash("Teacher Registered Successfully!", "success")
    return redirect(url_for('success_registered'))








# # ✅ **Route: Teacher Registration Page**
# @app.route('/register_teacher', methods=['GET', 'POST'])
# def register_teacher():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         phone = request.form['phone']
#         department = request.form['department']
#         subjects = request.form['subjects']
#         experience = request.form['experience']
#         password = request.form['password']
#         hashed_password = generate_password_hash(password)



#         # otp = request.form['otp']

#         # ✅ **Handle Profile Picture Upload**
#         file = request.files['profile_picture']
#         if file and file.filename != '':
#                 filename = secure_filename(file.filename)
#                 file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename) #SAVE CORRECTLY
#                 file.save(file_path)
#         else:
#                 filename='default.png'
#                 # file_path = ""

#          # ✅ **Insert Data into Database**
#         sql = "INSERT INTO teachers (name, email, phone, department, subjects, experience, profile_pic, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
#         cursor.execute(sql, (name, email, phone, department, subjects, experience, filename, hashed_password )) #STORE ONLY FILENAME 
#         # cursor.execute(sql, (name, email, phone, department, subjects, experience, file_path,hashed_password))
#         db.commit()

#         flash("Teacher Registered Successfully!", "success")
#         # return redirect(url_for('register_teacher'))
#         return redirect(url_for('success_registered'))
#         # else:
#         #     flash("Invalid OTP! Please try again.", "danger")

#     # return render_template('success.html')
#     flash("Teacher Registered Successfully!", "success")
#     return  redirect(url_for('success_registered'))


# SMTP Email Configuration
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_ADDRESS = "222021@sbsstc.ac.in"
EMAIL_PASSWORD = "ftjf pcvv zyem ndhs"


# EMAIL_ADDRESS = "pablomaxico262@gmail.com"  # Change to your email
# EMAIL_PASSWORD = "dynb qelf iirs kwlf"  # Change to your app password

def generate_otp():
    return str(random.randint(100000, 999999))  # Generate a 6-digit OTP

# Function to send OTP via email
def send_otp(email):




    
    otp = generate_otp()
    expiry_time = datetime.now() + timedelta(minutes=5)  # OTP expires in 5 minutes
    session['otp'] = otp # Store OTP in session
    session['otp_expiry'] = expiry_time.strftime("%Y-%m-%d %H:%M:%S")  # Store as string (Fixed!)
    session['otp_email'] = email  # ✅ Store the email in session (Fix!)
   
   
    print(f"✅ Debug: Stored OTP -> {session['otp']}, Email -> {session['otp_email']}")  # Debugging
    print(f"Generated OTP: {otp}, Expires at: {expiry_time}")

    

    subject = "Your OTP for Student Registration"

    body = f"""
    HELLO, {email}
            
     <div style="font-family: Arial, sans-serif; background-color: #000; padding: 40px; text-align: center;">
        <div style="background-color: #1e1e1e; padding: 20px; border-radius: 8px;">
         <h1 style="color: #ff9900; font-size: 15px; font-family:serif">SHAHEED BHAGAT SINGH STATE UNIVERSITY </h1>
            <p style="color: #fff; font-size: 18px;">Verification code</p>
            <h2 style="color: #fff; font-size: 48px; margin: 20px 0;">{otp}</h2>
            <p style="color: #888; font-size: 14px;">(This code will expire 5 minutes after it was sent.)</p>
            <hr style="border-color: #333; margin: 20px 0;">
            
            <hr style="border-color: #333; margin: 20px 0;">
            <p style="color: #fff; font-size: 12px;">This is a verification code email. Please do not share your code with anyone.</p>
            <p style="color: #fff; font-size: 12px;"> For any assistance, feel free to reach out to our suppurt team. </p>
        </div>
        </div>
    </div>
     
    <br>   
    <p>Thank You,</p>
    <p style="display:inline-block;  background: linear-gradient(90deg,  #002855, #00509E, #87CEFA, #78b1c0); color:red">**Deepak**</p>
    <p>Supoort Team</p>

    <hr style="border-color: #333; margin: 20px 0;">
    <body style="text-align:center">

<p style="color: #888; font-size: 12px; text-align: center;">
    This email was sent by <strong>Shaheed Bhagat Singh State University</strong> for verification purposes. 
    If you didn't request this verification, please ignore this email.
</p>
<p style="color: #ccc; font-size: 12px; text-align: center;">
    Need help? Contact our support team at 
    <a href="mailto:support@sbssu.ac.in" style="color: #00bcd4; text-decoration: none;">support@sbssu.ac.in</a>
</p>
<p style="color: #777; font-size: 12px; text-align: center;">
    Powered by the <strong>Smart Attendance System</strong> – Enhancing attendance management with technology.
</p>

    <hr style="border-color: #333; margin: 20px 40px;">

    <p style="color:grey; font-size:8px" >From</p>
    <p style="color:grey; font-size:12px; text-decoration:underline; font-family:fantasy;">Deepak</p>
    <p style="color:grey; font-size:10px ;text-decoration:underline;">imdeep2810@gmail.com</p>
    </body>
 
       """
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    
    
    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, email, msg.as_string())
        server.quit()
        print(f"✅ OTP Generated: {otp}, Expires at: {session['otp_expiry']}")  # Debugging
        print(f"✅ OTP Sent Successfully to {email}")
        return True
    except Exception as e:
        print("❌ Email Sending Error:", str(e)) 
        print("Email Error:", e)
        return False
    
# API to send OTP
@app.route('/send_otp', methods=['POST'])
def request_otp():
    data = request.json
    email = data.get("email")
    
    if email:
        otp = generate_otp()
        expiry_time = datetime.now() + timedelta(minutes=5)

        # ✅ Store OTP & email in session correctly
        session['otp'] = otp
        session['otp_expiry'] = expiry_time.strftime("%Y-%m-%d %H:%M:%S")
        session['otp_email'] = email  

        print(f"✅ Debug: Stored OTP -> {session.get('otp')}, Email -> {session.get('otp_email')}")  # Debugging

        if send_otp(email):  # Ensure email is sent successfully
            return jsonify({"message": "OTP sent successfully!"}), 200

    return jsonify({"error": "Failed to send OTP."}), 500


@app.route("/verify_otp", methods=["POST"])
def verify_otp():
    data = request.get_json()
    entered_otp = data.get("otp")

    print(f"🔍 Debug: User Entered OTP -> {entered_otp}")  # Debugging

    if "otp" not in session:
        return jsonify({"verified": False, "error": "OTP expired or not generated"}), 400

    stored_otp = session.get("otp")
    expiry_time_str = session.get("otp_expiry")

    if not stored_otp or not expiry_time_str:
        return jsonify({"verified": False, "error": "OTP expired or not generated"}), 400
    
    expiry_time = datetime.strptime(expiry_time_str, "%Y-%m-%d %H:%M:%S")
   
    if datetime.now() > expiry_time:
        session.pop("otp", None)  # Remove expired OTP
        session.pop("otp_expiry", None)
        return jsonify({"verified": False, "error": "OTP expired!"}), 400

    if str(entered_otp)== str(stored_otp):
        session['otp_verified'] = True  # Mark OTP as verified
        return jsonify({"verified": True})

    return jsonify({"verified": False, "error": "Invalid OTP"}), 400

# ✅ **Route: Student Registration Page**
@app.route('/register_student', methods=['GET', 'POST'])
def register_student():
    print(f"🔍 Debug: Full Session Data Before Registration -> {session}")  # Debugging
    if 'otp' not in session:
        print("❌ Debug: Session OTP Missing!")
    if request.method == 'POST':
        name = request.form['name']
        rollno = request.form['rollno']
        phone = request.form['phone']
        department = request.form['department']
        sem = request.form['sem']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        entered_otp = request.form['otp']

          # ✅ Debugging: Print form data
        print(f"🔍 Debug: Received Data -> Name: {name}, Email: {email}, OTP: {entered_otp}")

           # Validate OTP
           # ✅ Fix OTP Validation
        stored_otp = session.get('otp')
        stored_email = session.get('otp_email')
        otp_verified = session.get('otp_verified', False)

        print(f"🔍 Debug: Stored OTP -> {stored_otp}, Stored Email -> {stored_email}")  # Debugging
       
       # ✅ Ensure OTP is stored and matches correctly
        if not otp_verified or stored_email != email or str(stored_otp) != str(entered_otp):
           flash("❌ Invalid OTP! Please try again.", "danger")
           return redirect(url_for('student_registration'))
        

        # if 'otp' not in session or session.get('otp_email') != email or str(session['otp']) != entered_otp:
        #     flash("Invalid OTP! Please try again.", "danger")
        #     return redirect(url_for('student_registration'))

         # ✅ **Insert Data into Database**
        
           # ✅ Insert Data into Database

         # ✅ **Handle Profile Picture Upload**
        file = request.files['profile_picture']
        if file and file.filename != '':
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename) # SAVE CORRECTLY
                file.save(file_path)
        else:
                filename='default.png'
                # file_path = ""

        try:
            sql = "INSERT INTO login_students (name, roll_no, phone, department, sem, email, profile_pic, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (name, rollno, phone, department, sem, email, filename, hashed_password )) #STORE ONLY FILENAME 
            # cursor.execute(sql, (name, rollno, phone, department, sem, email, file_path, hashed_password ))
            db.commit()
            flash("Student Registered Successfully!", "success")

               # Clear OTP from session after successful registration
            session.pop('otp', None)
            session.pop('otp_expiry', None)
            session.pop('otp_email', None)
            session.pop('otp_verified', None)

            return redirect(url_for('success_registered'))
        except Exception as e:
            print("❌ Database Error:", str(e))
            flash("❌ Registration Failed! Please try again.", "danger")
            return redirect(url_for('student_registration'))
    return render_template('student_registration.html')
    # else:
    #     flash("Invalid OTP! Please try again.", "danger")

    # # return render_template('success.html')
    # flash("Student Registered Successfully!", "success")
    # return  redirect(url_for('success_registered'))

# lOGIN ACCOUNt SECTION both 

@app.route('/login_section')
def login_section():
   return render_template('login_dashboard.html')

#------------- Teacher Login section ----------------
# @app.route('/teacher_login')
# def teacher_login():
#     return render_template('teacher_login.html')


@app.route('/teacher_login', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']

        cursor = db.cursor()
        cursor.execute("SELECT * FROM teachers WHERE phone = %s", [phone])
        teacher = cursor.fetchone()
        cursor.close()

        if teacher:
            stored_hashed_password = teacher[8]  # Assuming password is in the 9 column (index 8)

            # Verify entered password with stored hashed password
            if check_password_hash(stored_hashed_password, password):
                session['phone'] = teacher[3]  # Store session
                session['teacher_name'] = teacher[1]  # Assuming name is in the 2nd column (index 1)
                session['teacher_profile_pic'] = teacher[7] if teacher[7] else "default.png" # Assuming profile picture is in the 8th column (index 7)
                session['teacher_id']=teacher[0] # Assuming id is in the 1st column[index 0]
                session['teacher_email'] = teacher[2]  # Assuming email is in the 6th column (index 5)

                flash("Login successful!", "success")
                print("Debug: Teacher Profile Pic ->", session.get('teacher_profile_pic'))

                return redirect(url_for('teacher_dashboard'))
            else:
                flash("Invalid password!", "danger")
        else:
            flash("phone number not found!", "danger")

    return render_template('teacher_login.html')


# Route: Teacher Forgot Password Page


# Route: Teacher Verify OTP Page


# <---------- Teacher dashboard -----------> 
@app.route('/teacher_dashboard')
def teacher_dashboard():
    # if 'teacher_name' not in session:
    if 'phone' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('teacher_login'))
   
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current time
    print("Current Time:", current_time)  # Debugging
    # print("Debug: Teacher Name in Session ->", session.get('teacher_name'))
    print("Debug: Teacher phone in Session ->", session.get('phone'))
    

    cursor = db.cursor()
    # cursor.execute("SELECT profile_pic FROM teachers WHERE  name = %s", (session['teacher_name'],))
    cursor.execute("SELECT profile_pic FROM teachers WHERE  phone = %s", (session['phone'],))
    profile_pic = cursor.fetchone()

    if profile_pic and profile_pic[0]:  
        session['teacher_profile_pic'] = profile_pic[0]
    else:
        session['teacher_profile_pic'] = "default.png"  # Use default if missing


    print("Debug: session['teacher_profile_pic'] ->", session.get('teacher_profile_pic'))  # Debugging output
    
    return render_template('teacher_dashboard.html',
        current_code=session.get('generated_code'),
        expires_at=session.get('expiry_time'),
        code_subject=session.get('code_subject'))



# @app.route('/teacher_dashboard')
# def teacher_dashboard():
#     if 'phone' not in session:
#         flash("Please log in first.", "warning")
#         return redirect(url_for('teacher_login'))

#     phone = session['phone']
#     current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current time

#     return render_template('teacher_dashboard.html',template_folder='templates' ,phone = phone, current_time=current_time)


generated_codes = {} # Store codes in memory 
# Route for Generating Code Page
@app.route('/generate-code')
def generate_code_page():
    time = request.args.get('time')
    subject = request.args.get('subject')
    teacher = request.args.get('teacher')
    
    return render_template('generate_code.html', time=time, subject=subject, teacher_name=teacher, datetime=datetime.now().strftime("%Y-%m-%d %H:%M"))


# Generate Attendance Code API
@app.route('/generate_code', methods=['POST'])
def generate_attendance_code():
    global generated_codes  # Ensure access to the global dictionary

    print("recieved form data:", request.form)# Debugging

    teacher = request.form.get('teacher_name') or request.json.get('teacher_name')
    subject = request.form.get('subject') or request.json.get('subject')
    time = request.form.get('datetime')or request.json.get('datetime')

    if not teacher or not subject or not time:
        print("❌ Error: Missing Data!")  # Debugging
        return jsonify({'error': 'Missing details'}), 400
    
    # Check if a valid code already exists for the subject
    if subject in generated_codes:
        existing_code_info = generated_codes[subject]
        if datetime.now().timestamp() < existing_code_info['expires_at']:
            # Return the existing code if it is still valid
            return jsonify({
                'generated_code': existing_code_info['code'],
                'expires_at': existing_code_info['expires_at']
            })


    # Generate a new code if no valid code exists
    code = random.randint(100000, 999999)  # Generate 6-digit code
    expiry_time = datetime.now() + timedelta(minutes=1)  # Code valid for 10 min
    expiry_timestamp = expiry_time.timestamp()  # Convert to timestamp for JavaScript countdown

     # ✅ Store code in Flask session
    session['generated_code'] = code
    session['expiry_time'] = expiry_timestamp
    session['code_subject'] = subject

    generated_codes[subject] = {"code": code, "expires_at": expiry_timestamp} # store code in dictionary
    
    print("Generated Codes:", generated_codes)  # DEBUGGING: Check stored codes

    return jsonify({'generated_code': code , 'expires_at': expiry_timestamp})
    
    # return jsonify({'generated_code': code , 'expires_at': expiry_time.strftime("%Y-%m-%d %H:%M:%S")})

# Timestamp for timeout generated code 
@app.route('/get_code_expiry')
def get_code_expiry():
    subject = request.args.get('subject')

    if subject in generated_codes:
        expiry_timestamp = generated_codes[subject]['expires_at']
        return jsonify({'expires_at': expiry_timestamp})

    return jsonify({'error': 'No active code'}), 404
   
#------------- Studees[subject] = {"code": code, "expires_at": expiry_time}
    
# @app.route('/student_login')
# def student_login():
#     return render_template('student_login.html')

@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        roll_no = request.form['roll_no']
        password = request.form['password']

        cursor = db.cursor()
        cursor.execute("SELECT * FROM login_students WHERE roll_no = %s", [roll_no])
        student = cursor.fetchone()
        cursor.close()

        if student:
            stored_hashed_password = student[8]  # Assuming password is in the 3rd column (index 2)

            # Verify entered password with stored hashed password
            if check_password_hash(stored_hashed_password, password):
                session['roll_no'] = roll_no  # Store session
                session['student_name'] = student[1]  # Assuming name is in the 2nd column (index 1)
                session['profile_pic'] = student[4]  # Assuming profile picture is in the 9th column (index 4)
                session['student_email'] = student[2]  # Assuming email is in the 3rd column (index 2)
                flash("Login successful!", "success")
                return redirect(url_for('student_dashboard'))
            else:
                flash("Invalid password!", "danger")
        else:
            flash("Roll number not found!", "danger")

    return render_template('student_login.html')

def send_reset_otp(email):
    otp = str(random.randint(100000, 999999))
    expiry_time = datetime.now() + timedelta(minutes=5)

    session["reset_otp"] = otp
    session["reset_email"] = email
    session["reset_otp_expiry"] = expiry_time.strftime("%Y-%m-%d %H:%M:%S")

    print(f"✅ Debug: Password Reset OTP Stored -> {otp}")  # Debugging

    # 🚀 TODO: Replace with actual email sending function if needed
    # return True
    subject = "Your OTP for Password Reset"
    body = f"Your OTP is {otp}. This OTP is valid for 5 minutes."
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, email, msg.as_string())
        server.quit()
        print(f"✅ OTP Generated: {otp}, Expires at: {session['reset_otp_expiry']}")  # Debugging
        print(f"✅ OTP Sent Successfully to {email}")
        return True
    except Exception as e:
        print("❌ Email Sending Error:", str(e)) 
        print("Email Error:", e)
        return False
# Route: Forgot Password Page
# ✅ Route: Forgot Password (Send OTP)
@app.route("/forgot_password", methods=["GET","POST"])
def forgot_password():
    if request.method == "GET":
        return render_template("forgot_password.html")  # ✅ Serve the forgot password page
   
   
    data = request.get_json()
    email = data.get("email")

   
    # ✅ Check in both student & teacher tables
    cursor.execute(
        "SELECT roll_no FROM login_students WHERE email = %s UNION SELECT id FROM teachers WHERE email = %s", 
        (email, email)
    )
    user = cursor.fetchone()

    if not user:
        return jsonify({"success": False, "error": "❌ Email not found!"}), 400

     # ✅ Clear any existing OTP to avoid multiple OTPs in session
    session.pop("reset_otp", None)
    session.pop("reset_otp_expiry", None)




      # ✅ Generate OTP
    otp = str(random.randint(100000, 999999))
    expiry_time = datetime.now() + timedelta(minutes=5)  # OTP expires in 5 minutes


     # ✅ Store OTP in session
    session["reset_otp"] = otp
    session["reset_email"] = email
    session["reset_otp_expiry"] = expiry_time.strftime("%Y-%m-%d %H:%M:%S")

    print(f"✅ Debug: OTP Stored in Session -> {session.get('reset_otp')}")  # Debugging

    send_reset_otp(email)
    return jsonify({"success": True}), 200

# ✅ Route: Verify OTP
@app.route("/verify_reset_otp", methods=["POST"])
def verify_reset_otp():
    data = request.get_json()
    entered_otp = data.get("otp")


      # ✅ Debug: Print full session data before checking OTP
    print(f"🔍 Debug: Full Session Data Before OTP Check -> {session}")


    # 🚨 Debugging
    stored_otp = session.get("reset_otp")# ✅ Only check `reset_otp`
    expiry_time_str = session.get("reset_otp_expiry")

    print(f"🔍 Debug: Entered OTP -> {entered_otp}, Stored OTP -> {stored_otp}")


    if not stored_otp or not expiry_time_str:
        return jsonify({"verified": False, "error": "❌ OTP expired or not generated"}), 400
    
    expiry_time = datetime.strptime(expiry_time_str, "%Y-%m-%d %H:%M:%S")

    if datetime.now() > expiry_time:
        session.pop("reset_otp", None)
        session.pop("reset_otp_expiry", None)
        return jsonify({"verified": False, "error": "❌ OTP expired!"}), 400

    if str(entered_otp).strip() == str(stored_otp).strip(): # ✅ Fix comparison to avoid whitespace issues
        session["reset_otp_verified"] = True
        return jsonify({"verified": True}), 200# ✅ Return success response when OTP is correct

    return jsonify({"verified": False, "error": "❌ Invalid OTP"}), 400



# ************************
    # if stored_otp and entered_otp == stored_otp:
    #     session["reset_otp_verified"] = True
    #     return jsonify({"verified": True}), 200
    # return jsonify({"verified": False, "error": "❌ Invalid OTP!"}), 400

# ✅ Route: Reset Password
@app.route("/reset_password", methods=["POST"])
def reset_password():
    if not session.get("reset_otp_verified"):
        flash("❌ Unauthorized request!", "danger")
        return redirect(url_for("forgot_password"))

    email = session.get("reset_email")
    new_password = request.form["new_password"]
    confirm_password = request.form["confirm_password"]

    # ✅ Validate password match
    if new_password != confirm_password:
        flash("❌ Passwords do not match!", "danger")
        return redirect(url_for("forgot_password"))

    # ✅ Hash the new password
    hashed_password = generate_password_hash(new_password)

     # ✅ Check if email belongs to a student or teacher
    cursor.execute("SELECT roll_no FROM login_students WHERE email = %s", (email,))
    student = cursor.fetchone()

    cursor.execute("SELECT id FROM teachers WHERE email = %s", (email,))
    teacher = cursor.fetchone()

     # ✅ Update the corresponding table
    if student:
        cursor.execute("UPDATE login_students SET password = %s WHERE email = %s", (hashed_password, email))        
        user_type = "student"

    elif teacher:
        cursor.execute("UPDATE teachers SET password = %s WHERE email = %s", (hashed_password, email))        
        user_type = "teacher"

    else:
        flash("❌ Email not found in records!", "danger")
        return redirect(url_for("forgot_password"))
    db.commit()
    session.clear()


    




    # # ✅ Update password in the correct table (Students or Teachers)

    # cursor.execute("UPDATE login_students SET password = %s WHERE email = %s", (hashed_password, email))
    # cursor.execute("UPDATE teachers SET password = %s WHERE email = %s", (hashed_password, email))
    
    # db.commit()
    # # cursor.close()
    # db.close()
    # # ✅ Clear session
    # session.clear()
    
    flash("✅ Password updated successfully! Please login.", "success")
    # return redirect(url_for("student_login"))

      # ✅ Redirect based on user type
    if user_type == "student":
        return redirect(url_for("student_login"))
    else:
        return redirect(url_for("teacher_login"))



# debug aoutput which route is called get / post request
@app.before_request
def debug_request():
    print(f"🔍 Debug: {request.method} {request.path}")


    
# <---------- Student dashboard -----------> 
@app.route('/student_dashboard')
def student_dashboard():
    if 'roll_no' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('student_login'))
    roll_no = session['roll_no']
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current time
    print("Current Time:", current_time)  # Debugging

    # return render_template('student_dashboard.html',template_folder='templates' ,roll_no = roll_no, current_time=current_time)
    print(f"✅ Student Dashboard - Current Time: {current_time}")  # Debugging

    return render_template('student_dashboard.html', roll_no=roll_no, current_time=current_time)

    # return f"Welcome, Student Roll No: {session['roll_no']}! (dashboard)"


#<----------------  Student_attendance  -----------------> 
@app.route('/student_attendance')
def student_attendance():
    if 'roll_no' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('student_login'))

    time = request.args.get('time')
    subject = request.args.get('subject')
    teacher_name = request.args.get('teacher')

    # ✅ Step 2: Store `teacher_name` in session (Modified section)
    if teacher_name:
        session['teacher_name'] = teacher_name  # 🔥 Now teacher_name is saved in session!

    
   

    # Fetch student details from session
    cursor.execute("SELECT name, roll_no FROM login_students WHERE roll_no = %s", (session['roll_no'],))
    student = cursor.fetchone()

    if student:
        student_name, roll_no = student
        return render_template('student_attendance.html', 
                               student_name=student_name, 
                               roll_no=roll_no, 
                               datetime=datetime.now().strftime("%Y-%m-%d %H:%M"),
                                teacher_name=teacher_name,  
                               subject=subject)
    else:
        flash("Student not found!", "danger")
        return redirect(url_for('student_dashboard'))

#<----------- get_student_details ------------>
@app.route('/get_student_details')
def get_student_details():
    if 'roll_no' not in session:
        return jsonify({"error": "User not logged in"}), 403  # Return JSON error

    roll_no = session['roll_no']

    # Fetch student details from database
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT name, roll_no FROM login_students WHERE roll_no = %s", (roll_no,))
    student = cursor.fetchone()

    if student:
        return jsonify({
            "name": student["name"],
            "roll_no": student["roll_no"],
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    else:
        return jsonify({"error": "Student not found"}), 404


#<-----------  Submit_attendance ------------> 
@app.route('/submit_attendance', methods=['POST'])
def submit_attendance():

    if 'roll_no' not in session:
        return redirect(url_for('student_login'))  # Ensure student is logged in


    student_name = request.form.get('student_name')
    roll_no = request.form.get('roll_no')
    subject = request.form.get('subject')
    entered_code = request.form.get('code')
    datetime_value = request.form['datetime']
    teacher_id = session.get('teacher_id')  # Get teacher_id from session


    if subject in generated_codes:
        stored_code = generated_codes[subject]['code']
        expiry = generated_codes[subject]['expires_at']

        if datetime.now() > datetime.fromtimestamp(expiry):
            flash("❌ Code expired! Please ask your teacher for a new one.", "danger")
        elif int(entered_code) == stored_code:
            flash("✅ Attendance marked successfully!", "success")
            # return render_template('attendance_success_std.html')
            # Store attendance in MySQL
            teacher_name = request.form.get('teacher_name')  # ✅ Get teacher name from form

            if not teacher_name:  # ✅ If missing, fetch from database
                  cursor.execute("SELECT name FROM teachers WHERE subject = %s", (subject,))
                  teacher_data = cursor.fetchone()
                  teacher_name = teacher_data["teacher_name"] if teacher_data else "Unknown Teacher"


            cursor.execute("INSERT INTO attendance (student_name, roll_no, subject, date, status, teacher_name, teacher_id) VALUES (%s, %s, %s, NOW(), 'Present', %s, %s)", 
                    (student_name, roll_no, subject, teacher_name, teacher_id))

            db.commit()
        else:
            flash("❌ Incorrect code! Try again.", "danger")
    else:
        flash("⚠️ No valid code found for this subject!", "danger")

    return redirect(url_for('student_dashboard'))




# coutn students which are submit_attendance (live / previus)

@app.route('/get_attendance_count', methods=['GET'])
def get_attendance_count():
    if 'teacher_id' not in session:
        return jsonify({'error': 'Unauthorized access'}), 403  

    selected_date = request.args.get('date')
    teacher_id = session['teacher_id']

    if not selected_date:
        return jsonify({'error': 'No date provided'}), 400

    try:
        cursor = db.cursor()

        # Fetch teacher's subject
        cursor.execute("SELECT subjects FROM teachers WHERE id = %s", (teacher_id,))
        teacher_subject = cursor.fetchone()
        
        if not teacher_subject:
            print("🔴 Error: No subject found for teacher_id:", teacher_id)  # Debugging output
            return jsonify({'error': 'Teacher subject not found'}), 404
        
        teacher_subject = teacher_subject[0]  # Extract subject

        # Debugging output
        print(f"✅ Teacher {teacher_id} is teaching {teacher_subject}")

        # Count attendance for this teacher's subject on the selected date
        cursor.execute("SELECT COUNT(*) FROM attendance WHERE date = %s AND subject = %s", 
                       (selected_date, teacher_subject))
        count = cursor.fetchone()

        if count is None:
            print("🔴 Error: No attendance records found for", selected_date, "and subject:", teacher_subject)
            return jsonify({'count': 0})  # Return 0 if no attendance found
        
        print(f"✅ Attendance Count for {teacher_subject} on {selected_date} -> {count[0]}")
        return jsonify({'count': count[0]})

    except Exception as e:
        print("🔴 Error Fetching Attendance Count:", str(e))  # Print exact error
        return jsonify({'error': str(e)}), 500

  
#Student login form with session 



# @app.route('/student', methods=['GET', 'POST'])
# def student():
#     student = None
#     if request.method == 'POST':
#         roll_no = request.form['roll_no']
#         password = request.form['password']
#         hashed_password = generate_password_hash(password)


#         # Fetch student from the database
#         cursor = db.cursor()
#         if roll_no == hashed_password:
#           cursor.execute("SELECT * FROM login_students WHERE roll_no = %s", (roll_no,))
#           student = cursor.fetchone()
#         #   cursor.close()
         
#         # Validate credentials
#         if student :
#             session['student_roll_no'] = student[0]  #store roll_no in a session 
#             flash("Login successful!", "success")
#             return redirect(url_for('student_dashboard'))  # Redirect to dashboard

#         else:
#             flash("Invalid Roll Number or Password", "danger")
    
#     return redirect(url_for('student_login'))

# Studetn Dashboard Route ###



# @app.route('/generate_code', methods=['POST'])
# def generate_code():
#     if 'phone' not in session:
#         return jsonify({'error': 'Unauthorized access'}), 403
    
#     generated_code = random.randint(100000, 999999)
#     session['attendance_code'] = generated_code  # Store in session for verification
    
#     return jsonify({'generated_code': generated_code})

# @app.route('/get_teacher_details')
# def get_teacher_details():
#     if 'phone' not in session:
#         return jsonify({'error': 'Unauthorized access'}), 403
    
#     phone = session['phone']
#     cursor.execute("SELECT name, subjects FROM teachers WHERE phone = %s", (phone,))
#     teacher = cursor.fetchone()
    
#     if teacher:
#         name, subject = teacher
#         return jsonify({'name': name, 'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'subject': subject})
#     else:
#         return jsonify({'error': 'Teacher not found'}), 404

# <----------------EDIT_PROFILE ROUTE STUDENT --------------------->
@app.route('/edit_profile')
def edit_profile():
    if 'roll_no' not in session:
        return redirect(url_for('student_login'))
    return render_template('student_profile.html')


# <---------------------HANDLE PROFILE UPDATE STUDENT--------------->
@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'roll_no' not in session:
        return redirect(url_for('student_login'))

    roll_no = session['roll_no']
    name = request.form['name']
    new_password = request.form['password']
    file = request.files['profile_picture']

    cursor = db.cursor()

    # Update name
    cursor.execute("UPDATE login_students SET name = %s WHERE roll_no = %s", (name, roll_no))
    session['student_name'] = name

    # Update profile picture
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        cursor.execute("UPDATE login_students SET profile_pic = %s WHERE roll_no = %s", (filename, roll_no))
        session['profile_pic'] = filename  # Update session

    # Update password if entered
    if new_password:
        hashed_password = generate_password_hash(new_password)
        cursor.execute("UPDATE login_students SET password = %s WHERE roll_no = %s", (hashed_password, roll_no))

    db.commit()
    cursor.close()
    
    return redirect(url_for('student_dashboard'))

# <---------------------REMOVE PROFILE PIC STUDENT --------------->
@app.route('/remove_profile_picture', methods=['POST'])
def remove_profile_picture():
    if 'roll_no' not in session:
        return redirect(url_for('student_login'))

    roll_no = session['roll_no']

    cursor = db.cursor()
    cursor.execute("UPDATE login_students SET profile_pic = %s WHERE roll_no = %s", ("default.png", roll_no))
    db.commit()
    cursor.close()

    session['profile_pic'] = "default.png"  # Update session
    return redirect(url_for('edit_profile'))


# <----------------EDIT_PROFILE ROUTE TEACHER --------------------->
@app.route('/edit_teacher_profile')
def edit_teacher_profile():
    if 'teacher_id' not in session:
        return redirect(url_for('teacher_login'))

    session.setdefault('teacher_name', 'Unknown Teacher')
    session.setdefault('teacher_profile_pic', 'default.png')


    # ALTERNATIVE WAY
    # if 'teacher_name' not in session:
    #     session['teacher_name'] = "Unknown Teacher"  # Default name
    # if 'teacher_profile_pic' not in session:
    #     session['teacher_profile_pic'] = "default.png"  # Default profile picture
    
    return render_template('teacher_profile.html')


# <---------------------HANDLE [ update teacher ]PROFILE UPDATE TEACHER--------------->
@app.route('/update_teacher_profile', methods=['POST'])
def update_teacher_profile():
    if 'teacher_id' not in session:
        return redirect(url_for('teacher_login'))

    teacher_id = session['teacher_id']
    name = request.form['name']
    new_password = request.form['password']
    file = request.files['profile_picture']

    cursor = db.cursor()

    # Update teacher name
    cursor.execute("UPDATE teachers SET name = %s WHERE id = %s", (name, teacher_id))
    session['teacher_name'] = name    # update teacher

    # Update teacher profile picture
    if file and file.filename != '':
        filename = secure_filename(file.filename) #Ensure safe filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Save only the filename in the database
        cursor.execute("UPDATE teachers SET profile_pic = %s WHERE id = %s", (filename, teacher_id))
        session['teacher_profile_pic'] = filename  # Update session

    # Update teacher password if entered
    if new_password:
        hashed_password = generate_password_hash(new_password)
        cursor.execute("UPDATE teachers SET password = %s WHERE id = %s", (hashed_password, teacher_id))

    db.commit()
    cursor.close()
    
    return redirect(url_for('teacher_dashboard'))

# <---------------------REMOVE PROFILE PIC TEACHER --------------->
@app.route('/remove_teacher_profile_picture', methods=['POST'])
def remove_teacher_profile_picture():
    if 'teacher_id' not in session:
        return redirect(url_for('teacher_login'))

    teacher_id = session['teacher_id']

    cursor = db.cursor()
    cursor.execute("UPDATE teachers SET profile_pic = %s WHERE id = %s", ("default.png", teacher_id))
    db.commit()
    cursor.close()

    session['teacher_profile_pic'] = "default.png"  # Update session
    return redirect(url_for('edit_teacher_profile'))


#<---------------- View attendance by teacher -------------->

@app.route('/view_teacher_attendance', methods=['GET', 'POST'])
def view_teacher_attendance():
    if 'teacher_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('teacher_login'))

    teacher_id = session.get('teacher_id', 'Unknown Teacher')
    date_filter = request.form.get('date', '')
    roll_no_filter = request.form.get('roll_no', '')

    # query = "SELECT * FROM attendance WHERE teacher_name = %s"
    cursor = db.cursor(pymysql.cursors.DictCursor)

    query = "SELECT student_name, roll_no, subject, DATE_FORMAT(date, '%%d-%%b-%%Y') AS formatted_date, status FROM attendance WHERE teacher_id = %s" # ✅ Use teacher_id -----[LOWER(teacher_name) = LOWER(%s)

    params = [teacher_id]

    if date_filter:
        query += " AND date = %s"
        params.append(date_filter)
    if roll_no_filter:
        query += " AND roll_no = %s"
        params.append(roll_no_filter)

    query += " ORDER BY date DESC"

    print("Debug: Executing Query ->", query)
    print("Debug: Parameters ->", params)

    # ✅ Proper cursor handling
    cursor = db.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute(query, params)
        attendance_records = cursor.fetchall()
    finally:
        cursor.close()  # ✅ Close cursor only after fetching

    print("Debug: Fetched Attendance Records ->", attendance_records)

    return render_template('view_teacher_attendance.html', attendance_records=attendance_records)


# @app.route('/view_teacher_attendance', methods=['GET', 'POST'])
# def view_teacher_attendance():
#     if 'teacher_name' not in session:
#         flash("Please log in first.", "warning")
#         return redirect(url_for('teacher_login'))

#     teacher_name = session['teacher_name']
#     date_filter = request.form.get('date', 'Unknown Teacher')  # Get selected date from form
#     roll_no_filter = request.form.get('roll_no', '')  # Get entered roll number from form

#     cursor = db.cursor(pymysql.cursors.DictCursor)


#      # Fetch attendance records
#     cursor.execute("SELECT * FROM attendance WHERE teacher_name = %s ORDER BY date DESC", (teacher_name,))
#     attendance_records = cursor.fetchall()
#     cursor.close()


#     # Query to get all students for the teacher's subject (Default)
#     query = "SELECT * FROM attendance WHERE teacher_name = %s"
#     params = [teacher_name]

#     # Apply filters based on user input
#     if date_filter:
#         query += " AND date = %s"
#         params.append(date_filter)
#     if roll_no_filter:
#         query += " AND roll_no = %s"
#         params.append(roll_no_filter)

#     query += " ORDER BY date DESC"  # Order by latest attendance

#     print("Debug: Executing Query ->", query)  # Print the query for debugging
#     print("Debug: Parameters ->", params)  # Print the parameters


#     cursor.execute(query, params)
#     attendance_records = cursor.fetchall()
#     cursor.close()

#     print("Debug: Fetched Attendance Records ->", attendance_records)  # Print fetched records


#     return render_template('view_teacher_attendance.html', attendance_records=attendance_records)

#<------------------ View attendance by studence -------------> 

@app.route('/view_student_attendance', methods=['GET', 'POST'])
def view_student_attendance():
    if 'roll_no' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('student_login'))

    roll_no = session.get('roll_no', 'Unknown Student')
    date_filter = request.form.get('date', '')
    selected_subject = request.form.get('subject', '')

     # Fetch student name from session
    student_name = session.get('student_name', 'Unknown Name')

     #  Fetch all distinct subjects from attendance table
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT DISTINCT subject FROM attendance WHERE roll_no = %s", [roll_no])
    subjects = [row['subject'] for row in cursor.fetchall()]

    # Fetch attendance records for the logged-in student
    query = "SELECT student_name, subject, DATE_FORMAT(date, '%%d-%%b-%%Y') AS formatted_date, status, teacher_name FROM attendance WHERE roll_no = %s"
    params = [roll_no]

    if date_filter:
        query += " AND date = %s"
        params.append(date_filter)
    
    if selected_subject:
        query += " AND subject = %s"
        params.append(selected_subject)

    query += " ORDER BY date DESC"

    print("Debug: Executing Query ->", query)
    print("Debug: Parameters ->", params)

    cursor = db.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute(query, params)
        student_attendance = cursor.fetchall()
    finally:
        cursor.close()

    print("Debug: Fetched Attendance Records ->", student_attendance)

    return render_template('view_student_attendance.html', student_attendance=student_attendance, 
                           student_name=student_name,
                           subjects=subjects)


#<------------- student attendance summary ----------->


@app.route('/student_attendance_summary')
def student_attendance_summary():
    if 'roll_no' not in session:
        return redirect(url_for('student_login'))

    roll_no = session['roll_no']
    cursor = db.cursor(pymysql.cursors.DictCursor)

    # Count total lectures per subject
    cursor.execute("""
        SELECT subject, COUNT(*) AS total_present
        FROM attendance
        WHERE roll_no = %s
        GROUP BY subject
    """, (roll_no,))
    attendance_data = cursor.fetchall()

    cursor.close()

    return jsonify(attendance_data)













#<--------------------------- LOGOUT SESSION ------------------>

@app.route('/logout')
def logout():
    session.pop('roll_no', None)  # Remove user from session
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)




# Close the database connection when the app is terminated