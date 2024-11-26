import * as cheerio from 'cheerio';
import { JSDOM } from 'jsdom';
import { convert } from 'html-to-text';

export interface ConversionOptions {
  selector?: string;
  bodyWidth?: number;
  preserveLinks?: boolean;
  preserveImages?: boolean;
  preserveEmphasis?: boolean;
  preserveTables?: boolean;
}

export async function convertHtmlToMarkdown(
  htmlContent: string,
  options: ConversionOptions = {}
): Promise<string> {
  try {
    // Set default options
    const {
      selector,
      bodyWidth = 0,
      preserveLinks = true,
      preserveImages = true,
      preserveEmphasis = true,
      preserveTables = true
    } = options;

    // Configure conversion options
    const conversionOptions = {
      wordwrap: bodyWidth,
      selectors: [
        { selector: 'a', options: { ignoreHref: !preserveLinks } },
        { selector: 'img', options: { ignoreImage: !preserveImages } },
        { selector: 'table', options: { skipTables: !preserveTables } },
        { selector: 'em,strong,b,i', options: { ignoreEmphasis: !preserveEmphasis } }
      ]
    };

    let contentToConvert = htmlContent;

    if (selector) {
      // Use cheerio for CSS selector-based content extraction
      const $ = cheerio.load(htmlContent);
      const selectedContent = $(selector);
      
      if (selectedContent.length > 0) {
        contentToConvert = selectedContent.map((_, el) => $.html(el)).get().join('\n');
      } else {
        // Fallback to basic DOM extraction if selector doesn't match
        const dom = new JSDOM(htmlContent);
        const { document } = dom.window;
        contentToConvert = document.body.innerHTML;
      }
    }

    // Convert to markdown
    const markdown = convert(contentToConvert, conversionOptions);
    return markdown.trim();
  } catch (error) {
    throw new Error(`Conversion error: ${error.message}`);
  }
}
