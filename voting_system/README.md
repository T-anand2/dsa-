# AI-Based Online Voting System

A complete, secure online voting system built with Python Flask, featuring AI-powered fraud detection, user authentication, and real-time result visualization.

## 🌟 Features

### Core Functionality
- **User Authentication**: Secure login/signup system for voters and administrators
- **Role-Based Access**: Separate dashboards for voters and admins
- **Secure Voting**: Each voter can vote only once per election
- **Real-Time Results**: Live vote counting and visualization with Chart.js
- **Election Management**: Admins can create elections and add candidates

### AI-Powered Security
- **Fraud Detection**: Machine learning-based anomaly detection using Isolation Forest
- **Pattern Analysis**: Monitors voting behavior, timing, and IP addresses
- **Suspicious Activity Flagging**: Automatic detection of:
  - Duplicate voting attempts
  - Multiple votes from same IP
  - Unusually fast voting behavior
  - Voting during unusual hours
  - Anomalous behavioral patterns

### Admin Features
- Create and manage elections
- Add candidates to elections
- View real-time voting statistics
- Monitor suspicious voting activity
- View detailed voter information
- Visualize results with interactive charts

### Voter Features
- View active, upcoming, and past elections
- Cast votes securely
- View election results after completion
- User-friendly interface with Bootstrap 5

## 📁 Project Structure

```
voting_system/
├── app/
│   ├── __init__.py                 # Flask app initialization
│   ├── models/                     # Database models
│   │   ├── __init__.py
│   │   ├── user.py                 # User model
│   │   ├── election.py             # Election model
│   │   ├── candidate.py            # Candidate model
│   │   ├── vote.py                 # Vote model
│   │   └── voting_pattern.py       # Voting pattern for AI
│   ├── routes/                     # Application routes
│   │   ├── __init__.py
│   │   ├── auth.py                 # Authentication routes
│   │   ├── voter.py                # Voter routes
│   │   └── admin.py                # Admin routes
│   ├── utils/                      # Utility functions
│   │   ├── __init__.py
│   │   ├── fraud_detection.py      # AI fraud detection
│   │   └── seed_data.py            # Initial data seeding
│   ├── templates/                  # HTML templates
│   │   ├── base.html               # Base template
│   │   ├── auth/                   # Authentication templates
│   │   │   ├── login.html
│   │   │   └── signup.html
│   │   ├── voter/                  # Voter templates
│   │   │   ├── dashboard.html
│   │   │   ├── vote.html
│   │   │   └── results.html
│   │   └── admin/                  # Admin templates
│   │       ├── dashboard.html
│   │       ├── elections.html
│   │       ├── create_election.html
│   │       ├── add_candidates.html
│   │       ├── results.html
│   │       ├── users.html
│   │       └── suspicious_votes.html
│   └── static/                     # Static files
│       ├── css/
│       │   └── style.css           # Custom styles
│       ├── js/
│       │   └── main.js             # Custom JavaScript
│       └── images/                 # Image assets
├── instance/                       # Instance folder (database)
├── migrations/                     # Database migrations
├── requirements.txt                # Python dependencies
├── run.py                          # Application entry point
└── README.md                       # This file
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone or Extract the Project
```bash
cd voting_system
```

### Step 2: Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database
The database will be automatically created when you first run the application. Initial demo data will be seeded automatically.

### Step 5: Run the Application
```bash
python run.py
```

The application will be available at: `http://localhost:5000`

## 👤 Demo Credentials

### Admin Account
- **Username**: `admin`
- **Password**: `admin123`

### Voter Accounts
- **Username**: `john_doe` | **Password**: `password123`
- **Username**: `jane_smith` | **Password**: `password123`

## 🔧 Configuration

### Database Configuration
The application uses SQLite by default. To change the database:

Edit `app/__init__.py`:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voting_system.db'
# For MySQL:
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/voting_db'
```

### Secret Key
For production, change the secret key in `app/__init__.py`:
```python
app.config['SECRET_KEY'] = 'your-secure-secret-key-here'
```

## 🤖 AI Fraud Detection

The system uses **Isolation Forest** algorithm for anomaly detection with the following features:

### Detection Features
1. **Vote Time Hour**: Hour of the day when vote was cast
2. **Time Spent**: Time spent on voting page
3. **IP Address Analysis**: Multiple votes from same IP
4. **User Vote Count**: Total votes by user
5. **Time Between Votes**: Time gap between consecutive votes
6. **Unusual Hours**: Voting during late night hours

### How It Works
1. System collects voting patterns for each vote
2. AI model analyzes patterns using 6 behavioral features
3. Anomaly score is calculated for each vote
4. Suspicious votes are automatically flagged
5. Admins can review flagged votes in the dashboard

### Model Training
- The model trains automatically as more votes are collected
- Requires minimum 10 votes for initial training
- Continuously adapts to new voting patterns
- Uses contamination rate of 10% for anomaly detection

## 📊 Database Schema

### Users Table
- id, username, email, password_hash, role, is_verified, created_at, last_login

### Elections Table
- id, title, description, start_date, end_date, is_active, created_at

### Candidates Table
- id, name, party, description, photo_url, election_id

### Votes Table
- id, user_id, candidate_id, election_id, timestamp, ip_address, user_agent, is_suspicious

### Voting Patterns Table
- id, user_id, election_id, vote_time_hour, time_spent_seconds, ip_address, device_fingerprint, anomaly_score, is_flagged, created_at

## 🎨 Technologies Used

### Backend
- **Flask 3.0.0**: Web framework
- **Flask-SQLAlchemy**: ORM for database
- **Flask-Login**: User session management
- **Werkzeug**: Password hashing
- **scikit-learn**: Machine learning for fraud detection
- **NumPy & Pandas**: Data processing

### Frontend
- **Bootstrap 5.3**: Responsive UI framework
- **Bootstrap Icons**: Icon library
- **Chart.js 4.4**: Data visualization
- **Vanilla JavaScript**: Client-side interactivity

### Database
- **SQLite**: Default database (easily switchable to MySQL/PostgreSQL)

## 🔒 Security Features

1. **Password Hashing**: Werkzeug's secure password hashing
2. **Session Management**: Flask-Login for secure sessions
3. **CSRF Protection**: Built-in Flask-WTF protection
4. **SQL Injection Prevention**: SQLAlchemy ORM
5. **One Vote Per User**: Database constraints
6. **AI Fraud Detection**: Real-time anomaly detection
7. **IP Tracking**: Monitor voting sources
8. **Role-Based Access**: Admin and voter separation

## 📈 Usage Guide

### For Voters
1. Sign up or log in with credentials
2. View active elections on dashboard
3. Click "Cast Your Vote" on an active election
4. Select a candidate and submit
5. View results after election ends

### For Administrators
1. Log in with admin credentials
2. Create new elections with start/end dates
3. Add candidates to elections
4. Monitor voting activity in real-time
5. View suspicious votes and patterns
6. Analyze results with interactive charts
7. Manage voter accounts

## 🐛 Troubleshooting

### Database Issues
```bash
# Delete the database and restart
rm instance/voting_system.db
python run.py
```

### Port Already in Use
```python
# Change port in run.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 🚀 Deployment

### For Production
1. Set `debug=False` in `run.py`
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Use PostgreSQL or MySQL instead of SQLite
4. Set strong SECRET_KEY
5. Enable HTTPS
6. Configure proper firewall rules

### Example with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## 📝 License

This project is created for educational purposes. Feel free to use and modify as needed.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## 📧 Support

For issues or questions, please open an issue in the repository.

## ✨ Future Enhancements

- Email verification for voters
- Two-factor authentication
- Blockchain integration for vote immutability
- Mobile app version
- Advanced analytics dashboard
- Multi-language support
- Biometric authentication
- Live election streaming

---

**Built with ❤️ using Flask, Bootstrap, and AI**
