import os
from flask import Flask, render_template, request, jsonify
from converter import convert_html_to_markdown
import trafilatura
from urllib.parse import urlparse

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
