from flask import Flask,render_template,request
import pickle
import os
import random
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
db_path = os.path.join(os.path.dirname(__file__),'cardetails.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

with open("new_work.pkl","rb") as f:
    mdl=pickle.load(f)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    username=request.form.get('username')
    password=request.form.get('password')
    email=request.form.get('email')
    new_user = User(username='sidd', email='email@gmail.com', password='Imsidd@123')
    db.session.add(new_user)
    db.session.commit()
    print(new_user.email)
    return 'signup'
@app.route('/',methods=["GET","POST"])
def hello_world():
    if request.method=="POST":
        car=int(request.form['car'])
        initial_payment=request.form["initial_payment"]
        range1, range2 = initial_payment.split('-')
        range1=int(range1)
        range2=int(range2)
        budget=random.randint(range1, range2)
        upfront=int(request.form["upfront"])
        contract_lenth=int(request.form["contract_length"])
        milage=int(request.form["milage"])
        doc_price=random.randint(275,325)
        new_car_no=random.randint(0,14)
        if car+new_car_no>=14:
            new_car_no=new_car_no
        else:
            new_car_no=car+new_car_no
        new_car_no1=new_car_no-1
        tight_budget=random.randint(0,40)
        budget1=budget+new_car_no+tight_budget
        budget2=budget+tight_budget
        list0=[new_car_no,upfront,contract_lenth,milage,doc_price,budget1]
        list1=[car,upfront,contract_lenth,milage,doc_price,budget]
        list2=[new_car_no1,upfront,contract_lenth,milage,doc_price,budget2]
        result=mdl.predict([list1])
        result1=mdl.predict([list0])
        result2=mdl.predict([list2])
        print(result,result1,result2)
        flat_list0 = [item for sublist in result for item in sublist]
        my_formatted_list0 = [ '%.2f' % elem for elem in flat_list0 ]
        flat_list1 = [item for sublist in result1 for item in sublist]
        my_formatted_list1 = [ '%.2f' % elem for elem in flat_list1 ]
        flat_list2 = [item for sublist in result2 for item in sublist]
        my_formatted_list2 = [ '%.2f' % elem for elem in flat_list2 ]
        price1 = my_formatted_list0[0]
        list0.append(price1)
        price2 = my_formatted_list1[0]
        list1.append(price2)
        price3 = my_formatted_list2[0]
        list2.append(price3)
        res=[list0,list1,list2]
        return render_template("older.html",res=res,lis=0)  
    return render_template("index.html")
    
if __name__ == "__main__":
    app.run(debug=True)

