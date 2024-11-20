import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create the main window
root = tk.Tk()
root.title("Attendance Tracker")
root.geometry("800x600")  # Set the window size

# Add a label
label = ttk.Label(root, text="Attendance Statistics", font=("Arial", 16))
label.pack(pady=10)

# Function to create a bar chart
def create_bar_chart():
    # Sample data
    students = ['Alice', 'Bob', 'Charlie', 'David', 'Eva']
    attendance = [90, 75, 80, 85, 95]
    
    # Create a figure and axes
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    
    # Create the bar chart
    ax.bar(students, attendance, color='skyblue')
    
    # Set labels and title
    ax.set_title('Student Attendance Rates')
    ax.set_xlabel('Students')
    ax.set_ylabel('Attendance (%)')
    
    # Embed the figure into Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    
    # Place the canvas on the Tkinter window
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Function to create a line graph
def create_line_graph():
    # Sample data
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    attendance_rate = [80, 85, 75, 90, 95]
    
    # Create a figure and axes
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    
    # Create the line graph
    ax.plot(days, attendance_rate, marker='o', linestyle='-', color='green')
    
    # Set labels and title
    ax.set_title('Attendance Trend Over the Week')
    ax.set_xlabel('Days')
    ax.set_ylabel('Attendance Rate (%)')
    
    # Embed the figure into Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    
    # Place the canvas on the Tkinter window
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create charts
create_bar_chart()
create_line_graph()

# Run the Tkinter event loop
root.mainloop()
