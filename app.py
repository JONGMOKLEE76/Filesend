import re
from flask import Flask, render_template, redirect, url_for, request, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users = [
    {
        'username': 'admin',
        'password': 'admin123',  # 실제 서비스에서는 암호화 필요
        'company': 'LG Electronics',
        'job': 'Administrator',
        'email': 'admin@example.com',
        'avatar': 'avatar1.png',
        'approved': True,
        'is_admin': True
    }
]

EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'
AVATAR_LIST = [f'avatar{i}.png' for i in range(1, 21)]  # avatar1.png ~ avatar20.png

@app.route('/')
def index():
    print('session:', dict(session))
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out.')
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    page = int(request.args.get('page', 1))
    avatars_per_page = 5
    start = (page - 1) * avatars_per_page
    end = start + avatars_per_page
    avatars = AVATAR_LIST[start:end]
    total_pages = (len(AVATAR_LIST) + avatars_per_page - 1) // avatars_per_page

    if request.method == 'POST':
        username = request.form.get('username') or request.args.get('username', '')
        password = request.form.get('password') or request.args.get('password', '')
        company = request.form.get('company') or request.args.get('company', '')
        job = request.form.get('job') or request.args.get('job', '')
        email = request.form.get('email') or request.args.get('email', '')
        avatar = request.form.get('avatar', avatars[0])

        if any(u['username'] == username for u in users):
            flash('Username already exists.')
            return render_template('signup.html', avatars=avatars, page=page, total_pages=total_pages)
        if len(password) < 4:
            flash('Password must be at least 4 characters.')
            return render_template('signup.html', avatars=avatars, page=page, total_pages=total_pages)
        if not re.match(EMAIL_REGEX, email):
            flash('Invalid email address format.')
            return render_template('signup.html', avatars=avatars, page=page, total_pages=total_pages)

        users.append({
            'username': username,
            'password': password,
            'company': company,
            'job': job,
            'email': email,
            'avatar': avatar,
            'approved': False  # 가입 시 미승인 상태
        })
        flash('Sign up successful!')
        return redirect(url_for('login'))
    return render_template('signup.html', avatars=avatars, page=page, total_pages=total_pages)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # approved가 True인 유저만 로그인 허용
        user = next((u for u in users if u['username'] == username and u['password'] == password and u.get('approved', False)), None)
        if user:
            session['username'] = username
            session['is_admin'] = user.get('is_admin', False)
            flash('Login successful!')
            return redirect(url_for('index'))
        else:
            flash('Invalid username, password, or not approved yet.')
    return render_template('login.html')

@app.route('/admin/users')
def admin_users():
    return render_template('admin_users.html', users=users)

@app.route('/admin/approve/<username>')
def approve_user(username):
    for user in users:
        if user['username'] == username:
            user['approved'] = True
            flash(f'User {username} approved.')
            break
    return redirect(url_for('admin_users'))

@app.route('/admin/reject/<username>')
def reject_user(username):
    global users
    users = [user for user in users if user['username'] != username]
    flash(f'User {username} rejected and removed.')
    return redirect(url_for('admin_users'))

if __name__ == '__main__':
    app.run()