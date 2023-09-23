import requests
import pandas as pd
import plotly.express as px
import streamlit as st 
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
from streamlit_folium import folium_static
import folium
from webscrape import WebScrape
from preprocessing import preprocessing
from predict import predict
from filter import filter
from drawcloud import plot_wordcloud

st.set_page_config(
    page_title="Restaurant Comments App",
    page_icon="🍴",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load GIF
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie_food = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_Ptt70m3Xfb.json")

with st.sidebar:
    selected = option_menu(
        menu_title = "Main Menu", 
        options = ["Search Restaurant", "Chatbot"], 
        icons = ["geo-alt", "robot"],
        menu_icon = "cast", 
        default_index = 0
    )

# Main menu -> Search Restaurant
if selected == "Search Restaurant":
    title1, title2, title3 = st.columns(3)
    with title2:
        st.write("""
            <div style="text-align: center;">
            <h1><strong>Restaurant Hunter</strong></h1>
            <h5>Explore the Flavor, Unveil the Feelings.</h5>
            </div>
            """,
            unsafe_allow_html=True)
    st.write("---")

    # Show how to use this app
    col1, col2 = st.columns(2)
    with st.container():
        with col1:
            st_lottie(
                lottie_food,
                speed = 0.8,
                reverse = False,
                quality = "high",
                loop = True,
                width = 400,
                height = None,
                key=None
            )

        with col2:
            st.write("""
            ## Steps using this app :point_down: 
            - ##### Input **:blue[restaurant name, location]**
            - ##### Choose how many comments you want to see
            - ##### Select comments you want to see (Positive:ok_woman: Negative:no_good:)
            """)
            
    st.write("---")
    col4, col5 = st.columns(2)

    with st.sidebar.form("my_form"):
        Restaurant_info = st.text_input("Input restaurant & location", "Tía Juana Grill, East Duane Avenue, Sunnyvale, CA, USA")
        Number_of_comment = st.slider("Show number of comments", 0, 500)
        Sort_comments = st.multiselect(
            'What comments do you want to see',
            ['Positive', 'Negative'],
            ['Positive', 'Negative']
        )
        submitted = st.form_submit_button("Enter")

    # Activate if submit button is push
    if submitted:
        progress_bar = st.sidebar.progress(0)

        st.sidebar.write('Scraping data from google map...')

        new_text_df, df, address, phone = WebScrape(Restaurant_info, Number_of_comment, progress_bar)

        # Show map
        col4.empty()
        col5.empty()

        with st.container():
            with col4:
                st.write(f"""
                        ## Restaurant Info 
                        ##### :house_with_garden: {Restaurant_info}
                        ##### :round_pushpin: {address}
                        ##### :telephone_receiver: {phone}
                        """)
            with col5:
                lat = df['lat'][0]
                lon = df['lon'][0]

                m = folium.Map(location=[lat, lon], zoom_start=15, control_scale=True)
                folium.Marker(
                    [lat, lon],
                    popup = f'{Restaurant_info}',
                    icon=folium.Icon(color="red", icon="info-sign")
                ).add_to(m)

                folium_static(m, width=400)

        st.write("---")
        google_comment_df = preprocessing(new_text_df)
        google_predict_comment_df, google_predict_positive_comment, google_predict_negative_comment, positive_comments_number, negative_comments_number = predict(google_comment_df)
        Neg_fdist, Pos_fdist = filter(google_predict_comment_df)

        data = {'Sentiment': ['Positive', 'Negative'],
        'Count': [positive_comments_number, negative_comments_number]}
        df = pd.DataFrame(data)

        bar1, bar2 = st.columns(2)
        with bar1:
            st.bar_chart(df.set_index('Sentiment'), width=350)
        with bar2:
            st.write(f"""
                        ## How many positive and negative comments 
                        - ##### There are <span style='color:green'>{positive_comments_number}</span> positive comments
                        - ##### There are <span style='color:red'>{negative_comments_number}</span> negative comments""", unsafe_allow_html=True)

        st.write("---")
        # Depict wordcloud
        if len(Sort_comments) == 1:
            tab1 = st.tabs(Sort_comments)
            col6, col7 = st.columns(2)

            with tab1:
                with col6:
                    if(Sort_comments[0] == 'Positive'):
                        positive_wordcloud_image = plot_wordcloud("Positive Wordcloud", Pos_fdist)
                        st.image(positive_wordcloud_image)
                    else:
                        negative_wordcloud_image = plot_wordcloud("Negative Wordcloud", Neg_fdist)
                        st.image(negative_wordcloud_image)
                with col7:
                    if(Sort_comments[0] == 'Negative'):
                        st.dataframe(google_predict_positive_comment)
                    else:
                        st.dataframe(google_predict_negative_comment)
                      
        else:
            tab1, tab2= st.tabs(Sort_comments)
            
            with tab1:
                col8, col9 = st.columns(2)

                with col8:
                    positive_wordcloud_image = plot_wordcloud("Positive Wordcloud", Pos_fdist)
                    st.image(positive_wordcloud_image)
                with col9:
                    st.dataframe(google_predict_positive_comment)
            with tab2:
                col10, col11 = st.columns(2)

                with col10:
                    negative_wordcloud_image = plot_wordcloud("Negative Wordcloud", Neg_fdist)
                    st.image(negative_wordcloud_image)
                with col11:
                    st.dataframe(google_predict_negative_comment)

        st.sidebar.success('Done!', icon="✅")

# Main menu -> Chatbot
if selected == "Chatbot":
    st.title("Chatbot")
    
