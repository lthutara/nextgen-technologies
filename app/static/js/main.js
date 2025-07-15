function triggerScraping(category = null) {
    const btn = event.target;
    const originalText = btn.textContent;
    
    btn.disabled = true;
    btn.textContent = 'Updating...';
    
    const url = category ? `/api/scrape?category=${encodeURIComponent(category)}` : '/api/scrape';
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('Articles updated successfully!', 'success');
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } else {
            showAlert('Error updating articles. Please try again.', 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Error updating articles. Please try again.', 'danger');
    })
    .finally(() => {
        btn.disabled = false;
        btn.textContent = originalText;
    });
}

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Auto-refresh functionality
function setupAutoRefresh() {
    const refreshInterval = 300000; // 5 minutes
    
    setInterval(() => {
        fetch('/api/articles?limit=1')
            .then(response => response.json())
            .then(data => {
                if (data.articles && data.articles.length > 0) {
                    const lastScraped = new Date(data.articles[0].scraped_date);
                    const fiveMinutesAgo = new Date(Date.now() - 5 * 60 * 1000);
                    
                    if (lastScraped > fiveMinutesAgo) {
                        showAlert('New articles available!', 'info');
                    }
                }
            })
            .catch(error => console.error('Auto-refresh error:', error));
    }, refreshInterval);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    setupAutoRefresh();
});