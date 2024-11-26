import os
import logging
from flask import Flask, render_template, request, jsonify, send_file
from converter import convert_html_to_markdown
import trafilatura
from urllib.parse import urlparse
from io import BytesIO

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "dev_key_123"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        url = request.form.get('url')
        selector = request.form.get('selector', '')

        logger.info(f"Received conversion request for URL: {url} with selector: {selector}")

        if not url:
            logger.warning("No URL provided in request")
            return jsonify({'error': 'URL is required'}), 400

        # Validate URL
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            logger.warning(f"Invalid URL format: {url}")
            return jsonify({'error': 'Invalid URL format'}), 400

        # Add scheme if missing
        if not parsed_url.scheme:
            url = 'https://' + url
            logger.info(f"Added https scheme to URL: {url}")

        # Fetch webpage content with retries
        try:
            downloaded = trafilatura.fetch_url(url)
            if not downloaded:
                # Try alternative fetch method
                logger.warning(f"Failed to fetch URL with trafilatura: {url}")
                downloaded = trafilatura.fetch_url(url, decode=True)
                
            if not downloaded:
                logger.error(f"All attempts to fetch URL failed: {url}")
                return jsonify({'error': 'Failed to fetch webpage. Please check if the URL is accessible.'}), 400
                
        except Exception as fetch_error:
            logger.error(f"Error fetching URL {url}: {str(fetch_error)}")
            return jsonify({'error': f'Failed to fetch webpage: {str(fetch_error)}'}), 400

        # Convert HTML to Markdown
        try:
            markdown_content = convert_html_to_markdown(downloaded, selector)
            logger.info("Successfully converted HTML to Markdown")
            return jsonify({'markdown': markdown_content})
        except Exception as convert_error:
            logger.error(f"Error converting HTML to Markdown: {str(convert_error)}")
            return jsonify({'error': f'Error converting content: {str(convert_error)}'}), 500

    except Exception as e:
        logger.error(f"Unexpected error in convert route: {str(e)}")
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
