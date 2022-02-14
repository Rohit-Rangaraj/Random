from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import mysql.connector 

global db

db = mysql.connector.connect(host ="localhost", user = "root", password = "", db ="traindbms")


def warmsg(msg1,msg2):
    messagebox.showwarning(msg1,msg2)

def infomsg(msg1,msg2):
    messagebox.showinfo(msg1,msg2)

def bktktf(arrval): # Book Ticket Function For Database
    
    cursor = db.cursor()
    arr = [str(x.get()) for x in arrval]
    mi = min(arr)

    if ((mi!="") and (mi!=" ")):
            cursor.execute(""" select * from train where trn_no ='"""+arr[-1]+"""'""")
            flag = cursor.fetchall()

            if(flag):

                cursor.execute("""insert into passengers(name,age,gender,phn_no,trn_nme,cls,frm,to_,dte,tme,pid,trn_no) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",arr)
                
                print(arrval)
                for x in arrval:
                    x.delete(0,END)
                infomsg("Train Ticket Reservation","Ticket Booked")
                print("ticket booked")
                db.commit()

            else:
                warmsg("Train Ticket Reservetion - Admin","Invalid Train Number")

    else:
        warmsg("Train Ticket Reservation","Please Fill All The Fields !!!")
        print("ticket not booked")


def inuptrnque(fn,arrval): # Function to insert train to database

    cursor = db.cursor()
    arr = [str(x.get()) for x in arrval]
    mi = min(arr)
    
    #insert into train(frm,to_,dte,tme,trn_no,trn_nme,pantry) values("chennai egmore","Hnizamuddin","5/05/21","9:05","06011","NZM EXP","yes");

    #frm,to_,dte,tme,trn_nme,pnt,trn_no

    #update train set frm =%s ,to_ =%s ,dte =%s ,tme =%s ,trn_nme =%s ,pantry =%s where trn_no =%s 

    if ((mi!="") and (mi!=" ")):

        if(fn=="Insert"):

            cursor.execute("""insert into train(frm,to_,dte,tme,trn_nme,pantry,trn_no) values (%s,%s,%s,%s,%s,%s,%s)""",arr)

            print(arrval)
            for x in arrval:
                x.delete(0,END)
            txtm = "Train " + fn +"ed" 
            infomsg("Train Ticket Reservation - Admin",txtm)
            print(fn + " - train - query")
            db.commit()

        else:
            cursor.execute(""" select * from train where trn_no ='"""+arr[-1]+"""'""")
            flag = cursor.fetchall()
            if(flag):
                cursor.execute("""update train set frm =%s ,to_ =%s ,dte =%s ,tme =%s ,trn_nme =%s ,pantry =%s where trn_no =%s""",arr)

                print(arrval)
                for x in arrval:
                    x.delete(0,END)
                txtm = "Train " + fn +"ed" 
                infomsg("Train Ticket Reservation - Admin",txtm)
                print(fn + " - train - query")
                db.commit()
            else:
                warmsg("Train Ticket Reservetion - Admin","Invalid Train Number")
                print(fn + " - train - query - warning - inv tn")
    else:
        warmsg("Train Ticket Reservation - Admin","Please Fill All The Fields !!!")

        print(fn + " - train - query")

def deltrnque(arrval): # Function to delete train from database

    cursor = db.cursor()
    arr = [str(x.get()) for x in arrval]
    mi = min(arr)

    if ((mi!="") and (mi!=" ")):

        cursor.execute(""" select * from train where trn_no ='"""+arr[0]+"""'""")
        flag = cursor.fetchall()

        if(flag):
            cursor.execute("""delete from train where trn_no =%s""",arr)

            for x in arrval:
                x.delete(0,END)

            infomsg("Train Ticket Reservation - Admin","Train Deleted")

            print("Deleted - train - query")
            db.commit()
        else:
            warmsg("Train Ticket Reservetion - Admin","Invalid Train Number")
            print("Delete - train - query - warning - inv tn")
    else:
        warmsg("Train Ticket Reservation - Admin","Please Enter Train No")

        print("Delete - train - query")


def cncltcktq(arrval): # Function to cancel ticket from database

    cursor = db.cursor()
    arr = [str(x.get()) for x in arrval]
    mi = min(arr)

    if ((mi!="") and (mi!=" ")):

        cursor.execute(""" select * from passengers where pid ='"""+ arr[0] + """"' and trn_no ='"""+ arr[1] +"""'""")
        flag = cursor.fetchall()

        if(flag):
            cursor.execute("""delete from passengers where pid =%s""",arr[0])

            for x in arrval:
                x.delete(0,END)

            infomsg("Train Ticket Reservation","Train Ticket Cancelled")

            print("Deleted - train - ticket - query")
            db.commit()
        else:
            warmsg("Train Ticket Reservetion - Admin","Invalid Passenger ID (or) Train Number")
            print("Delete - train - query - warning - inv tn")
    else:
        warmsg("Train Ticket Reservation","Please Fill The Fields")

        print("Delete - train - Ticket - query")


def passadmntab(tree):

    cursor = db.cursor()
    cursor.execute("""select * from passengers""")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)  

    print("passengers - admin - view")


def adlog(admn): # Function to log admin messages
    
    admn_nme = str(admn[0].get())
    admn_id = str(admn[1].get())

    if((admn_nme == "") or (admn_nme == " ")or(admn_id == "") or (admn_id == " ")):
        warmsg("Train Ticket Reservation","Please Fill The Fields")
    
    else:
        cur = db.cursor()
        cur.execute(""" select * from admin where name ='"""+ admn_nme +"""' and id ='"""+ admn_id +"""'""" )
        flag = cur.fetchall()

        if(flag):
            adminwin()
            print(" admin login success")

        else:
            warmsg("Train Ticket Reservation","Please Enter Correct Admin Name & Admin ID  !!!")


def viewtrnaval(tree): # Function to view available trains
    cursor = db.cursor()
    cursor.execute("""select * from train""")
    rows = cursor.fetchall()

    for i in tree.get_children():
        tree.delete(i)

    for row in rows:
        tree.insert("", tk.END, values=row)
    print("aval train")


def passadmn(): # Function to define Train Available window

    passadwin = tk.Tk()
    passadwin.resizable(False,False)
    passadwin.title("Train Ticket Reservation")
    
    tree = ttk.Treeview(passadwin, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11", "c12"), show='headings')
    tree.column("c1", width=110,anchor='c')
    tree.heading("c1", text="Name")

    tree.column("c2", width=110,anchor='se')
    tree.heading("c2", text="Age")

    tree.column("c3", width=110,anchor='se')
    tree.heading("c3", text="Gender")

    tree.column("c4",width=110, anchor='se')
    tree.heading("c4", text="Phone Number")

    tree.column("c5",width=110, anchor='se')
    tree.heading("c5", text="Train Name")

    tree.column("c6",width=110, anchor='se')
    tree.heading("c6", text="Class")

    tree.column("c7",width=110, anchor='se')
    tree.heading("c7", text="From")

    tree.column("c8",width=110, anchor='se')
    tree.heading("c8", text="To")
    
    tree.column("c9",width=110, anchor='se')
    tree.heading("c9", text="Date")

    tree.column("c10",width=110, anchor='se')
    tree.heading("c10", text="Time")

    tree.column("c11",width=110, anchor='se')
    tree.heading("c11", text="Train Number")

    tree.column("c12",width=110, anchor='se')
    tree.heading("c12", text="Passenger ID")

    tree.pack()

    passadmntab(tree)

    print("passengers - admin")


def trnadmn(): # Function to define train management window
    trnadmnwin = tk.Tk()
    trnadmnwin.resizable(False,False)
    trnadmnwin.title("Train Ticket Reservation - Admin")

    trnadtree = ttk.Treeview(trnadmnwin, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7"), show='headings')
    trnadtree.column("c1", width=110,anchor='c')
    trnadtree.heading("c1", text="From")

    trnadtree.column("c2", width=110,anchor='se')
    trnadtree.heading("c2", text="To")

    trnadtree.column("c3", width=110,anchor='se')
    trnadtree.heading("c3", text="Date")

    trnadtree.column("c4",width=110, anchor='se')
    trnadtree.heading("c4", text="Time")

    trnadtree.column("c5",width=110, anchor='se')
    trnadtree.heading("c5", text="Train_No")

    trnadtree.column("c6",width=110, anchor='se')
    trnadtree.heading("c6", text="Train_Name")

    trnadtree.column("c7",width=110, anchor='se')
    trnadtree.heading("c7", text="Pantry")

    trnadtree.grid(row=1,column=0,columnspan=4,pady=3)

    upbtn = tk.Button(trnadmnwin,text="Update",command=lambda:[inuptrn("Update")],height=2,width=16)
    inbtn =  tk.Button(trnadmnwin,text="Insert",command=lambda:[inuptrn("Insert")],height=2,width=16)
    delbtn =  tk.Button(trnadmnwin,text="Delete",command=deltrn,height=2,width=16)
    refbtn = tk.Button(trnadmnwin,text="Refresh",command=lambda:[viewtrnaval(trnadtree)],height=2,width=16)
    
    upbtn.grid(row=0,column=0,pady=5)
    inbtn.grid(row=0,column=1,pady=5)
    delbtn.grid(row=0,column=2,pady=5)
    refbtn.grid(row=0,column=3,pady=5)

    print("Train - admin view")


def trnaval(): # Train Available
    
    trnavalwin = tk.Tk()
    trnavalwin.resizable(False,False)
    trnavalwin.title("Train Ticket Reservation")
    
    tree = ttk.Treeview(trnavalwin, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7"), show='headings')
    tree.column("c1", width=110,anchor='c')
    tree.heading("c1", text="From")

    tree.column("c2", width=110,anchor='se')
    tree.heading("c2", text="To")

    tree.column("c3", width=110,anchor='se')
    tree.heading("c3", text="Date")

    tree.column("c4",width=110, anchor='se')
    tree.heading("c4", text="Time")

    tree.column("c5",width=110, anchor='se')
    tree.heading("c5", text="Train_No")

    tree.column("c6",width=110, anchor='se')
    tree.heading("c6", text="Train_Name")

    tree.column("c7",width=110, anchor='se')
    tree.heading("c7", text="Pantry")

    tree.pack()
    viewtrnaval(tree)

    print("Train Available")


def deltrn(): # Function to delete trains
    delwin = tk.Tk()
    delwin.resizable(False,False)
    delwin.title("Train Ticket Reservation - Admin")

    trnnol = Label(delwin,text="Train no :").grid(row = 0,column=0,padx=5,pady=5)
    trnno = Entry(delwin,width=37)
    trnno.grid(row = 0,column=1,padx=20,pady=5)

    arr = [trnno]

    submitbtn = tk.Button(delwin,text="Delete Train", command=lambda:[deltrnque(arr)])#,tcktbookdmsg()
    submitbtn.grid(row=12,column=0,columnspan=2,padx=10,pady=10,ipadx=100)
    
    print("delete - train")


def inuptrn(fn): # Function to define window to insert or update trains

    inupwin = tk.Tk()
    inupwin.resizable(False,False)
    inupwin.title("Train Ticket Reservation - Admin")

    Froml = Label(inupwin,text="From :").grid(row = 0,column=0,padx=5,pady=5)
    frm = Entry(inupwin,width=37)
    frm.grid(row = 0,column=1,padx=20,pady=5)
    

    Tol = Label(inupwin,text="To :").grid(row = 1,column=0,padx=5,pady=5)
    to_ = Entry(inupwin,width=37)
    to_.grid(row = 1,column=1,padx=20,pady=5)

    Datel = Label(inupwin,text="Date :").grid(row = 2,column=0,padx=5,pady=5)
    dte = Entry(inupwin,width=37)
    dte.grid(row = 2,column=1,padx=20,pady=5)

    Timel = Label(inupwin,text="Time :").grid(row = 3,column=0,padx=5,pady=5)
    tme = Entry(inupwin,width=37)
    tme.grid(row = 3,column=1,padx=5,pady=5)

    Train_nol = Label(inupwin,text="Train no :").grid(row = 4,column=0,padx=5,pady=5)
    trn_no = Entry(inupwin,width=37)
    trn_no.grid(row = 4,column=1,padx=5,pady=5)

    Train_namel = Label(inupwin,text="Train Name :").grid(row = 5,column=0,padx=5,pady=5)
    trn_nme = Entry(inupwin,width=37)
    trn_nme.grid(row = 5,column=1,padx=5,pady=5)

    Pantryl = Label(inupwin,text="Pantry :").grid(row = 6,column=0,padx=5,pady=5)
    pnt = Entry(inupwin,width=37)
    pnt.grid(row = 6,column=1,padx=20,pady=5)

    arr = [frm,to_,dte,tme,trn_nme,pnt,trn_no]

    txt = fn + " " + "Train"
    submitbtn = tk.Button(inupwin,text=txt, command=lambda:[inuptrnque(fn,arr)])
    submitbtn.grid(row=12,column=0,columnspan=2,padx=10,pady=10,ipadx=100)

    print(fn + " - train - query")


def tcktcncl(): # Function to define window to cancel tickets

    tcwin = tk.Tk()
    tcwin.geometry("360x220")
    tcwin.title("Train Ticket Reservation - Train")

    P_id = Label(tcwin,text="Passenger ID :")
    P_id.grid(row=0, column=0,padx=10,pady=20)
    pid = Entry(tcwin,width=37)
    pid.grid(row=0, column=1,padx=10,pady=20,ipady=2.2)
    
    Train_no = Label(tcwin,text="Train No :")
    Train_no.grid(row=1, column=0,padx=10,pady=20)
    trn_no = Entry(tcwin,width=37)
    trn_no.grid(row=1, column=1,padx=10,pady=20,ipady=2.21)

    tc = [pid,trn_no]

    cnclbtn = Button(tcwin,text = "Cancel Ticket", command= lambda:[cncltcktq(tc)])
    cnclbtn.grid(row=2,column=0,columnspan=2,padx=10,pady=10,ipadx=100)




    print("cncl")


 # Ticket Reservation

def tcktres(): # Function to define window to reserve tickets
    scndwin = tk.Tk()
    scndwin.resizable(False,False)
    scndwin.title("Train Ticket Reservation")

    Pidl = Label(scndwin,text="ID :").grid(row = 0,column=0,padx=5,pady=5)
    pid = Entry(scndwin,width=37)
    pid.grid(row = 0,column=1,padx=20,pady=5)
    

    Namel = Label(scndwin,text="Name :").grid(row = 1,column=0,padx=5,pady=5)
    name = Entry(scndwin,width=37)
    name.grid(row = 1,column=1,padx=20,pady=5)

    Agel = Label(scndwin,text="Age :").grid(row = 2,column=0,padx=5,pady=5)
    age = Entry(scndwin,width=37)
    age.grid(row = 2,column=1,padx=20,pady=5)

    Genderl = Label(scndwin,text="Gender :").grid(row = 3,column=0,padx=5,pady=5)
    gender = Entry(scndwin,width=37)
    gender.grid(row = 3,column=1,padx=5,pady=5)

    Phone_no = Label(scndwin,text="Phone no :").grid(row = 4,column=0,padx=5,pady=5)
    phn_no = Entry(scndwin,width=37)
    phn_no.grid(row = 4,column=1,padx=5,pady=5)

    Train_name = Label(scndwin,text="Train Name :").grid(row = 5,column=0,padx=5,pady=5)
    trn_nme = Entry(scndwin,width=37)
    trn_nme.grid(row = 5,column=1,padx=5,pady=5)

    Train_nol = Label(scndwin,text="Train no :").grid(row = 6,column=0,padx=5,pady=5)
    trn_no = Entry(scndwin,width=37)
    trn_no.grid(row = 6,column=1,padx=20,pady=5)
    
    Class_ = Label(scndwin,text="Class :").grid(row = 7,column=0,padx=5,pady=5)
    cls_ = Entry(scndwin,width=37)
    cls_.grid(row = 7,column=1,padx=5,pady=5)
    
    from_ = Label(scndwin,text="From :").grid(row = 8,column=0,padx=5,pady=5)
    frm = Entry(scndwin,width=37)
    frm.grid(row = 8,column=1,padx=5,pady=5)
    
    To_ = Label(scndwin,text="To :").grid(row = 9,column=0,padx=5,pady=5)
    to_ = Entry(scndwin,width=37)
    to_.grid(row = 9,column=1,padx=5,pady=5)
    
    Date = Label(scndwin,text="Date :").grid(row = 10,column=0,padx=5,pady=5)
    date = Entry(scndwin,width=37)
    date.grid(row = 10,column=1,padx=5,pady=5)
    
    Time_ = Label(scndwin,text="Time :").grid(row = 11,column=0,padx=5,pady=5)
    time_ = Entry(scndwin,width=37)
    time_.grid(row = 11,column=1,padx=5,pady=5)

    arr = [name,age,gender,phn_no,trn_nme,cls_,frm,to_,date,time_,pid,trn_no]


    submitbtn = tk.Button(scndwin,text="Book Ticket", command=lambda:[bktktf(arr)])#,tcktbookdmsg()
    submitbtn.grid(row=12,column=0,columnspan=2,padx=10,pady=10,ipadx=100)


    print("ticket reserved")

def adminlogin(): # Function to define the admin login page
    adlogwin = tk.Tk()
    adlogwin.resizable(False,False)
    adlogwin.geometry("360x220")
    adlogwin.title("Train Ticket Reservation - Train")

    Admin_name = Label(adlogwin,text="Admin Name :")
    Admin_name.grid(row=0, column=0,padx=10,pady=20)
    admin_nme = Entry(adlogwin,width=37)
    admin_nme.grid(row=0, column=1,padx=10,pady=20,ipady=2.2)
    
    Admin_id = Label(adlogwin,text="Admin ID :")
    Admin_id.grid(row=1, column=0,padx=10,pady=20)
    admin_id = Entry(adlogwin,width=37)
    admin_id.grid(row=1, column=1,padx=10,pady=20,ipady=2.21)

    admn = [admin_nme,admin_id]

    logbtn = Button(adlogwin,text = "Login", command= lambda:[adlog(admn)])
    logbtn.grid(row=2,column=0,columnspan=2,padx=10,pady=10,ipadx=100)


    print("admin login")    

    
def adminwin(): # Function to define the admin interface
    adwin = tk.Tk()
    adwin.resizable(False,False)
    adwin.geometry("360x245")
    adwin.title("Train Ticket Reservation - Admin")


    trnbtn = tk.Button(adwin,text="Train",command=trnadmn,height=3,width=16)
    passbtn =  tk.Button(adwin,text="Passengers",command=passadmn,height=3,width=16)

    trnbtn.grid(row=0,column=1)
    passbtn.grid(row=1,column=2)

    trnbtn.place(relx=0.5, rely=0.25, anchor=CENTER)
    passbtn.place(relx=0.5, rely=0.7, anchor=S)

    
# Train Ticket Button Window    

def tckt(): # Function to define the train ticket button window
    tcktwin = tk.Tk()
    tcktwin.resizable(False,False)
    tcktwin.title("Train Ticket Reservation")
    tcktwin.geometry("300x245")

    trnavalbtn = tk.Button(tcktwin,text="Train Available",command=trnaval,height=3,width=16)
    tcktresbtn =  tk.Button(tcktwin,text="Ticket Reservation",command=tcktres,height=3,width=16)
    tcktcnclbtn =  tk.Button(tcktwin,text="Ticket Cancelation",command=tcktcncl,height=3,width=16)


    trnavalbtn.grid(row=0,column=1)
    tcktresbtn.grid(row=1,column=1)
    tcktcnclbtn.grid(row=2,column=1)

    trnavalbtn.place(relx=0.5, rely=0.05, anchor=N)
    tcktresbtn.place(relx=0.5, rely=0.37, anchor=N)
    tcktcnclbtn.place(relx=0.5, rely=0.70, anchor=N)


root = tk.Tk()
root.resizable(False, False)

root.title("Train Ticket Reservation")
root.geometry("300x245")

adminbtn = tk.Button(root,text="Admin Login",command=adminlogin,height=3,width=16)
tktresbtn =  tk.Button(root,text="Passengers",command=tckt,height=3,width=16)

db.commit()

adminbtn.grid(row=0,column=1)
tktresbtn.grid(row=1,column=2)

adminbtn.place(relx=0.5, rely=0.25, anchor=CENTER)
tktresbtn.place(relx=0.5, rely=0.7, anchor=S)

mainloop()

db.close()