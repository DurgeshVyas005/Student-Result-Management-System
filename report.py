# report.py

from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3

class reportClass:
    def __init__(self,root):
        self.root=root
        self.root.title("View Student Results")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()
        
        # --- Variables ---
        self.var_search=StringVar()
        self.var_roll_to_delete="" # Stores the roll number of the result shown

        #====title====#
        title=Label(self.root,text="View Student Results",font=("goudy old style",20,"bold"),bg="orange",fg="#262626").place(x=10,y=15,width=1180,height=50)
        
        #=====search===========
        lbl_search=Label(self.root,text="Search by Roll No.",font=("goudy old style",20,"bold"),bg="white").place(x=280,y=100)
        Entry(self.root,textvariable=self.var_search,font=("goudy old style",20),bg="lightyellow").place(x=520,y=100,width=150)
        Button(self.root,text='Search',font=("goudy old style",15,"bold"),bg="#03a9f4",fg="white",cursor="hand2",command=self.search).place(x=680,y=100,width=100,height=35)
        Button(self.root,text='Clear',font=("goudy old style",15,"bold"),bg="gray",fg="white",cursor="hand2",command=self.clear).place(x=800,y=100,width=100,height=35)


        #=====result_labels (Headers) ===========
        header_y = 230
        result_y = 280
        width=150
        height=50
        
        Label(self.root,text="Roll No",font=("goudy old style",15,"bold"),bg="lightgray",bd=2,relief=GROOVE).place(x=150,y=header_y,width=width,height=height)
        Label(self.root,text="Name",font=("goudy old style",15,"bold"),bg="lightgray",bd=2,relief=GROOVE).place(x=300,y=header_y,width=width,height=height)
        Label(self.root,text="Course",font=("goudy old style",15,"bold"),bg="lightgray",bd=2,relief=GROOVE).place(x=450,y=header_y,width=width,height=height)
        Label(self.root,text="Marks Obtained",font=("goudy old style",15,"bold"),bg="lightgray",bd=2,relief=GROOVE).place(x=600,y=header_y,width=width,height=height)
        Label(self.root,text="Total Marks",font=("goudy old style",15,"bold"),bg="lightgray",bd=2,relief=GROOVE).place(x=750,y=header_y,width=width,height=height)
        Label(self.root,text="Percentage",font=("goudy old style",15,"bold"),bg="lightgray",bd=2,relief=GROOVE).place(x=900,y=header_y,width=width,height=height)
        
        #=====result_labels (Values - Dynamic) ===========
        self.roll=Label(self.root,font=("goudy old style",15,"bold"),bg="white",bd=2,relief=GROOVE)
        self.roll.place(x=150,y=result_y,width=width,height=height)
        
        self.name=Label(self.root,font=("goudy old style",15,"bold"),bg="white",bd=2,relief=GROOVE)
        self.name.place(x=300,y=result_y,width=width,height=height)
        
        self.course=Label(self.root,font=("goudy old style",15,"bold"),bg="white",bd=2,relief=GROOVE)
        self.course.place(x=450,y=result_y,width=width,height=height)
        
        self.marks=Label(self.root,font=("goudy old style",15,"bold"),bg="white",bd=2,relief=GROOVE)
        self.marks.place(x=600,y=result_y,width=width,height=height)
        
        self.full=Label(self.root,font=("goudy old style",15,"bold"),bg="white",bd=2,relief=GROOVE)
        self.full.place(x=750,y=result_y,width=width,height=height)
        
        self.per=Label(self.root,font=("goudy old style",15,"bold"),bg="white",bd=2,relief=GROOVE)
        self.per.place(x=900,y=result_y,width=width,height=height)
        
        #======= button delete=======
        Button(self.root,text='Delete Result',font=("goudy old style",15,"bold"),bg="red",fg="white",cursor="hand2",command=self.delete).place(x=500,y=350,width=200,height=35)

    # --- Methods ---
    def search(self):
        con=sqlite3.connect(database="rms.db") 
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Roll No. should be required",parent=self.root)
            else:
              # Fetches ONE result for the roll number
              cur.execute("select * from result where roll=?",(self.var_search.get(),))
              row=cur.fetchone()
              
              if row!=None:
                # row structure: (rid, roll, name, course, marks_ob, full_marks, per)
                self.var_roll_to_delete = row[1] 
                self.roll.config(text=row[1])
                self.name.config(text=row[2])
                self.course.config(text=row[3])
                self.marks.config(text=row[4])
                self.full.config(text=row[5])
                self.per.config(text=row[6] + "%")
              else:
                messagebox.showerror("Error","No record found for this roll number",parent=self.root)
                self.clear() 
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")
        finally:
            if con:
                con.close()

    def clear(self):
        self.var_roll_to_delete=""
        self.roll.config(text="")
        self.name.config(text="")
        self.course.config(text="")
        self.marks.config(text="")
        self.full.config(text="")
        self.per.config(text="")
        self.var_search.set("")

    def delete(self):
        con=sqlite3.connect(database="rms.db") 
        cur=con.cursor()
        try:
            if self.var_roll_to_delete=="":
                messagebox.showerror("Error","Search Student result first to delete",parent=self.root)
            else:
                op=messagebox.askyesno("Confirm",f"Do you really want to delete ALL results for Roll No. {self.var_roll_to_delete}?",parent=self.root)
                if op==True:
                    # Deletes ALL results for the displayed roll number
                    cur.execute("delete from result where roll=?",(self.var_roll_to_delete,))
                    con.commit()
                    messagebox.showinfo("Delete","Result(s) deleted successfully",parent=self.root)
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")
        finally:
            if con:
                con.close()

if __name__=="__main__":
    root=Tk()
    obj=reportClass(root)
    root.mainloop()