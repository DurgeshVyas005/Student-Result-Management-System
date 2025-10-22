# dashboard.py

from tkinter import *
from PIL import Image, ImageTk, ImageDraw
from tkinter import messagebox
import sqlite3
from course import CourseClass
from student import studentClass
from result import resultClass
from report import reportClass

class RMS:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        # Start maximized for best centering effect
        try:
            self.root.state('zoomed') 
        except TclError:
            # Fallback for systems that don't support 'zoomed' (e.g., some Linux WMs)
            self.root.geometry("1350x700+0+0") 
            
        self.root.config(bg="white") 

        # Variables for summary counts
        self.var_courses = StringVar(value="[ 0 ]")
        self.var_students = StringVar(value="[ 0 ]")
        self.var_results = StringVar(value="[ 0 ]")

        # ===title====
        title = Label(self.root, text="Student Result Management System", padx=20,
                      font=("goudy old style", 24, "bold"), bg="#033054", fg="white", anchor="center")
        title.place(x=0, y=0, relwidth=1, height=70)

        # ===Menu====
        M_Frame = Frame(self.root, bg="white")
        # Use relx=0.5, anchor=N to keep the menu centered horizontally
        M_Frame.place(relx=0.5, y=80, width=1330, height=80, anchor=N)

        # Menu Buttons (Relative placement is within M_Frame)
        Button(M_Frame, text="Course", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.add_course).place(x=20, y=20, width=200, height=40)
        Button(M_Frame, text="Student", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.add_student).place(x=240, y=20, width=200, height=40)
        Button(M_Frame, text="Result", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.add_result).place(x=460, y=20, width=200, height=40)
        Button(M_Frame, text="View Student Result", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.view_result).place(x=680, y=20, width=200, height=40)
        Button(M_Frame, text="Logout", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.logout).place(x=900, y=20, width=200, height=40)
        Button(M_Frame, text="Exit", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.root.destroy).place(x=1120, y=20, width=200, height=40)

        # ===content_window (Image)====
        try:
            # Assuming the image is in a subdirectory 'images' or the current directory
            self.bg_img = Image.open("images/dashboard.png") 
            self.bg_img = self.bg_img.resize((920, 350), Image.Resampling.LANCZOS)
            self.bg_img = ImageTk.PhotoImage(self.bg_img)
        except Exception:
            self.bg_img = None
            
        self.lbl_bg = Label(self.root, image=self.bg_img, bg="white")
        # **FIX 1: Use relative positioning for perfect centering**
        self.lbl_bg.place(relx=0.5, rely=0.45, anchor=CENTER, width=920, height=350)
        
        # ===update_details (Summary Boxes)===
        box_width = 300
        gap = 30
        
        # FIX 2: Create a separate frame for the summary boxes and center it
        Summary_Frame = Frame(self.root, bg="white")
        total_width = 3 * box_width + 2 * gap
        Summary_Frame.place(relx=0.5, y=560, width=total_width, height=100, anchor=N)

        summary_data = [
            ("Total Courses\n", self.var_courses, "#e43b06"),
            ("Total Students\n", self.var_students, "#0676ad"),
            ("Total Results\n", self.var_results, "#038074")
        ]

        for i, (text, var, color) in enumerate(summary_data):
            x_pos = i * (box_width + gap) # x position relative to Summary_Frame
            
            box_frame = Frame(Summary_Frame, bd=10, relief=RIDGE, bg=color)
            box_frame.place(x=x_pos, y=0, width=box_width, height=100)
            
            # Label for the static text (e.g., "Total Courses")
            Label(box_frame, text=text, font=("goudy old style", 15), 
                  bg=color, fg="white").pack(pady=(5,0))
            
            # Label for the variable content (the count)
            Label(box_frame, textvariable=var, font=("goudy old style", 20, "bold"), 
                  bg=color, fg="white").pack()
            
        self.update_details() 

        # ===footer====
        footer = Label(self.root, text="SRMS - Student Result Management System",
                       font=("goudy old style", 12), bg="#262626", fg="white")
        footer.pack(side=BOTTOM, fill=X)
        
    # --- Menu Button Commands (No changes here) ---
    def add_course(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = CourseClass(self.new_win)

    def add_student(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = studentClass(self.new_win)
        
    def add_result(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = resultClass(self.new_win)

    def view_result(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = reportClass(self.new_win)
        
    def logout(self):
        op = messagebox.askyesno("Confirm", "Do you really want to Logout?", parent=self.root)
        if op == True:
            self.root.destroy()
            
    def update_details(self):
        # ... (Database update logic remains the same) ...
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("select * from course")
            self.var_courses.set(f"[ {len(cur.fetchall())} ]")
            
            cur.execute("select * from student")
            self.var_students.set(f"[ {len(cur.fetchall())} ]")
            
            cur.execute("select * from result")
            self.var_results.set(f"[ {len(cur.fetchall())} ]")
            
        except Exception as ex:
            print(f"Error updating details: {str(ex)}")
        finally:
            if con:
                con.close()
            
        self.root.after(5000, self.update_details)


if __name__ == "__main__":
    root = Tk()
    obj = RMS(root)
    root.mainloop()