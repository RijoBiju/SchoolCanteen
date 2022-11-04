from tkinter import *
from tkinter.ttk import *
import mysql.connector
from tkinter import messagebox
from tkinter import ttk
import datetime
import csv

mydb = mysql.connector.connect(host="localhost", username="root", password="adis", database="school_canteen")

window = Tk() # main window to display all functions
app_width = 1200
app_height = 400

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height /2)

window.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")
labello = Label(window, text="WELCOME TO SCHOOL CANTEEN", font="-weight bold")
labello.grid(row=0, column=3)
window.title("School Canteen")


def showtheting(): # to show the menu 
    new_ting = Toplevel()

    app_width = 800
    app_height = 200

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height /2)

    new_ting.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")

    mycursor = mydb.cursor()

    height = "SELECT count(*) FROM information_schema.columns WHERE table_name = 'menu'"

    mycursor.execute(height)

    table = mycursor.fetchall()

    for row in table:
        x = row

    query = "SELECT * FROM menu "

    mycursor.execute(query)

    table = mycursor.fetchall()

    frame = Frame(new_ting)
    frame.grid(row=2, column=0, columnspan=10)

    tree = ttk.Treeview(frame, columns=(1, 2, 3, 4, 5), height=x, show="headings")
    tree.grid(row=2, column=0, columnspan=10)

    tree.heading(1, text="Serial_Number")
    tree.heading(2, text="Food_Item")
    tree.heading(3, text="Cost")
    tree.heading(4, text="Quantity")
    tree.heading(5, text="Category")

    tree.column(1, width=100)
    tree.column(2, width=170)
    tree.column(3, width=100)
    tree.column(4, width=100)
    tree.column(5, width=100)

    for val in table:
        tree.insert('', 'end', values=(val[0], val[1], val[3], val[4], val[2]))


def pudiyawindow(): #takes details to add food item to MySQL table
    global food_item
    global cost
    global quantity
    global category
    global new

    new = Toplevel()
    app_width = 600
    app_height = 200

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height /2)

    new.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")

    food_item = Entry(new, width=20)
    food_item_label = Label(new, text="Food item")
    food_item.grid(row=0, column=2)
    food_item_label.grid(row=0, column=1, sticky=E)

    cost = Entry(new, width=20)
    cost_label = Label(new, text="Cost of food item")
    cost.grid(row=1, column=2)
    cost_label.grid(row=1, column=1, sticky=E)

    quantity = Entry(new, width=20)
    quantity_label = Label(new, text="Quantity of food item")
    quantity.grid(row=2, column=2)
    quantity_label.grid(row=2, column=1, sticky=E)

    category = Entry(new, width=20)
    category_label = Label(new, text="Category of food item")
    category.grid(row=3, column=2)
    category_label.grid(row=3, column=1, sticky=E)

    add_records = Button(new, text="Add records to database", command=rowaddcheyyuva)
    add_records.grid(row=4, column=0, columnspan=2, ipadx=50)


def rowaddcheyyuva(): # adds the new food item to the MySQL table

    mycursor = mydb.cursor()

    food_item_get = food_item.get()
    cost_get = cost.get()
    quantity_get = quantity.get()
    category_get = category.get()

    values = "INSERT INTO menu (Food_Item, Cost, Quantity, Category)" \
             "VALUES ('{0}', {1}, {2}, '{3}')".format(food_item_get, cost_get, quantity_get, category_get)

    question = messagebox.askyesno("Assurance", "Are you sure you want to add this food item to the menu?")

    if question == 1:
        mycursor.execute(values)
        
        food_item.delete(0, 'end')
        cost.delete(0, 'end')
        quantity.delete(0, 'end')
        category.delete(0, 'end')

        added = Label(new, text="\n The specified food item has been added")
        added.grid(row=5, column=0, columnspan=2)

    elif question == 0:
        food_item.delete(0, 'end')
        cost.delete(0, 'end')
        quantity.delete(0, 'end')
        category.delete(0, 'end')

        reaction = Label(new, text="The specified food item has not been added")
        reaction.grid(row=5, column=0, columnspan=2)
        new.destroy()

    mydb.commit()


def aduthawindow(): # takes details on which food item is to be deleted/removed
    global new_window
    global delete_food

    new_window = Toplevel()

    app_width = 600
    app_height = 200

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height /2)

    new_window.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")

    delete_food = Entry(new_window, width=30)
    delete_food_label = Label(new_window, text="Food item to delete")
    delete_food.grid(row=0, column=2)
    delete_food_label.grid(row=0, column=1, sticky=E)

    delete_records = Button(new_window, text="Delete food item", command=deletecheyyam)
    delete_records.grid(row=1, column=0, columnspan=2, ipadx=45)


def deletecheyyam(): # deletes the above mentioned food item
    mycursor = mydb.cursor()

    delete_food_get = delete_food.get()

    query = "DELETE FROM menu WHERE Food_Item = '" + delete_food_get + "'"

    answer = messagebox.askyesno("Assurance", "Are you sure you want to delete this food item from the menu?")

    if answer == 1:
        mycursor.execute(query)

        delete_food.delete(0, 'end')

        deleted = Label(new_window, text="\n The specified food item has been deleted", font="-weight bold")
        deleted.grid(row=8, column=0, columnspan=2)

    elif answer == 0:
        delete_food.delete(0, 'end')

        reaction = Label(new_window, text="\n The specified food item has not been deleted", font="-weight bold")
        reaction.grid(row=8, column=0, columnspan=2)

    mydb.commit()


def nextwindow(): # takes details on which food item should be found
    global next_window
    global search_food

    next_window = Toplevel()
    app_width = 600
    app_height = 200

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height /2)

    next_window.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")

    search_food = Entry(next_window, width=30)
    search_food_label = Label(next_window, text="Food category to search")
    search_food.grid(row=0, column=2)
    search_food_label.grid(row=0, column=1, sticky=E)

    kandpikkaam = Button(next_window, text="Find food in this category", command=kandpidikkada)
    kandpikkaam.grid(row=1, column=0, columnspan=2, ipadx='50')


def kandpidikkada(): # uses the above details to get output from mysql
    mycursor = mydb.cursor()

    search_food_get = search_food.get()

    height = "SELECT count(*) FROM information_schema.columns WHERE table_name = 'menu'"

    mycursor.execute(height)

    table = mycursor.fetchall()

    for row in table:
        x = row[0]

    query = "SELECT * FROM menu WHERE Category = '" + search_food_get + "'"

    mycursor.execute(query)

    table = mycursor.fetchall()
    frame = Frame(next_window)
    frame.grid(row=2, column=0, columnspan=10)

    tree = ttk.Treeview(frame, columns=(1, 2, 3, 4, 5), height=x, show="headings")
    tree.grid(row=2, column=0, columnspan=10)

    tree.heading(1, text="Serial_Number")
    tree.heading(2, text="Food_Item")
    tree.heading(3, text="Cost")
    tree.heading(4, text="Quantity")
    tree.heading(5, text="Category")

    tree.column(1, width=100)
    tree.column(2, width=170)
    tree.column(3, width=100)
    tree.column(4, width=100)
    tree.column(5, width=100)

    for val in table:
        tree.insert('', 'end', values=(val[0], val[1], val[2], val[3], val[4]))

    submit = Button(next_window, text="Done", command=done)
    submit.grid(row=4, column=0, columnspan=10)


def done(): # to search for another food item
    answer = messagebox.askyesno("Assurance", "Would you like to see another category of food?")

    if answer == 1:
        search_food.delete(0, 'end')
        kandpidikkada()

    elif answer == 0:
        next_window.destroy()


def nallawindow(): # ordering data
    global nallatha
    global order_food
    global order_id
    global order_date
    global order_quantity

    nallatha = Toplevel()

    app_width = 800
    app_height = 300

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height /2)

    nallatha.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")

    order_date = datetime.datetime.now()

    order_food = Entry(nallatha, width=30)
    order_food_label = Label(nallatha, text="Food item")
    order_food.grid(row=0, column=2)
    order_food_label.grid(row=0, column=1, sticky=E)

    order_quantity = Entry(nallatha, width=30)
    order_quantity_label = Label(nallatha, text="Amount of food ordered")
    order_quantity.grid(row=1, column=2)
    order_quantity_label.grid(row=1, column=1, sticky=E)

    samosa = Button(nallatha, text="Samosa", command=samosaa)
    samosa.grid(row=3, column=1, ipadx=38)

    cutlet = Button(nallatha, text="Cutlet", command=cutlett)
    cutlet.grid(row=3, column=2, ipadx=40)

    chicken_sandwich = Button(nallatha, text="Chicken Sandwich", command=chickensandwichh)
    chicken_sandwich.grid(row=3, column=3, ipadx=10)

    vegetable_sandwich = Button(nallatha, text="Vegetable Sandwich", command=vegetablesandwichh)
    vegetable_sandwich.grid(row=4, column=1, ipadx=6)

    cheese_sandwich = Button(nallatha, text="Cheese Sandwich", command=cheesesandwichh)
    cheese_sandwich.grid(row=4, column=2, ipadx=10)

    chicken_pasta = Button(nallatha, text="Chicken Pasta", command=chickenpastaa)
    chicken_pasta.grid(row=4, column=3, ipadx=21)

    chicken_biryani = Button(nallatha, text="Chicken Biryani", command=chickenbiryanii)
    chicken_biryani.grid(row=5, column=1, ipadx=18)

    vegetable_biryani = Button(nallatha, text="Vegetable Biryani", command=vegetablebiryanii)
    vegetable_biryani.grid(row=5, column=2, ipadx=10)

    mutton_biryani = Button(nallatha, text="Mutton Biryani", command=muttonbiryanii)
    mutton_biryani.grid(row=5, column=3, ipadx=18)

    chocolate_milkshake = Button(nallatha, text="Chocolate Milkshake", command=chocolatemilkshakee)
    chocolate_milkshake.grid(row=6, column=1, ipadx=4)

    strawberry_milkshake = Button(nallatha, text="Strawberry Milkshake", command=strawberrymilkshakee)
    strawberry_milkshake.grid(row=6, column=2, ipadx=1)

    cold_coffee = Button(nallatha, text="Cold Coffee", command=coldcoffeee)
    cold_coffee.grid(row=6, column=3, ipadx=26)

    apple_juice = Button(nallatha, text="Apple Juice", command=applejuicee)
    apple_juice.grid(row=7, column=0, ipadx=29)

    orange_juice = Button(nallatha, text="Orange Juice", command=orangejuicee)
    orange_juice.grid(row=7, column=2, ipadx=23)

    mango_juice = Button(nallatha, text="Mango Juice", command=mangojuicee)
    mango_juice.grid(row=7, column=3, ipadx=24)

    order = Button(nallatha, text="Order", command=ordercheyyam)
    order.grid(row=8, column=1, columnspan=3, ipadx=200)


def samosaa():
    order_food.insert(0, "Samosa")


def cutlett():
    order_food.insert(0, "Cutlet")


def chickensandwichh():
    order_food.insert(0, "Chicken Sandwich")


def vegetablesandwichh():
    order_food.insert(0, "Vegetable Sandwich")


def cheesesandwichh():
    order_food.insert(0, "Cheese Sandwich")


def chickenpastaa():
    order_food.insert(0, "Chicken Pasta")


def chickenbiryanii():
    order_food.insert(0, "Chicken Biryani")


def vegetablebiryanii():
    order_food.insert(0, "Vegetable Biryani")


def muttonbiryanii():
    order_food.insert(0, "Mutton Biryani")


def chocolatemilkshakee():
    order_food.insert(0, "Chocolate Milkshake")


def strawberrymilkshakee():
    order_food.insert(0, "Strawberry Milkshake")


def coldcoffeee():
    order_food.insert(0, "Cold Coffee")


def applejuicee():
    order_food.insert(0, "Apple Juice")


def orangejuicee():
    order_food.insert(0, "Orange Juice")


def mangojuicee():
    order_food.insert(0, "Mango Juice")


def ordercheyyam():
    mycursor = mydb.cursor()

    query_1 = "INSERT into order_table(order_date, food_item, quantity)" \
              "values('{0}', '{1}', {2})".format(order_date, order_food.get(), order_quantity.get())

    query_2 = "select Cost from menu where Food_Item = '" + str(order_food.get()) + "'"

    query_3 = "select order_id from order_table"

    mycursor.execute(query_1)
    mycursor.execute(query_2)

    costt = mycursor.fetchall()

    row_ting = 0

    for row in costt:
        price = int(order_quantity.get()) * int(row[0])

    mycursor.execute(query_3)

    boss = mycursor.fetchall()

    for i in boss:
        row_ting = i[-1]

    query_4 = "update order_table set total_price = total_price + " + str(price) + " where order_id = " + str(row_ting)

    query_5 = "update menu set quantity = quantity - " + str(order_quantity.get()) +\
                  " where food_item = '" + str(order_food.get()) + "'"

    mycursor.execute(query_4)
    mycursor.execute(query_5)

    mydb.commit()

    kaniku = Label(nallatha, text="\n The order has been added")
    kaniku.grid(row=9, column=2, columnspan=2)


def updatecheyyada():
    global verae_oru_window
    global foo_item 
    global updation

    verae_oru_window = Toplevel()

    app_width = 800
    app_height = 300

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height /2)

    verae_oru_window.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")

    foo_item = Entry(verae_oru_window, width=20)
    foo_item_label = Label(verae_oru_window, text="Enter food item to update")
    foo_item.grid(row=0, column=2)
    foo_item_label.grid(row=0, column=1, sticky=E)

    updation = Entry(verae_oru_window, width=20)
    updation_label = Label(verae_oru_window, text="Enter amount to be added")
    updation.grid(row=1, column=2)
    updation_label.grid(row=1, column=1, sticky=E)

    updating_time = Button(verae_oru_window, text="Increase Quantity", command=timetoupdate)
    updating_time.grid(row=2, column=0, columnspan=2, ipadx=100)


def timetoupdate():

    mycursor = mydb.cursor()

    code = "update menu set quantity = quantity + " + str(updation.get()) + " where food_item = '" + str(foo_item.get()) + "'"

    mycursor.execute(code)

    mydb.commit()

    kaniku = Label(verae_oru_window, text="\n The amount of food has been updated")
    kaniku.grid(row=3, column=2, columnspan=2)


def veruthawindow():
    global verutha_window
    global year
    global months

    verutha_window = Toplevel()

    app_width = 800
    app_height = 300

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height /2)

    verutha_window.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")

    year = Entry(verutha_window, width=20)
    year_label = Label(verutha_window, text="Enter year of required data")
    year.grid(row=0, column=2)
    year_label.grid(row=0, column=1, sticky=E)

    months = Entry(verutha_window, width=20)
    month_label = Label(verutha_window, text="Enter month of required data")
    months.grid(row=1, column=2)
    month_label.grid(row=1, column=1, sticky=E)

    report_show = Button(verutha_window, text="Show report of specified timeline", command=kanikkaam)
    report_show.grid(row=2, column=0, columnspan=2, ipadx=100)


def kanikkaam():
    global count
    global year_get

    mycursor = mydb.cursor()

    height = "SELECT count(*) FROM information_schema.columns WHERE table_name = 'order_table'"

    mycursor.execute(height)

    table = mycursor.fetchall()

    for row in table:
        x = row[0]

    months_get = months.get()

    year_get = year.get()

    count = 0

    if months_get.upper() == 'JANUARY' or months_get == 1:
        count += 1

    elif months_get.upper() == 'FEBRUARY' or months_get == 2:
        count += 2

    elif months_get.upper() == 'MARCH' or months_get == 3:
        count += 3

    elif months_get.upper() == 'APRIL' or months_get == 4:
        count += 4

    elif months_get.upper() == 'MAY' or months_get == 5:
        count += 5

    elif months_get.upper() == 'JUNE' or months_get == 6:
        count += 6

    elif months_get.upper() == 'JULY' or months_get == 7:
        count += 7

    elif months_get.upper() == 'AUGUST' or months_get == 8:
        count += 8 

    elif months_get.upper() == 'SEPTEMBER' or months_get == 9:
        count += 9

    elif months_get.upper() == 'OCTOBER' or months_get == 10:
        count += 10

    elif months_get.upper() == 'NOVEMBER' or months_get == 11:
        count += 11

    elif months_get.upper() == 'DECEMBER' or months_get == 12:
        count += 12

    queries = "select * from order_table where month(order_date) = '" + str(count) + "'" + \
              "and year(order_date) = '" + str(year_get) + "'"

    mycursor.execute(queries)

    table = mycursor.fetchall()

    frames = Frame(verutha_window)
    frames.grid(row=4, column=0, columnspan=20)

    tree = ttk.Treeview(frames, columns=(1, 2, 3, 4, 5), height=x, show="headings")
    tree.grid(row=4, column=0, columnspan=20)

    tree.heading(1, text="Order_ID")
    tree.heading(2, text="Order_Date")
    tree.heading(3, text="Food_Item")
    tree.heading(4, text="Quantity")
    tree.heading(5, text="Total_Price")

    tree.column(1, width=65)
    tree.column(2, width=70)
    tree.column(3, width=130)
    tree.column(4, width=65)
    tree.column(5, width=65)

    for val in table:
        tree.insert('', 'end', values=(val[0], val[1], val[2], val[3], val[4]))

    saves = Button(verutha_window, text="Save report", command=savecheyyada)
    saves.grid(row=8, column=0)

    venda = Button(verutha_window, text="Exit", command=vidada)
    venda.grid(row=8, column=1)


def savecheyyada():
    mycursor = mydb.cursor()

    queriess = "select * from order_table where month(order_date) = '" + str(count) + "'" + \
               "and year(order_date) = '" + str(year_get) + "'"

    mycursor.execute(queriess)

    rows = mycursor.fetchall()

    column_names = [i[0] for i in mycursor.description]
    fp = open('C:/Users/RIJO/Desktop/data.csv', 'w')
    myFile = csv.writer(fp, lineterminator = '\n')
    myFile.writerow(column_names)   
    myFile.writerows(rows)
    fp.close()

    kazhinju = Label(verutha_window, text="The report has been saved", font="-weight bold")
    kazhinju.grid(row=9, column=0)


def vidada():
    verutha_window.destroy()


def pogaam():
    window.destroy()


show_record = Button(window, text="Show menu", command=showtheting)
show_record.grid(row=1, column=3, ipadx=41)

add_record_frame = Frame(window)
add_record_frame.grid(row=2, column=0)
add_record = Button(window, text="Add food item to the menu", command=pudiyawindow)
add_record.grid(row=4, column=2, padx=150)

delete_record_frame = Frame(window)
delete_record_frame.grid(row=4, column=0)
delete_record = Button(window, text="Delete food item from menu", command=aduthawindow)
delete_record.grid(row=6, column=3, ipadx=0)

search_record_frame = Frame(window)
search_record_frame.grid(row=6, column=0)
search_record = Button(window, text="Search food item", command=nextwindow)
search_record.grid(row=8, column=3, ipadx=30)

order_record_frame = Frame(window)
order_record_frame.grid(row=8, column=0)
order_record = Button(window, text="Order food item", command=nallawindow)
order_record.grid(row=10, column=3, ipadx=32)

update_record_frame = Frame(window)
update_record_frame.grid(row=10, column=0)
update_record = Button(window, text="Update quantity", command=updatecheyyada)
update_record.grid(row=12, column=3, ipadx=30)

report_record_frame = Frame(window)
report_record_frame.grid(row=12, column=0)
report_record = Button(window, text="Report", command=veruthawindow)
report_record.grid(row=14, column=3, ipadx=40)

exit_record_frame = Frame(window)
exit_record_frame.grid(row=14, column=0)
exit_record = Button(window, text="Exit", command=pogaam)
exit_record.grid(row=16, column=3, ipadx=40)


window.mainloop()