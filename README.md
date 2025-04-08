# ChatBerry - An AI-Powered Chatbot

## Overview
ChatBerry is a stateful chatbot designed to provide engaging and meaningful conversations. Built using advanced natural language processing techniques, it leverages the power of AI to understand and respond to user inputs effectively. The project is hosted on Hugging Face Spaces and offers a seamless web-based interface for interaction. Whether you're looking to explore AI-driven conversational agents or integrate a chatbot into your application, ChatBerry serves as a robust starting point.

## Live
🔹 Live App: 


## Features
- **Authentication**: Secure and private user interactions.
- **Stateful Conversations**: Maintains context for natural chats.
- **AI-Powered**: Accurate and meaningful responses.
- **Customizable**: Adaptable to various use cases.
- **Web Interface**: User-friendly and accessible.
- **Docker Support**: Easy deployment with Docker.
- **Open Source**: Community-driven and extensible.


## Prerequisites

- Python 3.8 or higher
- UV Package Manager
- Docker (if using the provided Docker setup)


## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/syeda-hoorain-ali/chatberry
    ```

2. Navigate to the project directory:
    ```bash
    cd chatberry
    ```

3. Create and activate virtual environment:
    ```bash
    uv venv
    ./venv/Scripts/activate
    ```

4. Install the dependencies:
    ```bash
    uv pip install .
    ```

5. Copy the `.env.example` file to `.env` and update the environment variables as needed:
    ```bash
    cp .env.example .env
    ```

## Database Setup

1. Navigate to the `chainlit-datalayer` folder:
    ```bash
    cd chainlit-datalayer
    ```

2. Add the following environment variables in `.env`:
    ```bash
    # To link to the PostgreSQL instance.
    DATABASE_URL=postgresql://postgres:<db_password>@localhost:5432/<db_name>
    ```
    
3. Deploy the database migrations:
    ```bash
    npx prisma migrate deploy
    ```

## Usage

1. Run the chatbot script:
    ```bash
    chainlit run src/main.py -w
    ```
2. Interact with the chatbot through the web interface.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
Special thanks to the open-source community for providing tools and libraries that made this project possible.
