import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import mysql.connector
import requests
import json


#############################################################################################################################

#SQL IMPORT 
# Connection parameters
connection_params = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'Lolptw@123',
    'database': 'Phonepe_viz' 
}

# Establish connection
connection = mysql.connector.connect(**connection_params)

# Create a cursor object
cursor = connection.cursor()

#Aggregated_insurance
# Execute the SQL query
cursor.execute("SELECT * FROM aggregated_insurance")
# Fetch all rows from the result set
table1 = cursor.fetchall()
# Create DataFrame from fetched data
aggregated_insurance = pd.DataFrame(table1,columns=("States","Years","Quarter","Transcation_type","Transcation_count","Transcation_amount"))

#Aggregated_transcation
cursor.execute("SELECT * FROM aggregated_transcation")
table2=cursor.fetchall()
aggregated_transcation=pd.DataFrame(table2,columns=("States","Years","Quarter","Transcation_type","Transcation_count","Transcation_amount"))

#Aggregated_user
cursor.execute("SELECT * FROM aggregated_user")
table3=cursor.fetchall()
aggregated_user=pd.DataFrame(table3,columns=("States","Years","Quarter","Brands","Transcation_count","Percentage"))

#map_insurance
cursor.execute("SELECT * FROM map_insurance")
table4=cursor.fetchall()
map_insurance=pd.DataFrame(table4,columns=("States","Years","Quarter","Transcation_count","Districts","Transcation_amount"))

#map_transcation
cursor.execute("SELECT * FROM map_transcation")
table5=cursor.fetchall()
map_transcation=pd.DataFrame(table5,columns=("States","Years","Quarter","Transcation_count","Districts","Transcation_amount"))

#map_user
cursor.execute("SELECT * FROM map_user")
table6=cursor.fetchall()
map_user=pd.DataFrame(table6,columns=("States","Years","Quarter","RegisteredUsers","AppOpens","Districts"))

#top_insurance
cursor.execute("SELECT * FROM top_insurance")
table7=cursor.fetchall()
top_insurance=pd.DataFrame(table7,columns=("States","Years","Quarter","Transcation_count","Transcation_amount","Pincodes"))

#top_transcation
cursor.execute("SELECT * FROM top_transcation")
table8=cursor.fetchall()
top_transcation=pd.DataFrame(table8,columns=("States","Years","Quarter","Transcation_count","Transcation_amount","Pincodes"))

#top_user
cursor.execute("SELECT * FROM top_user")
table9=cursor.fetchall()
top_user=pd.DataFrame(table9,columns=("States","Years","Quarter","RegisteredUsers","Pincodes"))



# Close cursor
cursor.close()

# Close connection
connection.close()

#################################################################################################################################


#1
#Creating the TACY(Transcation amount count Year ) Function

def Transcation_amount_count_Y(df, year):
    tacy=df[df["Years"] ==year]
    #tacy["Years"].unique()
    tacy.reset_index(drop=True,inplace=True)

    #tacy.reset_index(drop=True, inplace=True)
    tacyg = tacy.groupby("States")[["Transcation_amount","Transcation_count"]].sum().reset_index()
    tacyg.reset_index(inplace= True)


    

    #Transcation Amount
    

    fig_amount= px.bar(tacyg, x="States", y="Transcation_amount", title=f"{year}  Transcation amount")
    st.plotly_chart(fig_amount)

    #Transcation Count
    
            
    fig_count = px.bar(tacyg, x="States", y="Transcation_count", title=f"{year} Transcation count", color_discrete_sequence=px.colors.sequential.Viridis)
                               
    st.plotly_chart(fig_count)


    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)
    states=[]
    for feature in data1["features"]:
            states.append(feature["properties"]["ST_NM"])

    states.sort()

    fig_india_1= px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey="properties.ST_NM", color= "Transcation_amount", color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transcation_amount"].min(), tacyg["Transcation_amount"].max()),
                                hover_name="States", title= f"{year} TRANSCATION AMOUNT", fitbounds= "locations",
                                height=400, width=650)
    
    fig_india_2= px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey="properties.ST_NM", color= "Transcation_count", color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transcation_count"].min(), tacyg["Transcation_count"].max()),
                                hover_name="States", title= f"{year} TRANSCATION AMOUNT", fitbounds= "locations",
                                height=400, width=650)
    
    fig_india_1.update_geos(visible= False)

    fig_india_2.update_geos(visible= False)

    st.plotly_chart(fig_india_1)
    
    st.plotly_chart(fig_india_2)
    return tacy


###################################################################################################################################################################################


#2
#Creating the TACY(Transcation amount count Year ) Function for QUARTERS 

def Transcation_amount_count_Y_Quarter(df,quarter):
    tacy=df[df["Quarter"] ==quarter]
    #tacy["Years"].unique()
    tacy.reset_index(drop=True,inplace=True)

    
    tacyg = tacy.groupby("States")[["Transcation_amount","Transcation_count"]].sum().reset_index()
    tacyg.reset_index(drop=True, inplace=True)

    #Transcation Amount
    fig_amount= px.bar(tacyg, x="States", y="Transcation_amount", title=f"{tacy['Years'].min()} YEAR{quarter} QUARTER TRANSCATION AMOUNT"
,
                            height=400, width=800)

    st.plotly_chart(fig_amount)

    #Transcation Count
    fig_count = px.bar(tacyg, x="States", y="Transcation_count", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSCATON COUNT"
, color_discrete_sequence=px.colors.sequential.Viridis,
                                height=400, width=800)
    st.plotly_chart(fig_count)


    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)
    states=[]
    for feature in data1["features"]:
            states.append(feature["properties"]["ST_NM"])

    states.sort()

    fig_india_1= px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey="properties.ST_NM", color= "Transcation_amount", color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transcation_amount"].min(), tacyg["Transcation_amount"].max()),
                                hover_name="States", title= f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSCATION AMOUNT", fitbounds= "locations",
                                height=400, width=650)
    
    fig_india_2= px.choropleth(tacyg, geojson= data1, locations= "States", featureidkey="properties.ST_NM", color= "Transcation_count", color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transcation_count"].min(), tacyg["Transcation_count"].max()),
                                hover_name="States", title= f"{tacy['Years'].min()} {quarter} QUARTER TRANSCATION COUNT", fitbounds= "locations",
                                height=400, width=650)
    
    fig_india_1.update_geos(visible= False)

    fig_india_2.update_geos(visible= False)

    st.plotly_chart(fig_india_1)
    
    st.plotly_chart(fig_india_2)

    return tacy


##################################################################################################################################################


# 3 PIE CHART FUNCTION TRANSCATION TYPE

def Transcation_type_piechart(df, state):

    tacy = df[df["States"] == state]
    tacy.reset_index(drop=True, inplace=True)
    tacyg = tacy.groupby("Transcation_type")[["Transcation_amount", "Transcation_count"]].sum().reset_index()
    tacyg.reset_index(drop=True, inplace=True)

    # Define a color sequence
    color_sequence = px.colors.qualitative.Plotly

    # Pie chart code 
    fig_piechart_1 = px.pie(data_frame=tacyg, 
                            names="Transcation_type", 
                            values="Transcation_amount",
                            width=500, 
                            title=f"{state} Transcation Amount", 
                            hole=0.5,
                            color_discrete_sequence=color_sequence)

    fig_piechart_2 = px.pie(data_frame=tacyg, 
                            names="Transcation_type", 
                            values="Transcation_count",
                            width=500, 
                            title=f"{state} Transcation Count", 
                            hole=0.5,
                            color_discrete_sequence=color_sequence)

    st.plotly_chart(fig_piechart_1)
    st.plotly_chart(fig_piechart_2)
    return tacyg


#################################################################################################################################################

# Aggregated User analysis (Brands)

def aggregated_user_plot_1(df, year):
    aguy= df[df["Years"]== year]
    aguy.reset_index(drop=True, inplace=True)

    aguygrouped= pd.DataFrame(aguy.groupby("Brands")[["Transcation_count", "Percentage"]].sum())
    aguygrouped.reset_index(inplace=True)
    #aguygrouped

    fig_bar_1=px.bar(aguygrouped, x= "Brands",
                    y= "Transcation_count",
                    title=f"{year} Brands and their Transcation",
                    width=650, height=550,
                    color_discrete_sequence=px.colors.sequential.Oranges_r)

    st.plotly_chart(fig_bar_1)

    return aguy

#####################################################################################################################################################

#Aggregated user analysis 2 based on quarter

def Aggre_user_plot_2(df, quarter):
    aguyq= df[df["Quarter"]== quarter]
    aguyq.reset_index(drop=True, inplace=True)

    aguyqg=pd.DataFrame(aguyq.groupby("Brands")["Transcation_count"].sum())
    aguyqg.reset_index(inplace= True)

    fig_bar_2=px.bar(   aguyqg, x= "Brands",
                        y= "Transcation_count",
                        title=f"{quarter} Quarter Brands and their Transcation",
                        width=650, height=650,
                        color_discrete_sequence=px.colors.sequential.Oranges_r  )

    st.plotly_chart(fig_bar_2)
    return aguyq

#####################################################################################################################################################
# Aggregated user analysis 3 

def Aggre_user_plot_3(df, state):
    auyqs=df[df["States"]== state]
    auyqs.reset_index(drop= True, inplace= True)

    fig_line_1= px.line(auyqs, x="Brands",
                        y="Transcation_count",
                        hover_data="Percentage",
                        title= "Brands, Transcation count and their percentage",
                        width=650, height=650,
                        color_discrete_sequence=px.colors.sequential.Oranges_r,
                        markers= True,
                        )


    st.plotly_chart(fig_line_1)
    return auyqs

#################################################################################################################################################

#Map_insurance_district
def Map_insur_District(df, state):

    tacy= df[df["States"] == state]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("Districts")[["Transcation_count","Transcation_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_bar_1= px.bar(tacyg, 
                          x= "Transcation_amount", 
                          y= "Districts", orientation= "h", height= 600, width= 600,
                          title= f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", 
                          color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)

    with col2:

        fig_bar_2= px.bar(tacyg, 
                          x= "Transcation_count", y= "Districts",  
                          height= 600,width= 600,
                          title= f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence= px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_bar_2)

        return tacyg

###################################################################################################################################################

# map_user_plot_1

def map_user_plot_1(df, year):
    muy= df[df["Years"]== year]
    muy.reset_index(drop= True, inplace= True)

    muyg= muy.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_line_1= px.line(muyg, 
                        x= "States", y= ["RegisteredUser", "AppOpens"],
                        title= f"{year} REGISTERED USER, APPOPENS",
                        width= 650, height= 650, 
                        markers= True)
    st.plotly_chart(fig_line_1)
    return muy

########################################################################################################################################################
# map_user_plot_2


def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"]== quarter]
    muyq.reset_index(drop= True, inplace= True)

    muyqg= muyq.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_line_1= px.line(muyqg, 
                        x= "States", y= ["RegisteredUser", "AppOpens"],
                        title= f"{df['Years'].min()} YEARS {quarter} QUARTER REGISTERED USER, APPOPENS",
                        width= 600, height= 700, 
                        markers= True,
                        color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)

    return muyq
###########################################################################################################################
#Map user according to year

def map_user_histoplot_3(df, year): # comes under user 1 code 

    # Filter map_user DataFrame for the year 2021
    muy = df[df["Years"] == year]
    muy.reset_index(drop=True, inplace=True)

    # Group by states and sum the registered users and app opens
    muygrouped = muy.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muygrouped.reset_index(inplace=True)

    # Create a histogram with Plotly
    fig_histo_1 = px.histogram(muygrouped, 
                            x="States", 
                            y=["RegisteredUsers", "AppOpens"],
                            title=f"{year} RegisteredUsers and AppOpen according to map",
                            width=1000, 
                            height=950,
                            barmode='group',  # Group bars
                            color_discrete_sequence=px.colors.sequential.Rainbow_r)

    # Show the figure
    st.plotly_chart(fig_histo_1)

    return muy
###########################################################################################################################
#Map user according to quarter


def map_user_histoplot_quarter_2(df, quarter): # comes under user 2 code used for quarter

    # Filter map_user DataFrame for the year 2021
    muyq = df[df["Quarter"] == quarter]
    muyq.reset_index(drop=True, inplace=True)

    # Group by states and sum the registered users and app opens
    muyqgrouped = muyq.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyqgrouped.reset_index(inplace=True)

    # Create a histogram with Plotly
    fig_histo_1 = px.histogram(muyqgrouped, 
                            x="States", 
                            y=["RegisteredUsers", "AppOpens"],
                            title=f"{quarter} th Quarter RegisteredUsers and AppOpen according to map",
                            width=950, 
                            height=900,
                            barmode='group',  # Group bars
                            color_discrete_sequence=px.colors.sequential.Rainbow_r)

    
    st.plotly_chart(fig_histo_1)

    return muyq

#########################################################################################################################################################

# REGISTERED USERS AND APP OPENS BASED ON STATES 


def map_user_histoplot_4(df, states): # BASED ON STATES AND DISTRICTS 
    muyqs= df[df["States"]==states]
    muyqs.reset_index(drop=True, inplace=True)
    muyqs

    fig_map_user_bar_1=px.bar(muyqs,
                            x="RegisteredUsers",
                            y="Districts",
                            orientation="h",
                            title="Registered Users",
                            height= 750,
                            width=950,
                            color_discrete_sequence=px.colors.sequential.Rainbow_r)


    fig_map_user_bar_2=px.bar(muyqs,
                            x="AppOpens",
                            y="Districts",
                            orientation="h",
                            title="APP OPENS",
                            height= 750,
                            width=950,
                            color_discrete_sequence=px.colors.sequential.Rainbow_r)

    st.plotly_chart(fig_map_user_bar_1)
    st.plotly_chart(fig_map_user_bar_2)

    return muyqs

########################################################################################################################################################

# Top insurance based on sataes 1 

def Top_insurance_plot_1(df, state):
    tiy= df[df["States"]==state]
    tiy.reset_index(drop=True, inplace=True)
    

    # Top Insurance plot

    fig_top_insurance_bar_1=px.bar(tiy,
                                x="Quarter",
                                y="Transcation_amount",
                                #orientation="h",
                                title="TRANSCATION AMOUNT",
                                hover_data= "Pincodes",
                                height= 750,
                                width=950,
                                color_discrete_sequence=px.colors.sequential.Rainbow_r)
    
    fig_top_insurance_bar_2=px.bar(tiy,
                                x="Quarter",
                                y="Transcation_count",
                                #orientation="h",
                                title="TRANSCATION COUNT",
                                hover_data= "Pincodes",
                                height= 750,
                                width=950,
                                color_discrete_sequence=px.colors.sequential.Rainbow_r)

    st.plotly_chart(fig_top_insurance_bar_1)
    st.plotly_chart(fig_top_insurance_bar_2)

    return tiy

######################################################################################################################################################

#TOP TRANSCATION BASED ON STATES AND THE QUARTERS

def Top_transcation_plot_1(df, state):
    
    tt = df[df["States"] == state]
    tt.reset_index(drop=True, inplace=True)

    # Create a scatter plot
    tt_scatter_plot = px.scatter(
        tt,
        x="Quarter",  
        y="Transcation_amount",  
        title=f"Transaction Amounts Over Quarters in {state}",
        color="Years",  
        hover_data=["Transcation_amount"],
        size="Transcation_amount",  
        color_continuous_scale=px.colors.sequential.Rainbow_r
    )

    st.plotly_chart(tt_scatter_plot)
########################################################################################################################################################

# top_user_plot_1
def top_user_plot_1(df, year):
    tuy= df[df["Years"]== year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["States", "Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x= "States", y= "RegisteredUsers", color= "Quarter", width= 1000, height= 800,
                        color_discrete_sequence= px.colors.sequential.Burgyl, hover_name= "States",
                        title= f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)

    return tuy

################################################################################################################################################################

# top_user_plot_2
def top_user_plot_2(df, state):
    tuys= df[df["States"]== state]
    tuys.reset_index(drop= True, inplace= True)

    fig_top_pot_2= px.bar(tuys, x= "Quarter", y= "RegisteredUsers", title= "REGISTEREDUSERS, PINCODES, QUARTER",
                        width= 1000, height= 800, color= "RegisteredUsers", hover_data= "Pincodes",
                        color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_pot_2)

##################################################################################################################################################################

#########################################################  QUESTIONS CODE  #########################################################################

# Top chart transcation amount
def top_chart_transcation_amount(table_name):
    connection_params = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'Lolptw@123',
        'database': 'Phonepe_viz'
    }

    # Establish connection
    connection = mysql.connector.connect(**connection_params)
    cursor = connection.cursor()

    try:
        # Query for the first plot
        query1 = f'''
        SELECT states, SUM(transcation_amount) AS transcation_amount
        FROM {table_name}
        GROUP BY states
        ORDER BY transcation_amount DESC
        LIMIT 10;
        '''
        cursor.execute(query1)
        table_1 = cursor.fetchall()
        connection.commit()

        df_1 = pd.DataFrame(table_1, columns=("states", "transcation_amount"))

        col1, col2 = st.columns(2)
        with col1:
            fig_amount = px.bar(df_1, x="states", y="transcation_amount", title="TOP 10 OF TRANSCATION AMOUNT", hover_name="states",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)
            st.plotly_chart(fig_amount)

        # Query for the second plot
        query2 = f'''
        SELECT states, SUM(transcation_amount) AS transcation_amount
        FROM {table_name}
        GROUP BY states
        ORDER BY transcation_amount
        LIMIT 10;
        '''
        cursor.execute(query2)
        table_2 = cursor.fetchall()
        connection.commit()

        df_2 = pd.DataFrame(table_2, columns=("states", "transcation_amount"))

        with col2:
            fig_amount_2 = px.bar(df_2, x="states", y="transcation_amount", title="LAST 10 OF TRANSCATION AMOUNT", hover_name="states",
                                  color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)
            st.plotly_chart(fig_amount_2)

        # Query for the third plot
        query3 = f'''
        SELECT states, AVG(transcation_amount) AS transcation_amount
        FROM {table_name}
        GROUP BY states
        ORDER BY transcation_amount;
        '''
        cursor.execute(query3)
        table_3 = cursor.fetchall()
        connection.commit()

        df_3 = pd.DataFrame(table_3, columns=("states", "transcation_amount"))

        fig_amount_3 = px.bar(df_3, y="states", x="transcation_amount", title="AVERAGE OF TRANSCATION AMOUNT", hover_name="states", orientation="h",
                              color_discrete_sequence=px.colors.sequential.Bluered_r, height=800, width=1000)
        st.plotly_chart(fig_amount_3)

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()


###############################################################################################################################################

# Top chart transcation count
def top_chart_transaction_count(table_name):
    connection_params = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'Lolptw@123',
        'database': 'Phonepe_viz' 
    }

    # Establish connection
    connection = mysql.connector.connect(**connection_params)
    cursor = connection.cursor()

    try:
        # Query for the first plot
        query1 = f'''
        SELECT states, SUM(transaction_count) AS transaction_count
        FROM {table_name}
        GROUP BY states
        ORDER BY transaction_count DESC
        LIMIT 10;
        '''
        cursor.execute(query1)
        table_1 = cursor.fetchall()

        df_1 = pd.DataFrame(table_1, columns=("states", "transaction_count"))

        col1, col2 = st.columns(2)
        with col1:
            fig_amount = px.bar(df_1, x="states", y="transaction_count", title="TOP 10 OF TRANSACTION COUNT", hover_name="states",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)
            st.plotly_chart(fig_amount)

        # Query for the second plot
        query2 = f'''
        SELECT states, SUM(transaction_count) AS transaction_count
        FROM {table_name}
        GROUP BY states
        ORDER BY transaction_count
        LIMIT 10;
        '''
        cursor.execute(query2)
        table_2 = cursor.fetchall()

        df_2 = pd.DataFrame(table_2, columns=("states", "transaction_count"))

        with col2:
            fig_amount_2 = px.bar(df_2, x="states", y="transaction_count", title="LAST 10 OF TRANSACTION COUNT", hover_name="states",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)
            st.plotly_chart(fig_amount_2)

        # Query for the third plot
        query3 = f'''
        SELECT states, AVG(transaction_count) AS transaction_count
        FROM {table_name}
        GROUP BY states
        ORDER BY transaction_count;
        '''
        cursor.execute(query3)
        table_3 = cursor.fetchall()

        df_3 = pd.DataFrame(table_3, columns=("states", "transaction_count"))

        fig_amount_3 = px.bar(df_3, y="states", x="transaction_count", title="AVERAGE OF TRANSACTION COUNT", hover_name="states", orientation="h",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, height=800, width=1000)
        st.plotly_chart(fig_amount_3)

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

####################################################################################################################################################

def top_chart_registered_user(table_name, state):
    connection_params = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'Lolptw@123',
        'database': 'Phonepe_viz'
    }

    # Establish connection
    connection = mysql.connector.connect(**connection_params)
    cursor = connection.cursor()

    try:
        # Query for the first plot
        query1 = f'''
                SELECT districts, SUM(RegisteredUsers) AS RegisteredUsers
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY RegisteredUsers DESC
                LIMIT 10;
        '''
        cursor.execute(query1)
        table_1 = cursor.fetchall()
        connection.commit()

        df_1 = pd.DataFrame(table_1, columns=("districts", "RegisteredUsers"))

        col1, col2 = st.columns(2)
        with col1:
             fig_amount= px.bar(df_1,
                                 x="districts", y="RegisteredUsers", 
                                 title="TOP 10 OF REGISTERED USER", 
                                 hover_name= "districts",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)
            

        # Query for the second plot
        query2 = f'''SELECT districts, SUM(RegisteredUsers) AS RegisteredUsers
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY RegisteredUsers
                LIMIT 10;
        '''
        cursor.execute(query2)
        table_2 = cursor.fetchall()
        connection.commit()

        df_2 = pd.DataFrame(table_2, columns=("districts", "RegisteredUsers"))

        with col2:
            fig_amount_2= px.bar(df_2, 
                                 x="districts", y="RegisteredUsers", 
                                 title="LAST 10 REGISTERED USER", 
                                 hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

        # Query for the third plot
        query3 = f'''
        SELECT districts, AVG(RegisteredUsers) AS RegisteredUsers
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY RegisteredUsers;
        '''
        cursor.execute(query3)
        table_3 = cursor.fetchall()
        connection.commit()

        df_3 = pd.DataFrame(table_3, columns=("districts", "RegisteredUsers"))

        fig_amount_3= px.bar(df_3, y="districts", x="RegisteredUsers", title="AVERAGE OF REGISTERED USER", hover_name= "districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
        st.plotly_chart(fig_amount_3)

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()








#####################################################################################################################################################
def top_chart_appopens(table_name, state):
    connection_params = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'Lolptw@123',
        'database': 'Phonepe_viz'
    }

    # Establish connection
    connection = mysql.connector.connect(**connection_params)
    cursor = connection.cursor()

    try:
        # Query for the first plot
        query1 = f'''
        SELECT districts, SUM(appopens) AS appopens
        FROM {table_name}
        WHERE states= '{state}'
        GROUP BY districts
        ORDER BY appopens DESC
        LIMIT 10;
        '''
        cursor.execute(query1)
        table_1 = cursor.fetchall()

        df_1 = pd.DataFrame(table_1, columns=("districts", "appopens"))

        col1, col2 = st.columns(2)
        with col1:
            fig_amount = px.bar(df_1, x="districts", y="appopens", title="TOP 10 OF APPOPENS", hover_name="districts",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)
            st.plotly_chart(fig_amount)

        # Query for the second plot
        query2 = f'''
        SELECT districts, SUM(appopens) AS appopens
        FROM {table_name}
        WHERE states= '{state}'
        GROUP BY districts
        ORDER BY appopens
        LIMIT 10;
        '''
        cursor.execute(query2)
        table_2 = cursor.fetchall()

        df_2 = pd.DataFrame(table_2, columns=("districts", "appopens"))

        with col2:
            fig_amount_2 = px.bar(df_2, x="districts", y="appopens", title="LAST 10 APPOPENS", hover_name="districts",
                                  color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)
            st.plotly_chart(fig_amount_2)

        # Query for the third plot
        query3 = f'''
        SELECT districts, AVG(appopens) AS appopens
        FROM {table_name}
        WHERE states= '{state}'
        GROUP BY districts
        ORDER BY appopens;
        '''
        cursor.execute(query3)
        table_3 = cursor.fetchall()

        df_3 = pd.DataFrame(table_3, columns=("districts", "appopens"))

        fig_amount_3 = px.bar(df_3, y="districts", x="appopens", title="AVERAGE OF APPOPENS", hover_name="districts", orientation="h",
                              color_discrete_sequence=px.colors.sequential.Bluered_r, height=800, width=1000)
        st.plotly_chart(fig_amount_3)

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

#####################################################################################################################################################


def top_chart_registered_users(table_name):
    connection_params = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'Lolptw@123',
        'database': 'Phonepe_viz'
    }

    # Establish connection
    connection = mysql.connector.connect(**connection_params)
    cursor = connection.cursor()

    try:
        # Query for the first plot
        query1 = f'''
                SELECT states, SUM(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers DESC
                LIMIT 10;
        '''
        cursor.execute(query1)
        table_1 = cursor.fetchall()
        connection.commit()

        df_1 = pd.DataFrame(table_1, columns=("states", "registeredusers"))

        col1, col2 = st.columns(2)
        with col1:
             fig_amount= px.bar(df_1, x="states", y="registeredusers", title="TOP 10 OF REGISTERED USERS", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)
            

        # Query for the second plot
        query2 = f'''SELECT states, SUM(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers
        
                LIMIT 10;
        '''
        cursor.execute(query2)
        table_2 = cursor.fetchall()
        connection.commit()

        df_2 = pd.DataFrame(table_2, columns=("states", "registeredusers"))

        with col2:
            fig_amount_2= px.bar(df_2, x="states", y="registeredusers", title="LAST 10 REGISTERED USERS", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

        # Query for the third plot
        query3 = f'''
        SELECT states, AVG(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers;
        '''
        cursor.execute(query3)
        table_3 = cursor.fetchall()
        connection.commit()

        df_3 = pd.DataFrame(table_3, columns=("states", "registeredusers"))

        fig_amount_3= px.bar(df_3, y="states", x="registeredusers", title="AVERAGE OF REGISTERED USERS", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
        st.plotly_chart(fig_amount_3)

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()
##############################################################################################################################################
def top_chart_transaction_countq3(table_name): # for q3 tac
    connection_params = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'Lolptw@123',
        'database': 'Phonepe_viz' 
    }

    # Establish connection
    connection = mysql.connector.connect(**connection_params)
    cursor = connection.cursor()

    try:
        # Query for the first plot
        query1 = f'''
        SELECT states, SUM(transcation_count) AS transaction_count
        FROM {table_name}
        GROUP BY states
        ORDER BY transaction_count DESC
        LIMIT 10;
        '''
        cursor.execute(query1)
        table_1 = cursor.fetchall()

        df_1 = pd.DataFrame(table_1, columns=("states", "transaction_count"))

        col1, col2 = st.columns(2)
        with col1:
            fig_amount = px.bar(df_1, x="states", y="transaction_count", title="TOP 10 OF TRANSACTION COUNT", hover_name="states",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)
            st.plotly_chart(fig_amount)

        # Query for the second plot
        query2 = f'''
        SELECT states, SUM(transcation_count) AS transaction_count
        FROM {table_name}
        GROUP BY states
        ORDER BY transaction_count
        LIMIT 10;
        '''
        cursor.execute(query2)
        table_2 = cursor.fetchall()

        df_2 = pd.DataFrame(table_2, columns=("states", "transaction_count"))

        with col2:
            fig_amount_2 = px.bar(df_2, x="states", y="transaction_count", title="LAST 10 OF TRANSACTION COUNT", hover_name="states",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)
            st.plotly_chart(fig_amount_2)

        # Query for the third plot
        query3 = f'''
        SELECT states, AVG(transcation_count) AS transaction_count
        FROM {table_name}
        GROUP BY states
        ORDER BY transaction_count;
        '''
        cursor.execute(query3)
        table_3 = cursor.fetchall()

        df_3 = pd.DataFrame(table_3, columns=("states", "transaction_count"))

        fig_amount_3 = px.bar(df_3, y="states", x="transaction_count", title="AVERAGE OF TRANSACTION COUNT", hover_name="states", orientation="h",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, height=800, width=1000)
        st.plotly_chart(fig_amount_3)

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()      

#####################################################################################################################################################

def top_chart_transcation_amountq4(table_name):
    connection_params = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'Lolptw@123',
        'database': 'Phonepe_viz'
    }

    # Establish connection
    connection = mysql.connector.connect(**connection_params)
    cursor = connection.cursor()

    try:
        # Query for the first plot
        query1 = f'''
        SELECT states, SUM(transaction_amount) AS transaction_amount
        FROM {table_name}
        GROUP BY states
        ORDER BY transaction_amount DESC
        LIMIT 10;
        '''
        cursor.execute(query1)
        table_1 = cursor.fetchall()
        connection.commit()

        df_1 = pd.DataFrame(table_1, columns=("states", "transaction_amount"))

        col1, col2 = st.columns(2)
        with col1:
            fig_amount = px.bar(df_1, x="states", y="transaction_amount", title="TOP 10 OF TRANSCATION AMOUNT", hover_name="states",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)
            st.plotly_chart(fig_amount)

        # Query for the second plot
        query2 = f'''
        SELECT states, SUM(transaction_amount) AS transaction_amount
        FROM {table_name}
        GROUP BY states
        ORDER BY transaction_amount
        LIMIT 10;
        '''
        cursor.execute(query2)
        table_2 = cursor.fetchall()
        connection.commit()

        df_2 = pd.DataFrame(table_2, columns=("states", "transaction_amount"))

        with col2:
            fig_amount_2 = px.bar(df_2, x="states", y="transaction_amount", title="LAST 10 OF TRANSCATION AMOUNT", hover_name="states",
                                  color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)
            st.plotly_chart(fig_amount_2)

        # Query for the third plot
        query3 = f'''
        SELECT states, AVG(transaction_amount) AS transaction_amount
        FROM {table_name}
        GROUP BY states
        ORDER BY transaction_amount;
        '''
        cursor.execute(query3)
        table_3 = cursor.fetchall()
        connection.commit()

        df_3 = pd.DataFrame(table_3, columns=("states", "transaction_amount"))

        fig_amount_3 = px.bar(df_3, y="states", x="transaction_amount", title="AVERAGE OF TRANSCATION AMOUNT", hover_name="states", orientation="h",
                              color_discrete_sequence=px.colors.sequential.Bluered_r, height=800, width=1000)
        st.plotly_chart(fig_amount_3)

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()


###############################################################################################################################################

# Top chart transcation count
def top_chart_transaction_countq4(table_name):
    connection_params = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'Lolptw@123',
        'database': 'Phonepe_viz' 
    }

    # Establish connection
    connection = mysql.connector.connect(**connection_params)
    cursor = connection.cursor()

    try:
        # Query for the first plot
        query1 = f'''
        SELECT states, SUM(transaction_count) AS transaction_count
        FROM {table_name}
        GROUP BY states
        ORDER BY transaction_count DESC
        LIMIT 10;
        '''
        cursor.execute(query1)
        table_1 = cursor.fetchall()

        df_1 = pd.DataFrame(table_1, columns=("states", "transaction_count"))

        col1, col2 = st.columns(2)
        with col1:
            fig_amount = px.bar(df_1, x="states", y="transaction_count", title="TOP 10 OF TRANSACTION COUNT", hover_name="states",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)
            st.plotly_chart(fig_amount)

        # Query for the second plot
        query2 = f'''
        SELECT states, SUM(transaction_count) AS transaction_count
        FROM {table_name}
        GROUP BY states
        ORDER BY transaction_count
        LIMIT 10;
        '''
        cursor.execute(query2)
        table_2 = cursor.fetchall()

        df_2 = pd.DataFrame(table_2, columns=("states", "transaction_count"))

        with col2:
            fig_amount_2 = px.bar(df_2, x="states", y="transaction_count", title="LAST 10 OF TRANSACTION COUNT", hover_name="states",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height=650, width=600)
            st.plotly_chart(fig_amount_2)

        # Query for the third plot
        query3 = f'''
        SELECT states, AVG(transaction_count) AS transaction_count
        FROM {table_name}
        GROUP BY states
        ORDER BY transaction_count;
        '''
        cursor.execute(query3)
        table_3 = cursor.fetchall()

        df_3 = pd.DataFrame(table_3, columns=("states", "transaction_count"))

        fig_amount_3 = px.bar(df_3, y="states", x="transaction_count", title="AVERAGE OF TRANSACTION COUNT", hover_name="states", orientation="h",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, height=800, width=1000)
        st.plotly_chart(fig_amount_3)

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()



##################################################################################################################################################################################
##################################################################################################################################################################################


#Straeamlit part

st.set_page_config(layout="wide")
st.title("PhonePe Data Viz and Exploration")
with st.sidebar:
    select=option_menu("Main Menu",["HOME", "DATA EXPLORATION", "TOP CHARTS"])

if select=="HOME":
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")


elif select=="DATA EXPLORATION":
    tab1, tab2, tab3= st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])

    with tab1:

        method=st.radio("Select The Method",["Insurance Analysis","Transcation Analysis","User Analysis"])
##########################################
        if method == "Insurance Analysis":
            years=st.slider("Select Year",aggregated_insurance["Years"].min(),aggregated_insurance["Years"].max(), aggregated_insurance["Years"].min())
            tac_y=Transcation_amount_count_Y(aggregated_insurance,years)

            col1,col2=st.columns(2)
            with col1:
                 quarters=st.slider("Select Quarter",tac_y["Quarter"].min(),tac_y["Quarter"].max(), tac_y["Quarter"].min())

            Transcation_amount_count_Y_Quarter(tac_y, quarters)

############################################            

        elif method =="Transcation Analysis":
            

            if method == "Transcation Analysis":
                years=st.slider("Select Year",aggregated_transcation["Years"].min(),aggregated_transcation["Years"].max(), aggregated_transcation["Years"].min())
                Aggregaed_tac_y=Transcation_amount_count_Y(aggregated_transcation,years)

                col1,col2= st.columns(2)
                with col1:
                    states=st.selectbox("Select the states",Aggregaed_tac_y["States"].unique())

                    Transcation_type_piechart(Aggregaed_tac_y, states)


                col1,col2=st.columns(2)
            with col1:
                    quarters=st.slider("Select Quarter",Aggregaed_tac_y["Quarter"].min(),Aggregaed_tac_y["Quarter"].max(), Aggregaed_tac_y["Quarter"].min())

                    Aggregated_Transcation_Y_Q= Transcation_amount_count_Y_Quarter(Aggregaed_tac_y, quarters)

                
            col1,col2= st.columns(2)
            with col1:
                    states=st.selectbox("Select the states_ty",Aggregated_Transcation_Y_Q["States"].unique())

                    Transcation_type_piechart(Aggregated_Transcation_Y_Q, states)


######################################
        elif method =="User Analysis":
            col1,col2=st.columns(2)
            with col1:
                years=st.slider("Select Year",aggregated_user["Years"].min(),aggregated_user["Years"].max(), aggregated_user["Years"].min())
                Aggregated_user_year =aggregated_user_plot_1(aggregated_user,years)


        col1,col2=st.columns(2)
        with col1:
                    quarters=st.slider("Select Quarter",Aggregated_user_year["Quarter"].min(),Aggregated_user_year["Quarter"].max(), Aggregated_user_year["Quarter"].min())

                    Aggregated_user_year_quarter= Aggre_user_plot_2(Aggregated_user_year, quarters)


        col1,col2= st.columns(2)
        with col1:
                    states=st.selectbox("Select the states",Aggregated_user_year_quarter["States"].unique())

                    Aggre_user_plot_3(Aggregated_user_year_quarter, states)



#############################################################################################
    with tab2:

        method_2=st.radio("Select the method",["Map Insurance","Map Transcation","Map User"])

        if method_2 == "Map Insurance":

            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_mi",map_insurance["Years"].min(), map_insurance["Years"].max(),map_insurance["Years"].min())

                map_insur_tac_Y= Transcation_amount_count_Y(map_insurance, years)


            col1,col2= st.columns(2)
            with col1:
                    states= st.selectbox("Select The State_mi", map_insur_tac_Y["States"].unique())

                    Map_insur_District(map_insur_tac_Y, states)
        
            col1,col2= st.columns(2)
            with col1:

                    quarters= st.slider("Select The Quarter_mi",map_insur_tac_Y["Quarter"].min(), map_insur_tac_Y["Quarter"].max(),map_insur_tac_Y["Quarter"].min())

                    map_insur_tac_Y_Q= Transcation_amount_count_Y_Quarter(map_insur_tac_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                    states= st.selectbox("Select The State_Ty", map_insur_tac_Y_Q["States"].unique())

                    Map_insur_District(map_insur_tac_Y_Q, states)

        elif method_2 == "Map Transcation" :
        

        
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_mi",map_transcation["Years"].min(), map_transcation["Years"].max(),map_transcation["Years"].min())

                map_transcation_tac_Y= Transcation_amount_count_Y(map_transcation, years)


            col1,col2= st.columns(2)
            with col1:
                    states= st.selectbox("Select The State_mi", map_transcation_tac_Y["States"].unique())

                    Map_insur_District(map_transcation_tac_Y, states)
        
            col1,col2= st.columns(2)
            with col1:

                    quarters= st.slider("Select The Quarter_map insurance",map_transcation_tac_Y["Quarter"].min(), map_transcation_tac_Y["Quarter"].max(),map_transcation_tac_Y["Quarter"].min())

                    map_transcation_tac_Y_Q= Transcation_amount_count_Y_Quarter(map_transcation_tac_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_Ty", map_transcation_tac_Y_Q["States"].unique())

                Map_insur_District(map_transcation_tac_Y_Q, states)
###########################################################################################################
        elif method_2 == "Map User" :
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_mi",map_user["Years"].min(), map_user["Years"].max(),map_user["Years"].min())

                Map_user_1_RAP= map_user_histoplot_3(map_user, years)

            col1,col2= st.columns(2)
            with col1:

                    quarters= st.slider("Select The Quarter_mi",Map_user_1_RAP["Quarter"].min(), Map_user_1_RAP["Quarter"].max(),Map_user_1_RAP["Quarter"].min())

                    Map_user_1_RAPQ= map_user_histoplot_quarter_2(Map_user_1_RAP, quarters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_map_user", Map_user_1_RAPQ["States"].unique())

                Map_user__RAPSDY=map_user_histoplot_4(Map_user_1_RAPQ, states)

            
            
            
            



       
             
###############################################################################################           

    

############################################################################################
    with tab3:

        method_3=st.radio("Select the method",["Top Insurance","Top Transcation","Top User"])

        if method_3 == "Top Insurance":
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_top_insurance",top_insurance["Years"].min(), top_insurance["Years"].max(),top_insurance["Years"].min())

                Top_insurance_transcation=Transcation_amount_count_Y(top_insurance,years)


            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_top_insurance_user", Top_insurance_transcation["States"].unique())

                Top_insurance_accroding_to_state_pincode=Top_insurance_plot_1(Top_insurance_transcation, states)


            col1,col2= st.columns(2)
            with col1:

                    quarters= st.slider("Select The Quarter_mi",Top_insurance_transcation["Quarter"].min(), Top_insurance_transcation["Quarter"].max())

                    Top_insurance_transcation_Q= Transcation_amount_count_Y_Quarter(Top_insurance_transcation, quarters)
                 
###########################################################################################################################################################################################################
        elif method_3 =="Top Transcation": # TOP TRASCATION
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_top_transcation",top_transcation["Years"].min(), top_transcation["Years"].max(),top_transcation["Years"].min())

                Top_transcation_YEAR_1=Transcation_amount_count_Y(top_transcation,years)


            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_top_transcation", Top_transcation_YEAR_1["States"].unique())

                Top_insurance_accroding_to_state_pincode=Top_insurance_plot_1(Top_transcation_YEAR_1, states)


            col1,col2= st.columns(2)
            with col1:

                    quarters= st.slider("Select The Quarter_TT",Top_transcation_YEAR_1["Quarter"].min(),Top_transcation_YEAR_1["Quarter"].max(),Top_transcation_YEAR_1["Quarter"].min())

                    Top_transcation_Q= Transcation_amount_count_Y_Quarter(Top_transcation_YEAR_1, quarters)
            
            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_TT", Top_transcation_Q["States"].unique())

                top_transcation_according_to_state_Y_Q=Top_transcation_plot_1(top_transcation, states)


####################################################################################################################################################################################################################
        elif method_3 =="Top User":
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_top_user",top_user["Years"].min(), top_user["Years"].max(),top_user["Years"].min())

                top_user_Y= top_user_plot_1(top_user, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_tu", top_user_Y["States"].unique())

                top_user_plot_2(top_user_Y, states)

########################################################################################################################################################

elif select == "TOP CHARTS":
            question= st.selectbox("Select the Question",["1. Transaction Amount and Count of Aggregated Insurance",
                                                    "2. Transaction Amount and Count of Map Insurance",
                                                    "3. Transaction Amount and Count of Top Insurance",
                                                    "4. Transaction Amount and Count of Aggregated Transaction",
                                                    "5. Transaction Amount and Count of Map Transaction",
                                                    "6. Transaction Amount and Count of Top Transaction",
                                                    "7. Transaction Count of Aggregated User",
                                                    "8. Registered users of Map User",
                                                    "9. App opens of Map User",
                                                    "10. Registered users of Top User",
                                                    ])
    
            if question == "1. Transaction Amount and Count of Aggregated Insurance":

                st.subheader("TRANSACTION AMOUNT")
                top_chart_transcation_amountq4(table_name="Aggregated_Insurance")


            elif question == "2. Transaction Amount and Count of Map Insurance":

                st.subheader("TRANSACTION COUNT")
                top_chart_transcation_amountq4(table_name="Map_Insurance")

            elif question == "3. Transaction Amount and Count of Top Insurance":
        
                st.subheader("TRANSACTION AMOUNT")
                top_chart_transcation_amount("top_insurance")

                st.subheader("TRANSACTION COUNT")
                top_chart_transaction_countq3("top_insurance")

            elif question == "4. Transaction Amount and Count of Aggregated Transaction":
        
                st.subheader("TRANSACTION AMOUNT")
                top_chart_transcation_amountq4("aggregated_transcation")

                st.subheader("TRANSACTION COUNT")
                top_chart_transaction_countq4("aggregated_transcation")

            elif question == "5. Transaction Amount and Count of Map Transaction":
        
                st.subheader("TRANSACTION AMOUNT")
                top_chart_transcation_amount("map_transcation")

                st.subheader("TRANSACTION COUNT")
                top_chart_transaction_countq3("map_transcation")

            elif question == "6. Transaction Amount and Count of Top Transaction":
        
                st.subheader("TRANSACTION AMOUNT")
                top_chart_transcation_amount("top_transcation")

                st.subheader("TRANSACTION COUNT")
                top_chart_transaction_countq3("top_transcation")

            elif question == "7. Transaction Count of Aggregated User":

                st.subheader("TRANSACTION COUNT")
                top_chart_transaction_count("aggregated_user")

            elif question == "8. Registered users of Map User":
        
                states= st.selectbox("Select the State", map_user["States"].unique())   
                st.subheader("REGISTERED USERS")
                top_chart_registered_user("map_user", states)

            elif question == "9. App opens of Map User":
        
                states= st.selectbox("Select the State", map_user["States"].unique())   
                st.subheader("APPOPENS")
                top_chart_appopens("map_user", states)

            elif question == "10. Registered users of Top User":
          
                st.subheader("REGISTERED USERS")
                top_chart_registered_users("top_user")
            
            
