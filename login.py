import * from main

@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method=='POST':
        userDetails=request.form
        email= userDetails['email']
        password= userDetails['password']
        cur = mysql.connection.cursor()

        scanemail= cur.execute("select * from user where email='{}'".format(email,))
        if scanemail<=0:
            #message = Markup("<p>Email already in use</p>")
            flash("Email does not exist")
            return redirect('/login')
        else:
            cur.execute("select * from user where email='{}'".format(email, ))
            records=cur.fetchone()
            if password==records[2]:
                cur.execute("select * from user where email='{}'".format(email, ))
                Details = cur.fetchall()
                return render_template('booking.html', Details=Details)

            else:
                flash("incorrect password")
                return redirect('/login')



    return render_template('login.html')
    cur.close()
