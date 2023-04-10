import folium
import inflection
import pandas         as pd
import numpy          as np
import plotly.express as px
import streamlit      as st

from folium.plugins   import MarkerCluster
from streamlit_folium import folium_static
from library.util     import *
from PIL              import Image


st.set_page_config( page_title = 'Main', layout='wide' )

#-----------------------------------
#  Load  and Transforme Dataframe
#-----------------------------------
df_raw = pd.read_csv( 'datasets/zomato.csv' ) 

df = rename_columns(df_raw )

df = df.loc[ df.isna().any(axis=1) != True, :]

df["cuisines"] = df.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])

df['country_code'] = df.loc[:,'country_code'].apply( lambda x :  country_name( x ) ) 

df1 = df.copy()

# ----------------------------------------
# Aplicacao do filtro ao layout
# ----------------------------------------

country = [ "India", "Australia", "Brazil", "Canada", "Indonesia", "New Zeland" ]

list_country = list( df1['country_code'].unique() )
country_options = st.sidebar.multiselect( 'Select Countries', list_country ,default = country )


# Filtro de Traffic 
linhas_selecionadas = df1['country_code'].isin( country_options )
df1 = df1.loc[ linhas_selecionadas, : ]

# ----------------------------------------
# streamlit Barra Lateral
# ----------------------------------------

imagepath = 'pages/' 
image = Image.open( imagepath + 'logo.png')
st.sidebar.image( image, width=120 )

st.sidebar.markdown( '# Zomato Company' )
st.sidebar.markdown( '### The List Best Restaurants' )
st.sidebar.markdown( """---""" )


st.header( 'Marktplace - Visão Geral' )


# ----------------------------------------
# streamlit Layout - Body 
# ----------------------------------------

with st.container():
    st.header( 'Registered Totals' ) 
    col1, col2, col3, col4, col5 = st.columns( 5 )
    with col1:
        col1.metric('Restaurant', df1['restaurant_name'].nunique() )                 
    with col2:
        col2.metric('Countries', df1['country_code'].nunique() )
    with col3:
        col3.metric('Cities', df1['city'].nunique() )
    with col4:    
        col4.metric('Cuisines', df1['cuisines'].nunique() )
    with col5:    
        col5.metric('Wishes', df1['votes'].sum() )
        
with st.container():
    
    st.header( 'Geolocation' )
    
    df_aux = df1.loc[:, ['country_code','city','longitude','latitude']]
    
    map = folium.Map( zoom_start = 16, use_container_width=True ) #width=1500, height=800 )
    
    mCluster = MarkerCluster( name="Markers" ).add_to( map )

    for index, location_info in df_aux.iterrows():
        folium.Marker( [ location_info['latitude' ],
                         location_info['longitude']],
                         popup=location_info[[ 'country_code','city']] ).add_to( mCluster )
        
    

    folium_static( map  )
