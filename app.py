from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)


app.config['SECRET KEY'] = environ.get('SECRET_KEY')
app.config['SQLACLHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + environ.get('MYSQL_USER') + ':' + environ.get('dbPASS') + environ.get('MYSQL_HOST') + ':' + environ.get('MYSQL_PORT') + environ.get('dbNAME')
db = SQLAlchemy(app)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(30), nullable=False)
    l_name = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(300), nullable=False, unique=True)

    def __repr__(self):
        return ''.join(
            [
                'Title: ' + self.title + '\n'
                                         'Name:' + self.f_name + ' ' + self.l_name + '\n'
                                                                                     'Content: ' + self.content
            ]
        )


@app.route('/')
@app.route('/home')
def home():
    post_data = Posts.query.all()
    return render_template('homepage.html', title='Homepage', posts=post_data)


@app.route('/about')
def about():
    return render_template('about.html', title='About Page')


@app.route('/create')
def create():
    db.create_all()
    post = Posts(f_name="Gary", l_name='Forrow', title='My first db entry', content='Look at this content')
    post2 = Posts(f_name="Gary2", l_name='Forrow2', title='My first db entry2', content='Look at this content2')
    db.session.add(post)
    db.session.add(post2)
    db.session.commit()
    return "Added the table and populated it with records"


@app.route('/delete')
def delete():
    #db.drop_all()
    db.session.query(Posts).delete()
    db.session.commit()
    return "It's all gone"


if __name__ == '__main__':
    app.run()
