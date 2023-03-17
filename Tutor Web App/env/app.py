from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from email.message import EmailMessage
import ssl
import smtplib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
app.config['SQLALCHEMY_BINDS'] = {
    'second_database': 'sqlite:///staff.db',
    'third_database': 'sqlite:///applications.db',
    'forth_database': 'sqlite:///Faculty1.db',
    'fifth_database': 'sqlite:///Faculty2.db',
    'sixth_database': 'sqlite:///Faculty3.db',
}
db = SQLAlchemy(app)

class Student(db.Model):
    __tablename__ = 'Student'
    username = db.Column(db.String(200), primary_key=True)
    fullname = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contactno = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(25), nullable=False)
    gender = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.username

class Staff(db.Model):
    __bind_key__ = 'second_database'
    __tablename__ = 'Staff'
    staff_username = db.Column(db.String(200), primary_key=True)
    staff_fullname = db.Column(db.String(200), nullable=False)
    staff_email = db.Column(db.String(100), unique=True, nullable=False)
    staff_contactno = db.Column(db.Integer, nullable=False)
    staff_password = db.Column(db.String(25), nullable=False)
    staff_gender = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.username

class Application(db.Model):
    __bind_key__ = 'third_database'
    __tablename__ = 'Application'
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(200), nullable=False)
    qualification = db.Column(db.String(50), nullable=False)
    faculty = db.Column(db.String(50), nullable=False)
    module_name = db.Column(db.String(75), nullable=False)
    final_mark = db.Column(db.Integer, nullable=False) 
    status = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.id

class Faculty1(db.Model):
    __bind_key__ = 'forth_database'
    __tablename__ = 'Faculty1'
    id = db.Column(db.Integer, primary_key=True) 
    module_name = db.Column(db.String(75), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.id

class Faculty2(db.Model):
    __bind_key__ = 'fifth_database'
    __tablename__ = 'Faculty2'
    id = db.Column(db.Integer, primary_key=True) 
    module_name = db.Column(db.String(75), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.id

class Faculty3(db.Model):
    __bind_key__ = 'sixth_database'
    __tablename__ = 'Faculty3'
    id = db.Column(db.Integer, primary_key=True) 
    module_name = db.Column(db.String(75), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.id

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usernamepar = request.form['username']
        passwordpar = request.form['password']

        student = db.session.query(Student).filter_by(username=usernamepar, password=passwordpar).first()
        staff = db.session.query(Staff).filter_by(staff_username=usernamepar, staff_password=passwordpar).first()

        if staff:
            staffpar = db.session.query(Staff).filter_by(staff_username=usernamepar).first()
            countapplicationpar = db.session.query(Application).count()
            countacceptpar = db.session.query(Application).filter_by(status="Accepted").count()
            countrejectpar = db.session.query(Application).filter_by(status="Rejected").count()
            return render_template('staffportal.html',staff_fullname=staffpar.staff_fullname, staff_username=staffpar.staff_username,countapplication=countapplicationpar,countaccept=countacceptpar,countreject=countrejectpar)
        elif student:
            students = db.session.query(Student).filter_by(username=usernamepar).first()
            stud_status = db.session.query(Application).filter_by(username=usernamepar).first()
            if stud_status: 
                return  render_template('studentportal.html',Username=students.username, Fullname=students.fullname, Email=students.email, Cellno=students.contactno, Gender=students.gender, Appstatus=stud_status.status)
            else:
                return  render_template('studentportal.html',Username=students.username, Fullname=students.fullname, Email=students.email, Cellno=students.contactno, Gender=students.gender, Appstatus="No Appliction Submitted")                
        else:
            return render_template('login.html', error="User Name or Password incorrect!!Please try again")
    else:
        return render_template('login.html', error=False)

@app.route('/password', methods=['GET', 'POST'])
def password():
    if request.method == 'POST':
        usernamepar = request.form['username']
        
        student = db.session.query(Student).filter_by(username=usernamepar).first()
        staff = db.session.query(Staff).filter_by(staff_username=usernamepar).first()        

        if staff:
            staffpar = db.session.query(Staff).filter_by(staff_username=usernamepar).first() 
            try:
                email_sender= 'shais.mobileliteracy@gmail.com'
                email_password= 'ectualwggcwopgmy'

                email_receiver = students.staff_email

                subject = "Pasword Recovery"
                body = """
                Here is your Password: """ + staffpar.staff_password

                em= EmailMessage()
                em['From'] = email_sender
                em['To'] = email_receiver
                em['subject'] = subject
                em.set_content(body)

                context = ssl.create_default_context()

                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
                    smtp.sendmail(email_sender, email_receiver, em.as_string()) 
                
                return redirect(url_for('login'))
            except:
                return render_template('password.html', error="error occured,Check Connection")
        elif student:
            students = db.session.query(Student).filter_by(username=usernamepar).first()
            try:
                email_sender= 'shais.mobileliteracy@gmail.com'
                email_password= 'ectualwggcwopgmy'

                email_receiver = students.email

                subject = "Pasword Recovery"
                body = """
                Here is your Password: """ + students.password

                em= EmailMessage()
                em['From'] = email_sender
                em['To'] = email_receiver
                em['subject'] = subject
                em.set_content(body)

                context = ssl.create_default_context()

                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
                    smtp.sendmail(email_sender, email_receiver, em.as_string())
                
                return redirect(url_for('login'))
            except:
                return render_template('password.html', error="error occured,Check Connection")      
        else:
           return render_template('password.html', error="Please enter the correct Username to receive your password!") 
    else:
        return render_template('password.html', error=False)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":

        usernamePar = request.form['username']
        fullnamePar = request.form['fullname']
        emailPar = request.form['email']
        cellnoPar = request.form['cell-number']
        passwordPar = request.form['password']
        genderPar = request.form['gender']

        confirmpassword = request.form['confirmpassword']
        accountinformation = request.form['accountinformation']

        if (confirmpassword == passwordPar and cellnoPar[0]=="+"):
            if accountinformation == "Staff" :
                try:
                    new_staff= Staff(staff_username=usernamePar, staff_fullname=fullnamePar, staff_email=emailPar, staff_contactno=cellnoPar, staff_password=passwordPar, staff_gender=genderPar)
                    db.session.add(new_staff)
                    db.session.commit()
                    return redirect('/login')
                except:
                    return render_template('register.html', error="Error adding new staff member. Please try again.")
            elif accountinformation == "Student" :
                try:
                    new_student = Student(username=usernamePar, fullname=fullnamePar, email=emailPar, contactno=cellnoPar, password=passwordPar, gender=genderPar)
                    db.session.add(new_student)
                    db.session.commit()
                    return redirect('/login')
                except:
                    return render_template('register.html', error="Error adding new student. Please try again.")
        else:
            return render_template('register.html', error="Passwords do not match or Number must begin with +27. Please try again.")
    else :
        return render_template('register.html')

@app.route('/studentportal', methods=['GET', 'POST'])
def studentportal():
    if request.method == 'POST':
        username = request.form['username']
        qualification = request.form['qualification']
        faculty = request.form['faculty']
        module_name = request.form['modulename']
        final_mark = request.form['finalmark']
        status = "Pending"

        # check if the module exists based on the faculty
        if faculty == "Faculty1":
            module = db.session.query(Faculty1).filter_by(module_name=module_name).first()
        elif faculty == "Faculty2":
            module = db.session.query(Faculty2).filter_by(module_name=module_name).first()
        elif faculty == "Faculty3":
            module = db.session.query(Faculty3).filter_by(module_name=module_name).first()

        if not module:
            return render_template('login.html', error="Module does not exist in the selected faculty")

        # check if the application status is accepted or pending
        existing_application = db.session.query(Application).filter_by(username=username, faculty=faculty).first()
        if existing_application and existing_application.status != "Rejected":
            return render_template('login.html', error="You have already applied for a module in this faculty and your application is not rejected")
        else:
            application = Application(username=username, qualification=qualification, faculty=faculty, final_mark=final_mark, module_name=module_name, status=status)
            db.session.add(application)
            db.session.commit()
            return render_template('login.html', success="Your application has been submitted successfully!")
    
    return render_template('studentportal.html')

@app.route('/staffportal')
def staffportal():
        usernamepar = request.form['{{staff_username}}']
        staffpar = db.session.query(Staff).filter_by(staff_username=usernamepar).first()
        countapplicationpar = db.session.query(Application).count()
        countacceptpar = db.session.query(Application).filter_by(status="Accepted").count()
        countrejectpar = db.session.query(Application).filter_by(status="Rejected").count()
        return render_template('staffportal.html',staff_fullname=staffpar.staff_fullname, staff_username=staffpar.staff_username,countapplication=countapplicationpar,countaccept=countacceptpar,countreject=countrejectpar)

@app.route('/addmodule', methods=['POST', 'GET'])
def addmodule():
    if request.method == 'POST':
        facultyPar = request.form['Faculties']
        moduleName = request.form['Module']

        if facultyPar == "Faculty1":
            module = Faculty1.query.order_by(Faculty1.module_name).all()
            try:
                new_module = Faculty1(module_name=moduleName)
                db.session.add(new_module)
                db.session.commit()
                return render_template('addmodule.html', faculty=module)
            except:
                return("There error adding module")
        elif facultyPar == "Faculty2":
            module = Faculty2.query.order_by(Faculty2.module_name).all()
            try:
                new_module = Faculty2(module_name=moduleName)
                db.session.add(new_module)
                db.session.commit()
                return render_template('addmodule.html', faculty=module)
            except:
                return("There error adding module")
        elif facultyPar == "Faculty3":
            module = Faculty3.query.order_by(Faculty3.module_name).all()
            try:
                new_module = Faculty3(module_name=moduleName)
                db.session.add(new_module)
                db.session.commit()
                return render_template('addmodule.html', faculty=module)
            except:
                return("There error adding module")
    else:
        return render_template('addmodule.html')

@app.route('/approvals')
def database():
    return render_template('approvals.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST' or request.method == 'GET':
        modname = request.args.get('modulename')
        try:
            if modname:
                student = Application.query.filter_by(module_name=modname).first()
                if student:
                    return render_template('approvals.html', students=[student])
                else:
                    return render_template('approvals.html', error=True)
        except:
            return render_template('approvals.html', error=True)
    else:
        return render_template('approvals.html', error=False)

@app.route('/sort', methods=['GET', 'POST'])
def sort():
    if request.method == 'POST' or request.method == 'GET':
        sort = request.args.get('sort-by')
        order = request.args.get('sort-in')
        if order == "asc" :
            try:
                students = Application.query.order_by(getattr(Application, sort).asc()).all()
                if students:
                    return render_template('approvals.html', students=students)
                else:
                    return render_template('approvals.html', error=True)
            except:
                return render_template('approvals.html', error=True)
        elif order == "desc" :
            try:
                students = Application.query.order_by(getattr(Application, sort).desc()).all()
                if students:
                    return render_template('approvals.html', students=students)
                else:
                    return render_template('approvals.html', error=True)
            except:
                return render_template('approvals.html', error=True)
    else:
        return render_template('approvals.html', error=False)

@app.route('/accept', methods=['GET', 'POST'])
def accept():
    if request.method == 'POST':
        usernamepar = request.form['username']
        student = db.session.query(Student).filter_by(username=usernamepar).first()     

        if student:
            students = db.session.query(Student).filter_by(username=usernamepar).first()
            try:
                email_sender= 'shais.mobileliteracy@gmail.com'
                email_password= 'ectualwggcwopgmy'

                email_receiver = students.email

                subject = "Application Status"
                body = """
                You have been Accepted to tutor please come to the relevant Faculty office for interview"""

                em= EmailMessage()
                em['From'] = email_sender
                em['To'] = email_receiver
                em['subject'] = subject
                em.set_content(body)

                context = ssl.create_default_context()

                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
                    smtp.sendmail(email_sender, email_receiver, em.as_string())
                
                return render_template('login.html')
            except:
                return render_template('approvals.html', error="error occured,Check Connection")      
        else:
           return render_template('approvals.html', error="Please enter the correct Username to receive your password!") 
    else:
        return render_template('approvals.html', error=False)
    
@app.route('/reject', methods=['GET', 'POST'])
def reject():
    if request.method == 'POST':
        usernamepar = request.form['username']
        student = db.session.query(Student).filter_by(username=usernamepar).first()     

        if student:
            students = db.session.query(Student).filter_by(username=usernamepar).first()
            try:
                email_sender= 'shais.mobileliteracy@gmail.com'
                email_password= 'ectualwggcwopgmy'

                email_receiver = students.email

                subject = "Application Status "
                body = """
                You have been rejected as a tutor visit the relevant Faculty office for more information"""

                em= EmailMessage()
                em['From'] = email_sender
                em['To'] = email_receiver
                em['subject'] = subject
                em.set_content(body)

                context = ssl.create_default_context()

                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
                    smtp.sendmail(email_sender, email_receiver, em.as_string())
                
                return render_template('login.html')
            except:
                return render_template('approvals.html', error="error occured,Check Connection")      
        else:
           return render_template('approvals.html', error="Please enter the correct Username to receive your password!") 
    else:
        return render_template('approvals.html', error=False)

if __name__ == '__main__':
    app.run(debug=True)