import plotly.graph_objs as go
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy import stats

def interactive_bar_plot(df, x_column, y_column1, graph_title="Default Bar Chart Title", xaxis_title=None, yaxis_title=None, y2axis_title=None, y_column2=None):
    # Sort the dataframe by the y_column1 to ensure consistent ordering
    df_sorted = df.sort_values(by=y_column1)
    traces = []

    x_values = df_sorted[x_column]
    y_values1 = df_sorted[y_column1]
    trace1 = go.Bar(
        x=x_values,
        y=y_values1,
        name=y_column1,
        marker=dict(color='rgba(138, 213, 19, 0.91)'),
        width=0.3,
        offset=-0.15
    )
    traces.append(trace1)

    if y_column2:
        y_values2 = df_sorted[y_column2]
        trace2 = go.Bar(
            x=x_values,
            y=y_values2,
            name=y2axis_title or y_column2,  # Use y2axis_title if provided, otherwise y_column2
            marker=dict(color='rgba(180,180,180, 0.8)'),
            width=0.3,
            offset=0.15
        )
        traces.append(trace2)

    # Create the Plotly figure
    fig = go.Figure(data=traces)
    
    fig.update_layout(
        title=graph_title,  # Graph title
        xaxis_title=xaxis_title or x_column,  # Use xaxis_title if provided, otherwise x_column
        yaxis_title=yaxis_title or y_column1,  # Use yaxis_title if provided, otherwise y_column1
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        barmode='group',
        yaxis=dict(
            showgrid=True,  # Enable horizontal gridlines
            gridwidth=1,    # Width of the gridline
            gridcolor='rgba(200,200,200,0.7)'  # Color of the gridline (light grey)
        ),
    )

    # Convert the figure to JSON
    graph_json = fig.to_json()

    return graph_json

def interactive_line_plot(df, x_column, y_column, graph_title="Default Line Chart Title", xaxis_title=False, yaxis_title=False, add_regression=False, trim_percent=0.05):
    
    # Sort by the x_column to ensure dates are ordered
    df_sorted = df.sort_values(by=x_column)
    
    # Extract values for the x and y axes
    x_values = np.array(range(len(df_sorted)))  # Using the index as X (since dates are categorical)
    y_values = df_sorted[y_column].values
    if len(y_values) > 0:
        average = round(np.mean(y_values), 2)
        mode_result = stats.mode(y_values)
        mode_value = str(mode_result[0])
    

    # Initialize the traces list for Plotly plots
    traces = []

    # Create a line trace for the original data
    trace = go.Scatter(
        x=df_sorted[x_column],
        y=y_values,
        mode='lines+markers',
        name=y_column,
        marker=dict(color='rgba(55,128,191, 1.0)', size=6),
        line=dict(color='rgba(55,128,191, 0.8)', width=2),
    )
    traces.append(trace)

    # Add regression line and stats if requested
    regression_info = None
    if add_regression:
        # Sort by y_column to identify and trim outliers
        sorted_indices = np.argsort(y_values)  # Get indices that sort the y_values
        num_data_points = len(y_values)
        
        # Determine the indices that correspond to the central portion of the data
        lower_bound = int(trim_percent * num_data_points)
        upper_bound = int((1 - trim_percent) * num_data_points)
        
        # Use only the central portion of the sorted data
        trimmed_indices = sorted_indices[lower_bound:upper_bound]
        trimmed_x_values = x_values[trimmed_indices]
        trimmed_y_values = y_values[trimmed_indices]

        # Ensure there's enough data left after trimming for regression
        if len(trimmed_x_values) > 5:  # We need at least 2 points for a valid regression
            # Reshape X for sklearn and create a linear regression model using trimmed data
            X_reshaped = trimmed_x_values.reshape(-1, 1)
            reg = LinearRegression().fit(X_reshaped, trimmed_y_values)
            y_pred = reg.predict(X_reshaped)

            # Create a trace for the regression line
            reg_trace = go.Scatter(
                x=df_sorted.iloc[trimmed_indices][x_column],  # Use trimmed x values (in original order)
                y=y_pred,
                mode='lines',
                name='Regression Line',
                line=dict(color='rgba(255,0,0, 0.8)', width=2, dash='dash')
            )
            traces.append(reg_trace)

            # Calculate R^2 and the equation
            r_squared = reg.score(X_reshaped, trimmed_y_values)
            slope = reg.coef_[0]
            intercept = reg.intercept_

            regression_info = {
                'equation': f"y = {slope:.2f}x + {intercept:.2f}",
                'r_squared': f"{r_squared:.2f}",
                'average': f"{average}",
                'mode': f"{mode_value}",
            }
        else:
            regression_info = {
                'equation': "Muy poca data para intentar regresion",
                'r_squared': "N/A",
                'average': "N/A",
                'mode': "N/A",
            }

    # Create the layout for the plot
    if not xaxis_title:
        xaxis_title = x_column
    if not yaxis_title:
        yaxis_title = y_column

    layout = go.Layout(
        title=graph_title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        plot_bgcolor='rgba(0,0,0,0)',
    )

    # Create the figure with the traces and layout
    fig = go.Figure(data=traces, layout=layout)

    # Convert the figure to JSON format
    graph_json = fig.to_json()

    return graph_json, regression_info

