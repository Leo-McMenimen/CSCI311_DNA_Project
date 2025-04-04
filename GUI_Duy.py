
"""
Flask-based 
"""
from flask import Flask, render_template, request
import os
import tempfile
import file_handler
from algorithm import ALGORITHMS

app = Flask(__name__)

# Create a templates directory if it doesn't exist
os.makedirs('templates', exist_ok=True)

# Create the HTML template
with open('templates/index.html', 'w') as f:
    f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>DNA Seq</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .container {
            background-color: #f5f5f5;
            border-radius: 5px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #333;
            border-bottom: 1px solid #ddd;
            padding-bottom: 10px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        select, button {
            padding: 8px;
            border-radius: 4px;
            border: 1px solid #ddd;
        }
        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
            padding: 10px 15px;
        }
        button:hover {
            background-color: #45a049;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background-color: #e9f7ef;
            border-radius: 5px;
        }
        .flash-messages {
            padding: 10px;
            margin-bottom: 15px;
            border-radius: 4px;
        }
        .flash-error {
            background-color: #ffebee;
            color: #c62828;
        }
        .flash-success {
            background-color: #e8f5e9;
            color: #2e7d32;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>DNA Seq</h1>
        
        {% if messages %}
            <div class="flash-messages">
                {% for message in messages %}
                    <div class="flash-{{ message.category }}">{{ message }}</div>
                {% endfor %}
            </div>
        {% endif %}
        
        <form method="POST" enctype="multipart/form-data">
            <div class="form-group">
                <label for="database_file">DNA Sequence File:</label>
                <input type="file" id="database_file" name="database_file" accept=".txt,.fasta">
            </div>
            
            <div class="form-group">
                <label for="query_file">DNA Query File:</label>
                <input type="file" id="query_file" name="query_file" accept=".txt,.fasta">
            </div>
            
            <div class="form-group">
                <label for="algorithm">Select Algorithm:</label>
                <select id="algorithm" name="algorithm">
                    {% for algorithm in algorithms %}
                        <option value="{{ algorithm }}">{{ algorithm }}</option>
                    {% endfor %}
                </select>
            </div>
            
            <button type="submit">Run Analysis</button>
        </form>
        
        {% if result %}
            <div class="result">
                <h2>Analysis Results</h2>
                <p><strong>Best Match:</strong> {{ result.header }}</p>
                <p><strong>Sequence:</strong> {{ result.sequence_preview }}...</p>
            </div>
        {% endif %}
    </div>
</body>
</html>
''')

@app.route('/', methods=['GET', 'POST'])
def index():
    """Main page handler"""
    
    # Set up context with algorithm names
    context = {
        'algorithms': list(ALGORITHMS.keys()),
        'messages': [],
        'result': None
    }
    
    # Handle form submission
    if request.method == 'POST':
        # Check if files were provided
        if 'database_file' not in request.files or 'query_file' not in request.files:
            context['messages'].append({
                'text': 'Both database and query files are required',
                'category': 'error'
            })
            return render_template('index.html', **context)
        
        database_file = request.files['database_file']
        query_file = request.files['query_file']
        
        # Check if files are selected
        if database_file.filename == '' or query_file.filename == '':
            context['messages'].append({
                'text': 'Please select both database and query files',
                'category': 'error'
            })
            return render_template('index.html', **context)
        
        # Save uploaded files to temporary files
        db_temp = tempfile.NamedTemporaryFile(delete=False)
        query_temp = tempfile.NamedTemporaryFile(delete=False)
        
        try:
            # Save the files
            database_file.save(db_temp.name)
            query_file.save(query_temp.name)
            
            # Load the sequences
            database_sequences = file_handler.load_fasta(db_temp.name)
            query_sequences = file_handler.load_fasta(query_temp.name)
            
            if not database_sequences:
                raise ValueError("No sequences found in the database file")
                
            if not query_sequences:
                raise ValueError("No sequences found in the query file")
                
            # Get the query sequence (first sequence in file)
            query_sequence = query_sequences[0][1]
            
            # Get selected algorithm
            algorithm_name = request.form.get('algorithm')
            if algorithm_name not in ALGORITHMS:
                raise ValueError(f"Unknown algorithm: {algorithm_name}")
                
            algorithm_function = ALGORITHMS[algorithm_name]
            
            # Run the selected algorithm
            best_match = algorithm_function(query_sequence, database_sequences)
            
            # Prepare result for display
            sequence_preview = best_match[1][:50] if len(best_match[1]) > 50 else best_match[1]
            
            context['result'] = {
                'header': best_match[0],
                'sequence_preview': sequence_preview
            }
            
            context['messages'].append({
                'text': f'Analysis complete using {algorithm_name}',
                'category': 'success'
            })
            
        except Exception as e:
            context['messages'].append({
                'text': f'Error: {str(e)}',
                'category': 'error'
            })
        finally:
            # Clean up temporary files
            os.unlink(db_temp.name)
            os.unlink(query_temp.name)
    
    return render_template('index.html', **context)

if __name__ == '__main__':
    print("Starting DNA Sequence")
    print("http://127.0.0.1:3000")
    app.run(debug=True, port=3000) 
