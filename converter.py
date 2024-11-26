from bs4 import BeautifulSoup
import html2text
import trafilatura

def convert_html_to_markdown(html_content, selector=None):
    """
    Convert HTML content to Markdown format
    """
    try:
        # Initialize HTML to text converter
        converter = html2text.HTML2Text()
        converter.body_width = 0  # Disable line wrapping
        converter.ignore_links = False
        converter.ignore_images = False
        converter.ignore_emphasis = False
        converter.ignore_tables = False

        if selector:
            # Parse HTML and extract content based on selector
            soup = BeautifulSoup(html_content, 'html.parser')
            selected_content = soup.select(selector)
            if selected_content:
                html_content = ''.join(str(element) for element in selected_content)
            else:
                # If selector doesn't match, use trafilatura's extraction
                html_content = trafilatura.extract(html_content, include_tables=True, 
                                                 include_links=True, include_images=True,
                                                 output_format='html')

        # Convert to markdown
        markdown = converter.handle(html_content)
        return markdown.strip()
    except Exception as e:
        raise Exception(f"Conversion error: {str(e)}")
