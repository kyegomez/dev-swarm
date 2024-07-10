from dev_swarm.dev_swarm import DevSwarm


# Example usage
flow = "FunctionGenerator -> DocumentorAgent -> TesterAgent"
project = "openai_swarm"

dev_swarm = DevSwarm(max_loops=1, project=project, flow=flow)

output = dev_swarm.run(
    "Let's build an API that uses an LLM from OpenAI to generate code for the Google Calendar API."
)
print(output)
