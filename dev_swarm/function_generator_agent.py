from dev_swarm.documentor_agent import model
from dev_swarm.prompts import FUNCTION_GENERATOR_PROMPT
from swarms import Agent
from loguru import logger
import os
from swarms import extract_code_from_markdown


class FunctionGeneratorAgent(Agent):
    """
    Agent class for generating function code based on a given task.

    Args:
        agent_name (str, optional): Name of the agent. Defaults to "FunctionGenerator".
        system_prompt (str, optional): Prompt to use for the language model. Defaults to FUNCTION_GENERATOR_PROMPT.
        llm (LanguageModel, optional): Language model to use. Defaults to model.
        max_loops (int, optional): Maximum number of loops for generating code. Defaults to 1.
        autosave (bool, optional): Whether to autosave the agent's state. Defaults to True.
        saved_state_path (str, optional): Path to save the agent's state. Defaults to "function_generator.json".
        stopping_token (str, optional): Token to stop code generation. Defaults to "Stop!".
        interactive (bool, optional): Whether to run the agent in interactive mode. Defaults to True.
        context_length (int, optional): Length of the context for the language model. Defaults to 8000.
        **kwargs: Additional keyword arguments to pass to the base class.

    Attributes:
        agent_name (str): Name of the agent.
        system_prompt (str): Prompt to use for the language model.
        llm (LanguageModel): Language model to use.
        max_loops (int): Maximum number of loops for generating code.
        autosave (bool): Whether to autosave the agent's state.
        saved_state_path (str): Path to save the agent's state.
        stopping_token (str): Token to stop code generation.
        interactive (bool): Whether to run the agent in interactive mode.
        context_length (int): Length of the context for the language model.

    Methods:
        run(task: str, folder_path: str, file_name: str, *args, **kwargs) -> str:
            Runs the FunctionGeneratorAgent for the given task and generates code.
            Saves the generated code to a file in the specified folder path with the given file name.
            Returns the path of the created file.

        create_file(content: str, folder_path: str, file_name: str) -> str:
            Creates a file with the given content in the specified folder path with the given file name.
            Returns the path of the created file.
    """

    def __init__(
        self,
        agent_name: str = "FunctionGenerator",
        system_prompt: str = FUNCTION_GENERATOR_PROMPT,
        llm=model,
        max_loops: int = 1,
        autosave: bool = True,
        saved_state_path: str = "function_generator.json",
        stopping_token: str = "Stop!",
        interactive: bool = True,
        context_length: int = 8000,
        **kwargs,
    ):
        super().__init__(
            agent_name=agent_name,
            system_prompt=system_prompt,
            llm=llm,
            max_loops=max_loops,
            autosave=autosave,
            saved_state_path=saved_state_path,
            stopping_token=stopping_token,
            interactive=interactive,
            context_length=context_length,
            **kwargs,
        )

    def run(
        self,
        task: str,
        folder_path: str,
        file_name: str,
        *args,
        **kwargs,
    ) -> str:
        """
        Runs the FunctionGeneratorAgent for the given task and generates code.
        Saves the generated code to a file in the specified folder path with the given file name.
        Returns the path of the created file.

        Args:
            task (str): Task for which to generate code.
            folder_path (str): Path of the folder where the file should be saved.
            file_name (str): Name of the file to be created.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            str: Path of the created file.
        """
        logger.info(
            f"Running FunctionGeneratorAgent for task: {task}"
        )
        output = super().run(task, *args, **kwargs)
        output = extract_code_from_markdown(output)
        logger.debug(f"Generated output: {output}")
        file_path = self.create_file(output, folder_path, file_name)
        return file_path

    def create_file(
        self, content: str, folder_path: str, file_name: str
    ) -> str:
        """
        Creates a file with the given content in the specified folder path with the given file name.
        Returns the path of the created file.

        Args:
            content (str): Content to be written to the file.
            folder_path (str): Path of the folder where the file should be created.
            file_name (str): Name of the file to be created.

        Returns:
            str: Path of the created file.
        """
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "w") as file:
            file.write(content)
        logger.info(f"File created at {file_path}")
        return file_path
