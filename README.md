

# SceneMachine


SceneMachine is a Python prototype for generating, solving, and experimenting with classic cosy-style crime puzzles. It leverages large language models (LLMs) to create logic-based mysteries, and provides utilities for both puzzle generation and solution.
 
**Disclaimer:** This is a prototype, built for a bit of fun. There is absolutely no warranty, and the quality of the generated puzzles varies from OK to absolutely terrible :) Enjoy at your own risk!

---

## Features

- **Automatic Puzzle Generation:** Create crime puzzles in the style of classic British mysteries.
- **LLM Integration:** Modular architecture for integrating with various LLM providers.
- **Extensible Modes:** Easily add new puzzle types, solution modes, or LLM backends.
- **Example Outputs:** Browse the `examples/` directory for sample generated puzzles and solutions.
- **Developer Utilities:** Includes tasks for linting, formatting, type checking, and security analysis.

---


## OpenAI API Setup

To use OpenAI (or other LLM providers), you will need to provide an API key. The recommended way is to create a `.env` file in the project root with your credentials:

```
OPENAI_API_KEY=sk-...
```

Replace `sk-...` with your actual OpenAI API key. The application will load this automatically if you have a `.env` file present.

If you use a different provider, check the code or configuration for the required environment variable names.

---

## Installation

1. **Clone the repository:**
	 ```sh
	 git clone https://github.com/seamus-brady/SceneMachine.git
	 cd SceneMachine
	 ```
2. **Install dependencies** (preferably in a virtual environment):
	 ```sh
	 pip install -r requirements.txt
	 ```

---

## Usage

### Task Automation with Invoke

SceneMachine uses [Invoke](https://www.pyinvoke.org/) for common development and usage tasks. All tasks are defined in `tasks.py`.

**List available tasks:**
```sh
invoke --list
```

**Run all checks (lint, type, format, security, tests):**
```sh
invoke checks
```

**Run unit tests:**
```sh
invoke test
```

**Format code:**
```sh
invoke formatter
```

**Type check:**
```sh
invoke mypy
```

**Lint:**
```sh
invoke linter
```

**Security check:**
```sh
invoke bandit
```

**Sort imports:**
```sh
invoke isort
```

### Generating a Puzzle


To see how to generate a puzzle, look at the unit tests in `src/test/test_crime_puzzle_generator.py`. This file demonstrates how to invoke the puzzle generation logic programmatically.

There is no command-line or invoke task for puzzle generation at this time.

---

## Example Output

Example generated puzzles can be found in the `examples/` directory, such as:

- `the_apple_tart_affair_at_larkham_cottage.md`
- `the_bitter_almonds_at_thornley_garth.md`
- `the_case_of_the_forged_invoices_at_thornley_garth.md`

Each file contains a full puzzle scenario, clues, and solution in a readable Markdown format.

---

## Running Unit Tests

Unit tests are located in the `src/test/` directory. You can run all tests with:

```sh
invoke test
```

---

## Project Structure

- `src/` - Main source code
	- `scenemachine/` - Core logic, LLM integration, modes, utilities
	- `config/` - Configuration files and prompts
	- `test/` - Unit tests
- `examples/` - Example generated puzzles
- `tasks.py` - Invoke tasks for development and usage
- `requirements.txt` - Python dependencies

---

## License

This project is licensed under the [MIT License](LICENSE).
