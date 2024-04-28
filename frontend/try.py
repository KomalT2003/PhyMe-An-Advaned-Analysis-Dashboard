import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd

# Sample data
questions_ise1=pd.DataFrame({
    "questions":["question1","question2","question3"],
    "marks":[3,4,5],
    "category":["theory","numerical","numerical"],
    "topic":["topic1","topic2","topic3"],
    "maxScore":[3,5,5],
    "A_Scores":[[2.1,3.2,1.8,0,0.4,1.8,0.5,1.3,1.5,2.6],[3,4,5,4,2,3,5,2,4,5],[2,3,4,5,2.4,3,5,2,4,5]],
    "B_Scores":[[1,2.3,3,2.4,2.5,2,3,2.4,1.6,0.6],[3,4,5,2,2,3,5,2,4,5],[2,3,4,5,3,3,5,2,4,5]],
    "C_Scores":[[1.8,2.1,2.5,2.6,2.5,1.2,2,2,1.2,3],[3,4,5,1,2,3,5,2,4,5],[2,3,4,5,2.4,3,5,2,4,5]],
    "avgAScore":[2.4,3.45,3.122],
    "avgBScore":[2.21,3.35,3.512],
    "avgCScore":[2.45,3.13,4.10],
    "avgOverallScore":[2.4,3.45,3.122],
})

# Calculate overall average score for each question
questions_ise1["Overall_Avg"] = questions_ise1.apply(lambda row: sum(row["A_Scores"] + row["B_Scores"] + row["C_Scores"]) / (3 * len(row["A_Scores"])), axis=1)

# Define color gradients for divisions
color_gradients = {
    "A": "rgb(255, 0, 0)",  # Red
    "B": "rgb(0, 255, 0)",  # Green
    "C": "rgb(0, 0, 255)"   # Blue
}

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Question-wise Performance Analysis"),
    
    # Dropdown for selecting question
    html.Label("Select Question:"),
    dcc.Dropdown(
        id="question-dropdown",
        options=[{'label': q, 'value': q} for q in questions_ise1["questions"]],
        value=questions_ise1["questions"][0]
    ),
    
    # Scatter Plot of Scores for Each Question
    dcc.Graph(id='scores-scatter-plot',),
])

# Define callback to update the plot based on dropdown selection
@app.callback(
    dash.dependencies.Output('scores-scatter-plot', 'figure'),
    [dash.dependencies.Input('question-dropdown', 'value')]
)
def update_scores_plot(selected_question):
    # Filter data for the selected question
    selected_question_data = questions_ise1[questions_ise1["questions"] == selected_question]
    
    # Prepare data for plotting
    all_scores = selected_question_data["A_Scores"].explode().tolist() + \
                 selected_question_data["B_Scores"].explode().tolist() + \
                 selected_question_data["C_Scores"].explode().tolist()
    divisions = ["A"] * len(selected_question_data["A_Scores"].explode()) + \
                ["B"] * len(selected_question_data["B_Scores"].explode()) + \
                ["C"] * len(selected_question_data["C_Scores"].explode())
    
    # Create scatter plot
    fig = go.Figure()
    
    # Add trace for student marks with color gradients
    for division in ["A", "B", "C"]:
        division_scores = selected_question_data[f"{division}_Scores"].explode().tolist()
        fig.add_trace(go.Scatter(
            x=[division]*len(division_scores),
            y=division_scores,
            mode='markers',
            name=f'{division} Scores',
            marker=dict(symbol='circle', size=10, color=color_gradients[division]),
        ))
    
    # Add line for overall average
    fig.add_trace(go.Scatter(
        x=["A", "B", "C"],
        y=[selected_question_data["avgAScore"].iloc[0], selected_question_data["avgBScore"].iloc[0], selected_question_data["avgCScore"].iloc[0]],
        mode='lines',
        name='Overall Avg',
        line=dict(color='black', dash='dash')
    ))
    
    # Update layout
    fig.update_layout(
        title=f"Performance on {selected_question}",
        xaxis_title="Division",
        yaxis_title="Score",
        showlegend=True,
    )
    
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
