import os
from openai import OpenAI

key = OpenAI.api_key = "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"

client = OpenAI(api_key="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")

def askForCard(currentHand):
     
     prompt = "Ask for a card in go fish given your current hand: " + currentHand

     try:
         response = client.chat.completions.create(
            model="gpt-4o",
            messages=prompt,
            temperature=0.7
         )
         reply = response.choices[0].message.content.strip()
         print(reply)
         return reply
        

     except Exception as e:
        print(f"[ERROR] Failed to get response from ChatGPT: {e}")
        return "This is a dummy response until your API quota is available."
     
askForCard("queen" "king" "queen" "two" "one")
     



