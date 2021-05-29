from datetime import date
from flask import Flask, request ,render_template , jsonify
from pymongo import MongoClient

app=Flask("To-do-app")

@app.route('/home/')
def home():
    return render_template("home.html")
   
@app.route('/form')
def form():
    return render_template("form.html")

@app.route('/mydata')
def show():
    return render_template("mydata.html")

@app.route('/list')
def list():
    return render_template("list.html")


@app.route('/data',methods=['POST'])
def store():
    if request.method=='POST':
#       global data1
       d=request.form.get('date')
       m=request.form.get('month')
       y=request.form.get('year')
       d_name= "to-do-list-{}".format(str(y))
       t=request.form.get('task')
       db=[
         {
        "date": d,
        "month": m,
        "year": y,
        "task": t,
          }
            ]
       client = MongoClient("mongodb://127.0.0.1:27017")
       tdl_db=client[d_name]         # use to_do_list database per year or create new one
       coll=tdl_db[m]  
       key = {'date': d}
       data = {"$set":{"task":t}};
       coll.update(key, data, upsert=True);
       return render_template("home.html")
       
@app.route('/show',methods=['POST'])
def retrieve():
    if request.method=='POST':
       client = MongoClient("mongodb://127.0.0.1:27017")
       d=request.form.get('date')
       m=request.form.get('month')
       y=request.form.get('year')
       d_name= "to-do-list-{}".format(str(y))
       db=[{
        "date": d,
        "month": m,
        "year": y,
          }]
       client = MongoClient("mongodb://127.0.0.1:27017")
       tdl_db=client[d_name]         # use to_do_list database per year or create new one
       coll=tdl_db[m]
       x = coll.find({"date": d},{'_id': 0, 'task': 1})
       for i in x:
           y=i['task'].split('\r\n')
       return render_template("/list.html",x=y)

app.run(port=3333 ,debug=True)