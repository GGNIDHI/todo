from flask import Flask
from flask import *
import mysql.connector 

app=Flask(__name__)

#with open('D:\wiley_Git\mypass.txt', 'r') as file:
 #   data = file.read().replace('\n', '')


mydatabase = mysql.connector.connect(
    host='database-1.cdbr0xurh9oc.ap-south-1.rds.amazonaws.com', user='admin',
    passwd='NIDHI7673', database='todo',auth_plugin='mysql_native_password')   


mycursor = mydatabase.cursor()




@app.route("/")

def index():
    return render_template('index.html')

@app.route("/index.html")

def index_1():
    return render_template('index.html')

@app.route("/layout.html")

def layout():
    return render_template("layout.html")

@app.route("/lists.html")

def lists():
    return render_template("lists.html")


### LIST ROUTES HERE

@app.route("/create.html")
def create():
    return render_template("create.html")

# @app.route("/create.html", methods=['POST'])
# def create():
#     print("hello create")
#     if request.method == "POST":
#         print("method is post -- ASDF")
#     # print(request.form["list"])
#     # print(request.form["allItems"])
#     return render_template("create.html")

@app.route("/create_p", methods=['POST'])
def create_p():
    # print("hello create")
    items  = []
    if request.method == "POST":
        listname = request.form["list"]
        print(listname)
        allItems=request.form["item"]
        # items = allItems.split(",").strip()
        items = [x.strip() for x in allItems.split(',')]
        items = set(items)
        items = list(items)
        print(items)
    
    for i in items:
        ### IMPROVEMENT NEEDED - USING TRANSACTION HERE WILL HELP -> NAVYA AND AJINKYA
        mycursor.execute(f"INSERT INTO list (name, listname) values ('{i}', '{listname}');")
        mycursor.execute("commit;")
    mycursor.execute('SELECT listname FROM list group by listname;')
    data = mycursor.fetchall()

    dct = {}
    for i in data:
        val=f'select name from list where listname="{i[0]}"'
        mycursor.execute(val)
        dct[i] = mycursor.fetchall()

    return render_template('display.html',output_data=dct)

@app.route("/view.html")
def view():
    mycursor.execute('SELECT listname FROM list group by listname;')
    data = mycursor.fetchall()
    
    mycursor.execute( f"select name from list where listname='{data[0][0]}';" )
    item = mycursor.fetchall()
    return render_template("view.html", output_data=data , output_item=item , listname=data[0][0])

@app.route("/view_p",methods=["POST"])
def view_p():
    if request.method=="POST":
        l=request.form["item"]
        print(l)
    mycursor.execute('SELECT listname FROM list group by listname;')
    data = mycursor.fetchall()
    mycursor.execute( f"select name from list where listname='{l}';" )
    item = mycursor.fetchall()
    return render_template("view.html",output_data=data , output_item=item , listname = l)

@app.route("/view_p_p",methods=["POST"])
def view_p_p():
    if request.method=="POST":
        l=request.form["item"]
        lname = request.form["listname"]
        mycursor.execute(f"delete from list where listname='{lname}' and name='{l}'")
        mycursor.execute('commit;')
    mycursor.execute('SELECT listname FROM list group by listname;')
    data = mycursor.fetchall()
    mycursor.execute( f"select name from list where listname='{lname}';" )
    item = mycursor.fetchall()

    return render_template("view.html",output_data=data , output_item=item , listname=lname) 

@app.route("/display.html")
def display():
    mycursor.execute('SELECT listname FROM list group by listname;')
    data = mycursor.fetchall()

    dct = {}
    for i in data:
        val=f'select name from list where listname="{i[0]}"'
        mycursor.execute(val)
        dct[i] = mycursor.fetchall()

    return render_template('display.html',output_data=dct)

@app.route("/delete.html")
def delete():
    mycursor.execute("select listname from list group by listname")
    result = mycursor.fetchall()
    
    return render_template("delete.html",output_data=result)

@app.route("/delete_p",methods=["POST"])
def delete_p():
    if request.method=="POST":
        l=request.form["list"]
        mycursor.execute(f"delete from list where listname='{l}';")
        mycursor.execute("commit")
    mycursor.execute("select listname from list group by listname")
    result = mycursor.fetchall()
    
    return render_template("delete.html",output_data=result)



### TASKS ROUTES
# 


@application.route("/tasks.html")
def tasks():
    mycursor.execute('select * from task;')
    data = mycursor.fetchall()
    return render_template("tasks.html" , output_data = data)

@application.route("/tasks_p" , methods=["POST"])
def tasks_p():
    if request.method=="POST":
        l=request.form["id"]
        mycursor.execute(f"delete from task where id='{l}';")
        mycursor.execute('commit;')
        mycursor.execute(f"delete from hashtag where task_id='{l}';")
        mycursor.execute('commit;')

    mycursor.execute('select * from task;')
    data = mycursor.fetchall()
    return render_template("tasks.html" , output_data = data)




@application.route("/t_completed.html")
def t_completed():
    mycursor.execute("select * from task where status='1';")
    data = mycursor.fetchall()
    return render_template("t_completed.html" , output_data = data)

@application.route("/t_completed_p" , methods=["POST"])
def t_completed_p():
    if request.method=="POST":
        l=request.form["id"]
        mycursor.execute(f"update task set status='0' where id='{l}';")
        mycursor.execute('commit;')

    mycursor.execute("select * from task where status='1';")
    data = mycursor.fetchall()
    return render_template("t_completed.html" , output_data = data)


@application.route("/t_upcoming.html")
def t_upcoming():
    mycursor.execute("select * from task where status='0';")
    data = mycursor.fetchall()
    return render_template("t_upcoming.html" , output_data = data)


@application.route("/t_upcoming_p" , methods=["POST"])
def t_upcoming_p():
    if request.method=="POST":
        l=request.form["id"]
        mycursor.execute(f"update task set status='1' where id='{l}';")
        mycursor.execute('commit;')

    mycursor.execute("select * from task where status='0';")
    data = mycursor.fetchall()
    return render_template("t_upcoming.html" , output_data = data)


@application.route("/t_addtask.html")
def t_addtask():
    
    return render_template("t_addtask.html")

@application.route("/t_addtask_p", methods=["POST"])
def t_addtask_p():
    hashtags = []
    if request.method=="POST":
        l=request.form["name"]
        mycursor.execute(f"insert into task (task_name, status) values ('{l}' , '0');")
        mycursor.execute("commit;")
        mycursor.execute(f"select id from task order by id desc limit 1 ;")
        val = mycursor.fetchall()
        for i in l.split(" "):
            if i[0]=='#':
                mycursor.execute(f"insert into hashtag (task_id, hash_tag) values ('{val[0][0]}' , '{i[1:len(i)]}');")
                mycursor.execute("commit;")


    mycursor.execute('select * from task;')
    data = mycursor.fetchall()
    return render_template("tasks.html" , output_data = data)



@application.route("/t_search.html")
def t_search():
    mycursor.execute('select distinct hash_tag from hashtag;')
    data = mycursor.fetchall()
    return render_template("t_search.html", hash_data=data)

@application.route("/t_search_p", methods=["POST"])
def t_search_p():
    if request.method=="POST":
        l=request.form["search"]
        mycursor.execute(f"select distinct * from task inner join hashtag on task.id=hashtag.task_id where hash_tag='{l}';")
        data = mycursor.fetchall()
        mycursor.execute('select distinct hash_tag from hashtag;')
        data2 = mycursor.fetchall()
    return render_template("t_search.html", output_data=data , hash_data=data2)


@application.route("/t_update.html")
def t_update():
    mycursor.execute('select * from task;')
    data = mycursor.fetchall()
    return render_template("t_update.html", output_data=data)

@application.route("/t_update_task.html", methods=["POST"])
def t_update_task():
    if request.method=="POST":
        l=request.form["id"]
        mycursor.execute(f'select * from task where id={l};')
        data = mycursor.fetchall()
        print(data[0][1])
    return render_template("t_update_task.html" , output_data=data)

@application.route("/t_update_p", methods=["POST"])
def t_update_p():
    if request.method=="POST":
        l=request.form["name"]
        id=request.form["id"]
        print(l)
        print(id)

        mycursor.execute(f"update task set task_name='{l}' where id={id};")
        mycursor.execute("commit;")
        mycursor.execute(f"delete from hashtag where task_id={id}")
        mycursor.execute("commit;")
        for i in l.split(" "):
            if i[0]=='#':
                mycursor.execute(f"insert into hashtag (task_id, hash_tag) values ('{id}' , '{i[1:len(i)]}');")
                mycursor.execute("commit;")
    

    mycursor.execute('select * from task;')
    data = mycursor.fetchall()
    return render_template("tasks.html" , output_data = data)


if __name__=='__main__':
    application.run(debug=True)





