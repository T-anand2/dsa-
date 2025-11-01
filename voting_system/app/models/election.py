from app import db
from datetime import datetime

class Election(db.Model):
    __tablename__ = 'elections'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    candidates = db.relationship('Candidate', backref='election', lazy=True, cascade='all, delete-orphan')
    votes = db.relationship('Vote', backref='election', lazy=True, cascade='all, delete-orphan')
    
    def is_ongoing(self):
        now = datetime.utcnow()
        return self.start_date <= now <= self.end_date and self.is_active
    
    def has_started(self):
        return datetime.utcnow() >= self.start_date
    
    def has_ended(self):
        return datetime.utcnow() > self.end_date
    
    def get_total_votes(self):
        return len(self.votes)
    
    def get_results(self):
        from app.models.candidate import Candidate
        from app.models.vote import Vote
        from sqlalchemy import func
        
        results = db.session.query(
            Candidate.id,
            Candidate.name,
            Candidate.party,
            func.count(Vote.id).label('vote_count')
        ).outerjoin(Vote, (Vote.candidate_id == Candidate.id) & (Vote.election_id == self.id)
        ).filter(Candidate.election_id == self.id
        ).group_by(Candidate.id).all()
        
        return results
    
    def __repr__(self):
        return f'<Election {self.title}>'
