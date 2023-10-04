import os
from flask import Flask, render_template, request
from sqlalchemy.sql import text
from sqlalchemy import create_engine
from markupsafe import Markup 

#db_connect = create_engine('mysql://root:my-password@db/my_database')
db_connect = create_engine('sqlite:///mydb.db', echo=True)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = db_connect

@app.route("/")
def hello():
    return "<h1>Hello World!</h1>"

@app.route("/login")
def login():
    # Recuperar parâmetros passados via URL após "?"
    id = request.args.get('id')
    user = request.args.get('user')
    password = request.args.get('password')
    
    conn = db_connect.connect()

    sql_Query_Not_Injection = text("select * from user where id=:user_id")
    result = conn.execute(sql_Query_Not_Injection, parameters=dict(user_id = id))
    
    #sql_Query_Injection_False_Negative = text("select * from user where id={}".format(id))
    #result = conn.execute(sql_Query_Injection_False_Negative)

    # deprecated in SQLAlchemy >=2.0
    #sql_Query_Injection = "select * from user where id={}".format(id)
    #result = conn.execute(sql_Query_Injection)

    content = "<table>"
    content = content + str("<tr>")
    content = content + str("<th>id</th>")
    content = content + str("<th>user</th>")
    content = content + str("<th>password</th>")
    content = content + str("</tr>")

    for row in result:
        content = content + str("<tr>")
        content = content + str("<td>"+str(row[0])+"</td>")
        content = content + str("<td>"+str(row[1])+"</td>")
        content = content + str("<td>"+str(row[2])+"</td>")
        content = content + str("</tr>")
        

    content = content + str("</table>")
    result = Markup(content)

    return render_template('index.html', result=result)
    
if __name__ == "__main__":
    app.run()