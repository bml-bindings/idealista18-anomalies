"""idealista18-quality streamlit-based application

Dashboard with geolocation of House Market anomalies based on Idealista data

"""

import typing

import pandas as pd
import plotly.express as px
import streamlit as st

# streamlit-cloud won't install the package, so we can't
# do: from idealista18_quality import config
import config  # type: ignore
import maps  # type: ignore


TAB_DESCRIPTIONS = {
    "score": """Anomaly score for each house or flat.""",
    "price": """Sale price for each house or flat.""",
    "unit price": """Sale price per squared meter for each house or flat."""
}

TAB_LABELS = ["Barcelona", "Madrid", "Valencia"]


def ui_header():
    st.set_page_config(page_title=config.APP_NAME, page_icon="🏘️", layout="wide")
    st.header(f"🏘️ {config.APP_NAME}")
    st.markdown(
        """Anomalous properties in [Idealista18](https://www.idealista.com/labs/blog/?p=4207) data for Madrid, Barcelona and Valencia (Spain)."""
    )
    st.markdown(
        """Built by [BigML](https://bigml.com). Source available in [Github](https://github.com/bigmlcom/idealista18-anomalies).

  Powered by: """
    )
    col1, col2, col3, _ = st.columns([0.10, 0.10, 0.10, 0.70])
    with col1:
        st.image(config.BIGML_LOGO, width=120)
    with col2:
        st.image(config.STREAMLIT_LOGO, width=120)
    with col3:
        st.image(config.MAPBOX_LOGO, width=120)
    st.divider()
    return st.tabs(["Barcelona", "Madrid", "Valencia"])



def ui_tab(tab, label, field_name) -> None:
    with tab:
        st.markdown(
            TAB_DESCRIPTIONS.get(field_name, "")
        )
        data = config.load_data(label, field_name)
        maps_col_1, maps_col_2 = st.columns(2)


        with maps_col_1:
            anomaly_threshold = st.slider(
                "Select an anomaly threshold", 0.0, data["score"].max(), 0.6,
               	 key=label)
            map_data = data[data.score > anomaly_threshold]
            fig = px.histogram(data, x="score",
                               hover_data=data.columns)

            fig.add_vline(x=anomaly_threshold, line_dash = 'dash',
                          line_color = 'black')
            st.plotly_chart(fig, use_container_width=True)
            anomalies_number = map_data.score.count()
            total = data.score.count()
            anomalies_percentage = float(anomalies_number) * 100 / \
                total
            anomalies_percentage = "{:.2f}".format(anomalies_percentage)
            st.write (f"{anomalies_number} ({anomalies_percentage} %) out of "
                      f"{total} properties over that anomaly threshold.")
        with maps_col_2:
            st.pydeck_chart(maps.elevation(label, map_data, anomaly_threshold))


def main() -> None:
    tabs = ui_header()
    for i, tab in enumerate(tabs):
        ui_tab(tab, TAB_LABELS[i], "score")


if __name__ == "__main__":
    main()
