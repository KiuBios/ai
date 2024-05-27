import os
import sys
from groq import Groq

groq_key = "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"

chatStack = []

groq = Groq(api_key=groq_key) if groq_key else None

def groqChat(question):
    response = groq.chat.completions.create(
        messages=chatStack+[{"role": "user", "content": question}],
        # model="llama3-8b-8192",
        model="llama3-70b-8192",
    )
    return response.choices[0].message.content

def chat(question):
    try:
        return groqChat(question)
    except Exception as error:
        print(f"returned an API Error: {error}")
        return "Error: chat api fail!"

if __name__ == '__main__':
    response = chat(" ".join(sys.argv[1:]))
    print(response)

