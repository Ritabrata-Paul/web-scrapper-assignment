// static/js/script.js
// ...

// Handle form submission
document.getElementById("scrapeForm").addEventListener("submit", function (e) {
    e.preventDefault();
    var url = document.getElementById("urlInput").value;
    sendAjaxRequest("/", function (response) {
        var resultContainer = document.getElementById("resultContainer");
        resultContainer.innerHTML = response;
        window.location.href = "/result";  // Redirect to the result page
    });
});

// ...
