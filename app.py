import os
import logging
import time
import requests
from flask import Flask, render_template, request, jsonify, send_file
from converter import convert_html_to_markdown
import trafilatura
from urllib.parse import urlparse
from io import BytesIO

# Define common headers for requests
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'DNT': '1',
}

# Configure trafilatura settings
import trafilatura.settings
config = trafilatura.settings.use_config()
config.set('DEFAULT', 'USER_AGENT', DEFAULT_HEADERS['User-Agent'])

# Rate limiting settings
RATE_LIMIT_DELAY = 1  # seconds between requests
last_request_time = 0

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

        # Implement rate limiting
        global last_request_time
        current_time = time.time()
        if current_time - last_request_time < RATE_LIMIT_DELAY:
            time.sleep(RATE_LIMIT_DELAY - (current_time - last_request_time))
        last_request_time = time.time()

        # First attempt: Try with trafilatura and custom headers
        try:
            downloaded = trafilatura.fetch_url(url)
            
            if not downloaded:
                logger.warning(f"Failed to fetch URL with trafilatura: {url}")
                
                # Second attempt: Try with requests library
                try:
                    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=10)
                    response.raise_for_status()
                    downloaded = response.text
                    logger.info("Successfully fetched URL using requests library")
                    
                except requests.exceptions.HTTPError as http_err:
                    status_code = http_err.response.status_code
                    if status_code in (401, 403):
                        error_msg = "Access denied. The website might be blocking automated access."
                    elif status_code == 429:
                        error_msg = "Rate limit exceeded. Please try again later."
                    else:
                        error_msg = f"HTTP error occurred: {status_code}"
                    logger.error(f"HTTP error for URL {url}: {error_msg}")
                    return jsonify({'error': error_msg}), status_code
                    
                except requests.exceptions.ConnectionError:
                    error_msg = "Failed to connect to the website. Please check if the URL is correct and the website is accessible."
                    logger.error(f"Connection error for URL {url}")
                    return jsonify({'error': error_msg}), 400
                    
                except requests.exceptions.Timeout:
                    error_msg = "Request timed out. The website might be slow or unavailable."
                    logger.error(f"Timeout error for URL {url}")
                    return jsonify({'error': error_msg}), 408
                    
                except requests.exceptions.RequestException as e:
                    error_msg = f"An error occurred while fetching the webpage: {str(e)}"
                    logger.error(f"Request error for URL {url}: {str(e)}")
                    return jsonify({'error': error_msg}), 400
            
            if not downloaded:
                error_msg = "Failed to extract content from the webpage. The website might be using JavaScript or blocking content extraction."
                logger.error(f"Content extraction failed for URL {url}")
                return jsonify({'error': error_msg}), 400
                
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
