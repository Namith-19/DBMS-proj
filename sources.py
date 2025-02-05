import customtkinter as ctk
import tkinter as tk
import mysql.connector as ctr

# Mysql Connections
conn= ctr.connect(user="root",password="namit",host="localhost",database="dbmsproj")
curr=conn.cursor()


def clearFrame(frame):
       for widgets in frame.winfo_children():
           widgets.destroy()

def typeoQuery(Query):
    match Query:    
        case "Add Feild":
            add()
        case "Retrive Values":
            retrive()
        case 'Custom Query':
            cusQuery()
        
def add():
    customFrame.pack_forget()
    retriveFrame.pack_forget()
    addFrame.pack(side="top",fill="both")
    opDpLb.configure(text="Table: ")
    opDp.configure(values=["Books", 'Issue Detials',"Staff","Students","Table Detials","Table Reservations"], command=lambda a: populateTable("addFrame",a))
    opDp.set("Books")
    opDpLb.grid(row=1,column=0)
    opDp.grid(row=1,column=1)
    

def retrive():
    customFrame.pack_forget()
    addFrame.pack_forget()
    retriveFrame.pack(side="top",fill="both")
    opDpLb.configure(text="Query Type: ")
    opDp.configure(values=["Books Detials by Genre", 'Issue Detials by Issue Date',"Issue Detials by Not returned","Students by State","Students by Course","Table Reservations detials"], command=lambda a: populateTable("retriveFrame",a))
    opDp.set("Books Detials by Genre")
    opDpLb.grid(row=1,column=0)
    opDp.grid(row=1,column=1)

def cusQuery():
    def executeComm():
        query=queryVar.get()
        curr.execute(query)
        result=curr.fetchall()
        opRender(result)
    queryVar=tk.StringVar()
    addFrame.pack_forget()
    retriveFrame.pack_forget()
    customFrame.pack(side="top",fill="both")
    queryLb=ctk.CTkLabel(customFrame,text="Custom Query: ",)
    queryLb.grid(row=0,column=0)
    queryEnt=ctk.CTkEntry(customFrame,textvariable=queryVar)
    queryEnt.grid(row=0,column=1)
    executeBt=ctk.CTkButton(customFrame,text="Execute",command=executeComm)
    executeBt.grid(row=1)

def populateTable(frame,op):
    frameObj=globals()[frame]
    clearFrame(frameObj)
    global executeBt
    executeBt=ctk.CTkButton(frameObj,text="Execute",command=lambda : globals()[f"execute{frame}"](colList,op))
    match frame:
        case "addFrame":
            colList=[]
            op=op.replace(" ","_") 
            curr.execute(f"desc {op}")
            result=curr.fetchall()
            for x in result:
                colList.append(x[0])
            print(colList)
            i=int()
            for i in range(1,len(colList)+1):
                ctk.CTkLabel(frameObj,text=colList[i-1]).grid(row=i,column=0)
                globals()[f"{colList[i-1]}Var"]=tk.StringVar()
                globals()[f"{colList[i-1]}Ent"]=ctk.CTkEntry(frameObj,textvariable=globals()[f"{colList[i-1]}Var"])
                globals()[f"{colList[i-1]}Ent"].grid(row=i,column=1)
            executeBt.grid(row=i+1)
        case "retriveFrame":
            executeBt.configure(command=lambda : globals()[f"execute{frame}"](op))
            match op:
                case "Books Detials by Genre":
                    
                    genreLb=ctk.CTkLabel(frameObj,text="Genre: ")
                    genreEnt=ctk.CTkEntry(frameObj,textvariable=genreVar)
                    genreLb.grid(row=0,column=0)
                    genreEnt.grid(row=0,column=1)
                case 'Issue Detials by Issue Date':
                    
                    issuedtLb=ctk.CTkLabel(frameObj,text="Issue Date: ")
                    issuedtEnt=ctk.CTkEntry(frameObj,textvariable=issuedtVar)
                    issuedtLb.grid(row=0,column=0)
                    issuedtEnt.grid(row=0,column=1)
                case "Issue Detials by Not returned":
                    
                    retstatLb=ctk.CTkLabel(frameObj,text="Return Status: ")
                    retstatEnt=ctk.CTkEntry(frameObj,textvariable=retstatVar)
                    retstatLb.grid(row=0,column=0)
                    retstatEnt.grid(row=0,column=1)
                case "Students by State":
                    
                    ststateLb=ctk.CTkLabel(frameObj,text="State: ")
                    ststateEnt=ctk.CTkEntry(frameObj,textvariable=ststateVar)
                    ststateLb.grid(row=0,column=0)
                    ststateEnt.grid(row=0,column=1)
                case "Students by Course":
                   
                    stcourseLb=ctk.CTkLabel(frameObj,text="Course: ")
                    stcourseEnt=ctk.CTkEntry(frameObj,textvariable=stcourseVar)
                    stcourseLb.grid(row=0,column=0)
                    stcourseEnt.grid(row=0,column=1)
                case "Table Reservations detials":
                    
                    stregLb=ctk.CTkLabel(frameObj,text="Register No: ")
                    stregEnt=ctk.CTkEntry(frameObj,textvariable=stregVar)
                    stregLb.grid(row=0,column=0)
                    stregEnt.grid(row=0,column=1)
            executeBt.grid(row=1,column=0)

def executeaddFrame(colList,tab):
    tab=tab.replace(" ","_")
    tab=tab.lower()
    errorLb.configure(text="")
    queryval=[]
    retValues={}
    query=""
    for i in colList:
        try:
            retValues[f"{i}Var"]=int(globals()[f"{i}Var"].get())
        except:
            retValues[f"{i}Var"]=globals()[f"{i}Var"].get()
    queryval=list(retValues.values())

    if "" in list(retValues.values()) or " " in list(retValues.values()):
        errorLb.configure(text="Please Enter all the values!")
    else:
        match tab:
            case "books":
                print("books")
                query="insert into books values(%s,%s,%s,%s,%s,%s)"
            case "table_detials":
                query="insert into table_detials values(%s,%s,%s)"
            case "table_reservations":
                query="insert into table_reservations values(%s,%s,%s)"
            case "students":
                query="insert into students values(%s,%s,%s,%s,%s,%s,%s)"
            case "staff":
                query="insert into staff values(%s,%s,%s,%s)"

        curr.execute(query,queryval)
        conn.commit()
        errorLb.configure(text="Successfully Inserted Values!!")

def executeretriveFrame(op):
    retvals=[]
    match op:
        case "Books Detials by Genre":
            retvals.append(genreVar.get())
            curr.execute("select * from books where genre=%s",retvals)

        case 'Issue Detials by Issue Date':
            retvals.append(issuedtVar.get())
            curr.execute("select issue_detials.regno,book_id,students.name,students.phno,issue_date,due_date,returned from issue_detials join students on issue_detials.regno=students.regno where issue_detials.issue_date=%s",retvals)

        case "Issue Detials by Not returned":
            retvals.append(retstatVar.get())
            curr.execute("select issue_detials.regno,book_id,students.name,students.phno,issue_date,due_date,returned from issue_detials join students on issue_detials.regno=students.regno where issue_detials.returned=%s",retvals)

        case "Students by State":
            retvals.append(ststateVar.get())
            curr.execute("select * from students where state=%s",retvals)

        case "Students by Course":
            retvals.append(stcourseVar.get())
            curr.execute("select * from students where course=%s",retvals)

            
        case "Table Reservations detials":
            retvals.append(stregVar.get())
            curr.execute("select table_reservations.tableId,students.regno,students.name,students.phno,students.course from table_reservations join students on table_reservations.regno=students.regno where table_reservations.regno=%s",retvals)
    result=curr.fetchall()
    opRender(result)



def opRender(result):
    opWindow=ctk.CTkToplevel(app)
    opWindow.geometry("600x600")
    for x in result:
        ctk.CTkLabel(opWindow,text=x).pack(side="top",anchor="w")
    ctk.CTkButton(opWindow,text="Exit",command=opWindow.destroy).pack(side="top")
    opWindow.mainloop()

ctk.set_appearance_mode("system")
ctk.set_window_scaling(1.0)
app = ctk.CTk()
app.title("Library Management System")
app.geometry("500x500")
app.configure(bg="blue")

# Title
titleLb=ctk.CTkLabel(app,text="Library Management System")
titleLb.pack(side="top")

# Frames
mainFrame=ctk.CTkFrame(app,border_width=0,corner_radius=10)
mainFrame.pack(fill="x",side='top')
addFrame=ctk.CTkFrame(app,border_width=1,corner_radius=18)
retriveFrame=ctk.CTkFrame(app,border_width=1,corner_radius=18)
customFrame=ctk.CTkFrame(app,border_width=1,corner_radius=18)
errorLb=ctk.CTkLabel(app,text="",)
errorLb.pack(side="bottom",anchor="w")

# Type of Query
queryLb=ctk.CTkLabel(mainFrame,text="Query: ")
queryLb.grid(row=0,column=0)
typeQuery=ctk.CTkOptionMenu(master=mainFrame,values=["Add Feild", 'Retrive Values','Custom Query'], command=typeoQuery)
typeQuery.grid(row=0,column=1)

opDpLb=ctk.CTkLabel(mainFrame, text="Table: ")
opDp=ctk.CTkOptionMenu(master=mainFrame,values=["Books", 'Issue Detials',"Staff","Students","Table Detials","Table Reservations"], command=lambda a: populateTable("addFrame",a))

genreVar=tk.StringVar()
issuedtVar=tk.StringVar()
retstatVar=tk.StringVar()
ststateVar=tk.StringVar()
stcourseVar=tk.StringVar()
stregVar=tk.StringVar()

app.mainloop()
