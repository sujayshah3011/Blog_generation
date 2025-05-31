# Blog Generation System

A FastAPI-based application that leverages Large Language Models (LLMs) and research tools to automatically generate blog posts on a given topic. This system uses LangGraph to orchestrate a workflow involving research (via Wikipedia and Tavily Search) and content generation (via Google's Gemini model).

## Features

*   **Topic-based Blog Generation:** Provide a topic, and the system generates a blog post.
*   **Automated Research:** Utilizes Wikipedia and Tavily Search to gather relevant information.
*   **Structured Output:** Generates blog content in Markdown format with clear sections:
    *   Heading
    *   Introduction
    *   Content (supported by research)
    *   Summary
*   **LLM Powered:** Uses Google's Gemini model for natural language understanding and generation.
*   **Workflow Orchestration:** Employs LangGraph to manage the sequence of research and generation tasks.
*   **FastAPI Backend:** Provides a robust and easy-to-use API.

## Technologies Used

*   Python 3.x
*   FastAPI: For building the API.
*   Pydantic: For data validation.
*   Langchain: Framework for developing applications powered by LLMs.
    *   `langchain-google-genai`: Integration with Google's Generative AI models.
    *   `langchain-community`: Community-contributed tools and utilities (Wikipedia, Tavily Search).
*   LangGraph: For building stateful, multi-actor applications with LLMs.
*   `python-dotenv`: For managing environment variables.
*   Uvicorn: ASGI server for running FastAPI.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone git@github.com:sujayshah3011/Blog_generation.git
    cd Blog_generation
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`
    ```

3.  **Install dependencies:**
    Make sure you have your `requirements.txt` file correctly populated. The installation process might have highlighted some conflicts with other packages in your global/previous environment. For a clean setup for this project, ensure `requirements.txt` reflects the necessary versions.
    ```bash
    pip install -r requirements.txt
    ```
    If you encountered dependency issues previously, you might need to adjust `requirements.txt` or ensure your virtual environment is clean. The last successful installation attempt in our conversation resulted in:
    ```pip-requirements
    fastapi==0.115.0
    uvicorn==0.30.6
    langchain~=0.3.1  # Updated from 0.3.0
    langchain-community~=0.3.1 # Updated from 0.3.0
    langchain-google-genai==2.0.0
    langgraph # No version specified, pip will pick latest compatible
    python-dotenv==1.0.1
    pydantic==2.9.2
    # Potentially add langsmith~=0.3.18 if embedchain conflict persists elsewhere
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory of the project:
    ```env
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
    TAVILY_API_KEY="YOUR_TAVILY_API_KEY"
    ```
    Replace `"YOUR_GOOGLE_API_KEY"` and `"YOUR_TAVILY_API_KEY"` with your actual API keys.

## Running the Application

You can run the application using Uvicorn. The `blog_generation_system.py` script includes a main block to run the server:

```bash
python blog_generation_system.py
```

Alternatively, you can run it directly with Uvicorn for more options (like auto-reload):

```bash
uvicorn blog_generation_system:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at `http://localhost:8000`.

## API Endpoints

### Root

*   **URL:** `/`
*   **Method:** `GET`
*   **Description:** Welcome message for the API.
*   **Success Response (200 OK):**
    ```json
    {
        "message": "Welcome to the Blog Generation System. Use POST /generate-blog to generate a blog."
    }
    ```

### Generate Blog

*   **URL:** `/generate-blog`
*   **Method:** `POST`
*   **Description:** Generates a blog post based on the provided topic.
*   **Request Body (application/json):**
    ```json
    {
        "topic": "Your desired blog topic"
    }
    ```
*   **Success Response (200 OK):**
    ```json
    {
        "blog_content": "# Blog Title\\n\\n## Introduction\\n... (markdown content) ..."
    }
    ```
*   **Error Response (500 Internal Server Error):**
    ```json
    {
        "detail": "Error generating blog: <error_message>"
    }
    ```

## Example Usage

Here's an example of how to interact with the `/generate-blog` endpoint.

**Request:**

Using `curl`:
```bash
curl -X POST "http://localhost:8000/generate-blog" \
-H "Content-Type: application/json" \
-d '{
    "topic": "The Impact of AI on Modern Software Development"
}'
```

**Plausible Response (output will vary based on LLM generation):**

```json
{
    "blog_content": "# The Impact of AI on Modern Software Development\n\n**Introduction:**\n\nThe software development landscape is undergoing a dramatic transformation, fueled by the rapid advancements in artificial intelligence (AI).  No longer a futuristic fantasy, AI is becoming an integral part of the software development lifecycle, impacting everything from coding and testing to deployment and maintenance. This blog post explores the multifaceted ways AI is reshaping the way we build software, examining both the exciting opportunities and the potential challenges it presents.\n\n\n**Content:**\n\nWhile concrete research data isn't provided, we can still explore the significant impact AI is having on modern software development based on widely observed trends.  AI's influence manifests in several key areas:\n\n* **AI-Powered Code Generation:** Tools are emerging that can generate code snippets, even entire functions, based on natural language descriptions.  Imagine describing the functionality you need in plain English, and an AI assistant generating the corresponding code in your chosen language. This dramatically accelerates development, reducing time spent on repetitive tasks and allowing developers to focus on more complex problem-solving.  While these tools aren't perfect and require human oversight, their potential for boosting productivity is undeniable.\n\n* **Improved Code Quality and Security:** AI can analyze code for bugs, vulnerabilities, and style inconsistencies far more efficiently than a human reviewer.  Static and dynamic analysis powered by machine learning algorithms can identify potential problems early in the development process, leading to more robust and secure software.  This is crucial in today's security-conscious environment.\n\n* **Automated Testing and Debugging:**  AI is revolutionizing software testing by automating test case generation and execution.  Machine learning models can identify patterns in code and predict potential failure points, allowing developers to focus their testing efforts on the most critical areas.  Similarly, AI-powered debugging tools can assist in identifying and resolving errors more quickly and efficiently.\n\n* **Enhanced Collaboration and Communication:**  AI-powered tools can facilitate better communication and collaboration among development teams.  For example, AI chatbots can answer common questions, provide code documentation, and even assist with project management tasks, freeing up developers to concentrate on core development activities.\n\n* **Personalized Development Experiences:** AI can tailor the development environment to individual developer preferences and skill levels.  This could include intelligent code completion, personalized tutorials, and adaptive learning platforms that help developers improve their skills and efficiency.\n\n\n**Challenges:**\n\nDespite the many advantages, integrating AI into software development also presents challenges:\n\n* **Data Dependency:** AI models require large amounts of training data, which may not always be available or readily accessible.\n* **Bias and Fairness:** AI algorithms can inherit biases present in the training data, potentially leading to unfair or discriminatory outcomes in the software they generate.\n* **Explainability and Transparency:**  Understanding how complex AI models arrive at their decisions can be difficult, making it challenging to debug or troubleshoot errors.\n* **Job Displacement Concerns:**  While AI will likely augment rather than replace human developers, concerns about job displacement remain a valid area of discussion.\n\n\n**Summary:**\n\nAI is rapidly transforming modern software development, offering significant opportunities for increased productivity, improved code quality, and enhanced security.  AI-powered tools are automating repetitive tasks, improving collaboration, and personalizing the development experience. However, challenges related to data dependency, bias, explainability, and job displacement must be addressed to ensure responsible and ethical integration of AI into the software development lifecycle.  The future of software development is undoubtedly intertwined with AI, and navigating this evolving landscape requires a careful balance of embracing innovation and mitigating potential risks.\n"
}
```

## Contributing

Contributions are welcome! If you have suggestions for improvements or find any issues, please feel free to open an issue or submit a pull request to the GitHub repository: `git@github.com:sujayshah3011/Blog_generation.git`

## License

Consider adding a license file (e.g., MIT, Apache 2.0) to your project.
