import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
#login page
def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()
# logout page
def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

# Dashboard development
dashboard = st.Page(
    "utils.py", title="Dashboard", icon=":material/dashboard:", default=True
)
eda_report = st.Page("app.py", title="Generate EDA reports", icon="📊")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Reports": [dashboard, eda_report]
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()