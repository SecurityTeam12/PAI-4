document.addEventListener('DOMContentLoaded', () => {
    send_query();

    const urlParams = new URLSearchParams(window.location.search);
    const queryParam = urlParams.get('query');
    const queryInput = document.getElementById('query');
    if (queryParam && queryParam.trim() !== '') {
        queryInput.value = queryParam;
    }
    queryInput.dispatchEvent(new Event('input', { bubbles: true }));
});

function toggleSections() {
    const section1 = document.getElementById('normal-search');
    const section2 = document.getElementById('advanced-search');

    if (section1.style.display === 'block') {
        clearFilters();
        section1.style.display = 'none';
        section2.style.display = 'block';
    } else {
        clearFilters();
        section1.style.display = 'block';
        section2.style.display = 'none';
    }
}

function send_query() {
    console.log("send query...");

    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = ''; // Clear previous results
    document.getElementById("results_not_found").style.display = "none";
    console.log("hide not found icon");

    const filters = document.querySelectorAll('#filters input, #filters select, #filters [type="radio"], #filters number');

    filters.forEach(filter => {
        filter.addEventListener('input', () => {
            const csrfToken = document.getElementById('csrf_token').value;

            const maxSizeInput = document.querySelector('#query-max-size').value;
            const sizeUnit = document.getElementById('size-unit').value;
            const sizeValue = parseFloat(maxSizeInput);
            let sizeInBytes;

            switch (sizeUnit) {
                case 'kb':
                    sizeInBytes = sizeValue * 1024;
                    break;
                case 'mb':
                    sizeInBytes = sizeValue * 1024 * 1024;
                    break;
                case 'gb':
                    sizeInBytes = sizeValue * 1024 * 1024 * 1024;
                    break;
                default:
                    sizeInBytes = sizeValue;
            }

            const searchCriteria = {
                csrf_token: csrfToken,
                query: document.querySelector('#query').value,
                title: document.querySelector('#query-title').value,
                description: document.querySelector('#query-description').value,
                authors: document.querySelector('#query-authors').value,
                q_tags: document.querySelector('#query-tags').value,
                bytes: sizeInBytes,
                min_date: document.querySelector("#form-min-date").value,
                max_date: document.querySelector("#form-max-date").value,
                publication_type: document.querySelector('#publication_type').value
            };

            console.log(document.querySelector('#form-min-date').value);

            fetch('/exploreuvl', {
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
                    const resultText = resultCount === 1 ? 'Model' : 'Models';
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

                        const cardBody = document.createElement('div');
                        cardBody.className = 'card-body';

                        const titleRow = document.createElement('div');
                        titleRow.className = 'd-flex align-items-center justify-content-between';

                        const title = document.createElement('h3');
                        title.textContent = dataset.title;

                        const badgeContainer = document.createElement('div');
                        const badge = document.createElement('span');
                        badge.className = 'badge bg-primary';
                        badge.style.cursor = 'pointer';
                        badge.textContent = dataset.publication_type;
                        badge.onclick = () => set_publication_type_as_query(dataset.publication_type);
                        badgeContainer.appendChild(badge);

                        titleRow.appendChild(title);
                        titleRow.appendChild(badgeContainer);

                        const publicationDate = document.createElement('p');
                        publicationDate.className = 'text-secondary';
                        publicationDate.textContent = formatDate(dataset.publication_date);

                        const descriptionRow = createRow('Description', dataset.description);
                        const authorsRow = createRow('Authors', dataset.authors.map(author => `${author.name}${author.affiliation ? ` (${author.affiliation})` : ''}${author.orcid ? ` (${author.orcid})` : ''}`).join(', '));
                        const tagsRow = createRow('Tags', dataset.tags.map(tag => {
                            const tagElement = document.createElement('span');
                            tagElement.className = 'badge bg-primary me-1';
                            tagElement.style.cursor = 'pointer';
                            tagElement.textContent = tag;
                            tagElement.onclick = () => set_tag_as_query(tag);
                            return tagElement.outerHTML;
                        }).join(''));

                        const downloadRow = document.createElement('div');
                        downloadRow.className = 'row';
                        const downloadCol = document.createElement('div');
                        downloadCol.className = 'col-md-8 col-12';
                        const downloadLink = document.createElement('a');
                        downloadLink.className = 'btn btn-outline-primary btn-sm';
                        downloadLink.href = dataset.files[0].url;
                        downloadLink.textContent = `Download ${dataset.files.length} files (${get_total_size(dataset.files)} bytes)`;
                        downloadCol.appendChild(downloadLink);
                        downloadRow.appendChild(downloadCol);

                        cardBody.appendChild(titleRow);
                        cardBody.appendChild(publicationDate);
                        cardBody.appendChild(descriptionRow);
                        cardBody.appendChild(authorsRow);
                        cardBody.appendChild(tagsRow);
                        cardBody.appendChild(downloadRow);

                        const cardElement = document.createElement('div');
                        cardElement.className = 'card';
                        cardElement.appendChild(cardBody);

                        card.appendChild(cardElement);
                        resultsContainer.appendChild(card);
                    });
                });
        });
    });
}

function createRow(label, content) {
    const row = document.createElement('div');
    row.className = 'row mb-2';

    const labelCol = document.createElement('div');
    labelCol.className = 'col-md-4 col-12';
    const labelSpan = document.createElement('span');
    labelSpan.className = 'text-secondary';
    labelSpan.textContent = label;
    labelCol.appendChild(labelSpan);

    const contentCol = document.createElement('div');
    contentCol.className = 'col-md-8 col-12';
    if (typeof content === 'string') {
        const contentParagraph = document.createElement('p');
        contentParagraph.className = 'card-text';
        contentParagraph.textContent = content;
        contentCol.appendChild(contentParagraph);
    } else {
        contentCol.innerHTML = content; // For tags or other HTML-safe content
    }

    row.appendChild(labelCol);
    row.appendChild(contentCol);

    return row;
}

function get_total_size(files) {
    return files.reduce((acc, file) => acc + file.size_in_bytes, 0);
}

function setSelectValueByText(selectElement, textValue) {
    const trimmedValue = textValue.trim();
    for (let i = 0; i < selectElement.options.length; i++) {
        if (selectElement.options[i].text === trimmedValue) {
            selectElement.value = selectElement.options[i].value;
            break;
        }
    }
}

function formatDate(dateString) {
    const options = { day: 'numeric', month: 'long', year: 'numeric', hour: 'numeric', minute: 'numeric' };
    const date = new Date(dateString);
    return date.toLocaleString('en-US', options);
}

function set_tag_as_query(tagName) {
    const section1 = document.getElementById('normal-search');
    const queryInput = section1.style.display === 'block' ? document.getElementById('query') : document.getElementById('query-tags');
    queryInput.value = tagName.trim();
    queryInput.dispatchEvent(new Event('input', { bubbles: true }));
}

function set_publication_type_as_query(publicationType) {
    const publicationTypeSelect = document.getElementById('publication_type');
    setSelectValueByText(publicationTypeSelect, publicationType);
    publicationTypeSelect.dispatchEvent(new Event('input', { bubbles: true }));
}

document.getElementById('clear-filters').addEventListener('click', clearFilters);

function clearFilters() {
    const fieldsToClear = ['#query', '#query-title', '#query-authors', '#query-tags', '#query-description', '#query-max-size'];
    fieldsToClear.forEach(selector => {
        const field = document.querySelector(selector);
        if (field) field.value = '';
    });
    document.querySelector('#form-max-date').value = '';
    document.querySelector('#form-min-date').value = '';
    document.querySelector('#publication_type').value = 'any';
    document.getElementById('query').dispatchEvent(new Event('input', { bubbles: true }));
}

