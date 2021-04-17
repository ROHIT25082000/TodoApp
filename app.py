from flask import Flask, render_template, request, redirect
from datetime import datetime 
import pytz
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

class Todo(db.Model): 
    sno = db.Column(db.Integer, primary_key = True)  
    title = db.Column(db.String(200),nullable = False)
    desc = db.Column(db.String(500), nullable = False)

    date_created = db.Column(db.DateTime, default = datetime.now(pytz.timezone('Asia/Kolkata'))) 
    def __repr__(self)->str:  
        return f"{self.sno} - {self.title} at {self.date_created}"

some = None

@app.route('/')
def index_page(): 
    db.create_all()
    alltodo = Todo.query.all() 
    return render_template("index.html", alltodo = alltodo) 

@app.route('/update/<int:sno>',  methods = ['GET','POST'])
def update_page(sno):
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno = sno).first()
        todo.title = title
        todo.desc = desc 
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
        
    todo = Todo.query.filter_by(sno = sno).first()
    return render_template('Update.html',todo = todo)

@app.route('/todo', methods= ['GET', 'POST']) 
def todo_add(): 
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo_obj = Todo(title = title, desc = desc)
        db.session.add(todo_obj)
        db.session.commit()
        return redirect('/')


@app.route('/delete/<int:sno>')
def delete_todo(sno):  
    obj = Todo.query.filter_by(sno = sno).first()
    db.session.delete(obj)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__": 
    app.run(debug = True,port = 2000)
