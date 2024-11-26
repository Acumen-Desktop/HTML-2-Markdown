# HTML to Markdown Converter

A versatile HTML to Markdown converter application available in both web and desktop versions. This tool helps you easily convert HTML content to Markdown format with real-time preview functionality. It supports direct URL input, CSS selector targeting, and provides both online (Flask) and offline (Electron) implementations.

[![GitHub](https://img.shields.io/github/license/Acumen-Desktop/HTML-2-Markdown)](https://github.com/Acumen-Desktop/HTML-2-Markdown/blob/main/LICENSE)
[![Electron](https://img.shields.io/badge/Electron-20.x-blue.svg)](https://www.electronjs.org/)

## Features

- **Dual Implementation**:
  - Web-based version using Flask
  - Desktop application using Electron
- **Real-time Preview**: Live preview of converted markdown content
- **Monaco Editor Integration**: Professional code editing experience
- **Theme Support**: Light and dark theme options
- **URL Processing**: Direct URL input support
- **CSS Selector Support**: Target specific content using CSS selectors
- **Export Functionality**: Save converted content as .md files

## Web Version (Flask)

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python main.py
```

The web application will be available at `http://localhost:5000`

### Features
- Clean, responsive interface
- Real-time conversion
- Theme toggle support
- Direct URL input
- CSS selector customization
- Export to Markdown file

## Desktop Version (Electron)

### Setup

1. Install dependencies:
```bash
cd electron-markdown-converter
npm install
```

2. Run the application:
```bash
npm run dev
```

### Features
- Native desktop experience
- Cross-platform support (Windows, macOS, Linux)
- Offline functionality
- System-native window controls
- Integrated development tools

## Usage

1. Enter a URL in the input field
2. (Optional) Specify a CSS selector to target specific content
3. Click "Convert" to process the HTML
4. Preview the converted Markdown in the editor
5. Use the "Export" button to save as a .md file

### Example CSS Selectors
- Main content: `#main-content`
- Article body: `.article-body`
- Documentation: `#docs-content > div.text.content`

## Technologies Used

### Web Version
- Flask (Python web framework)
- Beautiful Soup 4 (HTML parsing)
- html2text (HTML to Markdown conversion)
- Trafilatura (content extraction)
- Monaco Editor (code editing)

### Desktop Version
- Electron (desktop application framework)
- SvelteKit (UI framework)
- TypeScript
- Tailwind CSS
- Monaco Editor
- html-to-text (HTML to Markdown conversion)

## Development

The project uses modern web technologies and follows best practices for both web and desktop development:

- Modular architecture
- Real-time preview
- Error handling
### Configuration

#### Web Version
- Default port: 5000
- Rate limiting: 1 request per second
- Supported formats: HTML, URLs
- Export format: Markdown (.md)

#### Desktop Version
- Cross-platform support (Windows, macOS, Linux)
- No rate limiting for local conversions
- Offline-first architecture
- System-native window controls
- Rate limiting for web scraping
- Responsive design
- Theme support

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Monaco Editor for the powerful editing capabilities
- Electron for enabling cross-platform desktop development
- Flask for the lightweight web framework
- All contributors and maintainers
