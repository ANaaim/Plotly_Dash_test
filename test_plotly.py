#test
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
# Create random data with numpy
import numpy as np
import random
np.random.seed(1)

def create_random_data(name_article,name_joint,name_dof,Angle_or_Translation, name_movement,nb_frame,initialize = False):
    
    if initialize:
        df = pd.DataFrame({'Article':[],
                        "Joint":[],
                        "Angle_Translation" : [],
                            'DoF':[],
                            'Mvt' : [],
                            'Humerothoracic_angle':[],
                            'Value':[]})
    else:
        random_x = np.linspace(0, 120, nb_frame)
        random_y0 = np.random.randn(nb_frame) + 5
        df = pd.DataFrame({'Article':[name_article]*nb_frame,
                    "Joint":[name_joint]*nb_frame,
                    "Angle_Translation" : [Angle_or_Translation]*nb_frame,
                    'DoF': [name_dof]*nb_frame,
                    'Mvt' : [name_movement]*nb_frame,
                    'Humerothoracic_angle':random_x,
                    'Value':random_y0})
        
            
    return df
## Create traces
#fig = go.Figure()
#fig.add_trace(go.Scatter(x=random_x, y=random_y0,
#                    mode='lines',
#                    name='lines'))
#fig.add_trace(go.Scatter(x=random_x, y=random_y1,
#                    mode='lines+markers',
#                    name='lines+markers'))
#fig.add_trace(go.Scatter(x=random_x, y=random_y2,
#                    mode='markers', name='markers'))
#
#fig.show()

def Generation_Full_Article (nb_article):
    nb_joint_by_article = [1,2,3]
    nb_dof_by_joint_angle = [0,1,2,3]
    nb_dof_by_joint_translation = [0,1,2,3]
    nb_movement_by_article = [1,2,3,4]

    name_joints = ['Humerothocracic angle','Glenohumeral angle','Scapulothoracic angle']
    name_movements = ['Mouvement_1','Mouvement_2','Mouvement_3','Mouvement_4']
    DoF_translation = ['X','Y','Z']
    DoF_angle = ['Flexion','Abduction','External rotation']
    nb_frame = [6,20,30]
    df = create_random_data('','','','','',6,initialize = True)
    for i in range(nb_article):
        name_article = 'Article_'+str(i)
        final_nb_frame = random.choice(nb_frame)
        final_nb_joint = random.choice(nb_joint_by_article)
        final_list_joint = random.sample(name_joints,final_nb_joint)
        
        final_number_dof_angle = random.choice(nb_dof_by_joint_angle)
        final_dof_angle = random.sample(DoF_angle,final_number_dof_angle)

        final_number_dof_translation = random.choice(nb_dof_by_joint_translation)
        final_dof_angle_translation = random.sample(DoF_translation,final_number_dof_translation)

        final_number_movement = random.choice(nb_movement_by_article)
        final_list_movement = random.sample(name_movements,final_number_movement)
        
        for name_joint in final_list_joint:
            for name_movement in final_list_movement:
                for name_dof in final_dof_angle:
                    df_temp = create_random_data(name_article,name_joint,name_dof,'Angle',name_movement,final_nb_frame)    
                    df = pd.concat([df,df_temp])
                for name_dof in final_dof_angle_translation:
                    df_temp = create_random_data(name_article,name_joint,name_dof,'Translation',name_movement,final_nb_frame)    
                    df = pd.concat([df,df_temp])

    return df

toto = Generation_Full_Article(10)

app = Dash(__name__)

# Read directly from the dataframe the different list aka extract the different unique values
# I dont yet understand what value correspond ? 

app.layout = html.Div([
    html.H4('Kinematics of the shoulder joint'),
    dcc.Graph(id="graph"),
    dcc.Checklist(
        id='Mouvement',
        options=sorted([i for i in toto.Mvt.unique()]),
        value=sorted([i for i in toto.Mvt.unique()]),
        inline=True
    ),
    dcc.Checklist(
        id='Joint',
        options= sorted([i for i in toto.Joint.unique()]),
        value=sorted([i for i in toto.Joint.unique()]),
        inline=True
    ),
    dcc.Dropdown(options= sorted([i for i in toto.Angle_Translation.unique()]),
                value=sorted([i for i in toto.Angle_Translation.unique()])[0],
                id='Angle_Translation'),

])

# Add a common X Axis and Title

@app.callback(
    Output("graph", "figure"), 
    Input('Mouvement', "value"),
    Input('Joint', "value"),
    Input('Angle_Translation',"value")
    )
def update_line_chart(Mvt,Joint,Angle_Translation):
    df = toto # replace with your own data source
    mask_mvt = df.Mvt.isin(Mvt)
    mask_joint = df.Joint.isin(Joint)
    # We have to put Angle translation in a list because it is a string
    mask_angle_translation = df.Angle_Translation.isin([Angle_Translation])
    if Angle_Translation == 'Angle':
        list_orga = ['Flexion','Abduction','External rotation']
    else:
        list_orga = ['X','Y','Z']
    fig = px.line(df[mask_mvt & mask_joint & mask_angle_translation], 
        x="Humerothoracic_angle", y="Value",color='Article',facet_row='Joint',facet_col='DoF',
        category_orders={"DoF": list_orga})
    # Allow to remove the "Mvt=" in the legend
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    
    fig.update_layout(
    autosize=True,
    width=1250,
    height=900,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    ))
    return fig


app.run_server(debug=True)