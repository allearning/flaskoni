from flask import Flask, render_template, request, redirect, url_for, get_flashed_messages, flash, make_response, session
import json
# Это уже нам знакомое callable WSGI-приложение
app = Flask(__name__)
Flask.secret_key = "d8ja"
USERS_FILE = 'package/data/users.txt'


def load_users():
    users = json.loads(request.cookies.get('users', json.dumps({})))
    print(users)
    return users


def append_user(name, email, response):
    users = load_users()
    users[len(users)] = {
        'name': name,
        'email': email,
        'id': str(len(users))
    }
    response.set_cookie('users', json.dumps(users))


def find_user(user_id, users):
    user = users[user_id]
    return user


def update_user(user, response):
    users = load_users()
    users[user['id']] = user
    response.set_cookie('users', json.dumps(users))


def delete_user_pers(user, response):
    users = load_users()
    del(users[user['id']])
    response.set_cookie('users', json.dumps(users))


def filter_users(part, data):
    if part is None:
        return data
    result = {k: v for (k,v) in data.items() if part in v['name']}
    return result


def validate(user, users=None):
    errors = {}
    if len(user['name']) <= 4:
        errors['name'] = "Nickname must be grater than 4 characters"
    if '@' not in user['email'] and '.' not in user['email']:
        errors['email'] = "Wrong e-mail"
    return errors


@app.route('/')
def hello_world():
    return '<a href="/users">Users</a>'


@app.get('/users')
def get_users():
    cred = session.get('username', None)
    users = load_users()
    messages = get_flashed_messages(with_categories=True)
    search_text = request.args.get('term', default='')
    return render_template(
        'users/index.html',
        search=search_text,
        messages=messages,
        credentails=cred,
        users=filter_users(search_text, users).values()
    )


@app.get('/users/new')
def get_new_user():
    user = {
        'name': '',
        'email': '',
        'id': '',
    }
    errors = {}
    return render_template('users/new.html', errors=errors, user=user)


@app.post('/users')
def post_users():
    users = load_users()
    id_ = len(users)
    user = {
        'name': request.form.get('nick'),
        'email': request.form.get('email'),
        'id': id_
    }
    errors = validate(user, users)
    if errors:
        return render_template('users/new.html', errors=errors, user=user), 422
    flash(f"User '{user['name']}' was added succesfully")
    response = make_response(redirect(url_for('get_users'), code=302))
    append_user(user['name'], user['email'], response)
    return response


@app.get('/user/<id>')
def get_user(id):
    users = load_users()
    user = find_user(id, users)
    if not user:
        return 'Page not Found', 404
    return render_template('users/show.html', user=user)


@app.get('/user/<id>/update')
def edit_user(id):
    users = load_users()
    user = find_user(id, users)
    errors = []
    return render_template('users/edit.html', user=user, errors=errors)


@app.post('/user/<id>/patch')
def patch_user(id):
    user = {
        'name': request.form.get('nick'),
        'email': request.form.get('email'),
        'id': id
    }
    errors = validate(user)
    if errors:
        return render_template('users/edit.html', user=user, errors=errors), 422
    response = redirect(url_for('get_users'), code=302)
    update_user(user, response)
    flash(f"User '{user['name']}' was edited succesfully")
    return response


@app.route('/user/<id>/delete', methods=['POST'])
def delete_user(id):
    users = load_users()
    print(users)
    print(id)
    user = find_user(id, users)
    response = redirect(url_for('get_users'), code=302)
    delete_user_pers(user, response)
    flash('User has been deleted', 'success')
    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form.get('mail')
        return redirect(url_for('get_users'), code=302)
    return render_template('users/login.html')


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('get_users'), code=302)
