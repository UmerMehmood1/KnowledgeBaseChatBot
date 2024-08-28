# LLM-Powered Chatbot with Django and FastAPI

This project integrates a FastAPI-based backend with a Django frontend to create a chatbot application. The backend uses Hugging Face Transformers and vector search to provide intelligent responses to user queries, while the Django frontend provides a simple UI for interaction.

## Features

- **FastAPI Backend**: Handles query processing and response generation.
- **Hugging Face Transformers**: Leverages pre-trained language models for generating responses.
- **DocArray Integration**: Performs vector search for document retrieval.
- **Django Frontend**: A simple web UI for user interaction.
- **CORS Support**: Enables cross-origin requests for seamless frontend-backend communication.

## Prerequisites

- Python 3.8 or higher
- Git (for version control)

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/UmerMehmood1/KnowledgeBaseChatBot.git
    cd KnowledgeBaseChatBot
    ```

2. **Create a virtual environment**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Migrate the Django database**:

    ```bash
    python manage.py migrate
    ```

5. **Run the Django development server**:

    ```bash
    python manage.py runserver
    ```

6. **Run the FastAPI server**:

    Open a new terminal window, activate the virtual environment, and run:

    ```bash
    uvicorn api.api:app --reload --host 127.0.0.2 --port 8080
    ```

    The FastAPI server should now be running at `http://127.0.0.2:8080`.

## Usage

1. Open your web browser and go to `http://127.0.0.1:8000` to access the Django frontend.
2. Type your query in the input box and click "Send."
3. The chatbot will process your query using the FastAPI backend and return a response.

## Demo

<p>Check out a <a href="https://github.com/UmerMehmood1/KnowledgeBaseChatBot/raw/main/demo/KnowledgeBaseChatBotVideo.mp4">video demonstration</a> of the chatbot in action.</p>
<video width="640" height="480" controls>
    <source src="https://github.com/UmerMehmood1/KnowledgeBaseChatBot/raw/main/demo/KnowledgeBaseChatBotVideo.mp4" type="video/mp4">
    Your browser does not support the video tag. You can download the video <a href="https://github.com/UmerMehmood1/KnowledgeBaseChatBot/raw/main/demo/KnowledgeBaseChatBotVideo.mp4">here</a>.
</video>
## Customization

- **Change Models**: To use a different language model, modify the `model_name` parameter in the `api.py` file.
- **Frontend Styling**: Customize the UI by editing `llm_app/templates/query_form.html` and updating the CSS.

## Troubleshooting

- **CORS Issues**: If you encounter CORS errors, ensure that the `allow_origins` in `api.py` is correctly configured to match your frontend's URL.
- **Model Loading Issues**: If models fail to load, ensure you have an active internet connection or the models are correctly downloaded.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please submit pull requests or open issues for any enhancements or bug fixes.

## Acknowledgments

- Hugging Face for providing pre-trained language models.
- Django and FastAPI communities for excellent web frameworks.
