// Telegram Web App Chemistry Solver
let currentUserId = 'anonymous';
let currentReaction = '';

// Initialize Telegram Web App
if (window.Telegram && window.Telegram.WebApp) {
    const webApp = window.Telegram.WebApp;

    // Get user info
    if (webApp.initDataUnsafe && webApp.initDataUnsafe.user) {
        currentUserId = webApp.initDataUnsafe.user.id.toString();
    }

    // Expand to full height
    webApp.expand();

    // Set main button (optional)
    webApp.MainButton.setText('Готово');
    webApp.MainButton.hide();
}

// Tab switching
function showTab(tabName) {
    // Hide all tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));

    // Remove active class from all buttons
    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(btn => btn.classList.remove('active'));

    // Show selected tab
    document.getElementById(tabName + '-tab').classList.add('active');

    // Add active class to clicked button
    event.target.classList.add('active');

    // Load data for specific tabs
    if (tabName === 'examples') {
        loadExamples();
    } else if (tabName === 'history') {
        loadHistory();
    } else if (tabName === 'favorites') {
        loadFavorites();
    }
}

// Solve reaction
async function solveReaction() {
    const input = document.getElementById('reaction-input');
    const query = input.value.trim();

    if (!query) {
        showToast('Введите запрос!', 'error');
        return;
    }

    // Show loading
    showLoading(true);
    currentReaction = query;

    try {
        const response = await fetch('/api/solve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                user_id: currentUserId,
                timestamp: new Date().toISOString()
            })
        });

        const data = await response.json();

        if (data.success) {
            showResult(data.result);
            showToast('Реакция решена успешно!');
        } else {
            showResult('❌ ' + data.error);
            showToast('Ошибка при решении', 'error');
        }
    } catch (error) {
        showResult('❌ Ошибка подключения к серверу');
        showToast('Ошибка сети', 'error');
        console.error('Error:', error);
    }

    showLoading(false);
}

// Quick solve for example buttons
function quickSolve(reaction) {
    document.getElementById('reaction-input').value = reaction;
    solveReaction();
}

// Handle Enter key
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        solveReaction();
    }
}

// Show result
function showResult(result) {
    const resultSection = document.getElementById('result-section');
    const resultContent = document.getElementById('result-content');

    resultContent.innerHTML = result.replace(/\n/g, '<br>');
    resultSection.style.display = 'block';

    // Scroll to result
    resultSection.scrollIntoView({ behavior: 'smooth' });
}

// Add to favorites
async function addToFavorites() {
    if (!currentReaction) {
        showToast('Сначала решите реакцию!', 'error');
        return;
    }

    try {
        const response = await fetch(`/api/favorites/${currentUserId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                reaction: currentReaction
            })
        });

        if (response.ok) {
            showToast('Добавлено в избранное! ⭐');
        } else {
            showToast('Ошибка при добавлении', 'error');
        }
    } catch (error) {
        showToast('Ошибка сети', 'error');
        console.error('Error:', error);
    }
}

// Clear result
function clearResult() {
    document.getElementById('result-section').style.display = 'none';
    document.getElementById('reaction-input').value = '';
    currentReaction = '';
}

// Load examples
async function loadExamples() {
    try {
        const response = await fetch('/api/examples');
        const data = await response.json();

        if (data.success) {
            const examples = data.examples;

            // Fill example categories
            Object.keys(examples).forEach(category => {
                const container = document.getElementById(category + '-examples');
                if (container) {
                    container.innerHTML = examples[category]
                        .map(example => `<button onclick="quickSolve('${example}')">${example}</button>`)
                        .join('');
                }
            });
        }
    } catch (error) {
        console.error('Error loading examples:', error);
    }
}

// Load history
async function loadHistory() {
    try {
        const response = await fetch(`/api/history/${currentUserId}`);
        const data = await response.json();

        const historyList = document.getElementById('history-list');

        if (data.success && data.history.length > 0) {
            historyList.innerHTML = data.history
                .slice(-10) // Show last 10
                .reverse() // Newest first
                .map(item => `
                    <div class="history-item">
                        <h5>${item.query}</h5>
                        <p>${item.result.substring(0, 100)}${item.result.length > 100 ? '...' : ''}</p>
                    </div>
                `)
                .join('');
        } else {
            historyList.innerHTML = '<p class="empty-message">История пуста. Попробуйте решить несколько реакций!</p>';
        }
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

// Load favorites
async function loadFavorites() {
    try {
        const response = await fetch(`/api/favorites/${currentUserId}`);
        const data = await response.json();

        const favoritesList = document.getElementById('favorites-list');

        if (data.success && data.favorites.length > 0) {
            favoritesList.innerHTML = data.favorites
                .map(reaction => `
                    <div class="favorite-item">
                        <h5>${reaction}</h5>
                        <p>Избранная реакция</p>
                    </div>
                `)
                .join('');
        } else {
            favoritesList.innerHTML = '<p class="empty-message">Избранное пусто. Добавьте реакции из результатов!</p>';
        }
    } catch (error) {
        console.error('Error loading favorites:', error);
    }
}

// Clear history
async function clearHistory() {
    if (confirm('Очистить всю историю? Это действие нельзя отменить.')) {
        // In a real app, you'd call an API to clear server-side data
        // For demo, we'll just clear local display
        document.getElementById('history-list').innerHTML =
            '<p class="empty-message">История очищена!</p>';
        showToast('История очищена');
    }
}

// Clear favorites
async function clearFavorites() {
    if (confirm('Очистить все избранное? Это действие нельзя отменить.')) {
        // In a real app, you'd call an API to clear server-side data
        document.getElementById('favorites-list').innerHTML =
            '<p class="empty-message">Избранное очищено!</p>';
        showToast('Избранное очищено');
    }
}

// Loading overlay
function showLoading(show) {
    const overlay = document.getElementById('loading-overlay');
    overlay.style.display = show ? 'flex' : 'none';
}

// Toast notifications
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;

    container.appendChild(toast);

    // Auto remove after 3 seconds
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    // Load examples on page load
    loadExamples();

    // Telegram Web App ready
    if (window.Telegram && window.Telegram.WebApp) {
        window.Telegram.WebApp.ready();
    }

    // Show welcome message
    setTimeout(() => {
        showToast('🧠 Chemistry AI Solver готов к работе!');
    }, 1000);
});

// Handle Telegram Web App back button
if (window.Telegram && window.Telegram.WebApp) {
    window.Telegram.WebApp.onEvent('backButtonClicked', function() {
        // Go back to solve tab
        showTab('solve');
    });
}