# Anomalies geolocation in Idealista18 data

Analyzing the records published in the
🔗 [Idealista post](https://www.idealista.com/labs/blog/?p=4207) to find
anomalous properties. 🔗 [Check it now!](https://idealista18-quality.streamlit.app/)

The data refers to properties sold in 2018 in Madrid, Barcelona and Valencia.
Using BigML, anomaly detector models have been built for each city to
assign an anomaly score. The score ranges from 0, meaning normal, to 1,
meaning totally anomalous, and is based on all the available attributes.
Field values, like the price, unitary price or anomaly score,
are geolocated to help understand the Housing Market distribution
in Madrid, Barcelona and Valencia.
