# result.py

from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3

class resultClass:
    def __init__(self,root):
        self.root = root
        self.root.title("Add Student Results")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg = 'white')
        self.root.focus_force()
        
        # --- Title ---
        title = Label(self.root,text = "Add Student Results",font=("goudy old style",20,"bold"),bg = "orange",fg = "#262626").place(x=10,y=15,width=1180,height=50)
        
        # --- Variables ---
        self.var_roll=StringVar()
        self.var_name=StringVar()
        self.var_course=StringVar()
        self.var_marks=StringVar()
        self.var_full_marks=StringVar() 
        self.roll_list=[]
        self.fetch_roll() 
        
        # --- Widgets ---
        lbl_select= Label(self.root,text = "Select Student Roll",font = ("goudy old style",20,'bold'),bg = 'white').place(x=50,y=100)
        lbl_name= Label(self.root,text = "Name",font = ("goudy old style",20,'bold'),bg ='white').place(x=50,y=160)
        lbl_course= Label(self.root,text = "Course",font = ("goudy old style",20,'bold'),bg = 'white').place(x=50,y=220)
        lbl_makrs_ob= Label(self.root,text = "Marks Obtained",font = ("goudy old style",20,'bold'),bg = 'white').place(x=50,y=280)
        lbl_full_marks=Label(self.root,text = "Full Marks ",font = ("goudy old style",20,'bold'),bg = 'white').place(x=50,y=340)
        
        self.txt_student =ttk.Combobox(self.root,textvariable = self.var_roll,values=self.roll_list,font = ("goudy old style",15,'bold'),state = 'readonly',justify=CENTER)
        self.txt_student.place(x=280,y=100,width=200)
        self.txt_student.set("Select")
        
        btn_search=Button(self.root,text='Search',font=("goudy old style",15,"bold"),bg="#2196f3",fg="white",cursor="hand2",command=self.search).place(x=500,y=100,width=120,height=28)
    
        Entry(self.root,textvariable=self.var_name,font=("goudy old style",15,'bold'),bg='lightyellow',state='readonly').place(x=280,y=160,width=320)
        Entry(self.root,textvariable=self.var_course,font=("goudy old style",15,'bold'),bg='lightyellow',state='readonly').place(x=280,y=220,width=320)
        Entry(self.root,textvariable=self.var_marks,font=("goudy old style",15,'bold'),bg='lightyellow').place(x=280,y=280,width=320)
        Entry(self.root,textvariable=self.var_full_marks,font=("goudy old style",15,'bold'),bg='lightyellow').place(x=280,y=340,width=320)
       
        # --- Buttons ---
        btn_add=Button(self.root,text="Submit",font=("times new roman",15),bg="lightgreen",activebackground="lightgreen",cursor="hand2",command=self.add).place(x=300,y=420,width=120,height=35)
        btn_clear=Button(self.root,text="Clear",font=("times new roman",15),bg="lightgray",activebackground="lightgray",cursor="hand2",command=self.clear).place(x=430,y=420,width=120,height=35)

        # --- Image ---
        try:
            self.bg_img=Image.open("C:\dbms pbl project\images\student.png") # Ensure image/bg.png exists
            self.bg_img=self.bg_img.resize((500,300),Image.Resampling.LANCZOS)
            self.bg_img=ImageTk.PhotoImage(self.bg_img)
        except FileNotFoundError:
            self.bg_img = None 
            messagebox.showerror("Error", "Image 'image/bg.png' not found.")

        self.lbl_bg=Label(self.root,image=self.bg_img, bg='white')
        self.lbl_bg.place(x=650,y=100)

    # --- Database and Logic Methods ---
    def fetch_roll(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            # Get roll numbers from the student table
            cur.execute("select roll from student") 
            rows=cur.fetchall()
            if len(rows)>0:
                self.roll_list = [row[0] for row in rows]
                if hasattr(self, 'txt_student'):
                    self.txt_student.config(values=self.roll_list)
        except Exception as ex:
            messagebox.showerror("Error",f"Error fetching rolls: {str(ex)}")

    def search(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            if self.var_roll.get() == "Select":
                messagebox.showerror("Error", "Please select a student roll number.", parent=self.root)
                return
                
            cur.execute("select name, course from student where roll=?",(self.var_roll.get(),))
            row=cur.fetchone()
            if row!=None:
              self.var_name.set(row[0])
              self.var_course.set(row[1])
            else:
                messagebox.showerror("Error","No student record found for this roll number",parent=self.root)      
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def add(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            if self.var_name.get()=="" or self.var_marks.get()=="" or self.var_full_marks.get()=="":
                messagebox.showerror("Error","Please search student and enter marks/full marks.",parent=self.root)
                return
            
            marks_ob = float(self.var_marks.get())
            full_marks = float(self.var_full_marks.get())
            
            if marks_ob > full_marks:
                messagebox.showerror("Error", "Marks Obtained cannot be greater than Full Marks.", parent=self.root)
                return
                
            cur.execute("select * from result where roll=? and course=?",(self.var_roll.get(),self.var_course.get()))
            row=cur.fetchone()
            
            if row!=None:
                messagebox.showerror("Error","Result already present for this student and course",parent=self.root)
            else:
                per = (marks_ob * 100) / full_marks
                
                cur.execute("insert into result (roll,name,course,marks_ob,full_marks,per) values(?,?,?,?,?,?)",(
                    self.var_roll.get(),
                    self.var_name.get(),
                    self.var_course.get(),
                    str(marks_ob),
                    str(full_marks),
                    str(round(per, 2))
                ))
                con.commit()
                messagebox.showinfo("Success","Result Added Successfully",parent=self.root)
                self.clear()
        except ValueError:
            messagebox.showerror("Error", "Marks and Full Marks must be valid numbers.", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def clear(self):
        self.var_roll.set("Select")
        self.var_name.set("")
        self.var_course.set("")
        self.var_marks.set("")
        self.var_full_marks.set("")
                                        
if __name__ == "__main__":
    root = Tk()
    obj = resultClass(root)
    root.mainloop()