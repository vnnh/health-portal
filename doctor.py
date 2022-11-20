import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
from util.twilio_interface import call, email


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

    st.markdown("# Patient Database")
    selection = aggrid_interactive_table(df=patient_data)
    if selection['selected_rows']:
        st.markdown("### Patient Information")

        individual_data = selection['selected_rows'][0].copy()
        individual_data.pop("_selectedRowNodeInfo")
        st.json(individual_data)

        st.markdown("""---""")

        if st.button("Call Emergency Contact"):
            call(selection['selected_rows'][0]['Emergency Contact Phone'])
            st.markdown(
                f"> Call sent to {selection['selected_rows'][0]['Emergency Contact Phone']}")

        patient_message = st.text_input("Patient notes")
        if st.button("Email Patient"):
            email(selection['selected_rows'][0]['Email'], patient_message)
            st.markdown(f"> Email sent to {selection['selected_rows'][0]['Email']}")
