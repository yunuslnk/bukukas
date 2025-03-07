document.addEventListener('DOMContentLoaded', function () {
    const searchInputs = document.querySelectorAll('input[id^="search"]');
    const table = document.getElementById('asetTable');
    const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');

    searchInputs.forEach(input => {
        input.addEventListener('keyup', function () {
            const column = Array.from(searchInputs).indexOf(this);
            const filter = this.value.toLowerCase();

            for (let i = 0; i < rows.length; i++) {
                const cell = rows[i].getElementsByTagName('td')[column];
                if (cell) {
                    const text = cell.textContent || cell.innerText;
                    rows[i].style.display = text.toLowerCase().indexOf(filter) > -1 ? '' : 'none';
                }
            }
        });
    });
});