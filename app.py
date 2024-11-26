import os
from flask import Flask, render_template, request, jsonify, send_file
from converter import convert_html_to_markdown
import trafilatura
from urllib.parse import urlparse
from io import BytesIO

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "dev_key_123"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        url = request.form.get('url')
        selector = request.form.get('selector')

        if not url:
            return jsonify({'error': 'URL is required'}), 400

        # Validate URL
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            return jsonify({'error': 'Invalid URL format'}), 400

        # Fetch webpage content
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            return jsonify({'error': 'Failed to fetch webpage'}), 400

        # Convert HTML to Markdown
        markdown_content = convert_html_to_markdown(downloaded, selector)
        return jsonify({'markdown': markdown_content})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/export', methods=['POST'])
def export():
    try:
        markdown_content = request.form.get('markdown')
        if not markdown_content:
            return jsonify({'error': 'No content to export'}), 400

        # Create BytesIO object with markdown content
        buffer = BytesIO()
        buffer.write(markdown_content.encode('utf-8'))
        buffer.seek(0)

        return send_file(
            buffer,
            mimetype='text/markdown',
            as_attachment=True,
            download_name='converted.md'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500
