// Main JavaScript file for SIAKAD

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Add loading animation to forms
    var forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            var submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                var originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
                submitBtn.disabled = true;
            }
        });
    });

    // Sidebar toggle for mobile
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
    }

    // Auto-dismiss success messages
    var successAlerts = document.querySelectorAll('.alert-success');
    successAlerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.remove();
            }, 300);
        }, 3000);
    });
});

// Utility functions
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

function confirmDelete(message = 'Apakah Anda yakin ingin menghapus data ini?') {
    return confirm(message);
}

function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function formatDate(date) {
    const options = { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    };
    return new Date(date).toLocaleDateString('id-ID', options);
}

// Form validation helpers
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhone(phone) {
    const re = /^[\d\-\+\(\)\s]+$/;
    return re.test(phone);
}

function validateNISN(nisn) {
    return /^\d{10}$/.test(nisn);
}

function validateNIP(nip) {
    return /^\d{18}$/.test(nip);
}

// Table search functionality
function searchTable(inputId, tableId, columns = []) {
    const input = document.getElementById(inputId);
    const table = document.getElementById(tableId);
    
    if (!input || !table) return;
    
    input.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');
        
        Array.from(rows).forEach(row => {
            let found = false;
            
            if (columns.length === 0) {
                // Search all columns
                const cells = row.getElementsByTagName('td');
                for (let cell of cells) {
                    if (cell.textContent.toLowerCase().includes(searchTerm)) {
                        found = true;
                        break;
                    }
                }
            } else {
                // Search specific columns
                columns.forEach(colIndex => {
                    const cell = row.cells[colIndex];
                    if (cell && cell.textContent.toLowerCase().includes(searchTerm)) {
                        found = true;
                    }
                });
            }
            
            row.style.display = found ? '' : 'none';
        });
    });
}

// Loading overlay
function showLoading() {
    const overlay = document.createElement('div');
    overlay.id = 'loadingOverlay';
    overlay.className = 'position-fixed w-100 h-100 d-flex align-items-center justify-content-center';
    overlay.style.cssText = 'top: 0; left: 0; background: rgba(0,0,0,0.5); z-index: 9999;';
    overlay.innerHTML = `
        <div class="text-center text-white">
            <div class="spinner-border mb-3" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p>Sedang memproses...</p>
        </div>
    `;
    document.body.appendChild(overlay);
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.remove();
    }
}

// Export functions
function exportTableToCSV(tableId, filename = 'data.csv') {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    for (let row of rows) {
        const cols = row.querySelectorAll('td, th');
        const csvRow = [];
        
        for (let col of cols) {
            csvRow.push('"' + col.textContent.replace(/"/g, '""') + '"');
        }
        
        csv.push(csvRow.join(','));
    }
    
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    
    window.URL.revokeObjectURL(url);
}

// Print functionality
function printTable(tableId) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <html>
        <head>
            <title>Print</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                @media print {
                    .no-print { display: none !important; }
                    body { font-size: 12px; }
                    table { font-size: 11px; }
                }
            </style>
        </head>
        <body>
            <div class="container-fluid">
                <h3 class="text-center mb-4">SIAKAD - Sistem Informasi Akademik</h3>
                ${table.outerHTML}
            </div>
        </body>
        </html>
    `);
    
    printWindow.document.close();
    printWindow.focus();
    printWindow.print();
    printWindow.close();
}

// Local storage helpers
function saveToStorage(key, data) {
    try {
        localStorage.setItem(key, JSON.stringify(data));
        return true;
    } catch (e) {
        console.error('Error saving to localStorage:', e);
        return false;
    }
}

function getFromStorage(key) {
    try {
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : null;
    } catch (e) {
        console.error('Error reading from localStorage:', e);
        return null;
    }
}

function removeFromStorage(key) {
    try {
        localStorage.removeItem(key);
        return true;
    } catch (e) {
        console.error('Error removing from localStorage:', e);
        return false;
    }
}

// Theme toggle (if needed in future)
function toggleTheme() {
    const body = document.body;
    const currentTheme = body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    body.setAttribute('data-theme', newTheme);
    saveToStorage('theme', newTheme);
}

// Initialize theme from storage
function initTheme() {
    const savedTheme = getFromStorage('theme');
    if (savedTheme) {
        document.body.setAttribute('data-theme', savedTheme);
    }
}

// Call theme initialization
initTheme();