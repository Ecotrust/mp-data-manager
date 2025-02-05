document.addEventListener('DOMContentLoaded', () => {
    const elements = document.querySelectorAll('.http-status');
    elements.forEach(el => {
        const url = el.getAttribute('data-url');
        if (url) {
            fetchStatus(url).then(status => {
                const statusText = status === 200 ? `OK ${status}` : `Fail ${status}`;
                el.textContent = statusText;
                el.classList.add(status === 200 ? 'success' : 'fail');
            });
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
