
import bcrypt
from flask import Flask, render_template, request,redirect,flash,url_for,session,get_flashed_messages
from datetime import datetime
import os
import psycopg2
from dotenv import load_dotenv

app=Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

load_dotenv()
def get_db():
    return psycopg2.connect(os.getenv("DATABASE_URL"))
    

@app.route("/")
def home():
   return render_template("index.html")

@app.route("/register",methods=['GET','POST'])
def register():
    flag=False
    msg = session.pop('msg',None)
    if request.method=='POST':
        user_name=request.form["username"]
        email=request.form["email"]
        password=request.form["password"]

        secret = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')



        cnt=get_db()
        curs=cnt.cursor()
        curs.execute("""insert into users(user_name,email,password) values(%s,%s,%s)""",(user_name,email,secret))

        cnt.commit()
        session['user_name']=user_name
        msg="Succesfully Register"
        flag=True

        curs.close()
        cnt.close()
        
       
    return render_template("register.html",msg=msg,flag=flag)




@app.route("/login", methods=['POST', 'GET'])
def login():
    cnt=get_db()
    curs=cnt.cursor()
    email = ''
    password = ''
    msg = session.pop('msg', None)
    ask_admin = False
    flag = False
    flag_anim = False
    # flag is for redirecting
    # flag_Anim prevents animation from playing on each page reload during error or success messages.`



    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        admin_pss = request.form.get("admin_pss")

        cnt = get_db()
        curs = cnt.cursor()

        # Step 1: Check if email exists in users table
        curs.execute("SELECT id, user_name, password, is_Admin FROM users WHERE email = %s", (email,))
        user = curs.fetchone()

        if user:
            user_id, user_name, hashed_password, is_admin = user
            if bcrypt.checkpw(
                password.encode('utf-8'),
                (hashed_password.decode('utf-8') if isinstance(hashed_password, bytes) else hashed_password).strip().encode('utf-8')
            ):
                session["user_id"] = user_id
                session["user_name"] = user_name
                session["is_admin"] = is_admin


                # Step 2: Check if user is listed in admin_auth table
                if not is_admin:
                    curs.execute("SELECT admin_password FROM admin_auth WHERE admin_email = %s", (email,))
                    admin_record = curs.fetchone()

                    if admin_record:
                        db_admin_password = admin_record[0]

                        if not admin_pss:
                            msg = "Enter admin password"
                            ask_admin = True
                        elif bcrypt.checkpw(admin_pss.encode('utf-8'), db_admin_password.encode('utf-8')):
                            # Promote to admin
                            curs.execute("UPDATE users SET is_Admin = %s WHERE email = %s", (True, email))
                            cnt.commit()
                            session["is_admin"] = True
                            msg = "Admin status granted successfully"
                            flag = True
                            flag_anim=True
                        else:
                            msg = "Incorrect admin password"
                            ask_admin = True
                            flag_anim=True
                    else:
                        msg = "Login successful<br>Welcome!"
                        flag = True
                        flag_anim = True
                else:
                    msg = "Welcome back admin" if is_admin  else "Login successful<br>Welcome!"
                    flag = True
                    flag_anim = True
            else:
                msg = "Invalid password"
                flag_anim = True
        else:
            msg = "Invalid email"
            flag_anim = True

        cnt.close()
        curs.close()

        return render_template("login.html", email=email, password=password,
                               ask_admin=ask_admin, rcat=flag, msg=msg, flag_anim=flag_anim)

    return render_template("login.html", ask_admin=ask_admin or "", email=email or "", 
                           password=password or "", rcat=flag, msg=msg, flag_anim=flag_anim)




@app.route("/catagories",methods=['POST','GET'])
def catagories():
    if 'user_id' not in session:
        return redirect(url_for("login"))
    cnt = get_db()
    curs = cnt.cursor()
    curs.execute("SELECT id, name FROM catogaries")
    catogaries = curs.fetchall()
    

    if request.method == 'POST':
        
        selected_category = request.form.get('catagory')
        session['selected_category'] = selected_category
        

    return render_template("catagories.html", catogaries=catogaries)


@app.route("/subcat/<int:cat_id>")
def subcat(cat_id):
    cnt=get_db()
    curs=cnt.cursor()
    curs.execute("select s_id, name, catogries_id from subcatogaries where catogries_id=%s",(cat_id,))
    subcat=curs.fetchall()

    return render_template("subcategory.html",subcat=subcat)

@app.route("/quizz/<int:id>/<int:id2>")
def quizz(id,id2):
    cnt=get_db()
    curs=cnt.cursor()
    curs.execute("select question,option1,option2,option3,option4,CORRECT_OPTION from questions where sub_id=%s",(id,))
    result=curs.fetchall()
    

    return render_template("quizz.html",result=result)

@app.route("/submit",methods=['GET','POST'])
def submit():
    
    answer={} 
    details={}
    score=0
    for i in request.form.keys():
        if i.startswith('ans'): 
            question=i.split('_')[1]
            answer[question]=request.form[i]
    total_attempt=len(answer)
    session['total_attempt']=total_attempt

    cnt=get_db()
    curs=cnt.cursor()
    for i,v in answer.items():
        curs.execute("select question,option1,option2,option3,option4,CORRECT_OPTION from questions where id=%s",(i,))
        crct=curs.fetchone()
        question,opt_a,opt_b,opt_c,opt_d,cr_op=crct

        option_txt={
            'a':opt_a,
            'b':opt_b,
            'c':opt_c,
            'd':opt_d,
        }
        status="Correct" if v==cr_op else "Incorrect"
        if status=="Correct":
            score+=1
       

        details[i]={
            "question":question,
            "user_ans":v,
            "user_txt":option_txt.get(v,"not answered"),
            "correct_op":cr_op,
            "correct_txt":option_txt.get(cr_op,"Not available"),
            "status":status

        }
        
    session['details']=details
    session['score']=score
    
    curs.execute("select count(*) from questions")
    total_ques=curs.fetchone()[0]
    
    user_name=session.get('user_name')
    
    total_attemptt=session.get('total_attempt',0)

    curs.execute("insert into submission(user_name,score,total_attempt,total_ques) values(%s,%s,%s,%s)",(user_name,score,total_attemptt,total_ques,))
    cnt.commit()

    curs.close()
    cnt.close()
    return redirect(url_for("result"))

        
    



@app.route("/result")
def result():
    det=session.get('details',{})
    score=session.get('score',0)
    return render_template("result.html",det=det,score=score)











@app.route("/admin",methods=['GET','POST'])
def admin():

    if 'is_admin' not in session or session['is_admin'] != 1:
        msg=("Access denied: Admins only")
        return redirect(url_for('admin_login'))  # redirect if not admin
    return render_template("admin.html")


@app.route("/admin/add_question",methods=['GET','POST'])
def add_question():
    msg = session.pop('msg',None)
    if 'is_admin' not in session or session['is_admin']!=True:
        msg="acess denied admin only"
        return redirect(url_for('home'))
    
    if session.get("user_name") != os.getenv("SUPER_ADMIN_EMAIL"):
        flash("❌ Access Denied: Only Super Admin can add questions")
        return redirect(url_for("admin"))
    cnt=get_db()
    curs=cnt.cursor()

    if request.method=='POST':
        ques = request.form.get('question')
        op1 = request.form.get('option1')
        op2 = request.form.get('option2')
        option3 = request.form.get('option3')
        option4 = request.form.get('option4')
        correct = request.form.get('correct_opt')
        sub_id = request.form.get('sub_id')
        try:
            curs.execute("insert into questions(question,option1,option2,option3,option4,correct_option,sub_id) values(%s,%s,%s,%s,%s,%s,%s)",(ques,op1,op2,option3,option4,correct,sub_id,))
            cnt.commit()
            msg="succesfully added"
        except Exception as err:
            msg=f"error occured{str(err)}"
        return render_template('question_add.html', msg=msg)
    curs.execute("SELECT s.s_id, s.name AS sub_name, c.name AS cat_name FROM subcatogaries s JOIN catogaries c ON s.catogries_id = c.id;")
    subcategories = curs.fetchall()                      

    curs.close()
    cnt.close()
    return render_template('question_add.html', msg=msg,subcategories=subcategories)

@app.route("/adminLogin", methods=['GET', 'POST'])
def adminLogin():
    msg = ""
    
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        cnt = get_db()
        curs = cnt.cursor()
        curs.execute("SELECT id, user_name, password, is_Admin FROM users WHERE email=%s", (email,))
        data = curs.fetchone()

        if data:
            user_id, user_name, hashed, is_admin = data
            if bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8')):
                if is_admin == 1:
                    session["admin_logged_in"] = True
                    session["user_id"] = user_id
                    session["user_name"] = user_name
                    session["is_admin"] = is_admin
                    msg = "Welcome back, Admin!"
                    return redirect(url_for("admin"))
                else:
                    session["msg"] = "Not authorized as admin."
                    
            else:
                session["msg"] = "Invalid password."
                
        else:
            session["msg"] = "Admin account not found."
            
            return redirect(url_for("adminLogin"))
    msg = session.pop("msg", "")

    return render_template("adminLogin.html", msg=msg)




@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

    


def questions(filepath):
    import json
    try:
        with open(filepath, 'r',encoding='utf-8') as file:
            data = json.load(file)
    except Exception as e:
        return f"❌ Error reading JSON file: {str(e)}"

    conn = get_db()
    cursor = conn.cursor()
    added_count = 0
    skipped_count = 0
    error_count = 0

    try:
        for category_name, subcats in data.get('categories', {}).items():
            # fetching category ID
            cursor.execute("SELECT id FROM catogaries WHERE name = %s", (category_name,))
            cat_result = cursor.fetchone()
            if not cat_result:
                print(f"⚠️ Category not found: {category_name}")
                continue
            cat_id = cat_result[0]

            for subcat_name, subcat_data in subcats.items():
                if not isinstance(subcat_data, dict):
                    continue

                sub_id = subcat_data.get("sub_id")
                questions_list = subcat_data.get("questions", [])

                # --Check if subcategory exists--
                cursor.execute("SELECT s_id FROM subcatogaries WHERE s_id = %s AND name = %s AND catogries_id = %s", (sub_id, subcat_name, cat_id))
                sub_result = cursor.fetchone()
                if not sub_result:
                    print(f"⚠️ Subcategory not found: {subcat_name} in {category_name}")
                    continue

                for q in questions_list:
                    question = q.get('question')
                    option1 = q.get('option1')
                    option2 = q.get('option2')
                    option3 = q.get('option3')
                    option4 = q.get('option4')
                    correct = q.get('correct_option')

                    if not question or not correct:
                        error_count += 1
                        continue

                    # --Check if question already exists in same subcategory--
                    cursor.execute("SELECT COUNT(*) FROM questions WHERE question = %s AND sub_id = %s", (question, sub_id))
                    if cursor.fetchone()[0] > 0:
                        skipped_count += 1
                        continue

                    try:
                        cursor.execute("""
                            INSERT INTO questions (question, option1, option2, option3, option4, sub_id, correct_option)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (question, option1, option2, option3, option4, sub_id, correct))
                        added_count += 1
                    except Exception as insert_err:
                        print(f"❌ Insert error for question: {question} -> {insert_err}")
                        error_count += 1
                        continue

        conn.commit()
        return f"✅ Import Completed\n🟢 Added: {added_count}\n🟡 Skipped: {skipped_count}\n🔴 Errors: {error_count}"

    except Exception as e:
        conn.rollback()
        return f"❌ Database error: {str(e)}"

    finally:
        cursor.close()
        conn.close()




@app.route("/import_questions", methods=["GET", "POST"])
def import_questions_route():
    import os
    if not session.get("is_admin"):
        return redirect("/login")

    message = ""
    if request.method == "POST":
        filepath = os.path.join("uploads", "questions.json")
        if os.path.exists(filepath):
            message = questions(filepath)
        else:
            message = "❌ questions.json not found in /uploads folder."

    return render_template("import_button.html", message=message)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
import os

@app.route("/upload_questions", methods=["POST"])
def upload_questions():
    
    if 'is_admin' not in session or session['is_admin'] != True:
        return redirect(url_for('home'))

    if session.get("user_name") != os.getenv("SUPER_ADMIN_EMAIL"):
        flash("❌ Access Denied: Only Super Admin can upload JSON file")
        return redirect(url_for("admin"))

    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'questions.json')
        file.save(filepath)
        result = questions(filepath)
        flash(result)
        return redirect(url_for('admin'))

@app.route("/import_questions", methods=["POST"])
def import_questions():
    if not session.get("is_admin") or session.get("user_name") != os.getenv("SUPER_ADMIN_EMAIL"):
        return "❌ Access Denied: Only Super Admin can import questions"
        
    filepath = "uploads/questions.json"
    if not os.path.exists(filepath):
        return "❌ questions.json file not found in uploads folder."

    result = questions("uploads/questions.json")
    return result

if __name__=="__main__":
    # port = int(os.environ.get("PORT",5000))
    # app.run(host="0.0.0.0",port=port,debug=False)
    app.run(debug=True)
