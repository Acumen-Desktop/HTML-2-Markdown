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

document.getElementById('convertBtn').addEventListener('click', async () => {
    const url = document.getElementById('urlInput').value;
    const selector = document.getElementById('selectorInput').value;
    const convertBtn = document.getElementById('convertBtn');

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
        } else {
            alert(data.error || 'Conversion failed');
        }
    } catch (error) {
        alert('An error occurred during conversion');
    } finally {
        convertBtn.disabled = false;
        convertBtn.innerHTML = 'Convert';
    }
});
