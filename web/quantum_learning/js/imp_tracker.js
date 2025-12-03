/**
 * IMP Tracker - Real-time 5D Intelligence Measurement
 * 
 * Tracks 5 dimensions:
 * - Autonomy (A): Did user choose freely? (0-1)
 * - Intrinsic Motivation (IM): Time spent / expected time (0-2)
 * - Resilience (R): Retries / errors (0-2)
 * - Social Participation (SP): Wants to share? (0-1)
 * - Authenticity (Au): Completed without hints? (0-1)
 * 
 * IMP Score = A × IM × R × SP × Au
 */

class IMPTracker {
    constructor() {
        this.dimensions = {
            autonomy: 0,
            motivation: 0,
            resilience: 0,
            social: 0,
            authenticity: 0
        };
        
        this.stats = {
            startTime: Date.now(),
            interactions: 0,
            retries: 0,
            hintsUsed: 0,
            completion: 0,
            selectedInterest: null
        };
        
        this.expectedTime = 600; // 10 minutes
        this.updateInterval = null;
    }
    
    start(interest) {
        this.stats.selectedInterest = interest;
        this.stats.startTime = Date.now();
        
        // Autonomy = 1.0 (user chose freely)
        this.dimensions.autonomy = 1.0;
        this.update();
        
        // Start tracking
        this.updateInterval = setInterval(() => this.trackMotivation(), 1000);
        
        console.log('🎯 IMP Tracking started for:', interest);
    }
    
    stop() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }
        
        // Calculate final scores
        this.calculateFinalScores();
        
        // Save to localStorage
        this.save();
        
        console.log('✅ IMP Tracking stopped. Final scores:', this.dimensions);
    }
    
    trackMotivation() {
        const timeSpent = (Date.now() - this.stats.startTime) / 1000; // seconds
        
        // IM = time spent / expected time (capped at 2.0 = super engaged!)
        this.dimensions.motivation = Math.min(timeSpent / this.expectedTime, 2.0);
        
        this.update();
    }
    
    trackInteraction() {
        this.stats.interactions++;
        this.update();
    }
    
    trackRetry() {
        this.stats.retries++;
        
        // R = 1 + (retries / 10) capped at 2.0 (resilient = trying again!)
        this.dimensions.resilience = Math.min(1 + this.stats.retries / 10, 2.0);
        
        this.update();
    }
    
    trackHint() {
        this.stats.hintsUsed++;
        
        // Au = 1 - (hints / 5) capped at 0 (authentic = no hints needed)
        this.dimensions.authenticity = Math.max(1 - this.stats.hintsUsed / 5, 0);
        
        this.update();
    }
    
    trackCompletion(percent) {
        this.stats.completion = percent;
        
        // Au increases with completion (even without hints)
        if (this.stats.hintsUsed === 0) {
            this.dimensions.authenticity = Math.min(percent / 100, 1.0);
        }
        
        this.update();
    }
    
    trackSocialIntent(wantsToShare) {
        // SP = 1.0 if user wants to share, 0.5 otherwise
        this.dimensions.social = wantsToShare ? 1.0 : 0.5;
        
        this.update();
    }
    
    calculateFinalScores() {
        // Ensure Resilience has minimum of 1.0 (completed = resilient)
        if (this.dimensions.resilience === 0) {
            this.dimensions.resilience = 1.0;
        }
        
        // Ensure Social has minimum of 0.5 (participated = social)
        if (this.dimensions.social === 0) {
            this.dimensions.social = 0.5;
        }
        
        // Ensure Authenticity has minimum based on completion
        if (this.dimensions.authenticity === 0) {
            this.dimensions.authenticity = Math.min(this.stats.completion / 100, 1.0);
        }
    }
    
    getIMPScore() {
        const { autonomy, motivation, resilience, social, authenticity } = this.dimensions;
        
        // IMP = A × IM × R × SP × Au (multiplicative!)
        return autonomy * motivation * resilience * social * authenticity;
    }
    
    update() {
        // Update UI
        this.updateBars();
        this.updateStats();
        
        // Log to console (for debugging)
        const imp = this.getIMPScore();
        console.log(`📊 IMP: ${imp.toFixed(3)} | A:${this.dimensions.autonomy.toFixed(2)} IM:${this.dimensions.motivation.toFixed(2)} R:${this.dimensions.resilience.toFixed(2)} SP:${this.dimensions.social.toFixed(2)} Au:${this.dimensions.authenticity.toFixed(2)}`);
    }
    
    updateBars() {
        const dims = [
            { id: 'a', value: this.dimensions.autonomy, max: 1 },
            { id: 'im', value: this.dimensions.motivation, max: 2 },
            { id: 'r', value: this.dimensions.resilience, max: 2 },
            { id: 'sp', value: this.dimensions.social, max: 1 },
            { id: 'au', value: this.dimensions.authenticity, max: 1 }
        ];
        
        dims.forEach(dim => {
            const percent = (dim.value / dim.max) * 100;
            const bar = document.getElementById(`bar-${dim.id}`);
            const score = document.getElementById(`score-${dim.id}`);
            
            if (bar) bar.style.width = `${percent}%`;
            if (score) score.textContent = dim.value.toFixed(2);
        });
        
        // Update IMP Score
        const imp = this.getIMPScore();
        const impBar = document.getElementById('bar-imp');
        const impScore = document.getElementById('score-imp');
        
        if (impBar) impBar.style.width = `${Math.min(imp * 100, 100)}%`;
        if (impScore) impScore.textContent = imp.toFixed(3);
    }
    
    updateStats() {
        const timeSpent = Math.floor((Date.now() - this.stats.startTime) / 1000);
        const minutes = Math.floor(timeSpent / 60);
        const seconds = timeSpent % 60;
        
        const timeEl = document.getElementById('time-spent');
        const interactionsEl = document.getElementById('interactions');
        const retriesEl = document.getElementById('retries');
        const completionEl = document.getElementById('completion');
        
        if (timeEl) timeEl.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        if (interactionsEl) interactionsEl.textContent = this.stats.interactions;
        if (retriesEl) retriesEl.textContent = this.stats.retries;
        if (completionEl) completionEl.textContent = `${this.stats.completion}%`;
    }
    
    save() {
        const data = {
            timestamp: new Date().toISOString(),
            interest: this.stats.selectedInterest,
            dimensions: this.dimensions,
            imp_score: this.getIMPScore(),
            stats: this.stats
        };
        
        // Save to localStorage
        const history = JSON.parse(localStorage.getItem('imp_history') || '[]');
        history.push(data);
        localStorage.setItem('imp_history', JSON.stringify(history));
        
        console.log('💾 Saved to localStorage:', data);
    }
    
    getHistory() {
        return JSON.parse(localStorage.getItem('imp_history') || '[]');
    }
}

// Global instance
const impTracker = new IMPTracker();
