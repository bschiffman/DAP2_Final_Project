from shiny import App, render, ui, reactive
import pandas as pd
import altair as alt
from shinywidgets import render_altair, output_widget

app_ui = ui.page_fluid(
    ui.input_select(id = "Variable", label = "Choose a variable:", choices = ["crime_deviation", "income_deviation", "le_deviation", "safe_play_deviation"]),
    output_widget("chart")
)

def server(input, output, session):
    @reactive.calc
    def data():
        return pd.read_csv("/Users/hallielovin/Documents/GitHub/DAP2_Final_Project/Data/final_df.csv")


    @reactive.calc
    def variable_group():
        df = data()  
        variable = input.Variable() 
        return df[["Name", variable, "median_income"]].dropna(subset=[variable])
    
    
    @render_altair
    def chart():
        variable_data = variable_group()  
        y_variable = input.Variable() 
        variable_data_clean = variable_data.dropna(subset=[y_variable])

        chart = alt.Chart(variable_data_clean).mark_bar().encode(
            x="Name:N",  
            y=f"{y_variable}:Q",  
            color=alt.Color("median_income:Q", scale=alt.Scale(scheme="inferno"))   
        ).properties(
            title="Deviation from Average Level"
        )
        return chart
        

app = App(app_ui, server)


