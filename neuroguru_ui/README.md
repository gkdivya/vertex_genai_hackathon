# NeuroGuru UI

NeuroGuru - A multi-lingual, interactive, and adaptive learning platform to make AI technology accessible and engaging for everyone. Harness the power of GenerativeAI to learn AI. 

## Technology Stack

* Streamlit
* Python

## Deployment

* GCP Cloud Run https://neuroguru-app-lozf7taqoa-uc.a.run.app

## Code Structure

* neuroguru.py - main streamlit application script
* languages.json - Supported Languages
* Language Jsons - Language specific values
  * language_data/language_data_german.json
  * language_data/language_data_french.json
  * language_data/language_data_english.json
  * language_data/language_data_dutch.json
  * language_data/language_data_spanish.json
* config.py - backend service url details
* neuroinstructor.png - application header image
* requirements.txt - required python libraries
* Dockerfile - used for docker image creation and deployment in GCP cloud run

## Limitations

Currently only english language is supported by Palm API - Bison model provided for hackathon. 

<img width="500" alt="Screenshot 2023-07-10 at 4 55 40 PM" src="https://github.com/gkdivya/vertex_genai_hackathon/assets/17870236/aefbd2ba-acd1-4f9c-b546-b775c2a6c3f7">

