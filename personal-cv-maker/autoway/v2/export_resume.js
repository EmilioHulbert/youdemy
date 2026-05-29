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
        console.log("Applying precise element isolation and stripping watermarks...");

        // Define the exact resume selector targeting your canvas container
        const targetSelector = 'div[data-testid="embd-95CA90b"]';

        await page.evaluate((selector) => {
            // 1. Instantly clear text blurs safely
            const allElements = document.querySelectorAll('*');
            allElements.forEach(el => {
                const style = window.getComputedStyle(el);
                if (style.filter.includes('blur') || style.backdropFilter.includes('blur')) {
                    el.style.filter = 'none !important';
                    el.style.backdropFilter = 'none !important';
                }
            });

            // 2. Clear out the hidden watermark text layers completely
            const invisibleJunk = document.querySelectorAll('[data-testid*="743pAvFP"], [style*="transparent"]');
            invisibleJunk.forEach(el => {
                if (el.textContent.includes("Resume Wizard") || el.textContent.includes("Bootstrapping")) {
                    el.remove(); 
                }
            });

            // 3. Force the resume container itself to take up 100% true A4 proportions with zero bounds
            const resumeCanvas = document.querySelector(selector);
            if (resumeCanvas) {
                resumeCanvas.style.setProperty('width', '210mm', 'important');
                resumeCanvas.style.setProperty('margin', '0px', 'important');
                resumeCanvas.style.setProperty('padding', '0px', 'important');
                resumeCanvas.style.setProperty('box-shadow', 'none', 'important');
                resumeCanvas.style.setProperty('transform', 'none', 'important');
            }

            // 4. Inject structural print style overrides directly to the element scope
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
                        margin: 0mm !important; /* Total removal of outer margins */
                    }
                    body {
                        margin: 0mm !important;
                        padding: 0mm !important;
                        background: #ffffff !important;
                    }
                    /* Smooth pagination breaks for text selection */
                    li, p, tr, [class*="item"] {
                        page-break-inside: auto !important;
                        break-inside: auto !important;
                        overflow: visible !important;
                    }
                }
            `;
            document.head.appendChild(styleOverride);
        }, targetSelector);

        // Give the page layout context an extra moment to drop side paddings smoothly
        await new Promise(r => setTimeout(r, 2000));

        console.log("Executing strict Element-Level PDF rendering pipeline...");
        
        // CRITICAL FIX: We tell Puppeteer to run the PDF generator using our optimized configuration parameters
        await page.pdf({
            path: '/home/hulbert/Desktop/try/Emilio_Hulbert_Resume.pdf',
            format: 'A4',
            printBackground: true,
            preferCSSPageSize: true, // Forces obedience to our 0mm page CSS
            margin: { top: '0mm', right: '0mm', bottom: '0mm', left: '0mm' } // Strict binary clamp
        });

        console.log("✓ Success! Flawless, edge-to-edge PDF compiled at ~/Desktop/try/Emilio_Hulbert_Resume.pdf");
        await browser.disconnect();

    } catch (error) {
        console.error("✕ Error encountered during execution pipeline:", error);
    }
})();