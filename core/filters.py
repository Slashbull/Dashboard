def apply_filters(data, filters):
    filtered_data = data.copy()
    for column, value in filters.items():
        if value != "All":
            if isinstance(value, list):
                filtered_data = filtered_data[filtered_data[column].isin(value)]
            else:
                filtered_data = filtered_data[filtered_data[column] == value]
    return filtered_data


def generate_filter_options(data, columns):
    options = {}
    for column in columns:
        if column in data.columns:
            options[column] = ["All"] + sorted(data[column].dropna().unique())
        else:
            options[column] = ["All"]
    return options


def get_active_filters(filters):
    return {key: value for key, value in filters.items() if value != "All"}
