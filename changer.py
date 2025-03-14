from typing import Tuple, Dict
import dotenv
import os
import json
import requests
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

load_dotenv()
EXCHANGERATE_API_KEY = os.getenv('EXCHANGERATE_API_KEY')
token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"



def get_exchange_rate(base: str, target: str, amount: str) -> Tuple:
    """Return a tuple of (base, target, amount, conversion_result (2 decimal places))"""
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/pair/{base}/{target}/{amount}"
    response = json.loads(requests.get(url).text)
    return (base, target, amount, f"{response['conversion_result']:.2f}")

def call_llm(textbox_input) -> Dict:
    """Make a call to the LLM with the textbox_input as the prompt.
       The output from the LLM should be a JSON (dict) with the base, amount and target"""
    try:
        client = OpenAI(
            base_url=endpoint,
            api_key=token,
        )

        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": textbox_input,
                }
            ],
            model=model_name,
        )
    except Exception as e:
        print(f"Exception {e} for {textbox_input}")
    else:
        return completion

def run_pipeline():
    """Based on textbox_input, determine if you need to use the tools (function calling) for the LLM.
    Call get_exchange_rate(...) if necessary"""

    if True: #tool_calls
        # Update this
        st.write(f'{base} {amount} is {target} {exchange_response["conversion_result"]:.2f}')

    elif True: #tools not used
        # Update this
        st.write(f"(Function calling not used) and response from the model")
    else:
        st.write("NotImplemented")





# Title
st.title('Change')

# Text Input
text_input = st.text_input("Enter some text")

# Button
if st.button('Submit'):
    st.write(call_llm(text_input).choices[0].message.content)