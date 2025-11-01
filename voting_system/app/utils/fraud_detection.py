import numpy as np
from sklearn.ensemble import IsolationForest
from datetime import datetime, timedelta
from app import db
from app.models.vote import Vote
from app.models.voting_pattern import VotingPattern

class FraudDetector:
    def __init__(self):
        self.model = IsolationForest(
            contamination=0.1,
            random_state=42,
            n_estimators=100
        )
        self.is_trained = False
    
    def extract_features(self, vote, pattern):
        """Extract features from vote and voting pattern for fraud detection"""
        features = []
        
        features.append(pattern.vote_time_hour if pattern.vote_time_hour else 12)
        features.append(pattern.time_spent_seconds if pattern.time_spent_seconds else 30)
        
        same_ip_votes = Vote.query.filter_by(
            ip_address=vote.ip_address,
            election_id=vote.election_id
        ).count()
        features.append(same_ip_votes)
        
        user_votes_count = Vote.query.filter_by(user_id=vote.user_id).count()
        features.append(user_votes_count)
        
        time_diff = 0
        last_vote = Vote.query.filter(
            Vote.user_id == vote.user_id,
            Vote.id != vote.id
        ).order_by(Vote.timestamp.desc()).first()
        
        if last_vote:
            time_diff = (vote.timestamp - last_vote.timestamp).total_seconds()
        features.append(time_diff)
        
        hour = vote.timestamp.hour
        is_unusual_hour = 1 if (hour < 6 or hour > 23) else 0
        features.append(is_unusual_hour)
        
        return np.array(features).reshape(1, -1)
    
    def train_model(self):
        """Train the fraud detection model on existing voting patterns"""
        patterns = VotingPattern.query.all()
        
        if len(patterns) < 10:
            return False
        
        features_list = []
        for pattern in patterns:
            vote = Vote.query.filter_by(
                user_id=pattern.user_id,
                election_id=pattern.election_id
            ).first()
            
            if vote:
                features = self.extract_features(vote, pattern)
                features_list.append(features.flatten())
        
        if len(features_list) >= 10:
            X = np.array(features_list)
            self.model.fit(X)
            self.is_trained = True
            return True
        
        return False
    
    def detect_fraud(self, vote, pattern):
        """Detect if a vote is potentially fraudulent"""
        features = self.extract_features(vote, pattern)
        
        if Vote.query.filter_by(
            user_id=vote.user_id,
            election_id=vote.election_id
        ).count() > 1:
            return True
        
        same_ip_count = Vote.query.filter_by(
            ip_address=vote.ip_address,
            election_id=vote.election_id
        ).count()
        
        if same_ip_count > 5:
            return True
        
        if pattern.time_spent_seconds and pattern.time_spent_seconds < 5:
            return True
        
        if self.is_trained or self.train_model():
            prediction = self.model.predict(features)
            anomaly_score = self.model.score_samples(features)[0]
            
            pattern.anomaly_score = float(anomaly_score)
            db.session.commit()
            
            if prediction[0] == -1:
                return True
        
        return False
    
    def get_fraud_statistics(self, election_id=None):
        """Get statistics about fraudulent votes"""
        query = Vote.query.filter_by(is_suspicious=True)
        
        if election_id:
            query = query.filter_by(election_id=election_id)
        
        suspicious_votes = query.count()
        total_votes = Vote.query.filter_by(election_id=election_id).count() if election_id else Vote.query.count()
        
        fraud_percentage = (suspicious_votes / total_votes * 100) if total_votes > 0 else 0
        
        return {
            'suspicious_votes': suspicious_votes,
            'total_votes': total_votes,
            'fraud_percentage': round(fraud_percentage, 2)
        }
