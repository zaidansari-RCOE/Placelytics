# Placelytics
Placelytics is a web platform designed for university placement cells to securely manage, analyze, and visualize student hiring data using a normalized MySQL database and real-time statistical dashboards.

****
# 📊 Placelytics: Campus Placement Analytics System

> **A dynamic, role-based DBMS and Analytics platform designed to transition college placement tracking from static spreadsheets to a normalized relational database.**

Placelytics is a web application built for university placement cells to securely manage, analyze, and visualize student hiring data. It features real-time statistical dashboards, automated insights, and a predictive probability engine, all powered by a robust MySQL backend.

---

## ✨ Key Features

* **🗄️ Relational Database Architecture:** Fully normalized MySQL schema utilizing Primary/Foreign keys, CASCADE deletions, and complex `JOIN` queries for data integrity.
* **🔐 Role-Based Access Control (RBAC):** Secure routing for **College Admins** (Data Entry & Management) and **Students** (Read-only Analytics).
* **📈 Real-Time Visual Dashboard:** Interactive graphs powered by Chart.js mapping top recruiters, average packages, and batch placement percentages.
* **🔮 Predictive Engine (Beta):** A prototype UI for forecasting student placement probability based on historical CGPA, skills, and internship metrics.
* **⚡ Instant Search & Export:** Millisecond-filtering of the complete student database and 1-click export functionality for AICTE/University reporting.

---

## 🛠️ Technology Stack

* **Backend:** Python 3, Flask framework
* **Database:** MySQL, PyMySQL (Connector)
* **Data Processing:** Pandas
* **Frontend:** HTML5, CSS3, Bootstrap 5
* **Data Visualization:** Chart.js, JavaScript

---

## 🗃️ Database Schema (DBMS Highlights)

The system moves away from flat-file storage into a 3-table normalized relational model:
1. `Students` `(student_id [PK], name, batch_year)`
2. `Companies` `(company_id [PK], company_name)`
3. `Placement_Records` `(record_id [PK], student_id [FK], company_id [FK], package_lpa, status)`

*DML Operations include `INNER JOIN` aggregations to calculate real-time averages and counts across all tables.*

---

## 🚀 Local Installation & Setup

Follow these steps to run Placelytics on your local machine:

### Prerequisites
* Python 3.8 or higher installed.
* XAMPP or MySQL Workbench installed.

### Step 1: Clone the Repository
```bash
git clone [https://github.com/yourusername/placelytics.git](https://github.com/yourusername/placelytics.git)
cd placelytics
```
*(Note: Replace `yourusername` with your actual GitHub username).*

### Step 2: Install Python Dependencies
```bash
pip install flask pandas pymysql
```

### Step 3: Setup the MySQL Database
1. Open MySQL Workbench or XAMPP (phpMyAdmin).
2. Create a new database named `placement_db`.
3. Open a new SQL query tab and execute the table creation queries provided in the project report (or import the `.sql` dump file).

### Step 4: Run the Application
1. Open your terminal in the project directory.
2. Start the Flask server:
```bash
python app.py
```
3. Open your web browser and navigate to `http://127.0.0.1:5000`.

### Default Access Credentials
* **Student View:** Select "Student" from the dropdown (No password required).
* **Admin View:** Select "College Admin" and use password: `admin123`

---

## 📤 GitHub Upload Steps

Follow these steps to finalize your repository submission:

1. Go to your repository on GitHub.
2. Click **"Add a README"** (or click the pencil icon to edit your existing one).
3. Paste this entire text into the editor.
4. Drag and drop your screenshots into the designated areas in the section below.
5. Click **"Commit changes"** to save.

---
*Developed as a Mini-Project.*

