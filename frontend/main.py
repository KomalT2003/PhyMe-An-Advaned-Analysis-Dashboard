import dash
import dash_html_components as html


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
                html.A('Students', href='http://localhost:5000', className='p-2  border-2 rounded-md bg-gray-800 hover:text-gray-400 focus:outline-none '),
                html.A('Teachers', href='http://localhost:3000', className='p-2 -ml-2 border-2 rounded-md bg-gray-800 hover:text-gray-400 focus:outline-none')
            ])
        ]),
    
        html.Div(id='output-container', className='p-4')
    ])
    
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
