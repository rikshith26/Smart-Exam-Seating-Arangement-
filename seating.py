import tkinter as tk
from tkinter import ttk, messagebox

# -----------------------------
# Quick Sort for students
# -----------------------------
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr)//2]
    left = [x for x in arr if (x[2], x[1]) < (pivot[2], pivot[1])]
    middle = [x for x in arr if (x[2], x[1]) == (pivot[2], pivot[1])]
    right = [x for x in arr if (x[2], x[1]) > (pivot[2], pivot[1])]
    return quick_sort(left) + middle + quick_sort(right)

# -----------------------------
# Seating Arrangement Logic
# -----------------------------
def arrange_seating(students, num_classes, benches_per_class):
    students = quick_sort(students)
    total_benches = num_classes * benches_per_class
    if len(students) > total_benches:
        messagebox.showerror("Error", "Not enough benches for all students!")
        return []

    seating = []
    class_num, bench_num = 1, 1
    for student in students:
        seating.append((student[0], student[1], student[2], class_num, bench_num))
        bench_num += 1
        if bench_num > benches_per_class:
            bench_num = 1
            class_num += 1
            if class_num > num_classes:
                class_num = 1
    return seating

# -----------------------------
# GUI Functions
# -----------------------------
def add_student():
    sid = entry_sid.get()
    sub = entry_sub.get()
    dept = entry_dept.get()
    if not sid or not sub or not dept:
        messagebox.showwarning("Input Error", "All fields are required!")
        return
    students.append((sid, sub, dept))
    listbox_students.insert(tk.END, f"{sid} | {sub} | {dept}")
    entry_sid.delete(0, tk.END)
    entry_sub.delete(0, tk.END)
    entry_dept.delete(0, tk.END)

def generate_seating():
    try:
        num_classes = int(entry_classes.get())
        benches_per_class = int(entry_benches.get())
    except ValueError:
        messagebox.showerror("Input Error", "Classes and benches must be integers")
        return
    if not students:
        messagebox.showwarning("No Students", "Add students first!")
        return
    arrangement = arrange_seating(students, num_classes, benches_per_class)
    for row in tree.get_children():
        tree.delete(row)
    color_map = {"CSE": "#FFCCCC", "ECE": "#CCFFCC", "MECH": "#CCCCFF", "OTHER": "#FFFFCC"}
    for sid, sub, dept, cls, bench in arrangement:
        color = color_map.get(dept.upper(), color_map["OTHER"])
        tree.insert("", tk.END, values=(sid, dept, sub, cls, bench), tags=('color',))
        tree.tag_configure('color', background=color)

# -----------------------------
# GUI Setup
# -----------------------------
root = tk.Tk()
root.title("Smart Exam Seating Arrangement")
root.geometry("750x600")

students = []

# Input frame
frame_input = tk.LabelFrame(root, text="Add Student", padx=10, pady=10)
frame_input.pack(padx=10, pady=10, fill="x")

tk.Label(frame_input, text="Student ID").grid(row=0, column=0, padx=5, pady=5)
tk.Label(frame_input, text="Subject Code").grid(row=0, column=1, padx=5, pady=5)
tk.Label(frame_input, text="Department").grid(row=0, column=2, padx=5, pady=5)

entry_sid = tk.Entry(frame_input)
entry_sid.grid(row=1, column=0, padx=5, pady=5)
entry_sub = tk.Entry(frame_input)
entry_sub.grid(row=1, column=1, padx=5, pady=5)
entry_dept = tk.Entry(frame_input)
entry_dept.grid(row=1, column=2, padx=5, pady=5)

btn_add = tk.Button(frame_input, text="Add Student", command=add_student)
btn_add.grid(row=1, column=3, padx=10, pady=5)

# Listbox to show students
listbox_students = tk.Listbox(root, height=6)
listbox_students.pack(padx=10, pady=5, fill="x")

# Classes & Benches input
frame_cb = tk.Frame(root)
frame_cb.pack(padx=10, pady=5, fill="x")
tk.Label(frame_cb, text="Number of Classes").grid(row=0, column=0, padx=5, pady=5)
tk.Label(frame_cb, text="Benches per Class").grid(row=0, column=1, padx=5, pady=5)
entry_classes = tk.Entry(frame_cb)
entry_classes.grid(row=1, column=0, padx=5, pady=5)
entry_benches = tk.Entry(frame_cb)
entry_benches.grid(row=1, column=1, padx=5, pady=5)

btn_generate = tk.Button(root, text="Generate Seating Arrangement", command=generate_seating)
btn_generate.pack(pady=10)

# Treeview for seating arrangement
columns = ("Student ID", "Department", "Subject", "Class", "Bench")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120, anchor="center")
tree.pack(padx=10, pady=10, fill="x")

root.mainloop()
