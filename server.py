from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import io
from agents import CoordinatorAgent, InformationExtractorAgent, ResearcherAgent
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Initialize agents
coordinator = CoordinatorAgent(client)
extractor = InformationExtractorAgent(client)
researcher = ResearcherAgent(client)

# Store data in memory (in production, use a proper database)
data_store = {}

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read the uploaded file
        contents = file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Generate a session ID (in production, use a proper session management)
        session_id = str(hash(contents))
        
        # Store the dataframe
        data_store[session_id] = df
        
        return jsonify({
            'session_id': session_id,
            'message': 'File uploaded successfully',
            'preview': df.head().to_dict(),
            'columns': df.columns.tolist()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        if not data or 'question' not in data or 'session_id' not in data:
            return jsonify({'error': 'Missing question or session_id'}), 400
        
        question = data['question']
        session_id = data['session_id']
        
        if session_id not in data_store:
            return jsonify({'error': 'Session not found'}), 404
        
        df = data_store[session_id]
        
        # Prepare dataset information
        df_info = f"""
        Dataset Information:
        - Number of rows: {len(df)}
        - Number of columns: {len(df.columns)}
        - Column names: {', '.join(df.columns)}
        - First few rows:
        {df.head().to_string()}
        """

        # Step 1: Coordinator determines how to handle the question
        coordination_plan = coordinator.coordinate(question, df_info)
        
        # Step 2: Information Extractor gets the raw data and analysis
        extracted_info = extractor.extract_info(question, df)
        
        # Step 3: Researcher provides insights and context
        research_insights = researcher.research(question, extracted_info)
        
        # Step 4: Coordinator synthesizes the final response
        final_response = coordinator.coordinate(
            f"Original question: {question}\n\nExtracted information: {extracted_info}\n\nResearch insights: {research_insights}",
            df_info
        )

        return jsonify({
            'response': final_response,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True) 