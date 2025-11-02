import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import date

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Priyanka$&1234",
    database="blood_donation_db"
)
cursor = conn.cursor()

root = tk.Tk()
root.title("Blood Donation Management System")
root.geometry("700x500")
root.config(bg="white")

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

add_donor_tab = tk.Frame(notebook, bg="white")
notebook.add(add_donor_tab, text="Add Donor")

tk.Label(add_donor_tab, text="Add Donor", font=("Arial", 18, "bold"), bg="white", fg="red").pack(pady=10)

fields = ["Name", "Gender (Male/Female)", "Age", "Blood Group", "City", "Phone"]
entries = {}

for field in fields:
    frame = tk.Frame(add_donor_tab, bg="white")
    frame.pack(pady=5)
    tk.Label(frame, text=field, width=20, anchor='w', bg="white").pack(side="left")
    entry = tk.Entry(frame, width=30)
    entry.pack(side="left")
    entries[field] = entry

def add_donor():
    try:
        name = entries["Name"].get()
        gender = entries["Gender (Male/Female)"].get()
        age = int(entries["Age"].get())
        blood_group = entries["Blood Group"].get()
        city = entries["City"].get()
        phone = entries["Phone"].get()
        if not (name and gender and blood_group):
            messagebox.showerror("Error", "Please fill all mandatory fields.")
            return
        query = """
        INSERT INTO donors (name, gender, age, blood_group, city, phone, last_donation_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        data = (name, gender, age, blood_group, city, phone, date.today())
        cursor.execute(query, data)
        conn.commit()
        messagebox.showinfo("Success", "Donor added successfully!")
        for e in entries.values():
            e.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Age must be a number")

tk.Button(add_donor_tab, text="Add Donor", command=add_donor, bg="red", fg="white", width=15).pack(pady=10)

view_donor_tab = tk.Frame(notebook, bg="white")
notebook.add(view_donor_tab, text="View Donor")

tk.Label(view_donor_tab, text="View Donor Details", font=("Arial", 18, "bold"), bg="white", fg="blue").pack(pady=10)

tree = ttk.Treeview(view_donor_tab, columns=("id", "name", "blood", "city", "date"), show="headings")
tree.heading("id", text="ID")
tree.heading("name", text="Name")
tree.heading("blood", text="Blood Group")
tree.heading("city", text="City")
tree.heading("date", text="Last Donation")

tree.column("id", width=50)
tree.column("name", width=150)
tree.column("blood", width=100)
tree.column("city", width=100)
tree.column("date", width=120)
tree.pack(pady=10, fill="x")

def load_donors():
    tree.delete(*tree.get_children())
    cursor.execute("SELECT donor_id, name, blood_group, city, last_donation_date FROM donors")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

tk.Button(view_donor_tab, text="Load Donors", command=load_donors, bg="blue", fg="white").pack(pady=10)

add_camp_tab = tk.Frame(notebook, bg="white")
notebook.add(add_camp_tab, text="Add Camp")

tk.Label(add_camp_tab, text="Add Donation Camp", font=("Arial", 18, "bold"), bg="white", fg="green").pack(pady=10)

camp_fields = ["Camp Name", "Location", "Date (YYYY-MM-DD)", "Organizer"]
camp_entries = {}

for field in camp_fields:
    frame = tk.Frame(add_camp_tab, bg="white")
    frame.pack(pady=5)
    tk.Label(frame, text=field, width=20, anchor='w', bg="white").pack(side="left")
    entry = tk.Entry(frame, width=30)
    entry.pack(side="left")
    camp_entries[field] = entry

def add_camp():
    try:
        camp_name = camp_entries["Camp Name"].get()
        location = camp_entries["Location"].get()
        camp_date = camp_entries["Date (YYYY-MM-DD)"].get()
        organizer = camp_entries["Organizer"].get()
        if not (camp_name and location and camp_date):
            messagebox.showerror("Error", "Please fill all mandatory fields.")
            return
        cursor.execute(
            "INSERT INTO camps (camp_name, location, camp_date, organizer) VALUES (%s, %s, %s, %s)",
            (camp_name, location, camp_date, organizer)
        )
        conn.commit()
        messagebox.showinfo("Success", "Camp added successfully!")
        for e in camp_entries.values():
            e.delete(0, tk.END)
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))

tk.Button(add_camp_tab, text="Add Camp", command=add_camp, bg="green", fg="white", width=15).pack(pady=10)

stats_tab = tk.Frame(notebook, bg="white")
notebook.add(stats_tab, text="View Statistics")

tk.Label(stats_tab, text="Donation Statistics", font=("Arial", 18, "bold"), bg="white", fg="purple").pack(pady=10)

stats_text = tk.Text(stats_tab, height=15, width=80)
stats_text.pack(pady=10)

def show_stats():
    stats_text.delete(1.0, tk.END)
    cursor.execute("SELECT COUNT(*) FROM donors")
    total_donors = cursor.fetchone()[0]
    cursor.execute("SELECT city, COUNT(*) FROM donors GROUP BY city")
    city_data = cursor.fetchall()
    stats_text.insert(tk.END, f"Total Donors: {total_donors}\n\n")
    stats_text.insert(tk.END, "Donors by City:\n")
    for city, count in city_data:
        stats_text.insert(tk.END, f"  {city}: {count}\n")

tk.Button(stats_tab, text="Show Statistics", command=show_stats, bg="purple", fg="white", width=18).pack(pady=10)

root.mainloop()
