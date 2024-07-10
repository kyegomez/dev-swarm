from swarms import Agent
import os

from dotenv import load_dotenv
from swarms import OpenAIChat
from dev_swarm.prompts import DOCUMENTATION_WRITER_SOP
from loguru import logger
from swarms.utils.loguru_logger import logger
from dev_swarm.utils import create_file

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

model = OpenAIChat(
    model_name="gpt-4-1106-preview",
    openai_api_key=api_key,
    max_tokens=4000,
)

# Ensure the log directory exists
log_directory = "dev_swarm_logs"
os.makedirs(log_directory, exist_ok=True)

logger.add(
    os.path.join(log_directory, "documentor_agent.log"),
    rotation="1 MB",
)


class DocumentorAgent(Agent):
    """
    Agent class for documenting items.

    Args:
        items (List[Any]): List of items to be documented.
        agent_name (str, optional): Name of the agent. Defaults to "DocumentorAgent".
        llm (model, optional): LLM model. Defaults to model.
        max_loops (int, optional): Maximum number of loops. Defaults to 1.
        module (str, optional): Module path. Defaults to "docs/swarms/structs".
        docs_folder_path (str, optional): Folder path for storing the documentation files. Defaults to "docs/swarms/structs".
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Attributes:
        items (List[Any]): List of items to be documented.
        module (str): Module path.
        agent_name (str): Name of the agent.
        max_loops (int): Maximum number of loops.
        docs_folder_path (str): Folder path for storing the documentation files.

    Methods:
        run(task: str, *args, **kwargs): Runs the DocumentorAgent for the specified task.
        fetch_docs(item): Fetches the documentation and source code for the given item.
        create_file(item, content: str = None): Creates a documentation file for the given item.

    """

    def __init__(
        self,
        agent_name: str = "DocumentorAgent",
        llm=model,
        max_loops: int = 1,
        module: str = None,
        docs_folder_path: str = None,
        *args,
        **kwargs,
    ):
        super(DocumentorAgent, self).__init__(
            agent_name=agent_name,
            llm=model,
            max_loops=max_loops,
            streaming_on=True,
            *args,
            **kwargs,
        )
        self.module = module
        self.agent_name = agent_name
        self.max_loops = max_loops
        self.docs_folder_path = docs_folder_path

    def run(self, task: str, *args, **kwargs) -> str:
        """
        Runs the DocumentorAgent for the specified task.

        Args:
            task (str): The task to be performed.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        """
        logger.info(f"Running DocumentorAgent for task: {task}")

        processed_content = super().run(
            DOCUMENTATION_WRITER_SOP(
                task, self.module, *args, **kwargs
            )
        )

        logger.info(f"Documentation: {processed_content}")

        doc_content = f"{processed_content}\n"
        file_path = create_file(self.module, doc_content, ".py")
        logger.info(f"Documentation created at {file_path}")

        return processed_content
