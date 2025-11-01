# Quick Setup Guide - AI Voting System

## 🚀 Quick Start (5 Minutes)

### Step 1: Navigate to Project Directory
```bash
cd voting_system
```

### Step 2: Create Virtual Environment
**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python run.py
```

### Step 5: Access the Application
Open your browser and go to: **http://localhost:5000**

## 👤 Login Credentials

### Admin Dashboard
- Username: `admin`
- Password: `admin123`
- Access: Full system control, create elections, view analytics

### Voter Account 1
- Username: `john_doe`
- Password: `password123`

### Voter Account 2
- Username: `jane_smith`
- Password: `password123`

## 📋 What's Included

✅ User authentication (login/signup)
✅ Admin dashboard with analytics
✅ Voter dashboard
✅ Election creation and management
✅ Candidate management
✅ Secure voting system (one vote per user)
✅ AI-based fraud detection
✅ Real-time result visualization with Chart.js
✅ Suspicious vote monitoring
✅ Responsive Bootstrap UI

## 🎯 Testing the System

### As a Voter:
1. Login with voter credentials
2. View active elections
3. Cast your vote
4. View results after election ends

### As an Admin:
1. Login with admin credentials
2. View dashboard statistics
3. Create a new election
4. Add candidates
5. Monitor voting activity
6. Check suspicious votes
7. View results with charts

## 🤖 AI Fraud Detection Features

The system automatically detects:
- Duplicate voting attempts
- Multiple votes from same IP
- Unusually fast voting (< 5 seconds)
- Voting during unusual hours
- Anomalous behavioral patterns

## 🔧 Troubleshooting

### Issue: Port 5000 already in use
**Solution:** Change port in `run.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: Module not found
**Solution:** Reinstall dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

### Issue: Database error
**Solution:** Delete database and restart:
```bash
# Windows
del instance\voting_system.db

# macOS/Linux
rm instance/voting_system.db

# Then restart
python run.py
```

## 📁 Important Files

- `run.py` - Start the application
- `app/__init__.py` - Flask app configuration
- `app/models/` - Database models
- `app/routes/` - Application routes
- `app/templates/` - HTML templates
- `app/static/` - CSS, JS, images
- `requirements.txt` - Python dependencies

## 🌐 Switching to MySQL

1. Install MySQL connector:
```bash
pip install pymysql
```

2. Update `app/__init__.py`:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/voting_db'
```

3. Create database:
```sql
CREATE DATABASE voting_db;
```

## 📊 Database Schema

- **users**: User accounts (voters and admins)
- **elections**: Election information
- **candidates**: Candidates for each election
- **votes**: Cast votes (anonymous)
- **voting_patterns**: AI analysis data

## 🎨 Customization

### Change Theme Colors
Edit `app/static/css/style.css`:
```css
:root {
    --primary-color: #0d6efd;
    --success-color: #198754;
    --danger-color: #dc3545;
}
```

### Add New Admin
Run Python shell:
```python
from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    admin = User(username='newadmin', email='admin@example.com', role='admin')
    admin.set_password('password')
    db.session.add(admin)
    db.session.commit()
```

## 📈 Production Deployment

1. Set `debug=False` in `run.py`
2. Use production server (Gunicorn):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```
3. Use PostgreSQL/MySQL instead of SQLite
4. Set strong SECRET_KEY
5. Enable HTTPS
6. Configure firewall

## 💡 Tips

- The system seeds demo data automatically on first run
- One demo election is created with 3 candidates
- AI model trains automatically after 10+ votes
- All passwords are securely hashed
- Sessions are managed securely with Flask-Login

## 📞 Need Help?

Check the main README.md for detailed documentation.

---

**Happy Voting! 🗳️**
