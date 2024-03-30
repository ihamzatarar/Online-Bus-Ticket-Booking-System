
from imports import *

#---------------------------------------------------- Creating Bus Objects -----------------------------------------------------------  
buses = {}

with open('TextFiles/buses.txt', "r") as f:                                 #Filling
    for line in f:
        Bus=line.rstrip("\n").split(',')                                    #Polymorphism
        if Bus[0][0] == 'e':
            buses[Bus[0]] = economyClass(Bus[0],Bus[1],Bus[2])
        elif Bus[0][0] == 'b':
            buses[Bus[0]] = businessClass(Bus[0],Bus[1],Bus[2])

#---------------------------------------------------- Creating Route Objects -----------------------------------------------------------  

routes = {}

with open("TextFiles/routes.txt", 'r') as f:                                  #Filling
    for line in f:
        Route = line.rstrip("\n").split(',')
        routes[Route[0]] = route(Route[0],Route[1],Route[2],Route[3],Route[4],Route[5],Route[6],Route[7])

#---------------------------------------------------- Creating Scheule Objects -----------------------------------------------------------  

Schedule = schedule()

with open("TextFiles/routes-buses.txt", 'r') as f:                              #Filling
    for line in f:
        pair = line.rstrip("\n").split(',')
        if pair[1] in buses and pair[0]:
            Schedule.add(buses[pair[1]],routes[pair[0]])                        #Aggregation

#---------------------------------------------------- Creating Contact us Object -----------------------------------------------------------  


Contact = contactUs('ihamzatarar14@gmail.com','+923056199042')

#---------------------------------------------------- Booking Class -----------------------------------------------------------  

class booking:   
    def __init__(self,customer):                                        #Aggregation
        self.customer = customer
        self.discount = discount(customer)                              #Composition
    
    def makeReservation(self,CNIC,routeId,busClass,seatNo,Date):
        if busClass == 'Economy Class':
            busClass = 'e'
        else:                                                            #Polymorphism
            busClass = 'b'
        routeId = routeId
        busid = None
        
        with open("TextFiles/routes-buses.txt", "r") as f:                #Filling
            for line in f:
                a=line.rstrip('\n').split(',')
                if a[0] == routeId and a[1][0] == busClass:
                    busid = a[1]
                    break
        
        if  buses[busid].seats[seatNo].availabilityFlag == 1:
            buses[busid].seats[seatNo].availabilityFlag = 0
            buses[busid].seats[seatNo].occupant = self.customer
        else:
            print('Seat is not available')
            return False
            
        index = 0
        with open("TextFiles/reservations.txt", "r") as f:                               #Filling
            for iline, line in enumerate(f, 1):
                index = str(iline)
        with open("TextFiles/reservations.txt", "a") as f:
                f.write(str(index)+','+CNIC+','+routeId+','+busClass+','+seatNo+','+Date+'\n')
        return index


    def cancelReservation(TicketNo):
        check = False
        with open("TextFiles/reservations.txt", "r") as input:                           #Filling
            with open("temp.txt", "w") as output:
                for line in input:
                    e = line.split(',')
                    if str(e[0]) != TicketNo:
                        output.write(line)
                    else:
                        check = True
            if check:
                with open('TextFiles/reservations.txt','r') as f:                        #Filling
                    for line in f:
                        a=line.rstrip('\n').split(',')
                        if str(a[0]) == str(TicketNo):
                            busid = a[3]+a[2]
                            buses[busid].seats[a[4]].occupant = None
                        
        os.replace('temp.txt', 'TextFiles/reservations.txt')
                        
        return check

    def checkMyReservation(CNIC):
        customerBookingList = []
        with open("TextFiles/reservations.txt", "r") as f:                               #Filling
            for line in f:
                a= line.rstrip("\n").split(',')
                if a[1] == CNIC:
                    customerBookingList.append(a)
            return customerBookingList


#---------------------------------------------------- Discount Class -----------------------------------------------------------  

class discount:
    def __init__(self,customer):                                                         #Aggregation                                        
        self.customer = customer
    def checkDiscountEligibility(self,ticket1,ticket2,ticket3):
        templst = []
        with open('TextFiles/reservations.txt','r') as f:
            for line in f:
                a = line.rstrip('\n').split(',')
                templst.append(a[0])
            if ticket1 and ticket2 and ticket3 in templst:
                return True
            return False

#---------------------------------------------------- Customer and Admin Object -----------------------------------------------------------  

activeUser = None
Admin =  None
 
#---------------------------------------------------- Login Page -----------------------------------------------------------  

class FirstPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        load = Image.open("images/login.jpg")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image=photo
        label.place(x=0,y=0)
        
        Label = tk.Label(self, text="Welcome Back", bg = "white",fg = "#1c345b", font=("Arial", 25))
        Label.place(x=520, y=100)
        
        L1 = tk.Label(self, text="Username", font=("Arial Bold", 15),bg='white', fg='#1c345b')
        L1.place(x=500, y=150)
        T1 = tk.Entry(self, width = 25)
        T1.place(x=500, y=200)
        
        L2 = tk.Label(self, text="Password", font=("Arial Bold", 15), bg='white',fg='#1c345b')
        L2.place(x=500, y=250)
        T2 = tk.Entry(self, width = 25, show='*')
        T2.place(x=500, y=300)
        
        def verify():
            global activeUser
            try:
                if customer.verify(T1.get(), T2.get()):
                    list1 = []
                    with open('TextFiles/userInfo.txt','r') as f:                                   #Filling
                        for Line in f:
                            list1.append(Line.rstrip("\n"))
                        for e in list1:
                            lst = e.split(',')
                            if T1.get() == lst[1]:
                                activeUser = customer(lst[0],lst[1],lst[2],lst[3],lst[4])         
                    controller.show_frame(HomePage)
                    
                    
                else:
                    messagebox.showinfo("Error", "Please provide correct username and password!!")
            except:
                messagebox.showinfo("Error", "Please provide correct username and password!!")
         
        B1 = tk.Button(self, text="Login", font=("Arial", 15),fg='#1c345b', command=verify)
        B1.place(x=530, y=350)
        
        def register():
            window = tk.Tk()
            window.resizable(0,0)

            window.title("Register")
            l1 = tk.Label(window, text="Username:", font=("Arial",15))
            l1.place(x=10, y=10)
            t1 = tk.Entry(window, width=30, bd=5)
            t1.place(x = 200, y=10)
            
            l2 = tk.Label(window, text="Password:", font=("Arial",15))
            l2.place(x=10, y=60)
            t2 = tk.Entry(window, width=30, show="*", bd=5)
            t2.place(x = 200, y=60)
            
            l3 = tk.Label(window, text="Confirm Password:", font=("Arial",15))
            l3.place(x=10, y=110)
            t3 = tk.Entry(window, width=30, show="*", bd=5)
            t3.place(x = 200, y=110)

            l4 = tk.Label(window, text="CNIC:", font=("Arial",15))
            l4.place(x=10, y=170)
            t4 = tk.Entry(window, width=30, bd=5)
            t4.place(x = 200, y=170)

            l5 = tk.Label(window, text="Gender:", font=("Arial",15))
            l5.place(x=10, y=230)
            t5 = tk.Entry(window, width=30, bd=5)
            t5.place(x = 200, y=230)

            l6 = tk.Label(window, text="Age:", font=("Arial",15))
            l6.place(x=10, y=290)
            t6 = tk.Entry(window, width=30, bd=5)
            t6.place(x = 200, y=290)

            l7 = tk.Label(window, text="DOB:", font=("Arial",15))
            l7.place(x=10, y=350)
            t7 = tk.Entry(window, width=30, bd=5)
            t7.place(x = 200, y=350)

            l8 = tk.Label(window, text="Phone No:", font=("Arial",15))
            l8.place(x=10, y=410)
            t8 = tk.Entry(window, width=30, bd=5)
            t8.place(x = 200, y=410)
            
            def check():
                if customer.register(t1.get(),t2.get(),t3.get(),t4.get(),t5.get(),t6.get(),t7.get(),t8.get()):     
                    messagebox.showinfo("Welcome","You are registered successfully!!")
                    if t2.get()!=t3.get():
                        messagebox.showinfo("Error","Your password didn't get match!!")
                else:
                    messagebox.showinfo("Error", "Please fill the complete field!!")
                    
            
            b1 = tk.Button(window, text="Sign up", font=("Arial",15), bg="#ffc22a", command=check)
            b1.place(x=250, y=500)
            window.geometry("600x600")
            window.mainloop()

        def adminLogin():
            window = tk.Tk()
            window.resizable(0,0)
            window.configure(bg="white")
            window.title("Register")
            l1 = tk.Label(window, text="Username:", font=("Arial",15),bg='white')
            l1.place(x=10, y=10)
            t1 = tk.Entry(window, width=30, bd=5)
            t1.place(x = 10, y=60)
            l2 = tk.Label(window, text="Password:", font=("Arial",15),bg='white')
            l2.place(x=10, y=100)
            t2 = tk.Entry(window, width=30, show="*", bd=5)
            t2.place(x = 10, y=150)

            def check():
                if admin.login(t1.get(),t2.get()):
                    global Admin
                    Admin = admin(12,'Boss','Male','50','12/5/1950','Boss@email.com','03056199042')
                    window.destroy()
                    controller.show_frame(AdminHomePage)

                else:
                    messagebox.showinfo("Error", "Please provide correct username and password!!")
            
            
            b1 = tk.Button(window, text="Login", font=("Arial",15), bg="#ffc22a", command=check)
            b1.place(x=100, y=200)
            
            window.geometry("300x250")
            window.mainloop()



        B2 = tk.Button(self, text="Register", bg = "#ffc22a",fg='#1c345b', font=("Arial",15), command=register)
        B2.place(x=640, y=350)

        B2 = tk.Button(self, text="Admin Login", bg = "#ffc22a",fg='#1c345b', font=("Arial",15), command=adminLogin)
        B2.place(x=570, y=400)

#---------------------------------------------------- Booking Object -----------------------------------------------------------  

customerBooking = booking(activeUser)

#---------------------------------------------------- User HomePage -----------------------------------------------------------  

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        load = Image.open("images/homepage.jpg")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image=photo
        label.place(x=0,y=0)

        
        Label = tk.Label(self, text="T&T",bg='#EAE9EE' ,fg = "Black", font=("Arial Bold", 25))
        Label.place(x=110, y=55)

        Button = tk.Button(self, text="Book A Seat", font=("Arial", 15), command=lambda: controller.show_frame(BookingPage))
        Button.place(x=170, y=283)


        Button = tk.Button(self, text="My Bookings", font=("Arial", 15), command=lambda: controller.show_frame(CheckBookingPage))
        Button.place(x=350, y=283)
        
        Button = tk.Button(self, text="Cancel Booking", font=("Arial", 15), command=lambda: controller.show_frame(CancelBookingPage))
        Button.place(x=500, y=283)

        Button = tk.Button(self, text="Check for Discount", font=("Arial", 15), command=lambda: controller.show_frame(DiscountPage))
        Button.place(x=180, y=60)

        Button = tk.Button(self, text="View Schedule", font=("Arial", 15), command=lambda: controller.show_frame(SchedulePage))
        Button.place(x=350, y=60)

        Button = tk.Button(self, text="Contact Us", font=("Arial", 15), command=lambda: contact())
        Button.place(x=500, y=60)
        
        
        Button = tk.Button(self, text="Log Out", font=("Arial", 15),bg='#eae9ee', command=lambda: controller.show_frame(FirstPage))
        Button.place(x=640, y=60)

        def contact():
            details = activeUser.contact(Contact)                                   #Assosiation
            messagebox.showinfo('Contactus', details)

#---------------------------------------------------- BookingPage -----------------------------------------------------------  

class BookingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        load = Image.open("images/booking.png")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image=photo
        label.place(x=0,y=0)

        Label1 = tk.Label(self, text="Enter Your CNIC", font=("Arial", 20))
        Label1.place(x=10, y=100)
        
        Label2 = tk.Label(self, text="Enter Route Id", font=("Arial", 20))
        Label2.place(x=10, y=170)

        Label3 = tk.Label(self, text="Choose Bus", font=("Arial", 20))
        Label3.place(x=10, y=240)

        Label4 = tk.Label(self, text="Choose Seat", font=("Arial", 20))
        Label4.place(x=10, y=310)
        
        Label5 = tk.Label(self, text="Enter Date", font=("Arial", 20))
        Label5.place(x=10, y=380)

        T1 = tk.Entry(self)
        T1.place(x=300, y=100)

        T2 = tk.Entry(self)
        T2.place(x=300, y=170)

        combo1 = Combobox(self)
        combo1.place(x=300,y=240)
        combo1['values'] = ("Economy Class","Business Class")

        combo2 = Combobox(self)
        combo2.place(x=300,y=310)
        combo2['values'] = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30)

        T3 = tk.Entry(self)
        T3.place(x=300, y=380)

        def book():
            ticketNo = customerBooking.makeReservation(T1.get(),T2.get(),combo1.get(),combo2.get(),T3.get())
            if ticketNo == False:
                messagebox.showinfo('Ticketinfo', 'Seat already Taken')
                return
            
            TicketNo = 'Your Ticket No is '+ str(ticketNo)
            messagebox.showinfo('sample 1', TicketNo )
            
            T1.delete(0,'end')
            T2.delete(0,'end')
            T3.delete(0,'end')
            combo1.set('')
            combo2.set('')
           



        Button1 = tk.Button(self, text="Book", font=("Arial", 15), command=lambda: book())
        Button1.place(x=400, y=450)
        Button2 = tk.Button(self, text="Home", font=("Arial", 15), command=lambda: controller.show_frame(HomePage))
        Button2.place(x=650, y=450)
        
#---------------------------------------------------- CancelBookingPage -----------------------------------------------------------  

class CancelBookingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        load = Image.open("images/cancel.png")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image=photo
        label.place(x=0,y=0)
        
        Label1 = tk.Label(self, text="Enter Your Ticket No", font=("Arial", 20))
        Label1.place(x=10, y=100)
        T1 = tk.Entry(self)
        T1.place(x=300, y=100)
        
        def cancelBooking():
            if booking.cancelReservation(str(T1.get())):
                messagebox.showinfo('information','You Reservation is Canceled')
                T1.delete(0,'end')
            else:
                messagebox.showinfo('information','No Reservation To Cancel')
        



        Button1 = tk.Button(self, text="Cancel", font=("Arial", 15), command=lambda: cancelBooking())
        Button1.place(x=400, y=450)
        Button = tk.Button(self, text="Home", font=("Arial", 15), command=lambda: controller.show_frame(HomePage))
        Button.place(x=650, y=450)
        
#---------------------------------------------------- CheckBookingPage -----------------------------------------------------------   

class CheckBookingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        load = Image.open("images/check.jpg")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image=photo
        label.place(x=0,y=0)
        Label1 = tk.Label(self, text="Enter Your CNIC", font=("Arial", 20))
        Label1.place(x=100, y=100)
        T1 = tk.Entry(self)
        T1.place(x=100, y=300)

   

        def checkBooking():
            lst = booking.checkMyReservation(str(T1.get()))
            if len(lst) == 0:
                messagebox.showinfo('information','You have no Reservations')
            else:
                my_tree =ttk.Treeview(self)
                my_tree.place(x=390, y=100)

                my_tree['columns']=("Ticket No","CNIC","Route Id","Bus","Seat No","Date")
                my_tree.column("#0",width=0,stretch=NO)
                my_tree.column("Ticket No",anchor=CENTER,width=60)
                my_tree.column("CNIC",width=60,anchor=CENTER,minwidth=25)
                my_tree.column("Route Id",anchor=CENTER,width=60)
                my_tree.column("Bus",width=60,anchor=CENTER,minwidth=25)
                my_tree.column("Seat No",anchor=CENTER,width=60)
                my_tree.column("Date",anchor=CENTER,width=65)
                 


                my_tree.heading("#0",text="Label",anchor=W)
                my_tree.heading("Ticket No",text="Ticket No",anchor=W)
                my_tree.heading("CNIC",text='CNIC',anchor=W)
                my_tree.heading("Route Id",text="Route Id",anchor=W)
                my_tree.heading("Bus",text="Bus",anchor=W)
                my_tree.heading("Seat No",text="Seat No",anchor=W)
                my_tree.heading("Date",text="Date",anchor=W)

                count=0
                for record in lst:
                    my_tree.insert(parent='',index='end',iid = count,text="",values=(record[0],\
                        record[1],record[2],record[3],record[4],record[5]))
                    count+=1
        
        Button1 = tk.Button(self, text="Check", font=("Arial", 15), command=lambda: checkBooking())
        Button1.place(x=100, y=500)
        Button = tk.Button(self, text="Home", font=("Arial", 15), command=lambda: controller.show_frame(HomePage))
        Button.place(x=200, y=500)
        
#---------------------------------------------------- SchedulePage -----------------------------------------------------------  

class SchedulePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        load = Image.open("images/schedule.jpg")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image=photo
        label.place(x=0,y=0)

        my_tree =ttk.Treeview(self)
        my_tree.place(x=135, y=195)

        my_tree['columns']=("ID","From","To","Depature Time","Arrival Time","Traveling Time","Total Distance","Fare")
        my_tree.column("#0",width=0,stretch=NO)
        my_tree.column("ID",anchor=CENTER,width=30)
        my_tree.column("From",width=100,anchor=CENTER)
        my_tree.column("To",anchor=CENTER,width=100)
        my_tree.column("Depature Time",width=100,anchor=CENTER)
        my_tree.column("Arrival Time",anchor=CENTER,width=100)
        my_tree.column("Traveling Time",width=50,anchor=CENTER)
        my_tree.column("Total Distance",anchor=CENTER,width=70)
        my_tree.column("Fare",anchor=CENTER,width=50)

        my_tree.heading("#0",text="Label",anchor=W)
        my_tree.heading("ID",text="ID",anchor=W)
        my_tree.heading("From",text='From',anchor=W)
        my_tree.heading("To",text="To",anchor=W)
        my_tree.heading("Depature Time",text="Depature Time",anchor=W)
        my_tree.heading("Arrival Time",text="Arrival Time",anchor=W)
        my_tree.heading("Traveling Time",text="Traveling Time",anchor=W)
        my_tree.heading("Total Distance",text="Total Distance",anchor=W)
        my_tree.heading("Fare",text="Fare",anchor=W)
        
        data = []
        with open("TextFiles/routes.txt", 'r') as f:
            for line in f:
                st= line.rstrip("\n")
                data.append(st.split(","))
        
        count=0
        for record in data:
            my_tree.insert(parent='',index='end',iid = count,text="",values=(record[0],\
                record[1],record[2],record[3],record[4],record[5],record[6],record[7]))
            count+=1

        
        
        Button = tk.Button(self, text="Home", font=("Arial", 15), command=lambda: controller.show_frame(HomePage))
        Button.place(x=650, y=450)

#---------------------------------------------------- DiscountPage ----------------------------------------------------------- 

class DiscountPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        load = Image.open("images/booking.png")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image=photo
        label.place(x=0,y=0)


        Label2 = tk.Label(self, text="Discount Criteria: 10% Discount on 3 or more bookings ", font=("Arial", 10))
        Label2.place(x=300, y=500)
        Label1 = tk.Label(self, text="Enter Your Three Tickets No", font=("Arial", 20))
        Label1.place(x=250, y=100)

        T1 = tk.Entry(self)
        T1.place(x=300, y=150)

        T2 = tk.Entry(self)
        T2.place(x=300, y=250)
        
        T3 = tk.Entry(self)
        T3.place(x=300, y=350)

        def check():
            ticketNo = customerBooking.discount.checkDiscountEligibility(T1.get(),T2.get(),T3.get())
            if ticketNo == False:
                messagebox.showinfo('Ticketinfo', 'No Discount')
                return
            messagebox.showinfo('sample 1','You get Discount of 10%\nReedeem your Dicount by Showing Tickets at Bus Terminal' )
        
            T1.delete(0,'end')
            T2.delete(0,'end')
            T3.delete(0,'end')



        Button1 = tk.Button(self, text="Check", font=("Arial", 15), command=lambda: check())
        Button1.place(x=350, y=450)
        Button2 = tk.Button(self, text="Home", font=("Arial", 15), command=lambda: controller.show_frame(HomePage))
        Button2.place(x=650, y=450)

#---------------------------------------------------- AdminHomePage -----------------------------------------------------------  

class AdminHomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        load = Image.open("images/adminhome.jpeg")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image=photo
        label.place(x=0,y=0)

        Label = tk.Label(self, text="Welcome,", bg = "white",fg = "Grey", font=("Arial", 25))
        Label.place(x=230, y=150)
        Label = tk.Label(self, text="Hamza", bg = "white",fg = "Black", font=("Arial", 25))
        Label.place(x=350, y=150)
        Label = tk.Label(self, text="Hamza Tarar", bg = "white",fg = "Black", font=("Arial Bold", 15))
        Label.place(x=600, y=80)
        Label = tk.Label(self, text="T&T", bg = "white",fg = "Black", font=("Arial Bold", 25))
        Label.place(x=90, y=80)

        Button = tk.Button(self, text="Add Bus", font=("Arial", 15), command=lambda: controller.show_frame(AddBusPage))
        Button.place(x=70, y=150)


        Button = tk.Button(self, text="Remove Bus", font=("Arial", 15), command=lambda: controller.show_frame(RemoveBusPage))
        Button.place(x=65, y=250)
        
        Button = tk.Button(self, text="Add Route", font=("Arial", 15), command=lambda: controller.show_frame(AddRoutePage))
        Button.place(x=67, y=200)
        
        Button = tk.Button(self, text="Remove Route", font=("Arial", 15), command=lambda: controller.show_frame(RemoveRoutePage))
        Button.place(x=60, y=300)
        
        Button = tk.Button(self, text="View Schedule", font=("Arial", 15), command=lambda: controller.show_frame(AdminSchedulePage))
        Button.place(x=250, y=80)

        Button = tk.Button(self, text="Edit Schedule", font=("Arial", 15), command=lambda: controller.show_frame(EditSchedulePage))
        Button.place(x=580, y=300)
        
        
        Button = tk.Button(self, text="Log out", font=("Arial", 15),bg='#eae9ee', command=lambda: controller.show_frame(FirstPage))
        Button.place(x=80, y=450)

#---------------------------------------------------- AddBusPage -----------------------------------------------------------  

class AddBusPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        load = Image.open("images/adminhome.jpeg")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image=photo
        label.place(x=0,y=0)
        Label = tk.Label(self, text="Hamza Tarar", bg = "white",fg = "Black", font=("Arial Bold", 15))
        Label.place(x=600, y=80)
        Label = tk.Label(self, text="T&T", bg = "white",fg = "Black", font=("Arial Bold", 25))
        Label.place(x=90, y=80)
        L1 = tk.Label(self, text="Enter Bus Id", font=("Arial", 15), bg = "white",fg = "Black")
        L1.place(x=60, y=200)
        T1 = tk.Entry(self)
        T1.place(x=250, y=200)
        L2 = tk.Label(self, text="Enter Bus Plate No", font=("Arial", 15), bg = "white",fg = "Black")
        L2.place(x=60, y=250)
        T2 = tk.Entry(self)
        T2.place(x=250, y=250)
        L3 = tk.Label(self, text="Enter Bus Maintaince Cost", font=("Arial", 15), bg = "white",fg = "Black")
        L3.place(x=60, y=300)
        T3 = tk.Entry(self)
        T3.place(x=250, y=300)

        
        def addBus():
            if  T1.get() != "" and T2.get() != "" and T3.get() != "":
                admin.addBus(T1.get(),T2.get(),T3.get())
                messagebox.showinfo('information','Bus Added SuccessFully!!')
            else:
                messagebox.showinfo('Error','Give Complete Data')



        
        Button1 = tk.Button(self, text="Add", font=("Arial", 15), command=lambda:addBus())
        Button1.place(x=80, y=400)
        Button = tk.Button(self, text="Home", font=("Arial", 15), command=lambda: controller.show_frame(AdminHomePage))
        Button.place(x=80, y=450)

#---------------------------------------------------- RemoveBusPage -----------------------------------------------------------  

class RemoveBusPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        load = Image.open("images/adminhome.jpeg")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image=photo
        label.place(x=0,y=0)
        Label = tk.Label(self, text="Hamza Tarar", bg = "white",fg = "Black", font=("Arial Bold", 15))
        Label.place(x=600, y=80)
        Label = tk.Label(self, text="T&T", bg = "white",fg = "Black", font=("Arial Bold", 25))
        Label.place(x=90, y=80)
        L1 = tk.Label(self, text="Enter Bus Id", font=("Arial", 15), bg = "white",fg = "Black")
        L1.place(x=60, y=150)
        T1 = tk.Entry(self) 
        T1.place(x=250, y=150)

        def removeBus():
            if admin.removeBus(T1.get()):
                messagebox.showinfo('information','Bus Removed SuccessFully!!')
            else:
                messagebox.showinfo('information','No Bus To Remove!!')



        Button1 = tk.Button(self, text="Remove", font=("Arial", 15), command=lambda:removeBus())
        Button1.place(x=80, y=400)
        Button = tk.Button(self, text="Home", font=("Arial", 15), command=lambda: controller.show_frame(AdminHomePage))
        Button.place(x=80, y=450)

#---------------------------------------------------- AddRoutePage -----------------------------------------------------------  

class AddRoutePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        load = Image.open("images/adminhome.jpeg")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image=photo
        label.place(x=0,y=0)
        Label = tk.Label(self, text="Hamza Tarar", bg = "white",fg = "Black", font=("Arial Bold", 15))
        Label.place(x=600, y=80)
        L1 = tk.Label(self, text="Route Id", font=("Arial", 15), bg = "white",fg = "Black")
        L1.place(x=60, y=100)
        T1 = tk.Entry(self)
        T1.place(x=250, y=100)
        L2 = tk.Label(self, text="From", font=("Arial", 15), bg = "white",fg = "Black")
        L2.place(x=60, y=150)
        T2 = tk.Entry(self)
        T2.place(x=250, y=150)
        L3 = tk.Label(self, text="To", font=("Arial", 15), bg = "white",fg = "Black")
        L3.place(x=60, y=200)
        T3 = tk.Entry(self)
        T3.place(x=250, y=200)
        L4 = tk.Label(self, text="Depature Time", font=("Arial", 15), bg = "white",fg = "Black")
        L4.place(x=60, y=250)
        T4 = tk.Entry(self)
        T4.place(x=250, y=250)
        L5 = tk.Label(self, text="Arrival Time", font=("Arial", 15), bg = "white",fg = "Black")
        L5.place(x=60, y=300)
        T5 = tk.Entry(self)
        T5.place(x=250, y=300)
        L6 = tk.Label(self, text="Traveling Time", font=("Arial", 15), bg = "white",fg = "Black")
        L6.place(x=60, y=350)
        T6 = tk.Entry(self)
        T6.place(x=250, y=350)
        L7 = tk.Label(self, text="Total Distance", font=("Arial", 15), bg = "white",fg = "Black")
        L7.place(x=60, y=400)
        T7 = tk.Entry(self)
        T7.place(x=250, y=400)
        L8 = tk.Label(self, text="Fare", font=("Arial", 15), bg = "white",fg = "Black")
        L8.place(x=60, y=450)
        T8 = tk.Entry(self)
        T8.place(x=250, y=450)

        
        def addRoute():
            if  T1.get() != "" and T2.get() != "" and T3.get() != "" and T4.get() != "" and T5.get() != "" and T6.get() != "" and T7.get() != "" and T8.get() != "":
                admin.addRoute(T1.get(),T2.get(),T3.get(),T4.get(),T5.get(),T6.get(),T7.get(),T8.get())
                messagebox.showinfo('information','Route Added SuccessFully!!')
            else:
                messagebox.showinfo('Error','Give Complete Data')



        
        Button1 = tk.Button(self, text="Add", font=("Arial", 15), command=lambda:addRoute())
        Button1.place(x=580, y=250)
        Button = tk.Button(self, text="Home", font=("Arial", 15), command=lambda: controller.show_frame(AdminHomePage))
        Button.place(x=580, y=300)

#---------------------------------------------------- RemoveRoutePage -----------------------------------------------------------  

class RemoveRoutePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        load = Image.open("images/adminhome.jpeg")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image=photo
        label.place(x=0,y=0)
        Label = tk.Label(self, text="Hamza Tarar", bg = "white",fg = "Black", font=("Arial Bold", 15))
        Label.place(x=600, y=80)
        Label = tk.Label(self, text="T&T", bg = "white",fg = "Black", font=("Arial Bold", 25))
        Label.place(x=90, y=80)
        L1 = tk.Label(self, text="Enter Route Id", font=("Arial", 15), bg = "white",fg = "Black")
        L1.place(x=60, y=150)
        T1 = tk.Entry(self) 
        T1.place(x=250, y=150)

        def removeRoute():
            if admin.removeRoute(T1.get()):
                messagebox.showinfo('information','Route Removed SuccessFully!!')
            else:
                messagebox.showinfo('information','No Route To Remove!!')



        Button1 = tk.Button(self, text="Remove", font=("Arial", 15), command=lambda:removeRoute())
        Button1.place(x=80, y=400)
        Button = tk.Button(self, text="Home", font=("Arial", 15), command=lambda: controller.show_frame(AdminHomePage))
        Button.place(x=80, y=450)

#---------------------------------------------------- EditSchedulePage -----------------------------------------------------------  

class EditSchedulePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        load = Image.open("images/adminhome.jpeg")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image=photo
        label.place(x=0,y=0)
        Label = tk.Label(self, text="Hamza Tarar", bg = "white",fg = "Black", font=("Arial Bold", 15))
        Label.place(x=600, y=80)
        Label = tk.Label(self, text="T&T", bg = "white",fg = "Black", font=("Arial Bold", 25))
        Label.place(x=90, y=80)
        L1 = tk.Label(self, text="Enter Route Id", font=("Arial", 15), bg = "white",fg = "Black")
        L1.place(x=60, y=150)
        T1 = tk.Entry(self) 
        T1.place(x=250, y=150)
        L2 = tk.Label(self, text="Enter Bus Id", font=("Arial", 15), bg = "white",fg = "Black")
        L2.place(x=60, y=200)
        T2 = tk.Entry(self) 
        T2.place(x=250, y=200)

        def addToSchedule():
            if  T1.get() != "" and T2.get() != "" :
                admin.addToSchedule(T1.get(),T2.get(),Schedule)                                     #Association
                messagebox.showinfo('information','Schedule Updated SuccessFully!!')
            else:
                messagebox.showinfo('Error','Give Complete Data')

        def removeFromSchedule():
            if admin.removeFromSchedule(T1.get(),T2.get(),Schedule):                                #Association
                messagebox.showinfo('information','Schedule Updated SuccessFully!!')
            else:
                messagebox.showinfo('information','No Route To Remove!!')



        Button1 = tk.Button(self, text="Add", font=("Arial", 15), command=lambda:addToSchedule())
        Button1.place(x=80, y=350)
        Button1 = tk.Button(self, text="Remove", font=("Arial", 15), command=lambda:removeFromSchedule())
        Button1.place(x=70, y=400)
        Button = tk.Button(self, text="Home", font=("Arial", 15), command=lambda: controller.show_frame(AdminHomePage))
        Button.place(x=80, y=450)

#---------------------------------------------------- AdminSchedulePage -----------------------------------------------------------  

class AdminSchedulePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        load = Image.open("images/schedule.jpg")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image=photo
        label.place(x=0,y=0)

        my_tree =ttk.Treeview(self)
        my_tree.place(x=135, y=195)

        my_tree['columns']=("ID","From","To","Depature Time","Arrival Time","Traveling Time","Total Distance","Fare")
        my_tree.column("#0",width=0,stretch=NO)
        my_tree.column("ID",anchor=CENTER,width=30)
        my_tree.column("From",width=100,anchor=CENTER)
        my_tree.column("To",anchor=CENTER,width=100)
        my_tree.column("Depature Time",width=100,anchor=CENTER)
        my_tree.column("Arrival Time",anchor=CENTER,width=100)
        my_tree.column("Traveling Time",width=50,anchor=CENTER)
        my_tree.column("Total Distance",anchor=CENTER,width=70)
        my_tree.column("Fare",anchor=CENTER,width=50)

        my_tree.heading("#0",text="Label",anchor=W)
        my_tree.heading("ID",text="ID",anchor=W)
        my_tree.heading("From",text='From',anchor=W)
        my_tree.heading("To",text="To",anchor=W)
        my_tree.heading("Depature Time",text="Depature Time",anchor=W)
        my_tree.heading("Arrival Time",text="Arrival Time",anchor=W)
        my_tree.heading("Traveling Time",text="Traveling Time",anchor=W)
        my_tree.heading("Total Distance",text="Total Distance",anchor=W)
        my_tree.heading("Fare",text="Fare",anchor=W)
        
        data = []
        with open("TextFiles/routes.txt", 'r') as f:
            for line in f:
                st= line.rstrip("\n")
                data.append(st.split(","))
        
        count=0
        for record in data:
            my_tree.insert(parent='',index='end',iid = count,text="",values=(record[0],\
                record[1],record[2],record[3],record[4],record[5],record[6],record[7]))
            count+=1

        
        
        Button = tk.Button(self, text="Home", font=("Arial", 15), command=lambda: controller.show_frame(AdminHomePage))
        Button.place(x=650, y=450)
#---------------------------------------------------- Application  -----------------------------------------------------------  
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        #creating a window
        window = tk.Frame(self)
        window.pack()
        
        window.grid_rowconfigure(0, minsize = 600)
        window.grid_columnconfigure(0, minsize = 800)
        
        self.frames = {}
        for F in (FirstPage, HomePage, BookingPage,CancelBookingPage,CheckBookingPage,SchedulePage,AdminHomePage,AddBusPage,RemoveBusPage,AddRoutePage,RemoveRoutePage,EditSchedulePage,DiscountPage,AdminSchedulePage):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row = 0, column=0, sticky="nsew")
            
        self.show_frame(FirstPage)
        
    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        self.title("T&T Tarar Travels")
        
app = Application()
app.maxsize(800,600)
app.mainloop()
