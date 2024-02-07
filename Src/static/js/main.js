document.addEventListener("DOMContentLoaded", function () {
    const fontSelect = document.getElementById('font');
    const colorSelect = document.getElementById('color');

    if (fontSelect) {
        fontSelect.addEventListener('change', function () {
            updateColorOptions(fontSelect.value);
        });
    }

    function updateColorOptions(fontValue) {
        let colorOptions = '';

        switch (fontValue) {
            case '1':
            case '2':
                colorOptions = `
                    <option value="Blue">Blue</option>
                    <option value="Orange-1">Orange 1</option>
                    <option value="Orange-2">Orange 2</option>`;
                break;

            case '3':
                colorOptions = `
                    <option value="Blue">Blue</option>
                    <option value="Orange-1">Orange 1</option>`;
                break;

            case '4':
                colorOptions = `
                    <option value="Blue">Blue</option>
                    <option value="Orange-1">Orange 1</option>
                    <option value="Yellow">Yellow</option>`;
                break;

            case '5':
                colorOptions = `<option value="Orange-1">Orange 1</option>`;
                break;

            default:
                return;
        }

        colorSelect.innerHTML = colorOptions;
    }

    const isHomePage = window.location.pathname === '/';
    if (performance.getEntriesByType("navigation")[0].type === "reload" && !isHomePage) {
        window.location.href = "/";
    }
});
