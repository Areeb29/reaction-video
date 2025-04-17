document.addEventListener("DOMContentLoaded", function () {
    var submitButton = document.getElementById("submit-button");
    submitButton.addEventListener("click", function () {
        var userInput = document.getElementById("user-input").value;
        var language = document.getElementById("language").value;
        var length = document.getElementById("length").value;
        var topic = document.getElementById("topic").value;
        var type = document.getElementById("type").value;

        if (!userInput) {
            alert("Enter Message.");
        } else {
            submitMessage(userInput, language, length, topic, type);
        }
    });
});

function submitMessage(userInput, language, length, topic, type) {
    fetch("/submit", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_input: userInput, language: language, length: length, topic: topic, type: type }),
    })
    .then((response) => response.json())
    .then((data) => {
        formatAndDisplayResponse(data.response);
    });
}

function formatAndDisplayResponse(response) {
    var responseContainer = document.getElementById("response-container");
    responseContainer.innerHTML = ''; // Clear previous responses

    var userInput = document.getElementById("user-input").value;

    // Split response into sections
    var sections = response.split(/\*+/);

    // Bold input text
    var boldInput = document.createElement("strong");
    var inputDiv = document.createElement("div");
    var responseee = document.createElement("strong");
    inputDiv.classList.add("input-text");
    boldInput.textContent = "Input: ";
    inputDiv.textContent = userInput;
    responseee.textContent = "Response:";
    responseContainer.appendChild(boldInput);
    responseContainer.appendChild(inputDiv);
    responseContainer.appendChild(document.createElement("br"));
    responseContainer.appendChild(responseee);

    // Process each section
    sections.forEach((section) => {
        var sectionDiv = document.createElement("div");
        sectionDiv.classList.add("section");

        // Split section into lines
        var lines = section.trim().split("\n");

        // Process each line
        lines.forEach((line) => {
            if (line.trim().startsWith("- **")) {
                // Subsection with bold text
                var subsection = document.createElement("div");
                subsection.classList.add("subsection");
                var boldText = line.trim().substring(4).split("**");
                var emphasizedText = boldText[1];
                var remainingText = boldText[2];
                subsection.innerHTML =
                    "<span class='emphasis'>" +
                    emphasizedText +
                    "</span>" +
                    remainingText;
                sectionDiv.appendChild(subsection);
            } else {
                // Regular content line
                var content = document.createElement("div");
                content.classList.add("content");
                content.textContent = line.trim();
                sectionDiv.appendChild(content);
            }
        });

        // Add section to the response container
        responseContainer.appendChild(sectionDiv);
    });

    // Add horizontal line between sections
    if (responseContainer.children.length > 0) {
        var hr = document.createElement("hr");
        responseContainer.appendChild(hr);
    }
}



//document.addEventListener("DOMContentLoaded", function () {
//    var submitButton = document.getElementById("submit-button");
//    submitButton.addEventListener("click", function () {
//      var userInput = document.getElementById("user-input").value;
//      if (!userInput) {
//        alert("Enter Message.");
//      } else {
//        submitMessage();
//      }
//
//    });
//  });
//
//  function submitMessage() {
//    var userInput = document.getElementById("user-input").value;
//    fetch("/submit", {
//      method: "POST",
//      headers: {
//        "Content-Type": "application/json",
//      },
//      body: JSON.stringify({ user_input: userInput }),
//    })
//      .then((response) => response.json())
//      .then((data) => {
//        formatAndDisplayResponse(data.response);
//      });
//  }
//
//  function formatAndDisplayResponse(response) {
//    var responseContainer = document.getElementById("response-container");
//    var userInput = document.getElementById("user-input").value;
//
//    // Split response into sections
//    var sections = response.split(/\*+/);
//
//   // Bold input text
//   var boldInput = document.createElement("strong");
//   var inputDiv = document.createElement("div");
//   var responseee = document.createElement("strong");
//   inputDiv.classList.add("input-text");
//   boldInput.textContent = "Input: ";
//   inputDiv.textContent = userInput;
//   responseee.textContent = "Response:";
//   responseContainer.appendChild(boldInput);
//   responseContainer.appendChild(inputDiv);
//   responseContainer.appendChild(document.createElement("br"));
//   responseContainer.appendChild(responseee);
//
//
//    // Process each section
//    sections.forEach((section) => {
//      var sectionDiv = document.createElement("div");
//      sectionDiv.classList.add("section");
//
//      // Split section into lines
//      var lines = section.trim().split("\n");
//
//      // Process each line
//      lines.forEach((line) => {
//        if (line.trim().startsWith("- **")) {
//          // Subsection with bold text
//          var subsection = document.createElement("div");
//          subsection.classList.add("subsection");
//          var boldText = line.trim().substring(4).split("**");
//          var emphasizedText = boldText[1];
//          var remainingText = boldText[2];
//          subsection.innerHTML =
//            "<span class='emphasis'>" +
//            emphasizedText +
//            "</span>" +
//            remainingText;
//          sectionDiv.appendChild(subsection);
//        } else {
//          // Regular content line
//          var content = document.createElement("div");
//          content.classList.add("content");
//          content.textContent = line.trim();
//          sectionDiv.appendChild(content);
//        }
//      });
//
//
//      // Add section to the response container
//      responseContainer.appendChild(sectionDiv);
//    });
//
//      // Add horizontal line between sections
//      if (responseContainer.children.length > 0) {
//        var hr = document.createElement("hr");
//        responseContainer.appendChild(hr);
//      }
//  }