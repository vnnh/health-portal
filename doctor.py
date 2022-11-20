import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
from util.twilio_interface import call, email
import os
import uuid
import util.table_interpreter as interpreter


def aggrid_interactive_table(df: pd.DataFrame):
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )

    options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )

    return selection


def app():
    patient_data = pd.read_csv(
        "./information.csv"
    )

    st.markdown("### Patient Upload")
    patient_file = st.file_uploader("", key="patient_upload", type=["png"])
    if patient_file is not None:
        temp_path = "./temp/" + str(uuid.uuid4()) + ".png"
        with open(temp_path, "wb") as f:
            f.write(patient_file.read())
        document_text = interpreter.interpret_patient_table(
            temp_path, display=False)
        if os.path.exists(temp_path):
            os.remove(temp_path)
        st.markdown("> Uploaded patient information!")

    st.markdown("### Vaccine Upload")
    vaccine_file = st.file_uploader("", key="vaccine_upload", type=["png"])
    if vaccine_file is not None:
        temp_path = "./temp/" + str(uuid.uuid4()) + ".png"
        with open(temp_path, "wb") as f:
            f.write(vaccine_file.read())
        info = interpreter.interpret_covid_table(
            temp_path, display=False)
        if info:
            for i, v in enumerate(patient_data["Name"]):
                if v == info["first_name"] + " " + info["middle_initial"] + " " + info["last_name"]:
                    copy = patient_data.copy()

                    copy.set_value(i, "Name", info["product_name"])
                    patient_data = copy

        if os.path.exists(temp_path):
            os.remove(temp_path)
        st.markdown("> Uploaded vaccine information!")

    st.markdown("""---""")

    st.markdown("# Patient Database")
    selection = aggrid_interactive_table(df=patient_data)
    if selection['selected_rows']:
        st.markdown("### Patient Information")

        individual_data = selection['selected_rows'][0].copy()
        individual_data.pop("_selectedRowNodeInfo")
        st.json(individual_data)

        st.markdown("""---""")

        
        st.markdown("### Patient Actions")

        if st.button("Call Emergency Contact"):
            call(selection['selected_rows'][0]['Emergency Contact Phone'])
            st.markdown(
                f"> Call sent to {selection['selected_rows'][0]['Emergency Contact Phone']}")

        st.markdown("##")
        patient_message = st.text_input("Patient notes")
        if st.button("Email Patient"):
            email(selection['selected_rows'][0]['Email'], patient_message)
            st.markdown(
                f"> Email sent to {selection['selected_rows'][0]['Email']}")

    st.markdown("""---""")

    st.markdown("# Global Actions")
    if st.button("Email Patients Without the COVID-19 Vaccine"):
        emails = patient_data["Email"]
        vaccines = patient_data["Vaccines"]

        for i, v in enumerate(vaccines):
            if v != v:
                print(emails[i])
                email(emails[i],
                      "Remember to get your COVID-19 vaccines!")

        st.markdown(
            f"> Emails sent!")
