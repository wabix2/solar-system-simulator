import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import webbrowser
import threading

st.set_page_config(page_title="3D Solar System", layout="wide")
st.title("🌞 3D Animated Solar System")

# Automatically open browser
def open_browser():
    webbrowser.open("http://localhost:8501")

threading.Timer(1, open_browser).start()

# Planet data: [semi-major axis, semi-minor axis, size, speed, color]
planets = {
    "Mercury": [0.4, 0.38, 80, 0.04, 'grey'],
    "Venus": [0.7, 0.69, 100, 0.03, 'orange'],
    "Earth": [1.0, 0.99, 120, 0.02, 'blue'],
    "Mars": [1.5, 1.48, 90, 0.015, 'red'],
    "Jupiter": [2.2, 2.15, 200, 0.01, 'brown'],
    "Saturn": [2.8, 2.7, 180, 0.008, 'gold'],
    "Uranus": [3.4, 3.35, 160, 0.006, 'lightblue'],
    "Neptune": [4.0, 3.95, 160, 0.005, 'darkblue']
}

# Setup figure
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor("black")
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_zlim(-1, 1)
ax.grid(False)
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])

# Draw Sun
sun = ax.scatter([0], [0], [0], s=400, color='yellow')

# Initialize planets and trails
planet_points = {}
trail_lines = {}
trail_history = {}
for planet, data in planets.items():
    x, y, z = 0, 0, 0
    planet_points[planet] = ax.scatter([x], [y], [z], s=data[2], color=data[4], label=planet)
    trail_lines[planet], = ax.plot([], [], [], color=data[4], linewidth=1, alpha=0.5)
    trail_history[planet] = [[], [], []]

# Animation update function
def update(frame):
    ax.view_init(elev=30, azim=frame*0.3)  # rotating camera
    for planet, data in planets.items():
        a, b, size, speed, color = data
        x = a * np.cos(speed * frame)
        y = b * np.sin(speed * frame)
        z = 0.05 * np.sin(speed * frame * 2)

        # Update planet position
        planet_points[planet]._offsets3d = ([x], [y], [z])

        # Update trail
        trail_history[planet][0].append(x)
        trail_history[planet][1].append(y)
        trail_history[planet][2].append(z)
        trail_lines[planet].set_data(trail_history[planet][0], trail_history[planet][1])
        trail_lines[planet].set_3d_properties(trail_history[planet][2])

        # Limit trail length for performance
        if len(trail_history[planet][0]) > 150:
            trail_history[planet][0].pop(0)
            trail_history[planet][1].pop(0)
            trail_history[planet][2].pop(0)
    return list(planet_points.values()) + list(trail_lines.values()) + [sun]

# Create animation
ani = FuncAnimation(fig, update, frames=np.arange(0, 628, 2), interval=40, blit=False)

# Display animation in Streamlit as GIF
from matplotlib.animation import PillowWriter
ani.save("solar_system.gif", writer=PillowWriter(fps=20))
st.image("solar_system.gif", use_column_width=True)
