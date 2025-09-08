import os
import logging
import urllib.parse
from crewai import Agent, Task, Crew, LLM
from crewai_tools import MCPServerAdapter
from dotenv import load_dotenv
import asyncio
from crewai.tools import tool
import warnings
from pydantic import PydanticDeprecatedSince20
# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

context=None

warnings.filterwarnings("ignore", category=PydanticDeprecatedSince20)
warnings.filterwarnings("ignore", category=SyntaxWarning)
@tool("Update_context_tool")
def update_context(context_input: str):
    """This tool will be used to update the context for the LLM for example more details about the type of reddit post the user have to generate"""
    global context
    context = context_input
    return "context has been updated"
    

def setup_mcp_tools():
    """Set up MCP server connection and get tools"""
    runtime = os.getenv("CORAL_ORCHESTRATION_RUNTIME", None)
    if runtime is None:
        load_dotenv(override=True)

    # Get Coral server configuration
    base_url = os.getenv("CORAL_SSE_URL")
    agent_id = os.getenv("CORAL_AGENT_ID")

    coral_params = {
        "agentId": agent_id,
        "agentDescription": "An AI agent that generates Reddit posts about AI and ML topics with context engineering"
    }

    query_string = urllib.parse.urlencode(coral_params)
    CORAL_SERVER_URL = f"{base_url}?{query_string}"
    print(f"Connecting to Coral Server: {CORAL_SERVER_URL}")
    logger.info(f"Connecting to Coral Server: {CORAL_SERVER_URL}")

    # Set up MCP Server connection
    server_params = {
        "url": CORAL_SERVER_URL,
        "timeout": 600,
        "sse_read_timeout": 600,
        "transport": "sse"
    }
    
    mcp_server_adapter = MCPServerAdapter(server_params)
    return mcp_server_adapter.tools


async def main():
    # Get MCP tools
    mcp_tools = setup_mcp_tools()
    
    # Initialize the LLM with retry logic
    try:
        llm = LLM(
               model="openrouter/openai/gpt-4.1-mini",
               base_url="https://openrouter.ai/api/v1",
               api_key=os.getenv("OPENROUTER_API_KEY"),
        )
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {str(e)}")
        raise
    
    # Create the Reddit Content Strategist agent
    reddit_agent = Agent(
        role="Reddit Content Strategist",
        goal="Create personalized and engaging Reddit post ideas based on user context",
        backstory="""You are an expert Reddit content strategist who excels at creating 
        engaging content ideas tailored to specific niches and goals. You understand the 
        importance of context in content creation and can adapt your suggestions to match 
        different tones and objectives.""",
        llm=llm,
        tools=mcp_tools +[update_context],
        verbose=True
    )

    # Create the task for generating posts
    post_task = Task(
        description=f"""
        Primary Task: Mention Monitoring and Response

        Step 1: Wait For Mentions
        - ALWAYS start by calling wait_for_mentions tool
        - Keep calling it until you receive a mention
        - Do not proceed to other tasks and do not call anyother tools without a mention
        - Record threadId and senderId when mentioned
        
         Step 2: Process Mention
        - Analyze the message content carefully
        - Understand what kind of posts are requested and then you have to call the update context tool and input the context the agent is asking about that context will be used to generate the reddit posts.If the context is None .Then keep calling wait for mentions tool until you receive a mention.
        and then call the update_context tool with the context the agent is asking about.
        - Then call the send_message tool to send the generated posts back the agent that requested the posts.
        - Then again keep calling wait_for_mentions tool until you receive a mention.
        
        based on the following context:
        {context}
        - Generate posts based on the request
        - Send response in the same thread
         Generate 5 posts covering the topic agent asks.
         
        Generate 5 complete Reddit posts based on the provided context.

        Output Format:
        Post [number]:
        Title: [engaging title]
        Content: [detailed content]
        Keywords: [#relevant #hashtags]

        Important:
        - Follow the output format EXACTLY as shown above
        - Use clear separators between posts (empty line)
        - Make each post complete and ready to publish
        - Include relevant hashtags for better visibility""",
        expected_output="""Response to mentions containing exactly 5 posts:
        - Each post strictly following the format: number, title, content, hashtag keywords
        - Posts covering different AI/ML subtopics
        - Clear response sent back to the mentioning agent""",
        agent=reddit_agent
    )

    # Create and run the crew
    crew = Crew(
        agents=[reddit_agent],
        tasks=[post_task],
        verbose=True
    )


    while True:
        try:
            logger.info("Starting new Reddit post generation cycle")
            crew.kickoff()
            await asyncio.sleep(1)  # Fixed: await the sleep
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt, shutting down gracefully...")
            break
        except Exception as e:
            logger.error(f"Error in agent loop: {str(e)}")
            await asyncio.sleep(5)  # Fixed: await the sleep
    
  

if __name__ == "__main__":
    asyncio.run(main())
