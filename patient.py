import streamlit as st
import pandas as pd


def app():
    patient_data = pd.read_csv(
        "./information.csv"
    )

    st.markdown("# Patient Portal")

    for i, v in enumerate(patient_data["Name"]):
        if v == st.session_state["name"]:
            patient = patient_data.iloc[i]

    st.json(patient.to_json())

    st.markdown("""---""")
    st.markdown("## Patient Status")

    st.markdown("Patient BMI: " +
                str('%.1f' % ((patient["Weight"]/2.205)/(patient["Height"]/100) ** 2)))

    st.markdown("""---""")
    st.markdown("## Patient Emergency Contacts")
    st.markdown("Emergency Contact Phone: " + patient["Emergency Contact Phone"])
    st.markdown("Emergency Contact Email: " + patient["Emergency Contact Email"])