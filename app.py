# ==============================================================================
# 24IT0537 (S.K.S.Udeshika)
# ==============================================================================
from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_unistay'

def get_db_connection():
    return pymysql.connect(
        host='localhost', user='root', password='', database='unistay_db',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        entered_username = request.form.get('username')
        entered_password = request.form.get('password')
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE unique_id = %s AND password = %s"
                cursor.execute(sql, (entered_username, entered_password))
                user = cursor.fetchone()
            connection.close()
            if user:
                session['user_id'] = user['unique_id']
                session['user_name'] = user['fullname']
                session['user_role'] = user['role']
                if user['role'] == 'student':
                    return redirect(url_for('student_dashboard'))
                elif user['role'] == 'warden':
                    return redirect(url_for('warden_dashboard'))
            else:
                return """
                <link class="styles" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.css">
                <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
                <script>
                    window.onload = function() {
                        Swal.fire({ icon: 'error', title: 'Login Failed', text: 'Invalid Username/Index No or Password!', confirmButtonColor: '#0099ff'
                        }).then(function() { window.location.href = '/'; });
                    }
                </script>
                """
        except pymysql.MySQLError as e:
            return f"<h1>Database Error: {e}</h1>"
    return render_template('login.html')

# ==============================================================================
# 📝 STUDENT / GENERAL REGISTER ROUTE
# ==============================================================================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_role = request.form.get('role')          
        fullname = request.form.get('fullname')        
        unique_id = request.form.get('unique_id')      
        email = request.form.get('email')              
        password = request.form.get('password')        
        confirm_password = request.form.get('confirm_password') 

        if password != confirm_password:
            return """
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.css">
            <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
            <script>
                window.onload = function() {
                    Swal.fire({ icon: 'warning', title: 'Oops...', text: 'Passwords do not match! Please try again.', confirmButtonColor: '#0099ff'
                    }).then(function() { window.history.back(); });
                }
            </script>
            """

        if user_role == 'warden' or unique_id.startswith('WD'):
            is_valid_warden = True
            if len(unique_id) != 6:
                is_valid_warden = False
            else:
                digits_part = unique_id[2:]
                if not digits_part.isdigit():
                    is_valid_warden = False
                else:
                    id_number = int(digits_part)
                    if not (5 <= id_number <= 20):
                        is_valid_warden = False
            
            if not is_valid_warden:
                return """
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.css">
                <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
                <script>
                    window.onload = function() {
                        Swal.fire({ icon: 'error', title: 'Registration Denied!', text: 'Invalid or Unauthorized ID Format.', confirmButtonColor: '#dc3545'
                        }).then(function() { window.history.back(); });
                    }
                </script>
                """

        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql_check = "SELECT * FROM users WHERE unique_id = %s OR email = %s"
                cursor.execute(sql_check, (unique_id, email))
                if cursor.fetchone():
                    return """
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.css">
                    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
                    <script>
                        window.onload = function() {
                            Swal.fire({ icon: 'error', title: 'Duplicate Error', text: 'ID or Email already exists! Please use a unique one.', confirmButtonColor: '#0099ff'
                            }).then(function() { window.history.back(); });
                        }
                    </script>
                    """

                sql_insert = "INSERT INTO users (role, fullname, unique_id, email, password) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql_insert, (user_role, fullname, unique_id, email, password))
                
            connection.commit()
            connection.close()
            return """
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.css">
            <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
            <script>
                window.onload = function() {
                    Swal.fire({ icon: 'success', title: 'Successful!', text: 'Registration Successful.', timer: 2000, showConfirmButton: false
                    }).then(function() { window.location.href = '/'; });
                }
            </script>
            """
        except pymysql.MySQLError as e:
            return f"<h1>Database Error: {e}</h1>"

    return render_template('register.html')



# ==============================================================================
# 24IT0480  D.K.M.N.T.Karunasagara 
# STUDENT DASHBOARD & SUB-ROUTES
# ==============================================================================
@app.route('/student')
def student_dashboard():
    if 'user_name' in session and session.get('user_role') == 'student':
        index_no = session['user_id']
        full_name = session['user_name']
        display_name = full_name.split()[-1]
        assigned_room = "Not Applied"
        
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql = "SELECT room_no FROM student_profile WHERE index_no = %s"
                cursor.execute(sql, (index_no,))
                profile = cursor.fetchone()
            connection.close()
            if profile and profile['room_no']:
                assigned_room = profile['room_no']
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            
        return render_template('student.html', view="dashboard", name=display_name, room=assigned_room)
    return redirect(url_for('login'))


@app.route('/student/profile')
def student_profile():
    if 'user_name' in session and session.get('user_role') == 'student':
        index_no = session['user_id']
        full_name = session['user_name']
        display_name = full_name.split()[-1]
        assigned_room = "Not Applied"
        profile_data = None
        
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql = "SELECT * FROM student_profile WHERE index_no = %s"
                cursor.execute(sql, (index_no,))
                profile = cursor.fetchone()
            connection.close()
            if profile:
                profile_data = profile
                if profile['room_no']:
                    assigned_room = profile['room_no']
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            
        return render_template('student.html', view="profile", name=display_name, room=assigned_room, profile=profile_data)
    return redirect(url_for('login'))  

@app.route('/save_profile', methods=['POST'])
def save_profile():
    if 'user_id' not in session: return redirect(url_for('login'))
    index_no = session['user_id']
    fullname = request.form.get('fullname')
    name_initials = request.form.get('name_initials')
    dob = request.form.get('dob')
    district = request.form.get('district')
    town = request.form.get('town')
    distance_itum = request.form.get('distance_itum')
    religion = request.form.get('religion')
    nation = request.form.get('nation')
    phone = request.form.get('phone')
    mother_name = request.form.get('mother_name')
    mother_phone = request.form.get('mother_phone')
    mother_job = request.form.get('mother_job')
    father_name = request.form.get('father_name')
    father_phone = request.form.get('father_phone')
    father_job = request.form.get('father_job')
    
    ol_year = request.form.get('ol_year')
    ol_index = request.form.get('ol_index')
    ol_science = request.form.get('ol_science')
    ol_maths = request.form.get('ol_maths')
    ol_english = request.form.get('ol_english')
    ol_religion = request.form.get('ol_religion')
    ol_language = request.form.get('ol_language')
    ol_history = request.form.get('ol_history')
    
    ol_basket1_name = request.form.get('ol_basket1_name')
    ol_basket1_grade = request.form.get('ol_basket1_grade')
    ol_basket2_name = request.form.get('ol_basket2_name')
    ol_basket2_grade = request.form.get('ol_basket2_grade')
    ol_basket3_name = request.form.get('ol_basket3_name')
    ol_basket3_grade = request.form.get('ol_basket3_grade')
    
    al_year = request.form.get('al_year')
    al_index = request.form.get('al_index')
    al_zscore = request.form.get('al_zscore')
    al_maths = request.form.get('al_maths')
    al_physics = request.form.get('al_physics')
    al_chemistry = request.form.get('al_chemistry')
    
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO student_profile 
                (index_no, fullname, name_initials, dob, district, town, distance_itum, religion, nation, phone, 
                 mother_name, mother_phone, mother_job, father_name, father_phone, father_job,
                 ol_year, ol_index, ol_science, ol_maths, ol_english, ol_religion, ol_language, ol_history, 
                 ol_basket1_name, ol_basket1_grade, ol_basket2_name, ol_basket2_grade, ol_basket3_name, ol_basket3_grade,
                 al_year, al_index, al_zscore, al_maths, al_physics, al_chemistry) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                fullname=%s, name_initials=%s, dob=%s, district=%s, town=%s, distance_itum=%s, religion=%s, nation=%s, phone=%s,
                mother_name=%s, mother_phone=%s, mother_job=%s, father_name=%s, father_phone=%s, father_job=%s,
                ol_year=%s, ol_index=%s, ol_science=%s, ol_maths=%s, ol_english=%s, ol_religion=%s, ol_language=%s, ol_history=%s, 
                ol_basket1_name=%s, ol_basket1_grade=%s, ol_basket2_name=%s, ol_basket2_grade=%s, ol_basket3_name=%s, ol_basket3_grade=%s,
                al_year=%s, al_index=%s, al_zscore=%s, al_maths=%s, al_physics=%s, al_chemistry=%s
            """
            data = (
                index_no, fullname, name_initials, dob, district, town, distance_itum, religion, nation, phone, mother_name, mother_phone, mother_job, father_name, father_phone, father_job,
                ol_year, ol_index, ol_science, ol_maths, ol_english, ol_religion, ol_language, ol_history, ol_basket1_name, ol_basket1_grade, ol_basket2_name, ol_basket2_grade, ol_basket3_name, ol_basket3_grade, al_year, al_index, al_zscore, al_maths, al_physics, al_chemistry,
                fullname, name_initials, dob, district, town, distance_itum, religion, nation, phone, mother_name, mother_phone, mother_job, father_name, father_phone, father_job,
                ol_year, ol_index, ol_science, ol_maths, ol_english, ol_religion, ol_language, ol_history, ol_basket1_name, ol_basket1_grade, ol_basket2_name, ol_basket2_grade, ol_basket3_name, ol_basket3_grade, al_year, al_index, al_zscore, al_maths, al_physics, al_chemistry
            )
            cursor.execute(sql, data)
        connection.commit()
        connection.close()
        return """
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.css">
        <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
        <script>
            window.onload = function() {
                Swal.fire({ icon: 'success', title: 'Profile Saved!', text: 'Updated successfully.', timer: 1500, showConfirmButton: false
                }).then(function() { window.location.href = '/student'; });
            }
        </script>
        """
    except pymysql.MySQLError as e:
        return f"<h1>Error: {e}</h1>"

# ==============================================================================
# 24IT0542  (W.G.V.W.Walpitagama)
# 🏠 Student Attendence
# ==============================================================================
@app.route('/student/attendance')
def student_attendance():
    if 'user_name' in session and session.get('user_role') == 'student':
        index_no = session['user_id']
        display_name = session['user_name'].split()[-1]
        go_home_list = []
        go_out_list = []
        
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql_home = "SELECT * FROM go_home_logs WHERE index_no = %s ORDER BY id DESC"
                cursor.execute(sql_home, (index_no,))
                go_home_list = cursor.fetchall()
                
                sql_out = "SELECT * FROM go_out_logs WHERE index_no = %s ORDER BY id DESC"
                cursor.execute(sql_out, (index_no,))
                go_out_list = cursor.fetchall()
            connection.close()
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            
        return render_template('student.html', view="attendance", name=display_name, go_home_list=go_home_list, go_out_list=go_out_list)
    return redirect(url_for('login'))


@app.route('/attendance/go_home/leave', methods=['POST'])
def go_home_leave():
    if 'user_id' not in session: return redirect(url_for('login'))
    index_no = session['user_id']
    dep_date = request.form.get('dep_date')
    dep_time = request.form.get('dep_time')
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "INSERT INTO go_home_logs (index_no, departure_date, departure_time, status) VALUES (%s, %s, %s, 'Away')"
            cursor.execute(sql, (index_no, dep_date, dep_time))
        connection.commit()
        connection.close()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    return redirect(url_for('student_attendance'))

@app.route('/attendance/go_home/return', methods=['POST'])
def go_home_return():
    if 'user_id' not in session: return redirect(url_for('login'))
    log_id = request.form.get('log_id')
    curr_date = datetime.now().strftime('%Y-%m-%d')
    curr_time = datetime.now().strftime('%H:%M:%S')
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "UPDATE go_home_logs SET arrival_date=%s, arrival_time=%s, status='Returned' WHERE id=%s"
            cursor.execute(sql, (curr_date, curr_time, log_id))
        connection.commit()
        connection.close()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    return redirect(url_for('student_attendance'))

# 🆕 Go Home - Undo Route
@app.route('/attendance/go_home/undo/<int:log_id>', methods=['GET'])
def go_home_undo(log_id):
    if 'user_id' not in session: return redirect(url_for('login'))
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
           
            sql = "UPDATE go_home_logs SET arrival_date=NULL, arrival_time=NULL, status='Away' WHERE id=%s"
            cursor.execute(sql, (log_id,))
        connection.commit()
        connection.close()
    except pymysql.MySQLError as e:
        print(f"Error executing Go-Home Undo: {e}")
    return redirect(url_for('student_attendance'))


@app.route('/attendance/go_out/leave', methods=['POST'])
def go_out_leave():
    if 'user_id' not in session: return redirect(url_for('login'))
    index_no = session['user_id']
    out_date = request.form.get('out_date')
    out_time = request.form.get('out_time')
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "INSERT INTO go_out_logs (index_no, out_date, out_time, status) VALUES (%s, %s, %s, 'Outside')"
            cursor.execute(sql, (index_no, out_date, out_time))
        connection.commit()
        connection.close()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    return redirect(url_for('student_attendance'))

@app.route('/attendance/go_out/return', methods=['POST'])
def go_out_return():
    if 'user_id' not in session: return redirect(url_for('login'))
    log_id = request.form.get('log_id')
    curr_date = datetime.now().strftime('%Y-%m-%d')
    curr_time = datetime.now().strftime('%H:%M:%S')
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "UPDATE go_out_logs SET in_date=%s, in_time=%s, status='Inside' WHERE id=%s"
            cursor.execute(sql, (curr_date, curr_time, log_id))
        connection.commit()
        connection.close()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    return redirect(url_for('student_attendance'))

# 🆕 Go Out - Undo Route
@app.route('/attendance/go_out/undo/<int:log_id>', methods=['GET'])
def go_out_undo(log_id):
    if 'user_id' not in session: return redirect(url_for('login'))
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "UPDATE go_out_logs SET in_date=NULL, in_time=NULL, status='Outside' WHERE id=%s"
            cursor.execute(sql, (log_id,))
        connection.commit()
        connection.close()
    except pymysql.MySQLError as e:
        print(f"Error executing Go-Out Undo: {e}")
    return redirect(url_for('student_attendance'))


# ==============================================================================
# 💰 BURSARY & COMPLAINT MANAGEMENT
# ==============================================================================
@app.route('/student/bursary')
def student_bursary():
    if 'user_name' in session and session.get('user_role') == 'student':
        index_no = session['user_id']
        display_name = session['user_name'].split()[-1]
        welfare_data = None
        monthly_records = []
        
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql = "SELECT * FROM student_welfare WHERE index_no = %s"
                cursor.execute(sql, (index_no,))
                welfare_data = cursor.fetchone()
                
                sql_months = "SELECT bursary_month, received_status, DATE_FORMAT(updated_at, '%%Y-%%m-%%d %%H:%%i') as updated_at FROM bursary_monthly_records WHERE index_no = %s ORDER BY FIELD(bursary_month, 'January','February','March','April','May','June','July','August','September','October','November','December')"
                cursor.execute(sql_months, (index_no,))
                monthly_records = cursor.fetchall()
            connection.close()
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            
        return render_template('student.html', view="bursary", name=display_name, welfare=welfare_data, monthly_records=monthly_records)
    return redirect(url_for('login'))


@app.route('/save_bursary_status', methods=['POST'])
def save_bursary_status():
    if 'user_id' not in session: return redirect(url_for('login'))
    index_no = session['user_id']
    bursary_month = request.form.get('bursary_month')
    monthly_status = request.form.get('monthly_status')
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO bursary_monthly_records (index_no, bursary_month, received_status) 
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE received_status = %s
            """
            cursor.execute(sql, (index_no, bursary_month, monthly_status, monthly_status))
        connection.commit()
        connection.close()
        return """
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.css">
        <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
        <script>
            window.onload = function() {
                Swal.fire({ icon: 'success', title: 'Bursary Record Saved!', text: 'Status recorded successfully.', timer: 1500, showConfirmButton: false
                }).then(function() { window.location.href = '/student/bursary'; });
            }
        </script>
        """
    except pymysql.MySQLError as e:
        return f"<h1>Error updating multi-month bursary status: {e}</h1>"

@app.route('/save_complaint', methods=['POST'])
def save_complaint():
    if 'user_id' not in session: return redirect(url_for('login'))
    index_no = session['user_id']
    title = request.form.get('title')
    description = request.form.get('description')
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO student_welfare (index_no, complaint_title, complaint_description, complaint_status) 
                VALUES (%s, %s, %s, 'Open')
                ON DUPLICATE KEY UPDATE complaint_title=%s, complaint_description=%s, complaint_status='Open'
            """
            cursor.execute(sql, (index_no, title, description, title, description))
        connection.commit()
        connection.close()
        return """
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.css">
        <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
        <script>
            window.onload = function() {
                Swal.fire({ icon: 'success', title: 'Complaint Submitted!', text: 'Sent successfully.', timer: 1500, showConfirmButton: false
                }).then(function() { window.location.href = '/student/bursary'; });
            }
        </script>
        """
    except pymysql.MySQLError as e:
        return f"<h1>Error: {e}</h1>"

# ==============================================================================
# 24IT0547  (W.M.M.N.K.Wijesingha)
# 🛡️ WARDEN ROUTE
# ==============================================================================
@app.route('/register/warden', methods=['GET', 'POST'])
def register_warden():
    if request.method == 'POST':
        user_role = 'warden'                                            
        fullname = request.form.get('fullname')        
        unique_id = request.form.get('unique_id')      
        email = request.form.get('email')              
        password = request.form.get('password')        
        confirm_password = request.form.get('confirm_password') 

        if password != confirm_password:
            return """
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.css">
            <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
            <script>
                window.onload = function() {
                    Swal.fire({ icon: 'warning', title: 'Match Error', text: 'Passwords do not match! Please try again.', confirmButtonColor: '#198754'
                    }).then(function() { window.history.back(); });
                }
            </script>
            """

        is_valid_id = True
        if not unique_id.startswith('WD') or len(unique_id) != 6:
            is_valid_id = False
        else:
            try:
                digits_part = unique_id[2:]
                if not digits_part.isdigit():
                    is_valid_id = False
                else:
                    id_number = int(digits_part)
                    if not (5 <= id_number <= 20):
                        is_valid_id = False
            except ValueError:
                is_valid_id = False

        if not is_valid_id:
            return """
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.css">
            <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
            <script>
                window.onload = function() {
                    Swal.fire({ icon: 'error', title: 'Registration Denied!', text: 'Invalid or Unauthorized Warden ID.', confirmButtonColor: '#dc3545'
                    }).then(function() { window.history.back(); });
                }
            </script>
            """

        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql_check = "SELECT * FROM users WHERE unique_id = %s OR email = %s"
                cursor.execute(sql_check, (unique_id, email))
                if cursor.fetchone():
                    return """
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.css">
                    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
                    <script>
                        window.onload = function() {
                            Swal.fire({ icon: 'error', title: 'Error', text: 'Warden ID or Email already exists!', confirmButtonColor: '#198754'
                            }).then(function() { window.history.back(); });
                        }
                    </script>
                    """

                sql_insert = "INSERT INTO users (role, fullname, unique_id, email, password) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql_insert, (user_role, fullname, unique_id, email, password))
                
            connection.commit()
            connection.close()
            return """
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.css">
            <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
            <script>
                window.onload = function() {
                    Swal.fire({ icon: 'success', title: 'Registered!', text: 'Warden Registration Successful.', timer: 2000, showConfirmButton: false
                    }).then(function() { window.location.href = '/'; });
                }
            </script>
            """
        except pymysql.MySQLError as e:
            return f"<h1>Database Error: {e}</h1>"

    return render_template('warden_register.html')

def get_student_count():
    count = 0
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "SELECT COUNT(*) as total FROM users WHERE role = 'student'"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result: count = result['total']
        connection.close()
    except pymysql.MySQLError as e:
        print(f"Database error while counting students: {e}")
    return count

def get_pending_complaints_count():
    count = 0
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """
                SELECT COUNT(*) as total 
                FROM student_welfare 
                WHERE complaint_status = 'Open' 
                  AND complaint_title IS NOT NULL 
                  AND complaint_title != ''
            """
            cursor.execute(sql)
            result = cursor.fetchone()
            if result: count = result['total']
        connection.close()
    except pymysql.MySQLError as e:
        print(f"Database error while counting complaints: {e}")
    return count

def get_inside_hostel_count():
    total_students = get_student_count()
    away_home = 0
    outside_short = 0
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as total FROM go_home_logs WHERE status = 'Away'")
            res_home = cursor.fetchone()
            if res_home: away_home = res_home['total']
            
            cursor.execute("SELECT COUNT(*) as total FROM go_out_logs WHERE status = 'Outside'")
            res_out = cursor.fetchone()
            if res_out: outside_short = res_out['total']
        connection.close()
    except pymysql.MySQLError as e:
        print(f"Database error while tracking location counters: {e}")
        
    inside_count = total_students - (away_home + outside_short)
    return inside_count if inside_count >= 0 else 0

@app.route('/warden')
def warden_dashboard():
    if 'user_name' in session and session.get('user_role') == 'warden':
        current_student_count = get_student_count()
        current_inside_count = get_inside_hostel_count()
        current_pending_complaints = get_pending_complaints_count()
        
        return render_template(
            'warden.html', 
            view="dashboard", 
            name=session['user_name'], 
            student_count=current_student_count,
            inside_count=current_inside_count, 
            pending_complaints=current_pending_complaints
        )
    return redirect(url_for('login'))

# ==============================================================================
# 24IT0535  (U.H.K.Udawaththa)
# 🛡️ ROOM ALLOCATION ROUTE
# ==============================================================================
@app.route('/warden/allocation')
def warden_allocation():
    if 'user_name' in session and session.get('user_role') == 'warden':
        eligible_students = []
        next_available_room = "CD200"
        
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
               
                sql = """
                    SELECT index_no, fullname, district, town, distance_itum, phone 
                    FROM student_profile 
                    WHERE (
                        CAST(REGEXP_REPLACE(distance_itum, '[^0-9.]', '') AS DECIMAL(10,2)) > 25.0 
                        OR CAST(distance_itum AS DECIMAL(10,2)) > 25.0
                    )
                    AND (room_no IS NULL OR room_no = '' OR room_no NOT LIKE 'CD%')
                    ORDER BY index_no ASC
                """
                cursor.execute(sql)
                eligible_students = cursor.fetchall()
                
                cursor.execute("""
                    SELECT room_no FROM student_profile 
                    WHERE room_no LIKE 'CD%' 
                    ORDER BY CAST(SUBSTRING(room_no, 3) AS UNSIGNED) DESC LIMIT 1
                """)
                last_room = cursor.fetchone()
                if last_room and last_room['room_no']:
                    try:
                        last_num = int(last_room['room_no'][2:])
                        next_available_room = f"CD{last_num + 1}"
                    except ValueError:
                        next_available_room = "CD200"
                    
            connection.close()
        except pymysql.MySQLError as e:
            print(f"Database Error in Allocation: {e}")
            
        return render_template(
            'warden.html', 
            view="allocation", 
            name=session['user_name'], 
            eligible_students=eligible_students,
            next_room=next_available_room
        )
    return redirect(url_for('login'))

@app.route('/warden/allocate_room', methods=['POST'])
def allocate_room():
    if 'user_id' not in session or session.get('user_role') != 'warden': 
        return redirect(url_for('login'))
        
    index_no = request.form.get('index_no')
    room_no = request.form.get('room_no')
    
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            
            sql = "UPDATE student_profile SET room_no = %s WHERE index_no = %s"
            cursor.execute(sql, (room_no, index_no))
        connection.commit()
        connection.close()
        
        return f"""
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.css">
        <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
        <script>
            window.onload = function() {{
                Swal.fire({{
                    icon: 'success',
                    title: 'Room Allocated Successfully!',
                    text: 'Room {room_no} has been assigned to Student {index_no}.',
                    confirmButtonColor: '#28a745',
                    timer: 2500
                }}).then(function() {{
                    window.location.href = '/warden/allocation';
                }});
            }}
        </script>
        """
    except pymysql.MySQLError as e:
        return f"<h1>Error allocating room in Database: {e}</h1>"

# ==============================================================================
# 24IT0538  (K.Vasanthini)
# 🛡️ VIEW STUDENT PROFILE ROUTE
# ==============================================================================
@app.route('/warden/students')
def warden_students():
    if 'user_name' in session and session.get('user_role') == 'warden':
        students_list = []
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql = "SELECT * FROM student_profile"
                cursor.execute(sql)
                students_list = cursor.fetchall()
            connection.close()
        except pymysql.MySQLError as e:
            print(f"Error fetching students: {e}")
            
        return render_template('warden.html', view="students", name=session['user_name'], student_count=get_student_count(), students=students_list)
    return redirect(url_for('login'))


# 🔎 VIEW SINGLE STUDENT PROFILE DETAILS
@app.route('/warden/students/view/<index_no>')
def warden_view_student(index_no):
    if 'user_name' in session and session.get('user_role') == 'warden':
        student_data = None
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql = "SELECT * FROM student_profile WHERE index_no = %s"
                cursor.execute(sql, (index_no,))
                student_data = cursor.fetchone()
            connection.close()
        except pymysql.MySQLError as e:
            print(f"Error fetching individual student: {e}")
        
        return render_template(
            'warden.html', 
            view="view_student", 
            name=session['user_name'], 
            student_count=get_student_count(), 
            student=student_data
        )
    return redirect(url_for('login'))


# 🎛️ Unified complaints & bursary router
@app.route('/warden/complaints')
def warden_complaints():
    if 'user_name' in session and session.get('user_role') == 'warden':
        problems_list = []
        bursary_yes = []
        bursary_no = []
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql_problems = """
                    SELECT w.*, p.fullname, p.room_no 
                    FROM student_welfare w
                    JOIN student_profile p ON w.index_no = p.index_no
                    WHERE w.complaint_title IS NOT NULL AND w.complaint_title != ''
                """
                cursor.execute(sql_problems)
                problems_list = cursor.fetchall()

                sql_bursary_yes = """
                    SELECT b.*, p.fullname 
                    FROM bursary_monthly_records b
                    JOIN student_profile p ON b.index_no = p.index_no
                    WHERE b.received_status = 'Yes'
                    ORDER BY b.updated_at DESC
                """
                cursor.execute(sql_bursary_yes)
                bursary_yes = cursor.fetchall()

                sql_bursary_no = """
                    SELECT b.*, p.fullname 
                    FROM bursary_monthly_records b
                    JOIN student_profile p ON b.index_no = p.index_no
                    WHERE b.received_status = 'No'
                    ORDER BY b.updated_at DESC
                """
                cursor.execute(sql_bursary_no)
                bursary_no = cursor.fetchall()

            connection.close()
        except pymysql.MySQLError as e:
            print(f"Error fetching data for unified complaints view: {e}")
            
        return render_template(
            'warden.html', 
            view="complaints", 
            name=session['user_name'], 
            student_count=get_student_count(),
            problems=problems_list,
            bursary_yes=bursary_yes,
            bursary_no=bursary_no
        )
    return redirect(url_for('login'))


# ==============================================================================
# 24IT0527   (E.M.T.S.Sewwandi) 
# STUDENT ATTENDANCE 
# ==============================================================================
@app.route('/warden/attendance')
def warden_attendance():
    if 'user_name' in session and session.get('user_role') == 'warden':
        inside_students = []
        search_query = request.args.get('search_index', '').strip()
        search_results_home = []
        search_results_out = []
        
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql = """
                    SELECT index_no, fullname, room_no, phone, 'No Logs Yet' AS last_date, '---' AS last_time 
                    FROM student_profile 
                    ORDER BY index_no ASC
                """
                cursor.execute(sql)
                inside_students = cursor.fetchall()
                
                if search_query:
                    cursor.execute("SELECT * FROM go_home_logs WHERE index_no = %s ORDER BY id DESC", (search_query,))
                    search_results_home = cursor.fetchall()
                    cursor.execute("SELECT * FROM go_out_logs WHERE index_no = %s ORDER BY id DESC", (search_query,))
                    search_results_out = cursor.fetchall()

            connection.close()
        except pymysql.MySQLError as e:
            print(f"Error in warden_attendance: {e}")

        student_count = len(inside_students) if inside_students else 0

        return render_template(
            'warden.html', view="attendance", name=session['user_name'], 
            student_count=student_count, inside_students=inside_students,
            search_query=search_query, search_results_home=search_results_home, search_results_out=search_results_out
        )
    return redirect(url_for('login'))
# ==============================================================================
# 🚪 2. LEFT STUDENTS 
# ==============================================================================
@app.route('/warden/leaves')
def warden_leaves():
    if 'user_name' in session and session.get('user_role') == 'warden':
        outside_students = []
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                
                sql = """
                    SELECT p.index_no, p.fullname, p.room_no, p.phone, 
                           last_log.last_date, last_log.last_time, last_log.status AS leave_type
                    FROM student_profile p
                    JOIN (
                        SELECT index_no, max_date AS last_date, max_time AS last_time, status
                        FROM (
                            SELECT index_no, out_date AS max_date, out_time AS max_time, status FROM go_out_logs
                            UNION ALL
                            SELECT index_no, in_date AS max_date, in_time AS max_time, 'Inside' as status FROM go_out_logs WHERE in_date IS NOT NULL
                            UNION ALL
                            SELECT index_no, out_date AS max_date, out_time AS max_time, status FROM go_home_logs
                            UNION ALL
                            SELECT index_no, in_date AS max_date, in_time AS max_time, 'Inside' as status FROM go_home_logs WHERE in_date IS NOT NULL
                        ) all_logs
                        WHERE (index_no, max_date, max_time) IN (
                            SELECT index_no, MAX(max_date), MAX(max_time)
                            FROM (
                                SELECT index_no, out_date AS max_date, out_time AS max_time FROM go_out_logs
                                UNION ALL
                                SELECT index_no, in_date AS max_date, in_time AS max_time FROM go_out_logs WHERE in_date IS NOT NULL
                                UNION ALL
                                SELECT index_no, out_date AS max_date, out_time AS max_time FROM go_home_logs
                                UNION ALL
                                SELECT index_no, in_date AS max_date, in_time AS max_time FROM go_home_logs WHERE in_date IS NOT NULL
                            ) t GROUP BY index_no
                        )
                    ) last_log ON p.index_no = last_log.index_no
                    WHERE last_log.status IN ('Outside', 'Away')
                    ORDER BY last_log.last_date DESC, last_log.last_time DESC
                """
                cursor.execute(sql)
                outside_students = cursor.fetchall()
            connection.close()
        except pymysql.MySQLError as e:
            print(f"Error in warden_leaves: {e}")

        return render_template(
            'warden.html', view="leaves", name=session['user_name'], 
            student_count=get_student_count(), outside_students=outside_students
        )
    return redirect(url_for('login'))


# ==============================================================================
# 🚪 LOGOUT ROUTE
# ==============================================================================
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)