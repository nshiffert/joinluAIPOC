import streamlit as st
from snowflake.snowpark import Session

# Function to establish a Snowpark session
@st.cache_resource
def get_snowflake_session():
    # Load connection parameters from Streamlit secrets
    connection_parameters = {
        "account": st.secrets["connections"]["snowflake"]["account"],
        "user": st.secrets["connections"]["snowflake"]["user"],
        "password": st.secrets["connections"]["snowflake"]["password"],
        "warehouse": st.secrets["connections"]["snowflake"]["warehouse"],
        "database": st.secrets["connections"]["snowflake"]["database"],
        "schema": st.secrets["connections"]["snowflake"]["schema"],
        "role": st.secrets["connections"]["snowflake"]["role"]
    }
    return Session.builder.configs(connection_parameters).create()

# Initialize Snowpark session
session = get_snowflake_session()

# Write directly to the app
st.image('https://joinlu.com/assets/img/logo.png?v2')
st.title("JOINLU Ai-Guided Maintenance POC")
st.image('https://s3.amazonaws.com/assets.ottomotors.com/vehicles/product-card-OTTO_100.png', caption='')
st.text('You can now ask any question you like of the LLM in \n regards to fixing the Otto 1500 AMR.\nImagine this app running on a tablet for your maintenance crew\n as they go from robot to robot fixing common problems\n and entering repair logs. Those same repair logs are then\n uploaded to Snowflake and the model \nuses them for the next query.')

# Get user input
question = st.text_input('Question', 'OTTO 1500 agv is not driving straight.  How do I troubleshoot and resolve this issue?')

if st.button(":snowflake: Submit", type="primary"):
    # Create Tabs
    tab1, tab2, tab3 = st.tabs(["1 - Repair Manuals (Only)", "2 - Internal Repair Logs (Only)", "3 - Combined Insights"])

    with tab1:
        # Review Manuals and provide response/recommendation
        manuals_query = f"""
        SELECT * FROM TABLE(REPAIR_MANUALS_LLM('{question}'));
        """
        manuals_response = session.sql(manuals_query).collect()

        st.subheader('Recommended actions from review of maintenance manuals:')
        st.write(manuals_response[0].FILE_NAME)
        st.write(manuals_response[0].RESPONSE)

        st.subheader('Repair manual "chunks" and their relative scores:')    
        st.write(manuals_response)

    with tab2:
	    
        logs_query = f"""SELECT * FROM TABLE(REPAIR_LOGS_LLM('{question}'));"""
        logs_response = session.sql(logs_query).collect()
        st.subheader('Recommended actions from review of repair logs:')
        st.write(logs_response[0].RESPONSE)

        st.subheader('Insights gathered from these most relevant repair logs:')
        st.write(logs_response[0].RELEVANT_REPAIR_LOGS)


    with tab3:
	    
        combined_query = f"""
        SELECT * FROM TABLE(COMBINED_REPAIR_LLM('{question}'));
        """

        combined_response = session.sql(combined_query).collect()

        st.subheader('Combined Recommendations:')
        st.write(logs_response[0].RESPONSE)