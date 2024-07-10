[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)

# Dev Swarm



## Install

```bash
$ pip install dev-swarm
```


## Usage

````python
from dev_swarm import DevSwarm

# Example usage
items = []
module = "docs/swarms/structs"
docs_folder_path = "docs/swarms/structs"
tests_folder_path = "tests/memory"
flow = "FunctionGenerator -> DocumentorAgent -> H -> TesterAgent -> H"

dev_swarm = DevSwarm(
  items=items,
  documentor_agent_name="DocumentorAgent",
  tester_agent_name="TesterAgent",
  function_generator_agent_name="FunctionGenerator",
  max_loops=1,
  module=module,
  docs_folder_path=docs_folder_path,
  tests_folder_path=tests_folder_path,
  flow=flow,
)

output = dev_swarm.run(task="Start your tasks")
print(output)

```


# Citation
Please cite Swarms in your paper or your project if you found it beneficial in any way! Appreciate you.

```bibtex
@misc{swarms,
  author = {Gomez, Kye},
  title = {{Swarms: The Multi-Agent Collaboration Framework}},
  howpublished = {\url{https://github.com/kyegomez/swarms}},
  year = {2023},
  note = {Accessed: Date}
}
```

