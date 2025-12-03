/**
 * Quantum Minecraft - Superposition Visualization
 * Using p5.js for interactive graphics
 */

let world = [];
let gridSize = 10;
let cellSize = 50;
let measured = 0;
let diamonds = 0;

function setup() {
    let canvas = createCanvas(gridSize * cellSize, gridSize * cellSize);
    canvas.parent('canvas-container');
    
    // Initialize world
    resetWorld();
    
    // Track completion
    impTracker.trackCompletion(0);
}

function draw() {
    background(255);
    
    // Draw grid
    for (let x = 0; x < gridSize; x++) {
        for (let y = 0; y < gridSize; y++) {
            let block = world[x][y];
            
            // Position
            let px = x * cellSize;
            let py = y * cellSize;
            
            if (block.measured) {
                // Collapsed state
                if (block.hasDiamond) {
                    fill(64, 224, 208); // Diamond (cyan)
                    stroke(0, 255, 255);
                } else {
                    fill(128, 128, 128); // Stone (gray)
                    stroke(64, 64, 64);
                }
                strokeWeight(2);
                rect(px, py, cellSize, cellSize);
                
                // Draw symbol
                fill(255);
                textAlign(CENTER, CENTER);
                textSize(30);
                text(block.hasDiamond ? '💎' : '🪨', px + cellSize/2, py + cellSize/2);
                
            } else {
                // Superposition state (shimmering)
                let shimmer = sin(frameCount * 0.1 + x + y) * 0.3 + 0.7;
                fill(200, 150, 255, shimmer * 255);
                stroke(150, 100, 200);
                strokeWeight(1);
                rect(px, py, cellSize, cellSize);
                
                // Draw probability
                fill(255);
                textAlign(CENTER, CENTER);
                textSize(12);
                text('?', px + cellSize/2, py + cellSize/2);
            }
        }
    }
    
    // Draw grid lines
    stroke(200);
    strokeWeight(1);
    for (let i = 0; i <= gridSize; i++) {
        line(i * cellSize, 0, i * cellSize, height);
        line(0, i * cellSize, width, i * cellSize);
    }
}

function mousePressed() {
    // Get clicked block
    let x = floor(mouseX / cellSize);
    let y = floor(mouseY / cellSize);
    
    if (x >= 0 && x < gridSize && y >= 0 && y < gridSize) {
        measureBlock(x, y);
    }
}

function measureBlock(x, y) {
    let block = world[x][y];
    
    if (!block.measured) {
        // Quantum measurement!
        block.measured = true;
        block.hasDiamond = random() < 0.1; // 10% chance
        
        measured++;
        if (block.hasDiamond) {
            diamonds++;
        }
        
        // Update stats
        updateStats();
        
        // Track interaction
        impTracker.trackInteraction();
        
        // Track completion
        let completion = (measured / (gridSize * gridSize)) * 100;
        impTracker.trackCompletion(completion);
        
        console.log(`⛏️ Measured (${x},${y}): ${block.hasDiamond ? 'DIAMOND!' : 'Stone'}`);
    }
}

function resetWorld() {
    world = [];
    for (let x = 0; x < gridSize; x++) {
        world[x] = [];
        for (let y = 0; y < gridSize; y++) {
            world[x][y] = {
                measured: false,
                hasDiamond: false
            };
        }
    }
    
    measured = 0;
    diamonds = 0;
    updateStats();
    
    // Track retry
    if (measured > 0) {
        impTracker.trackRetry();
    }
    
    console.log('🔄 New world created!');
}

function measureAll() {
    for (let x = 0; x < gridSize; x++) {
        for (let y = 0; y < gridSize; y++) {
            if (!world[x][y].measured) {
                measureBlock(x, y);
            }
        }
    }
    
    console.log('💥 All blocks measured!');
}

function showHint() {
    alert('💡 Tipp: Quantenmechanik ist PROBABILISTISCH!\n\n' +
          'Auch wenn jeder Block 10% Diamant hat, bedeutet das NICHT,\n' +
          'dass genau 10 von 100 Blöcken Diamanten sind!\n\n' +
          'Es könnten auch 5 sein... oder 15... oder sogar 0!\n\n' +
          'Das ist wie beim Würfeln: Manchmal hast du Glück! 🎲');
    
    impTracker.trackHint();
}

function updateStats() {
    document.getElementById('measured-count').textContent = measured;
    document.getElementById('diamond-count').textContent = diamonds;
    
    let successRate = measured > 0 ? (diamonds / measured * 100).toFixed(1) : 0;
    document.getElementById('success-rate').textContent = successRate + '%';
}

// Start tracking
impTracker.start('minecraft');
