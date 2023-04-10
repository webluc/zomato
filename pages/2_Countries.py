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


st.set_page_config( page_title = 'Countries', layout='wide' )

#-----------------------------------
#  Load  and Transforme Dataframe
#-----------------------------------
df_raw = pd.read_csv( 'datasets/zomato.csv' ) 

df = rename_columns(df_raw )

df = df.loc[ df.isna().any(axis=1) != True, :]

df["cuisines"] = df.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])

df['country_code'] = df.loc[:,'country_code'].apply( lambda x :  country_name( x ) ) 

df2 = df.copy()

# ----------------------------------------
# Aplicacao do filtro ao layout
# ----------------------------------------

country = [ "Australia", "Brazil", "Canada", "Indonesia", "New Zeland" ]


list_country = list( df2['country_code'].unique() )
country_options = st.sidebar.multiselect( 'Select Countries', list_country ,default = country )


# Filtro de Traffic 
linhas_selecionadas = df2['country_code'].isin( country_options )
df2 = df2.loc[ linhas_selecionadas, : ]

# ----------------------------------------
# streamlit Barra Lateral
# ----------------------------------------

imagepath = 'pages/' 
image = Image.open( imagepath + 'logo.png')
st.sidebar.image( image, width=120 )

st.sidebar.markdown( '# Zomato Company' )
st.sidebar.markdown( '### The List Best Restaurants' )
st.sidebar.markdown( """---""" )


st.header( 'Marktplace - View by countries' )


# ----------------------------------------
# streamlit Layout - Body 
# ----------------------------------------
with st.container():
    
    st.markdown( '### Sum of cities by country' ) 
                   
    # country_code, cityd
    df_aux = ( df2[ [ 'country_code', 'city'] ].groupby( 'country_code' )
                                               .count()
                                               .sort_values( 'city', ascending=False )
                                               .reset_index() )
    #print( country_name( df_aux.loc[0][0] ) )
    fig = px.pie( df_aux, 'country_code', 'city', title=f'Maior país :{ df_aux.loc[0][0] }' )
                   
    st.plotly_chart( fig, use_container_width=True )
    
with st.container():   
    
     st.markdown( '### Restaurant Sum per countries' ) 
        
    # restaurant_id,
     df_aux = ( df2[ [ 'country_code', 'restaurant_id'] ].groupby( 'country_code' ).count().sort_values( 'restaurant_id', ascending=False ).reset_index() )
    
     fig = px.scatter( df_aux, 'country_code', 'restaurant_id', title=f'Maior país :{ df_aux.loc[0][0] }' )
    
     st.plotly_chart( fig, use_container_width=True )
        
with st.container():
    col1, col2 = st.columns( 2 )
    with col1:
        
        st.markdown( '### Restaurant Sum per countries' ) 
        
        df21 = df2.loc[ df2['price_range'] == 4 , : ]

        df_aux = ( df21[ [ 'country_code', 'restaurant_id'] ].groupby( 'country_code' )
                                                   .count()
                                                   .sort_values( 'restaurant_id', ascending=False )
                                                   .reset_index() )

        st.dataframe( df_aux )
        
    with col2:
        st.markdown( '### Total votes' ) 
            
        df_aux = ( df2[ [ 'country_code', 'votes'] ].groupby( 'country_code' )
                                                    .sum()
                                                    .sort_values( 'votes', ascending=False )
                                                    .reset_index() )
        st.dataframe( df_aux  )

with st.container():

    # restaurant_id,
    df_aux = ( df2[ [ 'country_code', 'cuisines'] ].groupby( 'country_code' )
                                                   .nunique()
                                                   .sort_values( 'cuisines', ascending=False )
                                                   .reset_index() )
    fig = px.bar( df_aux, 'country_code', 'cuisines', title=f'Maior país :{df_aux.loc[0][0]}' )
    
    st.plotly_chart( fig, use_container_width=True )
        
