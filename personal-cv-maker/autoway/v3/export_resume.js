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
        console.log("Stripping structural frame borders and box reflections...");

        const targetSelector = 'div[data-testid="embd-95CA90b"]';

        await page.evaluate((selector) => {
            // 1. Instantly clear workspace text blurs
            const allElements = document.querySelectorAll('*');
            allElements.forEach(el => {
                const style = window.getComputedStyle(el);
                if (style.filter.includes('blur') || style.backdropFilter.includes('blur')) {
                    el.style.filter = 'none !important';
                    el.style.backdropFilter = 'none !important';
                }
            });

            // 2. Clear out the hidden metadata watermark layers completely
            const invisibleJunk = document.querySelectorAll('[data-testid*="743pAvFP"], [style*="transparent"]');
            invisibleJunk.forEach(el => {
                if (el.textContent.includes("Resume Wizard") || el.textContent.includes("Bootstrapping")) {
                    el.remove(); 
                }
            });

            // 3. TARGET THE ENCLOSING BOX: Strip borders, lines, and shadows directly off the canvas
            const resumeCanvas = document.querySelector(selector);
            if (resumeCanvas) {
                resumeCanvas.style.setProperty('width', '210mm', 'important');
                resumeCanvas.style.setProperty('margin', '0px', 'important');
                resumeCanvas.style.setProperty('padding', '0px', 'important');
                resumeCanvas.style.setProperty('border', 'none', 'important'); // Slashes the enclosing left border line
                resumeCanvas.style.setProperty('outline', 'none', 'important'); // Slashes any focus outlines
                resumeCanvas.style.setProperty('box-shadow', 'none', 'important'); // Removes wrapper depth reflection
                resumeCanvas.style.setProperty('transform', 'none', 'important');
            }

            // 4. Inject global overrides to force ancestral sheets to strip boundaries entirely
            const styleOverride = document.createElement('style');
            styleOverride.type = 'text/css';
            styleOverride.innerHTML = `
                /* Strip any custom premium element blurs universally */
                *, .doc-overlay, .para-overlay, [class*="blur"], [class*="overlay"] {
                    filter: none !important;
                    backdrop-filter: none !important;
                    opacity: 1 !important;
                }

                @media print {
                    @page {
                        size: A4 portrait;
                        margin: 0mm !important; /* Zero out native printer canvas bleed */
                    }
                    
                    /* Strip borders, lines, and shading from every single structural parent container */
                    html, body, #app, main, .main-content, [class*="workspace"], .preview-container, [class*="document-active"] {
                        visibility: visible !important;
                        display: block !important;
                        background: #ffffff !important;
                        box-shadow: none !important;
                        border: none !important;
                        outline: none !important;
                        margin: 0px !important;
                        padding: 0px !important;
                        width: 100vw !important;
                        height: auto !important;
                        overflow: visible !important;
                    }

                    /* Clear UI panels completely */
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
                        margin: 0px !important;
                        padding: 0px !important;
                        border: none !important;
                    }

                    /* Pin the pristine resume element perfectly flush to coordinate 0,0 */
                    ${selector} {
                        visibility: visible !important;
                        display: block !important;
                        position: absolute !important;
                        left: 0mm !important;
                        top: 0mm !important;
                        width: 210mm !important;
                        height: auto !important;
                        margin: 0mm auto !important;
                        padding: 0mm !important;
                        border: none !important; /* Enforces clean non-bordered edge */
                        outline: none !important;
                        box-shadow: none !important;
                        transform: scale(1) !important;
                        background-color: #ffffff !important;
                        -webkit-print-color-adjust: exact !important;
                        print-color-adjust: exact !important;
                    }

                    /* Keep text list bullets breaking across margins naturally */
                    li, p, tr, [class*="item"] {
                        page-break-inside: auto !important;
                        break-inside: auto !important;
                        overflow: visible !important;
                    }

                    h1, h2, h3, .section-title {
                        page-break-after: avoid !important;
                        break-after: avoid !important;
                    }
                }
            `;
            document.head.appendChild(styleOverride);
        }, targetSelector);

        // Small pause for the style tree parameters to settle smoothly
        await new Promise(r => setTimeout(r, 2000));

        console.log("Compiling final, borderless vector text PDF...");
        
        await page.pdf({
            path: '/home/hulbert/Desktop/try/Emilio_Hulbert_Resume.pdf',
            format: 'A4',
            printBackground: true,
            preferCSSPageSize: true,
            margin: { top: '0mm', right: '0mm', bottom: '0mm', left: '0mm' }
        });

        console.log("✓ Success! Crisp borderless PDF generated at ~/Desktop/try/Emilio_Hulbert_Resume.pdf");
        await browser.disconnect();

    } catch (error) {
        console.error("✕ Error encountered during execution pipeline:", error);
    }
})();