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


st.set_page_config( page_title = 'Cities', layout='wide' )

#-----------------------------------
#  Load  and Transforme Dataframe
#-----------------------------------
df_raw = pd.read_csv( 'datasets/zomato.csv' ) 

df = rename_columns(df_raw )

df = df.loc[ df.isna().any(axis=1) != True, :]

df["cuisines"] = df.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])

df['country_code'] = df.loc[:,'country_code'].apply( lambda x :  country_name( x ) ) 

df3 = df.copy()

# ----------------------------------------
# Aplicacao do filtro ao layout
# ----------------------------------------

country = [ "Australia", "Brazil", "Canada", "Indonesia", "New Zeland" ]


list_country = list( df3['country_code'].unique() )
country_options = st.sidebar.multiselect( 'Select Countries', list_country ,default = country )


# Filtro de Traffic 
linhas_selecionadas = df3['country_code'].isin( country_options )
df3 = df3.loc[ linhas_selecionadas, : ]

# ----------------------------------------
# streamlit Barra Lateral
# ----------------------------------------

imagepath = 'pages/' 
image = Image.open( imagepath + 'logo.png')
st.sidebar.image( image, width=120 )

st.sidebar.markdown( '# Zomato Company' )
st.sidebar.markdown( '### The List Best Restaurants' )
st.sidebar.markdown( """---""" )


st.header( 'Marktplace - View by cities' )


# ----------------------------------------
# streamlit Layout - Body 
# ----------------------------------------

with st.container():
    
    st.markdown( '### Sum of Restaurant by cities' ) 
    
    df_aux = ( df3[ ['country_code','city', 'restaurant_id' ] ].groupby( ['country_code','city'] )
                                             .count()
                                             .sort_values( 'restaurant_id', ascending=False )
                                             .reset_index() )
    
   # fig = px.histogram( df_aux , x="city", y="restaurant_id", color='country_code', barmode='group' )
    fig = px.bar( df_aux , x="city", y="restaurant_id", color='country_code', text_auto=True)
    
    #fig = px.bar( df_aux.head( 10 ), x = 'city' , y ='restaurant_id' )
    st.plotly_chart( fig, use_container_width=True )

with st.container():
    
    st.markdown( '### Aggregate rating' )
    
    rating = st.slider( "Aggregate rating:",  0.0 , 5.0,  1.5 ) 
    
    
    df31 = df3.loc[df3['aggregate_rating'] > rating , : ]
    df_aux = df31[['country_code','city', 'aggregate_rating']].groupby( ['country_code','city'] ).mean().reset_index()

    df_aux = df_aux.loc[ df_aux['aggregate_rating'] > 4, : ].sort_values( 'aggregate_rating' , ascending=False)
    
    # st.dataframe( df_aux )
    
    fig = px.bar( df_aux , x="city", y="aggregate_rating", color='country_code', text_auto=True)
    
    #fig = px.bar( df_aux.head( 10 ), x = 'city' , y ='restaurant_id' )
    st.plotly_chart( fig, use_container_width=True )
    
    