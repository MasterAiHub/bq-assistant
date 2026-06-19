// BQ AI Assistant - Main JavaScript

let isListening = false;
let bqPopupTimeout = null;

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 BQ AI Assistant loaded');
    
    // Setup keyboard shortcut (Ctrl+Enter)
    document.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            triggerBQAssist();
        }
    });
    
    // Setup mobile button
    const mobileBtn = document.getElementById('bqMobileBtn');
    if (mobileBtn) {
        mobileBtn.addEventListener('click', triggerBQAssist);
    }
    
    // Setup phone button
    const phoneBtn = document.querySelector('.phone-bq-btn');
    if (phoneBtn) {
        phoneBtn.addEventListener('click', triggerBQAssist);
    }
    
    // Start listening
    startListening();
});

async function startListening() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        isListening = true;
        console.log('🎙️ BQ is listening...');
        updateUIStatus('listening');
        
        // Start background processing
        startBackgroundProcessing();
    } catch (error) {
        console.error('Microphone error:', error);
        updateUIStatus('error');
    }
}

function startBackgroundProcessing() {
    // Simulate listening and processing
    setInterval(() => {
        if (isListening) {
            // Randomly detect questions in background
            const shouldDetect = Math.random() > 0.85;
            if (shouldDetect) {
                const questions = [
                    "How would you handle this project?",
                    "What's your approach to this problem?",
                    "Can you explain your strategy?",
                    "What would you recommend?"
                ];
                const question = questions[Math.floor(Math.random() * questions.length)];
                const context = "Product Manager Interview - Q3 Planning";
                
                // Get AI response in background
                getAIResponse(question, context).then(answer => {
                    showBQPopup(answer);
                });
            }
        }
    }, 8000);
}

async function triggerBQAssist() {
    const question = document.querySelector('.sim-footer span')?.textContent || '';
    const context = "Product Manager Interview - Live Meeting";
    
    updateUIStatus('thinking');
    const answer = await getAIResponse('', context);
    showBQPopup(answer);
    updateUIStatus('listening');
}

async function getAIResponse(question, context) {
    try {
        const response = await fetch('/api/ai/assist', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                question: question || "What should I say?",
                context: context
            })
        });
        
        const data = await response.json();
        if (data.success) {
            return data.answer;
        } else {
            return "Could not get response. Please try again.";
        }
    } catch (error) {
        console.error('AI error:', error);
        return "AI service unavailable. Please try again.";
    }
}

function showBQPopup(answer) {
    const popup = document.getElementById('bqPopup');
    const answerElement = popup?.querySelector('.popup-answer');
    
    if (popup && answerElement) {
        answerElement.textContent = `💡 BQ suggests: "${answer}"`;
        popup.classList.add('show');
        
        // Auto-hide after 10 seconds
        clearTimeout(bqPopupTimeout);
        bqPopupTimeout = setTimeout(() => {
            popup.classList.remove('show');
        }, 10000);
    }
}

function updateUIStatus(status) {
    const statusDot = document.querySelector('.status-dot');
    const statusText = document.querySelector('.status-text');
    
    if (statusDot && statusText) {
        const statuses = {
            listening: { class: 'listening', text: '🎙️ BQ is listening...' },
            thinking: { class: 'listening', text: '🧠 BQ is thinking...' },
            error: { class: '', text: '⚠️ BQ error - check microphone' }
        };
        const s = statuses[status] || statuses.listening;
        statusDot.className = `status-dot ${s.class}`;
        statusText.textContent = s.text;
    }
}

// Handle mobile button press with touch events
document.addEventListener('touchstart', function(e) {
    if (e.target.closest('#bqMobileBtn') || e.target.closest('.phone-bq-btn')) {
        e.preventDefault();
        triggerBQAssist();
    }
});

console.log('✅ BQ is ready! Press Ctrl+Enter or tap the button for answers.');
