import os
import json
import logging
from flask import Flask, request, jsonify
import pandas as pd
import io
from agents import CSVAgent
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize data store
data_store = {}

try:
    # Get API key from environment variable
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        raise Exception("OpenRouter API key not found in environment variables")
        
    # Initialize the CSV agent
    csv_agent = CSVAgent(api_key)
    logger.info("Successfully validated OpenRouter API key")
    
except Exception as e:
    logger.error(f"Failed to initialize OpenRouter client: {str(e)}")
    csv_agent = None
    logger.warning("Running in fallback mode without AI capabilities")

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        logger.info("Received file upload request")
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
            
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'File must be a CSV'}), 400
            
        logger.info(f"Processing file: {file.filename}")
        
        # Read the file content
        content = file.read()
        if not content:
            return jsonify({'error': 'File is empty'}), 400
            
        # Try different encodings and delimiters
        encodings = ['utf-8', 'latin1', 'cp1252']
        delimiters = [',', ';', '\t']
        
        for encoding in encodings:
            try:
                logger.info(f"Trying to read file with {encoding} encoding")
                content_str = content.decode(encoding)
                
                for delimiter in delimiters:
                    try:
                        logger.info(f"Trying delimiter: {delimiter}")
                        df = pd.read_csv(io.StringIO(content_str), delimiter=delimiter)
                        if not df.empty and len(df.columns) > 0:
                            logger.info(f"Successfully read file with {encoding} encoding and {delimiter} delimiter")
                            
                            # Generate a unique session ID
                            session_id = hash(file.filename + str(pd.Timestamp.now()))
                            data_store[session_id] = df
                            
                            logger.info(f"File uploaded successfully. Session ID: {session_id}")
                            return jsonify({
                                'message': 'File uploaded successfully',
                                'session_id': session_id
                            })
                    except Exception as e:
                        logger.info(f"Failed with delimiter {delimiter}: {str(e)}")
                        continue
                        
            except UnicodeDecodeError:
                continue
                
        logger.error("Failed to read CSV with any encoding or delimiter")
        return jsonify({'error': 'Could not read CSV file. Please ensure it is a valid CSV file.'}), 400
        
    except Exception as e:
        logger.error(f"Error in file upload: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        question = data.get('question', '')
        session_id = data.get('session_id')
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
            
        if not session_id or session_id not in data_store:
            return jsonify({'error': 'No file uploaded or invalid session'}), 400
            
        df = data_store[session_id]
        logger.info(f"Processing question: {question}")
        logger.info(f"Session ID: {session_id}")
        
        # Process the question using the single-call agent
        response = csv_agent.process_question(question, df)
        return jsonify({'response': response})
        
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True) 