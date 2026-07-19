# Test Case Generator

## Overview
The Test Case Generator is a Python application designed to automate the creation of test cases for payment processes. It leverages large language models (LLMs) to generate comprehensive test cases based on specified requirements.

## Agentic Project
The Test Case Generator is part of the Agentic Project, which aims to enhance automation in software testing through advanced AI-driven solutions. This project focuses on creating test cases dynamically, improving testing efficiency and accuracy, and reducing human error.

### Usages
- **Automated Test Case Generation:** Users can input requirements and the tool generates test cases that cover various scenarios, especially for payment methods.
- **Integration with LLMs:** The application supports multiple providers including OpenAI, Google Gemini, and Ollama, enabling flexibility in choosing the underlying technology for test case generation.
- **Ease of Configuration:** Through environment variables, users can easily set up their testing environment and API keys.
- **Data Handling:** The application can manage various input requirements and output formats, streamlining test management.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd TestCaseGenerator
   ```

2. **Set Up a Virtual Environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Environment Variables:**
   Copy `.env.example` to `.env` and update with your API keys and settings.
   ```dotenv
   PROVIDER=openai
   MODEL=gpt-4o-mini
   OPENAI_API_KEY=your_openai_api_key
   GOOGLE_API_KEY=your_google_api_key
   OLLAMA_HOST=http://localhost:11434
   ```

## Usage

To run the application, execute:  
python3 -m src.agents.testcase_agent  
python3 -m src.agents_langchain.testcase_langchain
