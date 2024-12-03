import dash
import plotly.graph_objs as go
import pandas as pd
from dash import html, dcc
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

server = app.server

app.layout = html.Div([
    html.Link(
        rel='stylesheet',
        href='https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css'
    ),
    html.Div(className="bg-gray-900 text-yellow-300 min-h-screen bg-cover ", children=[
        html.Nav(className="flex justify-between items-center border-b border-gray-800 p-4", children=[
            html.H1('PhyMe', className='ml-5 text-5xl font-bold'),
            html.Div(className="flex gap-5 mr-5", children=[
                html.A('Students', href='http://localhost:5000', className='p-2  border-2 rounded-md bg-gray-800 hover:text-gray-400 focus:outline-none '),
                html.A('Teachers', href='http://localhost:3000', className='p-2 -ml-2 border-2 rounded-md bg-gray-800 hover:text-gray-400 focus:outline-none')
            ])
        ]),
        html.Div(className="bg-gray-900 text-yellow-300 bg-cover flex flex-row ", children=[
            html.Div(className="mt-10 mb-10 flex flex-col bg-gray-800 text-white flex justify-center items-center p-4 rounded-md", children=[
                html.Button("Overall", id="performance-button", n_clicks=0, className="mt-60 bg-gray-900 rounded-md w-60 py-2 px-2 mb-2 hover:bg-gray-600 hover:text-yellow-400 focus:outline-none"),
                html.Button("Module 1", id="module1-button", n_clicks=0, className="bg-gray-900 rounded-md w-60 py-2 px-2 mb-2 hover:bg-gray-600 hover:text-yellow-400 focus:outline-none"),
                html.Button("Module 2", id="module2-button", n_clicks=0, className="bg-gray-900 rounded-md w-60 py-2 px-4 mb-2 hover:bg-gray-600 hover:text-yellow-400 focus:outline-none"),
                html.Button("Module 3", id="module3-button", n_clicks=0, className="bg-gray-900 rounded-md w-60 py-2 px-4 mb-2 hover:bg-gray-600 hover:text-yellow-400 focus:outline-none"),
                html.Button("Self study", id="module4-button", n_clicks=0, className="mb-60 bg-gray-900 rounded-md w-60 py-2 px-4 mb-2 hover:bg-gray-600 hover:text-yellow-400 focus:outline-none")
            ], id='sidebar'),
            html.Div(className="flex flex-col", children=[
                html.Div(className='flex h-24 bg-gray-900 text-blue-300 p-4 rounded-md ml-5', children=[ 
                    html.Button("ISE Exam", id="ise-button", className="border-2 w-72 mx-2 py-2 px-4 bg-gray-800 hover:bg-gray-600 rounded-md hover:text-yellow-400 focus:outline-none"),
                    html.Button("MSE Exam", id="mse-button", className="border-2 w-72 mx-2 py-2 px-4 bg-gray-800 hover:bg-gray-600 rounded-md hover:text-yellow-400 focus:outline-none"),
                    html.Button("ESE Exam", id="ese-button", className="border-2 w-72 mx-2 py-2 px-4 bg-gray-800 hover:bg-gray-600 rounded-md hover:text-yellow-400 focus:outline-none"),
                ], id='main-screen'),
                html.Div(className=' mr-30 flex bg-gray-900 text-blue-300 p-4 rounded-md ml-5', children=[
                    html.Div(id='main-container'),
                ]), 
                dcc.Store(id='exam-type-store', data='ISE'),
                dcc.Store(id='module-store', data='1')
            ])
        ])
    ])
])



weightage={"ise1":"0%","ise2":"100%","ise3":"0%","ise4":"0%","mse1":"75%","mse2":"0%","mse3":"0%","mse4":"25%","ese1":"40%", "ese2":"30%", "ese3":"30%"}

topics={
    #ise1 should have topics: de-Broglie hypothesis; experimental verification of de Brogliehypothesis; wave packet, group velocity and phase velocity;Wave function, Physical interpretation of wave function;Heisenberg's uncertainty principle; Electron diffractionexperiment; Applications of uncertainty principle
    "ise1":[("de-Broglie hypothesis",0),("experimental verification of de Brogliehypothesis",0),("wave packet, group velocity and phase velocity",0),("Wave function, Physical interpretation of wave function",0),("Heisenberg's uncertainty principle",0),("Electron diffractionexperiment",0),("Applications of uncertainty principle",0)],
    "ise4":[("Formation of a P-N junction, depletion region and barrier potential",0),("Effect of impurity concentration and temperature on the Fermi Level",0),("intrinsic carrier concentration,",0),("Hall Effect and its applications",0)],
    "ise3":[("Wave nature of matter",0),("Davisson-Germer experiment",0),("Bohr’s theory of hydrogen atom",0),("Spectrum of hydrogen atom",0),("Quantum numbers",0),("Pauli’s exclusion principle",0),("Aufbau principle",0),("Hund’s rule",0),("Electronic configuration of elements",0)],
    "ise2":[("Law of mass action",1),("Conduction in metals and semiconductors",4),("Intrinsic and extrinsic semiconductors, intrinsic conductivity and extrinsic conductivity,",7),("Drift and Diffusion current",1),("Fermi-Dirac distribution function",1),
("Formation of a P-N junction, depletion region and barrier potential",1),("Effect of impurity concentration and temperature on the Fermi Level",3),("intrinsic carrier concentration,",2),("Hall Effect and its applications",2)],
    "mse1":[("wave packet, group velocity and phase velocity",2),("Heisenberg’s uncertainty principle",4),("De-broglie wavelength and its application,",2),("Potential barrier(Tunnelling)",6),("Infinite Potential Well(Particle Trapped in 1d box) & Schrondinger Wave Eq",6)],
    "mse4":[("Interference of light in thin films having uniform thickness",2),("Applications of interference in anti-reflecting and highly reflecting thin films",2)],
    "mse2":[("Wave nature of matter",0),("Davisson-Germer experiment",0),("Bohr’s theory of hydrogen atom",0),("Spectrum of hydrogen atom",0),("Quantum numbers",0),("Pauli’s exclusion principle",0),("Aufbau principle",0),("Hund’s rule",0),("Electronic configuration of elements",0)],
    "mse3":[("Quantum mechanical model of atom",0),("Dual nature of electron",0),("Heisenberg’s uncertainty principle",0),("Quantum mechanical model of hydrogen atom",0),("Quantum numbers",0),("Electronic configuration of elements",0),("Pauli’s exclusion principle",0),("Aufbau principle",0),("Hund’s rule",0)],
    "ese1":[("Schrodinger's time dependent wave equation, time independent wave equation ",5),("wave packet, group velocity and phase velocity",5),("Application of time-independent Schrodinger equation - Particle trapped in one dimensional box and Potential barrier (Tunnelling), Harmonic oscillator (qualitative)",25),(",Electron diffraction experiment",5)],
   "ese2":[("Intrinsic and extrinsic semiconductors",20),("Formation of a P-N junction, depletion region and barrier potential",10),("ntrinsic conductivity and extrinsic conductivity",5),("intrinsic carrier concentration, electron and hole concentration",5)],
   "ese3":[("pumping and pumping schemes",5),("Processes - Absorption of light, spontaneous emission, stimulated emission",10),("optical resonance cavity",10),("Ruby and Helium Neon laser, semiconductor laser",10),("Applications of laser in industry, medicine and holography. (construction&reconstruction of holograms)",5)],
    "ise4":[("topic1",3),("topic2",4),("topix3",2)],
    "ese4":[("topic1",3),("topic2",4),("topix3",2)]
}
topics_list = [topic[0] for topic in topics["ise2"]]
marks_list = [topic[1] for topic in topics["ise2"]]

# Plot weightage of each topic
fig = go.Figure(go.Bar(
    x=topics_list,
    y=marks_list,
    marker_color='rgb(55, 83, 109)'
))

fig.update_layout(
    title='Weightage of Topics in ise2',
    xaxis=dict(
        title='Topics',
        tickfont_size=14,
    ),
    yaxis=dict(
        title='Weightage',
        titlefont_size=16,
        tickfont_size=14,
    ),
    bargap=0.15,  # gap between bars of adjacent location coordinates.
    bargroupgap=0.1  # gap between bars of the same location coordinate.
)

category={
      "ise1":[("numerical","0%"),("theory","0%")],
   "ise2":[("numerical","50%"),("theory","50%")],
   "ise3":[("numerical","0%"),("theory","0%")],
   "ise4":[("numerical","0%"),("theory","0%")],
   "mse1":[("numerical","62.50%"),("theory","12.50%")],
   "mse2":[("numerical","0%"),("theory","0%")],
   "mse3":[("numerical","0%"),("theory","0%")],
   "mse4":[("numerical","12.50%"),("theory","12.50%")],     
"ese1":[("numerical","75%"),("theory","25%")],
   "ese2":[("numerical","50%"),("theory","50%")],
   "ese3":[("numerical","17%"),("mcq","83%")],
    "ese4":[("numerical","10%"),("mcq","50%")]
}

questions_mse_1={
   "questions":["Define: Wave packet and group velocity.",
                "Show that an electron cannot be a part of the nucleus (r=10-14 m)using Heisenberg’s Uncertainty principle.",
                "The de-Broglie wavelength of a proton is 0.113pm, i) What is the speed of the proton?ii) Through what electric potential difference would the proton have to be accelerated from rest to acquire this speed?",
                "A proton and a deuteron, each having 3MeV of energy, attempt to penetrate a rectangular potential barrier of height 10MeV which particle has a higher probability of succeeding. Explain in qualitative terms.",
                "Consider an electron trapped in an infinite potential well whose width is 98.5 pm. If it is in a state with n=15, calculate (i) its energy (ii) the uncertainty in its momentum and (iii) the uncertainty in its position.",
                "An electron is trapped in an infinite potential well of width (L). If the electron is in its first excited state, what fraction of its time does it spend in the central one-third of the well?",
                "An electron of total energy 2 eV is approaching a barrier 5 eV high and 1 nm wide. Determine the wavelength of incident electron and probability of transmission through the barrier. What do you infer by the calculated value of the transmission probability"],
   "marks":[2,2,2,2,2,4,4],
   "category":["theory","theory","numerical","numerical","numerical","numerical","numerical"],
   "topic":[("wave packet, group velocity and phase velocity","Heisenberg’s uncertainty principle"),"De-broglie wavelength and its application"," Potential barrier(Tunnelling)",("Heisenberg’s uncertainty principle","Infinite Potential Well(Particle Trapped in 1d box) & Schrondinger Wave Eq"),"Infinite Potential Well(Particle Trapped in 1d box) & Schrondinger Wave Eq"," Potential barrier(Tunnelling)"],
   "A_Scores":[[2.0, 1.5, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 0.0, 2.0, 2.0, 2.0, 1.0, 1.5, 0.5, 0.0, 1.5, 2.0, 2.0, 0.5, 2.0, 2.0, 2.0, 2.0, 1.0, 0.5, 2.0, 2.0, 1.0, 2.0, 2.0, 0.5, 2.0, 2.0, 1.5, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 0.5, 2.0, 0.0, 2.0, 2.0, 2.0],
                [4.0, 2.0, 2.5, 1.0, 3.0, 4.0, 3.0, 3.0, 3.0, 4.0, 3.5, 3.0, 4.0, 3.0, 3.0, 4.0, 3.0, 3.0, 3.0, 2.5, 3.5, 0.0, 3.0, 3.5, 3.0, 2.0, 2.5, 0.5, 0.0, 1.5, 2.0, 2.0, 0.5, 3.0, 3.0, 2.0, 4.0, 2.5, 0.5, 2.0, 2.0, 1.5, 4.0, 3.0, 1.5, 4.0, 4.0, 3.5, 4.0, 4.0, 3.0, 4.0, 4.0, 3.0, 2.0, 4.0, 4.0, 3.0, 3.0, 3.0, 4.0, 3.5, 3.5, 0.5, 2.5, 0.0, 4.0, 2.5, 4.0],
                [2.0, 0.0, 2.0, 0.0, 2.0, 1.0, 2.0, 1.0, 2.0, 1.0, 2.0, 2.0, 2.0, 1.5, 2.0, 2.0, 2.0, 2.0, 1.5, 2.0, 1.0, 0.0, 2.0, 2.0, 2.0, 0.0, 1.0, 0.0, 0.0, 1.0, 2.0, 2.0, 0.0, 0.0, 1.0, 2.0, 2.0, 1.5, 0.0, 0.0, 2.0, 0.5, 2.0, 0.0, 2.0, 1.0, 0.0, 2.0, 2.0, 1.0, 2.0, 2.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.5, 1.0, 2.0, 2.0, 1.0, 0.5, 2.0, 1.5, 0.0, 2.0, 1.5, 2.0],
                [5.5, 5.5, 3.5, 2.5, 3.5, 3.0, 5.5, 1.5, 6.0, 3.0, 4.0, 3.0, 3.5, 3.0, 1.5, 4.0, 3.0, 6.0, 6.0, 0.5, 6.0, 0.5, 6.0, 4.0, 6.0, 6.0, 3.0, 1.0, 0.5, 1.0, 2.0, 3.0, 0.0, 5.5, 2.5, 4.0, 6.0, 2.5, 0.0, 1.0, 2.0, 1.5, 0.0, 5.0, 1.0, 1.5, 4.5, 5.5, 6.0, 6.0, 5.5, 4.0, 3.0, 6.0, 5.5, 6.0, 6.0, 3.5, 3.5, 6.0, 3.0, 5.0, 4.5, 1.0, 4.5, 0.0, 6.0, 1.0, 6.0],
                [4.0, 2.0, 2.5, 1.0, 3.0, 4.0, 3.0, 3.0, 3.0, 4.0, 3.5, 3.0, 4.0, 3.0, 3.0, 4.0, 3.0, 3.0, 3.0, 2.5, 3.5, 0.0, 3.0, 3.5, 3.0, 2.0, 2.5, 0.5, 0.0, 1.5, 2.0, 2.0, 0.5, 3.0, 3.0, 2.0, 4.0, 2.5, 0.5, 2.0, 2.0, 1.5, 4.0, 3.0, 1.5, 4.0, 4.0, 3.5, 4.0, 4.0, 3.0, 4.0, 4.0, 3.0, 2.0, 4.0, 4.0, 3.0, 3.0, 3.0, 4.0, 3.5, 3.5, 0.5, 2.5, 0.0, 4.0, 2.5, 4.0],
                [6.0, 1.0, 2.5, 0.0, 2.0, 3.0, 2.0, 1.5, 4.5, 2.5, 2.0, 3.0, 2.0, 2.0, 1.0, 6.0, 5.0, 3.0, 5.0, 4.0, 5.5, 1.0, 4.5, 5.5, 3.0, 3.5, 2.5, 0.0, 0.0, 1.0, 0.5, 0.0, 0.0, 1.5, 1.5, 2.0, 6.0, 2.5, 0.0, 1.0, 4.0, 1.5, 3.0, 5.0, 1.0, 4.0, 3.5, 6.0, 6.0, 6.0, 2.5, 5.5, 3.0, 5.0, 0.0, 6.0, 3.5, 4.0, 2.5, 4.5, 6.0, 5.0, 5.5, 1.5, 1.5, 0.0, 6.0, 2.5, 6.0],
                [6.0, 1.0, 2.5, 0.0, 2.0, 3.0, 2.0, 1.5, 4.5, 2.5, 2.0, 3.0, 2.0, 2.0, 1.0, 6.0, 5.0, 3.0, 5.0, 4.0, 5.5, 1.0, 4.5, 5.5, 3.0, 3.5, 2.5, 0.0, 0.0, 1.0, 0.5, 0.0, 0.0, 1.5, 1.5, 2.0, 6.0, 2.5, 0.0, 1.0, 4.0, 1.5, 3.0, 5.0, 1.0, 4.0, 3.5, 6.0, 6.0, 6.0, 2.5, 5.5, 3.0, 5.0, 0.0, 6.0, 3.5, 4.0, 2.5, 4.5, 6.0, 5.0, 5.5, 1.5, 1.5, 0.0, 6.0, 2.5, 6.0],
                [5.5, 5.5, 3.5, 2.5, 3.5, 3.0, 5.5, 1.5, 6.0, 3.0, 4.0, 3.0, 3.5, 3.0, 1.5, 4.0, 3.0, 6.0, 6.0, 0.5, 6.0, 0.5, 6.0, 4.0, 6.0, 6.0, 3.0, 1.0, 0.5, 1.0, 2.0, 3.0, 0.0, 5.5, 2.5, 4.0, 6.0, 2.5, 0.0, 1.0, 2.0, 1.5, 0.0, 5.0, 1.0, 1.5, 4.5, 5.5, 6.0, 6.0, 5.5, 4.0, 3.0, 6.0, 5.5, 6.0, 6.0, 3.5, 3.5, 6.0, 3.0, 5.0, 4.5, 1.0, 4.5, 0.0, 6.0, 1.0, 6.0]],

   "B_Scores":[[0.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.5, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.5, 0.5, 2.0, 2.0, 1.0, 1.5, 2.0, 1.0, 2.0, 2.0, 0.5, 2.0, 2.0, 2.0, 2.0, 2.0, 0.5, 0.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.5, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 2.0, 2.0, 2.0, 0.5, 2.0, 2.0, 2.0, 1.5, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 2.0],
               [0.5, 4.0, 3.0, 3.0, 3.0, 3.0, 2.5, 3.0, 2.0, 4.0, 4.0, 3.0, 4.0, 3.0, 3.0, 3.5, 1.0, 3.0, 3.0, 2.0, 2.5, 4.0, 1.0, 4.0, 4.0, 1.0, 3.5, 4.0, 4.0, 4.0, 3.0, 0.5, 0.0, 3.0, 3.0, 3.5, 2.0, 3.0, 4.0, 4.0, 4.0, 2.5, 2.0, 3.0, 3.5, 2.0, 2.5, 3.5, 4.0, 2.0, 3.5, 1.0, 3.0, 3.0, 2.0, 0.5, 3.0, 3.0, 3.0, 2.5, 4.0, 4.0, 2.0, 2.0, 3.5, 4.0, 4.0, 1.0, 4.0],
               [0.5, 1.0, 2.0, 2.0, 1.5, 2.0, 1.0, 0.5, 1.0, 2.0, 2.0, 1.5, 1.0, 1.0, 2.0, 2.0, 1.0, 2.0, 1.0, 1.0, 1.5, 2.0, 0.0, 2.0, 2.0, 1.0, 1.5, 1.0, 2.0, 2.0, 1.0, 0.0, 0.0, 2.0, 2.0, 2.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 0.5, 1.0, 1.5, 1.5, 1.0, 2.0, 2.0, 2.0, 2.0, 0.5, 1.5, 2.0, 1.0, 0.0, 1.5, 2.0, 1.5, 2.0, 1.5, 2.0, 1.0, 1.0, 2.0, 2.0, 2.0, 0.0, 2.0],
               [0.5, 2.0, 6.0, 0.5, 6.0, 4.0, 2.0, 3.0, 1.0, 6.0, 5.5, 5.5, 6.0, 5.5, 3.5, 4.5, 2.5, 1.0, 5.0, 3.0, 3.5, 3.0, 0.5, 6.0, 5.0, 4.0, 3.5, 2.0, 5.5, 6.0, 1.0, 0.0, 0.0, 5.5, 6.0, 4.0, 0.0, 4.5, 3.5, 6.0, 5.5, 5.5, 5.5, 3.5, 3.0, 4.0, 1.0, 2.5, 3.0, 5.5, 6.0, 2.0, 6.0, 2.0, 5.0, 1.0, 5.0, 6.0, 6.0, 5.5, 6.0, 5.0, 4.0, 4.5, 2.5, 6.0, 6.0, 3.0, 6.0],
               [0.5, 4.0, 3.0, 3.0, 3.0, 3.0, 2.5, 3.0, 2.0, 4.0, 4.0, 3.0, 4.0, 3.0, 3.0, 3.5, 1.0, 3.0, 3.0, 2.0, 2.5, 4.0, 1.0, 4.0, 4.0, 1.0, 3.5, 4.0, 4.0, 4.0, 3.0, 0.5, 0.0, 3.0, 3.0, 3.5, 2.0, 3.0, 4.0, 4.0, 4.0, 2.5, 2.0, 3.0, 3.5, 2.0, 2.5, 3.5, 4.0, 2.0, 3.5, 1.0, 3.0, 3.0, 2.0, 0.5, 3.0, 3.0, 3.0, 2.5, 4.0, 4.0, 2.0, 2.0, 3.5, 4.0, 4.0, 1.0, 4.0],
               [0.5, 2.5, 1.0, 2.0, 5.0, 3.0, 2.0, 2.0, 0.5, 6.0, 4.0, 4.5, 6.0, 4.5, 2.5, 6.0, 4.5, 4.0, 4.0, 2.0, 2.0, 6.0, 0.0, 4.5, 6.0, 0.5, 4.5, 2.5, 6.0, 5.0, 2.0, 0.0, 0.0, 1.5, 2.0, 5.5, 0.0, 2.0, 6.0, 4.0, 5.5, 4.0, 1.5, 2.0, 5.0, 0.5, 1.0, 3.5, 2.5, 0.0, 5.5, 0.0, 3.0, 1.0, 1.5, 0.0, 4.5, 5.0, 5.0, 1.5, 6.0, 5.0, 1.0, 3.0, 5.0, 4.0, 6.0, 0.0, 6.0],
               [0.5, 2.5, 1.0, 2.0, 5.0, 3.0, 2.0, 2.0, 0.5, 6.0, 4.0, 4.5, 6.0, 4.5, 2.5, 6.0, 4.5, 4.0, 4.0, 2.0, 2.0, 6.0, 0.0, 4.5, 6.0, 0.5, 4.5, 2.5, 6.0, 5.0, 2.0, 0.0, 0.0, 1.5, 2.0, 5.5, 0.0, 2.0, 6.0, 4.0, 5.5, 4.0, 1.5, 2.0, 5.0, 0.5, 1.0, 3.5, 2.5, 0.0, 5.5, 0.0, 3.0, 1.0, 1.5, 0.0, 4.5, 5.0, 5.0, 1.5, 6.0, 5.0, 1.0, 3.0, 5.0, 4.0, 6.0, 0.0, 6.0],
               [0.5, 2.0, 6.0, 0.5, 6.0, 4.0, 2.0, 3.0, 1.0, 6.0, 5.5, 5.5, 6.0, 5.5, 3.5, 4.5, 2.5, 1.0, 5.0, 3.0, 3.5, 3.0, 0.5, 6.0, 5.0, 4.0, 3.5, 2.0, 5.5, 6.0, 1.0, 0.0, 0.0, 5.5, 6.0, 4.0, 0.0, 4.5, 3.5, 6.0, 5.5, 5.5, 5.5, 3.5, 3.0, 4.0, 1.0, 2.5, 3.0, 5.5, 6.0, 2.0, 6.0, 2.0, 5.0, 1.0, 5.0, 6.0, 6.0, 5.5, 6.0, 5.0, 4.0, 4.5, 2.5, 6.0, 6.0, 3.0, 6.0]],

   "C_Scores":[[2.0, 2.0, 2.0, 2.0, 0.5, 1.5, 1.5, 2.0, 0.5, 1.5, 2.0, 2.0, 2.0, 2.0, 0.0, 1.0, 2.0, 1.0, 2.0, 2.0, 2.0, 1.5, 0.5, 1.5, 0.5, 1.0, 1.5, 1.5, 1.5, 1.5, 2.0, 1.0, 1.5, 2.0, 1.0, 1.0, 1.5, 1.5, 2.0, 2.0, 1.0, 2.0, 0.0, 2.0, 2.0, 1.5, 2.0, 0.0, 2.0, 2.0, 0.0, 1.5, 1.5, 2.0, 1.5, 1.0, 1.0, 2.0, 2.0, 1.0, 2.0, 1.5, 1.0, 2.0, 0.5, 0.0, 0.0],
               [3.0, 3.0, 3.0, 4.0, 1.5, 2.5, 2.5, 3.0, 1.5, 2.0, 4.0, 3.0, 4.0, 4.0, 0.0, 1.5, 2.0, 2.5, 3.0, 3.0, 2.5, 2.5, 1.0, 3.0, 1.5, 3.0, 2.5, 3.5, 3.0, 3.5, 3.0, 2.5, 2.5, 3.0, 2.0, 3.0, 3.5, 2.5, 3.0, 3.0, 3.0, 3.0, 1.0, 4.0, 3.5, 3.0, 3.0, 1.0, 3.0, 3.0, 1.0, 3.5, 3.5, 4.0, 2.5, 2.0, 2.0, 3.5, 2.5, 2.0, 2.5, 2.0, 2.5, 3.5, 1.5, 0.0, 1.0],
               [2.0, 2.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 1.5, 1.5, 2.0, 0.5, 2.0, 2.0, 0.5, 2.0, 2.0, 2.0, 1.0, 2.0, 0.0, 1.0, 1.0, 2.0, 1.5, 2.0, 2.0, 2.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 0.0, 2.0, 2.0, 1.5, 2.0, 2.0, 2.0, 2.0, 1.0, 1.5, 2.0, 1.0, 2.0, 1.0, 2.0, 1.5, 0.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.5, 1.0, 1.0, 2.0, 1.5, 2.0, 0.0, 1.0],
               [5.5, 5.5, 5.5, 4.0, 5.5, 5.5, 3.0, 1.0, 3.5, 3.0, 0.5, 1.0, 3.5, 2.0, 0.0, 4.5, 1.5, 4.5, 5.5, 0.0, 0.5, 3.0, 3.0, 2.5, 5.0, 3.0, 3.0, 4.0, 2.0, 1.5, 2.0, 6.0, 6.0, 5.5, 3.0, 5.5, 2.0, 0.5, 3.0, 3.0, 5.5, 1.0, 1.5, 5.5, 1.5, 1.5, 1.0, 0.0, 3.0, 3.5, 3.0, 5.5, 6.0, 6.0, 3.5, 3.0, 3.5, 3.0, 0.0, 4.0, 3.0, 0.0, 5.5, 3.5, 5.0, 1.0, 1.0],
               [3.0, 3.0, 3.0, 4.0, 1.5, 2.5, 2.5, 3.0, 1.5, 2.0, 4.0, 3.0, 4.0, 4.0, 0.0, 1.5, 2.0, 2.5, 3.0, 3.0, 2.5, 2.5, 1.0, 3.0, 1.5, 3.0, 2.5, 3.5, 3.0, 3.5, 3.0, 2.5, 2.5, 3.0, 2.0, 3.0, 3.5, 2.5, 3.0, 3.0, 3.0, 3.0, 1.0, 4.0, 3.5, 3.0, 3.0, 1.0, 3.0, 3.0, 1.0, 3.5, 3.5, 4.0, 2.5, 2.0, 2.0, 3.5, 2.5, 2.0, 2.5, 2.0, 2.5, 3.5, 1.5, 0.0, 1.0],
               [1.0, 5.0, 1.0, 4.0, 5.0, 3.5, 3.0, 5.0, 1.0, 2.0, 3.0, 2.0, 6.0, 3.5, 0.0, 1.5, 3.0, 3.0, 1.0, 1.0, 0.5, 1.0, 4.0, 1.5, 2.0, 3.0, 2.0, 2.0, 1.5, 2.0, 5.0, 1.5, 2.0, 4.5, 1.0, 3.5, 6.0, 2.0, 3.0, 1.0, 3.0, 1.0, 1.0, 6.0, 2.5, 1.5, 2.5, 3.0, 5.0, 2.0, 2.0, 5.5, 5.0, 3.5, 2.0, 1.0, 2.0, 2.5, 2.5, 1.0, 2.5, 0.5, 4.0, 4.5, 3.0, 0.5, 1.0],
               [1.0, 5.0, 1.0, 4.0, 5.0, 3.5, 3.0, 5.0, 1.0, 2.0, 3.0, 2.0, 6.0, 3.5, 0.0, 1.5, 3.0, 3.0, 1.0, 1.0, 0.5, 1.0, 4.0, 1.5, 2.0, 3.0, 2.0, 2.0, 1.5, 2.0, 5.0, 1.5, 2.0, 4.5, 1.0, 3.5, 6.0, 2.0, 3.0, 1.0, 3.0, 1.0, 1.0, 6.0, 2.5, 1.5, 2.5, 3.0, 5.0, 2.0, 2.0, 5.5, 5.0, 3.5, 2.0, 1.0, 2.0, 2.5, 2.5, 1.0, 2.5, 0.5, 4.0, 4.5, 3.0, 0.5, 1.0],
               [5.5, 5.5, 5.5, 4.0, 5.5, 5.5, 3.0, 1.0, 3.5, 3.0, 0.5, 1.0, 3.5, 2.0, 0.0, 4.5, 1.5, 4.5, 5.5, 0.0, 0.5, 3.0, 3.0, 2.5, 5.0, 3.0, 3.0, 4.0, 2.0, 1.5, 2.0, 6.0, 6.0, 5.5, 3.0, 5.5, 2.0, 0.5, 3.0, 3.0, 5.5, 1.0, 1.5, 5.5, 1.5, 1.5, 1.0, 0.0, 3.0, 3.5, 3.0, 5.5, 6.0, 6.0, 3.5, 3.0, 3.5, 3.0, 0.0, 4.0, 3.0, 0.0, 5.5, 3.5, 5.0, 1.0, 1.0]],
  
 "avgAScore":[1.7,2.77,1.29,3.58,2.77,3.04,3.04,3.58],
   "avgBScore":[1.76,2.86,1.4,3.89,2.86,3.11,3.11,3.89],
   "avgCScore":[1.41,2.59,1.59,3.12,2.59,2.59,2.59,3.12],   
   "avgOverallScore":[1.62,2.74,1.43,3.53,2.74,2.91,2.91,3.53],
}





questions_mse_4={
   "questions":["A soap film on a wire loop held in air appears dark at its thinnest portion when viewed by reflected light. Explain this phenomenon.",
                "In costume jewelry, rhinestones (made of glass with µ=1.5) are often coated with silicon monoxide (µ=2.0) to make them more reflective.How thick the coating be to achieve strong reflection for 560 nm light, incident normally?"],

   "marks":[2,2],
   "category":["theory","numerical"],
   "topic":["Interference of light in thin films having uniform thickness","Applications of interference in anti-reflecting and highly reflecting thin films"],
   "A_Scores":[[1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.5, 0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 2.0, 0.0, 2.0, 1.0, 0.0, 2.0, 0.5, 2.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 1.0],
               [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],

   "B_Scores":[[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 2.0, 2.0, 0.0, 0.5, 1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 1.0, 0.0, 2.0, 1.0, 0.0, 0.0, 1.0, 1.0, 2.0, 1.0, 2.0, 2.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 2.0],
               [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.5, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 1.5, 0.0, 0.0, 0.0]],

   "C_Scores":[[1.0, 1.0, 0.5, 0.0, 0.5, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 1.0, 0.0, 0.0, 2.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
               [0.0, 0.0, 1.5, 0.0, 1.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.5, 0.0, 0.0, 1.5, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 1.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0]],
  
 "avgAScore":[0.46,0.15],
   "avgBScore":[0.52,0.26],
   "avgCScore":[0.266,0.23],   
   "avgOverallScore":[0.415,0.2133],
}

questions_ese_3={
   "questions":["Differentiate between the three level and four level pumping schemes with neat energy level diagrams. Mention the names of the laser which employs these schemes.","Write the full form of LASER. How is the light beam emitted from a laser different from the light beam emitted by ordinary sources of light? Explain the role of plane parallel mirrors in optical resonators.","A Ruby laser emits light at a wavelength of 694.3 nm. If a laser pulse is emitted for 12 ps and the energy released per pulse is 150 mJ. (a) How many photons are there in each pulse? (b) calculate the rate of photons emitted.","Describe the construction of a Ruby laser using aschematic diagram. Explain its working with an energy level diagram. Mention two disadvantages of Ruby laser over the He-Ne laser. Why optical pumping cannot be used to achieve population inversion in He-Ne Laser? ","What is Holography? Mention any two advantages of holography over photography and write two important applications of holography?"],
   "marks":[5,5,5,10,5],
   "category":["theory","theory","numerical","theory","theory"],
   "topic":["pumping and pumping schemes","Processes - Absorption of light, spontaneous emission, stimulated emission","Processes - Absorption of light","Ruby and Helium Neon laser, semiconductor laser","Applications of laser in industry, medicine and holography. (construction&reconstruction of holograms)"],
"A_Scores":[[4.0, 1.0, 2.0, 1.0, 2.0, 2.0, 4.0, 2.0, 2.0, 3.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 4.0, 3.0, 3.0, 3.0, 2.0, 3.0, 4.0, 4.0, 4.0, 1.0, 2.0, 1.0, 0.0, 2.0, 3.0, 3.0, 1.0, 3.0, 2.0, 2.0, 4.0, 2.0, 0.0, 2.0, 4.0, 2.0, 0.0, 4.0, 2.0, 4.0, 4.0, 5.0, 4.0, 4.0, 3.0, 4.0, 2.0, 3.0, 4.0, 3.0, 3.0, 2.0, 3.0, 4.0, 2.0, 2.0, 4.0, 2.0, 2.0, 0.0, 4.0, 3.0, 4.0, 3.0],
[3.0, 2.0, 2.0, 2.0, 2.0, 2.0, 4.0, 3.0, 3.0, 2.0, 2.0, 2.0, 3.0, 4.0, 2.0, 3.0, 1.0, 3.0, 3.5, 4.0, 0.5, 0.5, 4.0, 4.0, 3.0, 0.5, 1.0, 0.0, 0.0, 1.0, 3.0, 1.0, 1.0, 2.0, 3.0, 1.0, 4.0, 1.0, 0.0, 2.0, 4.0, 0.5, 0.0, 1.0, 1.0, 4.0, 4.0, 5.0, 5.0, 5.0, 1.0, 2.5, 1.0, 4.0, 2.5, 4.0, 3.0, 2.0, 3.0, 4.5, 2.0, 2.5, 4.5, 4.5, 1.5, 0.0, 0.5, 3.5, 5.0, 0.0],


[2.0, 2.0, 3.0, 0.0, 2.0, 1.0, 2.0, 2.0, 1.0, 3.0, 1.0, 1.0, 3.0, 1.0, 1.0, 2.0, 1.0, 2.0, 2.0, 1.0, 3.0, 0.0, 4.0, 2.0, 2.0, 1.0, 3.0, 0.0, 0.0, 1.0, 1.0, 2.0, 0.0, 2.0, 1.0, 3.0, 4.0, 2.0, 0.0, 2.0, 4.0, 0.0, 0.0, 2.0, 1.0, 1.0, 2.0, 4.0, 5.0, 5.0, 2.0, 5.0, 5.0, 2.0, 1.0, 2.0, 3.0, 1.0, 4.0, 4.0, 4.0, 2.0, 2.0, 2.0, 2.0, 0.0, 2.0, 1.0, 4.0, 0.0],


[6.0, 4.0, 0.0, 5.0, 5.0, 3.0, 7.0, 6.0, 2.0, 2.0, 10.0, 9.0, 5.0, 6.0, 3.0, 7.0, 8.0, 8.5, 7.0, 7.0, 4.0, 0.0, 0.0, 10.0, 4.0, 0.0, 3.0, 2.0, 5.0, 3.0, 5.0, 3.0, 5.0, 8.0, 3.0, 5.0, 8.0, 4.0, 4.0, 3.0, 6.0, 3.0, 6.5, 2.0, 1.0, 2.0, 7.0, 10.0, 10.0, 10.0, 3.0, 7.0, 10.0, 8.0, 7.0, 8.0, 7.5, 8.0, 10.0, 5.0, 3.0, 3.0, 1.5, 8.0, 1.0, 0.0, 3.0, 2.0, 10.0, 2.5],
[6.0, 4.0, 0.0, 3.0, 5.0, 4.0, 4.0, 4.0, 4.0, 3.0, 2.0, 0.0, 0.0, 1.0, 5.0, 0.0, 1.5, 0.0, 3.0, 1.0, 5.0, 3.0, 5.0, 4.0, 4.0, 4.5, 5.0, 5.0, 1.0, 3.0, 4.0, 0.0, 0.0, 3.0, 5.0, 5.0, 5.0, 5.0, 3.0, 2.0, 6.0, 4.0, 5.0, 5.0, 4.0, 5.0, 1.0, 3.0, 5.0, 3.0, 5.0, 2.5, 5.0, 2.0, 4.0, 1.5, 5.0, 1.5, 4.0, 3.0, 5.0, 5.0, 6.0, 5.0, 2.0, 0.0, 4.0, 3.0, 4.0, 5.0]],


   "B_Scores":[[4.0, 4.0, 3.0, 2.0, 4.0, 3.0, 4.0, 2.0, 4.0, 4.0, 2.0, 2.0, 1.0, 4.0, 3.0, 2.0, 4.0, 4.0, 2.0, 2.0, 2.0, 1.0, 4.0, 4.0, 2.0, 2.0, 3.0, 4.0, 2.0, 3.0, 1.0, 0.0, 2.0, 2.0, 4.0, 2.0, 2.0, 2.0, 4.0, 3.0, 3.0, 2.0, 3.0, 2.0, 2.0, 3.0, 3.0, 4.0, 3.0, 3.0, 1.0, 4.0, 1.0, 3.0, 1.0, 4.0, 3.0, 2.0, 3.0, 4.0, 4.0, 2.0, 3.0, 4.0, 3.0, 4.0, 2.0, 3.0, 3.0, 4.0],
[0.5, 3.0, 1.0, 3.5, 2.5, 1.0, 3.0, 1.0, 2.5, 5.0, 2.5, 2.5, 2.0, 0.5, 2.5, 2.5, 2.5, 3.0, 3.0, 2.0, 1.0, 0.5, 1.5, 3.0, 2.0, 2.5, 4.0, 2.0, 1.5, 2.5, 1.0, 0.5, 1.5, 2.0, 2.5, 1.0, 2.0, 2.0, 4.5, 3.0, 3.0, 2.0, 0.5, 1.5, 2.5, 2.5, 2.0, 5.0, 3.5, 2.0, 1.0, 5.0, 2.5, 4.0, 0.0, 2.0, 3.0, 3.0, 2.5, 4.0, 4.0, 1.5, 4.0, 5.5, 4.5, 4.0, 2.0, 3.0, 2.0, 2.5],


[1.0, 1.0, 2.0, 3.0, 1.0, 1.0, 1.0, 3.0, 3.0, 2.0, 4.0, 2.0, 1.0, 2.0, 2.0, 1.0, 3.0, 2.0, 1.0, 2.0, 3.0, 0.0, 3.0, 4.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 0.0, 0.0, 3.0, 3.0, 3.0, 2.0, 3.0, 3.0, 4.0, 2.0, 3.0, 1.0, 2.0, 2.0, 1.0, 2.0, 2.0, 2.0, 3.0, 2.0, 1.0, 4.0, 1.0, 1.0, 0.0, 4.0, 2.0, 4.0, 3.0, 2.0, 3.0, 2.0, 1.0, 3.0, 1.0, 4.0, 3.0, 2.0, 2.0, 2.5],


[10.0, 10.0, 3.0, 6.5, 12.0, 5.5, 3.0, 5.0, 10.0, 8.0, 6.0, 2.0, 2.0, 
10.0, 2.0, 3.5, 10.0, 8.0, 4.0, 6.5, 6.0, 1.0, 5.0, 10.0, 2.0, 8.0, 5.0, 8.0, 8.0, 2.0, 0.0, 2.0, 8.0, 7.0, 8.0, 8.0, 5.0, 5.0, 10.0, 10.0, 10.0, 5.0, 5.0, 5.0, 5.0, 4.0, 3.0, 5.0, 5.0, 5.0, 4.5, 10.0, 8.0, 8.0, 2.0, 9.0, 5.0, 2.0, 4.0, 5.0, 5.0, 5.0, 8.0, 10.0, 5.0, 5.0, 0.0, 5.0, 7.0, 5.0],
[3.0, 1.0, 0.0, 0.0, 0.0, 5.0, 0.0, 3.0, 0.0, 4.0, 5.0, 3.0, 3.0, 2.5, 0.0, 0.0, 1.5, 3.0, 0.0, 0.0, 0.0, 0.0, 5.0, 0.5, 5.0, 0.5, 6.0, 2.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 1.0, 2.5, 1.0, 1.5, 4.0, 4.0, 4.0, 0.0, 1.5, 0.5, 5.0, 5.0, 5.0, 0.5, 0.0, 4.0, 0.5, 0.0, 0.0, 0.0, 4.0, 0.5, 5.0, 6.0, 6.0, 2.5, 2.0, 2.0, 2.5, 5.0, 0.0, 4.5, 0.0, 0.5]],

"C_Scores":[[1.0, 2.0, 3.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 3.0, 2.0, 2.0, 1.0, 2.0, 2.0, 1.0, 2.0, 1.0, 2.0, 2.0, 1.0, 2.0, 1.0, 1.0, 2.0, 5.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.5, 1.0, 2.0, 1.0, 1.0, 3.0, 1.0, 2.0, 2.5, 2.0, 2.0, 1.0, 3.0, 1.0, 0.5, 0.5, 1.5, 1.0, 0.5, 1.0, 0.5, 0.5, 0.5, 0.0, 1.0, 0.25, 0.5, 1.5, 0.5, 0.25, 0.5],
[2.0, 1.5, 3.0, 3.0, 2.0, 2.0, 3.0, 1.0, 3.0, 1.0, 2.0, 2.0, 1.0, 1.5, 1.5, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 1.0, 2.0, 2.0, 1.0, 1.0, 3.0, 1.0, 2.0, 2.0, 2.0, 1.0, 3.0, 1.0, 1.5, 2.0, 0.5, 1.0, 1.0, 0.0, 3.0, 2.0, 2.0, 1.5, 0.0, 2.0, 1.0, 0.5, 0.5, 0.5, 0.5, 0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 1.0, 0.25, 0.5, 0.5, 0.0, 0.25, 0.5],
[1.0, 1.0, 2.0, 4.0, 2.0, 1.0, 2.0, 2.5, 1.0, 2.5, 3.5, 2.0, 0.0, 4.0, 3.5, 0.0, 2.0, 1.0, 1.0, 1.0, 2.0, 1.0, 2.0, 2.0, 4.0, 2.0, 1.0, 1.0, 0.0, 2.0, 2.0, 4.0, 3.0, 2.0, 3.0, 2.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 2.0, 0.0, 1.0, 1.0, 2.0, 3.0, 3.0, 0.0, 2.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 2.0, 0.0, 0.0],
[6.0, 6.0, 5.0, 10.0, 5.0, 7.0, 5.0, 5.0, 5.0, 10.0, 10.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 10.0, 5.0, 4.0, 6.0, 2.0, 10.0, 5.0, 5.0, 5.0, 7.0, 7.0, 5.0, 5.0, 10.0, 7.0, 2.0, 5.0, 5.0, 5.0, 6.0, 5.0, 2.0, 5.0, 5.0, 6.0, 10.0, 5.0, 10.0, 10.0, 5.0, 3.0, 5.0, 5.0, 5.0, 5.0, 5.0, 2.0, 5.0, 3.0, 5.0, 0.0, 1.0, 10.0, 3.0, 4.0, 5.0],
[0.0, 0.0, 4.0, 0.5, 3.0, 0.0, 3.0, 0.0, 6.0, 2.0, 2.5, 4.0, 1.0, 0.0, 2.0, 3.0, 3.0, 1.0, 5.0, 2.0, 4.0, 0.0, 0.5, 0.0, 2.0, 4.0, 2.0, 2.0, 0.5, 0.5, 6.0, 0.0, 0.5, 0.0, 0.5, 5.5, 6.0, 3.0, 0.0, 3.0, 0.0, 6.0, 5.0, 0.0, 2.0, 4.0, 5.0, 3.5, 2.0, 0.0, 6.0, 4.0, 1.0, 5.0, 3.0, 0.0, 1.0, 0.0, 3.0, 0.0, 0.0, 1.5, 0.0, 0.0, 1.0]],


 "avgAScore":[2.4,3.45,3.122],
   "avgBScore":[2.21,3.35,3.512],
   "avgCScore":[2.45,3.13,4.10],   
   "avgOverallScore":[2.4,3.45,3.122],
}


questions_ese_2={
   "questions":["Draw the energy band diagram of an intrinsic semiconductor at room temperature and prove that the Fermi level of the intrinsic semiconductor lies at the center of the forbidden gap.","Explain the formation of the depletion region in a p-n junction with a proper diagram. Can the barrier potential be measured using a voltmeter? Justify your answer.","What is the significance of the forbidden energy gap? Describe the procedure to determine the forbidden energy gap of the extrinsic semiconductor at room temperature with the right mathematical expression.","In a doped semiconductor there are 4.52 × 1024 holes and 1.25 × 1014 electrons per m3 . What will be the intrinsic carrier density? Calculate the conductivity of the intrinsic and doped semiconductor. Given μe=0.38 m2/V.s and μh=0.18 m2/V.s.","The resistivity of the two sides of a Ge diode are 4 Ωcm on p-side and 2 Ωcm on n-side. Calculate the height of the potential energy barrier. Given: ni = 2.25x 1013/cm3, μe=0.38 m2/V.s and μh=0.18 m2 /V.s.","An n-type Si wafer is doped uniformly with Sb atoms, and the doped Si has donor concentration of 1016/cm3. Calculate the Fermi energy with respect to the Fermi energy in intrinsic Si. (ni = 1.45 x 1010/cm3)."],
   "marks":[5,5,5,5,5,5],
   "category":["theory","theory","theory","numerical","numerical","numerical"],
   "topic":[" Intrinsic and extrinsic semiconductors","Formation of a P-N junction, depletion region and barrier potential","Intrinsic and extrinsic semiconductors","Intrinsic and extrinsic semiconductors","Formation of a P-N junction, depletion region and barrier potential","Intrinsic and extrinsic semiconductors"],
"A_Scores":[[4.0, 3.0, 2.0, 1.0, 2.0, 3.0, 5.0, 3.0, 4.0, 5.0, 4.0, 4.0, 3.0, 2.0, 2.0, 4.0, 5.0, 4.0, 4.0, 4.0, 4.0, 2.0, 4.0, 5.0, 5.0, 2.0, 3.0, 2.0, 1.0, 2.0, 3.0, 4.0, 1.0, 3.0, 3.0, 3.0, 5.0, 2.0, 1.0, 2.0, 5.0, 3.0, 4.0, 5.0, 2.0, 4.0, 4.0, 5.0, 5.0, 5.0, 4.0, 5.0, 4.0, 4.0, 5.0, 4.0, 5.0, 4.0, 4.0, 5.0, 4.0, 4.0, 5.0, 4.0, 3.0, 0.0, 5.0, 4.0, 5.0, 3.0],
[1.0, 2.0, 2.0, 1.0, 3.0, 3.0, 5.0, 3.0, 4.0, 5.0, 4.0, 4.0, 2.0, 3.0, 3.0, 5.0, 5.0, 4.0, 4.0, 4.0, 3.0, 2.0, 4.0, 5.0, 5.0, 2.0, 3.0, 2.0, 1.0, 2.0, 3.0, 4.0, 1.0, 3.0, 3.0, 3.0, 5.0, 2.0, 1.0, 2.0, 5.0, 3.0, 4.0, 5.0, 2.0, 4.0, 4.0, 5.0, 5.0, 5.0, 3.0, 5.0, 4.0, 4.0, 5.0, 4.0, 5.0, 3.0, 4.0, 5.0, 3.0, 4.0, 5.0, 4.0, 3.0, 0.0, 5.0, 4.0, 5.0, 3.0],


[5.0, 2.0, 2.0, 1.0, 2.0, 2.0, 4.0, 2.0, 3.0, 4.0, 3.0, 3.0, 2.0, 2.0, 2.0, 3.0, 4.0, 4.0, 3.0, 4.0, 3.0, 3.0, 4.0, 4.0, 4.0, 2.0, 3.0, 2.0, 0.0, 2.0, 3.0, 4.0, 1.0, 3.0, 3.0, 3.0, 4.0, 2.0, 1.0, 2.0, 4.0, 2.0, 2.0, 4.0, 2.0, 4.0, 4.0, 5.0, 5.0, 4.0, 3.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 3.0, 4.0, 4.0, 3.0, 4.0, 4.0, 3.0, 2.0, 0.0, 4.0, 4.0, 4.0, 3.0],


[3.0, 2.0, 3.0, 1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 4.0, 2.0, 2.0, 3.0, 1.0, 1.0, 3.0, 2.0, 4.0, 4.0, 1.0, 3.0, 0.0, 4.0, 3.0, 3.0, 1.0, 3.0, 0.0, 0.0, 1.0, 1.0, 2.0, 0.0, 2.0, 1.0, 3.0, 5.0, 3.0, 0.0, 2.0, 4.0, 0.0, 1.0, 3.0, 1.0, 3.0, 3.0, 4.0, 5.0, 5.0, 3.0, 5.0, 5.0, 2.0, 1.0, 3.0, 4.0, 2.0, 5.0, 4.0, 4.0, 3.0, 3.0, 2.0, 2.0, 0.0, 4.0, 3.0, 4.0, 0.0],


[2.0, 2.0, 2.0, 1.0, 3.0, 1.0, 3.0, 1.0, 4.0, 4.0, 2.0, 3.0, 3.0, 2.0, 1.0, 4.0, 2.0, 3.0, 4.0, 1.0, 4.0, 0.0, 4.0, 4.0, 3.0, 1.0, 3.0, 0.0, 0.0, 1.0, 1.0, 2.0, 0.0, 2.0, 1.0, 3.0, 5.0, 2.0, 0.0, 2.0, 4.0, 0.0, 1.0, 2.0, 1.0, 3.0, 3.0, 4.0, 5.0, 5.0, 2.0, 5.0, 5.0, 2.0, 1.0, 3.0, 4.0, 2.0, 5.0, 4.0, 4.0, 3.0, 3.0, 2.0, 1.0, 0.0, 3.0, 3.0, 4.0, 0.0],


[3.0, 3.0, 4.0, 0.0, 1.5, 4.0, 3.0, 3.0, 2.5, 4.0, 2.0, 3.0, 4.0, 1.5, 0.0, 1.0, 1.5, 2.0, 2.0, 1.0, 5.0, 1.0, 6.5, 3.5, 2.5, 3.0, 2.0, 0.0, 0.0, 0.0, 3.0, 2.0, 0.0, 1.0, 2.0, 3.5, 4.0, 3.0, 2.0, 1.0, 4.0, 2.0, 1.0, 4.0, 2.0, 3.0, 3.0, 7.0, 5.0, 5.0, 2.0, 0.0, 0.0, 3.0, 2.0, 3.0, 3.0, 3.0, 2.0, 3.0, 2.0, 2.0, 5.0, 2.5, 2.0, 0.0, 2.0, 1.0, 0.0, 1.0]],


"B_Scores":[[5.0, 4.0, 3.0, 2.0, 4.0, 4.0, 4.0, 3.0, 5.0, 5.0, 4.0, 2.0, 1.0, 4.0, 3.0, 2.0, 5.0, 4.0, 3.0, 4.0, 4.0, 1.0, 5.0, 5.0, 3.0, 2.0, 4.0, 5.0, 4.0, 3.0, 0.0, 1.0, 4.0, 4.0, 5.0, 3.0, 4.0, 4.0, 5.0, 4.0, 4.0, 4.0, 4.0, 4.0, 3.0, 4.0, 4.0, 4.0, 4.0, 4.0, 2.0, 5.0, 1.0, 3.0, 1.0, 5.0, 4.0, 4.0, 4.0, 5.0, 5.0, 2.0, 4.0, 4.0, 4.0, 5.0, 2.0, 5.0, 4.0, 5.0],
[4.0, 4.0, 3.0, 2.0, 4.0, 4.0, 4.0, 2.0, 5.0, 5.0, 4.0, 2.0, 1.0, 4.0, 3.0, 2.0, 5.0, 4.0, 3.0, 4.0, 3.0, 1.0, 5.0, 5.0, 3.0, 2.0, 4.0, 5.0, 3.0, 3.0, 0.0, 1.0, 4.0, 4.0, 5.0, 3.0, 3.0, 3.0, 5.0, 4.0, 4.0, 4.0, 4.0, 3.0, 3.0, 4.0, 4.0, 4.0, 4.0, 4.0, 2.0, 5.0, 1.0, 3.0, 1.0, 5.0, 4.0, 3.0, 4.0, 5.0, 5.0, 2.0, 3.0, 4.0, 4.0, 5.0, 2.0, 5.0, 3.0, 4.0],


[4.0, 4.0, 3.0, 2.0, 4.0, 4.0, 4.0, 2.0, 4.0, 4.0, 4.0, 2.0, 1.0, 4.0, 3.0, 2.0, 5.0, 4.0, 2.0, 3.0, 3.0, 1.0, 4.0, 4.0, 2.0, 2.0, 4.0, 4.0, 3.0, 3.0, 0.0, 0.0, 4.0, 3.0, 4.0, 3.0, 3.0, 3.0, 4.0, 4.0, 4.0, 3.0, 4.0, 3.0, 2.0, 3.0, 3.0, 4.0, 4.0, 4.0, 2.0, 5.0, 1.0, 3.0, 1.0, 4.0, 4.0, 3.0, 4.0, 5.0, 5.0, 2.0, 3.0, 4.0, 4.0, 5.0, 2.0, 5.0, 4.0, 2.0],


[2.0, 3.0, 5.0, 5.0, 3.0, 2.0, 2.0, 4.0, 3.0, 4.0, 4.0, 3.0, 2.0, 3.0, 3.0, 1.0, 3.0, 3.0, 1.0, 2.0, 2.0, 0.0, 3.0, 4.0, 2.0, 2.0, 2.0, 1.0, 3.0, 3.0, 0.0, 0.0, 3.0, 2.0, 2.0, 2.0, 2.0, 4.0, 5.0, 4.0, 3.0, 1.0, 2.0, 3.0, 2.0, 3.0, 3.0, 3.0, 4.0, 3.0, 1.0, 5.0, 1.0, 1.0, 0.0, 4.0, 3.0, 5.0, 3.0, 4.0, 3.0, 2.0, 2.0, 3.0, 2.0, 4.0, 5.0, 4.0, 2.0, 2.5],


[1.0, 2.0, 5.0, 5.0, 2.0, 1.0, 2.0, 4.0, 3.0, 3.0, 4.0, 3.0, 1.0, 2.0, 1.0, 1.0, 4.0, 2.0, 1.0, 2.0, 2.0, 0.0, 4.0, 4.0, 2.0, 2.0, 2.0, 2.0, 3.0, 2.0, 0.0, 0.0, 3.0, 2.0, 4.0, 2.0, 3.0, 4.0, 5.0, 4.0, 3.0, 1.0, 3.0, 3.0, 1.0, 2.0, 2.0, 3.0, 4.0, 2.0, 1.0, 5.0, 1.0, 1.0, 0.0, 4.0, 3.0, 5.0, 3.0, 3.0, 3.0, 2.0, 1.0, 3.0, 2.0, 4.0, 5.0, 3.0, 2.0, 2.5],


[3.0, 1.0, 0.0, 1.0, 1.0, 1.0, 3.0, 0.0, 3.0, 2.0, 2.5, 1.0, 2.0, 3.0, 4.0, 1.0, 5.0, 3.0, 0.0, 4.0, 3.0, 0.0, 3.5, 3.0, 2.0, 3.0, 2.0, 1.0, 5.0, 4.0, 0.0, 0.0, 3.0, 2.5, 1.5, 1.0, 2.0, 3.0, 2.5, 3.5, 0.0, 2.0, 1.5, 3.5, 0.0, 1.0, 2.5, 3.5, 2.0, 2.5, 0.0, 4.0, 4.0, 2.0, 1.0, 2.0, 2.5, 2.5, 1.0, 1.0, 4.0, 3.0, 1.5, 4.0, 2.0, 3.0, 3.0, 2.0, 3.0, 1.0]],


"C_Scores":[[2.0, 3.0, 3.0, 3.0, 5.0, 4.0, 4.0, 5.0, 3.0, 5.0, 5.0, 4.0, 1.0, 5.0, 4.0, 2.0, 4.0, 3.0, 3.0, 2.0, 2.0, 3.0, 3.0, 2.0, 5.0, 5.0, 1.0, 2.0, 4.0, 3.0, 3.0, 3.0, 4.0, 4.0, 2.0, 2.0, 3.0, 2.0, 3.0, 5.0, 1.0, 4.0, 3.0, 3.5, 3.0, 2.5, 5.0, 4.0, 2.0, 4.0, 5.0, 4.5, 4.0, 5.0, 3.0, 5.0, 4.0, 4.0, 5.0, 1.0, 4.0, 4.0, 3.0, 1.0, 2.0],
[2.0, 3.0, 3.0, 2.0, 4.0, 3.0, 3.0, 4.0, 3.0, 4.0, 5.0, 3.0, 1.0, 4.0, 3.0, 1.5, 4.5, 2.5, 3.0, 2.0, 2.0, 2.0, 2.0, 2.0, 4.0, 5.0, 1.0, 2.0, 4.0, 3.0, 3.5, 3.0, 3.0, 3.0, 2.0, 2.0, 2.0, 2.0, 2.0, 5.0, 1.0, 3.0,
3.0, 3.0, 3.0, 2.5, 5.0, 3.0, 2.0, 3.0, 4.5, 3.5, 2.0, 4.0, 2.0, 5.0, 2.5, 2.0, 5.0, 1.0, 4.0, 4.0, 2.0, 1.0, 1.0],
[1.0, 2.0, 2.0, 2.0, 3.0, 3.0, 4.0, 4.0, 2.0, 4.0, 3.0, 2.0, 1.0, 4.0, 3.0, 1.0, 3.0, 2.0, 2.0, 2.0, 1.0, 2.0, 2.0, 1.0, 3.0, 5.0, 1.0, 2.0, 3.0, 2.0, 2.0, 3.0, 3.0, 4.0, 2.0, 1.0, 2.0, 2.0, 2.5, 4.0, 1.0, 4.0, 2.0, 2.0, 2.0, 1.0, 4.0, 2.0, 1.0, 1.5, 3.0, 2.0, 0.5, 2.0, 1.0, 2.5, 1.5, 0.5, 5.0, 0.5, 2.0, 2.0, 1.0, 0.5, 1.0],
[2.0, 2.0, 2.5, 4.0, 2.0, 2.0, 2.0, 2.5, 2.0, 2.5, 3.5, 3.0, 0.0, 4.0, 3.5, 1.0, 2.0, 1.0, 1.5, 2.0, 2.5, 2.0, 2.0, 2.0, 4.0, 2.0, 2.0, 1.0, 4.0, 2.0, 4.0, 5.0, 2.0, 2.0, 1.0, 4.0, 1.0, 2.0, 3.0, 2.0, 2.0, 3.0, 3.0, 1.0, 2.0, 2.0, 4.0, 3.0, 2.0, 4.0, 4.0, 2.0, 3.0, 2.0, 3.0, 1.0, 2.0, 1.0, 3.0, 0.0, 5.0, 3.0, 4.0, 0.0, 0.0],
[1.0, 1.0, 2.0, 1.0, 4.0, 1.0, 3.0, 1.0, 1.0, 0.5, 0.5, 0.5, 0.0, 0.5, 1.0, 0.0, 2.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.5, 1.0, 0.5, 0.0, 1.0, 0.0, 0.0, 2.0, 1.0, 2.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.5, 1.0, 1.0, 0.0, 0.5, 0.5, 0.0, 1.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.5, 1.0, 0.0, 1.5, 1.5, 0.0, 1.5, 0.0, 1.0, 0.0, 2.5, 1.0, 0.0, 0.0, 0.0]],


 "avgAScore":[2.4,3.45,3.122],
   "avgBScore":[2.21,3.35,3.512],
   "avgCScore":[2.45,3.13,4.10],   "avgOverallScore":[2.4,3.45,3.122],
}







questions_ese_1={
   "questions":["Develop a one-dimensional time independent Schrodinger wave equation for matter waves.","What is de Broglie’s hypothesis? Name the experiment which proves the validity of this hypothesis. Show that the velocity of a particle is equal to the group velocity of the associated matter waves.","A proton with energy E is incident on a barrier of height Vo and barrier thickness L, its transmission coefficient is TP. If this proton is replaced by an alpha particle, its transmission coefficient is T’ P. Express T’ P in terms of TP.","A particle is moving in a one-dimensional box of width 10 Å. Calculate the probability of finding the particle within an interval of 5 Å at the center of the box when the particle is in its lowest state.","A plane transmission grating has 6000 lines/cm. Calculate the highest order spectrum which can be observed with a light of wavelength 4000Å and the diffraction angle for the third order spectrum.","Derive the eigen values (En) and eigen functions (𝛙n) for a particle confined in an infinite potential well."],
   "marks":[5,5,5,5,5,15],
   "category":["theory","theory","numerical","numerical","numerical","numerical"],
   "topic":["Schrodinger's time dependent wave equation, time independent wave equation","wave packet, group velocity and phase velocity","Application of time-independent Schrodinger equation - Particle trapped in one dimensional box and Potential barrier (Tunnelling), Harmonic oscillator (qualitative)","Application of time-independent Schrodinger equation - Particle trapped in one dimensional box and Potential barrier (Tunnelling), Harmonic oscillator (qualitative),N,Intrinsic and extrinsic semiconductors","Electron diffraction experiment","Application of time-independent Schrodinger equation - Particle trapped in one dimensional box and Potential barrier (Tunnelling), Harmonic oscillator (qualitative)"],
   "A_Scores":[[5.0, 3.0, 3.0, 2.0, 2.0, 4.0, 5.0, 3.0, 5.0, 5.0, 5.0, 5.0, 3.0, 3.0, 2.0, 5.0, 4.0, 4.0, 4.0, 4.0, 4.0, 2.0, 5.0, 5.0, 5.0, 2.0, 4.0, 2.0, 1.0, 2.0, 4.0, 4.0, 1.0, 4.0, 4.0, 4.0, 5.0, 2.0, 1.0, 2.0, 5.0, 4.0, 5.0, 5.0, 2.0, 5.0, 4.0, 5.0, 5.0, 5.0, 4.0, 5.0, 4.0, 4.0, 5.0, 4.0, 5.0, 4.0, 4.0, 5.0, 4.0, 4.0, 5.0, 4.0, 3.0, 0.0, 5.0, 5.0, 5.0, 3.0],
[5.0, 3.0, 2.0, 2.0, 2.0, 4.0, 5.0, 3.0, 4.0, 5.0, 4.0, 4.0, 3.0, 2.0, 2.0, 4.0, 5.0, 4.0, 4.0, 4.0, 4.0, 2.0, 4.0, 5.0, 5.0, 2.0, 4.0, 2.0, 1.0, 2.0, 3.0, 4.0, 1.0, 3.0, 4.0, 4.0, 5.0, 2.0, 1.0, 2.0, 5.0, 3.0, 4.0, 5.0, 2.0, 4.0, 4.0, 5.0, 5.0, 5.0, 4.0, 5.0, 4.0, 4.0, 5.0, 4.0, 5.0, 4.0, 4.0, 5.0, 4.0, 4.0, 5.0, 4.0, 3.0, 0.0, 5.0, 4.0, 5.0, 3.0],
[4.0, 2.0, 3.0, 1.0, 2.0, 3.0, 2.0, 3.0, 4.0, 5.0, 2.0, 2.0, 3.0, 2.0, 1.0, 4.0, 2.0, 4.0, 4.0, 2.0, 3.0, 0.0, 4.0, 3.0, 3.0, 2.0, 3.0, 0.0, 0.0, 1.0, 1.0, 2.0, 0.0, 2.0, 1.0, 3.0, 5.0, 3.0, 0.0, 2.0, 4.0, 1.0, 1.0, 3.0, 2.0, 3.0, 3.0, 5.0, 5.0, 5.0, 3.0, 5.0, 5.0, 3.0, 1.0, 3.0, 4.0, 2.0, 5.0, 4.0, 4.0, 3.0, 3.0, 2.0, 2.0, 0.0, 4.0, 3.0, 5.0, 0.0],[4.0, 2.0, 3.0, 1.0, 3.0, 3.0, 3.0, 3.0, 3.0, 4.0, 2.0, 2.0, 2.0, 2.0, 1.0, 4.0, 2.0, 4.0, 4.0, 2.0, 3.0, 0.0, 4.0, 3.0, 3.0, 2.0, 2.0, 0.0, 0.0, 1.0, 1.0, 2.0, 0.0, 2.0, 1.0, 3.0, 5.0, 2.0, 0.0, 2.0, 4.0, 1.0, 0.0, 3.0, 2.0, 3.0, 3.0, 5.0, 5.0, 5.0, 3.0, 5.0, 5.0, 3.0, 1.0, 3.0, 4.0, 2.0, 5.0, 4.0, 4.0, 3.0, 2.0, 1.0, 2.0, 0.0, 4.0, 3.0, 5.0, 0.0],
[2.0, 2.0, 1.0, 0.0, 3.0, 1.0, 2.0, 1.0, 3.0, 3.0, 1.0, 2.0, 2.0, 1.0, 1.0, 2.0, 2.0, 2.0, 4.0, 1.0, 2.0, 0.0, 4.0, 4.0, 2.0, 1.0, 3.0, 0.0, 0.0, 1.0, 1.0, 2.0, 0.0, 2.0, 1.0, 2.0, 4.0, 2.0, 0.0, 2.0, 4.0, 0.0, 1.0, 2.0, 1.0, 2.0, 3.0, 4.0, 5.0, 5.0, 2.0, 5.0, 5.0, 2.0, 1.0, 3.0, 4.0, 1.0, 4.0, 4.0, 4.0, 3.0, 3.0, 2.0, 2.0, 0.0, 2.0, 2.0, 4.0, 0.0],
[15.0, 4.0, 14.0, 0.0, 13.0, 0.0, 15.0, 0.0, 14.0, 0.0, 8.0, 12.0, 5.0, 2.0, 0.0, 14.0, 13.0, 8.0, 14.0, 14.0, 14.0, 0.0, 14.0, 14.0, 14.0, 1.0, 10.0, 0.0, 0.0, 9.0, 2.0, 12.0, 0.0, 14.0, 5.0, 7.0, 14.0, 3.0, 10.0, 2.0, 15.0, 0.0, 0.0, 14.0, 0.0, 14.0, 14.0, 15.0, 14.0, 15.0, 13.0, 14.0, 9.0, 9.0, 13.0, 11.0, 11.0, 3.0, 15.0, 15.0, 13.0, 14.0, 15.0, 13.0, 10.0, 0.0, 12.0, 12.0,15.0, 4.0]],

 "B_Scores":[[5.0, 4.0, 3.0, 2.0, 5.0, 4.0, 4.0, 3.0, 5.0, 5.0, 4.0, 3.0, 2.0, 4.0, 4.0, 2.0, 5.0, 5.0, 3.0, 4.0, 4.0, 1.0, 5.0, 5.0, 3.0, 3.0, 4.0, 5.0, 4.0, 4.0, 0.0, 1.0, 4.0, 4.0, 5.0, 3.0, 4.0, 4.0, 5.0, 4.0, 4.0, 4.0, 4.0, 4.0, 3.0, 4.0, 4.0, 4.0, 4.0, 4.0, 2.0, 5.0, 1.0, 4.0, 1.0, 5.0, 4.0, 4.0, 4.0, 5.0, 5.0, 2.0, 4.0, 4.0, 4.0, 5.0, 2.0, 5.0, 4.0, 5.0],
            [5.0, 4.0, 3.0, 2.0, 4.0, 4.0, 4.0, 3.0, 5.0, 5.0, 4.0, 2.0, 2.0, 4.0, 4.0, 2.0, 5.0, 4.0, 3.0, 4.0, 4.0, 1.0, 5.0, 5.0, 3.0, 2.0, 4.0, 5.0, 4.0, 4.0, 0.0, 1.0, 4.0, 4.0, 5.0, 3.0, 4.0, 4.0, 5.0, 4.0, 4.0, 4.0, 4.0, 4.0, 3.0, 4.0, 4.0, 4.0, 4.0, 4.0, 2.0, 5.0, 1.0, 3.0, 1.0, 5.0, 4.0, 4.0, 4.0, 5.0, 5.0, 2.0, 4.0, 4.0, 4.0, 5.0, 2.0, 5.0, 5.0, 3.0],
            [2.0, 3.0, 5.0, 5.0, 3.0, 2.0, 2.0, 4.0, 4.0, 4.0, 4.0, 3.0, 2.0, 3.0, 3.0, 1.0, 4.0, 3.0, 1.0, 3.0, 3.0, 0.0, 4.0, 5.0, 2.0, 2.0, 3.0, 2.0, 3.0, 3.0, 0.0, 0.0, 4.0, 2.0, 3.0, 2.0, 3.0, 4.0, 5.0, 4.0, 3.0, 2.0, 2.0, 4.0, 2.0, 2.0, 3.0, 4.0, 4.0, 3.0, 1.0, 5.0, 2.0, 1.0, 0.0, 4.0, 4.0, 5.0, 4.0, 4.0, 4.0, 2.0, 2.0, 4.0, 2.0, 4.0, 5.0, 4.0, 2.0, 2.5],
            [2.0, 3.0, 5.0, 5.0, 3.0, 2.0, 2.0, 4.0, 4.0, 4.0, 4.0, 3.0, 1.0, 3.0, 2.0, 1.0, 3.0, 3.0, 1.0, 2.0, 3.0, 1.0, 4.0, 4.0, 2.0, 2.0, 2.0, 1.0, 4.0, 3.0, 0.0, 0.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 5.0, 4.0, 3.0, 1.0, 3.0, 3.0, 2.0, 2.0, 3.0, 4.0, 4.0, 3.0, 1.0, 5.0, 1.0, 1.0, 0.0, 4.0, 4.0, 5.0, 3.0, 4.0, 4.0, 2.0, 2.0, 3.0, 2.0, 4.0, 5.0, 4.0, 2.0, 2.5],
            [1.0, 2.0, 4.0, 4.0, 2.0, 1.0, 2.0, 4.0, 3.0, 3.0, 4.0, 3.0, 3.0, 4.0, 3.0, 0.0, 4.0, 2.0, 1.0, 2.0, 2.0, 0.0, 4.0, 5.0, 2.0, 2.0, 2.0, 2.0, 2.0, 3.0, 0.0, 0.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 4.0, 3.0, 2.0, 1.0, 2.0, 3.0, 2.0, 3.0, 3.0, 3.0, 4.0, 2.0, 1.0, 4.0, 1.0, 1.0, 0.0, 4.0, 3.0, 4.0, 3.0, 3.0, 3.0, 2.0, 2.0, 3.0, 1.0, 4.0, 4.0, 3.0, 2.0, 2.5],
            [13.0, 1.0, 8.0, 2.0, 13.0, 5.0, 11.0, 10.0, 14.0, 15.0, 13.0, 0.0, 2.0, 14.0, 9.0, 5.0, 10.0, 9.0, 3.0, 2.0, 0.0, 0.0, 14.0, 15.0, 2.0, 0.0, 15.0, 15.0, 10.0, 11.0, 0.0, 0.0, 9.0, 13.0, 14.0, 9.0, 14.0, 4.0, 14.0, 15.0, 14.0, 12.0, 9.0, 2.0, 9.0, 9.0, 13.5, 12.0, 10.0, 3.0, 0.0, 14.0, 0.0, 10.0, 0.0, 14.0, 15.0, 14.0, 14.0, 14.0, 14.0, 1.0, 13.0, 11.0, 15.0, 15.0, 10.0, 15.0, 11.0, 7.0] ] ,


"C_Scores":[[3.0, 5.0, 5.0, 4.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 4.0, 1.0, 5.0, 5.0, 3.0, 5.0, 4.0, 5.0, 4.0, 3.0, 4.0, 4.5, 3.0, 5.0, 5.0, 3.0, 2.0, 5.0, 4.0, 4.0, 5.0, 5.0, 5.0, 3.0, 3.0, 4.0, 3.0, 4.0, 5.0, 3.0, 5.0, 4.0, 4.0, 4.0, 3.5, 5.0, 5.0, 3.0, 5.0, 5.0, 5.0, 5.0, 5.0, 4.0, 5.0, 3.0, 5.0, 5.0, 2.0, 5.0, 5.0, 5.0, 2.0, 3.0],
[1.0, 4.0, 4.0, 2.0, 5.0, 5.0, 4.0, 5.0, 4.0, 5.0, 5.0, 4.0, 1.0, 5.0, 4.0, 2.0, 5.0, 4.0, 4.0, 3.0, 2.0, 3.0, 3.0, 2.0, 5.0, 5.0, 2.0, 2.0, 5.0, 4.0, 4.0, 4.0, 4.0, 4.0, 3.0, 2.0, 4.0, 3.0, 4.0, 5.0, 2.5, 4.0, 4.0, 4.0, 4.0, 2.5, 5.0, 4.0, 3.0, 5.0, 5.0, 5.0, 5.0, 5.0, 4.0, 5.0, 4.5, 5.0, 5.0, 1.0, 4.0, 4.0, 4.0, 2.0, 3.0],
[2.0, 2.0, 2.5, 4.0, 2.0, 2.0, 2.0, 2.5, 2.0, 2.5, 3.5, 3.0, 0.0, 4.0, 3.5, 1.0, 2.0, 2.0, 1.5, 2.0, 2.5, 2.0, 2.0, 2.0, 4.0, 2.0, 2.0, 1.0, 4.0, 2.0, 4.0, 5.0, 2.0, 2.0, 3.0, 2.0, 5.0, 3.0, 5.0, 4.0, 0.0, 5.0, 2.0, 2.0, 0.0, 2.0, 5.0, 3.0, 2.0, 4.0, 4.0, 2.0, 3.0, 3.0, 3.0, 5.0, 4.0, 1.0, 3.0, 0.0, 5.0, 5.0, 5.0, 0.0, 0.5],
[2.0, 2.0, 2.5, 4.0, 2.0, 2.0, 2.0, 2.5, 2.0, 2.5, 3.5, 3.0, 0.0, 4.0, 3.5, 1.0, 2.0, 1.0, 1.5, 2.0, 2.5, 2.0, 2.0, 2.0, 4.0, 2.0, 2.0, 1.0, 4.0, 2.0, 4.0, 5.0, 2.0, 2.0, 3.0, 4.0, 4.0, 2.0, 5.0, 4.0, 0.0, 2.0, 1.0, 2.0, 0.0, 2.0, 5.0, 3.0, 2.0, 4.0, 4.0, 2.0, 3.0, 4.0, 3.0, 1.0, 4.0, 1.0, 4.0, 0.0, 5.0, 3.0, 5.0, 0.0, 0.0],
[1.0, 2.0, 2.0, 4.0, 2.0, 1.0, 2.0, 2.5, 1.0, 2.5, 3.5, 3.0, 0.0, 4.0, 3.5, 1.0, 2.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 4.0, 2.0, 1.0, 1.0, 4.0, 2.0, 4.0, 4.0, 2.0, 2.0, 2.0, 1.0, 2.0, 2.0, 2.0, 1.0, 0.25, 0.5, 2.0, 0.5, 1.0, 1.0, 3.0, 2.0, 2.0, 1.0, 1.0, 2.0, 3.0, 2.0, 1.0, 2.0, 3.0, 0.0, 5.0, 0.0, 3.0, 2.0, 5.0, 0.0, 0.0],
[4.0, 10.0, 14.0, 13.0, 7.0, 9.0, 8.0, 14.0, 0.5, 13.0, 13.0, 8.0, 0.0, 12.0, 14.0, 6.0, 9.0, 10.0, 4.0, 2.0, 10.0, 1.0, 6.0, 9.0, 2.0, 7.0, 13.0, 6.0, 0.0, 6.0, 10.0, 14.0, 6.0, 0.0, 3.0, 6.0, 9.0, 0.0, 0.0, 13.0, 0.0, 13.0, 10.0, 10.0, 1.0, 2.0, 14.0, 15.0, 8.0, 13.0, 12.0, 4.0, 0.0, 14.0, 13.0, 12.0, 2.0, 4.0, 1.0, 0.0, 9.0, 14.0, 13.0, 0.0, 1.0]],




 "avgAScore":[2.4,3.45,3.122],
   "avgBScore":[2.21,3.35,3.512],
   "avgCScore":[2.45,3.13,4.10],   "avgOverallScore":[2.4,3.45,3.122],
}



color_gradients = {
    "A": "rgb(255, 0, 0)",  # Red
    "B": "rgb(0, 255, 0)",  # Green
    "C": "rgb(0, 0, 255)"   # Blue
}




def students_callbacks(app):
    @app.callback(
        [Output('exam-type-store', 'data'), Output('module-store', 'data')],
        [Input('ise-button', 'n_clicks'), Input('mse-button', 'n_clicks'), Input('ese-button', 'n_clicks'),
        Input('performance-button', 'n_clicks'),Input('module1-button', 'n_clicks'), Input('module2-button', 'n_clicks'), Input('module3-button', 'n_clicks'), Input('module4-button', 'n_clicks')],
        [State('exam-type-store', 'data'), State('module-store', 'data')]
    )
    def update_stores(ise_clicks, mse_clicks, ese_clicks, module1_clicks, module2_clicks, module3_clicks, module4_clicks,performance_clicks, exam_type, module):
        ctx = dash.callback_context
        if not ctx.triggered:
            return exam_type, module
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if button_id in ['performance-button']:
                exam_type = 'Performance'
            if button_id in ['ise-button', 'mse-button', 'ese-button']:
                exam_type = button_id.split('-')[0].upper()
            if button_id in ['module1-button', 'module2-button', 'module3-button', 'module4-button']:
                module = button_id.split('-')[0][-1]
            return exam_type, module
    


    @app.callback(
        Output('main-container', 'children'),
        [Input('exam-type-store', 'data'), Input('module-store', 'data')]
    )
    
    def update_main_container(exam_type, module):
        if exam_type == 'Performance':
            weightage_module=["40%","30%","30%"]
            category_module={"theory":"70%","numerical":"30%"}
            weightage_plot = dcc.Graph(
                figure={
                    'data': [
                        {
                            'labels': ['Module 1', 'Module 2', 'Module 3'],
                            'values': [30, 30, 40],
                            'type': 'pie',
                            'marker': {'colors': ['skyblue', 'lightgreen', 'orange']}
                        }
                    ],
                    'layout': {
                        'plot_bgcolor': 'rgba(0, 0, 0, 0)',  # Transparent background
                        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                        'title': 'Weightage of Each Module in ESE',
                        'font': {'color': 'white'}
                    }
                }
            )
            #plot the same for category_module
            category_plot=dcc.Graph(
                figure={

                    'data': [

                        {
                            'labels': ['Theory', 'Numerical'],
                            'values': [70, 30],
                            'type': 'pie',
                            'marker': {'colors': ['skyblue', 'lightgreen']}
                        }
                    ],
                    'layout': {
                        'plot_bgcolor': 'rgba(0, 0, 0, 0)',  # Transparent background
                        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                        'title': 'Category Wise Weightage in ESE',
                        'font': {'color': 'white'}
                    }
                }
            )

            return html.Div([
                html.P("ESE TOMORROW?? DON't FORGET TO SOLVE MODULE 1 NUMERICALLLSS!!!  ", className=" bg-red-500 text-xl text-yellow-100"),
                html.H1("Overall Module Wise weightage in ESE", className="text-4xl font-bold text-yellow-400"),
                #plot a pie chart of weightage_modul                
                weightage_plot,
                html.H1("Category Wise Weightage in ESE", className="text-4xl font-bold text-yellow-400"),
                #plot a pie chart of category_module
                category_plot,
                
            ], className="flex ml-32 flex-col items-center justify-center h-full")
        else:
           
            weightage_section = html.Div([
                html.H3("Weightage", className="text-xl font-bold text-yellow-400"),
                html.P(f"{weightage.get(exam_type.lower()+module)}", className="text-4xl font-bold text-yellow-100")
            ], className='flex flex-col border border-gray-700 drop-shadow-2xl justify-center bg-gray-800 h-1/3 w-full mb-4 p-4 rounded-md')

            topics_section = html.Div([
                html.H2("Topics", className="text-2xl font-bold text-yellow-400"),
                html.Div([
                    html.Div([
                        html.P(f"{topic[0]}", className="text-lg text-yellow-100"),
                        html.P(f"{topic[1]}", className="text-lg text-yellow-100")
                    ], className="mt-2 flex bg-gray-900 p-1 px-4 rounded-md justify-between")
                    for topic in topics.get(exam_type.lower()+module)], className="flex flex-col gap-2")
            ], className='rounded-md bg-gray-800 w-full border border-black mt-4 p-4')

            category_section = html.Div([
                html.H2("Category", className="text-2xl font-bold text-yellow-400"),
                html.Div([
                    html.Div([
                        html.P(f"{cat[0]}", className="text-lg text-yellow-100"),
                        html.P(f"{cat[1]}", className="text-lg text-yellow-100")
                    ], className="mt-2 flex bg-gray-900 p-1 px-4 rounded-md justify-between")
                    for cat in category.get(exam_type.lower()+module)], className="flex flex-col gap-2")
            ], className='rounded-md bg-gray-800 w-full mt-8 border-2 border-black drop-shadow-2xl  p-4')

            left_section = html.Div(className="flex flex-col w-1/2 ", children=[
                weightage_section,
                topics_section,
                category_section
            ])

            ise_2_section = html.Div([
                #plot graph of topics vs score for ise_exam_type_module
                dcc.Graph(figure=fig),
            ], className='flex p-4 bg-gray-800 w-full rounded-md')

            question_ise1_section = html.Div([
                html.H3(f"{exam_type} Exam Questions for Module {module}"),
                html.P(f"This is {exam_type} exam questions for Module {module}. Add your content here.")
            ])
            question_ise3_section = html.Div([
                html.H3(f"{exam_type} Exam Questions for Module {module}"),
                html.P(f"This is {exam_type} exam questions for Module {module}. Add your content here.")
            ])
            question_ise4_section = html.Div([
                html.H3(f"{exam_type} Exam Questions for Module {module}"),
                html.P(f"This is {exam_type} exam questions for Module {module}. Add your content here.")
            ])
            question_mse1_section = html.Div([
                #create a dropdown for questions in questions_mse_1 and display the selected question
                
                html.Label("Select Question"),
                dcc.Dropdown(
                    id='question-dropdown',
                    options=[{'label': f"Question {i+1}", 'value': i} for i in range(len(questions_mse_1['questions']))],
                    value=0
                ),
                html.Div(id='question-info')


            ])
        
            question_mse_2_section = html.Div([
            ])
            question_mse_3_section = html.Div([
            ])
            question_mse_4_section = html.Div([
                #create a dropdown for questions in questions_mse_4 and display the selected question
                
                html.Div([
            html.Label("Select Question Number:"),
            dcc.Dropdown(
                id='question-dropdown',
                options=[{'label': f"Question {i+1}", 'value': i} for i in range(len(questions_mse_4['questions']))],
                value=0,  # Default value
                className='mt-4',
            )
            
        ], className='mt-4'),
        html.Div(id='question-info')

            ])

            question_ese1_section=html.Div([
                html.Div([
            html.Label("Select Question Number:"),
            dcc.Dropdown(
                id='question-dropdown',
                options=[{'label': f"Question {i+1}", 'value': i} for i in range(len(questions_mse_4['questions']))],
                value=0,  # Default value
                className='mt-4',
            )
            
        ], className='mt-4'),
        html.Div(id='question-info')
            ])
            question_ese2_section=html.Div([
                html.Div([
            html.Label("Select Question Number:"),
            dcc.Dropdown(
                id='question-dropdown',
                options=[{'label': f"Question {i+1}", 'value': i} for i in range(len(questions_mse_4['questions']))],
                value=0,  # Default value
                className='mt-4',
            )
            
        ], className='mt-4'),
        html.Div(id='question-info')
            ])
            question_ese3_section=html.Div([
                html.Div([
            html.Label("Select Question Number:"),
            dcc.Dropdown(
                id='question-dropdown',
                options=[{'label': f"Question {i+1}", 'value': i} for i in range(len(questions_mse_4['questions']))],
                value=0,  # Default value
                className='mt-4',
            )
            
        ], className='mt-4'),
        html.Div(id='question-info')
            ])
            question_ese4_section=html.Div([
                html.H3(f"{exam_type} Exam Questions for Module {module}"),
                html.P(f"This is {exam_type} exam questions for Module {module}. Add your content here.")
            ])



            questions_section = html.Div([
        ise_2_section if exam_type == "ISE" and module == "2" else html.Div([
            
            question_ise1_section if exam_type == "ISE" and module == "1" else html.Div(),
            question_ise3_section if exam_type == "ISE" and module == "3" else html.Div(),
            question_ise4_section if exam_type == "ISE" and module == "4" else html.Div(),
            question_mse1_section if exam_type == "MSE" and module == "1" else html.Div(),
            question_mse_2_section if exam_type == "MSE" and module == "2" else html.Div(),
            question_mse_3_section if exam_type == "MSE" and module == "3" else html.Div(),
            question_mse_4_section if exam_type == "MSE" and module == "4" else html.Div(),
            question_ese1_section if exam_type == "ESE" and module == "1" else html.Div(),
            question_ese2_section if exam_type == "ESE" and module == "2" else html.Div(),
            question_ese3_section if exam_type == "ESE" and module == "3" else html.Div(),
            question_ese4_section if exam_type == "ESE" and module == "4" else html.Div(),

        ])
    ], className='flex p-4 bg-gray-800 w-full rounded-md')


            return html.Div([left_section, questions_section], className='flex flex-row gap-10')

@app.callback(
    Output('question-info', 'children'),
    [Input('question-dropdown', 'value')],
    [State('module-store', 'data')],
    [State('exam-type-store', 'data')]
)
def update_question_info(selected_question,module,exam_type):
    df = globals()[f'questions_{exam_type.lower()}_{module}']
    question = df['questions'][selected_question]
    category = df['category'][selected_question]
    avg_marks = df['avgOverallScore'][selected_question]
    marks = df['marks'][selected_question]


    a_scores_trace = go.Scatter(y=df['A_Scores'], mode='markers', name='A Scores', marker=dict(color='rgba(0, 255, 0, 0.8)'))
    b_scores_trace = go.Scatter(y=df['B_Scores'], mode='markers', name='B Scores', marker=dict(color='rgba(255, 0, 0, 0.8)'))
    c_scores_trace = go.Scatter(y=df['C_Scores'], mode='markers', name='C Scores', marker=dict(color='rgba(0, 0, 255, 0.8)'))

# Create a line trace for the average marks
    avg_marks_trace = go.Scatter(y=[avg_marks]*len(df), mode='lines', name='Average Marks', line=dict(color='rgba(255,255,0,0)', width=4))

# Create a dcc.Graph component with the scatter plot
    scatter_plot = dcc.Graph(
        figure=go.Figure(
            data=[a_scores_trace, b_scores_trace, c_scores_trace, avg_marks_trace],
            layout=go.Layout(
                plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
                paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
                font=dict(color='rgba(255, 255, 255, 0.8)'),  # White text
                xaxis=dict(gridcolor='rgba(255, 255, 255, 0.2)'),  # Light grid lines
                yaxis=dict(gridcolor='rgba(255, 255, 255, 0.2)'),  # Light grid lines
            )
        )
    )


    return html.Div([
        html.P([html.Span('Question: ', className='font-bold text-yellow-300 text-xl'), html.Span(question, className='text-yellow-100 text-xl')]),
        scatter_plot,  # Add the scatter plot here
        html.P([html.Span('Marks: ', className='font-bold text-yellow-300'), html.Span(marks, className='text-yellow-100')]),
        html.P([html.Span('Category: ', className='font-bold text-blue-300'), html.Span(category, className='text-blue-100')]),
        html.P([html.Span('Average Marks: ', className='font-bold text-pink-300'), html.Span(avg_marks, className='text-pink-100')]),
        html.P([html.Span('Difficulty: ', className='font-bold text-yellow-300'), html.Span("hard" if avg_marks<(marks//2) else "easy", className='text-yellow-100')]),
    ], className="bg-gray-800 mt-4 p-2 rounded-md")

students_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True, port=5000)
