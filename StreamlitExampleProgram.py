import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

iris = pd.read_csv(
    "https://raw.githubusercontent.com/vnnh/health-portal/main/information.csv"
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
        "https://raw.githubusercontent.com/vnnh/health-portal/main/information.csv"
    )
    selection = aggrid_interactive_table(df=iris)

    if selection:
        st.write("Patient Info:")
        st.json(selection["selected_rows"])

    messageTextbox = st.text_input("Message:")
    if st.button("Email patient"):
        st.write(f"Email sent to {selection['selected_rows']['email']}")
        