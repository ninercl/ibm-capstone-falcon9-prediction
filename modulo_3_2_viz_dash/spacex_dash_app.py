# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites = spacex_df['Launch Site'].unique().tolist() #listado launch site
dropdown_options = [{'label': 'All Sites', 'value': 'All'}] #Opciones dropdown
dropdown_options += [{'label': site, 'value': site} for site in launch_sites]
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                dcc.Dropdown(id="site-dropdown",
                                options = dropdown_options,
                                value='All',
                                placeholder='Select a Launch Site',
                                searchable=True
                            ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                marks={0 : "0",
                                       1000: "1000",
                                       2000: "2500",
                                       5000: "5000",
                                       7500 : "7500",
                                       10000 : "10000"

                                },
                                value=[min_payload, max_payload]
                                ),
                       

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value")
            )        
            
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == "All":
        fig = px.pie(spacex_df,
                     names="Launch Site",
                     values="class",
                     title="Total Successful Launches by Site"
        )
        return fig 
    else:
        #Pie chart por sitio
        filtered_df = spacex_df[spacex_df["Launch Site"] == entered_site]
        success_counts = filtered_df["class"].value_counts().reset_index()
        success_counts.columns = ["Outcome", "Count"]
        success_counts["Outcome"] = success_counts["Outcome"].replace({1: "Success", 0: "Failure"})

        fig = px.pie(success_counts,
                     names="Outcome",
                     values="Count",
                     title=f"Success vs Failure for site: {entered_site}"
                     )
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def get_scatter(entered_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df["Payload Mass (kg)"] >= low) &
                            (spacex_df["Payload Mass (kg)"] <= high)]


    if entered_site == "All":
        fig = px.scatter(
        spacex_df, x="Payload Mass (kg)", 
        y ="class",
        color ="Booster Version Category",
        title = f"Correlation between Payload and Success landing for ALL sites"
    )
    else: 
        site_df = filtered_df[filtered_df["Launch Site"] == entered_site]
        fig = px.scatter(
            site_df,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title=f"Correlation between Payload and Succes for site: {entered_site}"
        )
    return fig

# Run the app
if __name__ == '__main__':
    app.run()
