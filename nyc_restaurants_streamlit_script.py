import streamlit as st
import pandas as pd
import pydeck as pdk
from PIL import Image


# main function
def main():
    # get data
    garifuna_df = pd.read_csv("garifuna_data.csv", index_col=0,
                           usecols=['name', 'review_count', 'latitude', 'longitude'])
    ghana_df = pd.read_csv("ghana_data.csv", index_col=0,
                           usecols=['name', 'review_count', 'latitude', 'longitude'])
    uyghur_df = pd.read_csv("uyghur_data.csv", index_col=0,
                           usecols=['name', 'review_count', 'latitude', 'longitude'])

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
    st.title("Measuring Ethnic Neighborhoods in NYC Project")

    # add image that i found and put on medium for this project
    image = Image.open('new_littles.jpeg')
    st.image(image, use_column_width=True, caption="Stylized view of the new 'littles' in NYC")
    # width=850

    # "This project arose from the question:
    st.markdown("**How can you define an ethnic neighborhood?** "
             "In this app, we'll attempt to answer this using the cases of three minority ethnic/national groups in "
             "New York City: the _Garifuna_ (a native American group from Central America), the _Uyghurs_ "
             "(a Turkic group from north-western China) and Ghanaian peoples. Click on the side bar to learn more.")

    st.sidebar.subheader("Click on the approach you would like to learn more about:")
    if st.sidebar.checkbox("Restaurant Approach"):
        st.sidebar.markdown("Restaurants, rightly or wrongly, are one of the main places an ethnic/national group can proudly "
                 "show their identity. By scraping Yelp, I was able to get a list "
                 "of restaurants in NYC that are connected to these groups. After a spot check to make sure the "
                 "restaurants wholey represent that group (one dish out of 20 doesn't make the restaurant"
                 "represent that group), we were left with a list of restaurants for that group. "
                 "This measure is can be a proxy for 'visibility'.")

    if st.sidebar.checkbox("Census Approach"):
        st.sidebar.markdown("Ideally, the census will show us how many people truly live in a specified area. Unfortunately, "
                 "there are multiple problems with this approach. For one, the group chosen on the census "
                 "doesn't always match with the definitions of the groups here. For example, I chose 'Ghanaian peoples' "
                 "as a group here, but many would also consider themselves 'Ga', 'Fulani' or any of the other "
                 "ethnic groups found in Ghana. Another problem concerns the collection of the data itself. "
                 "Many people (understandably) worry about how that data will be used so there is likely significant "
                 "undercounting for recent immigrant groups. Nevertheless, it another approach to defining an "
                 "ethnic neighborhood that restaurants may miss.")


    # announcing map
    st.subheader("Map of restaurants in NYC")
    which_group = st.radio(label="Which group would you like to see on the map?",
                                     options=['Ghanaian peoples', 'Uyghurs', "Garifuna"])
    if which_group == 'Ghanaian peoples':
        data = ghana_df
    elif which_group == 'Uyghurs':
        data = uyghur_df
    elif which_group == "Garifuna":
        data = garifuna_df

    # layers
    scatterplotlayer = pdk.Layer(
                    'ScatterplotLayer',
                    data=data,
                    get_position=['longitude', 'latitude'],
                    get_color='[200, 30, 0, 160]',
                    get_radius=400,
                )
    initial_view_state = pdk.ViewState(
                latitude=mid_latitude,
                longitude=mid_longitude,
                zoom=9,
            )
    heatmaplayer = pdk.Layer(
        'HeatmapLayer',
        data=data,
        opacity=0.75,
        get_position=['longitude', 'latitude'],
        threshold=0.05,
        intensity=0.8
    )

    # printing map
    st.pydeck_chart(
        pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=initial_view_state,
            layers=[scatterplotlayer, heatmaplayer],
        )
    )

    # census section
    st.subheader("Map using census data")
    census_image = Image.open('Ghanaians_in_nyc_plot.jpg')
    st.image(census_image, use_column_width=True, caption="Distribution of Ghanaians in NYC")

    #learn more section
    st.sidebar.subheader("If you would like to learn more about any of these groups, click on one of the options below")
    st.sidebar.markdown("[Ghanaian peoples] (https://en.wikipedia.org/wiki/Ghanaian_people)")
    st.sidebar.markdown("[Uyghurs] (https://en.wikipedia.org/wiki/Uyghurs)")
    st.sidebar.markdown("[Garifuna] (https://en.wikipedia.org/wiki/Garifuna)")

    st.sidebar.subheader("To learn more about the project itself, click on one of the blogs below")
    st.sidebar.markdown('[Are Ethnic Restaurants in Ethnic Neighborhoods (Part 1)] '
                        '(https://medium.com/@gregfeliu/are-ethnic-restaurants-in-ethnic-neighborhoods-part-1-f0eccc394ff7)')
    st.sidebar.markdown('[Are Ethnic Restaurants in Ethnic Neighborhoods (Part 2)]'
                        ' (https://medium.com/@gregfeliu/are-ethnic-restaurants-in-ethnic-neighborhoods-part-2-ddbac417452a)')


if __name__ == '__main__':
    main()
