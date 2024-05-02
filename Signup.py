import * from main

@app.route('/signup', methods =['GET', 'POST'])
def signup():
    if request.method=='POST':
        userDetails=request.form
        name= userDetails['name']
        email= userDetails['email']
        password= userDetails['password']
        confirm_password=userDetails['confirm_password']
        cur = mysql.connection.cursor()

        scanemail= cur.execute("select * from user where email='{}'".format(email,))
        if scanemail>0:
            #message = Markup("<p>Email already in use</p>")
            flash("Email already in use")
            return redirect('/signup')

        if password==confirm_password:
            cur.execute("insert into user(name, email, password) values(%s, %s, %s)",(name,email, password))
            mysql.connection.commit()
            cur.close()
            return render_template('index.html')

    return render_template('signup.html')
