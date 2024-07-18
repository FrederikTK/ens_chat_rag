from openai import OpenAI
import requests
from dotenv import load_dotenv
import os

load_dotenv()
def call_llm_api(llm_config=False, data=False, user_input=False, system_input=False, model_put=False):
 ##################### OpenAI  #####################    
    if llm_config['service'] == 'openai':
        client = OpenAI()
        try:
            user_message_content = data['content'] if not user_input else user_input
            system_message_content = llm_config['prompt'] if not system_input else system_input
            model_choice = llm_config['model'] if not model_put else model_put
            print(model_choice,system_message_content)
            response = client.chat.completions.create(
                model=model_choice,
                messages=[
                    {"role": "system", "content": system_message_content},
                    {"role": "user", "content": user_message_content}
                ],
                max_tokens=llm_config['max_tokens']
            )
            # Access the text of the completion using the correct property method
            return response.choices[0].message.content
        except KeyError as e:
            # Handle cases where the expected keys are not present
            return f"Failed to retrieve message content: {str(e)}"
        except Exception as e:
            # General error handling
            return f"API error: {str(e)}"
        
 ##################### AWS #####################     
    elif llm_config['service'] == 'sagemaker':
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {llm_config['api_key']}"
        }
        response = requests.post(llm_config['endpoint_url'], json={"text": data['content']}, headers=headers)
        response.raise_for_status()
        # Extract text directly assuming response is in JSON format
        return response.json().get('summary', 'No summary available')
 
  ##################### LOCAL  #####################   
    elif llm_config['service'] == 'localhost':
        # Adjust the base URL to use host.docker.internal
        client = OpenAI(base_url="http://host.docker.internal:1234/v1", api_key="lm-studio")
        try:
            user_message_content = data['content'] if not user_input else user_input
            system_message_content = llm_config['prompt'] if not system_input else system_input
            model_choice = llm_config['model'] if not model_put else model_put
            response = client.chat.completions.create(
                model=model_choice,
                messages=[
                    {"role": "system", "content": system_message_content},
                    {"role": "user", "content": user_message_content}
                ],
                temperature=llm_config['temperature'],
            )
            return response.choices[0].message.content
        except KeyError as e:
            return f"Failed to retrieve message content: {str(e)}"
        except Exception as e:
            return f"API error: {str(e)}"