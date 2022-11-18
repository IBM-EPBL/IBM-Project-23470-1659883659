from flask import Flask, render_template, request, redirect, url_for,session


import ibm_db
import bcrypt
import os




try:
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=0c77d6f2-5da9-48a9-81f8-86b520b87518.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31198;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=vxz92171;PWD=mCH7uu0w9WXH0hlY",'','')
    print(conn)
    print("connection successfull")
except:
    print("Error in connection, sqlstate = ")
    errorState = ibm_db.conn_error()
    print(errorState)


app = Flask(__name__)
app.secret_key ='_5#y2L"F4Q8z\n\xec]/'

# def send_conformation_mail():
# load_dotenv()   #load keys from .env
# sg = sendgrid.SendGridAPIClient(api_key = os.environ.get('SENDGRID_API_KEY'))   #set SendGrid API Key
# from_email = Email("susanthykala@gmail.com")     #the address that sends emails to the users


      






# message = Mail(
#     from_email='susanthykala@gmail.com',
#     to_emails='susanthykala@gmail.com',
#     subject='Sending with Twilio SendGrid is Fun',
#     html_content='<strong>and easy to do anywhere, even with Python</strong>')
# try:
#     sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
#     response = sg.send(message)
#     print(response.status_code)
#     print(response.body)
#     print(response.headers)
# except Exception as e:
#     print(e.message)



# sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
# from_email = Email("susanthykala@gmail.com")  # Change to your verified sender
# to_email = To("susanthykala@gmail.com")  # Change to your recipient
# subject = "Sending with SendGrid is Fun"
# content = Content("text/plain", "and easy to do anywhere, even with Python")
# mail = Mail(from_email, to_email, subject, content)

# # Get a JSON-ready representation of the Mail object
# mail_json = mail.get()

# # Send an HTTP POST request to /mail/send
# response = sg.client.mail.send.post(request_body=mail_json)
# print(response.status_code)
# print(response.headers)







@app.route("/",methods=['GET'])
def index():
    # if 'email' not in session:
    #   return redirect(url_for('login'))
    return render_template('index.html',name='Home')

@app.route("/home",methods=['GET'])
def home():
    return render_template('home.html',name='Home1')    
# def home():
#   if 'name' in session:
#     return render_template('index.html',name=session['name']+"'s account")
#   else:
#     return render_template('index.html')    

@app.route("/register",methods=['GET','POST'])
def register():
  if request.method == 'POST':
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    cpassword = request.form['cpassword']

    if not email or not name or not password or not cpassword:
      return render_template('register.html',error='Please fill all fields')
    if password != cpassword:
        return render_template('register.html',error='The password is not same')
    else:
        hash=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

    query = "SELECT * FROM LOGINAUTHENTICATION WHERE useremail=?"
    stmt = ibm_db.prepare(conn, query)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.execute(stmt)
    isUser = ibm_db.fetch_assoc(stmt)
    
    if not isUser:
      insert_sql = "INSERT INTO LOGINAUTHENTICATION(USERNAME, USEREMAIL, PASSWORD) VALUES (?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, email)
      ibm_db.bind_param(prep_stmt, 3, hash)
      ibm_db.execute(prep_stmt)
      return render_template('login.html',success="You can login")
      # send_conformation_mail()
    else:
      return render_template('register.html',error='Invalid Credentials')

  return render_template('register.html')

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
      email = request.form['email']
      password = request.form['password']

      if not email or not password:
        return render_template('login.html',error='Please fill all fields')
      query = "SELECT * FROM LOGINAUTHENTICATION WHERE useremail=?"
      stmt = ibm_db.prepare(conn, query)
      ibm_db.bind_param(stmt,1,email)
      ibm_db.execute(stmt)
      isUser = ibm_db.fetch_assoc(stmt)
      print(isUser,password)

      if not isUser:
        return render_template('login.html',error='Invalid Credentials')
      #return render_template('login.html',error=isUser['PASSWORD'])
      isPasswordMatch = bcrypt.checkpw(password.encode('utf-8'),isUser['PASSWORD'].encode('utf-8'))

      if not isPasswordMatch:
        return render_template('login.html',error='Invalid Credentials')

      session['email'] = isUser['USEREMAIL']
      return redirect(url_for('home'))

    return render_template('login.html',name='Home')

@app.route('/user_map')
def user_map():
   return render_template('user_map.html',name='Map')

@app.route('/about')
def about():
   return render_template('about.html',name='Map')

@app.route('/success')
def success():
  #  conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=0c77d6f2-5da9-48a9-81f8-86b520b87518.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31198;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=vxz92171;PWD=mCH7uu0w9WXH0hlY",'','')
  #  conn.row_factory = sql.Row
   
  #  cur = con.cursor()
  #  cur.execute("select * from LOCATION")
   
  #  students = cur.fetchall();
  
   return render_template('success.html',name='Success')  


@app.route('/addzone',methods=['GET','POST'])
def addzone():
  if request.method == 'POST':
    longitude = request.form['longitude']
    latitude = request.form['latitude']
    city = request.form['city']
    pincode = request.form['pincode']
    email = session['email']

    if not longitude or not latitude or not city or not pincode:
      return render_template('addzone.html',error='Please fill all fields')

    query = "SELECT * FROM LOGINAUTHENTICATION WHERE useremail=?"
    stmt = ibm_db.prepare(conn, query)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.execute(stmt)
    isUser = ibm_db.fetch_assoc(stmt)
    
    if  isUser:
      insert_sql = "INSERT INTO LOCATION(LONGITUDE, LATITUDE, CITY,PINCODE) VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, longitude)
      ibm_db.bind_param(prep_stmt, 2, latitude)
      ibm_db.bind_param(prep_stmt, 3, city)
      ibm_db.bind_param(prep_stmt, 4, pincode)

      ibm_db.execute(prep_stmt)
      return render_template('success.html')
      # send_conformation_mail()
    else:
      return render_template('login.html',error='Invalid Credentials')

  return render_template('addzone.html')

    #  return render_template('addzone.html',name='Add') 

@app.route('/removezone')
def removezone():
     return render_template('removezone.html',name='Remove') 

@app.route('/table')
def table():
     return render_template('table.html',name='Table')      


@app.route('/data')
def data():
   return render_template('data.html',name='Map')  


@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('name', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
