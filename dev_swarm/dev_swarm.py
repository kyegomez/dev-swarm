from dev_swarm.documentor_agent import DocumentorAgent
from dev_swarm.tester_agent import TesterAgent
from dev_swarm.function_generator_agent import FunctionGeneratorAgent
from swarms.utils.loguru_logger import logger


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
        flow: str = "FunctionGenerator -> DocumentorAgent, TesterAgent",
        documentor_agent_name: str = "DocumentorAgent",
        tester_agent_name: str = "TesterAgent",
        function_generator_agent_name: str = "FunctionGeneratorAgent",
        max_loops: int = 1,
        project: str = "dev_swarm",
        *args,
        **kwargs,
    ):
        self.documentor_agent_name = documentor_agent_name
        self.tester_agent_name = tester_agent_name
        self.function_generator_agent_name = (
            function_generator_agent_name
        )
        self.max_loops = max_loops
        self.flow = flow
        self.max_loops = max_loops
        self.project = project

        # Initialize the agents
        self.documentor_agent = DocumentorAgent(
            agent_name=documentor_agent_name,
            max_loops=max_loops,
            module=project,
            docs_folder_path=project,
        )

        self.tester_agent = TesterAgent(
            agent_name=tester_agent_name,
            max_loops=max_loops,
            module=project,
            tests_folder_path=project,
        )

        self.function_generator_agent = FunctionGeneratorAgent(
            folder_path=project
        )

        self.agents = [
            self.documentor_agent,
            self.tester_agent,
            self.function_generator_agent,
        ]

    def run(self, task: str) -> str:
        """
        Runs the swarm task with the provided flow configuration.

        Args:
            task (str): The task to start.

        Returns:
            Optional[str]: The output of the rearrange function.
        """
        try:
            # out = AgentRearrange(
            #     agents=self.agents,
            #     flow=self.flow,
            #     max_loops=self.max_loops,
            # )
            # response = out.run(task)
            # return response
            logger.info(f"Running DevSwarm for task: {task}")
            generator = self.function_generator_agent.run(task)
            print("type: ", type(generator))
            logger.info(f"Generated code: {generator}")

            # Document the code
            document = self.documentor_agent.run(generator)
            logger.info(f"Documented code: {document}")

            # Test the code
            test = self.tester_agent.run(generator)
            logger.info(f"Tested code: {test}")

            return logger.info("DevSwarm completed successfully.")
        except Exception as e:
            print(f"Error: {e}")
            return None
