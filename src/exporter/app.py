
from flask import Flask, Response

app = Flask(__name__)

@app.route('/metrics')
def serve_prices():
    METRICS_FILE_PATH = '../../prices.txt'
    
    with open(METRICS_FILE_PATH, 'r') as file:
        file_content = file.read()
        
    prometheus_output = format_for_prometheus(file_content)

    return Response(prometheus_output, mimetype='text/plain')

def format_for_prometheus(content):
    lines = content.strip().split('\n')

    return "\n".join(lines)


if __name__ == '__main__':
    app.run()
