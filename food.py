import * from main

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

        # Email set up
        msg = Message("PassTrack Food Order Confirmation", sender='passtrackservices@gmail.com',
                      recipients=[email])

        # Email body formatting
        data = {"sub": subtotal, "ID": orderID, "tax": tax, "total": total ,"burritoF": burritoFormat, "sushiF": sushiFormat, "wingsF": wingsFormat, "burritoN": burrito, "sushiN": sushi, "wingsN": wings}
        msg.html = render_template("foodConfirmationEmailTemplate.html", data=data)
        mail.send(msg)
        return "success: food confirmation sent to " + email   # Need to create a confirmation webpage
    return render_template("newerfood.html")
