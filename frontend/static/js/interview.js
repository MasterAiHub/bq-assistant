// Interview-specific functionality for BQ AI Assistant

class InterviewAssistant {
    constructor() {
        this.isRecording = false;
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.currentQuestion = null;
        this.interviewContext = {
            title: '',
            interviewers: [],
            startTime: null,
            questions: [],
            answers: []
        };
    }

    /**
     * Starts recording the interview
     */
    async startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.mediaRecorder = new MediaRecorder(stream);
            this.audioChunks = [];

            this.mediaRecorder.ondataavailable = (event) => {
                this.audioChunks.push(event.data);
            };

            this.mediaRecorder.onstop = () => {
                const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
                this.handleRecordingStop(audioBlob);
            };

            this.mediaRecorder.start();
            this.isRecording = true;
            console.log('Interview recording started');
        } catch (error) {
            console.error('Failed to start recording:', error);
        }
    }

    /**
     * Stops recording the interview
     */
    stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.isRecording = false;
            console.log('Interview recording stopped');
        }
    }

    /**
     * Handles the end of recording
     */
    async handleRecordingStop(audioBlob) {
        const reader = new FileReader();
        reader.onloadend = async () => {
            const audioData = reader.result;
            const transcript = await transcribeAudio(audioData);
            if (transcript) {
                this.interviewContext.answers.push({
                    question: this.currentQuestion,
                    answer: transcript,
                    timestamp: new Date().toISOString()
                });
                console.log('Transcript:', transcript);
            }
        };
        reader.readAsArrayBuffer(audioBlob);
    }

    /**
     * Detects when a question is asked
     */
    detectQuestion(text) {
        // Simple heuristic: if text ends with "?" it's likely a question
        if (text.trim().endsWith('?')) {
            this.currentQuestion = text;
            console.log('Question detected:', text);
            return true;
        }
        return false;
    }

    /**
     * Gets AI assistance for the current question
     */
    async getAssistance() {
        if (!this.currentQuestion) {
            console.warn('No question detected');
            return null;
        }

        const context = `Interview: ${this.interviewContext.title}`;
        const assistance = await getAIAssist(this.currentQuestion, context);
        return assistance;
    }

    /**
     * Saves the interview summary
     */
    async saveInterviewSummary() {
        const summary = {
            title: this.interviewContext.title,
            startTime: this.interviewContext.startTime,
            endTime: new Date().toISOString(),
            questionsAsked: this.interviewContext.questions.length,
            answers: this.interviewContext.answers
        };
        console.log('Interview Summary:', summary);
        // In production, send this to the backend for storage
        return summary;
    }

    /**
     * Initializes the interview session
     */
    initializeInterview(title, interviewers = []) {
        this.interviewContext.title = title;
        this.interviewContext.interviewers = interviewers;
        this.interviewContext.startTime = new Date().toISOString();
        console.log('Interview initialized:', this.interviewContext);
    }

    /**
     * Adds a question to the interview context
     */
    addQuestion(question) {
        this.interviewContext.questions.push({
            question: question,
            timestamp: new Date().toISOString()
        });
    }

    /**
     * Gets interview statistics
     */
    getStatistics() {
        return {
            totalQuestions: this.interviewContext.questions.length,
            totalAnswers: this.interviewContext.answers.length,
            duration: this.interviewContext.startTime ? 
                (new Date() - new Date(this.interviewContext.startTime)) / 1000 : 0,
            interviewers: this.interviewContext.interviewers.length
        };
    }
}

// Create global instance
const interviewAssistant = new InterviewAssistant();

// Example usage and event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Setup interview controls if they exist
    const startRecordingBtn = document.getElementById('startRecording');
    const stopRecordingBtn = document.getElementById('stopRecording');
    const getAssistanceBtn = document.getElementById('getAssistance');

    if (startRecordingBtn) {
        startRecordingBtn.addEventListener('click', () => {
            interviewAssistant.startRecording();
        });
    }

    if (stopRecordingBtn) {
        stopRecordingBtn.addEventListener('click', () => {
            interviewAssistant.stopRecording();
        });
    }

    if (getAssistanceBtn) {
        getAssistanceBtn.addEventListener('click', async () => {
            const assistance = await interviewAssistant.getAssistance();
            if (assistance) {
                console.log('AI Assistance:', assistance);
                // Display assistance to user
            }
        });
    }
});
