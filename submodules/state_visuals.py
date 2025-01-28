import plotly.express as px

def generate_state_bar_chart(data):
    state_contributions = data.groupby("State", as_index=False)["Quantity"].sum()
    fig = px.bar(
        state_contributions,
        x="State",
        y="Quantity",
        title="State Contributions to Total Imports",
        labels={"State": "State", "Quantity": "Quantity (Kg)"}
    )
    st.plotly_chart(fig, use_container_width=True)

def generate_state_heatmap(data):
    state_contributions = data.groupby("State", as_index=False)["Quantity"].sum()
    fig = px.choropleth(
        state_contributions,
        locationmode="country names",
        locations="State",
        color="Quantity",
        title="State-Wise Import Heatmap",
        color_continuous_scale="Blues",
        labels={"Quantity": "Imports (Kg)"}
    )
    st.plotly_chart(fig, use_container_width=True)
