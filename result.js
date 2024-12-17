console.log('here');
document.getElementById('queryForm').addEventListener('submit', async (e) => {
    console.log('here');
    e.preventDefault();

    // Extract form inputs
    const query = document.getElementById('query').value;
    const start = document.getElementById('start').value;
    const rows = document.getElementById('rows').value;

    // Define Solr query parameters
    const params = {
        q: query,
        q_op: "AND",
        start: parseInt(start, 10),
        rows: parseInt(rows, 10),
        defType: "edismax",
        qf: "Description^5 Participants^4 Country^3 Name_War^2 Winner"
    };

    console.log(params);

    try {
        // Send the query to the Flask backend
        const response = await axios.post("http://127.0.0.1:5000/query-solr", {
            uri: "http://localhost:8983/solr", // Solr base URI
            collection: "wikiwar",            // Solr collection name
            params: params                    // Query parameters
        });

        // Display results
        const resultsDiv = document.getElementById('queryResults');
        resultsDiv.innerHTML = `<pre>${JSON.stringify(response.data.response.docs, null, 2)}</pre>`;
    } catch (error) {
        console.error("Error fetching Solr results:", error);
        alert("Failed to fetch Solr results. Check console for details.");
    }
});
