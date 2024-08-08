# community_views.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from backend.models import db, Community, CommunityMessage, User
from backend.utils import create_notification

community_bp = Blueprint('community', __name__)

@community_bp.route('/community')
@login_required
def index():
    communities = Community.query.all()
    user_communities = current_user.communities
    return render_template('community/index.html', communities=communities, user_communities=user_communities)

@community_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        community = Community(name=name, creator_id=current_user.id)
        community.members.append(current_user)
        db.session.add(community)
        db.session.commit()

        create_notification(current_user.id, f"You have created a new community: {name}")

        flash('Community created successfully!', 'success')
        return redirect(url_for('community.index'))
    return render_template('community/create.html')

@community_bp.route('/<int:community_id>')
@login_required
def view_community(community_id):
    community = Community.query.get_or_404(community_id)
    members = community.members
    if community.creator not in members:
        members.append(community.creator)
    messages = CommunityMessage.query.filter_by(community_id=community_id).order_by(CommunityMessage.timestamp).all()
    return render_template('community/community.html', community=community, members=members, messages=messages)

@community_bp.route('/<int:community_id>/join')
@login_required
def join(community_id):
    community = Community.query.get_or_404(community_id)
    if current_user not in community.members:
        community.members.append(current_user)
        db.session.commit()
        create_notification(current_user.id, f"You have joined the community: {community.name}")
        flash('You have joined the community.', 'success')
    else:
        flash('You are already a member of this community.', 'info')
    return redirect(url_for('community.view_community', community_id=community_id))

@community_bp.route('/<int:community_id>/message', methods=['POST'])
@login_required
def post_message(community_id):
    community = Community.query.get_or_404(community_id)
    if current_user not in community.members:
        flash('You do not have access to this community.', 'danger')
        return redirect(url_for('community.index'))
    message_text = request.form['message']
    message = CommunityMessage(community_id=community_id, user_id=current_user.id, message=message_text)
    db.session.add(message)
    db.session.commit()

    # Notify community members
    for member in community.members:
        if member.id != current_user.id:
            create_notification(member.id, f"New message in community {community.name}")

    return redirect(url_for('community.view_community', community_id=community_id))

@community_bp.route('/<int:community_id>/delete', methods=['POST'])
@login_required
def delete(community_id):
    community = Community.query.get_or_404(community_id)
    if community.creator_id != current_user.id:
        flash('You do not have permission to delete this community.', 'danger')
        return redirect(url_for('community.view_community', community_id=community_id))
    db.session.delete(community)
    db.session.commit()

    create_notification(community.creator_id, f"The community {community.name} has been deleted")

    flash('Community deleted successfully!', 'success')
    return redirect(url_for('main.dashboard'))

def setup_community_routes(app):
    app.register_blueprint(community_bp, url_prefix='/community')
