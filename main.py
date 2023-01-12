import os

from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo-data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app)


class TaskForm(FlaskForm):
    task_name = StringField(u'Task Name:', validators=[DataRequired()])
    submit = SubmitField(u'Submit')


class EditForm(FlaskForm):
    new_task = StringField(u'New Task: ', validators=[DataRequired()])
    submit = SubmitField(u'Submit')


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # task = db.Column(db.String(255), unique=True, nullable=False)
    task = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Task {self.task}>'


@app.route('/')
def home():
    all_tasks = Tasks.query.all()

    return render_template('index.html', tasks=all_tasks)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = TaskForm()
    if form.validate_on_submit() and request.method == "POST":
        add_task = Tasks(task=form.task_name.data)
        db.session.add(add_task)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('add.html', form=form)


@app.route("/edit", methods=['GET', 'POST'])
def edit_task():
    edit_form = EditForm()
    if edit_form.validate_on_submit() and request.method == "POST":
        task_id = request.args.get('id')
        query_to_update = Tasks.query.get(task_id)
        query_to_update.task = edit_form.new_task.data
        db.session.commit()
        print(query_to_update.task)

        return redirect(url_for('home'))

    task_id = request.args.get('id')
    task_query = Tasks.query.get(task_id)
    print(task_query)
    return render_template('edit_task.html', form=edit_form, task=task_query)


@app.route('/delete', methods=['GET', 'POST'])
def delete_entry():
    task_id = request.args.get('id')
    query_to_delete = Tasks.query.get(task_id)
    db.session.delete(query_to_delete)
    db.session.commit()

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
#     app.run(debug=True)
    db.create_all()
