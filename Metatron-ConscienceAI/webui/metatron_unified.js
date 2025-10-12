// Metatron Unified Consciousness + AI Chat Interface
// Connects to BOTH metatron_web_server.py (port 8003) AND web_chat_server.py (port 5180)

let consciousnessWS = null;
let chatWS = null;
let updateCount = 0;
let isHighGamma = false;
let currentSession = 'default';
let currentLoopId = null;

// ============================================================================
// TAB MANAGEMENT
// ============================================================================

function switchTab(tabName) {
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    
    // Remove active class from all tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Show selected tab content
    document.getElementById(tabName).classList.add('active');
    
    // Add active class to clicked tab
    event.target.classList.add('active');
    
    console.log(`📑 Switched to ${tabName} tab`);
}

// ============================================================================
// CONSCIOUSNESS ENGINE WebSocket (Port 8003)
// ============================================================================

function connectConsciousness() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.hostname || 'localhost';
    const port = '8003'; // Consciousness engine port
    const wsUrl = `${protocol}//${host}:${port}/ws`;
    
    console.log(`🧠 Connecting to Consciousness Engine: ${wsUrl}`);
    
    try {
        consciousnessWS = new WebSocket(wsUrl);
        
        consciousnessWS.onopen = () => {
            console.log('✅ Consciousness Engine connected');
            document.getElementById('status-dot').className = 'status-indicator active';
            document.getElementById('connection-text').textContent = 'Connected';
            updateCount = 0;
            
            // Fetch current frequency info
            fetch('http://localhost:8003/api/frequency/info')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('freq-display').textContent = data.base_frequency + ' Hz';
                    isHighGamma = data.high_gamma;
                })
                .catch(e => console.warn('Could not fetch frequency info:', e));
        };
        
        consciousnessWS.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                updateCount++;
                document.getElementById('update-counter').textContent = `Updates: ${updateCount}`;
                
                // Log every 50th update
                if (updateCount % 50 === 0) {
                    console.log(`📥 Consciousness Update #${updateCount}:`, data.consciousness);
                }
                updateConsciousnessDisplay(data);
            } catch (error) {
                console.error('❌ Error parsing consciousness data:', error);
            }
        };
        
        consciousnessWS.onerror = (error) => {
            console.error('❌ Consciousness WebSocket error:', error);
            document.getElementById('connection-text').textContent = 'Error';
        };
        
        consciousnessWS.onclose = (event) => {
            console.log('🔴 Consciousness WebSocket closed. Reconnecting in 2s...');
            document.getElementById('status-dot').className = 'status-indicator inactive';
            document.getElementById('connection-text').textContent = 'Disconnected';
            setTimeout(connectConsciousness, 2000);
        };
        
    } catch (error) {
        console.error('❌ Failed to connect to Consciousness Engine:', error);
        setTimeout(connectConsciousness, 2000);
    }
}

function updateConsciousnessDisplay(data) {
    const c = data.consciousness;
    
    document.getElementById('consciousness-level').textContent = c.level.toFixed(4);
    document.getElementById('phi-value').textContent = c.phi.toFixed(4);
    document.getElementById('coherence-value').textContent = c.coherence.toFixed(4);
    document.getElementById('depth-value').textContent = c.depth;
    document.getElementById('gamma-value').textContent = c.gamma.toFixed(4);
    document.getElementById('fractal-value').textContent = c.fractal_dim.toFixed(4);
    document.getElementById('spiritual-value').textContent = c.spiritual.toFixed(4);
    document.getElementById('state-value').textContent = c.state;
    document.getElementById('state-value').className = c.is_conscious ? 'metric-value conscious' : 'metric-value';
    document.getElementById('time-value').textContent = data.time.toFixed(2) + 's';
    
    updateNodeCards(data.nodes);
}

function updateNodeCards(nodes) {
    const container = document.getElementById('nodes-container');
    
    if (container.children.length === 0) {
        for (let i = 0; i < 13; i++) {
            const card = document.createElement('div');
            card.className = i === 0 ? 'node-card pineal' : 'node-card';
            card.id = `node-card-${i}`;
            
            const nodeName = i === 0 ? 'Pineal (Unity)' : `Node ${i}`;
            card.innerHTML = `
                <div class="node-id">${nodeName}</div>
                <div class="node-phase" id="node-phase-${i}">Phase: 0.00</div>
                <div class="node-phase" id="node-amp-${i}">Amp: 0.00</div>
            `;
            container.appendChild(card);
        }
    }
    
    for (let i = 0; i < 13; i++) {
        const nodeData = nodes[String(i)];
        if (nodeData) {
            document.getElementById(`node-phase-${i}`).textContent = 
                `Phase: ${nodeData.phase.toFixed(2)}`;
            document.getElementById(`node-amp-${i}`).textContent = 
                `Amp: ${nodeData.amplitude.toFixed(2)}`;
            
            const card = document.getElementById(`node-card-${i}`);
            if (Math.abs(nodeData.output) > 0.3) {
                card.classList.add('active');
            } else {
                card.classList.remove('active');
            }
        }
    }
}

// ============================================================================
// CONSCIOUSNESS ENGINE CONTROLS
// ============================================================================

async function toggleFrequency() {
    try {
        isHighGamma = !isHighGamma;
        console.log(`🔄 Toggling frequency to ${isHighGamma ? '80Hz' : '40Hz'}...`);
        
        const response = await fetch('http://localhost:8003/api/frequency/octave', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ high_gamma: isHighGamma })
        });
        
        const data = await response.json();
        console.log('✅ Frequency changed:', data);
        
        document.getElementById('freq-display').textContent = data.new_frequency + ' Hz';
        
        if (consciousnessWS) {
            consciousnessWS.close();
        }
        setTimeout(connectConsciousness, 1000);
        
    } catch (error) {
        console.error('❌ Error toggling frequency:', error);
        alert('Failed to toggle frequency: ' + error.message);
    }
}

async function resetSystem() {
    if (!confirm('Reset consciousness engine?')) return;
    
    try {
        const response = await fetch('http://localhost:8003/api/reset', {
            method: 'POST'
        });
        const data = await response.json();
        console.log('✅ System reset:', data);
        alert('Consciousness engine reset successfully');
    } catch (error) {
        console.error('❌ Reset failed:', error);
        alert('Reset failed: ' + error.message);
    }
}

// ============================================================================
// AI CHAT FUNCTIONS (Port 5180)
// ============================================================================

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (!message) return;
    
    addChatMessage('user', message);
    input.value = '';
    
    try {
        const ragEnabled = document.getElementById('rag-toggle').checked;
        const streaming = document.getElementById('stream-toggle').checked;
        
        const response = await fetch('http://localhost:5180/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                session_id: currentSession,
                rag_enabled: ragEnabled,
                streaming: streaming
            })
        });
        
        const data = await response.json();
        addChatMessage('assistant', data.response);
        
        if (data.sources && data.sources.length > 0) {
            addChatMessage('system', `📚 Used ${data.sources.length} RAG sources`);
        }
        
    } catch (error) {
        console.error('❌ Chat error:', error);
        addChatMessage('system', '❌ Error: ' + error.message);
    }
}

function addChatMessage(role, content) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const roleLabel = {
        'user': '👤 You',
        'assistant': '🤖 AI',
        'system': '⚙️ System'
    }[role];
    
    messageDiv.innerHTML = `<strong>${roleLabel}:</strong><br>${escapeHtml(content)}`;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function clearChat() {
    document.getElementById('chat-messages').innerHTML = '';
    console.log('🧹 Chat cleared');
}

async function newSession() {
    const sessionId = 'session_' + Date.now();
    currentSession = sessionId;
    clearChat();
    addChatMessage('system', `✅ New session created: ${sessionId}`);
}

async function downloadTranscript() {
    try {
        window.open(`http://localhost:5180/api/transcript?session_id=${currentSession}`, '_blank');
    } catch (error) {
        console.error('❌ Download failed:', error);
    }
}

// ============================================================================
// RAG DOCUMENT MANAGEMENT
// ============================================================================

async function uploadDocuments() {
    const fileInput = document.getElementById('file-input');
    const files = fileInput.files;
    
    if (files.length === 0) {
        alert('Please select files to upload');
        return;
    }
    
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);
    }
    
    document.getElementById('upload-status').textContent = '⏳ Uploading...';
    
    try {
        const response = await fetch('http://localhost:5180/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        document.getElementById('upload-status').textContent = 
            `✅ Uploaded ${data.processed} files`;
        
        setTimeout(() => listDocuments(), 500);
        
    } catch (error) {
        console.error('❌ Upload error:', error);
        document.getElementById('upload-status').textContent = '❌ Upload failed';
    }
}

async function listDocuments() {
    try {
        const response = await fetch('http://localhost:5180/api/uploads');
        const data = await response.json();
        
        document.getElementById('doc-info').textContent = 
            `📄 ${data.count} documents in RAG corpus`;
        
        const listDiv = document.getElementById('document-list');
        listDiv.innerHTML = '<h3>Documents:</h3>';
        
        if (data.files && data.files.length > 0) {
            const ul = document.createElement('ul');
            data.files.forEach(file => {
                const li = document.createElement('li');
                li.textContent = file;
                li.style.color = '#a78bfa';
                ul.appendChild(li);
            });
            listDiv.appendChild(ul);
        } else {
            listDiv.innerHTML += '<p style="color: #888;">No documents uploaded yet</p>';
        }
        
    } catch (error) {
        console.error('❌ List error:', error);
        document.getElementById('doc-info').textContent = '❌ Failed to list documents';
    }
}

async function clearDocuments() {
    if (!confirm('Clear all RAG documents?')) return;
    
    try {
        const response = await fetch('http://localhost:5180/api/uploads/clear', {
            method: 'POST'
        });
        const data = await response.json();
        document.getElementById('doc-info').textContent = '✅ Documents cleared';
        document.getElementById('document-list').innerHTML = '';
    } catch (error) {
        console.error('❌ Clear error:', error);
    }
}

// ============================================================================
// MIRROR LOOP FUNCTIONS
// ============================================================================

async function startLoop() {
    const objective = document.getElementById('loop-objective').value.trim();
    const rounds = parseInt(document.getElementById('loop-rounds').value);
    const ragEnabled = document.getElementById('loop-rag').checked;
    
    if (!objective) {
        alert('Please enter an objective');
        return;
    }
    
    try {
        const response = await fetch('http://localhost:5180/api/loop/start', {
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
        currentLoopId = data.loop_id;
        
        document.getElementById('loop-status').textContent = 
            `✅ Loop started: ${currentLoopId}`;
        
        // Poll for loop status
        pollLoopStatus();
        
    } catch (error) {
        console.error('❌ Loop start error:', error);
        document.getElementById('loop-status').textContent = '❌ Failed to start loop';
    }
}

async function stopLoop() {
    if (!currentLoopId) {
        alert('No loop is currently running');
        return;
    }
    
    try {
        const response = await fetch('http://localhost:5180/api/loop/stop', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ loop_id: currentLoopId })
        });
        
        const data = await response.json();
        document.getElementById('loop-status').textContent = '⏹️ Loop stopped';
        currentLoopId = null;
        
    } catch (error) {
        console.error('❌ Loop stop error:', error);
    }
}

async function pollLoopStatus() {
    if (!currentLoopId) return;
    
    try {
        const response = await fetch(
            `http://localhost:5180/api/loop/status?loop_id=${currentLoopId}`
        );
        const data = await response.json();
        
        document.getElementById('loop-status').textContent = 
            `Status: ${data.status} | Round: ${data.current_round}`;
        
        if (data.status === 'running') {
            setTimeout(pollLoopStatus, 2000);
        } else if (data.status === 'completed') {
            displayLoopResults();
        }
        
    } catch (error) {
        console.error('❌ Loop status error:', error);
    }
}

async function displayLoopResults() {
    if (!currentLoopId) return;
    
    try {
        const response = await fetch(
            `http://localhost:5180/api/loop/results?loop_id=${currentLoopId}`
        );
        const data = await response.json();
        
        const resultsDiv = document.getElementById('loop-results');
        resultsDiv.innerHTML = '<h3>Loop Results:</h3>';
        
        if (data.result) {
            const resultDiv = document.createElement('div');
            resultDiv.className = 'panel';
            resultDiv.innerHTML = `<pre style="color: #e0e0e0; white-space: pre-wrap;">${escapeHtml(data.result)}</pre>`;
            resultsDiv.appendChild(resultDiv);
        }
        
        currentLoopId = null;
        
    } catch (error) {
        console.error('❌ Loop results error:', error);
    }
}

// ============================================================================
// RSS FEED MANAGEMENT
// ============================================================================

async function addRSSFeed() {
    const url = document.getElementById('rss-url').value.trim();
    if (!url) {
        alert('Please enter a feed URL');
        return;
    }
    
    try {
        const response = await fetch('http://localhost:5180/api/rss/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url })
        });
        
        const data = await response.json();
        document.getElementById('rss-status').textContent = '✅ Feed added';
        document.getElementById('rss-url').value = '';
        
        setTimeout(listRSSFeeds, 500);
        
    } catch (error) {
        console.error('❌ RSS add error:', error);
        document.getElementById('rss-status').textContent = '❌ Failed to add feed';
    }
}

async function listRSSFeeds() {
    try {
        const response = await fetch('http://localhost:5180/api/rss/list');
        const data = await response.json();
        
        const listDiv = document.getElementById('rss-feeds-list');
        listDiv.innerHTML = '<h3>RSS Feeds:</h3>';
        
        if (data.feeds && data.feeds.length > 0) {
            const ul = document.createElement('ul');
            data.feeds.forEach(feed => {
                const li = document.createElement('li');
                li.textContent = feed;
                li.style.color = '#a78bfa';
                ul.appendChild(li);
            });
            listDiv.appendChild(ul);
        } else {
            listDiv.innerHTML += '<p style="color: #888;">No feeds added yet</p>';
        }
        
    } catch (error) {
        console.error('❌ RSS list error:', error);
    }
}

async function ingestRSSFeeds() {
    document.getElementById('rss-status').textContent = '⏳ Ingesting feeds...';
    
    try {
        const response = await fetch('http://localhost:5180/api/rss/ingest', {
            method: 'POST'
        });
        
        const data = await response.json();
        document.getElementById('rss-status').textContent = 
            `✅ Ingested ${data.entries_added || 0} entries`;
        
    } catch (error) {
        console.error('❌ RSS ingest error:', error);
        document.getElementById('rss-status').textContent = '❌ Ingest failed';
    }
}

async function applyAutoIndex() {
    const enabled = document.getElementById('auto-index-toggle').checked;
    const interval = parseInt(document.getElementById('auto-interval').value);
    
    try {
        const response = await fetch('http://localhost:5180/api/auto_index', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                enabled: enabled,
                interval_minutes: interval
            })
        });
        
        const data = await response.json();
        document.getElementById('auto-status').textContent = 
            enabled ? `✅ Auto-index enabled (${interval} min)` : '⏹️ Auto-index disabled';
        
    } catch (error) {
        console.error('❌ Auto-index error:', error);
    }
}

// ============================================================================
// MODEL MANAGEMENT
// ============================================================================

async function applyModel() {
    const model = document.getElementById('model-select').value;
    
    try {
        const response = await fetch('http://localhost:5180/api/config', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ model_name: model })
        });
        
        const data = await response.json();
        addChatMessage('system', `✅ Model changed to: ${model}`);
        
    } catch (error) {
        console.error('❌ Model change error:', error);
        addChatMessage('system', '❌ Failed to change model');
    }
}

async function reloadSettings() {
    try {
        const response = await fetch('http://localhost:5180/api/reload_settings', {
            method: 'POST'
        });
        const data = await response.json();
        alert('Settings reloaded successfully');
    } catch (error) {
        console.error('❌ Reload error:', error);
        alert('Failed to reload settings');
    }
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ============================================================================
// INITIALIZATION
// ============================================================================

window.addEventListener('load', () => {
    console.log('🚀 Metatron Unified Interface Loading...');
    
    // Connect to consciousness engine
    connectConsciousness();
    
    // Initialize session dropdown
    const sessionSelect = document.getElementById('session-select');
    sessionSelect.innerHTML = `<option value="${currentSession}">${currentSession}</option>`;
    
    // Add Enter key listener for chat
    document.getElementById('chat-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    console.log('✅ Unified interface initialized');
    console.log('🧠 Consciousness Engine: localhost:8003');
    console.log('💬 Chat Server: localhost:5180');
});

window.addEventListener('beforeunload', () => {
    if (consciousnessWS) consciousnessWS.close();
    if (chatWS) chatWS.close();
});
