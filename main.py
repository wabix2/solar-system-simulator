import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="3D Solar System Simulator", layout="wide")
st.title("🌞 Interactive 3D Solar System Simulator")

# ---------------------
# User controls
# ---------------------
speed = st.slider("Simulation Speed", min_value=0.01, max_value=0.1, value=0.02, step=0.01)
show_trails = st.checkbox("Show Planet Trails", value=True)

# ---------------------
# Planet data: [semi-major axis, semi-minor axis, size, color]
# ---------------------
planets = {
    "Mercury": [0.4, 0.38, 8, 'grey'],
    "Venus": [0.7, 0.69, 12, 'orange'],
    "Earth": [1.0, 0.99, 14, 'blue'],
    "Mars": [1.5, 1.48, 10, 'red'],
    "Jupiter": [2.2, 2.15, 20, 'brown'],
    "Saturn": [2.8, 2.7, 18, 'gold'],
    "Uranus": [3.4, 3.35, 16, 'lightblue'],
    "Neptune": [4.0, 3.95, 16, 'darkblue']
}

# Number of frames for the animation
num_frames = 300

# ---------------------
# Precompute planet positions
# ---------------------
planet_positions = {}
for planet, data in planets.items():
    a, b, size, color = data
    x = a * np.cos(speed * np.arange(num_frames) * 2*np.pi)
    y = b * np.sin(speed * np.arange(num_frames) * 2*np.pi)
    z = np.zeros(num_frames)
    planet_positions[planet] = (x, y, z)

# ---------------------
# Create Plotly frames
# ---------------------
frames = []
for i in range(num_frames):
    data = []
    # Sun
    sun = go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode='markers',
        marker=dict(size=35, color='yellow'),
        name='Sun',
        showlegend=False
    )
    data.append(sun)
    
    # Planets
    for planet, (x_arr, y_arr, z_arr) in planet_positions.items():
        planet_data = go.Scatter3d(
            x=[x_arr[i]], y=[y_arr[i]], z=[z_arr[i]],
            mode='markers+lines' if show_trails else 'markers',
            line=dict(width=2, color=planets[planet][3]) if show_trails else None,
            marker=dict(size=planets[planet][2], color=planets[planet][3]),
            name=planet,
            showlegend=True
        )
        if show_trails:
            planet_data['x'] = x_arr[:i+1]
            planet_data['y'] = y_arr[:i+1]
            planet_data['z'] = z_arr[:i+1]
        data.append(planet_data)
    
    frames.append(go.Frame(data=data, name=str(i)))

# Initial frame
initial_data = frames[0].data

# ---------------------
# Layout with play button
# ---------------------
fig = go.Figure(
    data=initial_data,
    layout=go.Layout(
        scene=dict(
            xaxis=dict(showbackground=False),
            yaxis=dict(showbackground=False),
            zaxis=dict(showbackground=False),
            aspectmode='data'
        ),
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            buttons=[dict(label='Play',
                          method='animate',
                          args=[None, dict(frame=dict(duration=50, redraw=True), fromcurrent=True)])]
        )]
    ),
    frames=frames
)

# Display interactive 3D simulator
st.plotly_chart(fig, use_container_width=True)
