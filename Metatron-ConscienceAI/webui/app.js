window.WebChat = (function(){
  const state = {
    session: 'default',
    lang: 'es',
  };

  const t = {
    es: {
      model: 'Modelo', rag: 'RAG', topk: 'Top‑K', maxchars: 'Max chars', maxnew: 'Max new tokens',
      clear: 'Limpiar', download: 'Descargar conversación', send: 'Enviar', sources: 'Fuentes (RAG)', help: 'Ayuda', placeholder: 'Escribe tu mensaje... (Ctrl+Enter para enviar)'
    },
    en: {
      model: 'Model', rag: 'RAG', topk: 'Top‑K', maxchars: 'Max chars', maxnew: 'Max new tokens',
      clear: 'Clear', download: 'Download conversation', send: 'Send', sources: 'Sources (RAG)', help: 'Help', placeholder: 'Type your message... (Ctrl+Enter to send)'
    }
  };

  function applyLang(){
    const tr = t[state.lang];
    document.getElementById('lblModel').textContent = tr.model;
    document.getElementById('lblRag').textContent = tr.rag;
    document.getElementById('lblTopK').textContent = tr.topk;
    document.getElementById('lblMaxChars').textContent = tr.maxchars;
    document.getElementById('lblMaxNew').textContent = tr.maxnew;
    document.getElementById('btnClear').textContent = tr.clear;
    document.getElementById('btnDownload').textContent = tr.download;
    document.getElementById('btnSend').textContent = tr.send;
    document.getElementById('lblSources').textContent = tr.sources;
    document.getElementById('lblHelp').textContent = tr.help;
    document.getElementById('messageInput').placeholder = tr.placeholder;
  }

  async function send(){
    const msgEl = document.getElementById('messageInput');
    const msg = msgEl.value.trim();
    if(!msg) return;
    const topK = parseInt(document.getElementById('topKInput').value || '3', 10);
    const maxChars = parseInt(document.getElementById('maxCharsInput').value || '1200', 10);
    const maxNew = parseInt(document.getElementById('maxNewInput').value || '128', 10);
    const rag = document.getElementById('ragToggle').checked;

    appendMsg('user', msg);
    msgEl.value = '';
    setLoading(true);
    try {
      const res = await fetch('/api/chat', {
        method: 'POST', headers: {'Content-Type':'application/json'},
        body: JSON.stringify({ message: msg, session_id: state.session, rag, top_k: topK, max_chars: maxChars, max_new_tokens: maxNew })
      });
      const data = await res.json();
      appendMsg('assistant', data.response);
      renderSources(data.sources||[]);
    } catch(e){
      appendMsg('assistant', '[ERROR] '+ e);
    } finally {
      setLoading(false);
    }
  }

  function appendMsg(role, text){
    const win = document.getElementById('chatWindow');
    const el = document.createElement('div'); el.className = 'msg';
    const roleEl = document.createElement('div'); roleEl.className = 'role'; roleEl.textContent = role==='user'?'Tú':'Asistente';
    const bubble = document.createElement('div'); bubble.className = 'bubble'; bubble.textContent = text;
    el.appendChild(roleEl); el.appendChild(bubble);
    win.appendChild(el); win.scrollTop = win.scrollHeight;
  }

  function renderSources(sources){
    const list = document.getElementById('sourcesList');
    list.innerHTML = '';
    sources.forEach(s => {
      const div = document.createElement('div'); div.className = 'source-item';
      const meta = s.meta || {}; const url = meta.url || meta.source || '';
      div.innerHTML = `score=${(s.score||0).toFixed(3)} · <a href="${url}" target="_blank">${url}</a>`;
      list.appendChild(div);
    });
  }

  function setLoading(on){
    document.getElementById('btnSend').disabled = on;
  }

  async function download(){
    const res = await fetch(`/api/transcript?session_id=${encodeURIComponent(state.session)}`);
    const data = await res.json();
    const blob = new Blob([JSON.stringify(data, null, 2)], {type:'application/json'});
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = `chat_${state.session}.json`; a.click();
    URL.revokeObjectURL(a.href);
  }

  function clear(){
    document.getElementById('chatWindow').innerHTML = '';
    document.getElementById('sourcesList').innerHTML = '';
  }

  function init(){
    // Initialize settings
    const lsLang = localStorage.getItem('webchat_lang');
    state.lang = lsLang || 'es';
    document.getElementById('langSelect').value = state.lang;
    applyLang();

    document.getElementById('btnSend').addEventListener('click', send);
    document.getElementById('btnClear').addEventListener('click', clear);
    document.getElementById('btnDownload').addEventListener('click', download);
    document.getElementById('langSelect').addEventListener('change', (e)=>{
      state.lang = e.target.value; localStorage.setItem('webchat_lang', state.lang); applyLang();
    });
    const msgEl = document.getElementById('messageInput');
    msgEl.addEventListener('keydown', (e)=>{
      if(e.key==='Enter' && (e.ctrlKey || e.metaKey)) send();
    });
  }

  return { init };
})();