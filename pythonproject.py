import tkinter as tk
from tkinter import ttk
import calendar
from datetime import datetime


class CalendarApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calendar GUI Application")
        self.geometry("1200x800")
        self.configure(bg="#f7f9fc")
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        self.today = datetime.now()
        self.events = {}  # Dictionary to store events
        self.create_widgets()

    def create_widgets(self):
        # Header Frame
        self.header_frame = ttk.Frame(self, style="Header.TFrame")
        self.header_frame.pack(fill=tk.X, pady=10)

        self.title_label = tk.Label(
            self.header_frame,
            text="Calendar",
            font=("Helvetica", 24, "bold"),
            bg="#4a90e2",
            fg="white",
        )
        self.title_label.pack(side=tk.TOP, pady=5, fill=tk.X)

        self.navigation_frame = ttk.Frame(self.header_frame)
        self.navigation_frame.pack(side=tk.BOTTOM, pady=5)

        self.prev_button = ttk.Button(self.navigation_frame, text="<<", command=self.prev_month)
        self.prev_button.pack(side=tk.LEFT, padx=20)

        self.next_button = ttk.Button(self.navigation_frame, text=">>", command=self.next_month)
        self.next_button.pack(side=tk.RIGHT, padx=20)

        # Main layout for calendar and events
        self.main_frame = tk.Frame(self, bg="#f7f9fc")
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Calendar Section
        self.calendar_frame = ttk.Frame(self.main_frame, relief="ridge")
        self.calendar_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Event Information Section
        self.info_frame = ttk.Frame(self.main_frame, relief="ridge")
        self.info_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Configure responsive resizing
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=2)
        self.main_frame.columnconfigure(1, weight=1)

        # Right Panel: Event Info
        self.info_label = tk.Label(
            self.info_frame, text="Event Information", font=("Helvetica", 16, "bold"), bg="#f7f9fc"
        )
        self.info_label.pack(pady=10)

        today_label = tk.Label(self.info_frame, text="Today:", font=("Helvetica", 12), bg="#f7f9fc")
        today_label.pack(anchor="w", padx=10, pady=5)

        self.today_display = tk.Frame(self.info_frame, bg="yellow", height=40, width=200)
        self.today_display.pack(padx=10, pady=5, anchor="w")
        self.today_display.pack_propagate(False)

        current_date_label = tk.Label(
            self.today_display, text=self.today.strftime("%Y-%m-%d"), font=("Helvetica", 12), bg="yellow"
        )
        current_date_label.pack(fill=tk.BOTH)

        event_label = tk.Label(self.info_frame, text="Events Added:", font=("Helvetica", 12), bg="#f7f9fc")
        event_label.pack(anchor="w", padx=10, pady=5)

        # Reduced the height of event display panel
        self.event_display = tk.Frame(self.info_frame, bg="lightblue", height=200, width=200)  # Shortened height
        self.event_display.pack(padx=10, pady=5, anchor="w")
        self.event_display.pack_propagate(False)

        self.event_list = tk.Label(
            self.event_display, text="", font=("Helvetica", 10), bg="lightblue", anchor="nw", justify="left", wraplength=180
        )
        self.event_list.pack(fill=tk.BOTH, expand=True)

        self.update_calendar()

    def update_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        cal = calendar.monthcalendar(self.current_year, self.current_month)
        month_name = calendar.month_name[self.current_month]
        self.title_label.config(text=f"{month_name} {self.current_year}")

        # Configure grid layout
        for i in range(7):
            self.calendar_frame.columnconfigure(i, weight=1)
        for i in range(len(cal) + 1):
            self.calendar_frame.rowconfigure(i, weight=1)

        # Day Headers
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for col, day in enumerate(days):
            day_label = tk.Label(
                self.calendar_frame,
                text=day,
                font=("Helvetica", 14, "bold"),
                bg="#dfe7f2",
                fg="#333333",
                relief="raised",
            )
            day_label.grid(row=0, column=col, sticky="nsew", padx=2, pady=2)

        # Add calendar days
        for row, week in enumerate(cal, start=1):
            for col, day in enumerate(week):
                frame = tk.Frame(self.calendar_frame, bg="white", relief="ridge", borderwidth=1)
                frame.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)

                if day == 0:
                    continue

                bg_color = "yellow" if (
                    self.current_year == self.today.year
                    and self.current_month == self.today.month
                    and day == self.today.day
                ) else "white"

                # Date Label
                date_label = tk.Label(frame, text=str(day), font=("Helvetica", 12), bg=bg_color, anchor="n")
                date_label.pack(fill=tk.X, pady=(5, 2))

                # Event Label
                date_key = f"{self.current_year}-{self.current_month:02}-{day:02}"
                events_label = tk.Label(
                    frame, text="", font=("Helvetica", 10), bg="white", anchor="nw", wraplength=75
                )
                events_label.pack(fill=tk.BOTH, expand=True)

                if date_key in self.events:
                    events_text = "\n".join(self.events[date_key])
                    events_label.config(text=events_text, bg="lightblue")

                # Click to Add Events
                frame.bind("<Button-1>", lambda e, d=day, lbl=events_label: self.add_event(d, lbl))
                date_label.bind("<Button-1>", lambda e, d=day, lbl=events_label: self.add_event(d, lbl))
                events_label.bind("<Button-1>", lambda e, d=day, lbl=events_label: self.add_event(d, lbl))

    def add_event(self, day, event_label):
        date_key = f"{self.current_year}-{self.current_month:02}-{day:02}"

        event_window = tk.Toplevel(self)
        event_window.title(f"Add Event for {date_key}")
        event_window.geometry("400x300")

        label = tk.Label(event_window, text=f"Select or Add Event for {date_key}:", font=("Helvetica", 12))
        label.pack(pady=10)

        # Dropdown for predefined options
        options = ["Meeting", "Anniversary", "Birthday", "Exam", "D-Day", "Holiday", "Other"]
        selected_option = tk.StringVar()
        selected_option.set("None")  # Default option
        dropdown = ttk.Combobox(event_window, textvariable=selected_option, values=options, state="readonly")
        dropdown.pack(pady=5)

        # Custom event entry (Initially hidden)
        custom_label = tk.Label(event_window, text="Custom Event (if 'Other' selected):")
        custom_label.pack(pady=5)
        custom_entry = tk.Entry(event_window, width=30)
        custom_entry.pack(pady=5)
        custom_entry.pack_forget()  # Hide the entry field initially

        def show_custom_entry(event):
            if selected_option.get() == "Other":
                custom_entry.pack(pady=5)  # Show the entry field when "Other" is selected
            else:
                custom_entry.pack_forget()  # Hide it for other selections

        dropdown.bind("<<ComboboxSelected>>", show_custom_entry)

        def save_event():
            event = selected_option.get()  # Get the selected option
            if event == "Other":
                custom_event = custom_entry.get().strip()
                event = custom_event if custom_event else "None"  # Use custom event or fallback to "None"

            if event == "None" and not custom_entry.get().strip():
                event = None  # Do not add event if "None" is selected and "Other" is empty

            if event:
                # Save event in dictionary
                if date_key not in self.events:
                    self.events[date_key] = []
                self.events[date_key].append(event)

                # Update event label in the calendar
                events_text = "\n".join(self.events[date_key])
                event_label.config(text=events_text, bg="lightblue")
                self.update_event_list()  # Refresh event summary on the side panel
            event_window.destroy()

        save_button = ttk.Button(event_window, text="Save Event", command=save_event)
        save_button.pack(pady=20)

    def update_event_list(self):
        events = [f"{key}: {', '.join(values)}" for key, values in self.events.items()]
        self.event_list.config(text="\n".join(events))

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.update_calendar()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.update_calendar()


if __name__ == "__main__":
    app = CalendarApp()
    app.mainloop()
