from tkinter import *
from tkinter import messagebox
import mysql.connector
from tkinter import ttk
root=Tk()
root.config(bg="silver")
root.geometry("500x500")
root.maxsize(700,700)
root.minsize(700,700)
root.title("Employee management system")

def connect():
    cur= mysql.connector.connect(
        host="localhost",
        user="root",
        password="Dipesh@143",
        database="mysql_company"
    )
    return cur

def insert():
    conn= connect()
    c = conn.cursor()
    deptno = txtNo.get()
    dname = txtName.get()
    loc = txtLoc.get()

    c.execute("insert into info values("+deptno+",'"+dname+"','"+loc+"')")
    conn.commit()
    conn.close()
    tree.insert('','end', values=(deptno,dname,loc))
    txtNo.delete(0,END)
    txtName.delete(0,END)
    txtLoc.delete(0,END)
    messagebox.showinfo("Information", "completed registration.....")

def show():
    # Clear previous data
    tree.delete(*tree.get_children())
    conn = connect()
    c = conn.cursor()
    c.execute("select * from info")
    res = c.fetchall()
    for i in res:
        tree.insert('','end',values=i)
    conn.commit()
    conn.close()

def clear():
    for i in tree.get_children():
        tree.delete(i)

def search():
    # Clear previous data
    tree.delete(*tree.get_children())
    conn = connect()
    c = conn.cursor()
    ser= s.get()
    query = "select deptno, dname,loc from info where deptno LIKE '%"+ser+"%'"
    c.execute(query)
    row=c.fetchall()
    for i in row:
        tree.insert('',END ,values=i)

    s.delete(0,END)




def delete():
    conn = connect()
    c = conn.cursor()
    select_del = tree.focus()
    if select_del:
        values = tree.item(select_del,'values')
        # id_to_delete= values[0]
        # delete in database
        query = f"delete from info where deptno = %s"
        c.execute(query,(values[0],))
        conn.commit()
        # delete in treeview
        tree.delete(select_del)
    messagebox.showinfo("Information", "The record is deleted.....")


def update():
    conn = connect()
    c = conn.cursor()

    deptno = txtNo.get()
    dname = txtName.get()
    dloc = txtLoc.get()

    query = "update info set dname = '%s', loc = '%s' where deptno = '%s' " % (dname,dloc,deptno)
    c.execute(query)
    conn.commit()

    selected_item = tree.selection()
    if len(selected_item) == 1:  # Ensure only one item is selected
        item = selected_item[0]
        # Update the values in the selected item
        tree.item(item, values=(f"{deptno}", f"{dname}", f"{dloc}"))
    messagebox.showinfo("Info", "Selected Record Updated Successfully")
def show_selected_row(event):
    selected_item = tree.focus()
    values = tree.item(selected_item, 'values')
    if values:
        txtNo.delete(0, END)
        txtName.delete(0, END)
        txtLoc.delete(0, END)
        txtNo.insert(0, values[0])
        txtName.insert(0, values[1])
        txtLoc.insert(0, values[2])

lbl1= Label(root,text="Employee  Management  System",bg="red",relief=RIDGE,font="time 15 bold",width=50,bd=5)
lbl2= Label(root,text="Enter DeptNo :",bg="blue",relief=RIDGE,font="time 12 bold",width=19)
lbl3= Label(root,text="Enter Department Name :",bg="blue",relief=RIDGE,font="time 12 bold")
lbl4= Label(root,text="Enter Location :",bg="blue",relief=RIDGE,font="time 12 bold",width=19)

lbl5=Label(root,text="Please select one record below to update or delete",bg="blue",relief=RIDGE,font="time 12 bold")

txtNo= Entry(root,width=30,bd=3)
txtName= Entry(root,width=30,bd=3)
txtLoc= Entry(root,width=30,bd=3)

register=Button(root,text="Register",bg="red",relief=RAISED,font="time 12 bold",command=insert)
update=Button(root,text="Update",bg="red",relief=RAISED,font="time 12 bold",command=update)
delete=Button(root,text="Delete",bg="red",relief=RAISED,font="time 12 bold",command=delete)
clear=Button(root,text="Clear",bg="red",relief=RAISED,font="time 12 bold",command=clear)
showall=Button(root,text="Show All",bg="red",relief=RAISED,font="time 12 bold",command=show)


lbl1.place(x=50,y=10)
lbl2.place(x=140,y=60)
lbl3.place(x=140,y=100)
lbl4.place(x=140,y=140)

txtNo.place(x=360,y=60)
txtName.place(x=360,y=100)
txtLoc.place(x=360,y=140)

register.place(x=80,y=220,width=90)
update.place(x=200,y=220,width=90)
delete.place(x=310,y=220,width=90)
clear.place(x=430,y=220,width=90)
showall.place(x=550,y=220,width=90)

lbl5.place(x=110,y=290,width=500)

frm1= Frame(root,width=570,height=200,bg="grey")
frm1.place(y=330,x=60)

columns = ("dno" , "dname" , "location")

tree = ttk.Treeview(frm1,columns=columns,show='headings')
tree.tag_configure("odd",background="silver")
tree.tag_configure("even",background="light gray")

tree.heading('dno',text="DeptNo",anchor=CENTER)
tree.heading('dname',text="DeptName",anchor=CENTER)
tree.heading('location',text="Location",anchor=CENTER)
tree.column('dno',anchor=CENTER)
tree.column('dname',anchor=CENTER)
tree.column('location',anchor=CENTER)

tree.bind("<<TreeviewSelect>>" ,show_selected_row)
tree.grid(row=0,column=0,sticky='ns')
#
scrollbar = ttk.Scrollbar(frm1,orient=VERTICAL,command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=0,column=1,sticky='ns')

# search label
s_Label = Label(root, text="Please enter deptno :-",width=18,height=1,relief=RIDGE,bg="blue",font="arial 12 bold ")
s_Label.pack(side=BOTTOM,anchor=NW,pady=70,padx=70)

# search entry
s = Entry(root,width=23,relief=RIDGE,bd=3)
s.place(x=260,y=603,height=27)

# search button
s_button = Button(root, text="Search",bg="red",relief=RAISED,font="time 12 bold",command=search)
s_button.place(x=410,y=603 , height=26)
root.mainloop()
