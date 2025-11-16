# AI Voice Counselor Module
# Uses browser Web Speech API - No external API keys required
# Provides human-like voice responses without dependencies

class AIVoiceCounselor:
    """
    AI Voice Counselor that provides spoken guidance without API keys.
    Uses browser's native Web Speech API for text-to-speech.
    """
    
    def __init__(self):
        self.responses = {
            'greeting': [
                'नमस्कार! आपले स्वागत आहे एडमिशनवाला येथे!',
                'Hello! Welcome to AdmitionWala, your education guidance platform!',
                'मी आपला आभासी सल्लागार आहे. कृपया आपली माहिती सांगा.',
                'I am your virtual counselor. Please tell me about your educational interests.'
            ],
            'interest': [
                'तुमचे शिक्षणात्मक क्षेत्र काय आहे?',
                'What is your field of interest?',
                'आप किस विषय में रुचि रखते हैं?',
                'Which stream are you interested in?'
            ],
            'location': [
                'आप कोणत्या शहरात शिक्षण घेऊ शकता?',
                'Which city would you prefer for your studies?',
                'आप किस शहर में अध्ययन करना चाहते हैं?',
                'What location do you prefer?'
            ],
            'budget': [
                'आपचे शिक्षण खर्चाचे अंदाजे बजेट काय आहे?',
                'What is your estimated budget for education?',
                'आपका शिक्षा बजट क्या है?',
                'What is your education budget?'
            ],
            'recommendation': [
                'आपके लिए सर्वश्रेष्ठ कॉलेज हैं: {college_name}। यह कॉलेज {location} में स्थित है।',
                'Based on your preferences, I recommend: {college_name} in {location}.',
                'आपच्या आवश्यकतांनुसार मी {college_name} ची शिफारस करतो.',
                'For your needs, {college_name} would be an excellent choice!'
            ],
            'courses': [
                'उपलब्ध कोर्स हैं: {courses}',
                'Available courses include: {courses}',
                'या कॉलेजमध्ये खालील कोर्स उपलब्ध आहेत: {courses}',
                'The courses offered are: {courses}'
            ],
            'closing': [
                'धन्यवाद! आपले साक्षात्कार संपले। कृपया लागू करा।',
                'Thank you for using our counseling service. Good luck with your applications!',
                'आपकी सहायता करने के लिए धन्यवाद। शुभकामनाएं!',
                'Best of luck with your education journey!'
            ]
        }

    def get_greeting(self, language='en'):
        """Get a welcome greeting"""
        if language.lower() == 'mr':
            return self.responses['greeting'][0]
        elif language.lower() == 'hi':
            return self.responses['greeting'][2]
        return self.responses['greeting'][1]

    def get_recommendation_text(self, college_name, location, courses=None):
        """Generate recommendation text"""
        text = f"Based on your preferences, I recommend {college_name} in {location}. "
        if courses:
            text += f"Available courses include {', '.join(courses[:3])}. "
        text += "This is an excellent institution with good infrastructure and faculty. Good luck with your application!"
        return text

    def generate_response(self, user_input, context=None):
        """Generate AI counselor response based on user input"""
        user_input = user_input.lower().strip()
        
        if any(word in user_input for word in ['hello', 'hi', 'start', 'नमस्कार', 'शुरुआत']):
            return self.responses['greeting'][1]
        elif any(word in user_input for word in ['interest', 'stream', 'field', 'रुचि', 'क्षेत्र']):
            return self.responses['interest'][1]
        elif any(word in user_input for word in ['location', 'city', 'place', 'शहर', 'ठिकाण']):
            return self.responses['location'][1]
        elif any(word in user_input for word in ['budget', 'cost', 'fee', 'खर्च', 'बजेट']):
            return self.responses['budget'][1]
        elif any(word in user_input for word in ['college', 'recommend', 'suggest', 'कॉलेज', 'सुझाव']):
            return "Based on your profile, here are the best colleges matching your criteria. Click to view details."
        else:
            return "Thank you for the information. Please continue by answering the next question or contact us for more details."

    @staticmethod
    def text_to_speech_javascript():
        """Return JavaScript code for text-to-speech functionality"""
        return """
        <script>
        // AI Voice Counselor - Text to Speech Module
        window.AIVoice = {
            isSpeaking: false,
            lang: 'en-US',
            
            speak: function(text, lang = 'en-US', rate = 0.95, pitch = 1.0) {
                if (!('speechSynthesis' in window)) {
                    console.warn('Speech Synthesis not supported');
                    return;
                }
                
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = lang;
                utterance.rate = rate;
                utterance.pitch = pitch;
                utterance.volume = 0.9;
                
                utterance.onstart = function() {
                    window.AIVoice.isSpeaking = true;
                };
                
                utterance.onend = function() {
                    window.AIVoice.isSpeaking = false;
                };
                
                utterance.onerror = function(event) {
                    console.error('Speech synthesis error:', event.error);
                    window.AIVoice.isSpeaking = false;
                };
                
                window.speechSynthesis.speak(utterance);
            },
            
            speakMarathi: function(text) {
                this.speak(text, 'mr-IN', 0.85, 0.8);
            },
            
            speakHindi: function(text) {
                this.speak(text, 'hi-IN', 0.85, 0.8);
            },
            
            speakEnglish: function(text) {
                this.speak(text, 'en-US', 0.95, 1.0);
            },
            
            stop: function() {
                window.speechSynthesis.cancel();
                this.isSpeaking = false;
            }
        };
        </script>
        """


def get_ai_voice_module():
    """Factory function to get AI Voice Counselor instance"""
    return AIVoiceCounselor()
