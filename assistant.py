from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import time
import os


if __name__ == "__main__":
    _ = load_dotenv(find_dotenv())

    ID_assistant = "asst_5F4uFodUSkxTVfHwlqiW1qMd"

    client = OpenAI(
        api_key = os.environ.get("OPENAI_API_KEY")
    )

    # Upload the user provided file to OpenAI
    message_file = client.files.create(
        file=open("nota_2.pdf", "rb"), purpose="assistants"
    )
    
    # Create a thread and attach the file to the message
    thread = client.beta.threads.create(
        messages=[
            {
            "role": "user",
            "content": f"escreva a tabela do arquivo {message_file.id}. PEGUE TODAS AS LINHAS SEM FALTAR NENHUMA",
            # Attach the new file to the message.
            "attachments": [
                { "file_id": message_file.id, "tools": [{"type": "file_search"}] }
            ],
            }
        ]
    )
    
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ID_assistant)
    print(f"Run created: {run.id}")

    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(f"Run Status: {run.status}")
        time.sleep(5)
    else:
        print(f"Run Completed!")
    
    message_response = client.beta.threads.messages.list(thread_id=thread.id)
    messages = message_response.data

    latest_message = messages[0]
    csv = latest_message.content[0].text.value

    with open("nota_1.txt", "w") as file:
        file.write(csv)