from flask import Flask, render_template, url_for, request, redirect
import cx_Oracle
from datetime import datetime

app = Flask(__name__)

class Session():
    def __init__(self, param):
        self.param = param
    def query(self):
        self.param += 1
        return self.param


@app.route('/', methods=['POST', 'GET'])
def Login():
    if request.method == 'POST':
        phone_no = request.form.get("login").rstrip()[:5]
        con = cx_Oracle.connect("priyanshu/0103@localhost:1521/xe")
        cur = con.cursor()
        cur.execute("SELECT * FROM DISP_PAGE")
        rows = cur.fetchall()
        cur.close()
        con.close()
        return render_template('index.html', rows=rows,phone_no=phone_no)
    else:
        return render_template('login.html')






@app.route('/index/<phone_no>', methods=['POST', 'GET'])
def index(phone_no):
    if request.method == 'POST':
        con = cx_Oracle.connect("priyanshu/0103@localhost:1521/xe")
        cur = con.cursor()
        # order_id = request.form.get("order_id").rstrip()
        sort_by = request.form.get("sort").rstrip()
        if sort_by != "":
            cur.execute(f"SELECT * FROM DISP_PAGE ORDER BY {sort_by}")
        else:
            filter = request.form.get("filter").rstrip()
            if filter != "":
                cur.execute(f"SELECT * FROM DISP_PAGE WHERE {filter}")
    else:

        con = cx_Oracle.connect("priyanshu/0103@localhost:1521/xe")
        cur = con.cursor()
        cur.execute("SELECT * FROM DISP_PAGE")

    rows = cur.fetchall()
    cur.close()
    con.close()
    return render_template('index.html',phone_no=phone_no, rows=rows)


@app.route('/add/<prod_id>/<seller_id>/<phone_no>')
def add(prod_id, seller_id,phone_no):
    con = cx_Oracle.connect("priyanshu/0103@localhost:1521/xe")
    cur = con.cursor()
    cur.execute(f"SELECT ID FROM ORDERS WHERE ID = {phone_no}")
    id = cur.fetchall()
    if len(id) == 0:
        cur.execute(f"INSERT INTO ORDERS VALUES ({phone_no},1,'16/8/2020',1,1)")
        con.commit()
    
    cur.execute(f"INSERT INTO ORDER_ITEMS VALUES ({phone_no}, {prod_id}, 1,  {seller_id}, NULL)")
    con.commit()
    cur.execute(f"SELECT PRODUCT_ID, QUANTITY, SELLER_ID FROM ORDER_ITEMS WHERE ORDER_ID = {phone_no}")
    rows = cur.fetchall()
    print("Added Successfully")
    basket_info = []
    for prod_id,Quant,seller_id in rows:
        cur.execute(f"SELECT NAME FROM PRODUCTS WHERE  ID = {prod_id}")
        product_name = cur.fetchall()[0][0]
        cur.execute(f"SELECT NAME FROM SELLERS WHERE  ID = {seller_id}")
        seller_name = cur.fetchall()[0][0]
        cur.execute(f"SELECT PRICE,DISCOUNT FROM PRICES WHERE  PRODUCT_ID = {prod_id} AND SELLER_ID = {seller_id}")
        price_discount = cur.fetchall()[0]
        basket_info.append([product_name, seller_name, Quant, price_discount[0], price_discount[1]])

    cur.close()
    con.close()
    try:
        return render_template('checkout.html', basket_info=basket_info)
        #return redirect('/')
    except:
        return 'There was a Problem in addition'






# @app.route('/delete/<int:id>')
# def delete(id):
#     task_to_delete = Todo.query.get_or_404(id)

#     try:
#         db.session.delete(task_to_delete)
#         db.session.commit()
#         return redirect('/')

#     except:
#         return 'There was a Problem in Deletion'


# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     task = Todo.query.get_or_404(id)

#     if request.method == 'POST':
#         task.content = request.form['content']

#         try:
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'There was an Error with Updating thr Task'

#     else:
#         return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)

