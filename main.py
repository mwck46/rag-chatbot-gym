
import openai
import os
from openai import OpenAI 
import requests
from dataHandler import DataHandler

data_path = "output/faqs.json"
persist_directory = "./chroma_db"
data_handler = DataHandler(data_path, persist_directory=persist_directory)


def build_prompt(user_question, retrieved_chunks):
    prompt = "You are a helpful chatbot designed to answer questions about Fitness Passport.\n\n"
    prompt += "Here is some information from our FAQs that might be relevant to the user's question:\n---\n"
    for chunk in retrieved_chunks:
        question, answer = chunk.split('\n', 1)
        prompt += f"Question: {question}\nAnswer: {answer}\n---\n"
    
    prompt += f"\nUser Question: {user_question}\n\n"
    prompt += "Based on the information provided above, answer the user's question to the best of your ability. If the context does not answer the question, you can tell the user that you don't have the answer."
    return prompt

def format_response_with_references(response_text, retrieved_metadatas): # we create a function for the references
    formatted_response = response_text + "\n\n" # we add the original response
    formatted_response += "References:\n"
    for metadata in retrieved_metadatas: # we loop in the metadatas
        source = metadata["source"]
        formatted_response += f"- [{source}]({source})\n" # we create the links using the source text
    return formatted_response

def get_openai_response(prompt, retrieved_metadatas): # we now pass the retrieved_metadatas
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI()  # Create an instance of the OpenAI client
    response = client.chat.completions.create(  # Use the new API interface
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    response_text=response.choices[0].message.content
    formatted_response = format_response_with_references(response_text, retrieved_metadatas) # we use our function to create the references
    return formatted_response


def llmstudio_local(prompt):
    url = "http://127.0.0.1:1234/api/v1/chat"
    headers = {
        'Content-Type': 'application/json'
    }
    llm_model = 'google/gemma-4-e4b'
    data = {
        "model": f'{llm_model}',
        "input": f'{prompt}'
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()


def get_llmstudio_response(prompt, retrieved_metadatas): # we now pass the retrieved_metadatas
    response = llmstudio_local(prompt)
    formatted_response = response['output'][1]['content']
    #formatted_response = format_response_with_references(response_text, retrieved_metadatas) # we use our function to create the references
    
    return formatted_response


if __name__ == "__main__":

    try:
        data_handler.chroma_client.get_collection(name=data_handler.collection_name)
        print("Collection exists")
    except Exception as e:  # if we cant, an error is raised
        print(f"Collection does not exist: {e}. We need to create it")
        collection = data_handler.process_data_and_create_collection()

    try:

        prompt = "How do I become a member?"
        results = data_handler.query_chroma(prompt)  # we get the full results (documents and metadatas)
        if results["documents"] and results["metadatas"]:  # if there are documents and metadatas
            retrieved_chunks = results["documents"][0]
            retrieved_metadatas = results["metadatas"][0]  # we get the metadatas
        else:
            retrieved_chunks = []
            retrieved_metadatas = []

        full_prompt = build_prompt(prompt, retrieved_chunks)
        print(full_prompt)


        llm_response = get_llmstudio_response(full_prompt, retrieved_metadatas)
        print(llm_response)
    except Exception as e: 
        print(f"Error: {e}")
