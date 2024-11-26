<script lang="ts">
    import { onMount } from 'svelte';
    import loader from '@monaco-editor/loader';
    import TurnDown from 'turndown';

    let urlInput: string = '';
    let selectorInput: string = '';
    let editor: any;
    let isDarkTheme = false;
    let isConverting = false;
    let canExport = false;

    onMount(async () => {
        // Initialize Monaco Editor
        loader.config({ paths: { vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs' } });
        const monaco = await loader.init();
        
        editor = monaco.editor.create(document.getElementById('monaco-editor'), {
            value: '# Converted Markdown will appear here',
            language: 'markdown',
            theme: isDarkTheme ? 'vs-dark' : 'vs',
            readOnly: false,
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            fontSize: 14,
            wordWrap: 'on'
        });

        // Handle window resize
        window.addEventListener('resize', () => editor?.layout());
        
        return () => {
            editor?.dispose();
        };
    });

    // Toggle theme function
    function toggleTheme() {
        isDarkTheme = !isDarkTheme;
        if (editor) {
            editor.updateOptions({ theme: isDarkTheme ? 'vs-dark' : 'vs' });
        }
        document.body.classList.toggle('dark');
    }

    // Convert HTML to Markdown
    async function convertToMarkdown() {
        if (!urlInput) {
            alert('Please enter a URL');
            return;
        }

        isConverting = true;
        try {
            const response = await fetch(urlInput);
            const html = await response.text();
            
            // Use TurnDown for conversion
            const turndownService = new TurnDown({
                headingStyle: 'atx',
                codeBlockStyle: 'fenced'
            });

            let content = html;
            if (selectorInput) {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const selected = doc.querySelector(selectorInput);
                content = selected ? selected.outerHTML : html;
            }

            const markdown = turndownService.turndown(content);
            editor.setValue(markdown);
            canExport = true;
        } catch (error) {
            alert('Error converting content: ' + error.message);
        } finally {
            isConverting = false;
        }
    }

    // Export Markdown
    function exportMarkdown() {
        const content = editor.getValue();
        if (!content || content === '# Converted Markdown will appear here') {
            alert('No content to export');
            return;
        }

        const blob = new Blob([content], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'converted.md';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
</script>

<div class="container mx-auto px-4 py-8">
    <nav class="flex items-center justify-between mb-8">
        <h1 class="text-2xl font-bold">HTML to Markdown Converter</h1>
        <button 
            on:click={toggleTheme}
            class="p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800"
        >
            {#if isDarkTheme}
                🌞
            {:else}
                🌙
            {/if}
        </button>
    </nav>

    <div class="space-y-4">
        <div class="flex gap-4">
            <input
                type="url"
                bind:value={urlInput}
                placeholder="Enter documentation URL"
                class="flex-1 p-2 border rounded-md dark:bg-gray-800 dark:border-gray-700"
            />
            <input
                type="text"
                bind:value={selectorInput}
                placeholder="CSS Selector (optional)"
                class="flex-1 p-2 border rounded-md dark:bg-gray-800 dark:border-gray-700"
            />
        </div>
        
        <div class="flex gap-4">
            <button
                on:click={convertToMarkdown}
                disabled={isConverting}
                class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:opacity-50"
            >
                {isConverting ? 'Converting...' : 'Convert'}
            </button>
            <button
                on:click={exportMarkdown}
                disabled={!canExport}
                class="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 disabled:opacity-50"
            >
                Export Markdown
            </button>
        </div>
    </div>

    <div class="mt-8 border rounded-lg overflow-hidden h-[600px]">
        <div id="monaco-editor" class="h-full w-full"></div>
    </div>
</div>

<style>
    :global(body.dark) {
        background-color: #1a1a1a;
        color: #ffffff;
    }

    :global(body.dark) input {
        color: #ffffff;
    }

    :global(.dark) button:not([class*="bg-"]) {
        background-color: #2d2d2d;
        color: #ffffff;
    }
</style>
