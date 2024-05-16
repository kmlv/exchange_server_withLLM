// Simulating backend response
const backendResponse = [
    "This is the first line of text.",
    "This is the second line of text.",
    "And here comes the third line of text.",
    "Finally, the last line of text."
];

// Function to display text
function displayText() {
    const textDisplay = document.getElementById('textDisplay');
    textDisplay.innerHTML = ""; // Clear existing content

    backendResponse.forEach(text => {
        const paragraph = document.createElement('p');
        paragraph.textContent = text;
        textDisplay.appendChild(paragraph);
    });
}

// Call displayText function when the page loads
window.onload = displayText;
