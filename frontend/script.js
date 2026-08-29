const API_URL = "http://127.0.0.1:8000";


async function searchDocuments() {

    const query =
        document.getElementById("searchInput").value;

    const mode =
        document.getElementById("searchMode").value;


    if (!query.trim()) {

        alert("Please enter a search keyword.");

        return;
    }


    try {

        const response = await fetch(
            `${API_URL}/search?query=${encodeURIComponent(query)}&mode=${mode}`
        );


        const data = await response.json();


        displayResults(data.results);

    } catch (error) {

        console.error(error);

        alert("Unable to connect to the server.");

    }
}


function displayResults(results) {

    const resultsDiv =
        document.getElementById("results");

    resultsDiv.innerHTML =
        "<h2>📊 Search Results</h2>";

    if (results.length === 0) {

        resultsDiv.innerHTML +=
            "<p>No documents found.</p>";

        return;
    }

    results.forEach(result => {

        const card =
            document.createElement("div");

        card.className = "result-card";

        card.innerHTML = `

            <h3>${result.title}</h3>

            <p>
                <strong>Relevance Score:</strong>
                ${result.score}
            </p>

            <p>
                <strong>Matched Keywords:</strong>
                ${result.matched_keywords}
            </p>

            <div class="result-actions">

                <button
                    class="view-button"
                    onclick="viewDocument(${result.document_id})">

                    👁 View

                </button>

                <button
                    class="edit-button"
                    onclick="editDocument(${result.document_id})">

                    ✏️ Edit

                </button>

                <button
                    class="delete-button"
                    onclick="deleteDocument(${result.document_id})">

                    🗑 Delete

                </button>

            </div>
        `;

        resultsDiv.appendChild(card);

    });
}


async function viewDocument(documentId) {

    try {

        const response = await fetch(
            `${API_URL}/documents/${documentId}`
        );


        const data = await response.json();


        if (!response.ok) {

            alert(
                data.message ||
                "Unable to retrieve document."
            );

            return;
        }


        document.getElementById(
            "modalTitle"
        ).textContent = data.title;


        document.getElementById(
            "modalContent"
        ).textContent = data.content;


        document.getElementById(
            "documentModal"
        ).style.display = "block";


    } catch (error) {

        console.error(error);

        alert(
            "Unable to connect to the server."
        );
    }
}
async function addDocument() {

    const title =
        document.getElementById("documentTitle").value;

    const content =
        document.getElementById("documentContent").value;

    const message =
        document.getElementById("uploadMessage");


    if (!title.trim() || !content.trim()) {

        message.textContent =
            "Please enter both title and content.";

        return;
    }


    try {

        const response = await fetch(
            `${API_URL}/documents`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    title: title,
                    content: content
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {

            message.textContent =
                "Failed to add document.";

            return;
        }


        message.textContent =
            `Document added successfully. ID: ${data.id}`;


        // Clear form

        document.getElementById(
            "documentTitle"
        ).value = "";

        document.getElementById(
            "documentContent"
        ).value = "";


    } catch (error) {

        console.error(error);

        message.textContent =
            "Unable to connect to the server.";

    }
}
async function editDocument(documentId) {

    try {

        const response = await fetch(
            `${API_URL}/documents/${documentId}`
        );

        const data = await response.json();


        const newTitle = prompt(
            "Enter new title:",
            data.title
        );

        if (newTitle === null) {
            return;
        }


        const newContent = prompt(
            "Enter new content:",
            data.content
        );

        if (newContent === null) {
            return;
        }


        const updateResponse = await fetch(
            `${API_URL}/documents/${documentId}`,
            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    title: newTitle,
                    content: newContent
                })
            }
        );


        const result = await updateResponse.json();


        if (updateResponse.ok) {

            alert("Document updated successfully!");

            searchDocuments();

        } else {

            alert(
                result.message ||
                "Failed to update document."
            );
        }


    } catch (error) {

        console.error(error);

        alert("Unable to update document.");
    }
}
async function deleteDocument(documentId) {

    const confirmDelete = confirm(
        "Are you sure you want to delete this document?"
    );


    if (!confirmDelete) {
        return;
    }


    try {

        const response = await fetch(
            `${API_URL}/documents/${documentId}`,
            {
                method: "DELETE"
            }
        );


        const data = await response.json();


        if (response.ok) {

            alert(
                "Document deleted successfully!"
            );

            searchDocuments();

        } else {

            alert(
                data.message ||
                "Failed to delete document."
            );
        }


    } catch (error) {

        console.error(error);

        alert(
            "Unable to delete document."
        );
    }
}
function closeModal() {

    document.getElementById(
        "documentModal"
    ).style.display = "none";
}


window.onclick = function(event) {

    const modal =
        document.getElementById("documentModal");


    if (event.target === modal) {

        modal.style.display = "none";
    }
};


function handleSearchKey(event) {

    if (event.key === "Enter") {

        searchDocuments();
    }
}