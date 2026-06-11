from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core.exceptions import ResourceExhausted
from dotenv import load_dotenv
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

prompt = "Say hello in one line"

try:
    response = llm.invoke(prompt)
    print("✅ RESPONSE:", response.content)

except ResourceExhausted as e:
    print("🚨 QUOTA ERROR (429):", repr(e))

except Exception as e:
    print("❌ OTHER ERROR:", repr(e))
    raise e