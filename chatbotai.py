# IMPORT LIBRARIES
import os
import PyPDF2
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

os.environ["GOOGLE_API_KEY"] = "AIzaSyCXHokFFqhcBKc-AZNDME30DdZNpjCV6ls"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# PDF READER FUNCTION 
def read_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text


# WEBSITE SCRAPER FUNCTION
def scrape_website(url):
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = soup.find_all("p")
    text = " ".join([p.get_text() for p in paragraphs])
    return text


# KEYWORD EXTRACTION
def extract_keywords(question):
    stopwords = [
        "how", "to", "is", "the", "a", "an", "of", "for", "in", "on",
        "tell", "me", "about", "what", "explain", "describe", "world"
    ]
    words = question.lower().split()
    return [word for word in words if word not in stopwords]



# KEYWORD-BASED CHATBOT (PART A)
def chatbot_response(question, pdf_text, web_text):

    # DOMAIN FILTER (MOST IMPORTANT)
    allowed_topics = ["uav", "drone", "unmanned", "aerial", "aircraft", "military"]

    if not any(topic in question.lower() for topic in allowed_topics):
        return "Sorry, no relevant instruction found."

    keywords = extract_keywords(question)

    # Search in PDF
    for line in pdf_text.split("\n"):
        line_lower = line.lower()
        if sum(1 for k in keywords if k in line_lower) >= 2:
            return "ChatBot (From PDF):\n" + line.strip()

    # Search in Website
    for line in web_text.split("."):
        line_lower = line.lower()
        if sum(1 for k in keywords if k in line_lower) >= 2:
            return "ChatBot (From Website):\n" + line.strip()

    return "Sorry, no relevant instruction found."




# AI-POWERED RESPONSE (PART B)
def ai_answer(question, pdf_text, web_text):
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
You are an assistant.
Use ONLY the given content to answer.
If the answer is not present, say:
"This information is not available."

PDF Content:
{pdf_text[:3000]}

Website Content:
{web_text[:3000]}

Question:
{question}

Answer clearly in simple steps.
"""

    response = model.generate_content(prompt)
    return response.text.strip()


# LOAD DATA 
pdf_text = read_pdf("C:\\Users\\LENOVO\\Downloads\\Coding\\Lab Manual Exp 3 Chatbot.pdf")
web_text = scrape_website("https://www.britannica.com/technology/military-aircraft/Unmanned-aerial-vehicles-UAVs#ref1074008")

print("Chatbot is ready. Type 'exit' to quit.\n")


# MAIN CHAT LOOP 
while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Bot: Goodbye!")
        break

    response = chatbot_response(user_input, pdf_text, web_text)

    if "Sorry, no relevant instruction found." in response:
        print("Bot (AI): Thinking...")
        response = ai_answer(user_input, pdf_text, web_text)

    print("Bot:", response, "\n")