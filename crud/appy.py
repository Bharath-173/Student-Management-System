from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB connection (LOCAL)
MONGO_URI = "mongodb://127.0.0.1:27017/"
client = MongoClient(MONGO_URI)
db = client["student_crud_db"]
students = db["students"]

@app.route("/")
def home():
    all_students = list(students.find())
    return render_template("index.html", students=all_students)

@app.route("/students/new", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        students.insert_one({
            "name": request.form["name"],
            "usn": request.form["usn"],
            "dept": request.form["dept"]
        })
        return redirect(url_for("home"))
    return render_template("add_student.html")

@app.route("/students/<id>/edit", methods=["GET", "POST"])
def edit_student(id):
    student = students.find_one({"_id": ObjectId(id)})
    if request.method == "POST":
        students.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "name": request.form["name"],
                "usn": request.form["usn"],
                "dept": request.form["dept"]
            }}
        )
        return redirect(url_for("home"))
    return render_template("edit_student.html", student=student)

@app.route("/students/<id>/delete", methods=["POST"])
def delete_student(id):
    students.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
