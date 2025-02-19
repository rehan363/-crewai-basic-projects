# Random Blog Generator and Summarizer

## Overview

This project is a Python-based application that generates a random blog post on the latest trending topic in 2025 and then summarizes it into one concise sentence. The project leverages the [CrewAI](https://www.crewai.com/) framework for managing the flow of operations, the [litellm](https://github.com/litellm) library for content generation, and the `python-dotenv` package for managing environment variables.

## Features

- **Random Blog Generation:**  
  Uses a language model to generate a blog post on a trending 2025 topic.
  
- **One-line Summarization:**  
  Summarizes the generated blog post into a single sentence.

- **Flow-based Design:**  
  Utilizes CrewAI's decorators (`@start`, `@listen`) to define and control the application's workflow.

## Technologies Used

- **Python:** Primary programming language.
- **CrewAI:** For building and managing conversational flows.
- **litellm:** To interact with language models for generating and summarizing content.
- **python-dotenv:** For loading environment variables (e.g., API keys).

