import inspect
import os
import re
import threading
from dotenv import load_dotenv
from loguru import logger
from swarms import Agent
from typing import List, Any
from dev_swarm.documentor_agent import model
from dev_swarm.prompts import TEST_WRITER_SOP_PROMPT

load_dotenv()
# Ensure the log directory exists
log_directory = "dev_swarm_logs"
os.makedirs(log_directory, exist_ok=True)

logger.add(
    os.path.join(log_directory, "tester_agent.log"), rotation="1 MB"
)


def extract_code_from_markdown(markdown_content: str):
    """
    Extracts code blocks from a Markdown string and returns them as a single string.

    Args:
    - markdown_content (str): The Markdown content as a string.

    Returns:
    - str: A single string containing all the code blocks separated by newlines.
    """
    pattern = r"```(?:\w+\n)?(.*?)```"
    matches = re.findall(pattern, markdown_content, re.DOTALL)
    return "\n".join(code.strip() for code in matches)


class TesterAgent(Agent):
    """
    A class representing a tester agent.

    Args:
        items (List[Any]): A list of items to be tested.
        agent_name (str, optional): The name of the tester agent. Defaults to "TesterAgent".
        llm (model, optional): The language model to be used. Defaults to model.
        max_loops (int, optional): The maximum number of loops. Defaults to 1.
        module (str, optional): The module to be used. Defaults to "tests/memory".
        tests_folder_path (str, optional): The folder path for storing the tests. Defaults to "tests/memory".

    Attributes:
        items (List[Any]): A list of items to be tested.
        module (str): The module to be used.
        agent_name (str): The name of the tester agent.
        max_loops (int): The maximum number of loops.
        tests_folder_path (str): The folder path for storing the tests.

    Methods:
        run(task: str, *args, **kwargs): Runs the tester agent for the specified task.
        fetch_docs(item): Fetches the documentation and source code for the specified item.
        create_file(item, content: str = None): Creates a test file for the specified item.

    """

    def __init__(
        self,
        items: List[Any],
        agent_name: str = "TesterAgent",
        llm=model,
        max_loops: int = 1,
        module: str = "tests/memory",
        tests_folder_path: str = "tests/memory",
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
        self.tests_folder_path = tests_folder_path

    def run(self, task: str, *args, **kwargs):
        """
        Runs the tester agent for the specified task.

        Args:
            task (str): The task to be performed.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        """
        logger.info(f"Running TesterAgent for task: {task}")

        def process_item(item):
            try:
                prompt = self.fetch_docs(item)
                logger.debug(
                    f"Fetched docs for item: {item.__name__}"
                )

                processed_content = super().run(
                    TEST_WRITER_SOP_PROMPT(
                        prompt, self.module, *args, **kwargs
                    )
                )
                logger.debug(
                    f"Processed content for item: {item.__name__}"
                )

                processed_content = extract_code_from_markdown(
                    processed_content
                )
                test_content = (
                    f"# {item.__name__}\n\n{processed_content}\n"
                )
                file_path = self.create_file(item, test_content)
                logger.info(
                    f"Test created for item: {item.__name__} at {file_path}"
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
        Fetches the documentation and source code for the specified item.

        Args:
            item: The item to fetch the documentation and source code for.

        Returns:
            str: The fetched documentation and source code.

        """
        doc = inspect.getdoc(item)
        source = inspect.getsource(item)
        is_class = inspect.isclass(item)
        item_type = (
            "Class"
            if is_class
            else "Function" if inspect.isfunction(item) else "Item"
        )
        input_content = f"{item_type} Name: {item.__name__}\n\nDocumentation:\n{doc}\n\nSource Code:\n{source}"
        logger.debug(
            f"Input content created for item: {item.__name__}"
        )
        return input_content

    def create_file(self, item, content: str = None):
        """
        Creates a test file for the specified item.

        Args:
            item: The item to create the test file for.
            content (str, optional): The content of the test file. Defaults to None.

        Returns:
            str: The file path of the created test file.

        """
        os.makedirs(self.tests_folder_path, exist_ok=True)
        file_path = os.path.join(
            self.tests_folder_path, f"{item.__name__.lower()}.py"
        )
        with open(file_path, "w") as file:
            file.write(content)
        logger.debug(
            f"File created at {file_path} for item: {item.__name__}"
        )
        return file_path


# def main(module: str = "tests/memory"):
#     items = [
#         DictInternalMemory,
#         DictSharedMemory,
#         LangchainChromaVectorMemory,
#         # Add other items as needed
#     ]

#     logger.info(f"Starting test generation for module: {module}")
#     agent = TesterAgent(items=items, module=module)
#     agent.run(task="Generate Tests")
#     logger.info(f"Tests generated in {module} directory.")


# if __name__ == "__main__":
#     main()
