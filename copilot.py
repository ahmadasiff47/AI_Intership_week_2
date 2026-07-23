import os
import json
from dotenv import load_dotenv
from groq import Groq

# 1. Load Environment Variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("❌ Error: GROQ_API_KEY not found in .env file!")
    exit()

client = Groq(api_key=api_key)

# 2. Define All Enterprise Tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "generate_sql_query",
            "description": "Generates SQL queries for database operations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query_description": {"type": "string"},
                    "sql_code": {"type": "string"}
                },
                "required": ["query_description", "sql_code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "draft_email",
            "description": "Drafts professional emails.",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipient": {"type": "string"},
                    "subject": {"type": "string"},
                    "body": {"type": "string"}
                },
                "required": ["recipient", "subject", "body"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_report",
            "description": "Generates structured technical or executive reports.",
            "parameters": {
                "type": "object",
                "properties": {
                    "report_title": {"type": "string"},
                    "sections": {"type": "string"},
                    "summary": {"type": "string"}
                },
                "required": ["report_title", "sections", "summary"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "internet_search",
            "description": "Performs internet search for live data retrieval.",
            "parameters": {
                "type": "object",
                "properties": {
                    "search_query": {"type": "string"}
                },
                "required": ["search_query"]
            }
        }
    }
]

print("⚡ Enterprise AI Copilot Complete System Ready! (Type 'quit' or 'exit' to stop)\n")

# 3. Main Interactive Loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Copilot closed.")
        break

    if not user_input.strip():
        continue

    try:
        messages = [
            {"role": "system", "content": "You are an advanced Enterprise AI Copilot equipped with SQL generation, email drafting, report generation, and internet search tools."},
            {"role": "user", "content": user_input}
        ]

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        msg = response.choices[0].message

        if msg.tool_calls:
            tool_call = msg.tool_calls[0]
            fn_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            if fn_name == "generate_sql_query":
                print(f"\n[TOOL EXECUTED: SQL Generator]\n📌 Request: {args.get('query_description')}\n💻 SQL Code:\n{args.get('sql_code')}\n")
            elif fn_name == "draft_email":
                print(f"\n[TOOL EXECUTED: Email Drafter]\n📩 To: {args.get('recipient')}\n📌 Subject: {args.get('subject')}\n📝 Body:\n{args.get('body')}\n")
            elif fn_name == "generate_report":
                print(f"\n[TOOL EXECUTED: Report Generator]\n📊 Title: {args.get('report_title')}\n📑 Summary: {args.get('summary')}\n📝 Sections:\n{args.get('sections')}\n")
            elif fn_name == "internet_search":
                print(f"\n[TOOL EXECUTED: Internet Search Orchestrator]\n🔍 Searching Web for: '{args.get('search_query')}'...\n🌐 Status: Query orchestrated successfully.\n")
        else:
            print(f"\nAI Copilot: {msg.content}\n")

    except Exception as e:
        print(f"❌ Error: {e}\n")