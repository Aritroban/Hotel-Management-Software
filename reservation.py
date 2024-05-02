import * from main

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
