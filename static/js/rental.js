/**
 * Rental-specific JavaScript
 */

// Real-time cost calculator
class RentalCostCalculator {
    constructor(hourlyRate, startTime) {
        this.hourlyRate = parseFloat(hourlyRate);
        this.startTime = new Date(startTime);
        this.lateFeePeriod = 24; // hours
        this.lateFeeRate = 0.5; // 50% extra
    }
    
    getCurrentDuration() {
        const now = new Date();
        const diffMs = now - this.startTime;
        return diffMs / (1000 * 60 * 60); // Convert to hours
    }
    
    calculateCost() {
        const hours = this.getCurrentDuration();
        let baseCost = this.hourlyRate * hours;
        let lateFee = 0;
        
        if (hours > this.lateFeePeriod) {
            const overtimeHours = hours - this.lateFeePeriod;
            lateFee = this.hourlyRate * overtimeHours * this.lateFeeRate;
        }
        
        return {
            hours: hours,
            baseCost: baseCost,
            lateFee: lateFee,
            totalCost: baseCost + lateFee,
            isOverdue: hours > this.lateFeePeriod
        };
    }
    
    formatCost(cost) {
        return `KES ${cost.toFixed(2)}`;
    }
}

// Initialize cost calculator on active rental page
document.addEventListener('DOMContentLoaded', function() {
    const costElement = document.getElementById('current-cost');
    const durationElement = document.getElementById('duration-timer');
    
    if (costElement && durationElement) {
        const hourlyRate = parseFloat(costElement.dataset.hourlyRate);
        const startTime = costElement.dataset.startTime;
        
        const calculator = new RentalCostCalculator(hourlyRate, startTime);
        
        function updateDisplay() {
            const cost = calculator.calculateCost();
            costElement.textContent = cost.totalCost.toFixed(2);
            durationElement.textContent = `${cost.hours.toFixed(1)} hours`;
            
            if (cost.isOverdue) {
                durationElement.classList.add('text-danger');
            }
        }
        
        // Update every 10 seconds
        setInterval(updateDisplay, 10000);
        updateDisplay();
    }
});

// Reservation countdown timer
class ReservationTimer {
    constructor(expiresAt, onExpire) {
        this.expiresAt = new Date(expiresAt);
        this.onExpire = onExpire;
        this.interval = null;
    }
    
    start() {
        this.update();
        this.interval = setInterval(() => this.update(), 1000);
    }
    
    stop() {
        if (this.interval) {
            clearInterval(this.interval);
        }
    }
    
    update() {
        const now = new Date();
        const remaining = this.expiresAt - now;
        
        if (remaining <= 0) {
            this.stop();
            if (this.onExpire) {
                this.onExpire();
            }
            return;
        }
        
        const minutes = Math.floor(remaining / 60000);
        const seconds = Math.floor((remaining % 60000) / 1000);
        
        this.display(minutes, seconds);
    }
    
    display(minutes, seconds) {
        const countdownElement = document.getElementById('countdown');
        if (countdownElement) {
            countdownElement.textContent = 
                `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            
            // Change color based on time remaining
            if (minutes < 5) {
                countdownElement.classList.remove('text-warning');
                countdownElement.classList.add('text-danger');
            } else if (minutes < 10) {
                countdownElement.classList.remove('text-success');
                countdownElement.classList.add('text-warning');
            }
        }
    }
}

// Return bicycle form validation
function setupReturnForm() {
    const returnForm = document.getElementById('return-form');
    if (returnForm) {
        returnForm.addEventListener('submit', function(e) {
            const station = document.getElementById('id_return_station');
            if (!station.value) {
                e.preventDefault();
                alert('Please select a return station');
                station.focus();
                return false;
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', setupReturnForm);

// Bicycle search with AJAX
function setupBicycleSearch() {
    const searchInput = document.getElementById('bicycle-search');
    if (searchInput) {
        let timeout = null;
        searchInput.addEventListener('input', function(e) {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                performSearch(e.target.value);
            }, 500);
        });
    }
}

async function performSearch(query) {
    if (query.length < 2) return;
    
    try {
        const response = await fetch(`/api/bicycles/?search=${encodeURIComponent(query)}`);
        const data = await response.json();
        displaySearchResults(data);
    } catch (error) {
        console.error('Search failed:', error);
    }
}

function displaySearchResults(results) {
    const container = document.getElementById('search-results');
    if (!container) return;
    
    if (results.length === 0) {
        container.innerHTML = '<p class="text-muted">No results found</p>';
        return;
    }
    
    container.innerHTML = results.map(bike => `
        <div class="search-result-item">
            <a href="/bicycles/${bike.slug}/">
                <strong>${bike.name}</strong> - ${bike.model}
                <span class="badge bg-${bike.status === 'available' ? 'success' : 'secondary'}">
                    ${bike.status}
                </span>
            </a>
        </div>
    `).join('');
}

// Confirm reservation
function confirmReservation(bicycleId) {
    if (confirm('Reserve this bicycle for 30 minutes?')) {
        document.getElementById(`reserve-form-${bicycleId}`).submit();
    }
}

// Export functions
window.RentalCostCalculator = RentalCostCalculator;
window.ReservationTimer = ReservationTimer;
window.confirmReservation = confirmReservation;