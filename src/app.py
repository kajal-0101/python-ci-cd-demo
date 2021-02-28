from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQL_ALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    ids = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route("/")
def index():
    # show all todos
    todo_list = Todo.query.all()
    print(todo_list)
    return render_template('index.html', todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    # add new item
    title = request.form.get("title")
    if title != "":
        new_todo = Todo(title=title, complete=False)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    # add new item
    todo = Todo.query.filter_by(ids=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # add new item
    todo = Todo.query.filter_by(ids=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/about")
def about():
    return "About Page for testing"

@app.route("/calculator")
def calculator():
    return render_template("calculator.html")

@app.route("/send", methods=["POST"])
def get_operand():
    if request.method == "POST":
        num1 = request.form['num1']
        num2 = request.form['num2']
        num1 = num1.strip()
        num2 = num2.strip()
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if (regex.search(num1) == None) and (regex.search(num2) == None) and(num1 != "") and (num2 != ""):
            if (num1.isalpha() == False) and (num2.isalpha() == False):
                operator = request.form['Operation']
                if operator == "add":
                    val = addition(num1, num2)
                    return render_template("calculator.html", result=val)
                elif operator == "sub":
                    val = substraction(num1, num2)
                    return render_template("calculator.html", result=val)
                elif operator == "mul":
                    val = multiplication(num1, num2)
                    return render_template("calculator.html", result=val)
                elif operator == "div":
                    val = division(num1, num2)
                    return render_template("calculator.html", result=val)
                elif operator == "mod":
                    val = modulus(num1, num2)
                    return render_template("calculator.html", result=val)
                else:
                    if operator == "pow":
                        val = power(num1, num2)
                        return render_template("calculator.html", result=val)
            else:
                val = "Only numeric value allowed"
                return render_template("calculator.html", result=val)
        else:
            val = "No special symbols must be there as well as the fields cannot be blank"
            return render_template("calculator.html", result=val)

def addition(num1, num2):
    return float(num1) + float(num2)

def substraction(num1, num2):
    return float(num1) - float(num2)

def multiplication(num1, num2):
    return float(num1) * float(num2)

def division(num1, num2):
    return float(num1) / float(num2)

def modulus(num1, num2):
    return float(num1) % float(num2)
def power(num1, num2):
    return float(num1) ** float(num2)

@app.route("/refresh_calculator")
def refresh_calculator():
    return redirect(url_for("calculator"))

if __name__ == "__main__":
    db.create_all()
    app.run()