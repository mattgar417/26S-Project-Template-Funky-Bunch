# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has functions to add links to the left sidebar based on the user's role.

import streamlit as st


# ---- General ----------------------------------------------------------------

def home_nav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")

    st.sidebar.page_link("pages/owner.py", label="Venue Dashboard", icon="🏢")



# example---- Role: usaid_worker -----------------------------------------------------

def usaid_worker_home_nav():
    st.sidebar.page_link(
        "pages/10_USAID_Worker_Home.py", label="USAID Worker Home", icon="🏠"
    )


def ngo_directory_nav():
    st.sidebar.page_link("pages/14_NGO_Directory.py", label="NGO Directory", icon="📁")


def add_ngo_nav():
    st.sidebar.page_link("pages/15_Add_NGO.py", label="Add New NGO", icon="➕")


def prediction_nav():
    st.sidebar.page_link(
        "pages/11_Prediction.py", label="Regression Prediction", icon="📈"
    )


def api_test_nav():
    st.sidebar.page_link("pages/12_API_Test.py", label="Test the API", icon="🛜")


def classification_nav():
    st.sidebar.page_link(
        "pages/13_Classification.py", label="Classification Demo", icon="🌺"
    )


# ---- Role: attendee ------------------------------------------------

def attendee_home_nav():
    st.sidebar.page_link("pages/attendee.py", label="Attendee Home", icon="🏠")

def view_events_nav():
    st.sidebar.page_link("pages/view_events.py", label="Browse Events", icon="🔎")

def view_feed_nav():
    st.sidebar.page_link("pages/view_feed.py", label="My Feed", icon="📰")

def view_attendee_events_nav():
    st.sidebar.page_link("pages/view_attendee_events.py", label="My RSVPs", icon="📅")

def view_events_list_nav():
    st.sidebar.page_link("pages/view_events_list.py", label="Saved Events", icon="⭐")

#---- Role: performer ------------------------------------------------


#---- Role: organizer ------------------------------------------------


# ---- Role: Venue Owner ------------------------------------------------


# ---- Sidebar assembly -------------------------------------------------------

def SideBarLinks(show_home=False):
    """
    Renders sidebar navigation links based on the logged-in user's role.
    The role is stored in st.session_state when the user logs in on Home.py.
    """

    # Logo appears at the top of the sidebar on every page
    st.sidebar.image("assets/logo.png", width=150)

    # If no one is logged in, send them to the Home (login) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        home_nav()

    if st.session_state["authenticated"]:
        #example
        if st.session_state["role"] == "pol_strat_advisor":
            pol_strat_home_nav()
            world_bank_viz_nav()
            map_demo_nav()

        if st.session_state["role"] == "attendee":
            attendee_home_nav()
            view_events_nav()
            view_feed_nav()
            view_attendee_events_nav()
            view_events_list_nav()
           
        #if st.session_state["role"] == "performer":
          
        #if st.session_state["role"] == "organizer":
            
            
        #if st.session_state["role"] == "venue_owner":
         

    # About link appears at the bottom for all ro
