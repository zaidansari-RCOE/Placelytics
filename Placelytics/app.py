from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
import csv
import os
import csv
import io

app = Flask(__name__)
app.secret_key = 'rizvi_super_secret_key' # Needed for secure login sessions

CSV_FILE = 'placement_data.csv'

import pymysql

# --- DATABASE CONNECTION FUNCTION ---
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',         # Your MySQL Workbench username
        password='Zaid@89537',         # Your MySQL Workbench password (leave blank if you don't use one)
        database='placement_db',
        cursorclass=pymysql.cursors.DictCursor
    )

# --- 1. LOGIN ROUTE ---
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form.get('role')
        password = request.form.get('password')

        # Role-Based Access Control
        if role == 'college' and password == 'admin123':
            session['role'] = 'college'
            return redirect(url_for('add_record'))
        elif role == 'student':
            session['role'] = 'student'
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html')

# --- 2. DASHBOARD ROUTE (MySQL Version) ---
@app.route('/dashboard')
def dashboard():
    if 'role' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Total Students
    cursor.execute("SELECT COUNT(*) as count FROM Students")
    total_students = cursor.fetchone()['count']

    # 2. Placed Students
    cursor.execute("SELECT COUNT(*) as count FROM Placement_Records WHERE status = 'Placed'")
    placed_students = cursor.fetchone()['count']

    # Placement Percentage
    placement_perc = round((placed_students / total_students) * 100, 1) if total_students > 0 else 0

    # 3. Average Package
    cursor.execute("SELECT AVG(package_lpa) as avg FROM Placement_Records WHERE status = 'Placed'")
    avg_result = cursor.fetchone()['avg']
    avg_package = round(avg_result, 2) if avg_result else 0

    # 4. Chart Data (Using a Relational JOIN)
    cursor.execute("""
        SELECT c.company_name, COUNT(p.record_id) as hires 
        FROM Placement_Records p 
        JOIN Companies c ON p.company_id = c.company_id 
        WHERE p.status = 'Placed' 
        GROUP BY c.company_name 
        ORDER BY hires DESC
    """)
    chart_data = cursor.fetchall()
    company_names = [row['company_name'] for row in chart_data]
    company_hires = [row['hires'] for row in chart_data]

    # 5. Automated Insights
    cursor.execute("SELECT MAX(package_lpa) as max_pkg FROM Placement_Records")
    max_pkg_result = cursor.fetchone()['max_pkg']
    highest_package = max_pkg_result if max_pkg_result else 0

    top_company = company_names[0] if company_names else "N/A"
    insight_text = f"Top Insight: {top_company} is currently the leading recruiter. The highest package secured this year is ₹{highest_package} LPA."

    conn.close()

    return render_template('dashboard.html', 
                           total=total_students, 
                           placed=placed_students,
                           perc=placement_perc, 
                           avg=avg_package,
                           companies=company_names,
                           hires=company_hires,
                           insight=insight_text)

# --- NEW: IN-DEPTH DETAILS ROUTE (MySQL Version) ---
@app.route('/details')
def details():
    if 'role' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            s.student_id, 
            s.name AS Student_Name, 
            s.linkedin_url, 
            c.company_name AS Company, 
            p.package_lpa AS Salary, 
            p.status AS Status, 
            s.batch_year AS Year
        FROM Placement_Records p
        JOIN Students s ON p.student_id = s.student_id
        JOIN Companies c ON p.company_id = c.company_id
        ORDER BY s.batch_year DESC, p.package_lpa DESC
    """)
    records = cursor.fetchall()
    conn.close()

    return render_template('details.html', records=records)
# --- 3. DATA ENTRY ROUTE (College Only) ---
# --- 3. DATA ENTRY ROUTE (MySQL Version) ---
@app.route('/add', methods=['GET', 'POST'])
def add_record():
    if session.get('role') != 'college':
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        name = request.form.get('name')
        linkedin = request.form.get('linkedin')
        company_name = request.form.get('company')
        salary = float(request.form.get('salary'))
        status = request.form.get('status')
        year = int(request.form.get('year'))

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # 1. Insert Student
            cursor.execute("""INSERT INTO Students (name, batch_year, linkedin_url) VALUES (%s, %s, %s)""", (name, year, linkedin))
            student_id = cursor.lastrowid 

            # 2. Check if Company exists, if not, insert it
            cursor.execute("SELECT company_id FROM Companies WHERE company_name = %s", (company_name,))
            company_result = cursor.fetchone()
            
            if company_result:
                company_id = company_result['company_id']
            else:
                cursor.execute("INSERT INTO Companies (company_name) VALUES (%s)", (company_name,))
                company_id = cursor.lastrowid

            # 3. Insert the Placement Record
            cursor.execute("""
                INSERT INTO Placement_Records (student_id, company_id, package_lpa, status) 
                VALUES (%s, %s, %s, %s)
            """, (student_id, company_id, salary, status))

            conn.commit() 
            flash('Placement record successfully added to MySQL Database!', 'success')
            
        except Exception as e:
            conn.rollback() 
            print("\n" + "="*30)
            print(f"🚨 MYSQL ERROR: {str(e)}")
            print("="*30 + "\n")
            flash(f'Database error: {str(e)}', 'danger')
            
        finally:
            conn.close()

        return redirect(url_for('add_record'))

    return render_template('add_record.html')

@app.route('/delete/<int:id>')
def delete_record(id):
    if session.get('role') != 'college':
        return redirect(url_for('dashboard'))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Since we have ON DELETE CASCADE, deleting the student 
        # will automatically delete their placement record!
        cursor.execute("DELETE FROM Students WHERE student_id = %s", (id,))
        conn.commit()
        flash('Record deleted successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error deleting record: {str(e)}', 'danger')
    finally:
        conn.close()

    return redirect(url_for('details'))


@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if session.get('role') != 'college':
        return redirect(url_for('dashboard'))

    file = request.files.get('file')
    if not file or not file.filename.endswith('.csv'):
        flash('Please upload a valid CSV file.', 'danger')
        return redirect(url_for('add_record'))

    # Read the CSV file
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.DictReader(stream)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        for row in csv_input:
            # 1. Insert Student (including LinkedIn)
            cursor.execute("""
                INSERT INTO Students (name, batch_year, linkedin_url) 
                VALUES (%s, %s, %s)
            """, (row['name'], row['year'], row.get('linkedin', '')))
            student_id = cursor.lastrowid

            # 2. Handle Company
            cursor.execute("SELECT company_id FROM Companies WHERE company_name = %s", (row['company'],))
            res = cursor.fetchone()
            if res:
                company_id = res['company_id']
            else:
                cursor.execute("INSERT INTO Companies (company_name) VALUES (%s)", (row['company'],))
                company_id = cursor.lastrowid

            # 3. Insert Record
            cursor.execute("""
                INSERT INTO Placement_Records (student_id, company_id, package_lpa, status) 
                VALUES (%s, %s, %s, %s)
            """, (student_id, company_id, float(row['salary']), row['status']))

        conn.commit()
        flash(f'Successfully imported records from CSV!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error during CSV import: {str(e)}', 'danger')
    finally:
        conn.close()

    return redirect(url_for('details'))

# --- 4. LOGOUT ROUTE ---
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
