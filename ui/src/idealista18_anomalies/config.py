import os
import typing
import urllib.parse
from datetime import datetime

import pandas as pd
import streamlit as st

APP_NAME = "Idealista18-anomalies"

STREAMLIT_LOGO = "https://github.com/unmonoqueteclea/valencianow/blob/main/ui/res/streamlit-logo.png?raw=true"
BIGML_LOGO = "https://static.bigml.com/static/images/brand_guidelines/bigml_primary_logo@2x.png"
MAPBOX_LOGO = "https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/mapbox-logo-icon.png"
# data sources
DATA_PATH = "./data"

DEFAULT_FIELDS = ["LONGITUDE", "LATITUDE"]



def _preprocess(df: pd.DataFrame) -> typing.Optional[pd.DataFrame]:
    # if dataframe is empty, return None
    if df.shape[0] > 0:
        if "LONGITUDE" in df.columns and "LATITUDE" in df.columns:
            df["lon"] = pd.to_numeric(df["LONGITUDE"])
            df["lat"] = pd.to_numeric(df["LATITUDE"])
            return df.drop(columns=["LONGITUDE", "LATITUDE"])
        return df
    return None


@st.cache_data
def load_data(
    file_prefix: str,
    field_name: typing.Optional[str],
) -> typing.Optional[pd.DataFrame]:
    """Load data from the given local file. """
    filename = os.path.abspath(
        os.path.join(DATA_PATH, f"{file_prefix}_Sale_anomalies.csv"))
    df = pd.read_csv(filename)
    """
        fields = DEFAULT_FIELDS[:]
        fields.append(field_name)
    """
    return _preprocess(df)
