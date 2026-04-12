from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
import csv
import os

app = Flask(__name__)
app.secret_key = 'rizvi_super_secret_key' # Needed for secure login sessions

CSV_FILE = 'placement_data.csv'

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

# --- 2. DASHBOARD ROUTE (Data Processing) ---
@app.route('/dashboard')
def dashboard():
    if 'role' not in session:
        return redirect(url_for('login'))

    # Read unstructured data and process it
    df = pd.read_csv(CSV_FILE)
    
    # Statistical Analysis
    total_students = len(df)
    placed_students = len(df[df['Status'] == 'Placed'])
    placement_perc = round((placed_students / total_students) * 100, 1) if total_students > 0 else 0
    
    # Calculate average package (excluding unplaced students)
    placed_df = df[df['Status'] == 'Placed']
    avg_package = round(placed_df['Salary'].mean(), 2) if not placed_df.empty else 0

    # Data for Charts
    # 1. Company-wise placements
    company_counts = placed_df['Company'].value_counts().to_dict()
    company_names = list(company_counts.keys())
    company_hires = list(company_counts.values())

    highest_package = df['Salary'].max()
    top_company = df['Company'].value_counts().idxmax() if not df['Company'].empty else "N/A"

    insight_text = f"Top Insight: {top_company} is currently the leading recruiter. The highest package secured this year is ₹{highest_package} LPA."
    
    return render_template('dashboard.html', 
                           total=total_students, 
                           placed=placed_students,
                           perc=placement_perc, 
                           avg=avg_package,
                           companies=company_names,
                           hires=company_hires,
                           insight=insight_text)

# --- NEW: IN-DEPTH DETAILS ROUTE ---
@app.route('/details')
def details():
    if 'role' not in session:
        return redirect(url_for('login'))

    # Read the data and convert it to a dictionary for the HTML table
    df = pd.read_csv(CSV_FILE)
    records = df.to_dict('records')

    return render_template('details.html', records=records)

# --- 3. DATA ENTRY ROUTE (College Only) ---
@app.route('/add', methods=['GET', 'POST'])
def add_record():
    if session.get('role') != 'college':
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        name = request.form.get('name')
        company = request.form.get('company')
        salary = float(request.form.get('salary'))
        status = request.form.get('status')
        year = request.form.get('year')

        # --- NEW SAFE SAVING METHOD ---
        # First, check if the file is missing a blank line at the end
        with open(CSV_FILE, 'r') as f:
            content = f.read()
            needs_newline = (len(content) > 0 and not content.endswith('\n'))

        # Append new data to the CSV securely
        with open(CSV_FILE, mode='a', newline='') as file:
            if needs_newline:
                file.write('\n') # Forces a new line if one is missing
                
            writer = csv.writer(file)
            writer.writerow([name, company, salary, status, year])
        
        flash('Placement record added successfully!', 'success')
        return redirect(url_for('add_record'))

    return render_template('add_record.html')

# --- 4. LOGOUT ROUTE ---
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)