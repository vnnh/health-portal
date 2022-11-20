import streamlit as st
import doctor
import patient
from PIL import Image


def check_password():
    def password_entered():
        if (
            st.session_state["username"] in st.secrets["users"]
            and st.session_state["password"]
            == st.secrets["users"][st.session_state["username"]]["password"]
        ):
            st.session_state["password_correct"] = True
            st.session_state["type"] = st.secrets["users"][st.session_state["username"]]["type"]
            st.session_state["name"] = st.secrets["users"][st.session_state["username"]]["name"]
            del st.session_state["password"]
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        _col1, col2, _col3 = st.columns([1, 1, 0.3])
        col2.image(Image.open("./temp/logo.png"), width=80)

        st.markdown("#")
        st.markdown("#")

        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        _col1, col2, _col3 = st.columns([1, 1, 0.3])
        col2.image(Image.open("./temp/logo.png"), width=80)

        st.markdown("#")
        st.markdown("#")

        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("Password incorrect")
        return False
    else:
        return True


if __name__ == "__main__":
    if check_password():
        if st.session_state["type"] == "doctor":
            doctor.app()
        else:
            patient.app()
