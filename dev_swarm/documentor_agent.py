from swarms import Agent
import inspect
import os
import threading

from dotenv import load_dotenv
from swarms import OpenAIChat
from dev_swarm.prompts import DOCUMENTATION_WRITER_SOP
from typing import List, Any
from loguru import logger

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
        items: List[Any],
        agent_name: str = "DocumentorAgent",
        llm=model,
        max_loops: int = 1,
        module: str = "docs/swarms/structs",
        docs_folder_path: str = "docs/swarms/structs",
        *args,
        **kwargs,
    ):
        super().__init__(
            agent_name, llm=llm, max_loops=max_loops, *args, **kwargs
        )
        self.items = items
        self.module = module
        self.agent_name = agent_name
        self.max_loops = max_loops
        self.docs_folder_path = docs_folder_path

    def run(self, task: str, *args, **kwargs):
        """
        Runs the DocumentorAgent for the specified task.

        Args:
            task (str): The task to be performed.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        """
        logger.info(f"Running DocumentorAgent for task: {task}")

        def process_item(item):
            try:
                prompt = self.fetch_docs(item)
                logger.debug(
                    f"Fetched docs for item: {item.__name__}"
                )

                processed_content = super().run(
                    DOCUMENTATION_WRITER_SOP(
                        prompt, self.module, *args, **kwargs
                    )
                )
                logger.debug(
                    f"Processed content for item: {item.__name__}"
                )

                doc_content = (
                    f"# {item.__name__}\n\n{processed_content}\n"
                )
                file_path = self.create_file(item, doc_content)
                logger.info(
                    f"Documentation created for item: {item.__name__} at {file_path}"
                )

            except Exception as e:
                logger.error(
                    f"Error processing item {item.__name__}: {e}"
                )

        threads = []
        for item in self.items:
            thread = threading.Thread(
                target=process_item, args=(item,)
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def fetch_docs(self, item):
        """
        Fetches the documentation and source code for the given item.

        Args:
            item: The item to fetch the documentation for.

        Returns:
            str: The fetched documentation and source code.

        """
        doc = inspect.getdoc(item)
        source = inspect.getsource(item)
        is_class = inspect.isclass(item)
        item_type = "Class Name" if is_class else "Name"
        input_content = f"{item_type}: {item.__name__}\n\nDocumentation:\n{doc}\n\nSource Code:\n{source}"
        logger.debug(
            f"Input content created for item: {item.__name__}"
        )
        return input_content

    def create_file(self, item, content: str = None):
        """
        Creates a documentation file for the given item.

        Args:
            item: The item to create the documentation file for.
            content (str, optional): The content to be written in the file. Defaults to None.

        Returns:
            str: The file path of the created documentation file.

        """
        os.makedirs(self.module, exist_ok=True)
        file_path = os.path.join(
            self.docs_folder_path, f"{item.__name__.lower()}.md"
        )
        with open(file_path, "w") as file:
            file.write(content)
        logger.debug(
            f"File created at {file_path} for item: {item.__name__}"
        )
        return file_path
