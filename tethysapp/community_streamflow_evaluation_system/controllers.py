import json
from pathlib import Path
import pandas as pd
import geopandas as gpd

from tethys_sdk.layouts import MapLayout
from tethys_sdk.routing import controller
from .app import CSES as app

#functions to load AWS data
import boto3
import os
from botocore import UNSIGNED 
from botocore.client import Config

#Date picker
from tethys_sdk.gizmos import DatePicker
from django.shortcuts import render, reverse, redirect
from tethys_sdk.gizmos import DatePicker, SelectInput, TextInput
import datetime
from django.http import JsonResponse
from django.urls import reverse_lazy

#Connect web pages
from django.http import HttpResponse 

# HOME = os.getcwd()
# MODEL_OUTPUT_FOLDER_NAME = 'sample_nextgen_data'

# #Connect to AWS s3 for data
# #home = Path(app_workspace.path) #"./workspaces/app_workspace"

# KEYPATH = f"{HOME}/tethysapp/community_streamflow_evaluation_system/AWSaccessKeys.csv"
# ACCESS = pd.read_csv(KEYPATH)

ACCESS_KEY_ID = app.get_custom_setting('Access_key_ID')
ACCESS_KEY_SECRET = app.get_custom_setting('Secret_access_key')


#start session
SESSION = boto3.Session(
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_KEY_SECRET
    # aws_access_key_id=ACCESS['Access key ID'][0],
    # aws_secret_access_key=ACCESS['Secret access key'][0],
)
s3 = SESSION.resource('s3')
#AWS bucket information
BUCKET_NAME = 'streamflow-app-data'
BUCKET = s3.Bucket(BUCKET_NAME) 
S3 = boto3.resource('s3', config=Config(signature_version=UNSIGNED))



@controller
def home(request):

        start_date_picker = DatePicker( 
            name='start-date',
            display_text='Start Date',
            autoclose=False,
            format='mm-dd-yyyy',
            start_date='01-01-1980',
            end_date= '12-30-2020',
            start_view='year',
            today_button=False, 
            initial='01-01-2019'
        ) 
        end_date_picker = DatePicker( 
            name='end-date',
            display_text='End Date',
            start_date='01-01-1980',
            end_date= '12-30-2020',
            autoclose=False,
            format='mm-dd-yyyy',
            start_view='year',
            today_button=False, 
            initial='06-11-2019'
        )
       

        context = { 
           'start_date_picker': start_date_picker,
           'end_date_picker': end_date_picker,
    
        }


        return render(request, 'community_streamflow_evaluation_system/home.html', context)


  

#Controller for the state class 
@controller(
    name="roset_state",
    url="roset_state/",
    app_workspace=True,
)   
class MapLayoutTutorialMapRosetState(MapLayout): 
    # Define base map options
    app = app
    back_url = reverse_lazy('community_streamflow_evaluation_system:home')
    base_template = 'community_streamflow_evaluation_system/base.html'
    map_title = 'Research Oriented Streamflow Evaluation Toolset'
    map_subtitle = 'An open-source hydrological model evaluation tool for NHDPlus models'
    basemaps = [
        {'ESRI': {'layer':'NatGeo_World_Map'}},
        {'ESRI': {'layer':'World_Street_Map'}},
        {'ESRI': {'layer':'World_Imagery'}},
        {'ESRI': {'layer':'World_Shaded_Relief'}},
        {'ESRI': {'layer':'World_Topo_Map'}},
        'OpenStreetMap',      
    ]
    default_map_extent = [-73.555665, 42.053811, -71.6359, 41.10654]
    max_zoom = 16
    min_zoom = 1
    show_properties_popup = True  
    plot_slide_sheet = True
    template_name = 'community_streamflow_evaluation_system/roset_state.html' 
   
    
 
    def update_data(self, request, *args, **kwargs):
        """
        #Custom REST method for updating data form Map Layout view.
        Controller for the app home page
        """
        self.startdate=request.POST.get('start_date')
        self.enddate=request.POST.get('end_date')
        self.modelid=request.POST.get('model_id')
        self.stateid=request.POST.get('state_id')

        print(self.startdate,self.enddate, self.stateid, self.modelid)
 
        return JsonResponse({'success': True})
     
    def get_context(self, request, *args, **kwargs):
        """
        Create context for the Map Layout view, with an override for the map extents based on stream and weather gauges.

        Args:
            request (HttpRequest): The request.
            context (dict): The context dictionary.

        Returns:
            dict: modified context dictionary.
        """

        start_date_picker = DatePicker( 
            name='start-date',
            display_text='Start Date',
            autoclose=False,
            format='mm-dd-yyyy',
            start_date='01-01-1980',
            end_date= '12-30-2020',
            start_view='year',
            today_button=False, 
            initial='01-01-2019'
        ) 
        end_date_picker = DatePicker( 
            name='end-date',
            display_text='End Date',
            start_date='01-01-1980',
            end_date= '12-30-2020',
            autoclose=False,
            format='mm-dd-yyyy',
            start_view='year',
            today_button=False, 
            initial='06-11-2019'
        )
        
        state_id = SelectInput(display_text='Select State',
                                    name='state_id',
                                    multiple=False,
                                    options=[("Alaska", "AK"),
                                            ("Alabama", "AL"),
                                            ("Arizona", "AZ"),
                                            ("Arkansas", "AR"),
                                            ("California", "CA"),
                                            ("Colorado", "CO"),
                                            ("Connecticut", "CT"),
                                            ("Delaware", "DE"),
                                            ("Florida", "FL"),
                                            ("Georgia", "GA"),
                                            ("Hawaii", "HI"),
                                            ("Idaho", "ID"),
                                            ("Illinois", "IL"),
                                            ("Indiana", "IN"),
                                            ("Iowa", "IA"),
                                            ("Kansas", "KS"),
                                            ("Kentucky", "KY"),
                                            ("Louisiana", "LA"),
                                            ("Maine", "ME"),
                                            ("Maryland", "MD"),
                                            ("Massachusetts", "MA"),  
                                            ("Michigan", "MI"),
                                            ("Minnesota", "MN"),
                                            ("Mississippi", "MS"),
                                            ("Missouri", "MO"),
                                            ("Montana", "MT"),
                                            ("Nebraska", "NE"),
                                            ("Nevada", "NV"),
                                            ("New Hampshire", "NH"),
                                            ("New Jersey", "NJ"),
                                            ("New Mexico", "NM"),
                                            ("New York", "NY"),
                                            ("North Carolina", "NC"),
                                            ("North Dakota", "ND"),
                                            ("Ohio", "OH"),
                                            ("Oklahoma", "OK"),
                                            ("Oregon", "OR"),
                                            ("Pennsylvania", "PA"),
                                            ("Rhode Island", "RI"),
                                            ("South Carolina", "SC"),
                                            ("South Dakota", "SD"),
                                            ("Tennessee", "TN"),
                                            ("Texas", "TX"),
                                            ("Utah", "UT"),
                                            ("Vermont", "VT"),
                                            ("Virginia", "VA"),
                                            ("Washington", "WA"),
                                            ("West Virginia", "WV"),   
                                            ("Wisconsin", "WI"),  
                                            ("Wyoming", "WY")
                                        ],
                                    initial=['Alabama'], #it would be cool to change this depending on the current state input.
                                    select2_options={'placeholder': 'Select a State',
                                                    'allowClear': True})
        
        model_id = SelectInput(display_text='Select Model',
                                    name='model_id',
                                    multiple=False,
                                    options=[
                                            ("National Water Model v2.1", "NWM_v2.1"),
                                            ("National Water Model v3.0", "NWM_v3.0"),
                                            ("NWM MLP extension", "MLP"),
                                            ("NWM XGBoost extension", "XGBoost"),
                                            ("NWM CNN extension", "CNN"),
                                            ("NWM LSTM extension", "LSTM"),
                                        
                                            ],
                                    initial=['National Water Model v2.1'],
                                    select2_options={'placeholder': 'Select a model',
                                                    'allowClear': True})

        # Call Super   
        context = super().get_context( 
            request,  
            *args, 
            **kwargs
        )
        context['start_date_picker'] = start_date_picker  
        context['end_date_picker'] = end_date_picker 
        context['state_id'] = state_id
        context['model_id'] = model_id
        return context

    def compose_layers(self, request, map_view, app_workspace, *args, **kwargs): #can we select the geojson files from the input fields (e.g: AL, or a dropdown)
        """
        Add layers to the MapLayout and create associated layer group objects.
        """
     
        #print(self.startdate,self.enddate, self.stateid, self.modelid)

        print(request)


        try: 
            state_id = request.GET.get('state_id')
            startdate = request.GET.get('start-date')
            enddate = request.GET.get('end-date')
            modelid = request.GET.get('model_id')
            print(state_id)
    
            # USGS stations - from AWS s3
            stations_path = f"GeoJSON/StreamStats_{state_id}_4326.geojson" #will need to change the filename to have state before 4326
            obj = s3.Object(BUCKET_NAME, stations_path)
            stations_geojson = json.load(obj.get()['Body']) 

            # set the map extend based on the stations
            gdf = gpd.read_file(obj.get()['Body'], driver='GeoJSON')
            map_view['view']['extent'] = list(gdf.geometry.total_bounds)
        

            stations_layer = self.build_geojson_layer(
                geojson=stations_geojson,
                layer_name='USGS Stations',
                layer_title='USGS Station',
                layer_variable='stations',
                visible=True,
                selectable=True,
                plottable=True,
            ) 

            # Create layer groups
            layer_groups = [
                self.build_layer_group(
                    id='nextgen-features',
                    display_name='NextGen Features',
                    layer_control='checkbox',  # 'checkbox' or 'radio'
                    layers=[
                        stations_layer,
                    #   flowpaths_layer,
                    ],
                    visible= True
                )
            ]

        except: 
            state_id = 'AL'
            startdate = '01-01-2019'
            enddate = '01-02-2019'
            modelid = 'NWM_v2.1'
            print(state_id)
    
            # USGS stations - from AWS s3
            stations_path = f"GeoJSON/StreamStats_{state_id}_4326.geojson" #will need to change the filename to have state before 4326
            obj = s3.Object(BUCKET_NAME, stations_path)
            stations_geojson = json.load(obj.get()['Body']) 

            # set the map extend based on the stations
            gdf = gpd.read_file(obj.get()['Body'], driver='GeoJSON')
            map_view['view']['extent'] = list(gdf.geometry.total_bounds)
        

            stations_layer = self.build_geojson_layer(
                geojson=stations_geojson,
                layer_name='USGS Stations',
                layer_title='USGS Station',
                layer_variable='stations',
                visible=True,
                selectable=True,
                plottable=True,
            )

            # Create layer groups
            layer_groups = [
                self.build_layer_group(
                    id='nextgen-features',
                    display_name='NextGen Features',
                    layer_control='checkbox',  # 'checkbox' or 'radio'
                    layers=[
                        stations_layer,
                    #   flowpaths_layer,
                    ],
                    visible= True
                )
            ]

        return layer_groups


    @classmethod
    def get_vector_style_map(cls):
        return {
            'Point': {'ol.style.Style': {
                'image': {'ol.style.Circle': {
                    'radius': 5,
                    'fill': {'ol.style.Fill': {
                        'color': 'white',
                    }},
                    'stroke': {'ol.style.Stroke': {
                        'color': 'red',
                        'width': 3
                    }}
                }}
            }},
            'MultiPolygon': {'ol.style.Style': {
                'stroke': {'ol.style.Stroke': {
                    'color': 'navy',
                    'width': 3
                }},
                'fill': {'ol.style.Fill': {
                    'color': 'rgba(0, 25, 128, 0.1)'
                }}
            }},
             'MultiLineString': {'ol.style.Style': {
                'stroke': {'ol.style.Stroke': {
                    'color': 'navy',
                    'width': 2
                }},
                'fill': {'ol.style.Fill': {
                    'color': 'rgba(0, 25, 128, 0.1)'
                }}
            }},
        }

    def get_plot_for_layer_feature(self, request, layer_name, feature_id, layer_data, feature_props, app_workspace,
                                *args, **kwargs):
        """
        Retrieves plot data for given feature on given layer.
        - Can we use this function to plot two streams - explore by adding the example one again but multiplying by a factor (e.g., *1.2)
        Args:
            layer_name (str): Name/id of layer.
            feature_id (str): ID of feature.
            layer_data (dict): The MVLayer.data dictionary.
            feature_props (dict): The properties of the selected feature.

        Returns:
            str, list<dict>, dict: plot title, data series, and layout options, respectively.
      """
        # Get the feature ids
        # startdate = request.GET.get('start-date')
        # enddate = request.GET.get('end-date')
        # modelid = request.GET.get('model_id')
        # modelid = request.GET.get('model_id')
        # state_id = request.GET.get('state_id')
        id = feature_props.get('id') 
        NHD_id = feature_props.get('NHD_id') 
        state = feature_props.get('state')
  
        # USGS observed flow
        if layer_name == 'USGS Stations':
            layout = {
                'yaxis': {
                    'title': 'Streamflow (cfs)'
                } 
            }
           
            #USGS observed flow
            USGS_directory = f"NWIS/NWIS_sites_{state}.h5/NWIS_{id}.csv"
            obj = BUCKET.Object(USGS_directory)
            body = obj.get()['Body']
            USGS_df = pd.read_csv(body)
            USGS_df.pop('Unnamed: 0')    

            #modeled flow, starting with NWM
            self.model = 'NWM_v2.1'
            model_directory = f"{self.model}/NHD_segments_{state}.h5/{self.model}_{NHD_id}.csv"  #put state in geojson file
            obj = BUCKET.Object(model_directory)
            body = obj.get()['Body']
            model_df = pd.read_csv(body)
            model_df.pop('Unnamed: 0')

            #combine Dfs, remove nans
            USGS_df.drop_duplicates(subset=['Datetime'], inplace=True)
            model_df.drop_duplicates(subset=['Datetime'],  inplace=True)
            USGS_df.set_index('Datetime', inplace = True)
            model_df.set_index('Datetime', inplace = True)
            DF = pd.concat([USGS_df, model_df], axis = 1, join = 'inner')
            DF.reset_index(inplace=True)
            time_col = DF.Datetime.to_list()[:45] # date, adjust per Data source, limited to less than 500 obs/days (currently defaulted to the first 450)
            USGS_streamflow_cfs = DF.USGS_flow.to_list()[:45] # date, adjust per Data source, limited to less than 500 obs/days (currently defaulted to the first 450)
            Mod_streamflow_cfs = DF[f"{self.model[:3]}_flow"].to_list()[:45] # date, adjust per Data source, limited to less than 500 obs/days (currently defaulted to the first 450)

            data = [
                {
                    'name': 'USGS Observed',
                    'mode': 'lines',
                    'x': time_col,
                    'y': USGS_streamflow_cfs,
                    'line': {
                        'width': 2,
                        'color': 'blue'
                    }
                },
                {
                    'name': f"{self.model} Modeled",
                    'mode': 'lines',
                    'x': time_col,
                    'y': Mod_streamflow_cfs,
                    'line': {
                        'width': 2,
                        'color': 'red'
                    }
                },
            ]


            return f'{self.model} Modeled and Observed Streamflow at USGS site: "{id}"', data, layout
        





# #Controller for the HUC class
@controller(
    name="roset_huc",
    url="roset_huc/",
    app_workspace=True,
)   
class MapLayoutTutorialMapRosetHUC(MapLayout): 
    # Define base map options
    app = app
    back_url = reverse_lazy('community_streamflow_evaluation_system:home')
    base_template = 'community_streamflow_evaluation_system/base.html'
    map_title = 'Research Oriented Streamflow Evaluation Toolset'
    map_subtitle = 'An open-source hydrological model evaluation tool for NHDPlus models'
    basemaps = [ 
        {'ESRI': {'layer':'NatGeo_World_Map'}},
        {'ESRI': {'layer':'World_Street_Map'}},
        {'ESRI': {'layer':'World_Imagery'}},
        {'ESRI': {'layer':'World_Shaded_Relief'}},
        {'ESRI': {'layer':'World_Topo_Map'}},
        'OpenStreetMap',      
    ]
    default_map_extent = [-73.555665, 42.053811, -71.6359, 41.10654]
    max_zoom = 16
    min_zoom = 1
    show_properties_popup = True  
    plot_slide_sheet = True
    template_name = 'community_streamflow_evaluation_system/roset_huc.html' 
   
    
 
    def update_data(self, request, *args, **kwargs):
        """
        #Custom REST method for updating data form Map Layout view.
        Controller for the app home page
        """
        self.startdate=request.POST.get('start_date')
        self.enddate=request.POST.get('end_date')
        self.modelid=request.POST.get('model_id')
        self.hucids=request.POST.get('huc_ids')

        print(self.startdate,self.enddate, self.hucids, self.modelid)
 
        return JsonResponse({'success': True})
     
    def get_context(self, request, *args, **kwargs):
        """
        Create context for the Map Layout view, with an override for the map extents based on stream and weather gauges.

        Args:
            request (HttpRequest): The request.
            context (dict): The context dictionary.

        Returns:
            dict: modified context dictionary.
        """

        start_date_picker = DatePicker( 
            name='start-date',
            display_text='Start Date',
            autoclose=False,
            format='mm-dd-yyyy',
            start_date='01-01-1980',
            end_date= '12-30-2020',
            start_view='year',
            today_button=False, 
            initial='01-01-2019'
        ) 
        end_date_picker = DatePicker( 
            name='end-date',
            display_text='End Date',
            start_date='01-01-1980',
            end_date= '12-30-2020',
            autoclose=False,
            format='mm-dd-yyyy',
            start_view='year',
            today_button=False, 
            initial='06-11-2019'
        )
        
        huc_ids = TextInput(display_text='Enter a list of HUC regions',
                                   name='huc_ids', 
                                   placeholder= 'e.g.: 1602, 1603',
                                   )
        
        model_id = SelectInput(display_text='Select Model',
                                    name='model_id',
                                    multiple=False,
                                    options=[
                                            ("National Water Model v2.1", "NWM_v2.1"),
                                            ("National Water Model v3.0", "NWM_v3.0"),
                                            ("NWM MLP extension", "MLP"),
                                            ("NWM XGBoost extension", "XGBoost"),
                                            ("NWM CNN extension", "CNN"),
                                            ("NWM LSTM extension", "LSTM"),
                                        
                                            ],
                                    initial=['National Water Model v2.1'],
                                    select2_options={'placeholder': 'Select a model',
                                                    'allowClear': True})

        # Call Super   
        context = super().get_context( 
            request,  
            *args, 
            **kwargs
        )
        context['start_date_picker'] = start_date_picker  
        context['end_date_picker'] = end_date_picker 
        context['huc_ids'] = huc_ids
        context['model_id'] = model_id
        return context

    def compose_layers(self, request, map_view, app_workspace, *args, **kwargs): #can we select the geojson files from the input fields (e.g: AL, or a dropdown)
        """
        Add layers to the MapLayout and create associated layer group objects.
        """
     
        #print(self.startdate,self.enddate, self.stateid, self.modelid)

        print(request)


        try: 
            huc_id = request.GET.get('huc_id')
            startdate = request.GET.get('start-date')
            enddate = request.GET.get('end-date')
            modelid = request.GET.get('model_id')
            # print(state_id)
            state_id = 'UT' # temp placeholder to show connections
    
            # USGS stations - from AWS s3
            stations_path = f"GeoJSON/StreamStats_{state_id}_4326.geojson" #will need to change the filename to have state before 4326
            obj = s3.Object(BUCKET_NAME, stations_path)
            stations_geojson = json.load(obj.get()['Body']) 

            # set the map extend based on the stations
            gdf = gpd.read_file(obj.get()['Body'], driver='GeoJSON')
            map_view['view']['extent'] = list(gdf.geometry.total_bounds)
        

            stations_layer = self.build_geojson_layer(
                geojson=stations_geojson,
                layer_name='USGS Stations',
                layer_title='USGS Station',
                layer_variable='stations',
                visible=True,
                selectable=True,
                plottable=True,
            ) 

            # Create layer groups
            layer_groups = [
                self.build_layer_group(
                    id='nextgen-features',
                    display_name='NextGen Features',
                    layer_control='checkbox',  # 'checkbox' or 'radio'
                    layers=[
                        stations_layer,
                    ],
                    visible= True
                )
            ]

        except: 
            state_id = 'UT'
            startdate = '01-01-2019'
            enddate = '01-02-2019'
            modelid = 'NWM_v2.1'
            print(state_id)
    
            # USGS stations - from AWS s3
            stations_path = f"GeoJSON/StreamStats_{state_id}_4326.geojson" #will need to change the filename to have state before 4326
            obj = s3.Object(BUCKET_NAME, stations_path)
            stations_geojson = json.load(obj.get()['Body']) 

            # set the map extend based on the stations
            gdf = gpd.read_file(obj.get()['Body'], driver='GeoJSON')
            map_view['view']['extent'] = list(gdf.geometry.total_bounds)
        

            stations_layer = self.build_geojson_layer(
                geojson=stations_geojson,
                layer_name='USGS Stations',
                layer_title='USGS Station',
                layer_variable='stations',
                visible=True,
                selectable=True,
                plottable=True,
            )

            # Create layer groups
            layer_groups = [
                self.build_layer_group(
                    id='nextgen-features',
                    display_name='NextGen Features',
                    layer_control='checkbox',  # 'checkbox' or 'radio'
                    layers=[
                        stations_layer,
                    #   flowpaths_layer,
                    ],
                    visible= True
                )
            ]

        return layer_groups


    @classmethod
    def get_vector_style_map(cls):
        return {
            'Point': {'ol.style.Style': {
                'image': {'ol.style.Circle': {
                    'radius': 5,
                    'fill': {'ol.style.Fill': {
                        'color': 'white',
                    }},
                    'stroke': {'ol.style.Stroke': {
                        'color': 'red',
                        'width': 3
                    }}
                }}
            }},
            'MultiPolygon': {'ol.style.Style': {
                'stroke': {'ol.style.Stroke': {
                    'color': 'navy',
                    'width': 3
                }},
                'fill': {'ol.style.Fill': {
                    'color': 'rgba(0, 25, 128, 0.1)'
                }}
            }},
             'MultiLineString': {'ol.style.Style': {
                'stroke': {'ol.style.Stroke': {
                    'color': 'navy',
                    'width': 2
                }},
                'fill': {'ol.style.Fill': {
                    'color': 'rgba(0, 25, 128, 0.1)'
                }}
            }},
        }

    def get_plot_for_layer_feature(self, request, layer_name, feature_id, layer_data, feature_props, app_workspace,
                                *args, **kwargs):
        """
        Retrieves plot data for given feature on given layer.
        - Can we use this function to plot two streams - explore by adding the example one again but multiplying by a factor (e.g., *1.2)
        Args:
            layer_name (str): Name/id of layer.
            feature_id (str): ID of feature.
            layer_data (dict): The MVLayer.data dictionary.
            feature_props (dict): The properties of the selected feature.

        Returns:
            str, list<dict>, dict: plot title, data series, and layout options, respectively.
      """
        # Get the feature ids
        # startdate = request.GET.get('start-date')
        # enddate = request.GET.get('end-date')
        # modelid = request.GET.get('model_id')
        # modelid = request.GET.get('model_id')
        # state_id = request.GET.get('state_id')
        id = feature_props.get('id') 
        NHD_id = feature_props.get('NHD_id') 
        state = feature_props.get('state')
  
        # USGS observed flow
        if layer_name == 'USGS Stations':
            layout = {
                'yaxis': {
                    'title': 'Streamflow (cfs)'
                } 
            }
           
            #USGS observed flow
            USGS_directory = f"NWIS/NWIS_sites_{state}.h5/NWIS_{id}.csv"
            obj = BUCKET.Object(USGS_directory)
            body = obj.get()['Body']
            USGS_df = pd.read_csv(body)
            USGS_df.pop('Unnamed: 0')    

            #modeled flow, starting with NWM
            self.model = 'NWM_v2.1'
            model_directory = f"{self.model}/NHD_segments_{state}.h5/{self.model}_{NHD_id}.csv"  #put state in geojson file
            obj = BUCKET.Object(model_directory)
            body = obj.get()['Body']
            model_df = pd.read_csv(body)
            model_df.pop('Unnamed: 0')

            #combine Dfs, remove nans
            USGS_df.drop_duplicates(subset=['Datetime'], inplace=True)
            model_df.drop_duplicates(subset=['Datetime'],  inplace=True)
            USGS_df.set_index('Datetime', inplace = True)
            model_df.set_index('Datetime', inplace = True)
            DF = pd.concat([USGS_df, model_df], axis = 1, join = 'inner')
            DF.reset_index(inplace=True)
            time_col = DF.Datetime.to_list()[:45] # date, adjust per Data source, limited to less than 500 obs/days (currently defaulted to the first 450)
            USGS_streamflow_cfs = DF.USGS_flow.to_list()[:45] # date, adjust per Data source, limited to less than 500 obs/days (currently defaulted to the first 450)
            Mod_streamflow_cfs = DF[f"{self.model[:3]}_flow"].to_list()[:45] # date, adjust per Data source, limited to less than 500 obs/days (currently defaulted to the first 450)

            data = [
                {
                    'name': 'USGS Observed',
                    'mode': 'lines',
                    'x': time_col,
                    'y': USGS_streamflow_cfs,
                    'line': {
                        'width': 2,
                        'color': 'blue'
                    }
                },
                {
                    'name': f"{self.model} Modeled",
                    'mode': 'lines',
                    'x': time_col,
                    'y': Mod_streamflow_cfs,
                    'line': {
                        'width': 2,
                        'color': 'red'
                    }
                },
            ]


            return f'{self.model} Modeled and Observed Streamflow at USGS site: "{id}"', data, layout


 




#Controller for the Reach class
@controller(
    name="roset_reach",
    url="roset_reach/",
    app_workspace=True,
)   
class MapLayoutTutorialMapRosetReach(MapLayout): 
    # Define base map options
    app = app
    back_url = reverse_lazy('community_streamflow_evaluation_system:home')
    base_template = 'community_streamflow_evaluation_system/base.html'
    map_title = 'Research Oriented Streamflow Evaluation Toolset'
    map_subtitle = 'An open-source hydrological model evaluation tool for NHDPlus models'
    basemaps = [
        {'ESRI': {'layer':'NatGeo_World_Map'}},
        {'ESRI': {'layer':'World_Street_Map'}},
        {'ESRI': {'layer':'World_Imagery'}},
        {'ESRI': {'layer':'World_Shaded_Relief'}},
        {'ESRI': {'layer':'World_Topo_Map'}},
        'OpenStreetMap',      
    ]
    default_map_extent = [-73.555665, 42.053811, -71.6359, 41.10654]
    max_zoom = 16
    min_zoom = 1
    show_properties_popup = True  
    plot_slide_sheet = True
    template_name = 'community_streamflow_evaluation_system/roset_reach.html' 
    
 
    def update_data(self, request, *args, **kwargs):
        """
        #Custom REST method for updating data form Map Layout view.
        Controller for the app home page
        """
        self.startdate=request.POST.get('start_date')
        self.enddate=request.POST.get('end_date')
        self.modelid=request.POST.get('model_id')
        self.reachids=request.POST.get('reach_ids')

        print(self.startdate,self.enddate, self.reachids, self.modelid)
 
        return JsonResponse({'success': True})
     
    def get_context(self, request, *args, **kwargs):
        """
        Create context for the Map Layout view, with an override for the map extents based on stream and weather gauges.

        Args:
            request (HttpRequest): The request.
            context (dict): The context dictionary.

        Returns:
            dict: modified context dictionary.
        """

        start_date_picker = DatePicker( 
            name='start-date',
            display_text='Start Date',
            autoclose=False,
            format='mm-dd-yyyy',
            start_date='01-01-1980',
            end_date= '12-30-2020',
            start_view='year',
            today_button=False, 
            initial='01-01-2019'
        ) 
        end_date_picker = DatePicker( 
            name='end-date',
            display_text='End Date',
            start_date='01-01-1980',
            end_date= '12-30-2020',
            autoclose=False,
            format='mm-dd-yyyy',
            start_view='year',
            today_button=False, 
            initial='06-11-2019'
        )
        
        reach_ids = TextInput(display_text='Enter a list of USGS sites',
                                   name='reach_ids', 
                                   placeholder= 'e.g.: 10224000, 10219000',
                                   )

        model_id = SelectInput(display_text='Select Model',
                                    name='model_id',
                                    multiple=False,
                                    options=[
                                            ("National Water Model v2.1", "NWM_v2.1"),
                                            ("National Water Model v3.0", "NWM_v3.0"),
                                            ("NWM MLP extension", "MLP"),
                                            ("NWM XGBoost extension", "XGBoost"),
                                            ("NWM CNN extension", "CNN"),
                                            ("NWM LSTM extension", "LSTM"),
                                        
                                            ],
                                    initial=['National Water Model v2.1'],
                                    select2_options={'placeholder': 'Select a model',
                                                    'allowClear': True})

        # Call Super   
        context = super().get_context( 
            request,  
            *args, 
            **kwargs
        )
        context['start_date_picker'] = start_date_picker  
        context['end_date_picker'] = end_date_picker 
        context['reach_ids'] = reach_ids
        context['model_id'] = model_id
        return context
    
    #function for getting reachids -- this could likely be placed into a utils.py file...
    def combine_jsons(self,file_list):
        #file_list = ['first.json', 'second.json',... ,'last.json']
        all_data_df = gpd.GeoDataFrame()
        for json_file in file_list:
                    # with open(json_file,'r+') as file:
            #    # First we load existing data into a dict.
            #    #file_data = json.load(file)
            obj = s3.Object(BUCKET_NAME, json_file)
            stations_geojson = json.load(obj.get()['Body']) 
            gdf = gpd.read_file(obj.get()['Body'], driver='GeoJSON')
            all_data_df = pd.concat([all_data_df, gdf]).set_crs(crs= 'EPSG:4326')

        return all_data_df

    def reach_json(self,reach_ids):
        csv_key = 'Streamstats/Streamstats.csv'
        obj = BUCKET.Object(csv_key)
        body = obj.get()['Body']
        Streamstats = pd.read_csv(body)
        Streamstats.pop('Unnamed: 0')
        Streamstats.drop_duplicates(subset = 'NWIS_site_id', inplace = True)
        Streamstats.reset_index(inplace = True, drop = True)

        #Convert to geodataframe
        StreamStats = gpd.GeoDataFrame(Streamstats, geometry=gpd.points_from_xy(Streamstats.dec_long_va, Streamstats.dec_lat_va))

        #the csv loses the 0 in front of USGS ids, fix
        NWIS = list(Streamstats['NWIS_site_id'].astype(str))
        Streamstats['NWIS_site_id'] = ["0"+str(i) if len(i) <8 else i for i in NWIS]  

        #Get streamstats information for each USGS location
        sites = pd.DataFrame()

        for site in reach_ids:
            print(site)
            s = Streamstats[Streamstats['NWIS_site_id'] ==  str(site)]
            sites = pd.concat([sites, s])

        #print(sites)
        stateids = list(set(list(sites['state_id'])))

        stationpaths = []
        for state in stateids:
            stations_path = f"GeoJSON/StreamStats_{state}_4326.geojson" #will need to change the filename to have state before 4326
            stationpaths.append(stations_path)

        #combine stations
        combined = self.combine_jsons(stationpaths)
        

        #get site ids out of DF to make new geojson
        finaldf = gpd.GeoDataFrame()
        for site in reach_ids:
            df = combined[combined['USGS_id'] == site]
            finaldf = pd.concat([finaldf, df])

        #reset index and drop any duplicates
        finaldf.reset_index(inplace = True, drop = True)
        finaldf.drop_duplicates('USGS_id', inplace = True)        

        return finaldf


    def compose_layers(self, request, map_view, app_workspace, *args, **kwargs): #can we select the geojson files from the input fields (e.g: AL, or a dropdown)
        """
        Add layers to the MapLayout and create associated layer group objects.
        """
     
        try: 
            reach_ids = request.GET.get('reach_ids')
            reach_ids = reach_ids.strip('][').split(', ')
            startdate = request.GET.get('start-date')
            enddate = request.GET.get('end-date')
            modelid = request.GET.get('model_id')
            print(reach_ids, startdate, enddate, modelid)
            #for reach in reach_ids:
             #   print(reach)
            #breakpoint()
            

            # USGS stations - from AWS s3
            finaldf = self.reach_json(reach_ids)
            print(finaldf)
            map_view['view']['extent'] = list(finaldf.geometry.total_bounds)
            stations_geojson = json.loads(finaldf.to_json()) 
            stations_geojson.update({"crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" }}})         


            stations_layer = self.build_geojson_layer(
                geojson=stations_geojson,
                layer_name='USGS Stations',
                layer_title='USGS Station',
                layer_variable='stations',
                visible=True,
                selectable=True,
                plottable=True,
            ) 

            # Create layer groups
            layer_groups = [
                self.build_layer_group(
                    id='nextgen-features',
                    display_name='NextGen Features',
                    layer_control='checkbox',  # 'checkbox' or 'radio'
                    layers=[
                        stations_layer,
                    ],
                    visible= True
                )
            ]

        except: 
            print('exception')
            #put in some defaults
            reach_ids = ['10126000', '10068500']
            startdate = '01-01-2019' 
            enddate = '01-02-2019'
            modelid = 'NWM_v2.1'

    
            finaldf = self.reach_json(reach_ids)
            map_view['view']['extent'] = list(finaldf.geometry.total_bounds)
            stations_geojson = json.loads(finaldf.to_json()) 
            stations_geojson.update({"crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" }}}) 


            stations_layer = self.build_geojson_layer(
                geojson=stations_geojson,
                layer_name='USGS Stations',
                layer_title='USGS Station',
                layer_variable='stations',
                visible=True,
                selectable=True,
                plottable=True,
            ) 
            
            # Create layer groups
            layer_groups = [
                self.build_layer_group(
                    id='nextgen-features',
                    display_name='NextGen Features',
                    layer_control='checkbox',  # 'checkbox' or 'radio'
                    layers=[
                        stations_layer,
                    ],
                    visible= True
                )
            ]

        return layer_groups


    @classmethod
    def get_vector_style_map(cls):
        return {
            'Point': {'ol.style.Style': {
                'image': {'ol.style.Circle': {
                    'radius': 5,
                    'fill': {'ol.style.Fill': {
                        'color': 'white',
                    }},
                    'stroke': {'ol.style.Stroke': {
                        'color': 'red',
                        'width': 3
                    }}
                }}
            }},
            'MultiPolygon': {'ol.style.Style': {
                'stroke': {'ol.style.Stroke': {
                    'color': 'navy',
                    'width': 3
                }},
                'fill': {'ol.style.Fill': {
                    'color': 'rgba(0, 25, 128, 0.1)'
                }}
            }},
             'MultiLineString': {'ol.style.Style': {
                'stroke': {'ol.style.Stroke': {
                    'color': 'navy',
                    'width': 2
                }},
                'fill': {'ol.style.Fill': {
                    'color': 'rgba(0, 25, 128, 0.1)'
                }}
            }},
        }

    def get_plot_for_layer_feature(self, request, layer_name, feature_id, layer_data, feature_props, app_workspace,
                                *args, **kwargs):
        """
        Retrieves plot data for given feature on given layer.
        - Can we use this function to plot two streams - explore by adding the example one again but multiplying by a factor (e.g., *1.2)
        Args:
            layer_name (str): Name/id of layer.
            feature_id (str): ID of feature.
            layer_data (dict): The MVLayer.data dictionary.
            feature_props (dict): The properties of the selected feature.

        Returns:
            str, list<dict>, dict: plot title, data series, and layout options, respectively.
      """
        # Get the feature ids
        # startdate = request.GET.get('start-date')
        # enddate = request.GET.get('end-date')
        # modelid = request.GET.get('model_id')
        # modelid = request.GET.get('model_id')
        # state_id = request.GET.get('state_id')
        id = feature_props.get('id') 
        NHD_id = feature_props.get('NHD_id') 
        state = feature_props.get('state')
  
        # USGS observed flow
        if layer_name == 'USGS Stations':
            layout = {
                'yaxis': {
                    'title': 'Streamflow (cfs)'
                } 
            }
           
            #USGS observed flow
            USGS_directory = f"NWIS/NWIS_sites_{state}.h5/NWIS_{id}.csv"
            obj = BUCKET.Object(USGS_directory)
            body = obj.get()['Body']
            USGS_df = pd.read_csv(body)
            USGS_df.pop('Unnamed: 0')    

            #modeled flow, starting with NWM
            self.model = 'NWM_v2.1'
            model_directory = f"{self.model}/NHD_segments_{state}.h5/{self.model}_{NHD_id}.csv"  #put state in geojson file
            obj = BUCKET.Object(model_directory)
            body = obj.get()['Body']
            model_df = pd.read_csv(body)
            model_df.pop('Unnamed: 0')

            #combine Dfs, remove nans
            USGS_df.drop_duplicates(subset=['Datetime'], inplace=True)
            model_df.drop_duplicates(subset=['Datetime'],  inplace=True)
            USGS_df.set_index('Datetime', inplace = True)
            model_df.set_index('Datetime', inplace = True)
            DF = pd.concat([USGS_df, model_df], axis = 1, join = 'inner')
            DF.reset_index(inplace=True)
            time_col = DF.Datetime.to_list()[:45] # date, adjust per Data source, limited to less than 500 obs/days (currently defaulted to the first 450)
            USGS_streamflow_cfs = DF.USGS_flow.to_list()[:45] # date, adjust per Data source, limited to less than 500 obs/days (currently defaulted to the first 450)
            Mod_streamflow_cfs = DF[f"{self.model[:3]}_flow"].to_list()[:45] # date, adjust per Data source, limited to less than 500 obs/days (currently defaulted to the first 450)

            data = [
                {
                    'name': 'USGS Observed',
                    'mode': 'lines',
                    'x': time_col,
                    'y': USGS_streamflow_cfs,
                    'line': {
                        'width': 2,
                        'color': 'blue'
                    }
                },
                {
                    'name': f"{self.model} Modeled",
                    'mode': 'lines',
                    'x': time_col,
                    'y': Mod_streamflow_cfs,
                    'line': {
                        'width': 2,
                        'color': 'red'
                    }
                },
            ]


            return f'{self.model} Modeled and Observed Streamflow at USGS site: "{id}"', data, layout