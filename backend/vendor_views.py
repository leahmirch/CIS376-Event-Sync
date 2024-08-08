# vendor_views.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from backend.models import db, Vendor, Event
from backend.utils import create_notification

vendor_bp = Blueprint('vendor', __name__)

@vendor_bp.route('/vendors')
@login_required
def vendor_list():
    vendors = Vendor.query.all()
    return render_template('vendor_list.html', vendors=vendors)

@vendor_bp.route('/vendor/new', methods=['GET', 'POST'])
@login_required
def new_vendor():
    if request.method == 'POST':
        name = request.form['name']
        contact_info = request.form['contact_info']
        contract_details = request.form['contract_details']
        
        new_vendor = Vendor(name=name, contact_info=contact_info, contract_details=contract_details)
        db.session.add(new_vendor)
        db.session.commit()

        create_notification(current_user.id, f"You have added a new vendor: {name}")
        
        flash('Vendor added successfully!', 'success')
        return redirect(url_for('vendor.vendor_list'))
    
    return render_template('new_vendor.html')

@vendor_bp.route('/vendor/<int:vendor_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_vendor(vendor_id):
    vendor = Vendor.query.get_or_404(vendor_id)
    if request.method == 'POST':
        vendor.name = request.form['name']
        vendor.contact_info = request.form['contact_info']
        vendor.contract_details = request.form['contract_details']
        
        db.session.commit()

        create_notification(current_user.id, f"You have edited the vendor: {vendor.name}")

        flash('Vendor updated successfully!', 'success')
        return redirect(url_for('vendor.vendor_list'))
    
    return render_template('edit_vendor.html', vendor=vendor)

@vendor_bp.route('/vendor/<int:vendor_id>/delete', methods=['POST'])
@login_required
def delete_vendor(vendor_id):
    vendor = Vendor.query.get_or_404(vendor_id)
    db.session.delete(vendor)
    db.session.commit()

    create_notification(current_user.id, f"You have deleted the vendor: {vendor.name}")

    flash('Vendor deleted successfully!', 'success')
    return redirect(url_for('vendor.vendor_list'))

def setup_vendor_routes(app):
    app.register_blueprint(vendor_bp)
