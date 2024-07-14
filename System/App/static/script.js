document.getElementById('sentimentForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const textInput = document.getElementById('textInput').value;

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ Text: textInput }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('result').textContent = `Error: ${data.error}`;
        } else {
            const prediction = data.predictions[0];
            const sentimentResult = document.getElementById('result');
            sentimentResult.textContent = `Result: ${prediction}`;

            // Update emoji based on prediction
            const emojiResult = document.getElementById('emojiResult');
            emojiResult.innerHTML = ''; // Clear previous emoji

            switch (prediction) {
                case 'Negative':
                    emojiResult.innerHTML = ' 😞'; // Sad emoji
                    break;
                case 'Positive':
                    emojiResult.innerHTML = ' 😊'; // Happy emoji
                    break;
                case 'Irrelevant':
                    emojiResult.innerHTML = ' 🤷‍♂️'; // Shrugging person emoji for Irrelevant
                    break;
                case 'Neutral':
                    emojiResult.innerHTML = ' 😐'; // Neutral face emoji for Neutral
                    break;
                default:
                    emojiResult.innerHTML = ''; // Default case
                    break;
            }
        }
    })
    .catch((error) => {
        document.getElementById('result').textContent = `Error: ${error}`;
    });
});
