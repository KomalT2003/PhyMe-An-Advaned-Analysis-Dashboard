import dash
import pandas as pd
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

server = app.server

app.layout = html.Div([
    html.Link(
        rel='stylesheet',
        href='https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css'
    ),
    html.Div(className="bg-gray-900 text-yellow-300 min-h-screen bg-cover min-h-screen", children=[
        html.Nav(className="flex justify-between items-center border-b border-gray-800 p-4", children=[
            html.H1('PhyMe', className='ml-5 text-5xl font-bold'),
            html.Div(className="flex gap-5 mr-5", children=[
                html.A('Students', href='https://phyme-an-advaned-analysis-dashboard.onrender.com/', className='p-2  border-2 rounded-md bg-gray-800 hover:text-gray-400 focus:outline-none '),
                html.A('Teachers', href='https://phyme-an-advaned-analysis-dashboard-08q6.onrender.com/', className='p-2 -ml-2 border-2 rounded-md bg-gray-800 hover:text-gray-400 focus:outline-none')
            ])
        ]),
        html.Div(className="bg-gray-900 text-yellow-300 bg-cover flex-col ", children=[
            html.Div(className="flex gap-4 justify-center bg-gray-800 text-white items-center p-4 rounded-md", children=[
                html.Button("Performance", id="performance-button", n_clicks=0, className="bg-gray-900 rounded-md w-60 py-2 px-2 mb-2 hover:bg-gray-600 hover:text-yellow-400 focus:outline-none"),
                html.Button("Module 1", id="module1-button", n_clicks=0, className="bg-gray-900 rounded-md w-60 py-2 px-2 mb-2 hover:bg-gray-600 hover:text-yellow-400 focus:outline-none"),
                html.Button("Module 2", id="module2-button", n_clicks=0, className="bg-gray-900 rounded-md w-60 py-2 px-4 mb-2 hover:bg-gray-600 hover:text-yellow-400 focus:outline-none"),
                html.Button("Module 3", id="module3-button", n_clicks=0, className="bg-gray-900 rounded-md w-60 py-2 px-4 mb-2 hover:bg-gray-600 hover:text-yellow-400 focus:outline-none"),
                html.Button("Module 4", id="module4-button", n_clicks=0, className="bg-gray-900 rounded-md w-60 py-2 px-4 mb-2 hover:bg-gray-600 hover:text-yellow-400 focus:outline-none"),
            ], id='sidebar'),
            html.Div(className="flex flex-col justify-center align-center ", children=[
                html.Div(className='flex justify-center align-center ml-42 h-24 bg-gray-900 text-blue-300 p-4 rounded-md ml-5', children=[ 
                    html.Button("COMPSA", id="compsa-button", className="border-2 w-72 mx-2 py-2 px-4 bg-gray-800 hover:bg-gray-600 rounded-md hover:text-yellow-400 focus:outline-none"),
                    html.Button("COMPSB", id="compsb-button", className="border-2 w-72 mx-2 py-2 px-4 bg-gray-800 hover:bg-gray-600 rounded-md hover:text-yellow-400 focus:outline-none"),
                    html.Button("AIML", id="aiml-button", className="border-2 w-72 mx-2 py-2 px-4 bg-gray-800 hover:bg-gray-600 rounded-md hover:text-yellow-400 focus:outline-none"),
                ], id='main-screen'),
                html.Div(className=' mr-30 flex bg-gray-900 text-blue-300 p-4 rounded-md ml-5', children=[
                    html.Div(id='main-container'),
                ]), 
                dcc.Store(id='division-store', data='COMPSA'),
                dcc.Store(id='module-store', data='1')
            ])
        ])
    ])
])


#DATA

topics_mse_1={
    "Topic":["wave packet, group velocity and phase velocity","Heisenberg’s uncertainty principle","De-broglie wavelength and its application"," Potential barrier (Tunnelling)","Infinite Potential Well(Particle Trapped in 1d box) & Schrondinger Wave Eq",		
],
    "Marks":[2,4,2,6,6],
    "COMPSA_Scores":[[2.0, 1.5, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 0.0, 2.0, 2.0, 2.0, 1.0, 1.5, 0.5, 0.0, 1.5, 2.0, 2.0, 0.5, 2.0, 2.0, 2.0, 2.0, 1.0, 0.5, 2.0, 2.0, 1.0, 2.0, 2.0, 0.5, 2.0, 2.0, 1.5, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 0.5, 2.0, 0.0, 2.0, 2.0, 2.0],
            [4.0, 2.0, 2.5, 1.0, 3.0, 4.0, 3.0, 3.0, 3.0, 4.0, 3.5, 3.0, 4.0, 3.0, 3.0, 4.0, 3.0, 3.0, 3.0, 2.5, 3.5, 0.0, 3.0, 3.5, 3.0, 2.0, 2.5, 0.5, 0.0, 1.5, 2.0, 2.0, 0.5, 3.0, 3.0, 2.0, 4.0, 2.5, 0.5, 2.0, 2.0, 1.5, 4.0, 3.0, 1.5, 4.0, 4.0, 3.5, 4.0, 4.0, 3.0, 4.0, 4.0, 3.0, 2.0, 4.0, 4.0, 3.0, 3.0, 3.0, 4.0, 3.5, 3.5, 0.5, 2.5, 0.0, 4.0, 2.5, 4.0],
            [2.0, 0.0, 2.0, 0.0, 2.0, 1.0, 2.0, 1.0, 2.0, 1.0, 2.0, 2.0, 2.0, 1.5, 2.0, 2.0, 2.0, 2.0, 1.5, 2.0, 1.0, 0.0, 2.0, 2.0, 2.0, 0.0, 1.0, 0.0, 0.0, 1.0, 2.0, 2.0, 0.0, 0.0, 1.0, 2.0, 2.0, 1.5, 0.0, 0.0, 2.0, 0.5, 2.0, 0.0, 2.0, 1.0, 0.0, 2.0, 2.0, 1.0, 2.0, 2.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.5, 1.0, 2.0, 2.0, 1.0, 0.5, 2.0, 1.5, 0.0, 2.0, 1.5, 2.0],
            [5.5, 5.5, 3.5, 2.5, 3.5, 3.0, 5.5, 1.5, 6.0, 3.0, 4.0, 3.0, 3.5, 3.0, 1.5, 4.0, 3.0, 6.0, 6.0, 0.5, 6.0, 0.5, 6.0, 4.0, 6.0, 6.0, 3.0, 1.0, 0.5, 1.0, 2.0, 3.0, 0.0, 5.5, 2.5, 4.0, 6.0, 2.5, 0.0, 1.0, 2.0, 1.5, 0.0, 5.0, 1.0, 1.5, 4.5, 5.5, 6.0, 6.0, 5.5, 4.0, 3.0, 6.0, 5.5, 6.0, 6.0, 3.5, 3.5, 6.0, 3.0, 5.0, 4.5, 1.0, 4.5, 0.0, 6.0, 1.0, 6.0],
            [6.0, 1.0, 2.5, 0.0, 2.0, 3.0, 2.0, 1.5, 4.5, 2.5, 2.0, 3.0, 2.0, 2.0, 1.0, 6.0, 5.0, 3.0, 5.0, 4.0, 5.5, 1.0, 4.5, 5.5, 3.0, 3.5, 2.5, 0.0, 0.0, 1.0, 0.5, 0.0, 0.0, 1.5, 1.5, 2.0, 6.0, 2.5, 0.0, 1.0, 4.0, 1.5, 3.0, 5.0, 1.0, 4.0, 3.5, 6.0, 6.0, 6.0, 2.5, 5.5, 3.0, 5.0, 0.0, 6.0, 3.5, 4.0, 2.5, 4.5, 6.0, 5.0, 5.5, 1.5, 1.5, 0.0, 6.0, 2.5, 6.0]],


"COMPSB_Scores":[[0.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.5, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.5, 0.5, 2.0, 2.0, 1.0, 1.5, 2.0, 1.0, 2.0, 2.0, 0.5, 2.0, 2.0, 2.0, 2.0, 2.0, 0.5, 0.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.5, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 2.0, 2.0, 2.0, 0.5, 2.0, 2.0, 2.0, 1.5, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 2.0],
                 [0.5, 4.0, 3.0, 3.0, 3.0, 3.0, 2.5, 3.0, 2.0, 4.0, 4.0, 3.0, 4.0, 3.0, 3.0, 3.5, 1.0, 3.0, 3.0, 2.0, 2.5, 4.0, 1.0, 4.0, 4.0, 1.0, 3.5, 4.0, 4.0, 4.0, 3.0, 0.5, 0.0, 3.0, 3.0, 3.5, 2.0, 3.0, 4.0, 4.0, 4.0, 2.5, 2.0, 3.0, 3.5, 2.0, 2.5, 3.5, 4.0, 2.0, 3.5, 1.0, 3.0, 3.0, 2.0, 0.5, 3.0, 3.0, 3.0, 2.5, 4.0, 4.0, 2.0, 2.0, 3.5, 4.0, 4.0, 1.0, 4.0],
                 [0.5, 1.0, 2.0, 2.0, 1.5, 2.0, 1.0, 0.5, 1.0, 2.0, 2.0, 1.5, 1.0, 1.0, 2.0, 2.0, 1.0, 2.0, 1.0, 1.0, 1.5, 2.0, 0.0, 2.0, 2.0, 1.0, 1.5, 1.0, 2.0, 2.0, 1.0, 0.0, 0.0, 2.0, 2.0, 2.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 0.5, 1.0, 1.5, 1.5, 1.0, 2.0, 2.0, 2.0, 2.0, 0.5, 1.5, 2.0, 1.0, 0.0, 1.5, 2.0, 1.5, 2.0, 1.5, 2.0, 1.0, 1.0, 2.0, 2.0, 2.0, 0.0, 2.0],
                 [0.5, 2.0, 6.0, 0.5, 6.0, 4.0, 2.0, 3.0, 1.0, 6.0, 5.5, 5.5, 6.0, 5.5, 3.5, 4.5, 2.5, 1.0, 5.0, 3.0, 3.5, 3.0, 0.5, 6.0, 5.0, 4.0, 3.5, 2.0, 5.5, 6.0, 1.0, 0.0, 0.0, 5.5, 6.0, 4.0, 0.0, 4.5, 3.5, 6.0, 5.5, 5.5, 5.5, 3.5, 3.0, 4.0, 1.0, 2.5, 3.0, 5.5, 6.0, 2.0, 6.0, 2.0, 5.0, 1.0, 5.0, 6.0, 6.0, 5.5, 6.0, 5.0, 4.0, 4.5, 2.5, 6.0, 6.0, 3.0, 6.0],
                 [0.5, 2.5, 1.0, 2.0, 5.0, 3.0, 2.0, 2.0, 0.5, 6.0, 4.0, 4.5, 6.0, 4.5, 2.5, 6.0, 4.5, 4.0, 4.0, 2.0, 2.0, 6.0, 0.0, 4.5, 6.0, 0.5, 4.5, 2.5, 6.0, 5.0, 2.0, 0.0, 0.0, 1.5, 2.0, 5.5, 0.0, 2.0, 6.0, 4.0, 5.5, 4.0, 1.5, 2.0, 5.0, 0.5, 1.0, 3.5, 2.5, 0.0, 5.5, 0.0, 3.0, 1.0, 1.5, 0.0, 4.5, 5.0, 5.0, 1.5, 6.0, 5.0, 1.0, 3.0, 5.0, 4.0, 6.0, 0.0, 6.0]],

"AIML_Scores":[[2.0, 2.0, 2.0, 2.0, 0.5, 1.5, 1.5, 2.0, 0.5, 1.5, 2.0, 2.0, 2.0, 2.0, 0.0, 1.0, 2.0, 1.0, 2.0, 2.0, 2.0, 1.5, 0.5, 1.5, 0.5, 1.0, 1.5, 1.5, 1.5, 1.5, 2.0, 1.0, 1.5, 2.0, 1.0, 1.0, 1.5, 1.5, 2.0, 2.0, 1.0, 2.0, 0.0, 2.0, 2.0, 1.5, 2.0, 0.0, 2.0, 2.0, 0.0, 1.5, 1.5, 2.0, 1.5, 1.0, 1.0, 2.0, 2.0, 1.0, 2.0, 1.5, 1.0, 2.0, 0.5, 0.0, 0.0],
               [3.0, 3.0, 3.0, 4.0, 1.5, 2.5, 2.5, 3.0, 1.5, 2.0, 4.0, 3.0, 4.0, 4.0, 0.0, 1.5, 2.0, 2.5, 3.0, 3.0, 2.5, 2.5, 1.0, 3.0, 1.5, 3.0, 2.5, 3.5, 3.0, 3.5, 3.0, 2.5, 2.5, 3.0, 2.0, 3.0, 3.5, 2.5, 3.0, 3.0, 3.0, 3.0, 1.0, 4.0, 3.5, 3.0, 3.0, 1.0, 3.0, 3.0, 1.0, 3.5, 3.5, 4.0, 2.5, 2.0, 2.0, 3.5, 2.5, 2.0, 2.5, 2.0, 2.5, 3.5, 1.5, 0.0, 1.0],
               [2.0, 2.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 1.5, 1.5, 2.0, 0.5, 2.0, 2.0, 0.5, 2.0, 2.0, 2.0, 1.0, 2.0, 0.0, 1.0, 1.0, 2.0, 1.5, 2.0, 2.0, 2.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 0.0, 2.0, 2.0, 1.5, 2.0, 2.0, 2.0, 2.0, 1.0, 1.5, 2.0, 1.0, 2.0, 1.0, 2.0, 1.5, 0.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.5, 1.0, 1.0, 2.0, 1.5, 2.0, 0.0, 1.0],
               [5.5, 5.5, 5.5, 4.0, 5.5, 5.5, 3.0, 1.0, 3.5, 3.0, 0.5, 1.0, 3.5, 2.0, 0.0, 4.5, 1.5, 4.5, 5.5, 0.0, 0.5, 3.0, 3.0, 2.5, 5.0, 3.0, 3.0, 4.0, 2.0, 1.5, 2.0, 6.0, 6.0, 5.5, 3.0, 5.5, 2.0, 0.5, 3.0, 3.0, 5.5, 1.0, 1.5, 5.5, 1.5, 1.5, 1.0, 0.0, 3.0, 3.5, 3.0, 5.5, 6.0, 6.0, 3.5, 3.0, 3.5, 3.0, 0.0, 4.0, 3.0, 0.0, 5.5, 3.5, 5.0, 1.0, 1.0],
               [1.0, 5.0, 1.0, 4.0, 5.0, 3.5, 3.0, 5.0, 1.0, 2.0, 3.0, 2.0, 6.0, 3.5, 0.0, 1.5, 3.0, 3.0, 1.0, 1.0, 0.5, 1.0, 4.0, 1.5, 2.0, 3.0, 2.0, 2.0, 1.5, 2.0, 5.0, 1.5, 2.0, 4.5, 1.0, 3.5, 6.0, 2.0, 3.0, 1.0, 3.0, 1.0, 1.0, 6.0, 2.5, 1.5, 2.5, 3.0, 5.0, 2.0, 2.0, 5.5, 5.0, 3.5, 2.0, 1.0, 2.0, 2.5, 2.5, 1.0, 2.5, 0.5, 4.0, 4.5, 3.0, 0.5, 1.0]],
    "avgCOMPSAScore":[1.7,2.77,1.29,3.58,(2.77,3.04),3.04,3.58],
   "avgCOMPSBScore":[1.76,2.86,1.4,3.89,2.86,3.11,3.11,3.89],
   "avgAIMLScore":[1.41,2.59,1.59,3.12,2.59,2.59,2.59,3.12],   
   "avgOverallScore":[1.855,1.823,1.685]
}


topics_mse_4={
   "topic":["Interference of light in thin films having uniform thickness","Applications of interference in anti-reflecting and highly reflecting thin films"],
    "Marks":[2,2],
   "COMPSA_Scores":[[1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.5, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 2.0, 0.0, 2.0, 1.0, 0.0, 2.0, 0.5, 2.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 1.0],[0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],

   "COMPSB_Scores":[[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 2.0, 2.0, 0.0, 0.5, 1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 1.0, 0.0, 2.0, 1.0, 0.0, 0.0, 1.0, 1.0, 2.0, 1.0, 2.0, 2.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 2.0],[0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.5, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 1.5, 0.0, 0.0, 0.0]],

   "AIML_Scores":[[1.0, 1.0, 0.5, 0.0, 0.5, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 1.0, 0.0, 0.0, 2.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 1.5, 0.0, 1.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.5, 0.0, 0.0, 1.5, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 1.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0]],
  
 "avgCOMPSAScore":[0.46,0.15],
   "avgCOMPSBScore":[0.52,0.26],
   "avgAIMLScore":[0.266,0.23],   
   "avgOverallScore":[0.415,0.2133],
}

topics_mse_2={
    "No. of Questions asked: ":0,
}

topics_mse_3={
    "No. of Questions asked: ":0,
}


topics_ese_1={
 "Topic":["Schrodinger's time dependent wave equation, time independent wave equation ","wave packet, group velocity and phase velocity","Application of time-independent Schrodinger equation - Particle trapped in one dimensional box and Potential barrier (Tunnelling), Harmonic oscillator (qualitative)",",Electron diffraction experiment"], 
 "Marks":[5,5,25,5], # topic weightage (total marks)    
 "COMPSA_Scores":[
     [5.0, 3.0, 3.0, 2.0, 2.0, 4.0, 5.0, 3.0, 5.0, 5.0, 5.0, 5.0, 3.0, 3.0, 2.0, 5.0, 4.0, 4.0, 4.0, 4.0, 4.0, 2.0, 5.0, 5.0, 5.0, 2.0, 4.0, 2.0, 1.0, 2.0, 4.0, 4.0, 1.0, 4.0, 4.0, 4.0, 5.0, 2.0, 1.0, 2.0, 5.0, 4.0, 5.0, 5.0, 2.0, 5.0, 4.0, 5.0, 5.0, 5.0, 4.0, 5.0, 4.0, 4.0, 5.0, 4.0, 5.0, 4.0, 4.0, 5.0, 4.0, 4.0, 5.0, 4.0, 3.0, 0.0, 5.0, 5.0, 5.0, 3.0],
     [5.0, 3.0, 2.0, 2.0, 2.0, 4.0, 5.0, 3.0, 4.0, 5.0, 4.0, 4.0, 3.0, 2.0, 2.0, 4.0, 5.0, 4.0, 4.0, 4.0, 4.0, 2.0, 4.0, 5.0, 5.0, 2.0, 4.0, 2.0, 1.0, 2.0, 3.0, 4.0, 1.0, 3.0, 4.0, 4.0, 5.0, 2.0, 1.0, 2.0, 5.0, 3.0, 4.0, 5.0, 2.0, 4.0, 4.0, 5.0, 5.0, 5.0, 4.0, 5.0, 4.0, 4.0, 5.0, 4.0, 5.0, 4.0, 4.0, 5.0, 4.0, 4.0, 5.0, 4.0, 3.0, 0.0, 5.0, 4.0, 5.0, 3.0],
     [23.0, 8.0, 20.0, 2.0, 18.0, 6.0, 20.0, 6.0, 21.0, 9.0, 12.0, 16.0, 10.0, 6.0, 2.0, 22.0, 17.0, 16.0, 22.0, 18.0, 20.0, 0.0, 22.0, 20.0, 20.0, 5.0, 15.0, 0.0, 0.0, 11.0, 4.0, 16.0, 0.0, 18.0, 7.0, 13.0, 24.0, 8.0, 10.0, 6.0, 23.0, 2.0, 1.0, 20.0, 4.0, 20.0, 20.0, 25.0, 24.0, 25.0, 19.0, 24.0, 19.0, 15.0, 15.0, 17.0, 19.0, 7.0, 25.0, 23.0, 21.0, 20.0, 20.0, 16.0, 14.0, 0.0, 20.0, 18.0, 25.0, 4.0],
     [2.0, 2.0, 1.0, 0.0, 3.0, 1.0, 2.0, 1.0, 3.0, 3.0, 1.0, 2.0, 2.0, 1.0, 1.0, 2.0, 2.0, 2.0, 4.0, 1.0, 2.0, 0.0, 4.0, 4.0, 2.0, 1.0, 3.0, 0.0, 0.0, 1.0, 1.0, 2.0, 0.0, 2.0, 1.0, 2.0, 4.0, 2.0, 0.0, 2.0, 4.0, 0.0, 1.0, 2.0, 1.0, 2.0, 3.0, 4.0, 5.0, 5.0, 2.0, 5.0, 5.0, 2.0, 1.0, 3.0, 4.0, 1.0, 4.0, 4.0, 4.0, 3.0, 3.0, 2.0, 2.0, 0.0, 2.0, 2.0, 4.0, 0.0]],

"COMPSB_Scores":[[5.0, 4.0, 3.0, 2.0, 5.0, 4.0, 4.0, 3.0, 5.0, 5.0, 4.0, 3.0, 2.0, 4.0, 4.0, 2.0, 5.0, 5.0, 3.0, 4.0, 4.0, 1.0, 5.0, 5.0, 3.0, 3.0, 4.0, 5.0, 4.0, 4.0, 0.0, 1.0, 4.0, 4.0, 5.0, 3.0, 4.0, 4.0, 5.0, 4.0, 4.0, 4.0, 4.0, 4.0, 3.0, 4.0, 4.0, 4.0, 4.0, 4.0, 2.0, 5.0, 1.0, 4.0, 1.0, 5.0, 4.0, 4.0, 4.0, 5.0, 5.0, 2.0, 4.0, 4.0, 4.0, 5.0, 2.0, 5.0, 4.0, 5.0],
[5.0, 4.0, 3.0, 2.0, 4.0, 4.0, 4.0, 3.0, 5.0, 5.0, 4.0, 2.0, 2.0, 4.0, 4.0, 2.0, 5.0, 4.0, 3.0, 4.0, 4.0, 1.0, 5.0, 5.0, 3.0, 2.0, 4.0, 5.0, 4.0, 4.0, 0.0, 1.0, 4.0, 4.0, 5.0, 3.0, 4.0, 4.0, 5.0, 4.0, 4.0, 4.0, 4.0, 4.0, 3.0, 4.0, 4.0, 4.0, 4.0, 4.0, 2.0, 5.0, 1.0, 3.0, 1.0, 5.0, 4.0, 4.0, 4.0, 5.0, 5.0, 2.0, 4.0, 4.0, 4.0, 5.0, 2.0, 5.0, 5.0, 3.0],
[17.0, 7.0, 18.0, 12.0, 19.0, 9.0, 15.0, 18.0, 22.0, 23.0, 21.0, 6.0, 5.0, 20.0, 14.0, 7.0, 17.0, 15.0, 5.0, 7.0, 6.0, 1.0, 22.0, 24.0, 6.0, 4.0, 20.0, 18.0, 17.0, 17.0, 0.0, 0.0, 16.0, 18.0, 20.0, 14.0, 20.0, 11.0, 24.0, 23.0, 20.0, 15.0, 14.0, 9.0, 13.0, 13.0, 19.5, 20.0, 18.0, 9.0, 2.0, 24.0, 3.0, 12.0, 0.0, 22.0, 23.0, 24.0, 21.0, 22.0, 22.0, 5.0, 17.0, 18.0, 19.0, 23.0, 20.0, 23.0, 15.0, 12.0],
[1.0, 2.0, 4.0, 4.0, 2.0, 1.0, 2.0, 4.0, 3.0, 3.0, 4.0, 3.0, 3.0, 4.0, 3.0, 0.0, 4.0, 2.0, 1.0, 2.0, 2.0, 0.0, 4.0, 5.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 0.0, 0.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 4.0, 3.0, 2.0, 1.0, 2.0, 3.0, 2.0, 3.0, 3.0, 3.0, 4.0, 2.0, 1.0, 4.0, 1.0, 1.0, 0.0, 4.0, 3.0, 4.0, 3.0, 3.0, 3.0, 2.0, 2.0, 3.0, 1.0, 4.0, 4.0, 3.0, 2.0, 2.5] ] ,

"AIML_Scores":[[3.0, 5.0, 5.0, 4.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 4.0, 1.0, 5.0, 5.0, 3.0, 5.0, 4.0, 5.0, 4.0, 3.0, 4.0, 4.5, 3.0, 5.0, 5.0, 3.0, 2.0, 5.0, 4.0, 4.0, 5.0, 5.0, 5.0, 3.0, 3.0, 4.0, 3.0, 4.0, 5.0, 3.0, 5.0, 4.0, 4.0, 4.0, 3.5, 5.0, 5.0, 3.0, 5.0, 5.0, 5.0, 5.0, 5.0, 4.0, 5.0, 3.0, 5.0, 5.0, 2.0, 5.0, 5.0, 5.0, 2.0, 3.0],
[1.0, 4.0, 4.0, 2.0, 5.0, 5.0, 4.0, 5.0, 4.0, 5.0, 5.0, 4.0, 1.0, 5.0, 4.0, 2.0, 5.0, 4.0, 4.0, 3.0, 2.0, 3.0, 3.0, 2.0, 5.0, 5.0, 2.0, 2.0, 5.0, 4.0, 4.0, 4.0, 4.0, 4.0, 3.0, 2.0, 4.0, 3.0, 4.0, 5.0, 2.5, 4.0, 4.0, 4.0, 4.0, 2.5, 5.0, 4.0, 3.0, 5.0, 5.0, 5.0, 5.0, 5.0, 4.0, 5.0, 4.5, 5.0, 5.0, 1.0, 4.0, 4.0, 4.0, 2.0, 3.0],
[8.0, 14.0, 19.0, 21.0, 11.0, 13.0, 12.0, 19.0, 4.5, 18.0, 20.0, 14.0, 0.0, 20.0, 21.0, 8.0, 13.0, 13.0, 7.0, 6.0, 15.0, 5.0, 10.0, 13.0, 10.0, 
11.0, 17.0, 8.0, 8.0, 10.0, 18.0, 24.0, 10.0, 4.0, 9.0, 12.0, 18.0, 5.0, 10.0, 21.0, 0.0, 20.0, 13.0, 14.0, 1.0, 6.0, 24.0, 21.0, 12.0, 21.0, 20.0, 8.0, 6.0, 21.0, 19.0, 18.0, 10.0, 6.0, 8.0, 0.0, 19.0, 22.0, 23.0, 0.0, 1.5, 0, 0, 0, 0, 0],
[1.0, 2.0, 2.0, 4.0, 2.0, 1.0, 2.0, 2.5, 1.0, 2.5, 3.5, 3.0, 0.0, 4.0, 3.5, 1.0, 2.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 4.0, 2.0, 1.0, 1.0, 4.0, 2.0, 4.0, 4.0, 2.0, 2.0, 2.0, 1.0, 2.0, 2.0, 2.0, 1.0, 0.25, 0.5, 2.0, 0.5, 1.0, 1.0, 3.0, 2.0, 2.0, 1.0, 1.0, 2.0, 3.0, 2.0, 1.0, 2.0, 3.0, 0.0, 5.0, 0.0, 3.0, 2.0, 5.0, 0.0, 0.0]],  


 "avgCOMPSAScore":[3.8,3.62,14.25,2.12],
   "avgCOMPSBScore":[3.74,3.65,14.79,2.52,],
   "avgAIMLScore":[4.2,3.77,11.61,1.94],   
   "avgOverallScore":[5.83,5.01,17.69,2.4],
}


topics_ese_2={
 "Topic":["Intrinsic and extrinsic semiconductors","Formation of a P-N junction, depletion region and barrier potential","ntrinsic conductivity and extrinsic conductivity","intrinsic carrier concentration, electron and hole concentration"], 
 "Marks":[20,10,5,5], # topic weightage (total marks)    
 "COMPSA_Scores":[[15.0, 10.0, 11.0, 3.0, 7.5, 11.0, 15.0, 11.0, 12.5, 17.0, 11.0, 12.0, 12.0, 6.5, 5.0, 11.0, 12.5, 14.0, 13.0, 10.0, 15.0, 6.0, 18.5, 15.5, 14.5, 8.0, 11.0, 4.0, 1.0, 5.0, 10.0, 12.0, 2.0, 9.0, 9.0, 12.5, 18.0, 10.0, 4.0, 7.0, 17.0, 7.0, 8.0, 16.0, 7.0, 14.0, 14.0, 21.0, 20.0, 19.0, 12.0, 14.0, 13.0, 13.0, 12.0, 14.0, 16.0, 12.0, 15.0, 16.0, 13.0, 13.0, 17.0, 11.5, 9.0, 0.0, 15.0, 12.0, 13.0, 7.0],


 [3.0, 4.0, 4.0, 2.0, 6.0, 4.0, 8.0, 4.0, 8.0, 9.0, 6.0, 7.0, 5.0, 5.0, 4.0, 9.0, 7.0, 7.0, 8.0, 5.0, 7.0, 2.0, 8.0, 9.0, 8.0, 3.0, 6.0, 2.0, 1.0, 3.0, 4.0, 6.0, 1.0, 5.0, 4.0, 6.0, 10.0, 4.0, 1.0, 4.0, 9.0, 3.0, 5.0, 7.0, 3.0, 7.0, 7.0, 9.0, 10.0, 10.0, 5.0, 10.0, 9.0, 6.0, 6.0, 7.0, 9.0, 5.0, 9.0, 9.0, 7.0, 7.0, 8.0, 6.0, 4.0, 0.0, 8.0, 7.0, 9.0, 3.0] ,


[15.0, 10.0, 11.0, 3.0, 7.5, 11.0, 15.0, 11.0, 12.5, 17.0, 11.0, 12.0, 12.0, 6.5, 5.0, 11.0, 12.5, 14.0, 13.0, 10.0, 15.0, 6.0, 18.5, 15.5, 14.5, 8.0, 11.0, 4.0, 1.0, 5.0, 10.0, 12.0, 2.0, 9.0, 9.0, 12.5, 18.0, 10.0, 4.0, 7.0, 17.0, 7.0, 8.0, 16.0, 7.0, 14.0, 14.0, 21.0, 20.0, 19.0, 12.0, 14.0, 13.0, 13.0, 12.0, 14.0, 16.0, 12.0, 15.0, 16.0, 13.0, 13.0, 17.0, 11.5, 9.0, 0.0, 15.0, 12.0, 13.0, 7.0] , 


[3.0, 3.0, 4.0, 0.0, 1.5, 4.0, 3.0, 3.0, 2.5, 4.0, 2.0, 3.0, 4.0, 1.5, 0.0, 1.0, 1.5, 2.0, 2.0, 1.0, 5.0, 1.0, 6.5, 3.5, 2.5, 3.0, 2.0, 0.0, 0.0, 0.0, 3.0, 2.0, 0.0, 1.0, 2.0, 3.5, 4.0, 3.0, 2.0, 1.0, 4.0, 2.0, 1.0, 4.0, 2.0, 3.0, 3.0, 7.0, 5.0, 5.0, 2.0, 0.0, 0.0, 3.0, 2.0, 3.0, 3.0, 3.0, 2.0, 3.0, 2.0, 2.0, 5.0, 2.5, 2.0, 0.0, 2.0, 1.0, 0.0, 1.0] ] , 
"COMPSB_Scores":[[14.0, 12.0, 11.0, 10.0, 12.0, 11.0, 13.0, 9.0, 15.0, 15.0, 14.5, 8.0, 6.0, 14.0, 13.0, 6.0, 18.0, 14.0, 6.0, 13.0, 12.0, 2.0, 15.5, 16.0, 9.0, 9.0, 12.0, 11.0, 15.0, 13.0, 0.0, 1.0, 14.0, 11.5, 12.5, 9.0, 11.0, 14.0, 16.5, 15.5, 11.0, 10.0, 11.5, 13.5, 7.0, 11.0, 12.5, 14.5, 14.0, 13.5, 5.0, 19.0, 7.0, 9.0, 3.0, 15.0, 13.5, 14.5, 12.0, 15.0, 17.0, 9.0, 10.5, 15.0, 12.0, 17.0, 12.0, 16.0, 13.0, 10.5],


[5.0, 6.0, 8.0, 7.0, 6.0, 5.0, 6.0, 6.0, 8.0, 8.0, 8.0, 5.0, 2.0, 6.0, 4.0, 3.0, 9.0, 6.0, 4.0, 6.0, 5.0, 1.0, 9.0, 9.0, 5.0, 4.0, 6.0, 7.0, 6.0, 5.0, 0.0, 1.0, 7.0, 6.0, 9.0, 5.0, 6.0, 7.0, 10.0, 8.0, 7.0, 5.0, 7.0, 6.0, 4.0, 6.0, 6.0, 7.0, 8.0, 6.0, 3.0, 10.0, 2.0, 4.0, 1.0, 9.0, 7.0, 8.0, 7.0, 8.0, 8.0, 4.0, 4.0, 7.0, 6.0, 9.0, 7.0, 8.0, 5.0, 6.5],


[14.0, 12.0, 11.0, 10.0, 12.0, 11.0, 13.0, 9.0, 15.0, 15.0, 14.5, 8.0, 6.0, 14.0, 13.0, 6.0, 18.0, 14.0, 6.0, 13.0, 12.0, 2.0, 15.5, 16.0, 9.0, 9.0, 12.0, 11.0, 15.0, 13.0, 0.0, 1.0, 14.0, 11.5, 12.5, 9.0, 11.0, 14.0, 16.5, 15.5, 11.0, 10.0, 11.5, 13.5, 7.0, 11.0, 12.5, 14.5, 14.0, 13.5, 5.0, 19.0, 7.0, 9.0, 3.0, 15.0, 13.5, 14.5, 12.0, 15.0, 17.0, 9.0, 10.5, 15.0, 12.0, 17.0, 12.0, 16.0, 13.0, 10.5],


[3.0, 1.0, 0.0, 1.0, 1.0, 1.0, 3.0, 0.0, 3.0, 2.0, 2.5, 1.0, 2.0, 3.0, 4.0, 1.0, 5.0, 3.0, 0.0, 4.0, 3.0, 0.0, 3.5, 3.0, 2.0, 3.0, 2.0, 1.0, 5.0, 4.0, 0.0, 0.0, 3.0, 2.5, 1.5, 1.0, 2.0, 3.0, 2.5, 3.5, 0.0, 2.0, 1.5, 3.5, 0.0, 1.0, 2.5, 3.5, 2.0, 2.5, 0.0, 4.0, 4.0, 2.0, 1.0, 2.0, 2.5, 2.5, 1.0, 1.0, 4.0, 3.0, 1.5, 4.0, 2.0, 3.0, 3.0, 2.0, 3.0, 1.0]],


"AIML_Scores":[[6.0, 8.0, 9.5, 10.0, 14.0, 10.0, 13.0, 12.5, 8.0, 12.0, 12.0, 9.5, 2.0, 13.5, 11.5, 4.0, 11.0, 7.0, 7.5, 7.0, 6.5, 7.5, 7.5, 6.0, 12.5, 12.0, 5.0, 5.0, 11.0, 9.0, 10.0, 13.0, 10.0, 11.0, 5.0, 8.0, 7.0, 6.5, 9.5, 12.0, 4.0, 11.5, 8.5, 6.5, 8.0, 5.5, 15.0, 11.0, 5.0, 9.5, 12.5, 9.5, 7.5, 10.5, 8.5, 8.5, 9.0, 5.5, 14.0, 1.5, 13.5, 10.0, 8.0, 1.5, 3.0, 0, 0, 0, 0, 0],
[4.0, 5.0, 5.5, 6.0, 6.0, 4.0, 5.0, 6.5, 5.0, 6.5, 8.5, 6.0, 1.0, 8.0, 6.5, 2.5, 6.5, 3.5, 4.5, 3.0, 4.5, 4.0, 4.0, 4.0, 8.0, 7.0, 2.0, 3.0, 8.0, 5.0, 7.5, 6.0, 4.0, 5.0, 5.0, 4.0, 6.0, 3.0, 4.0, 6.0, 1.25, 3.0, 5.0, 4.0, 5.0, 3.5, 10.0, 6.0, 4.0, 6.0, 7.5, 5.5, 5.0, 5.0, 3.0, 6.0, 5.5, 3.0, 7.0, 1.0, 6.0, 7.0, 7.0, 1.0, 1.5, 0, 0, 0, 0, 0],


[6.0, 8.0, 9.5, 10.0, 14.0, 10.0, 13.0, 12.5, 8.0, 12.0, 12.0, 9.5, 2.0, 13.5, 11.5, 4.0, 11.0, 7.0, 7.5, 7.0, 6.5, 7.5, 7.5, 6.0, 12.5, 12.0, 5.0, 5.0, 11.0, 9.0, 10.0, 13.0, 10.0, 11.0, 5.0, 8.0, 7.0, 6.5, 9.5, 12.0, 4.0, 11.5, 8.5, 6.5, 8.0, 5.5, 15.0, 11.0, 5.0, 9.5, 12.5, 9.5, 7.5, 10.5, 8.5, 8.5, 9.0, 5.5, 14.0, 1.5, 13.5, 10.0, 8.0, 1.5, 3.0, 0, 0, 0, 0, 0],
[1.0, 1.0, 2.0, 1.0, 4.0, 1.0, 3.0, 1.0, 1.0, 0.5, 0.5, 0.5, 0.0, 0.5, 1.0, 0.0, 2.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.5, 1.0, 0.5, 0.0, 1.0, 0.0, 0.0, 2.0, 1.0, 2.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.5, 1.0, 1.0, 0.0, 0.5, 0.5, 0.0, 1.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.5, 1.0, 0.0, 1.5, 1.5, 0.0, 1.5, 0.0, 1.0, 0.0, 2.5, 1.0, 0.0, 0.0, 0.0]],
 
 "avgCOMPSAScore":[11.46 , 5.9 , 11.46 , 2.36],
   "avgCOMPSBScore":[11.67 , 5.99 , 11.67 , 2.15],
   "avgAIMLScore":[8.13 , 4.60 , 8.13 , 0.85],   
"avgOverallScore":[5.831, 5.831, 5.831, 5.8308333333333335],
}


topics_ese_3={
 "Topic":["pumping and pumping schemes","Processes - Absorption of light, spontaneous emission, stimulated emission","optical resonance cavity","Ruby and Helium Neon laser, semiconductor laser","Applications of laser in industry, medicine and holography. (construction&reconstruction of holograms)"], 
 "Marks":[5,10,10,10,5], # topic weightage (total marks)  
 "COMPSA_Scores":[[4.0, 1.0, 2.0, 1.0, 2.0, 2.0, 4.0, 2.0, 2.0, 3.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 4.0, 3.0, 3.0, 3.0, 2.0, 3.0, 4.0, 4.0, 4.0, 1.0, 2.0, 1.0, 0.0, 2.0, 3.0, 3.0, 1.0, 3.0, 2.0, 2.0, 4.0, 2.0, 0.0, 2.0, 4.0, 2.0, 0.0, 4.0, 2.0, 4.0, 4.0, 5.0, 4.0, 4.0, 3.0, 4.0, 2.0, 3.0, 4.0, 3.0, 3.0, 2.0, 3.0, 4.0, 2.0, 2.0, 4.0, 2.0, 2.0, 0.0, 4.0, 3.0, 4.0, 3.0],
[5.0, 4.0, 5.0, 2.0, 4.0, 3.0, 6.0, 5.0, 4.0, 5.0, 3.0, 3.0, 6.0, 5.0, 3.0, 5.0, 2.0, 5.0, 5.5, 5.0, 3.5, 0.5, 8.0, 6.0, 5.0, 1.5, 4.0, 0.0, 0.0, 2.0, 4.0, 3.0, 1.0, 4.0, 4.0, 4.0, 8.0, 3.0, 0.0, 4.0, 8.0, 0.5, 0.0, 3.0, 2.0, 5.0, 6.0, 9.0, 10.0, 10.0, 3.0, 7.5, 6.0, 6.0, 3.5, 6.0, 6.0, 3.0, 7.0, 8.5, 6.0, 4.5, 6.5, 6.5, 3.5, 0.0, 2.5, 4.5, 9.0, 0.0],


[5.0, 4.0, 5.0, 2.0, 4.0, 3.0, 6.0, 5.0, 4.0, 5.0, 3.0, 3.0, 6.0, 5.0, 3.0, 5.0, 2.0, 5.0, 5.5, 5.0, 3.5, 0.5, 8.0, 6.0, 5.0, 1.5, 4.0, 0.0, 0.0, 2.0, 4.0, 3.0, 1.0, 4.0, 4.0, 4.0, 8.0, 3.0, 0.0, 4.0, 8.0, 0.5, 0.0, 3.0, 2.0, 5.0, 6.0, 9.0, 10.0, 10.0, 3.0, 7.5, 6.0, 6.0, 3.5, 6.0, 6.0, 3.0, 7.0, 8.5, 6.0, 4.5, 6.5, 6.5, 3.5, 0.0, 2.5, 4.5, 9.0, 0.0],

[6.0, 4.0, 0.0, 5.0, 5.0, 3.0, 7.0, 6.0, 2.0, 2.0, 10.0, 9.0, 5.0, 6.0, 3.0, 7.0, 8.0, 8.5, 7.0, 7.0, 4.0, 0.0, 0.0, 10.0, 4.0, 0.0, 3.0, 2.0, 5.0, 3.0, 5.0, 3.0, 5.0, 8.0, 3.0, 5.0, 8.0, 4.0, 4.0, 3.0, 6.0, 3.0, 6.5, 2.0, 1.0, 2.0, 7.0, 10.0, 10.0, 10.0, 3.0, 7.0, 10.0, 8.0, 7.0, 8.0, 7.5, 8.0, 10.0, 5.0, 3.0, 3.0, 1.5, 8.0, 1.0, 0.0, 3.0, 2.0, 10.0, 2.5],


[6.0, 4.0, 0.0, 3.0, 5.0, 4.0, 4.0, 4.0, 4.0, 3.0, 2.0, 0.0, 0.0, 1.0, 5.0, 0.0, 1.5, 0.0, 3.0, 1.0, 5.0, 3.0, 5.0, 4.0, 4.0, 4.5, 5.0, 5.0, 1.0, 3.0, 4.0, 0.0, 0.0, 3.0, 5.0, 5.0, 5.0, 5.0, 3.0, 2.0, 6.0, 4.0, 5.0, 5.0, 4.0, 5.0, 1.0, 3.0, 5.0, 3.0, 5.0, 2.5, 5.0, 2.0, 4.0, 1.5, 5.0, 1.5, 4.0, 3.0, 5.0, 5.0, 6.0, 5.0, 2.0, 0.0, 4.0, 3.0, 4.0, 5.0]],




   "COMPSB_Scores":[[4.0, 4.0, 3.0, 2.0, 4.0, 3.0, 4.0, 2.0, 4.0, 4.0, 2.0, 2.0, 1.0, 4.0, 3.0, 2.0, 4.0, 4.0, 2.0, 2.0, 2.0, 1.0, 4.0, 4.0, 2.0, 2.0, 3.0, 4.0, 2.0, 3.0, 1.0, 0.0, 2.0, 2.0, 4.0, 2.0, 2.0, 2.0, 4.0, 3.0, 3.0, 2.0, 3.0, 2.0, 2.0, 3.0, 3.0, 4.0, 3.0, 3.0, 1.0, 4.0, 1.0, 3.0, 1.0, 4.0, 3.0, 2.0, 3.0, 4.0, 4.0, 2.0, 3.0, 4.0, 3.0, 4.0, 2.0, 3.0, 3.0, 4.0],


[1.5, 4.0, 3.0, 6.5, 3.5, 2.0, 4.0, 4.0, 5.5, 7.0, 6.5, 4.5, 3.0, 2.5, 4.5, 3.5, 5.5, 5.0, 4.0, 4.0, 4.0, 0.5, 4.5, 7.0, 4.0, 4.5, 6.0, 4.0, 3.5, 4.5, 1.0, 0.5, 4.5, 5.0, 5.5, 3.0, 5.0, 5.0, 8.5, 5.0, 6.0, 3.0, 2.5, 3.5, 3.5, 4.5, 4.0, 7.0, 6.5, 4.0, 2.0, 9.0, 3.5, 5.0, 0.0, 6.0, 5.0, 7.0, 5.5, 6.0, 7.0, 3.5, 5.0, 8.5, 5.5, 8.0, 5.0, 5.0, 4.0, 5.0],
[1.5, 4.0, 3.0, 6.5, 3.5, 2.0, 4.0, 4.0, 5.5, 7.0, 6.5, 4.5, 3.0, 2.5, 4.5, 3.5, 5.5, 5.0, 4.0, 4.0, 4.0, 0.5, 4.5, 7.0, 4.0, 4.5, 6.0, 4.0, 3.5, 4.5, 1.0, 0.5, 4.5, 5.0, 5.5, 3.0, 5.0, 5.0, 8.5, 5.0, 6.0, 3.0, 2.5, 3.5, 3.5, 4.5, 4.0, 7.0, 6.5, 4.0, 2.0, 9.0, 3.5, 5.0, 0.0, 6.0, 5.0, 7.0, 5.5, 6.0, 7.0, 3.5, 5.0, 8.5, 5.5, 8.0, 5.0, 5.0, 4.0, 5.0],


[10.0, 10.0, 3.0, 6.5, 12.0, 5.5, 3.0, 5.0, 10.0, 8.0, 6.0, 2.0, 2.0, 10.0, 2.0, 3.5, 10.0, 8.0, 4.0, 6.5, 6.0, 1.0, 5.0, 10.0, 2.0, 8.0, 5.0, 8.0, 8.0, 2.0, 0.0, 2.0, 8.0, 7.0, 8.0, 8.0, 5.0, 5.0, 10.0, 10.0, 10.0, 5.0, 5.0, 5.0, 5.0, 4.0, 3.0, 5.0, 5.0, 5.0, 4.5, 10.0, 8.0, 8.0, 2.0, 9.0, 5.0, 2.0, 4.0, 5.0, 5.0, 5.0, 8.0, 10.0, 5.0, 5.0, 0.0, 5.0, 7.0, 5.0],
[3.0, 1.0, 0.0, 0.0, 0.0, 5.0, 0.0, 3.0, 0.0, 4.0, 5.0, 3.0, 3.0, 2.5, 0.0, 0.0, 1.5, 3.0, 0.0, 0.0, 0.0, 0.0, 5.0, 0.5, 5.0, 0.5, 6.0, 2.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 1.0, 2.5, 1.0, 1.5, 4.0, 4.0, 4.0, 0.0, 1.5, 0.5, 5.0, 5.0, 5.0, 0.5, 0.0, 4.0, 0.5, 0.0, 0.0, 0.0, 4.0, 0.5, 5.0, 6.0, 6.0, 2.5, 2.0, 2.0, 2.5, 5.0, 0.0, 4.5, 0.0, 0.5]],


"AIML_Scores":[[1.0, 2.0, 3.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, 2.0, 2.0, 1.0, 2.0, 2.0, 1.0, 2.0, 1.0, 2.0, 2.0, 1.0, 2.0, 1.0, 1.0, 2.0, 5.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.5, 1.0, 2.0, 1.0, 1.0, 3.0, 1.0, 2.0, 2.5, 2.0, 2.0, 1.0, 3.0, 1.0, 0.5, 0.5, 1.5, 1.0, 0.5, 1.0, 0.5, 0.5, 0.5, 0.0, 1.0, 0.25, 0.5, 1.5, 0.5, 0.25, 0.5],


[3.0, 2.5, 5.0, 7.0, 4.0, 3.0, 5.0, 3.5, 4.0, 3.5, 5.5, 4.0, 1.0, 5.5, 5.0, 1.0, 3.0, 2.0, 2.0, 3.0, 4.0, 3.0, 3.0, 4.0, 6.0, 3.0, 2.0, 4.0, 1.0, 4.0, 4.0, 6.0, 4.0, 5.0, 4.0, 3.5, 3.0, 1.5, 2.0, 2.0, 0.0, 3.0, 3.0, 2.0, 2.5, 0.0, 3.0, 3.0, 0.5, 1.5, 1.5, 2.5, 3.0, 3.0, 0.5, 2.5, 1.5, 0.5, 2.0, 0.25, 1.5, 1.5, 2.0, 0.25, 0.5, 0, 0, 0, 0, 0],


[3.0, 2.5, 5.0, 7.0, 4.0, 3.0, 5.0, 3.5, 4.0, 3.5, 5.5, 4.0, 1.0, 5.5, 5.0, 1.0, 3.0, 2.0, 2.0, 3.0, 4.0, 3.0, 3.0, 4.0, 6.0, 3.0, 2.0, 4.0, 1.0, 4.0, 4.0, 6.0, 4.0, 5.0, 4.0, 3.5, 3.0, 1.5, 2.0, 2.0, 0.0, 3.0, 3.0, 2.0, 2.5, 0.0, 3.0, 3.0, 0.5, 1.5, 1.5, 2.5, 3.0, 3.0, 0.5, 2.5, 1.5, 0.5, 2.0, 0.25, 1.5, 1.5, 2.0, 0.25, 0.5, 0, 0, 0, 0, 0],


[6.0, 6.0, 5.0, 10.0, 5.0, 7.0, 5.0, 5.0, 5.0, 10.0, 10.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 10.0, 5.0, 4.0, 6.0, 2.0, 10.0, 5.0, 5.0, 5.0, 7.0, 7.0, 5.0, 5.0, 10.0, 7.0, 2.0, 5.0, 5.0, 5.0, 6.0, 5.0, 2.0, 5.0, 5.0, 6.0, 10.0, 5.0, 10.0, 10.0, 5.0, 3.0, 5.0, 5.0, 5.0, 5.0, 5.0, 2.0, 5.0, 3.0, 5.0, 0.0, 1.0, 10.0, 3.0, 4.0, 5.0],
[0.0, 0.0, 4.0, 0.5, 3.0, 0.0, 3.0, 0.0, 6.0, 2.0, 2.5, 4.0, 1.0, 0.0, 2.0, 3.0, 3.0, 1.0, 5.0, 2.0, 4.0, 0.0, 0.5, 0.0, 2.0, 4.0, 2.0, 2.0, 0.5, 0.5, 6.0, 0.0, 0.5, 0.0, 0.5, 5.5, 6.0, 3.0, 0.0, 3.0, 0.0, 6.0, 5.0, 0.0, 2.0, 4.0, 5.0, 3.5, 2.0, 0.0, 6.0, 4.0, 1.0, 5.0, 3.0, 0.0, 1.0, 0.0, 3.0, 0.0, 0.0, 1.5, 0.0, 0.0, 1.0]],


 "avgCOMPSAScore":[2.61 , 4.34 , 4,34 , 5.06 , 3.36],
   "avgCOMPSBScore":[2.78 , 4.56 , 4.56 , 5.85 , 1.92],
   "avgAIMLScore":[1.53 , 2.16 , 2.61 , 5.52 , 2.07],   
"avgOverallScore":[2.30 , 3.68 , 3.83  , 5.14 , 2.45 ],
}



# topics_ese_1={
#  "Topic":["pumping and pumping schemes","Processes - Absorption of light, spontaneous emission, stimulated emission","optical resonance cavity","Ruby and Helium Neon laser, semiconductor laser","Applications of laser in industry, medicine and holography. (construction&reconstruction of holograms)"], 
#  "Marks":[5,10,10,10,5], # topic weightage (total marks)  
#    "COMPSA_Scores":[[4,3,4,5,2],[8,5,9,8,2],[4,9,9,9,1],[2,8,8,6,2],[1,4,2,1,0]],
#    "COMPSB_Scores":[[4,3,4,5,2],[8,5,9,8,2],[4,9,9,9,1],[2,8,8,6,2],[1,4,2,1,0]],
#    "AIML_Scores":[[4,3,4,5,2],[8,5,9,8,2],[4,9,9,9,1],[2,8,8,6,2],[1,4,2,1,0]],
  
#  "avgCOMPSAScore":[2.4,3.45,3.122,5.7,3],
#    "avgCOMPSBScore":[2.21,3.35,3.512,5.4,3],
#    "avgAIMLScore":[2.45,3.13,4.10,5.2,2.5],   
#    "avgOverallScore":[2.4,3.45,3.122,5.3,4],
# }











#now in weightage render the weightage of the exam and module 
#for example if ise and module1 is selected then the weightage will be 80% 

#now in topic render topic name on left and marks on right
#for example if ise and module1 is selected then the topics will be topic1, topic2 and topic3 with marks 3,4,2 respectively

#now in category render the category name on left and percentage on right
#for example if ise and module1 is selected then the category will be numerical and mcq with percentage 80% and 20% respectively

#now in questions render the questions with a dropdown
#user can select from questions question1,2,3 etc
#display the question, plot the scatter plot plotted in try.py
#show the answer, if avg<(maxmarks/2), write diffuclty as medium


def callbacks2(app):
    @app.callback(
        [Output('division-store', 'data'), Output('module-store', 'data')],
        [Input('compsa-button', 'n_clicks'), Input('compsb-button', 'n_clicks'), Input('aiml-button', 'n_clicks'),
        Input('module1-button', 'n_clicks'), Input('module2-button', 'n_clicks'), Input('module3-button', 'n_clicks'), Input('module4-button', 'n_clicks')],
        [State('division-store', 'data'), State('module-store', 'data')]
    )
    def update_stores(compsa_clicks, compsb_clicks, aiml_clicks, module1_clicks, module2_clicks, module3_clicks, module4_clicks, division, module):
        ctx = dash.callback_context
        if not ctx.triggered:
            return division, module
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if button_id in ['compsa-button', 'compsb-button', 'aiml-button']:
                division = button_id.split('-')[0].upper()
            if button_id in ['module1-button', 'module2-button', 'module3-button','module4-button']:
                module = button_id.split('-')[0][-1]
                print("module selected: ",module)
            return division, module

    @app.callback(
        Output('main-container', 'children'),
        [Input('division-store', 'data'), Input('module-store', 'data')]
    )
    def update_main_container(division, module):
        
        ise_section = html.Div([
            html.H3(f"{division} Exam Weightage for Module {module}"),
            html.P(f"This is {division} exam weightage for Module {module}. Add your content here.")
        ], className='flex p-4 bg-gray-800 w-full rounded-md')
        mse_section = html.Div([
            html.H3(f"{division} Exam Topics for Module {module}"),
            html.P(f"This is {division} exam topics for Module {module}. Add your content here.")
        ], className='flex p-4 bg-gray-800 w-full rounded-md')

        ese_section = html.Div([
            html.P(f"Topic-wise Performance Analysis"),
            #list out all the topics of module 1 asked in ese exam from topics_ese_1
            html.Div([
                html.Div(f"{topic} - {marks} marks", className='flex justify-between')
                for topic, marks in zip(topics_ese_1["Topic"], topics_ese_1["Marks"])
            ], className='flex flex-col gap-2')


        ], className='flex p-4 bg-gray-800 w-full rounded-md')

        main_section=html.Div([
            #create a dropdown for selecting exams like ese, mse, ise
            html.Label("Select Exam:"),
            dcc.Dropdown(
                id="exam-dropdown",
                options=[{'label': exam, 'value': exam} for exam in ["ESE", "MSE", "ISE"]],
                value="ESE"
            ),
            #depening on the exam selected, render the respective section
            html.Div(id='exam-section', className="w-full")
        ])

        return html.Div([main_section], className='flex flex-row gap-10')

    @app.callback(
        Output('exam-section', 'children'),
        [Input('exam-dropdown', 'value')],
        [State('module-store', 'data')],
        [State('division-store','data')]
    )
    def update_exam_section(exam,module,division):

        if exam == "ESE":
            df = globals()[f'topics_ese_{module}']
            #I want to plot topic wise performance of students so x axis has score and y axis has count of students that got that score and render inside the below div for each topic and selected division

            # Plotting topic-wise performance of students
            topic_plots = []
            for i in range(len(df['Topic'])):
                topic = df['Topic'][i]
                scores = df[f"{division}_Scores"][i]
                max_marks = df['Marks'][i]
                avg_score = df[f"avg{division}Score"][i]
                
                # Create histogram data
                hist_data = [score for score in scores]
                hist_bins = list(range(0, max_marks+1))
                
                # Calculate average and median
                avg = sum(scores) / len(scores)
                median = sorted(scores)[len(scores) // 2]
                
                # Create vertical line for average
                avg_line = {
                    'type': 'line',
                    'x0': avg,
                    'x1': avg,
                    'y0': 0,
                    'y1': len(scores),
                    'line': {'color': 'white', 'width': 3}
                }
                
                # Create dotted line for median
                median_line = {
                    'type': 'line',
                    'x0': median,
                    'x1': median,
                    'y0': 0,
                    'y1': len(scores),
                    'line': {'color': 'yellow', 'width': 2, 'dash': 'dot'}
                }
                
                # Create histogram plot
                topic_plot = dcc.Graph(
                    figure={
                        'data': [
                            {
                                'x': hist_data,
                                'type': 'histogram',
                                'xbins': {'start': hist_bins[0], 'end': hist_bins[-1], 'size': 1},
                                'marker': {'color': 'skyblue'}
                            }
                        ],
                        'layout': {
                            'plot_bgcolor':'rgba(0, 0, 0, 0)',  # Transparent background
                            'paper_bgcolor':'rgba(0, 0, 0, 0)', 
                            'title': f"Topic: {topic}",
                            'xaxis': {'title': 'Score', 'color': 'white', 'gridcolor': 'gray'},
                            'yaxis': {'title': 'Performance', 'color': 'white', 'gridcolor': 'gray'},
                            'showlegend': False,
                            'shapes': [avg_line, median_line],
                            'font': {'color': 'white'}
                        }
                    }
                )
                hist_bins = list(range(0, max_marks+1))
                topic_plots.append(topic_plot)

                
            return html.Div([
                html.H2("Topics", className="text-4xl font-bold text-yellow-400"),
                html.Div([
                    html.Div([
                        html.P(f"{i+1}:{df['Topic'][i]}", className="mt-4 w-full text-2xl font-bold text-yellow-100"),
                        html.P(f"Marks: {df['Marks'][i]}", className="w-full text-xl text-pink-300"),
                        html.Div([topic_plots[i]]),  # Wrap topic_plots[i] inside an html.Div component
                                    
                    ], className="mt-2 flex flex-col bg-gray-900 p-1 px-4 rounded-md justify-between")
                    for i in range(0, len(df['Topic']))
                ], className="flex flex-col gap-4 justify-between")
            ], className='rounded-md bg-gray-800 w-full border border-black mt-4 p-4')
            

        elif exam == "MSE":
            print(type(module))
            if module=="1" or module=="4":
                df = globals()[f'topics_mse_{module}']
                #I want to plot topic wise performance of students so x axis has score and y axis has count of students that got that score and render inside the below div for each topic and selected division

                # Plotting topic-wise performance of students
                topic_plots = []
                for i in range(len(df['Topic'])):
                    topic = df['Topic'][i]
                    scores = df[f"{division}_Scores"][i]
                    max_marks = df['Marks'][i]
                    avg_score = df[f"avg{division}Score"][i]
                    
                    # Create histogram data
                    hist_data = [score for score in scores]
                    hist_bins = list(range(0, max_marks+1))
                    
                    # Calculate average and median
                    avg = sum(scores) / len(scores)
                    median = sorted(scores)[len(scores) // 2]
                    
                    # Create vertical line for average
                    avg_line = {
                        'type': 'line',
                        'x0': avg,
                        'x1': avg,
                        'y0': 0,
                        'y1': len(scores),
                        'line': {'color': 'white', 'width': 3}
                    }
                    
                    # Create dotted line for median
                    median_line = {
                        'type': 'line',
                        'x0': median,
                        'x1': median,
                        'y0': 0,
                        'y1': len(scores),
                        'line': {'color': 'yellow', 'width': 2, 'dash': 'dot'}
                    }
                    
                    # Create histogram plot
                    topic_plot = dcc.Graph(
                        figure={
                            'data': [
                                {
                                    'x': hist_data,
                                    'type': 'histogram',
                                    'xbins': {'start': hist_bins[0], 'end': hist_bins[-1], 'size': 1},
                                    'marker': {'color': 'skyblue'}
                                }
                            ],
                            'layout': {
                                'plot_bgcolor':'rgba(0, 0, 0, 0)',  # Transparent background
                                'paper_bgcolor':'rgba(0, 0, 0, 0)', 
                                'title': f"Topic: {topic}",
                                'xaxis': {'title': 'Score', 'color': 'white', 'gridcolor': 'gray'},
                                'yaxis': {'title': 'Performance', 'color': 'white', 'gridcolor': 'gray'},
                                'showlegend': False,
                                'shapes': [avg_line, median_line],
                                'font': {'color': 'white'}
                            }
                        }
                    )
                    hist_bins = list(range(0, max_marks+1))
                    topic_plots.append(topic_plot)

                    
                return html.Div([
                    html.H2("Topics", className="text-4xl font-bold text-yellow-400"),
                    html.Div([
                        html.Div([
                            html.P(f"{i+1}:{df['Topic'][i]}", className="mt-4 w-full text-2xl font-bold text-yellow-100"),
                            html.P(f"Marks: {df['Marks'][i]}", className="w-full text-xl text-pink-300"),
                            html.Div([topic_plots[i]]),  # Wrap topic_plots[i] inside an html.Div component
                                        
                        ], className="mt-2 flex flex-col bg-gray-900 p-1 px-4 rounded-md justify-between")
                        for i in range(0, len(df['Topic']))
                    ], className="flex flex-col gap-4 justify-between")
                ], className='rounded-md bg-gray-800 w-full border border-black mt-4 p-4')
                

      
            else:
                return html.Div([
                html.H2("No question was asked in MSE from this Module"),
                html.P("No data to display")
            ])

        elif exam == "ISE":
            return html.Div([
                html.H2("ISE Exam Section"),
                html.P("This is the ISE exam section. Add your content here.")
            ])
callbacks2(app)
if __name__ == '__main__':
    app.run_server(debug=True, port="3000")