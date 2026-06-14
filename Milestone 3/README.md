# FareShare Ride-Sharing System

## Project Description

FareShare is an innovative ride-sharing and fare-sharing platform designed specifically for the Pakistani market, focusing initially on the Mianwali region. The system allows riders to book rides, enables fare-sharing between multiple passengers, provides SOS emergency alerts, and includes comprehensive driver verification by administrators. The platform operates on a cash-only payment model and includes three user roles: Riders, Drivers, and Administrators.

### Key Features

- **Rider Features:** Book rides, share fares, track rides in real-time, rate drivers, manage emergency contacts, trigger SOS alerts
- **Driver Features:** Go online/offline, receive ride requests, accept/decline rides, navigate to pickups/dropoffs, track earnings
- **Admin Features:** Verify driver documents, manage users, monitor active rides, view system analytics and reports
- **Safety Features:** SOS emergency alerts, emergency contact management, ride tracking, driver verification

---

## System Requirements

### Hardware Requirements

| Component | Minimum Requirement |
|-----------|---------------------|
| Processor | Dual-core 2.0 GHz |
| RAM | 4 GB |
| Storage | 500 MB free space |
| Display | 1366 x 768 resolution |

### Software Requirements

| Software | Version | Purpose |
|----------|---------|---------|
| Operating System | Windows 10/11, macOS, or Linux | Run the application |
| Python | 3.8 or higher | Application runtime |
| MySQL Server | 8.0 or higher | Database server |
| MySQL Workbench (optional) | 8.0 | Database management |

### Python Libraries Required

```
mysql-connector-python
tkinter (included with Python)
uuid (included with Python)
datetime (included with Python)
random (included with Python)
threading (included with Python)
```

---

## Installation Instructions

### Step 1: Install MySQL Server

1. Download MySQL Installer from [mysql.com](https://dev.mysql.com/downloads/installer/)
2. Run the installer and select "Developer Default" setup type
3. Follow the installation wizard
4. Set root password (remember this for later configuration)
5. Complete the installation

### Step 2: Install Python

1. Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **IMPORTANT:** Check "Add Python to PATH" during installation
4. Complete the installation

### Step 3: Install Required Python Library

Open Command Prompt (Windows) or Terminal (Mac/Linux) and run:

```bash
pip install mysql-connector-python
```

### Step 4: Create the Database

1. Open MySQL Command Line Client or MySQL Workbench
2. Login with your root password
3. Run the DDL script to create the database schema:

```sql
source path/to/dbDDL.sql;
```

Or manually execute the SQL commands from the `dbDDL.sql` file.

### Step 5: Load Sample Data

After creating the database structure, load the sample data:

```sql
source path/to/dbDML.sql;
```

### Step 6: Configure Database Connection

Open the `fareshare.py` file and update the database connection settings (around line 403):

```python
self.connection = mysql.connector.connect(
    host='localhost',
    database='fareshare_db',
    user='root',
    password='YOUR_MYSQL_PASSWORD_HERE',
    autocommit=False
)
```

---

## Running the Application

### Method 1: Command Line

Navigate to the project directory and run:

```bash
python fareshare.py
```

### Method 2: Double-click (Windows)

Simply double-click the `fareshare.py` file if Python is properly associated with `.py` files.

---

## Usage Instructions

### Login Credentials (Demo Accounts)

| Role | Phone Number | Password/Notes |
|------|--------------|----------------|
| **Rider** | +923001234501 | No password (OTP-based in real system, direct login in demo) |
| **Rider** | +923001234502 | No password required |
| **Driver** | +923011234501 | No password required |
| **Driver** | +923011234502 | No password required |
| **Admin** | +923021234501 | No password required |

### How to Use - Rider

1. **Login:** Select "Rider" role and enter a rider phone number (e.g., +923001234501)
2. **Book a Ride:**
   - Enter pickup and dropoff locations
   - Select vehicle type (Bike, Rickshaw, Mini, Sedan)
   - Toggle "Enable Fare Sharing" if desired
   - Select a driver from the available drivers list
   - Click "Book Ride Now"
3. **Track Ride:** Watch the animated ride progress with ETA and distance
4. **Complete Ride:** Pay cash to driver when ride completes
5. **Rate Driver:** Go to "My Rides" tab and rate completed rides
6. **Emergency:** Add emergency contacts in "Emergency" tab and use SOS button if needed

### How to Use - Driver

1. **Login:** Select "Driver" role and enter a driver phone number (e.g., +923011234501)
2. **Go Online:** Click the "Go Online" button to start receiving ride requests
3. **Accept Rides:**
   - View incoming requests in the "Ride Requests" tab
   - Click "Simulate" to test with demo requests
   - Click "Accept" to accept a ride request
   - Click "Decline" to reject
4. **Track Earnings:** View earnings dashboard in the "Earnings" tab
5. **Go Offline:** Click "Offline" button when done

### How to Use - Admin

1. **Login:** Select "Admin" role and enter admin phone number (e.g., +923021234501)
2. **Verify Drivers:**
   - Go to "Verifications" tab
   - Select pending driver verifications
   - Click "Approve" or "Reject"
3. **Manage Users:** Search and view all users in the "Users" tab
4. **Monitor Rides:** View active rides in the "Rides" tab
5. **View Reports:** Generate system reports in the "Reports" tab

---

## Code Structure

```
FareShare-Ride-Sharing-System/
│
├── fareshare.py          # Main application file (Python + Tkinter GUI)
├── dbDDL.sql             # Database schema creation script
├── dbDML.sql             # Sample data insertion script
├── Database Design Document - Template.docx  # Design documentation
├── FareShare Design Report.pdf               # Complete design report
├── FareShare SRS 2.0 (1).pdf                 # Software requirements spec
├── EERD.png              # Entity relationship diagram
├── Specialization.png    # Database schema diagram
└── README.md             # This file
```

### Key Files Explained

| File | Description |
|------|-------------|
| `fareshare.py` | Main Python application with complete GUI and database integration |
| `dbDDL.sql` | Contains CREATE TABLE statements, constraints, triggers, procedures, and views |
| `dbDML.sql` | Contains INSERT statements for sample data (20+ rows per table) |

### Application Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FareShare Application                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Rider GUI   │  │ Driver GUI  │  │ Admin GUI           │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
│         │                │                    │             │
│         └────────────────┼────────────────────┘             │
│                          │                                  │
│                  ┌───────▼───────┐                          │
│                  │ DatabaseManager│                         │
│                  │   (Python)     │                         │
│                  └───────┬───────┘                          │
└──────────────────────────┼──────────────────────────────────┘
                           │
                  ┌────────▼────────┐
                  │ MySQL Database  │
                  │ (fareshare_db)  │
                  └─────────────────┘
```

---

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'mysql'"

**Solution:** Install the MySQL connector:

```bash
pip install mysql-connector-python
```

### Problem: Database connection error

**Solution:**
1. Ensure MySQL server is running
2. Check your MySQL password in the `fareshare.py` connection settings
3. Verify the database 'fareshare_db' exists

### Problem: "Access denied for user 'root'"

**Solution:** Update the password in the connection string to match your MySQL root password

### Problem: Tables not found when running application

**Solution:** Run the DDL script first to create all tables:

```bash
mysql -u root -p < dbDDL.sql
mysql -u root -p < dbDML.sql
```

### Problem: "Duplicate Entry" error when approving drivers

**Solution:** This is fixed in the latest version. The system now updates existing records instead of creating new ones.

### Problem: Foreign key constraint error when accepting simulated rides

**Solution:** This is fixed in the latest version. Simulated rides no longer attempt database insertion.

---

## Database Schema Overview

The database contains 12 normalized tables (3NF):

| Table | Description |
|-------|-------------|
| User | Supertype for all users (Rider, Driver, Admin) |
| Rider | Rider-specific attributes |
| Driver | Driver-specific attributes |
| Admin | Admin-specific attributes |
| Vehicle | Driver's vehicle information |
| Ride | Ride transaction records |
| RideParticipant | Associative table for ride sharing |
| Payment | Cash payment records |
| DriverVerification | Driver document verification logs |
| SOSAlert | Emergency alert records |
| EmergencyContact | User emergency contacts (max 3) |
| Rating | User ratings and feedback (max 2 per ride) |

---

## Recent Updates

### Version 2.0 - Latest Features

✅ **Manual Ride Request Management**
- Drivers can now accept/decline rides directly from the table
- New "Accept" and "Decline" buttons in driver dashboard
- No longer dependent only on popup notifications

✅ **Bug Fixes**
- Fixed "Duplicate Entry" error in driver verification
- Fixed foreign key constraint error for simulated rides
- Removed hardcoded database password for security

✅ **UI Improvements**
- Compact button sizes (120px width)
- Better spacing and layout
- Improved instructions and feedback
- Cleaner, more intuitive interface

✅ **Code Optimization**
- Reduced code by ~150 lines
- Consolidated repetitive functions
- Better error handling
- Improved performance

---

## Project Team

| Name | Roll Number | Role |
|------|-------------|------|
| Muhammad Naveed | NUM-BSCS-2024-54 | Group Lead |
| Munawar Ali | NUM-BSCS-2024-60 | Group Member |
| Areeba Tahir | NUM-BSCS-2024-15 | Group Member |

**Supervisor:** Ms. Asiya Batool  
**Institution:** Namal University, Mianwali  
**Course:** Database Systems (CSC-271)

---

## Support

For issues or questions regarding this project, please contact the project team through the GitHub repository.

---

## License

This project was developed for academic purposes as part of the Database Systems course at Namal University, Mianwali.

---

## Quick Start Guide

1. Install Python 3.8+
2. Install MySQL Server 8.0+
3. Run: `pip install mysql-connector-python`
4. Import `dbDDL.sql` and `dbDML.sql` into MySQL
5. Update database password in `fareshare.py` (line 403)
6. Run: `python fareshare.py`
7. Login with demo credentials and explore!

**Happy Ride Sharing! 🚗**
