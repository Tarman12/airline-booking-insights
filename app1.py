
import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime, timedelta

# Title
st.title("✈️ Airline Booking Market Demand Dashboard (Mock Data)")
st.markdown("Simulated insights on airline demand trends and pricing")

# Generate Mock Data
@st.cache_data
def generate_mock_data(n=200):
    airlines = ['Qantas', 'Jetstar', 'Virgin Australia', 'Rex Airlines']
    cities = ['SYD', 'MEL', 'BNE', 'ADL', 'PER']
    statuses = ['scheduled', 'delayed', 'cancelled']
    
    data = []
    for _ in range(n):
        dep, arr = random.sample(cities, 2)
        record = {
            'Airline': random.choice(airlines),
            'Flight Number': f"{random.randint(100,999)}",
            'Departure': dep,
            'Arrival': arr,
            'Price ($AUD)': round(random.uniform(100, 500), 2),
            'Status': random.choices(statuses, weights=[0.7, 0.2, 0.1])[0],
            'Date': (datetime.today() + timedelta(days=random.randint(0, 30))).date()
        }
        data.append(record)
    return pd.DataFrame(data)

# Load Data
df = generate_mock_data()

# Sidebar Filters
st.sidebar.header("📍 Filter Flights")
selected_airline = st.sidebar.multiselect("Airline", df["Airline"].unique())
selected_route = st.sidebar.multiselect("Route", df["Departure"] + " ➝ " + df["Arrival"])
selected_status = st.sidebar.multiselect("Status", df["Status"].unique())

# Apply Filters
if selected_airline:
    df = df[df["Airline"].isin(selected_airline)]
if selected_route:
    routes = [r.split(" ➝ ") for r in selected_route]
    df = df[df.apply(lambda x: any(x["Departure"] == d and x["Arrival"] == a for d, a in routes), axis=1)]
if selected_status:
    df = df[df["Status"].isin(selected_status)]

# Show Data
st.subheader("📊 Flight Records")
st.dataframe(df)

# Visualizations
if not df.empty:
    st.subheader("✈️ Top Routes by Frequency")
    route_counts = df.groupby(['Departure', 'Arrival']).size().reset_index(name='Count')
    route_counts["Route"] = route_counts["Departure"] + " ➝ " + route_counts["Arrival"]
    fig1 = px.bar(route_counts.sort_values("Count", ascending=False).head(10),
                  x="Route", y="Count", title="Most Frequent Routes")
    st.plotly_chart(fig1)

    st.subheader("💰 Price Trends by Airline")
    fig2 = px.box(df, x="Airline", y="Price ($AUD)", color="Airline")
    st.plotly_chart(fig2)

    st.subheader("📈 Demand Over Time")
    date_counts = df.groupby("Date").size().reset_index(name="Bookings")
    fig3 = px.line(date_counts, x="Date", y="Bookings", title="Booking Demand Over Time")
    st.plotly_chart(fig3)

    st.subheader("🚦 Status Distribution")
    fig4 = px.pie(df, names="Status", title="Flight Status Breakdown")
    st.plotly_chart(fig4)
else:
    st.warning("No results with selected filters.")
