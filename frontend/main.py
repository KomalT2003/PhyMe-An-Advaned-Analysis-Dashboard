import dash
import dash_html_components as html
from dash.dependencies import Input, Output
from students import students_layout,callbacks
from teachers import teachers_layout,callbacks

# Initialize the Dash app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# Define the layout of the app
app.layout = html.Div([
    
    # use the tailwind css cdn
    html.Link(
        rel='stylesheet',
        href='https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css'
    ),
    #create a navbar
    html.Div(className="bg-gray-900 text-yellow-300 min-h-screen bg-cover ", children=[
        html.Nav(className="flex justify-between items-center border-b border-gray-800 p-4", children=[
            html.H1('PhyMe', className='ml-5 text-5xl font-bold'),
            html.Div(className="flex gap-5 mr-5", children=[
                html.Button('Students', id='students', n_clicks=0, className='p-2  border-2 rounded-md bg-gray-800 hover:text-gray-400 focus:outline-none '),
                html.Button('Teachers', id='teachers', n_clicks=0, className='p-2 -ml-2 border-2 rounded-md bg-gray-800 hover:text-gray-400 focus:outline-none')
            ])
        ]),
    
        html.Div(id='output-container', className='p-4')
    ])
    
])

# Define the callback to switch themes
@app.callback(
    Output('output-container', 'children'),
    [Input('students', 'n_clicks'),
     Input('teachers', 'n_clicks')]
)
def update_output(dark_clicks, yellow_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'students' in changed_id:
        return students_layout
    elif 'teachers' in changed_id:
        return "techers"
        

callbacks(app)
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
