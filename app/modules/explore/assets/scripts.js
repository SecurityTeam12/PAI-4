document.addEventListener('DOMContentLoaded', () => {
    send_query();
});



function send_query() {
    console.log("send query...");

    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = ''; // Clear previous results
    document.getElementById("results_not_found").style.display = "none";
    console.log("hide not found icon");

    const filters = document.querySelectorAll('#filters input, #filters select, #filters [type="radio"]');

    filters.forEach(filter => {
        filter.addEventListener('input', () => {
            const csrfToken = document.getElementById('csrf_token').value;

            const searchCriteria = {
                csrf_token: csrfToken,
                query: document.querySelector('#query').value,
                publication_type: document.querySelector('#publication_type').value,
                sorting: document.querySelector('[name="sorting"]:checked').value,
                min_number_of_models: document.querySelector('#min_number_of_models').value || 0,
                max_number_of_models: document.querySelector('#max_number_of_models').value || 100,
                min_number_of_features: document.querySelector('#min_number_of_features').value || 0,
                max_number_of_features: document.querySelector('#max_number_of_features').value || 100,
                day: document.querySelector('#day').value,
                month: document.querySelector('#month').value,
                year: document.querySelector('#year').value,
                max_size: parseFloat(document.querySelector('#max_size').value),
                size_unit: document.querySelector('#size_unit').value,
            };
            
            function renderTag(tag) {
                return `<span class="badge bg-primary me-1" style="cursor: pointer;" onclick="set_tag_as_query('${tag}')">${tag}</span>`;
            }
            

            console.log(document.querySelector('#publication_type').value);

            fetch('/explore', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(searchCriteria),
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    resultsContainer.innerHTML = ''; // Clear results

                    // Update results counter
                    const resultCount = data.length;
                    const resultText = resultCount === 1 ? 'dataset' : 'datasets';
                    document.getElementById('results_number').textContent = `${resultCount} ${resultText} found`;

                    if (resultCount === 0) {
                        console.log("show not found icon");
                        document.getElementById("results_not_found").style.display = "block";
                    } else {
                        document.getElementById("results_not_found").style.display = "none";
                    }

                    // Render each dataset
                    data.forEach(dataset => {
                        const card = document.createElement('div');
                        card.className = 'col-12';

                        const cardContent = `
                            <div class="card">
                                <div class="card-body">
                                    <div class="d-flex align-items-center justify-content-between">
                                        <h3></h3>
                                        <div>
                                            <span class="badge bg-primary" style="cursor: pointer;"></span>
                                        </div>
                                    </div>
                                    <p class="text-secondary"></p>
                                    <div class="row mb-2">
                                        <div class="col-md-4 col-12">
                                            <span class="text-secondary">Description</span>
                                        </div>
                                        <div class="col-md-8 col-12">
                                            <p class="card-text"></p>
                                        </div>
                                    </div>
                                    <div class="row mb-2">
                                        <div class="col-md-4 col-12">
                                            <span class="text-secondary">Authors</span>
                                        </div>
                                        <div class="col-md-8 col-12">
                                            ${dataset.authors.map(renderAuthor).join('')}
                                        </div>

                                    </div>
                                    <div class="row mb-2">
                                        <div class="col-md-4 col-12">
                                            <span class="text-secondary">Tags</span>
                                        </div>
                                        <div class="col-md-8 col-12">
                                            ${dataset.tags.map(renderTag).join('')}
                                        </div>

                                    </div>
                                    <div class="row">
                                        <div class="col-md-4 col-12"></div>
                                        <div class="col-md-8 col-12">
                                            <a class="btn btn-outline-primary btn-sm" style="border-radius: 5px;">View dataset</a>
                                            <a class="btn btn-outline-primary btn-sm" style="border-radius: 5px;">Download</a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        `;

                        card.innerHTML = cardContent;

                        // Set dynamic content safely
                        card.querySelector('h3').textContent = dataset.title;
                        card.querySelector('.badge').textContent = dataset.publication_type;
                        card.querySelector('.badge').onclick = () => set_publication_type_as_query(dataset.publication_type);
                        card.querySelector('p.text-secondary').textContent = formatDate(dataset.created_at);
                        card.querySelector('.card-text').textContent = dataset.description;

                        const authorsContainer = card.querySelector('.col-md-8.col-12:nth-of-type(2)');
                        dataset.authors.forEach(author => {
                            authorsContainer.appendChild(createAuthorElement(author));
                        });

                        const tagsContainer = card.querySelector('.col-md-8.col-12:nth-of-type(3)');
                        dataset.tags.forEach(tag => {
                            const tagElement = document.createElement('span');
                            tagElement.className = 'badge bg-primary me-1';
                            tagElement.style.cursor = 'pointer';
                            tagElement.textContent = tag;
                            tagElement.onclick = () => set_tag_as_query(tag);
                            tagsContainer.appendChild(tagElement);
                        });

                        const viewDatasetLink = card.querySelector('a:nth-of-type(1)');
                        viewDatasetLink.href = dataset.url;

                        const downloadLink = card.querySelector('a:nth-of-type(2)');
                        downloadLink.href = `/dataset/download/${dataset.id}`;
                        downloadLink.textContent = `Download (${dataset.total_size_in_human_format})`;

                        resultsContainer.appendChild(card);
                    });
                });
        });
    });
}

function formatDate(dateString) {
    const options = {day: 'numeric', month: 'long', year: 'numeric', hour: 'numeric', minute: 'numeric'};
    const date = new Date(dateString);
    return date.toLocaleString('en-US', options);
}

function set_tag_as_query(tagName) {
    const queryInput = document.getElementById('query');
    queryInput.value = tagName.trim();
    queryInput.dispatchEvent(new Event('input', {bubbles: true}));
}

function createAuthorElement(author) {
    const element = document.createElement('p');
    element.className = 'p-0 m-0';
    element.textContent = `${author.name}${author.affiliation ? ` (${author.affiliation})` : ''}${author.orcid ? ` (${author.orcid})` : ''}`;
    return element;
}

function set_publication_type_as_query(publicationType) {
    const publicationTypeSelect = document.getElementById('publication_type');
    for (let i = 0; i < publicationTypeSelect.options.length; i++) {
        if (publicationTypeSelect.options[i].text === publicationType.trim()) {
            // Set the value of the select to the value of the matching option
            publicationTypeSelect.value = publicationTypeSelect.options[i].value;
            break;
        }
    }
    publicationTypeSelect.dispatchEvent(new Event('input', {bubbles: true}));
}

document.getElementById('clear-filters').addEventListener('click', clearFilters);

function clearFilters() {

    // Reset the search query
    let queryInput = document.querySelector('#query');
    queryInput.value = "";

    // Reset the publication type to its default value
    let publicationTypeSelect = document.querySelector('#publication_type');
    publicationTypeSelect.value = "any"; // replace "any" with whatever your default value is

    // Reset the sorting option
    let sortingOptions = document.querySelectorAll('[name="sorting"]');
    sortingOptions.forEach(option => {
        option.checked = option.value == "newest"; // replace "default" with whatever your default value is
    });

    // Reset the number of models and features filters
    let minNumberOfModelsInput = document.querySelector('#min_number_of_models');
    minNumberOfModelsInput.value = "0";
    document.getElementById('min_models_output').value = "0";

    let maxNumberOfModelsInput = document.querySelector('#max_number_of_models');
    maxNumberOfModelsInput.value = "100";
    document.getElementById('max_models_output').value = "100";

    let minNumberOfFeaturesInput = document.querySelector('#min_number_of_features');
    minNumberOfFeaturesInput.value = "0";
    document.getElementById('min_features_output').value = "0";

    let maxNumberOfFeaturesInput = document.querySelector('#max_number_of_features');
    maxNumberOfFeaturesInput.value = "100";
    document.getElementById('max_features_output').value = "100";

    let dayInput = document.querySelector('#day');
    dayInput.value = "";

    let monthInput = document.querySelector('#month');
    monthInput.value = "";

    let yearInput = document.querySelector('#year');
    yearInput.value = "";

    let maxSizeInput = document.querySelector('#max_size');
    maxSizeInput.value = "";

    let sizeUnitSelect = document.querySelector('#size_unit');
    sizeUnitSelect.value = "bytes";

    // Perform a new search with the reset filters
    queryInput.dispatchEvent(new Event('input', {bubbles: true}));
}

document.addEventListener('DOMContentLoaded', () => {


    let urlParams = new URLSearchParams(window.location.search);
    let queryParam = urlParams.get('query');

    if (queryParam && queryParam.trim() !== '') {

        const queryInput = document.getElementById('query');
        queryInput.value = queryParam
        queryInput.dispatchEvent(new Event('input', {bubbles: true}));
        console.log("throw event");

    } else {
        const queryInput = document.getElementById('query');
        queryInput.dispatchEvent(new Event('input', {bubbles: true}));
    }
});