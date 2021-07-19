import json
from os import name
import cx_Oracle
con = cx_Oracle.connect("priyanshu/0103@localhost:1521/xe")
cur = con.cursor()
products_info = []
limit = 2000
i = 0
for line in open('amazon_fashion_products.ldjson', 'r'):
    if i > 1000:
        products_info.append(json.loads(line))
    i += 1
    if i >= limit:
        break

#print(products_info[0]['uniq_id'])

# Perform Following Inserts
# CATEGORIES TABLE Set Categories to hold "FASHION" get category id
# BRANDS Insert product_info['brand'] into brands and get ID
# PRODUCTS Insert uniq_id[:6], 'productname', Category_id and brand_id, <add> ''Rating''
# PRODUCT_URLS Product_id, Image URL "medium", Product_url,  
# PRICES INSERT product_id, seller_id(Const), sales_price, Discount % (discountpercentage)
# 

# cur.execute("INSERT INTO CATEGORIES VALUES (544, 'FASHION')")
# con.commit()



id = 58597
for product_info in products_info:
    brand = product_info['brand'].replace("'","''")[:40]
    cur.execute(f"INSERT INTO BRANDS VALUES ({id}, '{brand}')")
    con.commit()
    name = name.replace("'"," ")[:40]
    cur.execute(f"INSERT INTO PRODUCTS VALUES ({id}, '{name}', {id}, {544}, '{product_info['rating']}')")
    con.commit()
    cur.execute(f"INSERT INTO PRODUCT_URLS VALUES ({id}, '{product_info['medium']}', '{product_info['product_url']}')")
    con.commit()
    cur.execute(f"INSERT INTO PRICES VALUES ({id}, 496, {float(product_info['sales_price'])}, {id%6572})")
    con.commit()
    id += 1
    print(id)
    


cur.close()
con.close()
#id = cur.fetchall()

