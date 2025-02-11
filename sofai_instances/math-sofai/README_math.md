# Math Solver using SOFAI

This repository contains an implementation of an arithmetic (BODMAS) problem-solving system using `sofai_tool`.

## Features

- **Problem Generation**: Random arithmetic expressions are generated.
- **System 1 Solver**: Uses an LLM (Mistral) to evaluate expressions.
- **System 2 Solver**: Uses Python’s `eval()` function for deterministic computation.
- **Metacognition**: Decides when to switch System 1 to System 2.

## Setup

1. Install dependencies:
   ```sh
   cd sofai_tool
   pip install .
