document.addEventListener('DOMContentLoaded', () => {
    const statusElements = document.querySelectorAll('.http-status');
    statusElements.forEach(el => {
        const url = el.dataset.url;
        if (!url) return;
        // Initially update the status element.
        updateStatus(el, url);
        // Append a refresh button next to the status element.
        el.parentNode.appendChild(createRefreshButton(el, url));
    });
});

async function updateStatus(el, url) {
    // Show refreshing state.
    el.classList.add("refreshing");
    el.textContent = "Refreshing...";
    try {
        const status = await fetchStatus(url);
        displayStatus(el, status);
    } catch (error) {
        console.error("Error fetching status:", error);
        displayStatus(el, 404);
    } finally {
        el.classList.remove("refreshing");
    }
}

async function fetchStatus(url) {
    const response = await fetch(url);
    return response.status;
}

function displayStatus(el, status) {
    const success = status === 200;
    el.textContent = success ? `OK ${status}` : `Fail ${status}`;
    el.classList.toggle('success', success);
    el.classList.toggle('fail', !success);
}

function createRefreshButton(el, url) {
    const button = document.createElement("button");
    button.className = "btn-refresh";
    button.type = "button";
    button.title = "Refresh Status";
    button.addEventListener("click", async (e) => {
        e.preventDefault();
        button.disabled = true;
        button.classList.add("active");
        await updateStatus(el, url);
        button.classList.remove("active");
        button.disabled = false;
    });
    return button;
}
