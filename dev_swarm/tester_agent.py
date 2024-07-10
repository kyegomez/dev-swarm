import os
import re
from dotenv import load_dotenv
from loguru import logger
from swarms import Agent
from dev_swarm.documentor_agent import model
from dev_swarm.prompts import TEST_WRITER_SOP_PROMPT
from dev_swarm.utils import create_file

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
        agent_name: str = "TesterAgent",
        llm=model,
        max_loops: int = 1,
        module: str = "tests/memory",
        tests_folder_path: str = "tests/memory",
        *args,
        **kwargs,
    ):
        super(TesterAgent, self).__init__(
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
        self.tests_folder_path = tests_folder_path

    def run(self, task: str, *args, **kwargs):
        """
        Runs the tester agent for the specified task.

        Args:
            task (str): The task to be performed.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        """
        response = super().run(
            TEST_WRITER_SOP_PROMPT(task, self.module, *args, **kwargs)
        )
        processed_content = extract_code_from_markdown(response)
        test_content = f"{processed_content}\n"
        file_path = create_file(self.module, test_content, ".py")
        logger.info(f"Test created for item: at {file_path}")

        return processed_content


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
