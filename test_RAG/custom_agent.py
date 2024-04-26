
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.agent import FunctionCallingAgentWorker, AgentRunner
from llama_index.llms.openai import OpenAI
_GPT_MODEL = "gpt-3.5-turbo"



def script_runner(code_str):
    print("Running Script ", code_str)



llm = OpenAI(_GPT_MODEL)
# Load data
docs = SimpleDirectoryReader(input_dir='./test_RAG/data3').load_data()

# build index
index = VectorStoreIndex.from_documents(docs)

engine = index.as_query_engine(llm=llm)

query_engine_tool = QueryEngineTool(
    query_engine=engine,
    metadata=ToolMetadata(
        name='RAG_ENGINE',
        description=(
            "Provides information about Continuous Double Auctions."
            "Provides Python Functions that can be called"
        )
    )
)

my_aunt = FunctionCallingAgentWorker.from_tools(
    [query_engine_tool], llm=llm, verbose=True,
)

my_agent_alp = AgentRunner(agent_worker=my_aunt)

response = my_agent_alp.chat("sell 183 shares at 3")

print(response)