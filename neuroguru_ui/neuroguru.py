import streamlit as st
import requests
import json
import textwrap

# from googletrans import Translator

import config as cfg
import os

# List of languages for the dropdown
# Initial page settings
st.set_page_config(page_title="NeuroGuru-AI Educational Platform", page_icon=":books:")

# Create two columns
col1, col2 = st.columns([2,3])  # adjust the numbers to manage the width of columns

# Add an image to the first column
col1.image('neuroinstructor.png', use_column_width=True)
# Add other elements to the second column
col2.markdown("<h1 style='text-align: left; color: black;'>NeuroGuru</h1>", unsafe_allow_html=True)   
col2.markdown("<h5 style='text-align: left; color: black;'>AI Educational Platform</h5>", unsafe_allow_html=True) 
#col2.subheader("Powered by Vertex - Generative AI")
# Continue adding elements to col2

global languages

def get_prompt(prompt_template, selected_topic, selected_subtopic, selected_language):
    # Replace placeholders with actual values
    prompt = prompt_template.format(selected_topic=selected_topic, selected_subtopic=selected_subtopic, selected_language=selected_language)
    
    return prompt

def get_answer():
    data = {}
    user_input = ""
    # List of languages for the dropdown
    # languages = ["English", "Spanish", "German", "French", "Italian", "Dutch", "Portuguese", "Russian"]
    language_data = {}
    cwd = os.getcwd()
    
    try:
        file_name = ""
        language = ""
        # Initial page settings
        # st.set_page_config(page_title=language_data["English"]["title"], page_icon=":books:")
        # Select language
        with open("languages.json", "r") as f:
            languages = json.load(f)
            lng_labels = [lng['language'] for lng in languages["languages"]]
            language = st.selectbox("Choose your language", lng_labels)
            # language = st.selectbox(language_data["English"]["language_choice"], languages)

            file_name = f"language_data/language_data_{language.lower()}.json"
            # print(f"file_name: {file_name}")
            # Load language data
            with open(file_name, 'r') as f:
                language_data = json.load(f)
            if language_data:
                # Set language data based on selected language
                data = language_data[language]

            if data:
                # Title and intro
                #st.title(data["title"])
                st.write(data["intro"])
                # Display information based on chosen language
                if language:
                    st.header(f"{data['selected_language']}: {language}")
                    st.write(f"{data['start_journey']}")
                    
                    # Add here more interactive elements
                    st.subheader(f"{data['ai_topic']}")
                    topics = data["topics"]
                    all_topics = [d['topic'] for d in topics]
                    selected_topic = st.selectbox(data["select_topic"], all_topics)
                    
                    if selected_topic:
                        st.subheader(f"{data['selected_topic']}: {selected_topic}")
                        if selected_topic in all_topics:
                            sub_topic_obj = next(d for d in topics if d['topic'] == selected_topic)
                            sub_topics = sub_topic_obj["sub_topics"]
                            selected_subtopic = st.selectbox(data["select_subtopic"], sub_topics)                            
                            if selected_subtopic:
                                # st.subheader(f"Selected Sub-topic: {selected_subtopic}")
                                
                                # Define the list of suggestions as dropdown
                                sel_prompt = ""
                                sel_prompt = st.selectbox(f"{data['choose_learn']}", data["prompts"])

                                # print(f"sel_prompt: {sel_prompt}")
                                # set backend service url
                                url = cfg.service_url
                                headers = {
                                    "Content-type": "application/json",
                                    "Accept": "application/json"
                                }
                                if st.button(data["generate"]):
                                    if cfg.service_env == "local":
                                        url = f"{url}{cfg.port}"

                                    prompt = get_prompt(data['prompts'][sel_prompt], selected_topic, selected_subtopic, language)   
                                    print(prompt) 

                                    st.write(prompt)
                                    response = requests.post(f"{url}/code?code_prompt={prompt}", headers=headers)
                                    # Check response code and proceed
                                    if response.status_code == 200:
                                        resp_json = response.json() 
                                        st.write(textwrap.dedent(resp_json['response']))
                                        # print(f"response json : {resp_json['response']}")
                                    else:
                                        st.write("Something went wrong. Please try again.")
    except requests.exceptions.HTTPError as errh:
        st.write("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        st.write("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        st.write("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        st.write("Oops! Something went wrong. Please try again.",err)
    except Exception as ex:
        st.write(f"Error occurred: {ex}")

get_answer()
