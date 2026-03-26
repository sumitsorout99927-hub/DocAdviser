from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types
import os

app = Flask(__name__)
# CORS allows your HTML file to communicate with this Python server
CORS(app) 

# The server will now securely grab the key from Render's hidden settings!
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Initialize the new Gemini Client
client = genai.Client(api_key="AIzaSyAy6i1mEvCkOEL4853ktI20KC3nt_39s3U")

# Set up the persona for DocAdviser
system_instruction = """
You are DocAdviser, a helpful and expert AI assistant for Indian citizens. 
Your goal is to guide users through the process of applying for, correcting, and understanding Indian documents.
You specialize in national IDs (Aadhaar, PAN, Voter ID), student documents (Income Certificates, scholarships), state-level documents (like Domicile certificates, especially in northern states like Haryana), and agricultural documents (like the Kisan Credit Card or Jamabandi records).
Keep your answers concise, structured, and easy to read. Do not hallucinate government URLs; tell them to visit the official state portal or e-District website.
"""

@app.route('/api/chat', methods=['POST'])
def chat():
    # Get the user's message from the frontend
    user_message = request.json.get('message')
    
    if not user_message:
        return jsonify({"reply": "Please provide a message."}), 400

    try:
        # Send the message to Gemini using the NEW library syntax
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )
        ai_reply = response.text
        
        # Send the response back to the frontend
        return jsonify({"reply": ai_reply})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "Sorry, I am having trouble connecting to my document database right now. Please try again later."}), 500

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=10000)
