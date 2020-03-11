from flask import Flask,render_template, request, redirect
import os
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class Book(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Title: {}>".format(self.title)

if app.config["ENV"] == "development":
    app.config.from_object("config.Staging")
if app.config["ENV"] == "production":
    app.config.from_object("config.Production")
if app.config["ENV"] == "testing":
    app.config.from_object("config.Testing")


@app.route("/book/", methods=["GET", "POST"])
def book():
    
    if request.form:
        book = Book(title=request.form.get("title"))
        db.session.add(book)
        db.session.commit()
    books = Book.query.all()

    return render_template("home.html", books=books)

@app.route("/book/edit/<string:title>", methods=["GET", "POST"])
def edit(title):

    if request.form:
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        book = Book.query.filter_by(title=oldtitle).first()
        book.title = newtitle
        db.session.commit()
        return redirect("/book/")
        
    book = Book.query.filter_by(title=title).first()
    return render_template("edit.html", book=book)

@app.route("/book/delete/<string:title>", methods=["GET", "POST"])
def delete(title):
    book = Book.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/book/")

if __name__ == "__main__":
    app.run()