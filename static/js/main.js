let editor;

require.config({ paths: { 'vs': 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs' }});
require(['vs/editor/editor.main'], function() {
    editor = monaco.editor.create(document.getElementById('monaco-editor'), {
        value: '# Converted Markdown will appear here',
        language: 'markdown',
        theme: document.body.classList.contains('dark-theme') ? 'vs-dark' : 'vs',
        readOnly: true,
        minimap: { enabled: false },
        scrollBeyondLastLine: false,
        fontSize: 14,
        wordWrap: 'on'
    });

    window.addEventListener('resize', () => {
        editor.layout();
    });
});

const convertBtn = document.getElementById('convertBtn');
const exportBtn = document.getElementById('exportBtn');

document.getElementById('convertBtn').addEventListener('click', async () => {
    const url = document.getElementById('urlInput').value;
    const selector = document.getElementById('selectorInput').value;

    if (!url) {
        alert('Please enter a URL');
        return;
    }

    try {
        convertBtn.disabled = true;
        convertBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Converting...';

        const response = await fetch('/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `url=${encodeURIComponent(url)}&selector=${encodeURIComponent(selector)}`
        });

        const data = await response.json();

        if (response.ok) {
            editor.setValue(data.markdown);
            exportBtn.disabled = false;
        } else {
            alert(data.error || 'Conversion failed');
            exportBtn.disabled = true;
        }
    } catch (error) {
        alert('An error occurred during conversion');
    } finally {
        convertBtn.disabled = false;

document.getElementById('exportBtn').addEventListener('click', async () => {
    const markdown = editor.getValue();
    
    if (!markdown || markdown === '# Converted Markdown will appear here') {
        alert('No content to export');
        return;
    }

    try {
        exportBtn.disabled = true;
        exportBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Exporting...';

        const form = document.createElement('form');
        form.method = 'POST';
        form.action = '/export';

        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'markdown';
        input.value = markdown;

        form.appendChild(input);
        document.body.appendChild(form);
        form.submit();
        document.body.removeChild(form);
    } catch (error) {
        alert('An error occurred during export');
    } finally {
        exportBtn.disabled = false;
        exportBtn.innerHTML = 'Export Markdown';
    }
});
        convertBtn.innerHTML = 'Convert';
    }
});
