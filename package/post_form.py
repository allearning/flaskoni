from flask import Flask, render_template, request, redirect, url_for, get_flashed_messages, flash
import json
# Это уже нам знакомое callable WSGI-приложение
app = Flask(__name__)
users = ['mike', 'mishel', 'adel', 'keks', 'kamila']
id_ = 0
Flask.secret_key = "d8ja"


def filter_users(part, data):
    if part is None:
        return data
    result = filter(lambda text: part in text, data)
    return list(result)


@app.route('/')
def hello_world():
    return 'Testing forms, go to /users'


@app.get('/users')
def get_users():
    messages = get_flashed_messages(with_categories=True)
    search_text = request.args.get('term', default='')
    return render_template(
        'users/index.html',
        search=search_text,
        messages=messages,
        users=filter_users(search_text, users)
    )

@app.get('/users/<id>')
def get_user(id):
    user = load_user(id)
    if not user:
        return 'Page not found', 404
    return render_template('users/show.html')
    

@app.get('/users/new')
def get_new_user():
    return render_template('users/new.html')


@app.post('/users')
def post_users():
    global id_
    user = {
        'name': request.form.get('nick'),
        'email': request.form.get('email'),
        'id': id_
    }
    users.append(user['name'])

    with open('users.txt', 'w') as file:
        json.dump(user, file)

    id_ += 1
    if False:
        return render_template(
            'users/index.html',
            search=search_text,
            users=filter_users(search_text, users)
        )
    flash(f"User '{user['name']}' was added succesfully")
    return redirect(url_for('get_users'), code=302)
