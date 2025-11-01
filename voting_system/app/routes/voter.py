from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.election import Election
from app.models.candidate import Candidate
from app.models.vote import Vote
from app.models.voting_pattern import VotingPattern
from app.utils.fraud_detection import FraudDetector
from datetime import datetime

bp = Blueprint('voter', __name__, url_prefix='/voter')

@bp.route('/')
@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    
    elections = Election.query.filter_by(is_active=True).all()
    ongoing_elections = [e for e in elections if e.is_ongoing()]
    upcoming_elections = [e for e in elections if not e.has_started()]
    past_elections = [e for e in elections if e.has_ended()]
    
    return render_template('voter/dashboard.html', 
                         ongoing_elections=ongoing_elections,
                         upcoming_elections=upcoming_elections,
                         past_elections=past_elections)

@bp.route('/election/<int:election_id>')
@login_required
def view_election(election_id):
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    
    election = Election.query.get_or_404(election_id)
    
    if not election.is_ongoing():
        flash('This election is not currently active.', 'warning')
        return redirect(url_for('voter.dashboard'))
    
    if current_user.has_voted(election_id):
        flash('You have already voted in this election.', 'info')
        return redirect(url_for('voter.dashboard'))
    
    candidates = Candidate.query.filter_by(election_id=election_id).all()
    
    return render_template('voter/vote.html', election=election, candidates=candidates)

@bp.route('/vote/<int:election_id>', methods=['POST'])
@login_required
def cast_vote(election_id):
    if current_user.is_admin():
        flash('Admins cannot vote.', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    election = Election.query.get_or_404(election_id)
    
    if not election.is_ongoing():
        flash('This election is not currently active.', 'danger')
        return redirect(url_for('voter.dashboard'))
    
    if current_user.has_voted(election_id):
        flash('You have already voted in this election.', 'danger')
        return redirect(url_for('voter.dashboard'))
    
    candidate_id = request.form.get('candidate_id')
    if not candidate_id:
        flash('Please select a candidate.', 'danger')
        return redirect(url_for('voter.view_election', election_id=election_id))
    
    candidate = Candidate.query.get_or_404(candidate_id)
    
    if candidate.election_id != election_id:
        flash('Invalid candidate selection.', 'danger')
        return redirect(url_for('voter.dashboard'))
    
    vote = Vote(
        user_id=current_user.id,
        candidate_id=candidate_id,
        election_id=election_id,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent', '')[:255]
    )
    
    voting_pattern = VotingPattern(
        user_id=current_user.id,
        election_id=election_id,
        vote_time_hour=datetime.utcnow().hour,
        time_spent_seconds=request.form.get('time_spent', 0),
        ip_address=request.remote_addr,
        device_fingerprint=request.headers.get('User-Agent', '')[:255]
    )
    
    db.session.add(vote)
    db.session.add(voting_pattern)
    db.session.commit()
    
    fraud_detector = FraudDetector()
    is_suspicious = fraud_detector.detect_fraud(vote, voting_pattern)
    
    if is_suspicious:
        vote.is_suspicious = True
        voting_pattern.is_flagged = True
        db.session.commit()
    
    flash('Your vote has been recorded successfully!', 'success')
    return redirect(url_for('voter.dashboard'))

@bp.route('/results/<int:election_id>')
@login_required
def view_results(election_id):
    election = Election.query.get_or_404(election_id)
    
    if not election.has_ended():
        flash('Results will be available after the election ends.', 'info')
        return redirect(url_for('voter.dashboard'))
    
    results = election.get_results()
    total_votes = election.get_total_votes()
    
    return render_template('voter/results.html', 
                         election=election, 
                         results=results,
                         total_votes=total_votes)
