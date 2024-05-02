from flask import Flask, render_template, request, redirect, flash
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from datetime import *
import stripe

stripe.api_key = "your_stripe_secret_key"  # Replace with your actual secret key



app=Flask(__name__)

app.config['SECRET_KEY'] = 'hjshjhdjah kaefjshkjdhjs'
app.config['MYSQL_HOST']='sql5.freemysqlhosting.net'
app.config['MYSQL_USER']='sql5489484'
app.config['MYSQL_PASSWORD']='yIiGRUTHjD'
app.config['MYSQL_DB']='sql5489484'


mysql=MySQL(app)



app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = '465'
app.config['MAIL_USERNAME'] = 'hotelpasstrack@gmail.com'
app.config['MAIL_PASSWORD'] = 'hotelservice'
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


#signup begins
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
#signup ends

#directing to login
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

@app.route('/food', methods=["GET", "POST"])
def food():
    burritoPrice = 7.00
    sushiPrice = 10.00
    wingsPrice = 10.00

    if request.method == "POST":
        ''' fetch form data '''
        foodDetails = request.form

        burrito = foodDetails["burrito"]
        if burrito == '':
            burrito = 0

        sushi = foodDetails["sushi"]
        if sushi == '':
            sushi = 0

        wings = foodDetails["wings"]
        if wings == '':
            wings = 0

        email = foodDetails["email"]

        #Import data into food_orders table in database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO food_orders(sushi, burrito, wings, email) VALUES(%s, %s, %s, %s)", (sushi, burrito, wings, email))
        mysql.connection.commit()
        cur.close()

        # Getting order ID
        cur = mysql.connection.cursor()
        cur.execute("select * from food_orders order by ID DESC LIMIT 1")
        result = cur.fetchall()
        order = result[0]
        orderID = order[0]

        # Calculating total prices
        burritoTotal = float(burrito) * burritoPrice
        burritoFormat = "{:.2f}".format(burritoTotal)

        sushiTotal = float(sushi) * sushiPrice
        sushiFormat = "{:.2f}".format(sushiTotal)

        wingsTotal = float(wings) * wingsPrice
        wingsFormat = "{:.2f}".format(wingsTotal)

        total = burritoTotal + sushiTotal + wingsTotal
        subtotal = "{:.2f}".format(total)
        tax = total * 0.08
        total += tax
        tax = "{:.2f}".format(tax)
        total = "{:.2f}".format(total)

        try:
            # Create PaymentIntent on the server-side
            intent = stripe.PaymentIntent.create(
                amount=int(total * 100),  # Convert to cents
                currency="usd",
                description="Food Order",
            )

            # Pass the client secret to the client-side for confirmation
            return jsonify({"clientSecret": intent.client_secret})

        except stripe.error.StripeError as e:
            return jsonify({"error": str(e)}), 400

        @app.route('/confirm-payment', methods=['POST'])
    def confirm_payment():
        data = request.get_json()
    
        try:
            # Confirm the PaymentIntent with the provided token
            stripe.PaymentIntent.confirm(data['paymentIntentId'], data['token'])
    
            # Process successful payment: update database, send emails, etc.
            return jsonify({'status': 'success'})
    
        except stripe.error.StripeError as e:
            return jsonify({'error': str(e)}), 400


        # Email set up
        msg = Message("PassTrack Food Order Confirmation", sender='passtrackservices@gmail.com',
                      recipients=[email])

        # Email body formatting
        data = {"sub": subtotal, "ID": orderID, "tax": tax, "total": total ,"burritoF": burritoFormat, "sushiF": sushiFormat, "wingsF": wingsFormat, "burritoN": burrito, "sushiN": sushi, "wingsN": wings}
        msg.html = render_template("foodConfirmationEmailTemplate.html", data=data)
        mail.send(msg)
        return "success: food confirmation sent to " + email   # Need to create a confirmation webpage
    return render_template("newerfood.html")



#room booking begins
@app.route('/result', methods =['GET', 'POST'])
def reservation():
    if request.method == "POST":
        bookingDetails = request.form
        checkin = bookingDetails['chekin']
        checkout = bookingDetails['chekout']
        adult = bookingDetails['adult']
        children = bookingDetails['children']
        email = bookingDetails['email']

        rooms = bookingDetails['rooms']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO booking_info(checkin, checkout, adult, children, email, rooms) VALUES(%s, %s, %s, %s, %s, %s)", (checkin, checkout, adult, children, email, rooms))
        mysql.connection.commit()
        cur.close()
        msg = Message("Booking Confirmation Pass Track", sender='hotelpasstrack@gmail.com', recipients=[email])
        msg.body = "This email is to confirm your room booking at Hotel California through PassTrack software"

        mail.send(msg)
        flash("Your request has been completed")
        return render_template('booking.html')
    return render_template('booking.html')


#room booking ends

#redirect to users list begins
@app.route('/admin', methods =['GET', 'POST'])
def users():
    if request.method == "POST":
        try:
            details = request.form
            newRooms = int(details['rooms'])
            cur6 = mysql.connection.cursor()
            cur6.execute(' update room_track set total={}'.format(newRooms))
            cur6.execute("select sum(rooms) from booking_info where status ='active'")
            occupiedRooms = cur6.fetchone()
            available_rooms = newRooms - occupiedRooms[0]
            cur6.execute("update room_track set available='{}'".format(available_rooms))
            mysql.connection.commit()
            return redirect('/admin')
        except:
            return redirect('/admin')

    cur=mysql.connection.cursor()
    cur1=mysql.connection.cursor()
    cur2=mysql.connection.cursor()
    result=cur.execute("select *from user")
    cur1.execute("select * from booking_info where status='active'")
    cur2.execute("select * from room_track")
    cur3=mysql.connection.cursor()
    cur3.execute("select * from booking_info order by status")
    cur4 = mysql.connection.cursor()
    cur4.execute("select * from food_orders order by ID desc")
    #if result>0:
    userDetails=cur.fetchall()
    reserve=cur1.fetchall()
    rooms_active=cur2.fetchall()
    rooms_all=cur3.fetchall()
    food=cur4.fetchall()
    cur3.close()
    cur3 = mysql.connection.cursor()
    cur3.execute("update booking_info set status='inactive' where checkout<=curdate()")
    cur3.execute("select sum(rooms) from booking_info where status='active'")
    sum_value = cur3.fetchone()
    cur3.execute("update room_track set occupied='{}'".format(sum_value[0], ))
    cur3.execute("select * from room_track")
    cur3.execute("select sum(total) from room_track")
    totalRooms = cur3.fetchone()
    available_rooms = int(totalRooms[0])- sum_value[0]
    cur3.execute("update room_track set available='{}'".format(available_rooms))
    mysql.connection.commit()
    cur3.close()






    return render_template('users.html', userDetails=userDetails, reserve=reserve, rooms_active=rooms_active,rooms_all=rooms_all,food=food)
    cur.close()
    cur1.close()
    cur2.close()
    cur3.close()
    cur4.close()
    cur6.close()



#redirect to users list ends



if __name__== '__main__':
    app.run(debug=True)
