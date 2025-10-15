// frontend/app.js

const backendBaseURL = "http://127.0.0.1:5000";
const apiURL = `${backendBaseURL}/api/search`;

document.getElementById("searchBtn").addEventListener("click", async () => {
  const fileInput = document.getElementById("imgFile");
  const urlInput = document.getElementById("imgUrl").value.trim();
  const loadingDiv = document.getElementById("loading");
  const queryDiv = document.getElementById("queryImage");
  const resultsDiv = document.getElementById("results");

  // Clear previous results
  queryDiv.innerHTML = "";
  resultsDiv.innerHTML = "";
  loadingDiv.style.display = "block";

  let formData;
  let useFile = false;

  if (fileInput.files.length > 0) {
    formData = new FormData();
    formData.append("file", fileInput.files[0]);
    useFile = true;
  } else if (urlInput) {
    formData = JSON.stringify({ image_url: urlInput });
  } else {
    alert("Please upload an image or enter a URL!");
    loadingDiv.style.display = "none";
    return;
  }

  try {
    let response;
    if (useFile) {
      response = await fetch(apiURL, { method: "POST", body: formData });
    } else {
      response = await fetch(apiURL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: formData,
      });
    }
    
    // Check if the server responded with an error (like 404)
    if (!response.ok) {
        throw new Error(`Server responded with status: ${response.status}`);
    }

    const data = await response.json();
    loadingDiv.style.display = "none";

    // Display query image
    if (useFile) {
      const imgURL = URL.createObjectURL(fileInput.files[0]);
      queryDiv.innerHTML = `<h3>Your Query Image:</h3><img src="${imgURL}" alt="query image">`;
    } else {
      queryDiv.innerHTML = `<h3>Your Query Image:</h3><img src="${urlInput}" alt="query image">`;
    }

    // Display similar products
    if (data.results && data.results.length > 0) {
      data.results.forEach((p) => {
        const card = document.createElement("div");
        card.classList.add("card");
        // IMPORTANT: Use the backendBaseURL for image sources
        card.innerHTML = `
          <img src="${backendBaseURL}/${p.image}" alt="${p.name}">
          <h3>${p.name}</h3>
          <p>${p.category}</p>
          <p>Similarity: ${p.similarity}</p>
        `;
        resultsDiv.appendChild(card);
      });
    } else {
      resultsDiv.innerHTML = "<p>No similar products found 😔</p>";
    }
  } catch (err) {
    console.error(err);
    loadingDiv.style.display = "none";
    alert("Error: Unable to connect to backend. Please check the console for details.");
  }
});