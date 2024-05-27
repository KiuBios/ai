# Make sure you have an API key and set it as an environment variable

from langchain import hub
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from config import GROQ_API_KEY

from poi import TravelPOITool
from ticket import TravelTicketTool
from exp import TravelExpTool
from weather import WeatherDataTool
from product import ProductTool

# model_name="mixtral-8x7b-32768", Context Window: 32,768 tokens
# 備用 model_name = "llama3-8b-8192", Context Window: 8,192 tokens
chat = ChatGroq(temperature=0, groq_api_key=GROQ_API_KEY, model_name="mixtral-8x7b-32768")

tools = [TravelPOITool(), TravelTicketTool(),
         TravelExpTool(), WeatherDataTool(), ProductTool(), DuckDuckGoSearchRun()]

# 初始版本
#system = "You are a helpful assistant."
#human = "{text}"
#prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
#chain = prompt | chat

# Create the agent 版本
prompt = hub.pull("hwchase17/openai-functions-agent")
agent = create_tool_calling_agent(chat, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

message_history = ChatMessageHistory()
agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: message_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)
agent_with_chat_history.invoke(
    {"input": "hi! my name is Miquella"},
    config={"configurable": {"session_id": "<foo>"}},
)

while True:
    try:
        question = input("請問我有什麼可以幫忙的? ")
        if (question == "exit") : break 
        
        # Create the agent 版本
        #agent_executor.invoke({"input": question})
        agent_with_chat_history.invoke(
        {"input": question},
        config={"configurable": {"session_id": "<foo>"}},
)

        # 初始版本
        #for chunk in chain.stream({"text": question}):
        #    print(chunk.content, end="", flush=True)

        print("\n")
    except KeyboardInterrupt:
        break