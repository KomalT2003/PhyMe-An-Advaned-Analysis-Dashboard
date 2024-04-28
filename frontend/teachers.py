import dash
import pandas as pd
from dash import html, dcc
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

teachers_layout = html.Div([
    html.Link(
        rel='stylesheet',
        href='https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css'
    ),
    html.Div(className="bg-gray-900 text-yellow-300 bg-cover flex flex-row ", children=[
    html.Div(className="flex flex-col bg-gray-800 text-white flex justify-center items-center p-4 rounded-md",children=[
        html.Button("Performance", id="performance-button", n_clicks=0, className="mt-60 bg-gray-900 rounded-md w-60 py-2 px-2 mb-2 hover:bg-gray-600 hover:text-yellow-400 focus:outline-none"),
        html.Button("Module 1", id="module1-button", n_clicks=0, className="bg-gray-900 rounded-md w-60 py-2 px-2 mb-2 hover:bg-gray-600 hover:text-yellow-400 focus:outline-none"),
        html.Button("Module 2", id="module2-button", n_clicks=0, className="bg-gray-900 rounded-md w-60 py-2 px-4 mb-2 hover:bg-gray-600 hover:text-yellow-400 focus:outline-none"),
        html.Button("Module 3", id="module3-button", n_clicks=0, className="mb-60 bg-gray-900 rounded-md w-60 py-2 px-4 mb-2 hover:bg-gray-600 hover:text-yellow-400 focus:outline-none")
    ], id='sidebar'),
    html.Div(className="flex flex-col", children=[
    html.Div(className='flex h-24 bg-gray-900 text-blue-300 p-4 rounded-md ml-5',children=[ 
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

#DATA
weightage={"compsa1":"80%", "compsa2":"20%", "compsa3":"0%", "compsb1":"60%", "compsb2":"40%", "compsb3":"0%", "aiml1":"40%", "aiml2":"40%", "aiml3":"20%"}
#dictionary of topics and marks of each topic asked from module in exam
topics={
    "ise1":[("topic1",3),("topic2",4),("topix3",2)],
    "ise2":[("topic1",3),("topic2",4),("topix3",2)],
    "ise3":[("topic1",3),("topic2",4),("topix3",2)],
    "mse1":[("topic1",3),("topic2",4),("topix3",2)],
    "mse2":[("topic1",3),("topic2",4),("topix3",2)],
    "mse3":[("topic1",3),("topic2",4),("topix3",2)],
    "ese1":[("topic1",3),("topic2",4),("topix3",2)],
    "ese2":[("topic1",3),("topic2",4),("topix3",2)],
    "ese3":[("topic1",3),("topic2",4),("topix3",2)],
}

category={
    "ise1":[("numerical","80%"),("mcq","20%")],
    "ise2":[("numerical","60%"),("mcq","40%")],
    "ise3":[("numerical","40%"),("mcq","60%")],
    "mse1":[("numerical","80%"),("mcq","20%")],
    "mse2":[("numerical","60%"),("mcq","40%")],
    "mse3":[("numerical","40%"),("mcq","60%")],
    "ese1":[("numerical","80%"),("mcq","20%")],
    "ese2":[("numerical","60%"),("mcq","40%")],
    "ese3":[("numerical","40%"),("mcq","60%")]
                                 
}


questions_ise_1=pd.DataFrame({
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
        Input('module1-button', 'n_clicks'), Input('module2-button', 'n_clicks'), Input('module3-button', 'n_clicks')],
        [State('division-store', 'data'), State('module-store', 'data')]
    )
    def update_stores(compsa_clicks, compsb_clicks, aiml_clicks, module1_clicks, module2_clicks, module3_clicks, division, module):
        ctx = dash.callback_context
        if not ctx.triggered:
            return division, module
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if button_id in ['compsa-button', 'compsb-button', 'aiml-button']:
                division = button_id.split('-')[0].upper()
            if button_id in ['module1-button', 'module2-button', 'module3-button']:
                module = button_id.split('-')[0][-1]
                print("module selected: ",module)
            return division, module

    @app.callback(
        Output('main-container', 'children'),
        [Input('division-store', 'data'), Input('module-store', 'data')]
    )
    def update_main_container(division, module):
        
        weightage_section = html.Div([
            html.H3("Weightage", className="text-xl font-bold text-yellow-400"),
            html.P(f"{weightage.get(division.lower()+module)}", className="text-4xl font-bold text-yellow-100")
        ], className='flex flex-col border border-gray-700 drop-shadow-2xl justify-center bg-gray-800 h-1/3 w-full mb-4 p-4 rounded-md')

        topics_section = html.Div([
            html.H2("Topics", className="text-2xl font-bold text-yellow-400"),
            html.Div([
                html.Div([
                    html.P(f"{topic[0]}", className="text-lg text-yellow-100"),
                    html.P(f"{topic[1]}", className="text-lg text-yellow-100")
                ], className="mt-2 flex bg-gray-900 p-1 px-4 rounded-md justify-between")
                for topic in topics.get(division.lower()+module)], className="flex flex-col gap-2")
        ], className='rounded-md bg-gray-800 w-full border border-black mt-4 p-4')

        category_section = html.Div([
            html.H2("Category", className="text-2xl font-bold text-yellow-400"),
            html.Div([
                html.Div([
                    html.P(f"{cat[0]}", className="text-lg text-yellow-100"),
                    html.P(f"{cat[1]}", className="text-lg text-yellow-100")
                ], className="mt-2 flex bg-gray-900 p-1 px-4 rounded-md justify-between")
                for cat in category.get(division.lower()+module)], className="flex flex-col gap-2")
        ], className='rounded-md bg-gray-800 w-full mt-8 border-2 border-black drop-shadow-2xl  p-4')

        left_section = html.Div(className="flex flex-col w-1/2 ", children=[
            weightage_section,
            topics_section,
            category_section
        ])

    
        questions_section = html.Div([
            #access dataframe of questions_exam_type_module
            html.H3(f"{division} Exam Questions for Module {module}"),
            html.P(f"This is {division} exam questions for Module {module}. Add your content here.")
        ], className='flex p-4 bg-gray-800 w-full rounded-md')

        return html.Div([left_section, questions_section], className='flex flex-row gap-10')

    # if __name__ == '__main__':
    #     app.run_server(debug=True)