import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import StringVar, simpledialog, messagebox

# Function to calculate neutral buoyancy point
def calculate_buoyancy_point(weight, equip_weight, height, depth, p0=101325, density=1000, gravity=9.8, drag_coefficient=0.3):
    # Constants
    V0 = weight / density  # Volume of incompressible part
    P0 = p0  # Atmospheric pressure in Pascals
    g = gravity  # Acceleration due to gravity
    Cd = drag_coefficient  # Drag coefficient
    A = V0 / height  # Frontal area approximation

    # Static neutral buoyancy point calculation
    V1 = (depth + P0 / (density * g)) * equip_weight * g / P0
    f = lambda v: 0.5 * Cd * density * A * v ** 2
    p = P0 + density * g * depth
    fb = density * g * V1
    # Example velocities for plot
    velocities = np.linspace(0, 1.4, 100)  # Velocities from 0 to 2 m/s
    descent_depths = []
    ascent_depths = []

    for v in velocities:
        # Descent depth
        descent_depth = depth + (p / density / g) * f(v) / (fb * p0/ p - f(v))
        descent_depths.append(descent_depth)
        # Ascent depth
        ascent_depth = depth + (p / density / g) * (-f(v)) / (fb * p0/ p + f(v))
        ascent_depths.append(ascent_depth)

    return velocities, descent_depths, ascent_depths

# Function to clear inputs and reset plot
def clear_inputs():
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    depth_entry.delete(0, tk.END)
    density_entry.delete(0, tk.END)
    gravity_entry.delete(0, tk.END)
    drag_entry.delete(0, tk.END)
    p0_entry.delete(0, tk.END)
    equip_entry.delete(0, tk.END)

    depth_var.set("10")
    density_var.set("1000")
    gravity_var.set("9.8")
    drag_var.set("0.4")
    p0_var.set("101325")
    equip_var.set("3")

    plt.close('all')
    
# Function to get user input and plot results
def plot_results():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        depth = float(depth_entry.get() or 10)
        density = float(density_entry.get() or 1000)
        gravity = float(gravity_entry.get() or 9.8)
        drag_coefficient = float(drag_entry.get() or 0.4)
        p0 = float(p0_entry.get() or 101325)
        equip_weight = float(equip_entry.get() or 3)
    except (ValueError, TypeError):
        messagebox.showerror("Error", "Invalid input. Please enter all numerical values correctly.")
        return

    # Calculate buoyancy points
    velocities, descent_depths, ascent_depths = calculate_buoyancy_point(weight, equip_weight, height, depth, p0, density, gravity, drag_coefficient)

    # Plot the results
    plt.figure()
    plt.plot(velocities, descent_depths, label='Descent Depth')
    plt.plot(velocities, ascent_depths, label='Ascent Depth')
    plt.xlabel('Velocity (m/s)')
    plt.ylabel('Depth (m)')
    plt.title('Neutral Buoyancy Point vs. Velocity')
    plt.legend()
    plt.grid(True)
    plt.show()

# Create main application window
root = tk.Tk()
root.title("Neutral Buoyancy Calculator")

# Labels and entries for user input
tk.Label(root, text="Weight (kg):").grid(row=0, column=0, sticky=tk.W)
weight_entry = tk.Entry(root)
weight_entry.grid(row=0, column=1)

tk.Label(root, text="Height (m):").grid(row=1, column=0, sticky=tk.W)
height_entry = tk.Entry(root)
height_entry.grid(row=1, column=1)

# Default values
depth_var = StringVar(value="10")
density_var = StringVar(value="1000")
gravity_var = StringVar(value="9.8")
drag_var = StringVar(value="0.4")
p0_var = StringVar(value="101325")
equip_var = StringVar(value="3")

tk.Label(root, text="Neutral Buoyancy Depth (m):").grid(row=2, column=0, sticky=tk.W)
depth_entry = tk.Entry(root, textvariable=depth_var)
depth_entry.grid(row=2, column=1)

tk.Label(root, text="Equipment Weight (kg):").grid(row=2, column=0, sticky=tk.W)
equip_entry = tk.Entry(root, textvariable=equip_var)
equip_entry.grid(row=2, column=1)

tk.Label(root, text="Density (kg/m³):").grid(row=3, column=0, sticky=tk.W)
density_entry = tk.Entry(root, textvariable=density_var)
density_entry.grid(row=3, column=1)

tk.Label(root, text="Gravity (m/s²):").grid(row=4, column=0, sticky=tk.W)
gravity_entry = tk.Entry(root, textvariable=gravity_var)
gravity_entry.grid(row=4, column=1)

tk.Label(root, text="Drag Coefficient:").grid(row=5, column=0, sticky=tk.W)
drag_entry = tk.Entry(root, textvariable=drag_var)
drag_entry.grid(row=5, column=1)

tk.Label(root, text="Atmospheric Pressure (Pa):").grid(row=6, column=0, sticky=tk.W)
p0_entry = tk.Entry(root, textvariable=p0_var)
p0_entry.grid(row=6, column=1)

# Buttons to plot results and clear inputs
plot_button = tk.Button(root, text="Plot Results", command=plot_results)
plot_button.grid(row=7, column=0, pady=10)

clear_button = tk.Button(root, text="Clear", command=clear_inputs)
clear_button.grid(row=7, column=1, pady=10)

# Warning message
tk.Label(root, text="The curve is theoretical analysis for your reference,\nplease adjust the depth based on your own experience and preference.", fg="red").grid(row=8, column=0, columnspan=2)


# Run the application
root.mainloop()
