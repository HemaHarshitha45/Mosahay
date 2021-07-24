import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import glob
import random
import seaborn as sns
sns.set_style('whitegrid')
from geopy.geocoders import Nominatim
import os
import geopandas as gpd
import descartes
import json
import pickle
import ast
from geopy.distance import geodesic

from bokeh.io import curdoc, output_notebook
from bokeh.models import  HoverTool
from bokeh.layouts import widgetbox, row, column
from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure,save
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar,Column, Button
from bokeh.palettes import brewer
from bokeh.models.widgets import Dropdown, Select, TextInput
from math import pi

from bokeh.palettes import Category20c
from bokeh.transform import cumsum
from bokeh.models import ColumnDataSource, CustomJS, Slider

# ### Reading all the required csv files
skill_df=pd.read_csv(r"data/master_skill.csv")
df=pd.read_csv(r"data/Uttar_Pradesh/Skill_to_district.csv")
dist_df=pd.read_csv(r"data/Uttar_Pradesh/Distance_among_districts.csv")
list_df=pd.read_csv(r"data/Uttar_Pradesh/DistrictsFinal.csv")
skill_list=['Choose a Skill']
skill_list.extend(skill_df.sort_values(by='Skills')['Skills'].tolist())

# ### Importing the shape file of Uttar Pradesh
mapdf=gpd.read_file('data/Uttar_Pradesh/uttarpradesh_district/uttarpradesh_district.shp')
mapdf=mapdf=mapdf[['district','geometry']]


# ### Changes to the shape file as per the given data
mapdf.replace('Faizabad','Ayodhya',inplace=True)
mapdf.replace('Lakhimpur Kheri','Kheri',inplace=True)
#mapdf.replace('Sant Ravi Das Nagar(Bhadohi)','Sant Ravidas Nagar',inplace=True)
mapdf.replace('Allahabad','Prayagraj',inplace=True)
mapdf.replace('Rae Bareli','Raebareli',inplace=True)
mapdf.replace('Mahamaya Nagar','Hathras',inplace=True)
mapdf.replace('Shrawasti','Shravasti',inplace=True)
mapdf.district=mapdf.district.str.lower()
mapdf.district=mapdf.district.str.replace(" ","")
mapdf.district=mapdf.district.str.replace('santkabirnagar','santkabeernagar')
mapdf.replace('santravidasnagar(bhadohi)','santravidasnagar',inplace=True)

# ### Function to generate the required output
def calc_area(list):
    sum=0
    for i in list:
        sum = sum + list_df[list_df['District']==i]['Area'].values
    return int(sum)
    

#The function takes skill and required number of workers as input
#The function outputs two lists: the districts and their corresponding number of workers
def GetOptimalSol(skillName,requirement):
    if skillName=="Choose a Skill" or requirement<=0:
        final_list=list_df.sort_values(by='District')['District'].tolist()
        final_count=[0]*len(final_list)
        return final_list,final_count
    worker_count_data = pd.DataFrame(df[df['Skills']==skillName].values[0][1:],columns=['Worker_count'])
    worker_count_data.insert(0,'District_name',df.columns[1:])
    worker_count_data.sort_values(by=['Worker_count'],ascending=False,inplace=True)
    worker_count_data.reset_index(drop=True,inplace=True)
    #worker_count_data.head()
    
    nd1=worker_count_data['District_name'][0]
    nd2=worker_count_data['District_name'][1]
    nd3=worker_count_data['District_name'][2]
    

    t1=pd.DataFrame(dist_df, columns=[nd1])
    t1.insert(1,'District',dist_df['District'])
    t1.sort_values(by=[nd1],inplace=True)
    t1.head()

    got=0
    nlist1=[]
    for i in t1['District'].values:
        got=got+df[df['Skills']==skillName][i].values[0]
        nlist1.append(i)
        if got >= requirement :
            #print(nlist1)
            break
            
    t1=pd.DataFrame(dist_df, columns=[nd2])
    t1.insert(1,'District',dist_df['District'])
    t1.sort_values(by=[nd2],inplace=True)
    t1.head()

    got=0
    nlist2=[]
    for i in t1['District'].values:
        got=got+df[df['Skills']==skillName][i].values[0]
        nlist2.append(i)
        if got >= requirement :
            #print(nlist2)
            break
    
    t1=pd.DataFrame(dist_df, columns=[nd3])
    t1.insert(1,'District',dist_df['District'])
    t1.sort_values(by=[nd3],inplace=True)
    t1.head()

    got=0
    nlist3=[]
    for i in t1['District'].values:
        got=got+df[df['Skills']==skillName][i].values[0]
        nlist3.append(i)
        if got >= requirement :
            #print(nlist3)
            break    
            
    
    worker_count_data.sort_values(by=['District_name'],ascending=True,inplace=True)
    worker_count_data.reset_index(drop=True,inplace=True)

    worker_count_data.insert(2,'Area',list_df['Area'].values)

    worker_count_data.insert(1,'Skill_density',worker_count_data['Worker_count']/list_df['Area'])
    worker_count_data.sort_values(by=['Skill_density'],ascending=False,inplace=True)
    worker_count_data.reset_index(drop=True,inplace=True)
    #print(worker_count_data.head())
    
    dd1=worker_count_data['District_name'][0]
    dd2=worker_count_data['District_name'][1]
    dd3=worker_count_data['District_name'][2]
    
    t1=pd.DataFrame(dist_df, columns=[dd1])
    t1.insert(1,'District',dist_df['District'])
    t1.sort_values(by=[dd1],inplace=True)
    t1.head()

    got=0
    dlist1=[]
    for i in t1['District'].values:
        got=got+df[df['Skills']==skillName][i].values[0]
        dlist1.append(i)
        if got >= requirement :
            #print(dlist1)
            break

    t1=pd.DataFrame(dist_df, columns=[dd2])
    t1.insert(1,'District',dist_df['District'])
    t1.sort_values(by=[dd2],inplace=True)
    t1.head()

    got=0
    dlist2=[]
    for i in t1['District'].values:
        got=got+df[df['Skills']==skillName][i].values[0]
        dlist2.append(i)
        if got >= requirement :
            #print(dlist2)
            break
            
    t1=pd.DataFrame(dist_df, columns=[dd3])
    t1.insert(1,'District',dist_df['District'])
    t1.sort_values(by=[dd3],inplace=True)
    t1.head()

    got=0
    dlist3=[]
    for i in t1['District'].values:
        got=got+df[df['Skills']==skillName][i].values[0]
        dlist3.append(i)
        if got >= requirement :
            #print(dlist3)
            break
            
    final_list=[calc_area(nlist1),calc_area(nlist2),calc_area(nlist3),calc_area(dlist1),calc_area(dlist2),calc_area(dlist3)]
    op=final_list.index(min(final_list))
    if op==0:
        final_list=nlist1
    if op==1:
        final_list=nlist2
    if op==2:
        final_list=nlist3
    if op==3:
        final_list=dlist1
    if op==4:
        final_list=dlist2
    if op==5:
        final_list=dlist3
    final_count=[]
    for i in final_list:
        final_count.append(df[df['Skills']==skillName][i].values[0])
    return final_list,final_count


# ### function to generate the output for pie chart
def GetSkillDistribution(district_name):
    df.sort_values(by=[district_name],ascending=False,inplace=True)
    l1=df['Skills'].tolist()[0:5]
    l2=df[district_name].tolist()[0:5]
    return dict(zip(l1,l2))

#print(find_skill_distribution('gorakhpur'))

# ### plot function
def GetPlot(skillQuery,num,nameDist):
    def GetJsonData(skillQuery,num):
        names,outputs=GetOptimalSol(skillQuery,int(num))    
        #result=getData(skillQuery)[1:]
        print(names,outputs)
        data=pd.DataFrame({'district':names,'values':outputs})
        df=mapdf.merge(data,left_on='district',right_on='district',how='left')
        df['values']=df['values'].astype(float)
        df.fillna({'values':'0'}, inplace = True)
        merged_json = json.loads(df.to_json())
        #Convert to String like object.
        json_data = json.dumps(merged_json)
        return json_data,names,outputs
    
    query=skillQuery
    json_data,dists,nums= GetJsonData(skillQuery,num)
    #print(json_data['features'][0]['properties']['district'])
    #print(json.loads(json_data)['features'][0]['properties'])
    geosource = GeoJSONDataSource(geojson = json_data)
    palette = brewer['YlGnBu'][9]
    palette = palette[::-1]
    #Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors. Input nan_color.
    color_mapper = LinearColorMapper(palette = palette, low =0, high = 1000, low_color = '#ffffff')


    #tick_labels = {'0': '0', '5': '5', '10':'10', '15':'15', '20':'20', '25':'25', '30':'30','35':'35', '40': '>40'}
    hoverover = HoverTool(tooltips = [ ('District','@district'),('No. of workers', '@values')])
    #Create color bar. 
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,border_line_color=None,location = (0,0), orientation = 'horizontal')
    #Create figure object.
    p = figure(title='Please choose a Skill and number to view the district-wise availability of workers', plot_height = 600 , plot_width = 850, toolbar_location = None, tools = [hoverover])
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    #Add patch renderer to figure. 
    p.patches('xs','ys', source = geosource,fill_color = {'field' :'values', 'transform' : color_mapper},line_color = 'black', line_width = 0.25, fill_alpha = 1)
    #Specify layout
    p.add_layout(color_bar, 'below')
    
    def GetSourceData(distName):
        x=GetSkillDistribution(distName)
        df = pd.Series(x).reset_index(name='value').rename(columns={'index':'district'})
        df['angle'] = df['value']/df['value'].sum() * 2*pi
        df['color'] = Category20c[len(x)]
        return df
    
    data_df=GetSourceData(nameDist)
    colsource = ColumnDataSource(data=data_df)
    fig = figure(plot_height=600,plot_width=600, title="Skill-wise distribution of workers", toolbar_location=None,tools="hover", tooltips="@district: @value", x_range=(-0.5, 1.0))
    fig.wedge(x=0, y=1, radius=0.36,
    start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
    line_color="white", fill_color='color', legend_field='district', source=colsource)

    fig.axis.axis_label=None
    fig.axis.visible=False
    fig.grid.grid_line_color = None


    
    def UpdateMap(attr,old,new):
        query= selectSkill.value
        num=num_input.value
        new_data,distnames,nums = GetJsonData(query,num)
        geosource.geojson = new_data
        if int(num)<0:
            p.title.text='Please Enter a valid input for number of workers'
        elif query=='Choose a Skill':
            p.title.text='Please choose a Skill and to view the district-wise availability of workers'
        else:
            p.title.text ='Availability of '+query+' in various Districts'

    def UpdateChart(attr,old,new):
        distName=distInput.value
        new_df=GetSourceData(distName)
        colsource.data=new_df
        
    selectSkill= Select(title='Choose a skill',value='Choose a Skill',options=skill_list)
    selectSkill.on_change('value',UpdateMap)
    
    num_input = TextInput(value="0", title="Enter number of workers")
    num_input.on_change("value", UpdateMap)
    
    distInput=Select(title='Choose a District to view the skill-wise distribution of workers',value='agra',options=list_df.sort_values(by='District')['District'].tolist())
    distInput.on_change("value",UpdateChart)
    
    first=column(row(selectSkill,num_input),p)
    second=column(distInput,fig)
    
    layout = row(first,second)
    curdoc().add_root(layout)
    #output_notebook()
    show(layout)
