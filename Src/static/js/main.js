document.addEventListener("DOMContentLoaded", function () {
    const fontSelect = document.getElementById('font');
    const colorSelect = document.getElementById('color');

    if (fontSelect) {
        fontSelect.addEventListener('change', updateColorOptions);
    }

    function updateColorOptions() {
        const fontValue = fontSelect.value;
        const colorMap = {
            '1': ['Blue', 'Orange-1', 'Orange-2'],
            '2': ['Blue', 'Orange-1', 'Orange-2'],
            '3': ['Blue', 'Orange-1'],
            '4': ['Blue', 'Orange-1', 'Yellow'],
            '5': ['Orange-1']
        };

        const colors = colorMap[fontValue] || [];
        const colorOptions = colors.map(color => `<option value="${color}">${color}</option>`).join('');

        colorSelect.innerHTML = colorOptions;
    }

    const isHomePage = window.location.pathname === '/';
    const isResultPage = window.location.pathname === '/result';
    const isReload = performance.getEntriesByType("navigation")[0]?.type === "reload";

    if (isReload && !isHomePage && isResultPage) {
        window.location.href = "/";
    }
});
