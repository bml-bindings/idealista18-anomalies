"""functions to build all the maps shown in the application

"""
import pandas as pd
import pydeck as pdk
import streamlit as st


CITY_CENTERS = {
    "Madrid": (40.42, -3.69),
    "Barcelona": (41.40, 2.17),
    "Valencia": (39.47, -0.38)
}

MAX_VALUE = 1

SEPARATORS = ["\n", " | ", " | "]

def on_click_fn(e):
    st.write("clicked on %s" % e)


def exclude_fields(field_name):
    return field_name not in ["score", "lon", "lat",
                              "ASSETID", "PRICE", "UNITPRICE"]


@st.cache_resource(max_entries=6, experimental_allow_widgets=True)
def elevation(city, data: pd.DataFrame, threshold) -> None:
    """Map with columns representing field values"""
    lat, lon = CITY_CENTERS[city]
    scale = 500
    radius = 10
    max_ih = MAX_VALUE

    tooltip = ("🔢 anomaly score: {score}\nid: {ASSETID}\n"
               "price: {PRICE}\nunitprice: {UNITPRICE}\n")

    field_names = filter(exclude_fields, data.head())
    for i, field_name in enumerate(field_names):
            index = i % len(SEPARATORS)
            tooltip += "%s %s: {%s}" % (
                SEPARATORS[index], field_name.lower(), field_name)

    max_score = data['score'].max()

    mapbox = pdk.Deck(
        # map_style=None,  # type: ignore
        map_style=pdk.map_styles.SATELLITE,
        map_provider="mapbox",
        initial_view_state=pdk.ViewState(
            latitude=lat, longitude=lon, zoom=12, pitch=40
        ),
        tooltip = {"text": tooltip},
        layers=[
            pdk.Layer(
                "ColumnLayer",
                data,
                get_elevation="score",
                get_fill_color=[
                    # gradient from green to red
                    f"score > 0.5 ? 255*score : 0",
                    f"255*(1-score/{max_score})",
                    f"255*(1-score/{max_score})",
                    "200",
                ],
                get_position=["lon", "lat"],
                elevation_aggregation="MEAN",
                auto_highlight=True,
                elevation_scale=scale,
                radius=radius,
                pickable=True,
                coverage=1,
                on_click=on_click_fn
            )
        ],
    )
    return mapbox
