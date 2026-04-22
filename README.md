# Placement Data Analysis System (PlaceLytics)

> **Abstract** : The Placement Data Analysis System is a simple application used to study and understand student placement data of a college. It collects information such as branch, company name, and salary package, and analyzes it to show placement results in an easy way. The system displays useful details like placement percentage, average package, and top recruiting companies using charts and graphs. This helps students and the placement cell to clearly understand placement performance and trends.

### Project Members
1. ANSARI MD. ZAID MASHOOQUE  [ Team Leader ] 
2. MULLA ARHAAN ASLAM 
3. JHA SAKSHAM KRISHNA KUMAR 
4. SHAIKH MOHAMMED KHALID MOHD SHAHID 

### Project Guides
1. PROF. DINESH DEORE  [ Primary Guide ] 

### Deployment Steps
Please follow the below steps to run this project on a local machine.

1. **Extract the Project:** Unzip the project folder (`RollNo_Zaid_Ansari_Placelytics.zip`) and open it in your code editor (e.g., VS Code).
2. **Database Setup:** - Open MySQL Workbench.
   - Go to `File` -> `Open SQL Script...` and select the `placement_db_backup.sql` file included in the folder.
   - Run the script (Lightning Bolt icon) to automatically create the `placement_db` database, tables, and insert all student records.
3. **Configure Database Credentials:** Open `app.py` and update the MySQL connection settings (username and password) to match your local MySQL configuration.
4. **Install Dependencies:** Open the terminal in the project directory and run the following command to install the required Python libraries:
   ```bash
   pip install -r requirements.txt
5. Run the Application: Start the Flask server by running:
   ```bash
   python app.py
6. Access the Portal: Open your web browser and go to http://127.0.0.1:5000 to view the dashboard.

Subject Details
Class : SE (COMP) Div A - 2025-2026

Subject : Mini Project-I (MP-1)

Project Type : Mini Project

Platform, Libraries and Frameworks used
Frontend: HTML5, Bootstrap 5, Chart.js (for analytics)

Backend: Python, Flask Framework

Database: MySQL, PyMySQL (Connector)

Dataset Used
Custom Generated Database: A normalized relational database (placement_db) containing 50+ records of realistic student placement data, including simulated LinkedIn profiles, packages, and recruiting companies.
References
-[Flask Documentation](https://flask.palletsprojects.com/)

-[MySQL Workbench User Guide](https://dev.mysql.com/doc/workbench/en/)

-[Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/getting-started/introduction/)
   
   
