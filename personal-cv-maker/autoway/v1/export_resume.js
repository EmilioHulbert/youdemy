const puppeteer = require('puppeteer');

(async () => {
    try {
        console.log("Connecting to your active Chrome profile session on port 9222...");
        
        const browser = await puppeteer.connect({
            browserURL: 'http://127.0.0.1:9222',
            defaultViewport: null
        });

        const pages = await browser.pages();
        const page = pages.find(p => p.url().includes('zety.com'));

        if (!page) {
            console.error("✕ Error: Could not find an active Zety builder tab.");
            await browser.disconnect();
            return;
        }

        console.log(`✓ Attached successfully to tab: "${await page.title()}"`);
        console.log("Applying structural cleanup and stripping invisible watermarks...");

        await page.evaluate(() => {
            // 1. Instantly clear text blurs safely across the viewport
            const allElements = document.querySelectorAll('*');
            allElements.forEach(el => {
                const style = window.getComputedStyle(el);
                if (style.filter.includes('blur') || style.backdropFilter.includes('blur')) {
                    el.style.filter = 'none !important';
                    el.style.backdropFilter = 'none !important';
                }
            });

            // 2. TARGET THE HIDDEN BOOTSTRAPPING TEXT: Obliterate the invisible overlay text strings
            const invisibleJunk = document.querySelectorAll('[data-testid*="743pAvFP"], [style*="transparent"]');
            invisibleJunk.forEach(el => {
                // Check if it's the annoying watermark text so we don't drop actual structural components
                if (el.textContent.includes("Resume Wizard") || el.textContent.includes("Bootstrapping")) {
                    el.remove(); 
                }
            });

            const targetSelector = 'div[data-testid="embd-95CA90b"]';

            // 3. Inject an optimized style block allowing text columns to split naturally without gaps
            const styleOverride = document.createElement('style');
            styleOverride.type = 'text/css';
            styleOverride.innerHTML = `
                *, .doc-overlay, .para-overlay, [class*="blur"], [class*="overlay"] {
                    filter: none !important;
                    backdrop-filter: none !important;
                    opacity: 1 !important;
                }

                @media print {
                    @page {
                        size: A4 portrait;
                        margin: 0mm !important;
                    }

                    /* Allow wrappers to flow continuously without clamping heights or forcing massive gaps */
                    html, body, #app, main, .main-content, [class*="workspace"], .preview-container {
                        visibility: visible !important;
                        display: block !important;
                        background: #ffffff !important;
                        box-shadow: none !important;
                        margin: 0px !important;
                        padding: 0px !important;
                        width: 210mm !important;
                        height: auto !important;
                        overflow: visible !important;
                    }

                    /* Hide explicit interface panels and editing tool buttons */
                    div.tab-panel, 
                    div[data-testid="embd-70WfaMp"],
                    .finalize-action-right, 
                    #scrollPanelBody,
                    div[data-testid="embd-67ScGvd"],
                    .panel-header,
                    div[data-testid="embd-69R5sVn4"],
                    .cv-score-wrapperV2, 
                    nav, 
                    .left-navbar, 
                    ul.finalize-btn-wrap, 
                    footer, 
                    #footer, 
                    .footer, 
                    nav[data-testid="embd-63ZeVMJ"],
                    div[data-testid="embd-32TRaeqb"],
                    div[data-testid="embd-70AbE0Gv"],
                    .social-proof-banner,
                    .skip-content-link,
                    #editIcons, 
                    .document-tool, 
                    .sec-tool, 
                    .para-tool,
                    [class*="button-wrapper"],
                    [class*="sidebar"] {
                        display: none !important;
                        visibility: hidden !important;
                        opacity: 0 !important;
                        height: 0px !important;
                        width: 0px !important;
                    }

                    /* Align layout root sharply against canvas boundary edges */
                    ${targetSelector} {
                        visibility: visible !important;
                        display: block !important;
                        position: relative !important;
                        left: 0mm !important;
                        top: 0mm !important;
                        width: 210mm !important;
                        height: auto !important;
                        margin: 0mm auto !important;
                        box-sizing: border-box !important;
                        transform: none !important;
                        background-color: #ffffff !important;
                        -webkit-print-color-adjust: exact !important;
                        print-color-adjust: exact !important;
                    }

                    /* Force text elements to split lines across page boundaries beautifully */
                    li, p, tr, [class*="item"] {
                        page-break-inside: auto !important;
                        break-inside: auto !important;
                        overflow: visible !important;
                    }

                    /* Prevent headings from being separated from their content */
                    h1, h2, h3, .section-title {
                        page-break-after: avoid !important;
                        break-after: avoid !important;
                    }
                }
            `;
            document.head.appendChild(styleOverride);
            console.log("✓ Dynamic spacing adjustments and bootstrap patches applied.");
        });

        // Small buffer delay to allow the layout layout context to settle down smoothly
        await new Promise(r => setTimeout(r, 1500));

        console.log("Compiling final selectable text PDF asset...");
        
        await page.pdf({
            path: '/home/hulbert/Desktop/try/Emilio_Hulbert_Resume.pdf',
            format: 'A4',
            printBackground: true,
            preferCSSPageSize: true
        });

        console.log("✓ Done! Check your updated PDF at ~/Desktop/try/Emilio_Hulbert_Resume.pdf");
        await browser.disconnect();

    } catch (error) {
        console.error("✕ Error encountered during execution pipeline:", error);
    }
})();