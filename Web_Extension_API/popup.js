// popup.js

// Function to handle prediction
function predict() {
  console.log('Predict function called');

  var url = document.getElementById('urlInput').value.trim();

  if (!url) {
    document.getElementById('result').innerText = "Please enter a URL.";
    return;
  }

  // Show loading spinner
  document.getElementById('loading').style.display = 'flex';

  fetch('http://127.0.0.1:5000/predict', {   // ✅ FIXED URL
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ url: url })
  })
  .then(response => {
    if (!response.ok) {
      throw new Error("Server error: " + response.status);
    }
    return response.json();
  })
  .then(data => {
    document.getElementById('loading').style.display = 'none';

    var resultElement = document.getElementById('result');
    resultElement.innerHTML = '';

    // Pick color
    var color = data.result_str === "URL IS SAFE!" ? "#28a745" : "#dc3545";

    // Result card
    var resultDiv = document.createElement('div');
    resultDiv.textContent = data.result_str;
    resultDiv.classList.add('result-card');
    resultDiv.style.backgroundColor = color;
    resultElement.appendChild(resultDiv);

    // Show similar URLs (if any)
    if (data.google_results && data.google_results.length > 0) {
      var similarUrlsContainer = document.createElement('div');

      data.google_results.forEach(function(u) {
        var similarUrlCard = document.createElement('div');
        similarUrlCard.classList.add('similar-card');

        var link = document.createElement('a');
        link.href = u;
        link.target = "_blank";
        link.textContent = u;

        similarUrlCard.appendChild(link);
        similarUrlsContainer.appendChild(similarUrlCard);
      });

      resultElement.appendChild(similarUrlsContainer);
    }
  })
  .catch(error => {
    console.error("Prediction error:", error);
    document.getElementById('loading').style.display = 'none';
    document.getElementById('result').innerText =
      "Error: Could not connect to API. Make sure Flask is running.";
  });
}


// Attach click handler (Manifest V3 compatible)
document.addEventListener('DOMContentLoaded', function () {
  const btn = document.getElementById('predictButton');
  if (btn) {
    btn.addEventListener('click', predict);
  } else {
    console.error("Predict button not found");
  }
});
