from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from google.auth import credentials
from google.oauth2 import service_account
import google.cloud.aiplatform as aiplatform
from vertexai.preview.language_models import ChatModel, InputOutputTextPair
from vertexai.preview.language_models import CodeGenerationModel
from vertexai.language_models import TextGenerationModel
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
import vertexai
import json  # add this line

# Load the service account json file
# Update the values in the json file with your own
with open(
    "service_account.json"
) as f:  # replace 'serviceAccount.json' with the path to your file if necessary
    service_account_info = json.load(f)

my_credentials = service_account.Credentials.from_service_account_info(
    service_account_info
)

# Initialize Google AI Platform with project details and credentials
aiplatform.init(
    credentials=my_credentials,
)

with open("service_account.json", encoding="utf-8") as f:
    project_json = json.load(f)
    project_id = project_json["project_id"]


# Initialize Vertex AI with project and location
vertexai.init(project=project_id, location="us-central1")

# Initialize the FastAPI application
app = FastAPI()

# Configure CORS for the application
origins = ["http://localhost", "http://localhost:8080", "http://localhost:3000"]
origin_regex = r"https://(.*\.)?alexsystems\.ai"
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
delimiter = "'''"

@app.get("/")
async def root():
    """Root endpoint that returns available endpoints in the application"""
    return {
        "Endpoints": {
            "chat": "/chat",
        }
    }


@app.get("/docs")
async def get_documentation():
    """Endpoint to serve Swagger UI for API documentation"""
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@app.get("/redoc")
async def get_documentation():
    """Endpoint to serve ReDoc for API documentation"""
    return get_redoc_html(openapi_url="/openapi.json", title="redoc")


@app.post("/chat")
async def handle_chat(human_msg: str):
    """
    Endpoint to handle chat.
    Receives a message from the user, processes it, and returns a response from the model.
    """
    chat_model = ChatModel.from_pretrained("chat-bison@001")
    parameters = {
        "temperature": 0.8,
        "max_output_tokens": 1024,
        "top_p": 0.8,
        "top_k": 40,
    }
    chat = chat_model.start_chat(  # Initialize the chat with model
        # chat context and examples go here
    )
    # Send the human message to the model and get a response
    response = chat.send_message(human_msg, **parameters)
    # Return the model's response
    return {"response": response.text}


@app.post("/code")
async def handle_code(code_prompt: str):
    """
    Endpoint to handle code.
    Receives a message from the user, processes it, and returns a response from the model.
    """
    model = CodeGenerationModel.from_pretrained("code-bison@001")
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 1024
    }
    # delimiter = "'''"
    message = delimiter + code_prompt + delimiter
    response = model.predict(
        prefix = message,
        **parameters
    )
    return {"response": response.text}

@app.post("/text")
async def text_code(code_prompt: str):
    """
    Endpoint to handle Text Prompt.
    Receives a message from the user, processes it, and returns a response from the model.
    """
    vertexai.init(project="logical-pilot-392211", location="us-central1")
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 256,
        "top_p": 0.8,
        "top_k": 40
    }
    model = TextGenerationModel.from_pretrained("text-bison@001")

    # format input
    message = delimiter + code_prompt + delimiter
    response = model.predict(
        message,
        **parameters
    )
        
    return {"response": response.text}