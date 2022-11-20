import streamlit as st
import doctor
import patient


def check_password():
    def password_entered():
        if (
            st.session_state["username"] in st.secrets["users"]
            and st.session_state["password"]
            == st.secrets["users"][st.session_state["username"]]["password"]
        ):
            st.session_state["password_correct"] = True
            st.session_state["type"] = st.secrets["users"][st.session_state["username"]]["type"]
            del st.session_state["password"]
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
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
