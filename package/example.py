from flask import Flask, render_template

# Это уже нам знакомое callable WSGI-приложение
app = Flask(__name__)


@app.route('/')
def hello_world():
    return '200!!!!!!!!!!!!!!!!!!!!'


@app.get('/users/<id>')
def users_get(id):
    return render_template(
        'users/show.html',
        id=id,
        name='nickname-' + id
    )


@app.post('/users')
def users():
    return 'Users', 302


@app.route('/courses/<id>')
def courses(id):
    return f'Course id: {id}'
