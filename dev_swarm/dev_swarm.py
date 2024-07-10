from dev_swarm.documentor_agent import DocumentorAgent
from dev_swarm.tester_agent import TesterAgent

items = []

module = "docs/swarms/structs"
docs_folder_path = "docs/swarms/structs"
tests_folder_path = "tests/memory"

documentor_agent = DocumentorAgent(
    items=[],
    agent_name="DocumentorAgent",
    max_loops=1,
    module=module,
    docs_folder_path=docs_folder_path,
)

tester_agent = TesterAgent(
    items=[],
    agent_name="TesterAgent",
    max_loops=1,
    module=module,
    tests_folder_path=docs_folder_path,
)

agents = [documentor_agent, tester_agent]

flow = "DocumentorAgent -> H -> TesterAgent -> H"
