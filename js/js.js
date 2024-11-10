function sortByYear() {
    const table = document.getElementById('result_table');
    const rows = Array.from(table.querySelectorAll('tbody tr'));

    rows.sort((rowA, rowB) => {
        const yearA = parseInt(rowA.cells[0].textContent);
        const yearB = parseInt(rowB.cells[0].textContent);
        return yearA - yearB;
    });

    // Append sorted rows back to the table
    rows.forEach(row => table.querySelector('tbody').appendChild(row));
}

function sortByResult() {
    const table = document.getElementById('result_table');
    const rows = Array.from(table.querySelectorAll('tbody tr'));

    rows.sort((rowA, rowB) => {
        const resultA = rowA.cells[1].textContent.match(/[\d:.]+/)[0];
        const resultB = rowB.cells[1].textContent.match(/[\d:.]+/)[0];

        const [minutesA, secondsA] = resultA.split(':').map(parseFloat);
        const [minutesB, secondsB] = resultB.split(':').map(parseFloat);

        const timeA = minutesA * 60 + secondsA;
        const timeB = minutesB * 60 + secondsB;

        return timeA - timeB;
    });

    // Append sorted rows back to the table
    rows.forEach(row => table.querySelector('tbody').appendChild(row));
}

// Attach event listeners to the buttons
document.getElementById('sortByYear').addEventListener('click', sortByYear);
document.getElementById('sortByResult').addEventListener('click', sortByResult);


const tableBody = document.querySelector('#athlete-table tbody');
const originalHTML = tableBody.innerHTML;

// Function to sort by Athlete Place
function sortByPlace() {
    const rows = Array.from(tableBody.querySelectorAll('.result-row'));

    rows.sort((rowA, rowB) => {
        const placeA = parseInt(rowA.cells[2].textContent.trim());
        const placeB = parseInt(rowB.cells[2].textContent.trim());
        return placeA - placeB;
    });

    // Append sorted rows back to the table
    rows.forEach(row => tableBody.appendChild(row));
}

// Function to sort by Athlete Time
function sortByTime() {
    const rows = Array.from(tableBody.querySelectorAll('.result-row'));

    rows.sort((rowA, rowB) => {
        const timeA = rowA.cells[1].textContent.match(/[\d:.]+/)[0];
        const timeB = rowB.cells[1].textContent.match(/[\d:.]+/)[0];

        const [minutesA, secondsA] = timeA.split(':').map(parseFloat);
        const [minutesB, secondsB] = timeB.split(':').map(parseFloat);

        const totalSecondsA = minutesA * 60 + secondsA;
        const totalSecondsB = minutesB * 60 + secondsB;

        return totalSecondsA - totalSecondsB;
    });

    // Append sorted rows back to the table
    rows.forEach(row => tableBody.appendChild(row));
}

// Function to reset the table to its original order
function resetOrder() {
    tableBody.innerHTML = originalHTML;
}

// Attach event listeners to the buttons
document.getElementById('sortByPlace').addEventListener('click', sortByPlace);
document.getElementById('sortByTime').addEventListener('click', sortByTime);
document.getElementById('resetOrder').addEventListener('click', resetOrder);

// Filter results based on search query
function searchRace() {
    const query = document.getElementById('searchInput').value.toLowerCase();
    const rows = document.querySelectorAll('.result-row');

    rows.forEach(row => {
        const eventName = row.querySelector('td:first-child').textContent.toLowerCase();
        if (eventName.includes(query)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// Add event listener to search input
document.getElementById('searchInput').addEventListener('input', searchRace);

// Find the row with the fastest time and highlight it in green
function highlightFastestTime() {
    const rows = document.querySelectorAll('.result-row');
    let fastestTimeRow = null;
    let fastestTime = Infinity;

    rows.forEach(row => {
        const timeCell = row.querySelector('td:nth-child(2)'); // Assuming time is in the second column
        const timeText = timeCell.textContent;
        const timeParts = timeText.split(':');
        const timeInSeconds = parseInt(timeParts[0]) * 60 + parseFloat(timeParts[1]);

        if (timeInSeconds < fastestTime) {
            fastestTime = timeInSeconds;
            fastestTimeRow = row;
        }
    });

    if (fastestTimeRow) {
        fastestTimeRow.style.backgroundColor = 'lightgreen';
    }
}

// Call the function to highlight the fastest time
highlightFastestTime();

// Function to set a default image if the specified image fails to load
function setDefaultImage(imageId, defaultImagePath) {
    const imageElement = document.getElementById(imageId);

    // Check if the image element exists on the page
    if (imageElement) {
        // Set the default image on error
        imageElement.onerror = function() {
            imageElement.src = defaultImagePath;
        };
    }
}

// Apply to the image with ID 'athlete-image', using 'default_image.jpg' as fallback
setDefaultImage('athlete-image', '../images/default_image.jpg');