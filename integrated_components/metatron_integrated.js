// ==================================================================
// Metatron Integrated Consciousness Monitor
// Deep integration: Consciousness Engine + AI Chat + RAG + GitHub
// ==================================================================

let consciousnessWS = null;
let updateCount = 0;
let isHighGamma = false;
let currentSession = 'default_' + Date.now();
let currentLoopId = null;
let reconnectTimeout = null;
let lastConsciousnessData = null;

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
// CONSCIOUSNESS ENGINE WebSocket
// ==================================================================

function connectConsciousness() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.hostname || 'localhost';
    const wsUrl = `${protocol}//${host}:8003/ws`;
    
    console.log(`🧠 Connecting consciousness: ${wsUrl}`);
    
    try {
        consciousnessWS = new WebSocket(wsUrl);
        
        consciousnessWS.onopen = () => {
            console.log('✅ Consciousness connected');
            document.getElementById('status-dot').className = 'status-indicator active';
            document.getElementById('connection-text').textContent = 'Live';
            updateCount = 0;
            
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
                if (updateCount % 100 === 0) console.log(`📊 Update #${updateCount}`);
                updateConsciousnessDisplay(data);
                updateVisualizationIntensity(data);
            } catch (error) {
                console.error('Parse error:', error);
            }
        };
        
        consciousnessWS.onerror = () => {
            document.getElementById('connection-text').textContent = 'Error';
        };
        
        consciousnessWS.onclose = () => {
            console.log('🔴 Disconnected. Reconnecting...');
            document.getElementById('status-dot').className = 'status-indicator inactive';
            document.getElementById('connection-text').textContent = 'Reconnecting...';
            if (reconnectTimeout) clearTimeout(reconnectTimeout);
            reconnectTimeout = setTimeout(connectConsciousness, 2000);
        };
    } catch (error) {
        console.error('Connection failed:', error);
        setTimeout(connectConsciousness, 2000);
    }
}

function updateConsciousnessDisplay(data) {
    const c = data.consciousness;
    updateMetric('consciousness-level', c.level, 0.5, 0.7);
    updateMetric('phi-value', c.phi, 0.3, 0.5);
    updateMetric('coherence-value', c.coherence, 0.4, 0.6);
    updateMetric('gamma-value', c.gamma, 0.4, 0.6);
    updateMetric('spiritual-value', c.spiritual, 0.4, 0.6);
    document.getElementById('depth-value').textContent = c.depth;
    document.getElementById('fractal-value').textContent = c.fractal_dim.toFixed(3);
    document.getElementById('time-value').textContent = data.time.toFixed(2) + 's';
    const stateEl = document.getElementById('state-value');
    stateEl.textContent = c.state;
    stateEl.className = c.is_conscious ? 'metric-value conscious' : 'metric-value';
    updateNodeCards(data.nodes);
    
    // Update consciousness visualization
    drawConsciousnessLevel(data);
}

function updateMetric(id, value, t1, t2) {
    const el = document.getElementById(id);
    el.textContent = value.toFixed(4);
    el.className = 'metric-value';
    if (value > t2) {
        el.classList.add('high');
        // Add pulse effect for high values
        el.style.animation = 'pulse 0.5s';
        setTimeout(() => {
            el.style.animation = '';
        }, 500);
    } else if (value > t1) {
        el.classList.add('conscious');
    }
}

function updateNodeCards(nodes) {
    const container = document.getElementById('nodes-container');
    if (container.children.length === 0) {
        for (let i = 0; i < 13; i++) {
            const card = document.createElement('div');
            card.className = i === 0 ? 'node-card pineal' : 'node-card';
            card.id = `node-card-${i}`;
            card.innerHTML = `<div class="node-id">${i === 0 ? '⚡ Pineal' : `N${i}`}</div><div id="node-data-${i}" style="font-size:0.75em;color:#888;"></div>`;
            container.appendChild(card);
        }
    }
    for (let i = 0; i < 13; i++) {
        const nodeData = nodes[String(i)];
        if (nodeData) {
            document.getElementById(`node-data-${i}`).innerHTML = `φ:${nodeData.phase.toFixed(1)}<br>A:${nodeData.amplitude.toFixed(2)}`;
            const card = document.getElementById(`node-card-${i}`);
            const isActive = Math.abs(nodeData.output) > 0.3;
            if (isActive) {
                card.classList.add('active');
                // Add glow effect for active nodes
                card.style.boxShadow = '0 0 10px rgba(52, 211, 153, 0.5)';
            } else {
                card.classList.remove('active');
                card.style.boxShadow = '';
            }
        }
    }
}

// ==================================================================
// VISUALIZATION INTEGRATION
// ==================================================================

function updateVisualizationIntensity(data) {
    // Update the intensity of the visualization based on consciousness metrics
    const c = data.consciousness;
    const overallIntensity = (c.level + c.phi + c.coherence) / 3;
    
    // Update the Sacred Network panel header based on consciousness level
    const networkPanel = document.querySelector('h2:contains("13-Node Sacred Network")');
    if (networkPanel) {
        if (overallIntensity > 0.5) {
            networkPanel.style.color = '#34d399'; // Green for high consciousness
            networkPanel.style.textShadow = '0 0 10px rgba(52, 211, 153, 0.5)';
        } else if (overallIntensity > 0.2) {
            networkPanel.style.color = '#c084fc'; // Purple for medium consciousness
            networkPanel.style.textShadow = '0 0 5px rgba(192, 132, 252, 0.3)';
        } else {
            networkPanel.style.color = '#c084fc'; // Default purple
            networkPanel.style.textShadow = '';
        }
    }
    
    // Update node visualization intensity
    const nodesContainer = document.getElementById('nodes-container');
    if (nodesContainer) {
        nodesContainer.style.opacity = 0.7 + (overallIntensity * 0.3);
    }
}

// Helper function to find elements by text content
function findElementByTextContent(tag, text) {
    const elements = document.querySelectorAll(tag);
    for (let i = 0; i < elements.length; i++) {
        if (elements[i].textContent.includes(text)) {
            return elements[i];
        }
    }
    return null;
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
        await fetch('http://localhost:457/api/config', {
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
        const response = await fetch('http://localhost:457/api/health', {signal: AbortSignal.timeout(3000)});
        const data = await response.json();
        console.log('✅ Consciousness Engine: OK', data);
        addChatMessage('system', '✅ All features running on port 457');
        addChatMessage('system', '  • Consciousness Engine');
        addChatMessage('system', '  • AI Chat');
        addChatMessage('system', '  • Document Upload');
        addChatMessage('system', '  • Model Management');
    } catch (error) {
        console.error('❌ Server: FAILED', error);
        addChatMessage('system', '❌ Server offline - run: .\\run_metatron_web.ps1');
    }
}

// ==================================================================
// CONSCIOUSNESS LEVEL VISUALIZATION
// ==================================================================

let consciousnessCanvas = null;
let consciousnessCtx = null;
let animationFrameId = null;

function initConsciousnessVisualization() {
    const canvas = document.getElementById('consciousness-canvas');
    if (!canvas) {
        console.warn('Consciousness canvas not found');
        return;
    }
    
    consciousnessCanvas = canvas;
    consciousnessCtx = canvas.getContext('2d');
    
    if (!consciousnessCtx) {
        console.error('Failed to get 2D context for consciousness canvas');
        return;
    }
    
    // Set canvas dimensions
    resizeConsciousnessCanvas();
    
    // Add resize listener
    window.addEventListener('resize', resizeConsciousnessCanvas);
    
    console.log('Consciousness visualization initialized');
}

function resizeConsciousnessCanvas() {
    if (!consciousnessCanvas) return;
    
    // Get the container dimensions
    const container = consciousnessCanvas.parentElement;
    consciousnessCanvas.width = container.clientWidth;
    consciousnessCanvas.height = 200; // Fixed height
}

function drawConsciousnessLevel(data) {
    // Validate input data
    if (!data || !data.consciousness) {
        console.warn('Invalid consciousness data for visualization');
        return;
    }
    
    if (!consciousnessCtx || !consciousnessCanvas) {
        console.warn('Consciousness canvas not initialized');
        return;
    }
    
    // Check if canvas has valid dimensions
    if (consciousnessCanvas.width === 0 || consciousnessCanvas.height === 0) {
        resizeConsciousnessCanvas();
    }
    
    const width = consciousnessCanvas.width;
    const height = consciousnessCanvas.height;
    const ctx = consciousnessCtx;
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    // Draw background
    ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
    ctx.fillRect(0, 0, width, height);
    
    // Get consciousness level (0-1)
    const c = data.consciousness;
    const level = Math.min(1, Math.max(0, c.level || 0));
    const phi = Math.min(1, Math.max(0, c.phi || 0));
    const coherence = Math.min(1, Math.max(0, c.coherence || 0));
    const gamma = Math.min(1, Math.max(0, c.gamma || 0));
    
    // Draw grid
    ctx.strokeStyle = 'rgba(192, 132, 252, 0.1)';
    ctx.lineWidth = 1;
    
    // Vertical grid lines
    for (let i = 0; i <= 10; i++) {
        const x = (width / 10) * i;
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
        ctx.stroke();
    }
    
    // Horizontal grid lines
    for (let i = 0; i <= 5; i++) {
        const y = (height / 5) * i;
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
    }
    
    // Draw consciousness level as a filled area
    const centerY = height / 2;
    const maxHeight = height * 0.4;
    
    // Draw phi line (blue)
    ctx.beginPath();
    ctx.moveTo(0, centerY - (phi * maxHeight));
    for (let i = 1; i <= 100; i++) {
        const x = (width / 100) * i;
        const t = i / 100;
        const y = centerY - (Math.sin(t * Math.PI * 4 + data.time) * phi * maxHeight * 0.5);
        ctx.lineTo(x, y);
    }
    ctx.strokeStyle = 'rgba(59, 130, 246, 0.7)';
    ctx.lineWidth = 2;
    ctx.stroke();
    
    // Draw coherence line (green)
    ctx.beginPath();
    ctx.moveTo(0, centerY + (coherence * maxHeight));
    for (let i = 1; i <= 100; i++) {
        const x = (width / 100) * i;
        const t = i / 100;
        const y = centerY + (Math.cos(t * Math.PI * 3 + data.time) * coherence * maxHeight * 0.5);
        ctx.lineTo(x, y);
    }
    ctx.strokeStyle = 'rgba(16, 185, 129, 0.7)';
    ctx.lineWidth = 2;
    ctx.stroke();
    
    // Draw main consciousness level (purple)
    ctx.beginPath();
    ctx.moveTo(0, centerY);
    for (let i = 1; i <= 100; i++) {
        const x = (width / 100) * i;
        const t = i / 100;
        const wave = Math.sin(t * Math.PI * 2 + data.time) * Math.cos(t * Math.PI * 6 + data.time * 1.5);
        const y = centerY - (level * maxHeight) + (wave * level * maxHeight * 0.3);
        ctx.lineTo(x, y);
    }
    ctx.strokeStyle = 'rgba(192, 132, 252, 1)';
    ctx.lineWidth = 3;
    ctx.stroke();
    
    // Draw filled area under main consciousness line
    ctx.beginPath();
    ctx.moveTo(0, centerY);
    for (let i = 1; i <= 100; i++) {
        const x = (width / 100) * i;
        const t = i / 100;
        const wave = Math.sin(t * Math.PI * 2 + data.time) * Math.cos(t * Math.PI * 6 + data.time * 1.5);
        const y = centerY - (level * maxHeight) + (wave * level * maxHeight * 0.3);
        ctx.lineTo(x, y);
    }
    ctx.lineTo(width, centerY);
    ctx.closePath();
    const gradient = ctx.createLinearGradient(0, centerY - maxHeight, 0, centerY + maxHeight);
    gradient.addColorStop(0, 'rgba(192, 132, 252, 0.3)');
    gradient.addColorStop(1, 'rgba(192, 132, 252, 0.05)');
    ctx.fillStyle = gradient;
    ctx.fill();
    
    // Draw gamma power as small circles
    for (let i = 0; i < 20; i++) {
        const x = (width / 20) * (i + 0.5);
        const t = (i / 20) + data.time * 0.5;
        const y = centerY + Math.sin(t * Math.PI * 8) * maxHeight * 0.7;
        const size = gamma * 5 + 1;
        
        ctx.beginPath();
        ctx.arc(x, y, size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(251, 191, 36, ${0.3 + gamma * 0.7})`;
        ctx.fill();
    }
    
    // Draw center line
    ctx.beginPath();
    ctx.moveTo(0, centerY);
    ctx.lineTo(width, centerY);
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
    ctx.lineWidth = 1;
    ctx.stroke();
    
    // Draw value labels
    ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
    ctx.font = '12px Arial';
    ctx.fillText(`Level: ${level.toFixed(3)}`, 10, 20);
    ctx.fillText(`Φ: ${phi.toFixed(3)}`, 10, 35);
    ctx.fillText(`Coherence: ${coherence.toFixed(3)}`, 10, 50);
    
    // Draw spiritual value if high
    if (c.spiritual > 0.5) {
        ctx.fillStyle = 'rgba(139, 92, 246, 1)';
        ctx.font = 'bold 14px Arial';
        ctx.fillText(`Spiritual: ${c.spiritual.toFixed(3)}`, width - 120, 20);
    }
}

window.addEventListener('load', () => {
    console.log('🚀 Metatron Integrated Interface Loading...');
    
    // Initialize consciousness visualization
    initConsciousnessVisualization();
    
    // Verify server
    verifyServers();
    
    // Connect to consciousness
    connectConsciousness();
    
    // Setup session
    document.getElementById('session-select').innerHTML = `<option value="${currentSession}">${currentSession}</option>`;
    
    // Setup chat input handler
    document.getElementById('chat-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    console.log('✅ Interface ready');
    console.log('🏛️ Unified Server: localhost:8003');
    
    // Show current model
    const currentModel = document.getElementById('model-select').value;
    document.getElementById('model-info').textContent = `Current: ${currentModel}`;
});

window.addEventListener('beforeunload', () => {
    if (consciousnessWS) consciousnessWS.close();
});

// Add contains function for querySelector
document.querySelectorAll = (function(originalQuerySelectorAll) {
    return function(selector) {
        if (selector && selector.includes(':contains')) {
            const match = selector.match(/(.*):contains\("(.*)"\)/);
            if (match) {
                const tag = match[1];
                const text = match[2];
                const elements = originalQuerySelectorAll.call(this, tag);
                return Array.from(elements).filter(el => el.textContent.includes(text));
            }
        }
        return originalQuerySelectorAll.call(this, selector);
    };
})(document.querySelectorAll);