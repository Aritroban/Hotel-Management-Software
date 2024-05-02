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
