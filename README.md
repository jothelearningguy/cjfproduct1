# CSV Chatbot

A powerful chatbot application that allows users to upload CSV files and ask questions about the data using AI-powered agents.

## Features

- Upload and analyze CSV files
- Ask questions about your data in natural language
- AI-powered data analysis and insights
- Real-time responses
- Clean and intuitive user interface

## Tech Stack

- Frontend: Streamlit
- Backend: Flask
- AI: DeepSeek AI
- Data Processing: Pandas

## Setup

1. Clone the repository:
```bash
git clone https://github.com/jothelearningguy/cjfproduct1.git
cd cjfproduct1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your DeepSeek API key:
```
DEEPSEEK_API_KEY=your_api_key_here
```

4. Start the Flask server:
```bash
python server.py
```

5. In a new terminal, start the Streamlit frontend:
```bash
streamlit run app.py
```

## Usage

1. Open your browser and navigate to `http://localhost:8501`
2. Upload a CSV file using the file uploader
3. Ask questions about your data in the chat interface
4. Get instant AI-powered insights and analysis

## Project Structure

- `app.py`: Streamlit frontend application
- `server.py`: Flask backend server
- `agents.py`: AI agent implementations
- `requirements.txt`: Project dependencies
- `.env`: Environment variables (not tracked in git)

## License

MIT License

## Example Questions

- "What are the column names in this dataset?"
- "Show me the summary statistics for the numeric columns"
- "What is the average value of [column_name]?"
- "How many rows are in this dataset?"
- "What are the unique values in [column_name]?"

## Note

Make sure you have a valid DeepSeek API key to use this application. The application uses DeepSeek's chat model to process and answer questions about your data. 