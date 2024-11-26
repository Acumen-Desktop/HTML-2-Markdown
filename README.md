# HTML to Markdown Converter

A versatile HTML to Markdown converter application with both web (Flask) and desktop (Electron) implementations. This tool helps you easily convert HTML content to Markdown format with real-time preview functionality, supporting direct URL input and CSS selector targeting.

[![GitHub](https://img.shields.io/github/license/Acumen-Desktop/HTML-2-Markdown)](https://github.com/Acumen-Desktop/HTML-2-Markdown/blob/main/LICENSE)
[![Flask](https://img.shields.io/badge/Flask-3.1.x-green.svg)](https://flask.palletsprojects.com/)
[![Electron](https://img.shields.io/badge/Electron-33.x-blue.svg)](https://www.electronjs.org/)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)

## Features

- HTML to Markdown conversion with real-time preview
- Direct URL input support
- CSS selector targeting for specific content extraction
- Monaco Editor integration with syntax highlighting
- Theme switching (Light/Dark mode)
- Export functionality to .md files
- Cross-platform support (Web & Desktop)
- Responsive design
- Rate limiting for web scraping

## Quick Start

### Web Version (Flask)
```bash
# Clone the repository
git clone https://github.com/Acumen-Desktop/HTML-2-Markdown.git
cd HTML-2-Markdown

# Install Python dependencies
pip install -r requirements.txt

# Run the Flask server
python main.py
```
The web application will be available at `http://localhost:5000`

### Desktop Version (Electron)
```bash
# Clone the repository
git clone https://github.com/Acumen-Desktop/HTML-2-Markdown.git
cd HTML-2-Markdown/electron-markdown-converter

# Install dependencies
npm install   # or pnpm install

# Start the application
npm run dev   # or pnpm dev
```

## Configuration

### Web Version
- Default port: 5000
- Rate limiting: 1 request per second
- Supported formats: HTML, URLs
- Export format: Markdown (.md)

### Desktop Version
- Cross-platform support (Windows, macOS, Linux)
- No rate limiting for local conversions
- Offline-first architecture
- System-native window controls

## Development

### Prerequisites
- Python 3.11+
- Node.js 20+
- npm or pnpm

### Project Structure
```
├── app.py              # Flask application core
├── converter.py        # HTML to Markdown conversion logic
├── static/            # Static assets (CSS, JS)
├── templates/         # HTML templates
└── electron-markdown-converter/
    ├── src/           # Electron application source
    ├── static/        # Electron static assets
    └── vite/          # Vite configuration
```

### Building

#### Web Version
The Flask version runs directly from source and doesn't require building.

#### Desktop Version
```bash
# Package the application
npm run package

# Create distributables
npm run make
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
