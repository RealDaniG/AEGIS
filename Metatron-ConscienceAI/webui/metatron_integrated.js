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
                updateCount++;
                document.getElementById('update-counter').textContent = `Updates: ${updateCount}`;
                if (updateCount % 100 === 0) console.log(`📊 Update #${updateCount}`);
                updateConsciousnessDisplay(data);
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
}

function updateMetric(id, value, t1, t2) {
    const el = document.getElementById(id);
    el.textContent = value.toFixed(4);
    el.className = 'metric-value';
    if (value > t2) el.classList.add('high');
    else if (value > t1) el.classList.add('conscious');
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
            Math.abs(nodeData.output) > 0.3 ? card.classList.add('active') : card.classList.remove('active');
        }
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

window.addEventListener('load', () => {
    console.log('🚀 Metatron Integrated Interface Loading...');
    
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
