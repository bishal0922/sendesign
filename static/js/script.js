function refreshStatus() {
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            document.getElementById('cupsInHand').textContent = data.cupsInHand;
            document.getElementById('cleanCups').textContent = data.cleanCups;
            document.getElementById('usedCups').textContent = data.usedCups;
            document.getElementById('coffeeLeft').textContent = data.coffeeLeft + ' L';
            document.getElementById('batteryLevel').textContent = data.batteryLevel + '%';
            document.getElementById('timeTillRefill').textContent = data.timeTillRefill;
        })
        .catch(error => console.error('Error fetching status:', error));
}

document.addEventListener('DOMContentLoaded', function() {
    // setTimeout(refreshStatus, 20000); // Add a 2-second delay before executing refreshStatus
    
    // it executes immediately for some reason
    setInterval(refreshStatus, 2500); // Execute refreshStatus every 20 seconds
});


