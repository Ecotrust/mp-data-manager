document.addEventListener('DOMContentLoaded', () => {
    const elements = document.querySelectorAll('.http-status');
    elements.forEach(el => {
        const url = el.getAttribute('data-url');
        if (url) {
            fetchStatus(url).then(status => {
                addStatus(el, status);
            });
            addRefreshButton(el, url);
        }
    });
});

async function fetchStatus(url) {
    try {
        const response = await fetch(url);
        return response.status;
    } catch (error) {
        console.error('Fetch error:', error);
        return 404;
    }
}

function addStatus(el, status) {
    const statusText = status === 200 ? `OK ${status}` : `Fail ${status}`;
    el.textContent = statusText;
    el.classList.add(status === 200 ? 'success' : 'fail');
}

function addRefreshButton(el, url) {
    let refreshLink = document.createElement("a");
    refreshLink.href = url;
    refreshLink.title = "Refresh Statuses";
    refreshLink.style.display = "block";
    refreshLink.style.width = "40px";
    refreshLink.style.height = "40px";
    refreshLink.innerHTML = `
        <svg width="24" height="24" viewBox="0 0 24 24">
            <path d="M12 4V1L8 5l4 4V6c3.31 0 6 2.69 6 6 
                     0 .46-.05.91-.14 1.34l1.46 1.46C19.48 13.16 
                     20 12.12 20 11c0-4.42-3.58-8-8-8zm-6.36.64L4.22 
                     6.04C3.87 6.53 3.67 7.12 3.67 7.75c0 4.42 3.58 8 
                     8 8v3l4-4-4-4v3c-3.31 0-6-2.69-6-6 0-.63.2-1.22.56-1.71z" 
                  fill="#000"/>
        </svg>
    `;
    refreshLink.addEventListener("click", function (event) {
        event.preventDefault();
        el.classList.add("refreshing");
        el.textContent = "Refreshing...";
        fetchStatus(url).then(status => {
            addStatus(el, status);
        }).finally(() => {
            el.classList.remove("refreshing");
        });
    });
    el.parentNode.appendChild(refreshLink);
    console.log(el)
}
