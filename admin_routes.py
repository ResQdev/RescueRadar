from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password) and user.username == "admin":
            session['user_id'] = user.id
            session['is_admin'] = True
            return redirect(url_for('admin.admin_dashboard'))
        else:
            return render_template('admin_login.html', error="❌ Ungültige Admin-Zugangsdaten")

    return render_template('admin_login.html', error=None)

@admin_bp.route('/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('index'))

@admin_bp.route('/')
def admin_dashboard():
    if not session.get("is_admin"):
        return redirect(url_for("index"))
    users = User.query.all()
    return render_template("admin.html", users=users)

@admin_bp.route('/create', methods=['GET', 'POST'])
def create_user():
    if not session.get("is_admin"):
        return redirect(url_for("index"))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        vehicle_id = request.form['vehicle_id']

        new_user = User(username=username, vehicle_id=vehicle_id)
        new_user.password = password
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('admin.admin_dashboard'))

    return render_template('create_user.html')

@admin_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if not session.get("is_admin"):
        return redirect(url_for("index"))

    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.username = request.form['username']
        user.vehicle_id = request.form['vehicle_id']
        password = request.form.get('password')
        if password:
            user.password = password
        db.session.commit()
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('edit_user.html', user=user)

@admin_bp.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if not session.get("is_admin"):
        return redirect(url_for("index"))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.admin_dashboard'))