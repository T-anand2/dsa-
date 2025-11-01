from app import db

class Candidate(db.Model):
    __tablename__ = 'candidates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    party = db.Column(db.String(100))
    description = db.Column(db.Text)
    photo_url = db.Column(db.String(255))
    election_id = db.Column(db.Integer, db.ForeignKey('elections.id'), nullable=False)
    
    votes = db.relationship('Vote', backref='candidate', lazy=True, cascade='all, delete-orphan')
    
    def get_vote_count(self):
        return len(self.votes)
    
    def __repr__(self):
        return f'<Candidate {self.name}>'
