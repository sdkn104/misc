from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app.models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # バリデーション
        if not username or not email or not password:
            flash('全ての項目を入力してください。')
            return redirect(url_for('auth.register'))
        if len(password) < 8:
            flash('パスワードは8文字以上で入力してください。')
            return redirect(url_for('auth.register'))
        if '@' not in email or '.' not in email:
            flash('メールアドレスの形式が正しくありません。')
            return redirect(url_for('auth.register'))
        if User.query.filter_by(email=email).first():
            flash('このメールアドレスは既に登録されています。')
            return redirect(url_for('auth.register'))
        if User.query.filter_by(username=username).first():
            flash('このユーザー名は既に使用されています。')
            return redirect(url_for('auth.register'))

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        flash('登録が完了しました。ログインしてください。')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('ログイン成功')
            return redirect(url_for('index'))
        else:
            flash('メールアドレスまたはパスワードが間違っています。')
            return redirect(url_for('auth.login'))
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ログアウトしました。')
    return redirect(url_for('index'))
