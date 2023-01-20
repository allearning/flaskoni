from flask import Flask, render_template, request

# Это уже нам знакомое callable WSGI-приложение
app = Flask(__name__)
users = ['mike', 'mishel', 'adel', 'keks', 'kamila']


def filter_users(part, data):
    if part is None:
        return data
    result = filter(lambda text: part in text, data)
    return list(result)


@app.route('/')
def hello_world():
    return 'Testing forms, go to /users'


@app.route('/users')
def get_users():
    search_text = request.args.get('term', default='')
    return render_template(
        'users/index.html',
        search=search_text,
        users=filter_users(search_text, users)
    )
