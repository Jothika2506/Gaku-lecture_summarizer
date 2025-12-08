import os
import assemblyai as aai
from dotenv import load_dotenv

load_dotenv()

class Transcriber:
    def __init__(self):
        """Initialize the transcriber with AssemblyAI API key"""
        self.api_key = os.getenv('ASSEMBLYAI_API_KEY')
        if not self.api_key:
            raise ValueError("ASSEMBLYAI_API_KEY not found in environment variables")
        
        aai.settings.api_key = self.api_key
        print("✅ AssemblyAI transcriber initialized")
    
    def transcribe_audio(self, audio_file_path):
        """
        Transcribe audio file to text using AssemblyAI
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            dict: Contains 'text', 'words' (with timestamps), 'duration' and 'status'
        """
        try:
            print(f"🎤 Starting transcription for: {audio_file_path}")
            
            # Check if file exists
            if not os.path.exists(audio_file_path):
                return {
                    'status': 'error',
                    'text': None,
                    'words': None,
                    'duration': None,
                    'error': 'Audio file not found'
                }
            
            # Get file size
            file_size = os.path.getsize(audio_file_path)
            print(f"📁 File size: {file_size / (1024*1024):.2f}MB")
            
            # Configure transcriber with optimal settings
            config = aai.TranscriptionConfig(
                speaker_labels=False,  # Don't need speaker identification for lectures
                punctuate=True,        # Add punctuation
                format_text=True,      # Format the text nicely
                word_boost=[],         # Can add technical terms here if needed
                boost_param="default"  # default, low, or high
            )
            
            # Create transcriber and transcribe
            transcriber = aai.Transcriber(config=config)
            print("⏳ Uploading and transcribing audio...")
            transcript = transcriber.transcribe(audio_file_path)
            
            # Check if transcription was successful
            if transcript.status == aai.TranscriptStatus.error:
                print(f"❌ Transcription error: {transcript.error}")
                return {
                    'status': 'error',
                    'text': None,
                    'words': None,
                    'duration': None,
                    'error': transcript.error or 'Transcription failed'
                }
            
            # Extract word-level timestamps (optional - can be used for navigation)
            words_with_timestamps = []
            if hasattr(transcript, 'words') and transcript.words:
                # Only store first 100 words with timestamps to avoid large payload
                for word in transcript.words[:100]:
                    words_with_timestamps.append({
                        'text': word.text,
                        'start': word.start,  # milliseconds
                        'end': word.end,
                        'confidence': word.confidence
                    })
            
            # Get audio duration if available
            duration = None
            if hasattr(transcript, 'audio_duration'):
                duration = transcript.audio_duration  # in milliseconds
                print(f"⏱️ Audio duration: {duration / 1000:.1f} seconds")
            
            # Get transcript text
            text = transcript.text
            word_count = len(text.split())
            
            print(f"✅ Transcription completed successfully!")
            print(f"📝 Word count: {word_count}")
            print(f"📏 Character count: {len(text)}")
            
            return {
                'status': 'success',
                'text': text,
                'words': words_with_timestamps,  # First 100 words with timestamps
                'duration': duration,
                'word_count': word_count,
                'error': None
            }
            
        except Exception as e:
            print(f"❌ Error during transcription: {str(e)}")
            return {
                'status': 'error',
                'text': None,
                'words': None,
                'duration': None,
                'error': str(e)
            }
    
    def transcribe_from_url(self, audio_url):
        """
        Transcribe audio from URL
        
        Args:
            audio_url: URL of the audio file
            
        Returns:
            dict: Contains 'text' (transcription) and 'status' (success/error)
        """
        try:
            print(f"🌐 Starting transcription from URL: {audio_url}")
            
            config = aai.TranscriptionConfig(
                speaker_labels=False,
                punctuate=True,
                format_text=True
            )
            
            transcriber = aai.Transcriber(config=config)
            transcript = transcriber.transcribe(audio_url)
            
            if transcript.status == aai.TranscriptStatus.error:
                print(f"❌ Transcription error: {transcript.error}")
                return {
                    'status': 'error',
                    'text': None,
                    'error': transcript.error or 'Transcription failed'
                }
            
            print("✅ Transcription completed successfully!")
            print(f"📝 Word count: {len(transcript.text.split())}")
            
            return {
                'status': 'success',
                'text': transcript.text,
                'error': None
            }
            
        except Exception as e:
            print(f"❌ Error during transcription: {str(e)}")
            return {
                'status': 'error',
                'text': None,
                'error': str(e)
            }