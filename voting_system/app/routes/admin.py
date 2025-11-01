from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models.user import User
from app.models.election import Election
from app.models.candidate import Candidate
from app.models.vote import Vote
from app.models.voting_pattern import VotingPattern
from datetime import datetime

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('You need admin privileges to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_users = User.query.filter_by(role='voter').count()
    total_elections = Election.query.count()
    active_elections = Election.query.filter_by(is_active=True).count()
    total_votes = Vote.query.count()
    suspicious_votes = Vote.query.filter_by(is_suspicious=True).count()
    
    elections = Election.query.order_by(Election.created_at.desc()).all()
    recent_votes = Vote.query.order_by(Vote.timestamp.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_elections=total_elections,
                         active_elections=active_elections,
                         total_votes=total_votes,
                         suspicious_votes=suspicious_votes,
                         elections=elections,
                         recent_votes=recent_votes)

@bp.route('/elections')
@login_required
@admin_required
def elections():
    elections = Election.query.order_by(Election.created_at.desc()).all()
    return render_template('admin/elections.html', elections=elections)

@bp.route('/election/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_election():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%dT%H:%M')
        end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%dT%H:%M')
        
        if end_date <= start_date:
            flash('End date must be after start date.', 'danger')
            return redirect(url_for('admin.create_election'))
        
        election = Election(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date
        )
        
        db.session.add(election)
        db.session.commit()
        
        flash('Election created successfully!', 'success')
        return redirect(url_for('admin.add_candidates', election_id=election.id))
    
    return render_template('admin/create_election.html')

@bp.route('/election/<int:election_id>/candidates', methods=['GET', 'POST'])
@login_required
@admin_required
def add_candidates(election_id):
    election = Election.query.get_or_404(election_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        party = request.form.get('party')
        description = request.form.get('description')
        
        candidate = Candidate(
            name=name,
            party=party,
            description=description,
            election_id=election_id
        )
        
        db.session.add(candidate)
        db.session.commit()
        
        flash(f'Candidate {name} added successfully!', 'success')
        return redirect(url_for('admin.add_candidates', election_id=election_id))
    
    candidates = Candidate.query.filter_by(election_id=election_id).all()
    return render_template('admin/add_candidates.html', election=election, candidates=candidates)

@bp.route('/election/<int:election_id>/results')
@login_required
@admin_required
def election_results(election_id):
    election = Election.query.get_or_404(election_id)
    results = election.get_results()
    total_votes = election.get_total_votes()
    
    return render_template('admin/results.html', 
                         election=election, 
                         results=results,
                         total_votes=total_votes)

@bp.route('/election/<int:election_id>/results/data')
@login_required
@admin_required
def election_results_data(election_id):
    election = Election.query.get_or_404(election_id)
    results = election.get_results()
    
    data = {
        'labels': [r.name for r in results],
        'votes': [r.vote_count for r in results],
        'parties': [r.party for r in results]
    }
    
    return jsonify(data)

@bp.route('/users')
@login_required
@admin_required
def users():
    users = User.query.filter_by(role='voter').order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@bp.route('/suspicious-votes')
@login_required
@admin_required
def suspicious_votes():
    suspicious = Vote.query.filter_by(is_suspicious=True).order_by(Vote.timestamp.desc()).all()
    patterns = VotingPattern.query.filter_by(is_flagged=True).order_by(VotingPattern.created_at.desc()).all()
    
    return render_template('admin/suspicious_votes.html', 
                         suspicious_votes=suspicious,
                         patterns=patterns)

@bp.route('/election/<int:election_id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_election(election_id):
    election = Election.query.get_or_404(election_id)
    election.is_active = not election.is_active
    db.session.commit()
    
    status = 'activated' if election.is_active else 'deactivated'
    flash(f'Election {election.title} has been {status}.', 'success')
    return redirect(url_for('admin.elections'))
