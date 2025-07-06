from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, AIMessage
from calendar_utils import get_free_slots, create_event
import os
import json
from dateutil import parser
from datetime import datetime, timedelta
import pytz

# Set your Gemini API key (use dotenv in production)
os.environ["GOOGLE_API_KEY"] = "AIzaSyCK84_BXPT4rXXe88KjiUEUUmgvl8PZmVs"

# Define the Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

# 🧠 Convert natural language to RFC 3339 datetime string
def parse_natural_time(natural_time_str):
    try:
        now = datetime.now(pytz.timezone("Asia/Kolkata"))  # Adjust timezone
        if "tomorrow" in natural_time_str.lower():
            time_part = natural_time_str.lower().replace("tomorrow", "").strip()
            dt = parser.parse(time_part)
            combined = now + timedelta(days=1)
            combined = combined.replace(hour=dt.hour, minute=dt.minute, second=0, microsecond=0)
            return combined.isoformat()
        else:
            return parser.parse(natural_time_str).isoformat()
    except Exception as e:
        raise ValueError(f"Invalid time format: {natural_time_str} — {e}")

# Wrapper for create_event tool
def create_event_tool(input):
    if isinstance(input, str):
        input = json.loads(input)

    start_time_str = input.get("start_time")
    end_time_str = input.get("end_time")
    summary = input.get("summary")

    if not all([start_time_str, end_time_str, summary]):
        raise ValueError("Missing one of: start_time, end_time, summary")

    # ⏰ Parse natural time to ISO 8601
    start_time = parse_natural_time(start_time_str)
    end_time = parse_natural_time(end_time_str)

    return create_event(start_time, end_time, summary)

# Define tools
tools = [
    Tool(
        name="CheckCalendarAvailability",
        func=get_free_slots,
        description="Check free time slots for a given date."
    ),
    Tool(
        name="CreateCalendarEvent",
        func=create_event_tool,
        description="Create a calendar event using start_time, end_time, and summary."
    )
]

# Initialize the agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True
)

# Maintain conversation context
chat_history = []

# Handle user input and run the agent
def handle_user_input(user_input: str) -> str:
    global chat_history
    try:
        response = agent.invoke({
            "input": user_input,
            "chat_history": chat_history
        })
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=response["output"]))
        return response["output"]
    except Exception as e:
        print("❌ Error in agent.invoke:", e)
        return "Sorry, I couldn't process that."
