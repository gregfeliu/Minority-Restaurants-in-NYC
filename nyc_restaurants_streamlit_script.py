import streamlit as st
import pandas as pd
import pydeck as pdk


# main function
def main():
    # get data
    garifuna_df = pd.read_csv("garifuna_data.csv", index_col=0)
    ghana_df = pd.read_csv("ghana_data.csv", index_col=0)
    uyghur_df = pd.read_csv("uyghur_data.csv", index_col=0)

    # getting average values so that the map is centered
    latitude_sum = 0
    longitude_sum = 0
    num_of_values = 0
    for df in [ghana_df, garifuna_df, uyghur_df]:
        latitude_sum += sum(df['latitude'].values)
        longitude_sum += sum(df['longitude'].values)
        num_of_values += len(df)
    mid_latitude = latitude_sum / num_of_values
    mid_longitude = longitude_sum / num_of_values

    # title
    st.title("Welcome to my minority ethnic restaurants in NYC project")
    st.write(f"mid lon = {mid_longitude}")
    st.write(f"mid lat = {mid_latitude}")

    # defining layers
    initial_view = pdk.ViewState(
        # map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=mid_latitude,
            longitude=mid_longitude,
            zoom=11,
            pitch=50,))

    scatterplot = pdk.Layer(
        'ScatterplotLayer',
        data=garifuna_df,
        get_position=['longitude', 'latitude'],
        get_color='[200, 30, 0, 160]',
        get_radius=200)

    # printing map
    st.pydeck_chart(
        pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=initial_view,
                        layers=[scatterplot]
                    ))

    st.map(uyghur_df, zoom=12)

if __name__ == '__main__':
    main()
