import os
from typing import Dict, List, TypedDict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Blog Generation System")

# Define input model for FastAPI
class BlogRequest(BaseModel):
    topic: str

# Define state for LangGraph
class BlogState(TypedDict):
    topic: str
    research_data: List[str]
    blog_content: str

# Initialize language model (Gemini)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)

# Initialize tools
wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
tavily_tool = TavilySearchResults(tavily_api_key=os.getenv("TAVILY_API_KEY"))

# Define tools list
tools = [wikipedia_tool, tavily_tool]

# Bind tools to LLM
llm_with_tools = llm.bind_tools(tools)

# Research prompt
research_prompt = ChatPromptTemplate.from_template("""
You are a research assistant. Given the topic "{topic}", use the provided tools to gather relevant information.
Return a list of key points or facts in bullet points.
""")

# Blog generation prompt
blog_prompt = ChatPromptTemplate.from_template("""
You are a professional blog writer. Using the following research data and topic, write a well-structured blog in markdown format with the following sections:
- Heading: Clearly define the topic.
- Introduction: Engaging introduction to the topic.
- Content: Detailed and informative content, supported by the research data.
- Summary: Summarize the main points.

Topic: {topic}

Research Data:
{research_data}

Output the blog in markdown format.
""")

# Research node
def research_node(state: BlogState) -> BlogState:
    prompt = research_prompt.format(topic=state["topic"])
    response = llm_with_tools.invoke(prompt)
    research_data = []
    
    # Check if tool calls are present
    if hasattr(response, "tool_calls") and response.tool_calls:
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            if tool_name == "wikipedia":
                result = wikipedia_tool.invoke(tool_args)
            elif tool_name == "tavily_search":
                result = tavily_tool.invoke(tool_args)
            else:
                continue
            research_data.append(str(result))
    
    state["research_data"] = research_data
    return state

# Blog generation node
def generate_blog_node(state: BlogState) -> BlogState:
    research_data = "\n".join(state["research_data"]) if state["research_data"] else "No research data available."
    prompt = blog_prompt.format(topic=state["topic"], research_data=research_data)
    response = llm.invoke(prompt)
    state["blog_content"] = response.content
    return state

# Define LangGraph workflow
workflow = StateGraph(BlogState)
workflow.add_node("research", research_node)
workflow.add_node("generate_blog", generate_blog_node)
workflow.add_edge("research", "generate_blog")
workflow.add_edge("generate_blog", END)
workflow.set_entry_point("research")

# Compile the graph
graph = workflow.compile()

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Blog Generation System. Use POST /generate-blog to generate a blog."}

# FastAPI endpoint for blog generation
@app.post("/generate-blog")
async def generate_blog(request: BlogRequest):
    try:
        # Initialize state
        state = BlogState(topic=request.topic, research_data=[], blog_content="")
        # Run the workflow
        result = graph.invoke(state)
        return {"blog_content": result["blog_content"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating blog: {str(e)}")

# Run the FastAPI app (for local testing)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)