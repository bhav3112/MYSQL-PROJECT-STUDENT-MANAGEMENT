import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import get_connection
import matplotlib.pyplot as plt
import csv

# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("Student Performance Analysis System")
root.geometry("1350x700")

# ---------------- TABLE ----------------
columns = (
    "ID", "Gender", "Race", "Parent Education",
    "Lunch", "Prep", "Math", "Reading", "Writing"
)

tree = ttk.Treeview(root, columns=columns, show="headings")
tree.pack(fill=tk.BOTH, expand=True)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=140)

tree.tag_configure("updated", background="lightyellow")

# ---------------- COMMON ----------------
def clear_table():
    for r in tree.get_children():
        tree.delete(r)

def load_data(query="SELECT * FROM performance"):
    clear_table()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)
    conn.close()

# ---------------- FILTER & SEARCH ----------------
def filter_gender():
    g = gender_var.get()
    load_data() if g == "" else load_data(
        f"SELECT * FROM performance WHERE gender='{g}'"
    )

def search_data():
    v = search_entry.get()
    load_data() if v == "" else load_data(
        f"""SELECT * FROM performance
            WHERE gender LIKE '%{v}%'
            OR parental_education LIKE '%{v}%'"""
    )

# ---------------- TOPPERS ----------------
def overall_topper():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, gender, math_score, reading_score, writing_score,
        (math_score+reading_score+writing_score) total
        FROM performance ORDER BY total DESC LIMIT 1
    """)
    t = cursor.fetchone()
    conn.close()
    messagebox.showinfo(
        "Overall Topper",
        f"Student ID: {t[0]}\nGender: {t[1]}"
        f"\nMath: {t[2]}\nReading: {t[3]}"
        f"\nWriting: {t[4]}\nTotal: {t[5]}"
    )

def subject_topper(sub):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT id, gender, {sub}_score FROM performance "
        f"ORDER BY {sub}_score DESC LIMIT 1"
    )
    t = cursor.fetchone()
    conn.close()
    messagebox.showinfo(
        f"{sub.capitalize()} Topper",
        f"Student ID: {t[0]}\nGender: {t[1]}"
        f"\nScore: {t[2]}"
    )

# ---------------- UPDATE SCORE ----------------
def update_score():
    sel = tree.focus()
    if not sel:
        messagebox.showerror("Error", "Select a student")
        return

    try:
        marks = int(marks_entry.get())
    except:
        messagebox.showerror("Error", "Enter valid marks")
        return

    subject_map = {
        "Math": "math_score",
        "Reading": "reading_score",
        "Writing": "writing_score"
    }

    col = subject_map[subject_var.get()]
    sid = tree.item(sel)["values"][0]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE performance SET {col}={col}+%s WHERE id=%s",
        (marks, sid)
    )
    conn.commit()
    conn.close()

    load_data()
    tree.item(sel, tags=("updated",))
    messagebox.showinfo("Updated", "Score updated successfully")

# ---------------- RANK LIST ----------------
def show_rank_list():
    clear_table()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, gender, race_ethnicity, parental_education,
        lunch, test_prep, math_score, reading_score, writing_score,
        (math_score+reading_score+writing_score) total
        FROM performance ORDER BY total DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    rank = 1
    for r in rows:
        tree.insert("", tk.END, values=r[:-1])
        rank += 1

# ---------------- PASS / FAIL ----------------
def show_pass_fail():
    clear_table()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT *, CASE
        WHEN math_score>=35 AND reading_score>=35 AND writing_score>=35
        THEN 'PASS' ELSE 'FAIL' END
        FROM performance
    """)
    for r in cursor.fetchall():
        tree.insert("", tk.END, values=r[:-1])
    conn.close()

# ---------------- CHARTS ----------------
def avg_chart():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT AVG(math_score),AVG(reading_score),AVG(writing_score) FROM performance"
    )
    a = cursor.fetchone()
    conn.close()
    plt.bar(["Math","Reading","Writing"], a)
    plt.title("Average Scores")
    plt.show()

def gender_chart():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT gender,AVG(math_score) FROM performance GROUP BY gender"
    )
    d = cursor.fetchall()
    conn.close()
    plt.bar([x[0] for x in d], [x[1] for x in d])
    plt.title("Gender-wise Math Performance")
    plt.show()

def subject_compare():
    avg_chart()

# ---------------- EXPORT ----------------
def export_all():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM performance")
    rows = cursor.fetchall()
    conn.close()
    with open("all_students.csv","w",newline="") as f:
        csv.writer(f).writerows(rows)
    messagebox.showinfo("Export", "All data exported")

def export_female():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM performance WHERE gender='female'")
    rows = cursor.fetchall()
    conn.close()
    with open("female_students.csv","w",newline="") as f:
        csv.writer(f).writerows(rows)
    messagebox.showinfo("Export", "Female data exported")

# ---------------- CONTROLS ----------------
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Button(frame,text="Load All",command=load_data).grid(row=0,column=0)
gender_var=tk.StringVar()
ttk.Combobox(frame,textvariable=gender_var,
             values=["male","female"],
             state="readonly",width=10).grid(row=0,column=1)
tk.Button(frame,text="Filter Gender",command=filter_gender).grid(row=0,column=2)

search_entry=tk.Entry(frame,width=20)
search_entry.grid(row=0,column=3)
tk.Button(frame,text="Search",command=search_data).grid(row=0,column=4)
tk.Button(frame,text="Overall Topper",command=overall_topper).grid(row=0,column=5)

tk.Button(frame,text="Math Topper",command=lambda:subject_topper("math")).grid(row=1,column=0)
tk.Button(frame,text="Reading Topper",command=lambda:subject_topper("reading")).grid(row=1,column=1)
tk.Button(frame,text="Writing Topper",command=lambda:subject_topper("writing")).grid(row=1,column=2)
tk.Button(frame,text="Rank List",command=show_rank_list).grid(row=1,column=3)
tk.Button(frame,text="Pass / Fail",command=show_pass_fail).grid(row=1,column=4)

subject_var=tk.StringVar(value="Math")
ttk.Combobox(frame,textvariable=subject_var,
             values=["Math","Reading","Writing"],
             state="readonly",width=10).grid(row=2,column=0)
marks_entry=tk.Entry(frame,width=10)
marks_entry.grid(row=2,column=1)
tk.Button(frame,text="Update Score",command=update_score).grid(row=2,column=2)

tk.Button(frame,text="Average Chart",command=avg_chart).grid(row=3,column=0)
tk.Button(frame,text="Gender Chart",command=gender_chart).grid(row=3,column=1)
tk.Button(frame,text="Export All CSV",command=export_all).grid(row=3,column=2)
tk.Button(frame,text="Export Female CSV",command=export_female).grid(row=3,column=3)

# ---------------- START ----------------
load_data()
root.mainloop()
