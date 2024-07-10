from dev_swarm.documentor_agent import DocumentorAgent
from dev_swarm.tester_agent import TesterAgent
from dev_swarm.function_generator_agent import FunctionGeneratorAgent
from swarms import rearrange
from typing import List, Optional, Any


class DevSwarm:
    """
    Initializes the DevSwarm with customizable settings.

    Args:
        items (List[str]): A list of items for the agents.
        documentor_agent_name (str): The name of the DocumentorAgent.
        tester_agent_name (str): The name of the TesterAgent.
        function_generator_agent_name (str): The name of the FunctionGeneratorAgent.
        max_loops (int): The maximum number of loops for the agents.
        module (str): The module path for the agents.
        docs_folder_path (str): The path to the documentation folder.
        tests_folder_path (str): The path to the tests folder.
        flow (str): The flow configuration for rearranging the agents.
    """

    def __init__(
        self,
        items: List[Any],
        documentor_agent_name: str,
        tester_agent_name: str,
        function_generator_agent_name: str,
        max_loops: int,
        module: str,
        docs_folder_path: str,
        tests_folder_path: str,
        flow: str,
    ):
        self.items = items
        self.documentor_agent = DocumentorAgent(
            items=items,
            agent_name=documentor_agent_name,
            max_loops=max_loops,
            module=module,
            docs_folder_path=docs_folder_path,
        )
        self.tester_agent = TesterAgent(
            items=items,
            agent_name=tester_agent_name,
            max_loops=max_loops,
            module=module,
            tests_folder_path=tests_folder_path,
        )
        self.function_generator_agent = FunctionGeneratorAgent(
            agent_name=function_generator_agent_name,
        )
        self.agents = [self.documentor_agent, self.tester_agent]
        self.flow = flow

    def run(self, task: str) -> Optional[str]:
        """
        Runs the swarm task with the provided flow configuration.

        Args:
            task (str): The task to start.

        Returns:
            Optional[str]: The output of the rearrange function.
        """
        try:
            out = rearrange(self.agents, self.flow, task=task)
            return out
        except Exception as e:
            print(f"Error: {e}")
            return None
