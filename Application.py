from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
from openai import OpenAI
from prompt_template import template
import os

Application = Flask(__name__)
CORS(Application)

load_dotenv()
Api_token = os.getenv("Api_Token")
os.environ["OPENAI_API_KEY"] = os.getenv("OPEN_API")
client = OpenAI()
chat_history = []


@Application.route("/")
def home_route():
    return {"Message": "Hello Route"}


@Application.route("/query", methods=["POST"])
def enter_query():
    api = request.headers.get("Authorization")
    if Api_token == api:
        data = request.get_json()
        try:
            if data["query"]:
                query = data["query"]
                completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": template},
                        {"role": "user", "content": query + str(chat_history)}
                    ])
                chat_history.append({"role": "user",
                                     "content": query})
                chat_history.append({"role": "assistant",
                                     "content": completion.choices[0].message.content})
                return {"output": str(completion.choices[0].message.content)}
            else:
                return {"message": "Please enter your query"}
        except Exception as e:
            return e
    elif api and api != Api_token:
        return {"message" : "Unauthorized access"}
    else:
        return {"message": "Api key needed"}

if "__main__" == __name__:
    Application.run(debug=True)