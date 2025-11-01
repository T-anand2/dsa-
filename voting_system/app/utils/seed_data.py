from app import db
from app.models.user import User
from app.models.election import Election
from app.models.candidate import Candidate
from datetime import datetime, timedelta

def seed_initial_data():
    """Seed initial data for testing"""
    
    if User.query.filter_by(username='admin').first():
        return
    
    admin = User(
        username='admin',
        email='admin@voting.com',
        role='admin',
        is_verified=True
    )
    admin.set_password('admin123')
    db.session.add(admin)
    
    voter1 = User(
        username='john_doe',
        email='john@example.com',
        role='voter',
        is_verified=True
    )
    voter1.set_password('password123')
    db.session.add(voter1)
    
    voter2 = User(
        username='jane_smith',
        email='jane@example.com',
        role='voter',
        is_verified=True
    )
    voter2.set_password('password123')
    db.session.add(voter2)
    
    election = Election(
        title='Presidential Election 2025',
        description='Vote for the next president of the student council',
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=7),
        is_active=True
    )
    db.session.add(election)
    db.session.commit()
    
    candidates_data = [
        {'name': 'Alice Johnson', 'party': 'Progressive Party', 'description': 'Experienced leader with focus on education reform'},
        {'name': 'Bob Williams', 'party': 'Unity Party', 'description': 'Advocate for student welfare and campus improvements'},
        {'name': 'Carol Davis', 'party': 'Innovation Party', 'description': 'Tech-savvy candidate promoting digital transformation'},
    ]
    
    for candidate_data in candidates_data:
        candidate = Candidate(
            name=candidate_data['name'],
            party=candidate_data['party'],
            description=candidate_data['description'],
            election_id=election.id
        )
        db.session.add(candidate)
    
    db.session.commit()
    print("Initial data seeded successfully!")
