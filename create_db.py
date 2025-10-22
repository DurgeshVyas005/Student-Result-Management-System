import sqlite3

def create_db():
    try:
        con = sqlite3.connect("rms.db")
        cur = con.cursor()

        # 1. Course Table (Fixed: Syntax was mostly correct)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS course (
            cid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            duration TEXT,
            charges TEXT,
            description TEXT
        )
        """)

        # 2. Student Table (Fixed: Syntax error in column definitions)
        # Note: 'roll' is the PRIMARY KEY and is a TEXT field for flexibility, 
        # but is treated as unique identifier.
        cur.execute("""
        CREATE TABLE IF NOT EXISTS student (
            roll TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            gender TEXT,
            dob TEXT,
            contact TEXT,
            admission TEXT,
            course TEXT,
            state TEXT,
            city TEXT,
            pin TEXT,
            address TEXT
        )
        """)

        # 3. Result Table (Fixed: Syntax error and logical column definitions)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS result (
            rid INTEGER PRIMARY KEY AUTOINCREMENT,
            roll TEXT,
            name TEXT,
            course TEXT,
            marks_ob TEXT,
            full_marks TEXT,
            per TEXT,
            UNIQUE(roll, course) 
        )
        """)
        
        con.commit()
        print("Database (rms.db) and all tables created successfully.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if con:
            con.close()

if __name__ == '__main__':
    create_db()