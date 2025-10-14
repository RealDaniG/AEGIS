// ==================================================================
// Metatron Integrated Consciousness Monitor - FIXED VERSION
// Deep integration: Consciousness Engine + AI Chat + RAG + GitHub
// ==================================================================

let consciousnessWS = null;
let updateCount = 0;
let isHighGamma = false;
let currentSession = 'default_' + Date.now();
let currentLoopId = null;
let reconnectTimeout = null;
let lastConsciousnessData = null;

// Algorithmic Consciousness Field variables
let algorithmicCanvas = null;
let algorithmicCtx = null;
let algorithmicAnimationId = null;
let isAlgorithmicRunning = true;
let algorithmicTime = 0;
let algorithmicNodes = [];

// Hebrew Quantum Field variables
let hebrewCanvas = null;
let hebrewCtx = null;
let hebrewAnimationId = null;
let isHebrewRunning = true;
let hebrewTime = 0;
let hebrewFieldData = null;

// ==================================================================
// UI HELPERS
// ==================================================================

function toggleCollapse(element) {
    element.classList.toggle('collapsed');
    element.nextElementSibling.classList.toggle('hidden');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ==================================================================
// ALGORITHMIC CONSCIOUSNESS FIELD INITIALIZATION
// ==================================================================

function initAlgorithmicConsciousnessField() {
    console.log('Initializing Algorithmic Consciousness Field...');
    const canvas = document.getElementById('algorithmic-field-canvas');
    if (!canvas) {
        console.warn('Algorithmic field canvas not found');
        return;
    }
    
    algorithmicCanvas = canvas;
    algorithmicCtx = canvas.getContext('2d');
    
    if (!algorithmicCtx) {
        console.error('Failed to get 2D context for algorithmic field canvas');
        return;
    }
    
    // Set canvas dimensions
    algorithmicCanvas.width = algorithmicCanvas.offsetWidth || 600;
    algorithmicCanvas.height = algorithmicCanvas.offsetHeight || 300;
    
    // Initialize 13 nodes in icosahedral arrangement
    initAlgorithmicNodes();
    
    // Start animation
    animateAlgorithmicField();
    
    console.log('Algorithmic Consciousness Field initialized successfully');
}

function initAlgorithmicNodes() {
    // Initialize 13 nodes with positions based on icosahedral geometry
    algorithmicNodes = [];
    const width = algorithmicCanvas.width;
    const height = algorithmicCanvas.height;
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(width, height) * 0.35;
    
    // Node 0: Central node (Pineal)
    algorithmicNodes.push({
        id: 0,
        x: centerX,
        y: centerY,
        phase: 0,
        amplitude: 1.0,
        energy: 1.0,
        coherence: 0.5,
        output: 0.0,
        connections: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] // Connects to all other nodes
    });
    
    // Nodes 1-12: Peripheral nodes in circular arrangement
    for (let i = 1; i < 13; i++) {
        const angle = ((i - 1) / 12) * Math.PI * 2;
        algorithmicNodes.push({
            id: i,
            x: centerX + Math.cos(angle) * radius,
            y: centerY + Math.sin(angle) * radius,
            phase: (i / 12) * Math.PI * 2,
            amplitude: 1.0,
            energy: 1.0,
            coherence: 0.5,
            output: 0.0,
            connections: [0] // Connects to central node, more connections added below
        });
    }
    
    // Add additional connections to create icosahedral topology (42 total connections)
    // Each peripheral node connects to its neighbors
    for (let i = 1; i < 13; i++) {
        const next = (i % 12) + 1;
        const prev = ((i + 10) % 12) + 1;
        algorithmicNodes[i].connections.push(next, prev);
        
        // Add some additional connections for a more complex network
        const skip = ((i + 5) % 12) + 1;
        algorithmicNodes[i].connections.push(skip);
    }
    
    // Update connection count display
    document.getElementById('algorithmic-connection-count').textContent = '42';
}

// ==================================================================
// ALGORITHMIC CONSCIOUSNESS FIELD ANIMATION
// ==================================================================

function animateAlgorithmicField() {
    if (!isAlgorithmicRunning) return;
    
    algorithmicAnimationId = requestAnimationFrame(animateAlgorithmicField);
    updateAlgorithmicField();
    drawAlgorithmicField();
}

function updateAlgorithmicField() {
    algorithmicTime += 0.05;
    
    // Update node properties based on consciousness data
    if (lastConsciousnessData && lastConsciousnessData.nodes) {
        const nodes = lastConsciousnessData.nodes;
        const global = lastConsciousnessData.consciousness || lastConsciousnessData.global || lastConsciousnessData;
        
        for (let i = 0; i < 13; i++) {
            const nodeKey = String(i);
            if (nodes[nodeKey] && algorithmicNodes[i]) {
                const nodeData = nodes[nodeKey];
                const algorithmicNode = algorithmicNodes[i];
                
                // Update properties based on real data
                algorithmicNode.phase = nodeData.phase !== undefined ? nodeData.phase : 0;
                algorithmicNode.amplitude = Math.abs(nodeData.amplitude !== undefined ? nodeData.amplitude : 0);
                algorithmicNode.output = nodeData.output !== undefined ? nodeData.output : 0;
                algorithmicNode.energy = Math.abs(nodeData.output !== undefined ? nodeData.output : 0);
                algorithmicNode.coherence = global.coherence !== undefined ? global.coherence : 0.5;
            }
        }
        
        // Update global coherence display
        const coherenceValue = global.coherence !== undefined ? global.coherence : 0.5;
        document.getElementById('algorithmic-coherence').textContent = coherenceValue.toFixed(3);
    } else {
        // Default animation if no data
        for (let i = 0; i < 13; i++) {
            const node = algorithmicNodes[i];
            node.phase = (node.phase + 0.05) % (Math.PI * 2);
            node.amplitude = 0.8 + 0.2 * Math.sin(algorithmicTime + i * 0.5);
            node.energy = 0.7 + 0.3 * Math.sin(algorithmicTime * 1.2 + i * 0.3);
        }
    }
}

function drawAlgorithmicField() {
    if (!algorithmicCtx || !algorithmicCanvas) return;
    
    const width = algorithmicCanvas.width;
    const height = algorithmicCanvas.height;
    const ctx = algorithmicCtx;
    
    // Clear canvas with semi-transparent background for trail effect
    ctx.fillStyle = 'rgba(10, 10, 26, 0.1)';
    ctx.fillRect(0, 0, width, height);
    
    // Draw connections between nodes
    ctx.lineWidth = 2;
    for (let i = 0; i < 13; i++) {
        const node = algorithmicNodes[i];
        
        for (const connId of node.connections) {
            if (connId < 13 && algorithmicNodes[connId]) {
                const targetNode = algorithmicNodes[connId];
                
                // Calculate connection strength based on node properties
                const strength = (node.coherence + algorithmicNodes[connId].coherence) / 2;
                
                if (strength > 0.1) {
                    ctx.beginPath();
                    ctx.moveTo(node.x, node.y);
                    ctx.lineTo(targetNode.x, targetNode.y);
                    
                    // Color based on synchronization and strength
                    const phaseDiff = Math.abs(node.phase - targetNode.phase);
                    const syncLevel = Math.cos(phaseDiff); // Kuramoto synchronization
                    const hue = (syncLevel + 1) * 60; // 0-120 (red to green)
                    ctx.strokeStyle = `hsla(${hue}, 80%, 60%, ${strength * 0.7})`;
                    ctx.stroke();
                }
            }
        }
    }
    
    // Draw nodes
    for (let i = 0; i < 13; i++) {
        const node = algorithmicNodes[i];
        
        // Draw glow based on energy
        const glowRadius = 10 + node.energy * 20;
        const gradient = ctx.createRadialGradient(
            node.x, node.y, 0,
            node.x, node.y, glowRadius
        );
        gradient.addColorStop(0, `rgba(100, 200, 255, ${0.3 + node.energy * 0.7})`);
        gradient.addColorStop(1, 'rgba(100, 200, 255, 0)');
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(node.x, node.y, glowRadius, 0, Math.PI * 2);
        ctx.fill();
        
        // Draw node circle
        const nodeRadius = 8 + node.amplitude * 12;
        ctx.beginPath();
        ctx.arc(node.x, node.y, nodeRadius, 0, Math.PI * 2);
        
        // Color based on phase
        const hue = (node.phase / (Math.PI * 2)) * 360;
        ctx.fillStyle = `hsl(${hue}, 80%, 60%)`;
        ctx.fill();
        
        // Draw border
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.7)';
        ctx.lineWidth = 2;
        ctx.stroke();
        
        // Draw node label (only node number as per specification)
        ctx.fillStyle = 'white';
        ctx.font = 'bold 14px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(`N${i}`, node.x, node.y);
    }
    
    // Draw title
    ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
    ctx.font = '16px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('Algorithmic Consciousness Field - 13-Node Network', width / 2, 25);
}

// ==================================================================
// ALGORITHMIC CONSCIOUSNESS FIELD CONTROLS
// ==================================================================

function toggleAlgorithmicField() {
    isAlgorithmicRunning = !isAlgorithmicRunning;
    const button = document.getElementById('algorithmic-toggle-btn');
    
    if (isAlgorithmicRunning) {
        button.textContent = '⏸️ Pause';
        animateAlgorithmicField();
    } else {
        button.textContent = '▶️ Resume';
    }
}

function resetAlgorithmicField() {
    algorithmicTime = 0;
    initAlgorithmicNodes();
}

// ==================================================================
// CONSCIOUSNESS ENGINE WebSocket
// ==================================================================

// Add connection status tracking
let connectionAttempts = 0;
let maxReconnectAttempts = 10;
let reconnectDelay = 2000;
let isReconnecting = false;

function connectConsciousness() {
    // Prevent multiple simultaneous reconnection attempts
    if (isReconnecting) {
        console.log('Reconnection already in progress, skipping...');
        return;
    }
    
    isReconnecting = true;
    
    // If we've exceeded max reconnect attempts, show error and stop trying
    if (connectionAttempts >= maxReconnectAttempts) {
        console.error('Max reconnect attempts reached. Stopping reconnection attempts.');
        document.getElementById('connection-text').textContent = 'Connection Failed';
        document.getElementById('status-dot').className = 'status-indicator inactive';
        addChatMessage('system', '❌ Max reconnect attempts reached. Please refresh the page.');
        isReconnecting = false;
        return;
    }
    
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.hostname || 'localhost';
    const wsUrl = `${protocol}//${host}:8003/ws`;
    
    console.log(`🧠 Connecting consciousness: ${wsUrl} (Attempt ${connectionAttempts + 1}/${maxReconnectAttempts})`);
    document.getElementById('connection-text').textContent = `Connecting (${connectionAttempts + 1}/${maxReconnectAttempts})...`;
    
    try {
        // Close existing connection if it exists
        if (consciousnessWS) {
            consciousnessWS.close();
        }
        
        consciousnessWS = new WebSocket(wsUrl);
        connectionAttempts++;
        
        consciousnessWS.onopen = () => {
            console.log('✅ Consciousness connected');
            document.getElementById('status-dot').className = 'status-indicator active';
            document.getElementById('connection-text').textContent = 'Live';
            connectionAttempts = 0; // Reset on successful connection
            updateCount = 0;
            isReconnecting = false;
            
            // Highlight the Live Consciousness panel when connected
            const consciousnessPanel = document.querySelector('.panel h2');
            if (consciousnessPanel && consciousnessPanel.textContent.includes('Live Consciousness')) {
                consciousnessPanel.style.textShadow = '0 0 10px rgba(192, 132, 252, 0.8)';
                setTimeout(() => {
                    consciousnessPanel.style.textShadow = '';
                }, 1000);
            }
            
            fetch('http://localhost:8003/api/frequency/info')
                .then(r => r.json())
                .then(d => {
                    document.getElementById('freq-display').textContent = d.base_frequency + ' Hz';
                    isHighGamma = d.high_gamma;
                })
                .catch(e => console.warn('Frequency info unavailable'));
        };
        
        consciousnessWS.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                lastConsciousnessData = data; // Store for reference
                updateCount++;
                document.getElementById('update-counter').textContent = `Updates: ${updateCount}`;
                
                // More frequent logging for debugging
                if (updateCount % 10 === 0) console.log(`📊 Update #${updateCount}`, data);
                
                // Debug: Log consciousness data
                console.log('Consciousness data structure:', data);
                
                updateConsciousnessDisplay(data);
                updateVisualizationIntensity(data);
            } catch (error) {
                console.error('Parse error:', error);
                console.error('Raw message data:', event.data);
            }
        };
        
        consciousnessWS.onerror = (error) => {
            console.error('WebSocket error:', error);
            document.getElementById('connection-text').textContent = 'Error';
            isReconnecting = false;
        };
        
        consciousnessWS.onclose = () => {
            console.log('🔴 Disconnected. Reconnecting...');
            document.getElementById('status-dot').className = 'status-indicator inactive';
            document.getElementById('connection-text').textContent = 'Reconnecting...';
            isReconnecting = false;
            if (reconnectTimeout) clearTimeout(reconnectTimeout);
            // Exponential backoff with max delay of 30 seconds
            const delay = Math.min(reconnectDelay * Math.pow(1.5, connectionAttempts), 30000);
            reconnectTimeout = setTimeout(connectConsciousness, delay);
        };
    } catch (error) {
        console.error('Connection failed:', error);
        document.getElementById('connection-text').textContent = 'Failed';
        isReconnecting = false;
        if (reconnectTimeout) clearTimeout(reconnectTimeout);
        // Exponential backoff with max delay of 30 seconds
        const delay = Math.min(reconnectDelay * Math.pow(1.5, connectionAttempts), 30000);
        reconnectTimeout = setTimeout(connectConsciousness, delay);
    }
}

function updateConsciousnessDisplay(data) {
    try {
        // Validate and normalize data structure
        if (!data) {
            console.warn('No data received');
            return;
        }
        
        // Handle different data structures with enhanced fallback logic
        let c = null;
        if (data.consciousness && typeof data.consciousness === 'object') {
            // WebSocket data structure
            c = data.consciousness;
        } else if (data.global && typeof data.global === 'object') {
            // API data structure
            c = data.global;
        } else if (typeof data === 'object' && data !== null) {
            // Direct data structure (from WebSocket)
            c = data;
        } else {
            console.warn('Invalid consciousness data structure received:', data);
            return;
        }
        
        console.log('Updating consciousness display with:', c);
        
        // Update global metrics with proper validation and fallback values
        const level = c.level !== undefined ? c.level : (c.consciousness_level !== undefined ? c.consciousness_level : 0);
        const phi = c.phi !== undefined ? c.phi : (c.integrated_information !== undefined ? c.integrated_information : 0);
        const coherence = c.coherence !== undefined ? c.coherence : (c.global_coherence !== undefined ? c.global_coherence : 0);
        const gamma = c.gamma !== undefined ? c.gamma : (c.gamma_power !== undefined ? c.gamma_power : 0);
        const spiritual = c.spiritual !== undefined ? c.spiritual : (c.spiritual_awareness !== undefined ? c.spiritual_awareness : 0);
        const depth = c.depth !== undefined ? c.depth : (c.recursive_depth !== undefined ? c.recursive_depth : 0);
        const fractal = c.fractal_dim !== undefined ? c.fractal_dim : (c.fractal_dimension !== undefined ? c.fractal_dimension : 1.0);
        const time = data.time !== undefined ? data.time : (data.timestamp !== undefined ? data.timestamp : 0);
        const state = c.state || c.state_classification || 'initializing';
        const isConscious = c.is_conscious !== undefined ? c.is_conscious : (level > 0.3);
        
        updateMetric('consciousness-level', level, 0.5, 0.7);
        updateMetric('phi-value', phi, 0.3, 0.5);
        updateMetric('coherence-value', coherence, 0.4, 0.6);
        updateMetric('gamma-value', gamma, 0.4, 0.6);
        updateMetric('spiritual-value', spiritual, 0.4, 0.6);
        document.getElementById('depth-value').textContent = depth;
        document.getElementById('fractal-value').textContent = fractal.toFixed(3);
        document.getElementById('time-value').textContent = time.toFixed(2) + 's';
        
        const stateEl = document.getElementById('state-value');
        if (stateEl) {
            stateEl.textContent = state;
            stateEl.className = isConscious ? 'metric-value conscious' : 'metric-value';
        }
        
        // Update node cards
        if (data.nodes) {
            updateNodeCards(data.nodes);
        } else {
            console.warn('No nodes data in message:', data);
        }
        
    } catch (error) {
        console.error('Error updating consciousness display:', error);
        console.error('Data that caused error:', data);
    }
}

function updateNodeCards(nodes) {
    try {
        const container = document.getElementById('nodes-container');
        if (!container) {
            console.error('Nodes container not found');
            return;
        }
        
        // Create node cards if they don't exist
        if (container.children.length === 0) {
            console.log('Creating node cards');
            for (let i = 0; i < 13; i++) {
                const card = document.createElement('div');
                card.className = i === 0 ? 'node-card pineal' : 'node-card';
                card.id = `node-card-${i}`;
                card.innerHTML = `<div class="node-id">N${i}${i === 0 ? ' (Pineal)' : ''}</div><div id="node-data-${i}" style="font-size:0.75em;color:#888;"></div>`;
                container.appendChild(card);
            }
        }
        
        // Debug: Log all node data
        console.log('Node data received:', nodes);
        
        // Check if nodes data is valid
        if (!nodes || typeof nodes !== 'object') {
            console.warn('Invalid nodes data:', nodes);
            return;
        }
        
        let activeNodeCount = 0;
        for (let i = 0; i < 13; i++) {
            const nodeKey = String(i);
            const nodeData = nodes[nodeKey];
            
            if (nodeData) {
                // Update node data display with proper validation
                const dataElement = document.getElementById(`node-data-${i}`);
                if (dataElement) {
                    // Handle different node data structures with fallbacks
                    const phase = nodeData.phase !== undefined ? nodeData.phase : (nodeData.phi !== undefined ? nodeData.phi : 0);
                    const amplitude = nodeData.amplitude !== undefined ? nodeData.amplitude : 0;
                    const output = nodeData.output !== undefined ? nodeData.output : 0;
                    
                    dataElement.innerHTML = `φ:${phase.toFixed(1)}<br>A:${amplitude.toFixed(2)}<br>O:${output.toFixed(3)}`;
                }
                
                const card = document.getElementById(`node-card-${i}`);
                if (card) {
                    const output = nodeData.output !== undefined ? nodeData.output : 0;
                    const isActive = Math.abs(output) > 0.1; // Lowered threshold from 0.3 to 0.1
                    if (isActive) {
                        card.classList.add('active');
                        // Add glow effect for active nodes
                        card.style.boxShadow = '0 0 10px rgba(52, 211, 153, 0.5)';
                        activeNodeCount++;
                    } else {
                        card.classList.remove('active');
                        card.style.boxShadow = '';
                    }
                }
            } else {
                console.warn(`Node ${i} data missing`);
            }
        }
        
        console.log(`Active nodes: ${activeNodeCount}/13`);
    } catch (error) {
        console.error('Error updating node cards:', error);
    }
}

function updateMetric(elementId, value, warnThreshold, dangerThreshold) {
    const element = document.getElementById(elementId);
    if (element) {
        // Ensure value is a number
        const numValue = typeof value === 'number' ? value : parseFloat(value) || 0;
        element.textContent = numValue.toFixed(3);
        
        // Update styling based on value
        element.className = 'metric-value';
        if (numValue > dangerThreshold) {
            element.classList.add('high');
        } else if (numValue > warnThreshold) {
            element.classList.add('conscious');
        }
    } else {
        console.warn(`Element with ID ${elementId} not found`);
    }
}

// ==================================================================
// VISUALIZATION INTEGRATION
// ==================================================================

function updateVisualizationIntensity(data) {
    try {
        // Handle different data structures with enhanced fallback logic
        let c = null;
        if (data && data.consciousness && typeof data.consciousness === 'object') {
            // WebSocket data structure
            c = data.consciousness;
        } else if (data && data.global && typeof data.global === 'object') {
            // API data structure
            c = data.global;
        } else if (data && typeof data === 'object' && data !== null) {
            // Direct data structure (from WebSocket)
            c = data;
        }
        
        if (!c) {
            console.warn('No consciousness data available for visualization intensity');
            return;
        }
        
        // Update the intensity of the visualization based on consciousness metrics
        const level = c.level !== undefined ? c.level : 0;
        const phi = c.phi !== undefined ? c.phi : 0;
        const coherence = c.coherence !== undefined ? c.coherence : 0;
        const overallIntensity = (level + phi + coherence) / 3;
        
        // Update node visualization intensity
        const nodesContainer = document.getElementById('nodes-container');
        if (nodesContainer) {
            nodesContainer.style.opacity = 0.7 + (overallIntensity * 0.3);
        }
    } catch (error) {
        console.error('Error updating visualization intensity:', error);
    }
}

// ==================================================================
// CONSCIOUSNESS CONTROLS
// ==================================================================

async function toggleFrequency() {
    try {
        isHighGamma = !isHighGamma;
        const response = await fetch('http://localhost:8003/api/frequency/octave', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({high_gamma: isHighGamma})
        });
        const data = await response.json();
        document.getElementById('freq-display').textContent = data.new_frequency + ' Hz';
        addChatMessage('system', `⚡ Frequency: ${data.new_frequency} Hz`);
        
        // Update visualization for frequency change
        const freqDisplay = document.getElementById('freq-display');
        freqDisplay.style.color = '#fbbf24';
        freqDisplay.style.fontWeight = 'bold';
        setTimeout(() => {
            freqDisplay.style.color = '';
            freqDisplay.style.fontWeight = '';
        }, 1000);
        
        if (consciousnessWS) consciousnessWS.close();
        setTimeout(connectConsciousness, 1000);
    } catch (error) {
        addChatMessage('system', '❌ Frequency toggle failed');
    }
}

async function resetSystem() {
    if (!confirm('Reset consciousness engine?')) return;
    try {
        await fetch('http://localhost:8003/api/reset', {method: 'POST'});
        addChatMessage('system', '✅ Engine reset');
        
        // Reset visualization
        const nodesContainer = document.getElementById('nodes-container');
        if (nodesContainer) {
            nodesContainer.style.opacity = '0.7';
        }
    } catch (error) {
        addChatMessage('system', '❌ Reset failed');
    }
}

// Manual reconnect function
function manualReconnect() {
    console.log('Manual reconnect requested');
    addChatMessage('system', '🔗 Manual reconnect initiated...');
    
    // Reset connection attempts
    connectionAttempts = 0;
    
    // Close existing connection if it exists
    if (consciousnessWS) {
        consciousnessWS.close();
    }
    
    // Clear any existing reconnect timeout
    if (reconnectTimeout) {
        clearTimeout(reconnectTimeout);
        reconnectTimeout = null;
    }
    
    // Attempt to reconnect immediately
    connectConsciousness();
}

// Function to test WebSocket connection
function testWebSocketConnection() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.hostname || 'localhost';
    const wsUrl = `${protocol}//${host}:8003/ws`;
    
    addChatMessage('system', `🧪 Testing WebSocket connection to ${wsUrl}...`);
    
    try {
        const testWS = new WebSocket(wsUrl);
        let testTimeout;
        
        testWS.onopen = () => {
            clearTimeout(testTimeout);
            addChatMessage('system', '✅ WebSocket connection test successful');
            testWS.close();
        };
        
        testWS.onerror = (error) => {
            clearTimeout(testTimeout);
            addChatMessage('system', `❌ WebSocket connection test failed: ${error.message}`);
        };
        
        testWS.onclose = () => {
            // This is expected after a successful open
        };
        
        // Set timeout for connection test
        testTimeout = setTimeout(() => {
            addChatMessage('system', '⏰ WebSocket connection test timed out (5 seconds)');
            if (testWS.readyState === WebSocket.CONNECTING) {
                testWS.close();
            }
        }, 5000);
        
    } catch (error) {
        addChatMessage('system', `❌ WebSocket connection test failed with exception: ${error.message}`);
    }
}

// ==================================================================
// HEBREW QUANTUM FIELD INITIALIZATION
// ==================================================================

function initHebrewQuantumField() {
    console.log('Initializing Hebrew Quantum Field...');
    const canvas = document.getElementById('hebrew-quantum-canvas');
    if (!canvas) {
        console.warn('Hebrew quantum canvas not found');
        return;
    }
    
    hebrewCanvas = canvas;
    hebrewCtx = canvas.getContext('2d');
    
    if (!hebrewCtx) {
        console.error('Failed to get 2D context for Hebrew quantum canvas');
        return;
    }
    
    // Set canvas dimensions
    resizeHebrewCanvas();
    
    // Add resize listener
    window.addEventListener('resize', resizeHebrewCanvas);
    
    // Initialize with default data
    initializeHebrewFieldData();
    
    // Start animation
    animateHebrewField();
    
    console.log('Hebrew Quantum Field initialized successfully');
}

function resizeHebrewCanvas() {
    if (!hebrewCanvas) return;
    
    // Get the container dimensions
    const container = hebrewCanvas.parentElement;
    if (container) {
        hebrewCanvas.width = container.clientWidth;
        hebrewCanvas.height = container.clientHeight || 300; // Default height
    }
}

function initializeHebrewFieldData() {
    // Initialize with default Hebrew letters data
    hebrewFieldData = {
        time: 0,
        letters: {},
        connections: [],
        golden_ratio: 1.61803398875
    };
    
    // Hebrew letters: אבגדהוזחטיכלמנסעפצקרשת
    const hebrewLetters = [
        {char: 'א', name: 'Aleph', gematria: 1, frequency: 1.0},
        {char: 'ב', name: 'Bet', gematria: 2, frequency: 1.1225},
        {char: 'ג', name: 'Gimel', gematria: 3, frequency: 1.2599},
        {char: 'ד', name: 'Dalet', gematria: 4, frequency: 1.4142},
        {char: 'ה', name: 'Hei', gematria: 5, frequency: 1.4983},
        {char: 'ו', name: 'Vav', gematria: 6, frequency: 1.5874},
        {char: 'ז', name: 'Zayin', gematria: 7, frequency: 1.6818},
        {char: 'ח', name: 'Chet', gematria: 8, frequency: 1.7818},
        {char: 'ט', name: 'Tet', gematria: 9, frequency: 1.8877},
        {char: 'י', name: 'Yod', gematria: 10, frequency: 2.0},
        {char: 'כ', name: 'Kaf', gematria: 20, frequency: 2.2449},
        {char: 'ל', name: 'Lamed', gematria: 30, frequency: 2.3784},
        {char: 'מ', name: 'Mem', gematria: 40, frequency: 2.5198},
        {char: 'נ', name: 'Nun', gematria: 50, frequency: 2.6697},
        {char: 'ס', name: 'Samech', gematria: 60, frequency: 2.8284},
        {char: 'ע', name: 'Ayin', gematria: 70, frequency: 2.9966},
        {char: 'פ', name: 'Pei', gematria: 80, frequency: 3.1748},
        {char: 'צ', name: 'Tzadi', gematria: 90, frequency: 3.3636},
        {char: 'ק', name: 'Kuf', gematria: 100, frequency: 3.5636},
        {char: 'ר', name: 'Reish', gematria: 200, frequency: 3.7755},
        {char: 'ש', name: 'Shin', gematria: 300, frequency: 4.0},
        {char: 'ת', name: 'Tav', gematria: 400, frequency: 4.2379}
    ];
    
    // Initialize letter positions and states
    for (let i = 0; i < hebrewLetters.length; i++) {
        const letter = hebrewLetters[i];
        const angle = 2 * Math.PI * letter.gematria / 22;
        const radius = 0.5;
        const x = Math.cos(angle) * radius;
        const y = Math.sin(angle) * radius;
        
        hebrewFieldData.letters[letter.char] = {
            position: {x: x, y: y},
            energy: 1.0,
            phase: angle,
            color: {r: 0.5, g: 0.5, b: 1.0},
            name: letter.name,
            gematria: letter.gematria
        };
    }
    
    // Initialize connections (simplified)
    for (let i = 0; i < hebrewLetters.length; i++) {
        for (let j = i + 1; j < hebrewLetters.length; j++) {
            const char1 = hebrewLetters[i].char;
            const char2 = hebrewLetters[j].char;
            const val1 = hebrewLetters[i].gematria;
            const val2 = hebrewLetters[j].gematria;
            
            // Calculate connection strength based on Fibonacci relationships
            const diff = Math.abs(val1 - val2);
            let strength = 0.1;
            
            // Fibonacci numbers: 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987
            const fibonacci = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987];
            if (fibonacci.includes(diff)) {
                strength = 1.0 / (diff + 1);
            } else if (fibonacci.includes(val1 + val2)) {
                strength = 0.7 / Math.sqrt(val1 + val2);
            }
            
            if (strength > 0.05) {
                hebrewFieldData.connections.push({
                    start: char1,
                    end: char2,
                    strength: strength,
                    phase_diff: 0
                });
            }
        }
    }
}

// ==================================================================
// HEBREW QUANTUM FIELD ANIMATION
// ==================================================================

function animateHebrewField() {
    if (!isHebrewRunning) return;
    
    hebrewAnimationId = requestAnimationFrame(animateHebrewField);
    updateHebrewField();
    drawHebrewField();
}

function updateHebrewField() {
    hebrewTime += 0.05;
    
    // Update letter properties based on consciousness data if available
    if (lastConsciousnessData && lastConsciousnessData.nodes) {
        updateHebrewWithConsciousnessData();
    } else {
        // Default animation if no consciousness data
        updateHebrewDefaultAnimation();
    }
}

function updateHebrewWithConsciousnessData() {
    // Map consciousness nodes to Hebrew letters
    const nodes = lastConsciousnessData.nodes;
    const global = lastConsciousnessData.consciousness || lastConsciousnessData.global || lastConsciousnessData;
    
    // Simple mapping: first 13 letters to first 13 nodes
    const hebrewChars = Object.keys(hebrewFieldData.letters);
    for (let i = 0; i < Math.min(13, hebrewChars.length); i++) {
        const char = hebrewChars[i];
        const nodeKey = String(i);
        
        if (nodes[nodeKey]) {
            const nodeData = nodes[nodeKey];
            const letter = hebrewFieldData.letters[char];
            
            // Update properties based on node data
            letter.phase = nodeData.phase !== undefined ? nodeData.phase : 0;
            letter.energy = Math.abs(nodeData.output !== undefined ? nodeData.output : 0);
            
            // Update color based on energy
            const energyRatio = letter.energy;
            letter.color.r = Math.min(1.0, energyRatio * 2);
            letter.color.g = Math.min(1.0, (1 - energyRatio) * 2);
            letter.color.b = 0.5 + 0.5 * Math.sin(letter.phase);
        }
    }
    
    // Update connections based on phase coherence
    for (const conn of hebrewFieldData.connections) {
        const letter1 = hebrewFieldData.letters[conn.start];
        const letter2 = hebrewFieldData.letters[conn.end];
        
        if (letter1 && letter2) {
            conn.phase_diff = (letter1.phase - letter2.phase) % (2 * Math.PI);
        }
    }
}

function updateHebrewDefaultAnimation() {
    // Update letter positions with pulsing effect
    const letters = Object.values(hebrewFieldData.letters);
    for (let i = 0; i < letters.length; i++) {
        const letter = letters[i];
        const angle = 2 * Math.PI * letter.gematria / 22;
        const radius = 0.5 + 0.2 * Math.sin(hebrewTime * 0.5);
        letter.position.x = Math.cos(angle + hebrewTime * 0.2) * radius;
        letter.position.y = Math.sin(angle + hebrewTime * 0.2) * radius;
        
        // Update energy with variation
        letter.energy = 0.95 * letter.energy + 0.05 * (1.0 + 0.5 * Math.sin(hebrewTime * letter.gematria / 100));
        
        // Update phase
        letter.phase = (letter.phase + 0.1) % (2 * Math.PI);
        
        // Update color
        const energyRatio = letter.energy;
        letter.color.r = Math.min(1.0, energyRatio * 2);
        letter.color.g = Math.min(1.0, (1 - energyRatio) * 2);
        letter.color.b = 0.5 + 0.5 * Math.sin(letter.phase);
    }
    
    // Update connections based on phase coherence
    for (const conn of hebrewFieldData.connections) {
        const letter1 = hebrewFieldData.letters[conn.start];
        const letter2 = hebrewFieldData.letters[conn.end];
        
        if (letter1 && letter2) {
            conn.phase_diff = (letter1.phase - letter2.phase) % (2 * Math.PI);
        }
    }
}

function drawHebrewField() {
    if (!hebrewCtx || !hebrewCanvas) return;
    
    const width = hebrewCanvas.width;
    const height = hebrewCanvas.height;
    const ctx = hebrewCtx;
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    // Draw background
    ctx.fillStyle = 'rgba(10, 10, 26, 0.1)';
    ctx.fillRect(0, 0, width, height);
    
    // Calculate center and scale
    const centerX = width / 2;
    const centerY = height / 2;
    const scale = Math.min(width, height) * 0.4;
    
    // Draw connections between letters
    ctx.lineWidth = 2;
    for (const conn of hebrewFieldData.connections) {
        const letter1 = hebrewFieldData.letters[conn.start];
        const letter2 = hebrewFieldData.letters[conn.end];
        
        if (letter1 && letter2 && conn.strength > 0.1) {
            const x1 = centerX + letter1.position.x * scale;
            const y1 = centerY + letter1.position.y * scale;
            const x2 = centerX + letter2.position.x * scale;
            const y2 = centerY + letter2.position.y * scale;
            
            // Color based on phase difference and strength
            const hue = (conn.phase_diff / (2 * Math.PI)) * 360;
            ctx.strokeStyle = `hsla(${hue}, 80%, 60%, ${conn.strength * 0.7})`;
            
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.stroke();
        }
    }
    
    // Draw letters
    const letters = Object.entries(hebrewFieldData.letters);
    for (const [char, letter] of letters) {
        const x = centerX + letter.position.x * scale;
        const y = centerY + letter.position.y * scale;
        
        // Draw glow based on energy
        const glowRadius = 15 + letter.energy * 20;
        const gradient = ctx.createRadialGradient(x, y, 0, x, y, glowRadius);
        gradient.addColorStop(0, `rgba(${letter.color.r * 255}, ${letter.color.g * 255}, ${letter.color.b * 255}, ${0.3 + letter.energy * 0.7})`);
        gradient.addColorStop(1, `rgba(${letter.color.r * 255}, ${letter.color.g * 255}, ${letter.color.b * 255}, 0)`);
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(x, y, glowRadius, 0, Math.PI * 2);
        ctx.fill();
        
        // Draw letter circle
        const letterRadius = 12 + letter.energy * 8;
        ctx.beginPath();
        ctx.arc(x, y, letterRadius, 0, Math.PI * 2);
        ctx.fillStyle = `rgb(${letter.color.r * 255}, ${letter.color.g * 255}, ${letter.color.b * 255})`;
        ctx.fill();
        
        // Draw border
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.7)';
        ctx.lineWidth = 2;
        ctx.stroke();
        
        // Draw Hebrew letter
        ctx.fillStyle = 'white';
        ctx.font = 'bold 16px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(char, x, y);
    }
    
    // Draw title
    ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
    ctx.font = '16px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('Hebrew Quantum Field - 22 Letters in Quantum Harmony', width / 2, 25);
}

// ==================================================================
// HEBREW QUANTUM FIELD CONTROLS
// ==================================================================

function toggleHebrewField() {
    isHebrewRunning = !isHebrewRunning;
    const button = document.getElementById('hebrew-toggle-btn');
    
    if (isHebrewRunning) {
        button.textContent = '⏸️ Pause';
        animateHebrewField();
    } else {
        button.textContent = '▶️ Resume';
    }
}

function resetHebrewField() {
    hebrewTime = 0;
    initializeHebrewFieldData();
}

// ==================================================================
// AI CHAT
// ==================================================================

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (!message) return;
    addChatMessage('user', message);
    input.value = '';
    try {
        const response = await fetch('http://localhost:8003/api/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                message: message,
                session_id: currentSession,
                model_name: document.getElementById('model-select').value,
                max_new_tokens: 128
            })
        });
        const data = await response.json();
        if (data.response) {
            addChatMessage('assistant', data.response);
            // Only show model info if it's different from current model
            // This prevents automatic model notifications after every reply
            const currentModel = document.getElementById('model-select').value;
            if (data.model && data.model !== currentModel) {
                addChatMessage('system', `✅ Model changed to: ${data.model}`);
            }
        } else if (data.error) {
            addChatMessage('system', `❌ Error: ${data.error}`);
        }
    } catch (error) {
        addChatMessage('system', `❌ Chat error: ${error.message}`);
    }
}

function addChatMessage(role, content) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    const icons = {user: '👤', assistant: '🤖', system: '⚙️'};
    const labels = {user: 'You', assistant: 'AI', system: 'System'};
    messageDiv.innerHTML = `<strong>${icons[role] || '📝'} ${labels[role] || 'Message'}:</strong><br>${escapeHtml(content)}`;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function clearChat() {
    if (confirm('Clear chat?')) {
        document.getElementById('chat-messages').innerHTML = '';
    }
}

async function newSession() {
    currentSession = 'session_' + Date.now();
    const select = document.getElementById('session-select');
    const option = document.createElement('option');
    option.value = currentSession;
    option.textContent = currentSession;
    option.selected = true;
    select.appendChild(option);
    clearChat();
    addChatMessage('system', `✅ New session: ${currentSession}`);
}

async function downloadTranscript() {
    window.open(`http://localhost:8003/api/transcript?session_id=${currentSession}`, '_blank');
}

// ==================================================================
// RAG DOCUMENTS
// ==================================================================

async function uploadDocuments() {
    const files = document.getElementById('file-input').files;
    if (files.length === 0) {
        addChatMessage('system', '⚠️ Please select files first');
        return;
    }
    
    const statusEl = document.getElementById('upload-status');
    statusEl.textContent = `⏳ Uploading ${files.length} file(s)...`;
    
    // Upload files one by one
    let successCount = 0;
    let totalChunks = 0;
    
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        addChatMessage('system', `📄 Uploading ${i+1}/${files.length}: ${file.name} (${(file.size / 1024).toFixed(1)} KB)`);
        
        try {
            const formData = new FormData();
            formData.append('file', file);
            
            const response = await fetch('http://localhost:8003/api/upload', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP ${response.status}: ${errorText}`);
            }
            
            const data = await response.json();
            if (data.ok) {
                successCount++;
                totalChunks += (data.chunks || 0);
                addChatMessage('system', `  ✅ ${file.name}: ${data.chunks} chunks`);
            } else {
                addChatMessage('system', `  ❌ ${file.name}: ${data.error || 'Unknown error'}`);
            }
        } catch (error) {
            addChatMessage('system', `  ❌ ${file.name}: ${error.message}`);
            console.error('Upload error for', file.name, ':', error);
        }
        
        // Small delay between uploads
        if (i < files.length - 1) {
            await new Promise(resolve => setTimeout(resolve, 100));
        }
    }
    
    const msg = `✅ Uploaded ${successCount}/${files.length} files (${totalChunks} chunks)`;
    statusEl.textContent = msg;
    addChatMessage('system', msg);
    
    // Auto-refresh document list
    if (successCount > 0) {
        setTimeout(listDocuments, 500);
    }
    
    // Clear file input
    document.getElementById('file-input').value = '';
}

async function listDocuments() {
    try {
        const response = await fetch('http://localhost:8003/api/uploads');
        const data = await response.json();
        
        const uploads = data.uploads || [];
        const count = uploads.length;
        
        document.getElementById('doc-info').textContent = `📄 ${count} documents`;
        const listDiv = document.getElementById('document-list');
        listDiv.style.display = 'block';
        listDiv.innerHTML = '';
        
        if (uploads.length > 0) {
            uploads.forEach(upload => {
                const item = document.createElement('div');
                item.className = 'file-item';
                item.textContent = `📄 ${upload.source} (${upload.chunks} chunks)`;
                listDiv.appendChild(item);
            });
        } else {
            listDiv.innerHTML = '<div class="file-item">No documents</div>';
        }
    } catch (error) {
        document.getElementById('doc-info').textContent = '❌ Failed';
        console.error('List documents error:', error);
    }
}

async function clearDocuments() {
    if (!confirm('Clear all RAG documents?')) return;
    try {
        await fetch('http://localhost:8003/api/uploads/clear', {method: 'POST'});
        document.getElementById('doc-info').textContent = '✅ Cleared';
        document.getElementById('document-list').innerHTML = '';
        addChatMessage('system', '✅ Documents cleared');
    } catch (error) {
        console.error('Clear error:', error);
    }
}

// ==================================================================
// MIRROR LOOP
// ==================================================================

async function startLoop() {
    const objective = document.getElementById('loop-objective').value.trim();
    const rounds = parseInt(document.getElementById('loop-rounds').value);
    const ragEnabled = document.getElementById('loop-rag').checked;
    
    if (!objective) {
        addChatMessage('system', '⚠️ Please enter loop objective');
        return;
    }
    
    try {
        document.getElementById('loop-status-display').style.display = 'block';
        document.getElementById('loop-status').textContent = '🔁 Running loop...';
        addChatMessage('system', `🔁 Starting Mirror Loop (${rounds} rounds)`);
        
        const response = await fetch('http://localhost:8003/api/loop/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                objective: objective,
                rounds: rounds,
                rag_enabled: ragEnabled,
                session_id: currentSession
            })
        });
        
        const data = await response.json();
        
        if (data.ok) {
            document.getElementById('loop-status').textContent = '✅ Loop completed';
            addChatMessage('system', `✅ Mirror Loop completed`);
            
            // Display the result
            if (data.result) {
                addChatMessage('assistant', `🔁 Loop Result:\n${data.result.substring(0, 1000)}${data.result.length > 1000 ? '...' : ''}`);
            }
            
            // Display metrics if available
            if (data.metrics && data.metrics.length > 0) {
                const metricsInfo = data.metrics.map(m => 
                    `Round ${m.round}: Lead ${m.lead} (${m.chosen}) - Score: ${m.score_lead?.total?.toFixed(3) || 'N/A'}`
                ).join('\n');
                addChatMessage('system', `📊 Metrics:\n${metricsInfo}`);
            }
        } else {
            throw new Error(data.error || 'Loop failed');
        }
        
    } catch (error) {
        console.error('❌ [Loop] Start error:', error);
        document.getElementById('loop-status').textContent = `❌ Failed: ${error.message}`;
        addChatMessage('system', `❌ Loop failed: ${error.message}`);
    }
}

async function stopLoop() {
    addChatMessage('system', '⚠️ Loop runs are synchronous and complete immediately');
}

// ==================================================================
// RSS FEEDS - NOT IMPLEMENTED IN SINGLE SERVER
// ==================================================================

async function addRSSFeed() {
    addChatMessage('system', '⚠️ RSS feeds not implemented in single-server mode. Feature available in full chat server.');
}

async function listRSSFeeds() {
    addChatMessage('system', '⚠️ RSS feeds not implemented in single-server mode.');
}

async function ingestRSSFeeds() {
    addChatMessage('system', '⚠️ RSS feeds not implemented in single-server mode.');
}

async function applyAutoIndex() {
    addChatMessage('system', '⚠️ Auto-index not implemented in single-server mode.');
}

// ==================================================================
// MODEL MANAGEMENT
// ==================================================================

async function applyModel() {
    const model = document.getElementById('model-select').value;
    try {
        await fetch('http://localhost:8003/api/config', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({model_name: model})
        });
        addChatMessage('system', `✅ Model changed to: ${model}`);
    } catch (error) {
        addChatMessage('system', '❌ Model change failed');
    }
}

async function reloadSettings() {
    addChatMessage('system', '✅ Settings reloaded (local only)');
}

// ==================================================================
// INITIALIZATION
// ==================================================================

async function verifyServers() {
    console.log('🔍 Verifying server connection...');
    
    try {
        const response = await fetch('http://localhost:8003/api/health', {signal: AbortSignal.timeout(3000)});
        const data = await response.json();
        console.log('✅ Consciousness Engine: OK', data);
        addChatMessage('system', '✅ All features running on port 8003');
        addChatMessage('system', '  • Consciousness Engine');
        addChatMessage('system', '  • AI Chat');
        addChatMessage('system', '  • Document Upload');
        addChatMessage('system', '  • Model Management');
    } catch (error) {
        console.error('❌ Server: FAILED', error);
        addChatMessage('system', '❌ Server offline - run: .\\run_metatron_web.ps1');
    }
}

// Initialize when page loads
window.addEventListener('load', () => {
    console.log('Initializing Metatron Integrated System...');
    
    // Initialize Algorithmic Consciousness Field
    console.log('Initializing Algorithmic Consciousness Field...');
    setTimeout(() => {
        initAlgorithmicConsciousnessField();
    }, 500);
    
    // Initialize Hebrew Quantum Field
    console.log('Initializing Hebrew Quantum Field...');
    setTimeout(() => {
        initHebrewQuantumField();
    }, 750);
    
    // Initialize WebSocket connection
    console.log('Initializing WebSocket connection...');
    setTimeout(() => {
        connectConsciousness();
    }, 1000);
    
    // Setup chat resize functionality
    setupChatResize();
});

// Setup chat resizing functionality
function setupChatResize() {
    const resizeHandle = document.getElementById('chat-resize-handle');
    const chatPanel = document.getElementById('chat-panel');
    const chatMessages = document.getElementById('chat-messages');
    
    let isResizing = false;
    
    resizeHandle.addEventListener('mousedown', (e) => {
        isResizing = true;
        document.body.style.cursor = 'ns-resize';
        e.preventDefault();
    });
    
    document.addEventListener('mousemove', (e) => {
        if (!isResizing) return;
        
        // Calculate new height for chat messages
        const rect = chatPanel.getBoundingClientRect();
        const newHeight = e.clientY - rect.top - 100; // Adjust for header and controls
        
        if (newHeight > 100 && newHeight < 500) {
            chatMessages.style.maxHeight = newHeight + 'px';
        }
    });
    
    document.addEventListener('mouseup', () => {
        isResizing = false;
        document.body.style.cursor = 'default';
    });
}