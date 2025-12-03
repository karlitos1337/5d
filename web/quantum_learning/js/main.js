/**
 * Main Application Logic
 */

let currentInterest = null;

function selectInterest(interest) {
    // Highlight selected card
    document.querySelectorAll('.card').forEach(card => {
        card.classList.remove('selected');
    });
    
    const selectedCard = document.querySelector(`[data-interest="${interest}"]`);
    if (selectedCard) {
        selectedCard.classList.add('selected');
    }
    
    currentInterest = interest;
    
    // Start IMP tracking
    impTracker.start(interest);
    
    // Show stats section
    document.getElementById('stats').style.display = 'block';
    
    // Load corresponding lesson
    setTimeout(() => {
        window.location.href = `${interest}.html`;
    }, 1000);
    
    console.log(`🎮 Selected interest: ${interest}`);
}

// Track interactions (clicks, keyboard)
document.addEventListener('click', () => {
    if (currentInterest) {
        impTracker.trackInteraction();
    }
});

document.addEventListener('keydown', () => {
    if (currentInterest) {
        impTracker.trackInteraction();
    }
});

// Ask about sharing before leaving
window.addEventListener('beforeunload', (e) => {
    if (currentInterest && impTracker.stats.completion > 50) {
        const wantsToShare = confirm('Möchtest du dieses Experiment mit Freunden teilen? 🤝');
        impTracker.trackSocialIntent(wantsToShare);
        impTracker.stop();
    }
});

// Load history on page load
document.addEventListener('DOMContentLoaded', () => {
    const history = impTracker.getHistory();
    
    if (history.length > 0) {
        console.log('📚 IMP History:', history);
        
        // Show average IMP score
        const avgIMP = history.reduce((sum, item) => sum + item.imp_score, 0) / history.length;
        console.log(`📊 Average IMP Score: ${avgIMP.toFixed(3)}`);
    }
});
