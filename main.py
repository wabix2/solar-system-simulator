import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="3D Solar System Simulator", layout="wide")
st.title("🌞 Advanced 3D Solar System Simulator")

# ---------------------
# User controls
# ---------------------
st.sidebar.header("Simulation Controls")
speed = st.sidebar.slider("Simulation Speed", min_value=0.01, max_value=0.1, value=0.02, step=0.01)
show_trails = st.sidebar.checkbox("Show Planet Trails", value=True)
planet_size_multiplier = st.sidebar.slider("Planet Size Multiplier", min_value=0.5, max_value=3.0, value=1.0, step=0.1)

# ---------------------
# Planet data: [semi-major axis, semi-minor axis, base size, color]
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

num_frames = 300

# ---------------------
# Precompute positions
# ---------------------
planet_positions = {}
for planet, data in planets.items():
    a, b, base_size, color = data
    x = a * np.cos(speed * np.arange(num_frames) * 2*np.pi)
    y = b * np.sin(speed * np.arange(num_frames) * 2*np.pi)
    z = np.zeros(num_frames)
    planet_positions[planet] = (x, y, z, base_size, color)

# ---------------------
# Create frames
# ---------------------
frames = []
for i in range(num_frames):
    data = []
    # Sun
    sun = go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode='markers+text',
        marker=dict(size=35, color='yellow'),
        text=["Sun"], textposition="bottom center",
        name='Sun'
    )
    data.append(sun)
    
    # Planets
    for planet, (x_arr, y_arr, z_arr, base_size, color) in planet_positions.items():
        planet_data = go.Scatter3d(
            x=x_arr[:i+1] if show_trails else [x_arr[i]],
            y=y_arr[:i+1] if show_trails else [y_arr[i]],
            z=z_arr[:i+1] if show_trails else [z_arr[i]],
            mode='markers+lines+text' if show_trails else 'markers+text',
            line=dict(width=2, color=color) if show_trails else None,
            marker=dict(size=base_size*planet_size_multiplier, color=color),
            text=[planet] if i == num_frames-1 else None,
            name=planet,
            showlegend=True
        )
        data.append(planet_data)
    
    frames.append(go.Frame(data=data, name=str(i)))

# Initial frame
initial_data = frames[0].data

# ---------------------
# Layout with buttons
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
            x=0.1,
            y=0,
            buttons=[
                dict(label='Play',
                     method='animate',
                     args=[None, dict(frame=dict(duration=50, redraw=True), fromcurrent=True, mode='immediate')]),
                dict(label='Pause',
                     method='animate',
                     args=[[None], dict(frame=dict(duration=0, redraw=False), mode='immediate')])
            ]
        )]
    ),
    frames=frames
)

# ---------------------
# Display simulator
# ---------------------
st.plotly_chart(fig, use_container_width=True)
