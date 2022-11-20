import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

iris = pd.read_csv(
    "./information.csv"
)

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


if __name__ == "__main__":
    iris = pd.read_csv(
        "./information.csv"
    )
    selection = aggrid_interactive_table(df=iris)

    if selection:
        st.write("Patient Info:")
        st.json(selection["selected_rows"])

    if st.button("Call Emergency Contact"):
        st.write(f"Call sent to {selection['selected_rows'][0]['Emergency Contact Phone']}")
        