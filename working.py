from collections import Counter
from spellchecker import SpellChecker
import re

# Initialize the spell checker
spell = SpellChecker()

def process_text(input_text):
    """Process multi-line input text."""
    text_data = {}
    
    # Split the input into lines and process each one
    lines = input_text.strip().split("\n")
    previous_timestamp = None
    text = ""
    
    for line in lines:
        # Check for timestamp lines (e.g., 34.9 --> 60.9)
        if '-->' in line:
            if previous_timestamp is not None and text.strip():
                # Store previous text data
                text_data[previous_timestamp] = text.strip()
            # Update the current timestamp and reset text
            previous_timestamp = line.strip()
            text = ""
        else:
            # Accumulate transcript for each timestamp
            text += " " + line.strip()
    
    # Add the last accumulated line
    if previous_timestamp is not None and text.strip():
        text_data[previous_timestamp] = text.strip()
    
    return text_data

def detect_inaccurate_words(transcribed_words):
    """Detect inaccurate words using spelling check and common error patterns."""
    inaccurate_words = []
    
    for word in transcribed_words:
        # Ignore punctuation marks
        word_cleaned = re.sub(r'[^\w\s]', '', word)
        
        if word_cleaned and not spell.correction(word_cleaned) == word_cleaned:
            inaccurate_words.append(word)
    
    return inaccurate_words

def analyze_transcripts(input_text):
    """Analyze transcripts and detect inaccuracies."""
    results = []
    total_accurate = total_inaccurate = total_words = 0
    duplicates = []
    
    try:
        text_data = process_text(input_text)
    except Exception as e:
        print(f"Error processing input text: {e}")
        return {"line_analysis": [], "file_metrics": {"error": str(e)}}
        
    seen_lines = Counter()
    for timestamp, transcript in text_data.items():
        try:
            print(f"Processing text: {transcript}")  # Debugging statement
            
            # Split the transcript into words
            transcribed_words = transcript.split()
            print(f"Transcribed words: {transcribed_words}")  # Debugging statement
            
            if not transcribed_words:
                print(f"No transcribed words for text: {transcript}")  # Debugging statement
                continue
            
            # Detect inaccurate words based on spelling and common patterns
            inaccurate_words = detect_inaccurate_words(transcribed_words)
            
            total_inaccurate += len(inaccurate_words)
            total_words += len(transcribed_words)
            
            accuracy_score = (len(transcribed_words) - len(inaccurate_words)) / len(transcribed_words) if transcribed_words else 0
            
            results.append({
                "timestamp": timestamp,
                "transcript": transcript,
                "accuracy_score": round(accuracy_score, 2),
                "accurate_words": len(transcribed_words) - len(inaccurate_words),
                "inaccurate_words": len(inaccurate_words),
                "inaccurate_words_list": inaccurate_words,
                "duplicated": transcript in duplicates
            })
            
        except Exception as e:
            print(f"Error processing line: {e}")
            continue
    
    if not total_words:
        return {"line_analysis": [], "file_metrics": {"error": "No valid words processed"}}
        
    overall_score = (total_words - total_inaccurate) / total_words if total_words else 0
    
    return {
        "line_analysis": results,
        "file_metrics": {
            "total_words": total_words,
            "total_accurate": total_words - total_inaccurate,
            "total_inaccurate": total_inaccurate,
            "overall_score": round(overall_score, 2),
            "duplicates": duplicates
        }
    }

if __name__ == "__main__":
    try:
        # Example multi-line text input
        input_text = """
        34.9 --> 60.9
        Student: Hi, how are you?
        
        54.7 --> 55.7
        Tutor: Hello?
        
        55.7 --> 58.7
        Tutor: I'm grate, thank you.
        
        58.7 --> 61.7
        Tutor: How are you doing?
        
        60.9 --> 70.9
        Student: Good, thanx you.
        
        61.7 --> 62.7
        Tutor: Awsome.
        
        62.7 --> 63.7
        Tutor: Amzing.
        """

        analysis = analyze_transcripts(input_text)
        
        if analysis:
            print("Analysis Results:")
            if 'error' in analysis['file_metrics']:
                print(f"Error: {analysis['file_metrics']['error']}")
            else:
                print(f"Total Words: {analysis['file_metrics']['total_words']}")
                print(f"Accurate Words: {analysis['file_metrics']['total_accurate']}")
                print(f"Inaccurate Words: {analysis['file_metrics']['total_inaccurate']}")
                print(f"Overall Score: {analysis['file_metrics']['overall_score']}")
                for line in analysis["line_analysis"]:
                    print(f"Timestamp: {line['timestamp']}")
                    print(f"Inaccurate Words: {line['inaccurate_words_list']}")
    except Exception as e:
        print(f"Error: {e}")
