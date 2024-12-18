console.log('here');
document.getElementById('queryForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    // Extrair dados do formulário
    const query = document.getElementById('query').value;
    const rows = document.getElementById('rows').value;

    // Obter intervalo de anos
    const minYear = parseInt(document.getElementById('minYear').value, 10);
    const maxYear = parseInt(document.getElementById('maxYear').value, 10);

    // Definir parâmetros da consulta Solr
    const params = {
        q: query,
        q_op: "AND",
        start: 0,
        rows: parseInt(rows, 10),
        defType: "edismax",
        qf: "Description^5 Participants^4 Country^3 Name_War^2 Winner"
    };

    try {
        // Enviar consulta para o backend Flask
        const response = await axios.post("http://127.0.0.1:5000/query-solr", {
            uri: "http://localhost:8983/solr", // URI base do Solr
            collection: "wikiwar",            // Nome da coleção Solr
            params: params                    // Parâmetros da consulta
        });

        // Exibir resultados
        const resultsDiv = document.getElementById('queryResults');
        resultsDiv.innerHTML = ""; // Limpar resultados anteriores

        const docs = response.data.response.docs;

        docs.forEach(doc => {
            // Extrair título e descrição
            const title = "Battle of " + doc.ID;
            const description = doc.Description || 'No description available.';
            const year = doc.Year;

            // Filtrar resultados com base no intervalo de anos
            if (year < minYear || year > maxYear) {
                return; // Ignorar resultados fora do intervalo de anos
            }

            // Criar elemento para cada resultado
            const resultDiv = document.createElement('div');
            resultDiv.classList.add('result');

            // Inserir conteúdo da batalha
            resultDiv.innerHTML = `
                <h2 class="battle-title">${title}</h2>
                <p class="battle-description">${description}</p>
                <p class="battle-year">Year: ${year}</p>
                <a href="http://127.0.0.1:5000/battle-detail/${doc.ID}" class="see-more-btn">See more details about this battle</a>
            `;

            // Adicionar ao contêiner de resultados
            resultsDiv.appendChild(resultDiv);
        });

    } catch (error) {
        console.error("Erro ao buscar resultados do Solr:", error);
        alert("Falha ao buscar resultados do Solr. Verifique o console para mais detalhes.");
    }
});
