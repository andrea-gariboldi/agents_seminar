# LLM Agents Seminar
## Goal
The goal of this repository is to introduce the audience to basic concepts when developing Large Language Models (LLMs) agents. In particular, this seminar is designed to explain the need of LLM based agents, tool calling and output validation.

## How to use
The notebook provided is designed to be self-contained and run through Google colab. For sharing an editable copy of the notebook, use this link: [Agents Seminar Colab](https://colab.research.google.com/github/andrea-gariboldi/agents_seminar/blob/master/workshop_start.ipynb?copy=true). Important: when opening in Colab, make sure to change the runtime to use GPU, as it will be needed to make LLM run smoothly.

The ```workshop_start.ipynb``` file is the starting point of the seminar. It contains a partially implemented agent that is supposed to solve a clustering task using a dataset provided in the ```agents_workspace/data/``` folder. From here, the goal is to implement together with the audience a minimal set of tools for reaching the goal.

The ```solution.ipynb``` file contains a possible solution to the clustering task, including the implementation of the tools and the agent configuration.

## Already developed
- ``utils/agent_utils.py`` contains the ``run_agent`` function for running the agent loop. 
- ``utils/printing_utils.py`` implements the printing utils, using different colors for each agent call (e.g tool call, thinking tokens).
- ``utils/workspace_utils.py`` contains the helpers for deleting the workspace before the start of a new agent run, avoiding lingering files from previous runs.
- ``utils/dataset_utils.py`` helpers for metrics calculation.
- ``eval/evaluate_results.py`` runs the produces clustering script and evaluates the performances of the produced clusters.

## Repository structure

```
.
├── README.md
├── env.yaml                  # (Conda) Environment configuration file
├── workshop_start.ipynb      # Starting notebook for the seminar
├── solution.ipynb             # Complete solution with agent implementation
├── agents_workspace/
│   └── data/
│       └── ecoli.csv          # Ecoli dataset for clustering task
├── tools/
│   └── bash_tool.py           # Bash execution tool for agent
├── eval/
│   └── evaluate_result.py     # Evaluation functions for agent results
└── utils/
    ├── workspace_utils.py     # Workspace management utilities
    ├── dataset_utils.py       # Dataset handling utilities
    ├── agent_utils.py         # Agent helper functions
    ├── agent_output.py        # Agent output structures
    └── printing_utils.py      # Output formatting utilities
```


## Dataset
The dataset provided is an adapted version of the ecoli dataset from the UCI Machine Learning Repository ([link](https://archive.ics.uci.edu/dataset/39/ecoli)).