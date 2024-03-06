from flask import Flask, send_file
from waitress import serve
import parameterized_register

app = Flask(__name__)

@app.route('/get_file_contents/<filename>')
def get_file_contents(filename):
    try:
        filepath = f'./{filename}'
        with open(filepath, 'r') as file:
            file_contents = file.read()
        return file_contents
    except Exception as e:
        return f"Error: {str(e)}"
    
@app.route('/download/<filename>')
def download_file(filename):
    try:
        filepath = f'./{filename}'
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    #create_file_script.create_sample_file()
    #app.run(debug=True)
    parameterized_register.create_estate_file()
    from waitress import serve
    serve(app, host='127.0.0.1', port='8888')