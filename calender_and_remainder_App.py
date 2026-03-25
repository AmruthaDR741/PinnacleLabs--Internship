import tkinter as tk
from tkinter import messagebox, ttk
import calendar
from datetime import datetime, timedelta
import json
import os
from tkinter import font

class CalendarReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar & Reminder App")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        
        # Current date
        self.current_date = datetime.now()
        self.selected_date = self.current_date
        
        # Reminders storage
        self.reminders_file = "reminders.json"
        self.reminders = self.load_reminders()
        
        # Colors and styles
        self.bg_color = "#f0f0f0"
        self.header_color = "#2c3e50"
        self.header_text_color = "white"
        self.day_color = "#3498db"
        self.today_color = "#e74c3c"
        self.reminder_color = "#27ae60"
        self.weekend_color = "#95a5a6"
        
        self.root.configure(bg=self.bg_color)
        
        # Setup UI
        self.setup_ui()
        self.display_calendar()
        self.display_reminders()
    
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Calendar
        left_panel = tk.Frame(main_frame, bg="white", relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Calendar header
        self.cal_header = tk.Frame(left_panel, bg=self.header_color)
        self.cal_header.pack(fill=tk.X)
        
        # Navigation buttons
        self.prev_btn = tk.Button(self.cal_header, text="◀", command=self.prev_month,
                                  bg=self.header_color, fg=self.header_text_color,
                                  font=("Arial", 12, "bold"), bd=0, padx=10)
        self.prev_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.month_year_label = tk.Label(self.cal_header, bg=self.header_color,
                                         fg=self.header_text_color,
                                         font=("Arial", 14, "bold"))
        self.month_year_label.pack(side=tk.LEFT, expand=True, pady=5)
        
        self.next_btn = tk.Button(self.cal_header, text="▶", command=self.next_month,
                                  bg=self.header_color, fg=self.header_text_color,
                                  font=("Arial", 12, "bold"), bd=0, padx=10)
        self.next_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Weekdays header
        weekdays_frame = tk.Frame(left_panel, bg=self.day_color)
        weekdays_frame.pack(fill=tk.X)
        
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(weekdays):
            label = tk.Label(weekdays_frame, text=day, bg=self.day_color,
                           fg="white", font=("Arial", 10, "bold"), width=10)
            label.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=1, pady=2)
        
        # Calendar grid
        self.calendar_frame = tk.Frame(left_panel, bg="white")
        self.calendar_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Right panel - Reminders
        right_panel = tk.Frame(main_frame, bg="white", relief=tk.RAISED, bd=2, width=300)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        right_panel.pack_propagate(False)
        
        # Reminder header
        reminder_header = tk.Frame(right_panel, bg=self.header_color)
        reminder_header.pack(fill=tk.X)
        
        tk.Label(reminder_header, text="Reminders", bg=self.header_color,
                fg=self.header_text_color, font=("Arial", 14, "bold")).pack(pady=10)
        
        # Selected date display
        self.date_label = tk.Label(right_panel, text="", font=("Arial", 12, "bold"),
                                   bg="white", fg=self.day_color)
        self.date_label.pack(pady=5)
        
        # Reminder input
        input_frame = tk.Frame(right_panel, bg="white")
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(input_frame, text="New Reminder:", bg="white",
                font=("Arial", 10)).pack(anchor=tk.W)
        
        self.reminder_entry = tk.Text(input_frame, height=3, width=30,
                                      font=("Arial", 10))
        self.reminder_entry.pack(fill=tk.X, pady=5)
        
        # Time selector
        time_frame = tk.Frame(input_frame, bg="white")
        time_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(time_frame, text="Time (HH:MM):", bg="white",
                font=("Arial", 10)).pack(side=tk.LEFT)
        
        self.time_entry = tk.Entry(time_frame, width=10, font=("Arial", 10))
        self.time_entry.pack(side=tk.LEFT, padx=5)
        self.time_entry.insert(0, "09:00")
        
        # Priority selector
        priority_frame = tk.Frame(input_frame, bg="white")
        priority_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(priority_frame, text="Priority:", bg="white",
                font=("Arial", 10)).pack(side=tk.LEFT)
        
        self.priority_var = tk.StringVar(value="Medium")
        priorities = ["High", "Medium", "Low"]
        priority_menu = ttk.Combobox(priority_frame, textvariable=self.priority_var,
                                     values=priorities, width=10, state="readonly")
        priority_menu.pack(side=tk.LEFT, padx=5)
        
        # Buttons
        btn_frame = tk.Frame(input_frame, bg="white")
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame, text="Add Reminder", command=self.add_reminder,
                 bg=self.reminder_color, fg="white", font=("Arial", 10, "bold"),
                 padx=10, pady=5).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Delete Selected", command=self.delete_reminder,
                 bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                 padx=10, pady=5).pack(side=tk.LEFT, padx=5)
        
        # Reminders list
        list_frame = tk.Frame(right_panel, bg="white")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        tk.Label(list_frame, text="Reminders for selected date:", bg="white",
                font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        # Listbox with scrollbar
        list_container = tk.Frame(list_frame, bg="white")
        list_container.pack(fill=tk.BOTH, expand=True, pady=5)
        
        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.reminders_listbox = tk.Listbox(list_container, yscrollcommand=scrollbar.set,
                                           font=("Arial", 10), height=15,
                                           selectmode=tk.SINGLE)
        self.reminders_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.reminders_listbox.yview)
        
        # Delete all button
        tk.Button(list_frame, text="Delete All for Date", command=self.delete_all_reminders,
                 bg="#95a5a6", fg="white", font=("Arial", 10),
                 padx=10, pady=5).pack(pady=5)
    
    def display_calendar(self):
        # Clear previous calendar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        
        # Update month/year label
        month_year = self.current_date.strftime("%B %Y")
        self.month_year_label.config(text=month_year)
        
        # Get calendar data
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)
        
        # Display days
        today = datetime.now().date()
        
        for week in cal:
            week_frame = tk.Frame(self.calendar_frame, bg="white")
            week_frame.pack(fill=tk.X, expand=True, pady=1)
            
            for day in week:
                day_frame = tk.Frame(week_frame, bg="white", relief=tk.RIDGE, bd=1)
                day_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=1)
                
                if day != 0:
                    # Create date object for this day
                    date_obj = datetime(self.current_date.year, self.current_date.month, day).date()
                    
                    # Determine background color
                    if date_obj == today:
                        bg_color = self.today_color
                        fg_color = "white"
                    elif date_obj.weekday() >= 5:  # Weekend
                        bg_color = self.weekend_color
                        fg_color = "white"
                    else:
                        bg_color = "white"
                        fg_color = "black"
                    
                    # Check if date has reminders
                    date_str = date_obj.strftime("%Y-%m-%d")
                    if date_str in self.reminders and self.reminders[date_str]:
                        # Add reminder indicator
                        day_frame.configure(bg=self.reminder_color)
                        bg_color = self.reminder_color
                        fg_color = "white"
                    
                    # Day number
                    day_label = tk.Label(day_frame, text=str(day), bg=bg_color,
                                       fg=fg_color, font=("Arial", 10, "bold"))
                    day_label.pack(pady=2)
                    
                    # Make clickable
                    day_label.bind("<Button-1>", lambda e, d=date_obj: self.select_date(d))
                    day_frame.bind("<Button-1>", lambda e, d=date_obj: self.select_date(d))
                    
                    # Preview of first reminder if exists
                    if date_str in self.reminders and self.reminders[date_str]:
                        preview = self.reminders[date_str][0]['text'][:15] + "..."
                        preview_label = tk.Label(day_frame, text=preview, bg=bg_color,
                                               fg=fg_color, font=("Arial", 7))
                        preview_label.pack(pady=1)
                        preview_label.bind("<Button-1>", lambda e, d=date_obj: self.select_date(d))
    
    def select_date(self, date_obj):
        self.selected_date = date_obj
        self.date_label.config(text=f"Selected: {date_obj.strftime('%B %d, %Y')}")
        self.display_reminders()
    
    def add_reminder(self):
        reminder_text = self.reminder_entry.get("1.0", tk.END).strip()
        reminder_time = self.time_entry.get().strip()
        priority = self.priority_var.get()
        
        if not reminder_text:
            messagebox.showwarning("Warning", "Please enter a reminder text!")
            return
        
        # Validate time format
        try:
            datetime.strptime(reminder_time, "%H:%M")
        except ValueError:
            messagebox.showwarning("Warning", "Please enter time in HH:MM format!")
            return
        
        date_str = self.selected_date.strftime("%Y-%m-%d")
        
        if date_str not in self.reminders:
            self.reminders[date_str] = []
        
        # Add reminder
        reminder = {
            'text': reminder_text,
            'time': reminder_time,
            'priority': priority,
            'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.reminders[date_str].append(reminder)
        
        # Sort reminders by time
        self.reminders[date_str].sort(key=lambda x: x['time'])
        
        # Clear input
        self.reminder_entry.delete("1.0", tk.END)
        
        # Save to file
        self.save_reminders()
        
        # Update displays
        self.display_calendar()
        self.display_reminders()
        
        messagebox.showinfo("Success", "Reminder added successfully!")
    
    def delete_reminder(self):
        selection = self.reminders_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a reminder to delete!")
            return
        
        date_str = self.selected_date.strftime("%Y-%m-%d")
        if date_str in self.reminders:
            index = selection[0]
            if index < len(self.reminders[date_str]):
                del self.reminders[date_str][index]
                
                # Remove date key if no reminders left
                if not self.reminders[date_str]:
                    del self.reminders[date_str]
                
                self.save_reminders()
                self.display_calendar()
                self.display_reminders()
    
    def delete_all_reminders(self):
        date_str = self.selected_date.strftime("%Y-%m-%d")
        if date_str in self.reminders:
            result = messagebox.askyesno("Confirm", f"Delete all reminders for {date_str}?")
            if result:
                del self.reminders[date_str]
                self.save_reminders()
                self.display_calendar()
                self.display_reminders()
    
    def display_reminders(self):
        self.reminders_listbox.delete(0, tk.END)
        date_str = self.selected_date.strftime("%Y-%m-%d")
        
        if date_str in self.reminders and self.reminders[date_str]:
            for reminder in self.reminders[date_str]:
                # Format display with priority
                priority_symbol = "🔴" if reminder['priority'] == "High" else "🟡" if reminder['priority'] == "Medium" else "🟢"
                display_text = f"{priority_symbol} [{reminder['time']}] {reminder['text']}"
                self.reminders_listbox.insert(tk.END, display_text)
                
                # Color code based on priority
                if reminder['priority'] == "High":
                    self.reminders_listbox.itemconfig(tk.END, fg="#e74c3c")
                elif reminder['priority'] == "Medium":
                    self.reminders_listbox.itemconfig(tk.END, fg="#f39c12")
        else:
            self.reminders_listbox.insert(tk.END, "No reminders for this date")
    
    def prev_month(self):
        self.current_date = self.current_date.replace(day=1) - timedelta(days=1)
        self.display_calendar()
    
    def next_month(self):
        next_month = self.current_date.replace(day=28) + timedelta(days=4)
        self.current_date = next_month - timedelta(days=next_month.day)
        self.display_calendar()
    
    def load_reminders(self):
        if os.path.exists(self.reminders_file):
            try:
                with open(self.reminders_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_reminders(self):
        with open(self.reminders_file, 'w') as f:
            json.dump(self.reminders, f, indent=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarReminderApp(root)
    root.mainloop()