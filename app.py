from flask import Flask, redirect, url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from os import environ
from forms import PostsForm

app = Flask(__name__)

# 'f09e631cbbef362ed90263d2ddf8811e'
# app.config['SECRET KEY'] = environ.get('SECRET_KEY')
#app.config['SECRET KEY'] = 'f09e631cbbef362ed90263d2ddf8811e'

app.config['SECRET_KEY'] = 'ea1c41f19b792a6ca6a81516f977aa29'
app.config['SQLACLHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + \
                                        environ.get('MYSQL_USER') + \
                                        ':' + \
                                        environ.get('MYSQL_PASS') + \
                                        '@' + \
                                        environ.get('MYSQL_HOST') + \
                                        ':' + \
                                        environ.get('MYSQL_PORT') + \
                                        '/' + \
                                        environ.get('MYSQL_dbNAME')
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
    return render_template('homepage.html', title='Homepage')


@app.route('/about')
def about():
    post_data = Posts.query.all()
    return render_template('about.html', title='About Page', posts=post_data)

# GET - displays data
# POST - which sends data from website to app
# DELETE - deletes some data
# Insert - sends data, but more used for updating


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = PostsForm()
    if form.validate_on_submit():
        post_data = Posts(
            f_name=form.f_name.data,
            l_name=form.l_name.data,
            title=form.title.data,
            content=form.content.data
        )
        db.session.add(post_data)
        db.session.commit()

        return redirect(url_for('home'))
    else:
        return render_template('post.html', title='Add a post', form=form)


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
    # db.drop_all()
    db.session.query(Posts).delete()
    db.session.commit()
    return "It's all gone"


if __name__ == '__main__':
    app.run()
