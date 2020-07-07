from flask import Flask
from flask import render_template

app = Flask(__name__)

dummyData = [
    {
        "f_name": "Gary",
        "l_name": "Forrow",
        "title": "My First Blog Post",
        "content": "Blaaah blaaaaahhhhhh",
    },
    {
        "f_name": "Semore",
        "l_name": "Content",
        "title": "How much I'd like to see.",
        "content": "I would like to see more",
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('homepage.html', title='Homepage', posts=dummyData)


@app.route('/about')
def about():
    return render_template('about.html', title='About Page')


if __name__ == '__main__':
    app.run()

