def calculate_kpis(data):
    if data.empty:
        return 0, 0, 0, 0

    total_imports = data["Quantity"].sum()
    unique_states = data["State"].nunique()

    year_groups = data.groupby("Year")["Quantity"].sum()
    yoy_growth = (
        ((year_groups.iloc[-1] - year_groups.iloc[-2]) / year_groups.iloc[-2] * 100)
        if len(year_groups) > 1 else 0
    )

    month_groups = data.groupby("Month")["Quantity"].sum()
    mom_growth = (
        ((month_groups.iloc[-1] - month_groups.iloc[-2]) / month_groups.iloc[-2] * 100)
        if len(month_groups) > 1 else 0
    )

    return total_imports, unique_states, yoy_growth, mom_growth
