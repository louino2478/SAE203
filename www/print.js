/* ouvre une fenêtre pop-up pour imprimer la page */
document.addEventListener('DOMContentLoaded', () => {
    const printBtn = document.getElementById('printBtn');
    const printableDiv = document.getElementById('print');

    if (!printBtn || !printableDiv) return;
    
    printBtn.addEventListener('click', () => {
        // Ouvrir la nouvelle fenêtre
        const win = window.open('', 'Impression', 'width=1100,height=800');
        // Injecter le HTML + CSS
        win.document.write(`
            <html>
                <head>
                    <title>SAE203</title>
                    <link rel="stylesheet" href="style.css">
                    <script>
                        window.addEventListener('load', function () {
                            /* le CSS est maintenant appliqué */
                            window.focus();
                            window.print();
                        });
                        window.addEventListener('afterprint', function () {
                            window.close();
                        });
                    <\/script>
                </head>
                <body>
                    ${printableDiv.innerHTML}
                </body>
            </html>
        `);
        win.document.close();
    });
});
