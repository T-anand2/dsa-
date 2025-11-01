from app import db
from datetime import datetime

class VotingPattern(db.Model):
    __tablename__ = 'voting_patterns'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    election_id = db.Column(db.Integer, db.ForeignKey('elections.id'), nullable=False)
    vote_time_hour = db.Column(db.Integer)
    time_spent_seconds = db.Column(db.Integer)
    ip_address = db.Column(db.String(45))
    device_fingerprint = db.Column(db.String(255))
    anomaly_score = db.Column(db.Float, default=0.0)
    is_flagged = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<VotingPattern user_id={self.user_id} election_id={self.election_id}>'
