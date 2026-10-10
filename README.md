# Local Intelligence

A lightweight, local-first intelligent assistant designed to execute tasks through modular tools and locally running language models.

The goal of Local Intelligence is to build a flexible assistant that can understand user requests, select appropriate tools, and execute actions locally—without depending on cloud-based AI services.

## Goals

- **Local-first:** Run language models locally and minimize dependence on external services.
- **Model-independent:** Support different LLM backends through a common interface.
- **Modular tools:** Add new capabilities without coupling them to a specific model.
- **Controlled execution:** Validate tool arguments and check permissions before executing actions.
- **Lightweight architecture:** Keep the core understandable and suitable for future deployment on small computers and home-lab hardware.

## Current Features

- Local language model integration through Needle.
- A model-independent `BaseLLM` interface.
- A tool registry for registering and executing tools.
- Argument validation and permission checks.
- Arithmetic tools for addition, subtraction, multiplication, and division.
- A command-line interface for interacting with the assistant.
- Task execution through a dedicated controller.

## Architecture

```text
User
 |
 v
CLI
 |
 v
ModelController
 |
 v
BaseLLM
 |
 v
NeedleLLM
 |
 v
Local Model
 |
 v
Tool Calls
 |
 v
TaskController
 |
 v
ToolRegistry
 |
 v
PermissionGate + Argument Validation
 |
 v
Tool Execution
```

The LLM interface separates model integration from the rest of the application. This makes it possible to experiment with different local models without rewriting the tool system.

## Tech Stack

- **Language:** Python
- **Model integration:** `cactus-needle`
- **Development environment:** Python virtual environment
- **Version control:** Git and GitHub

## Getting Started

### Requirements

- Python 3.10 or later
- Git
- A compatible local model supported by Needle

### Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/local-intelligence.git
cd local-intelligence
```

Create and activate a virtual environment on Windows:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

Install the project's dependencies using its dependency file, once provided.

### Run

From the project root, use Windows CMD:

```cmd
set PYTHONPATH=src
python -m src.core.cli
```

You can then enter requests such as:

```text
You: Add 10 and 5
Result: {'result': 15.0}

You: Multiply 6 by 7
Result: {'result': 42.0}
```

Type `exit` to quit.

## Project Status

**Early development.**

The core tool-execution structure and initial Needle integration are in place. Model selection, natural-language reliability, and additional assistant capabilities are still being explored.

## Roadmap

- [x] Establish the core tool interface and registry.
- [x] Add argument validation and permission checks.
- [x] Implement basic arithmetic tools.
- [x] Introduce a model-independent LLM interface.
- [x] Integrate Needle through an LLM adapter.
- [ ] Evaluate alternative local language models.
- [ ] Improve tool-selection reliability.
- [ ] Develop a dedicated agent and reasoning loop.
- [ ] Add more useful local tools.
- [ ] Explore deployment on Raspberry Pi and home-lab systems.

## Design Philosophy

Local Intelligence is being developed incrementally. The focus is on keeping components small, replaceable, and easy to understand rather than building a large framework before the essential functionality is reliable.

## License

No license has been selected yet. Until one is added, the project should be treated as having all rights reserved.