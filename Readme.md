
# Chat-Based Order Management System

Welcome to the Chat-Based Order Management System! This system allows users to interactively manage orders through a chat interface powered by FastAPI and ChatterBot. Users can place orders, track orders, add items to existing orders, and remove orders using natural language commands.

## Features

- **Chat Interface**: Communicate with the system using natural language commands.
- **Order Management**: Place, track, add items to, and remove orders seamlessly.
- **Menu Integration**: Browse the menu and select items to order.
- **Customer Information**: Provide customer details to complete orders.
- **MongoDB Backend**: Efficiently store and retrieve order and menu data.
- **Stanford NER**: Extract named entities like person names and addresses from user input.
- **Spacy NLP**: Perform natural language processing tasks for order extraction.

## Setup Instructions

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/Michael-Lyon/chat-order-management.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the FastAPI server:

   ```bash
   uvicorn main:app --reload
   ```

4. Access the API documentation at `http://localhost:8000/docs` to interact with the system.

## Usage

- Use the chat endpoint (`/chat`) to interact with the system using natural language commands.
<!-- - Explore the `/menu` endpoint to view available menu items.
- Utilize the `/orders` endpoint to manage orders. -->

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature/your-feature`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- This project utilizes the [ChatterBot](https://github.com/gunthercox/ChatterBot) library for conversational interactions.
- Menu data is populated using initial data provided by the user.
- The system leverages MongoDB for efficient storage and retrieval of order and menu data.

