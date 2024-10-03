form.addEventListener("submit", function (e) {
    e.preventDefault();

    // Collect user preferences
    const roastLevel = document.querySelector("#roast-level").value;
    const acidity = document.querySelector("#acidity").value;
    const drinkType = document.querySelector("#drink-type").value;
    const idealCup = document.querySelector("#ideal-cup").value;
    const drinkTime = document.querySelector("#drink-time").value;
    const strength = document.querySelector("#strength").value;

    // Create user preference object
    const preferences = {
        roast_level: roastLevel,
        acidity: acidity,
        drink_type: drinkType,
        description: idealCup,
        drink_time: drinkTime,
        strength: strength
    };

    // Send preferences to API
    fetch("/recommend", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(preferences)
    })
    .then(response => response.json())
    .then(data => {
        displayRecommendations(data);  // Single recommendation
    })
    .catch(error => console.error("Error:", error));
});

function displayRecommendations(data) {
    recommendationSection.innerHTML = "";

    const card = document.createElement("div");
    card.classList.add("result-card");

    const title = document.createElement("h3");
    title.innerText = data.Flavor;

    const country = document.createElement("p");
    country.innerText = `Country: ${data.Country}`;

    const healthBenefit = document.createElement("p");
    healthBenefit.innerText = `Health Benefit: ${data['Health Benefit']}`;

    const description = document.createElement("p");
    description.innerText = `Description: ${data.Description}`;

    const videoLink = document.createElement("a");
    videoLink.href = data['Video URL'];
    videoLink.classList.add("video-link");
    videoLink.innerText = "Watch Video";

    card.appendChild(title);
    card.appendChild(country);
    card.appendChild(healthBenefit);
    card.appendChild(description);
    card.appendChild(videoLink);

    recommendationSection.appendChild(card);
}
