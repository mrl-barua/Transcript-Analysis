from collections import Counter

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

def analyze_transcripts(input_text):
    """Analyze transcripts accuracy."""
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
            
            # Here you would add the logic to compare the transcript with a reference document (docx)
            # For simplicity, I'm assuming the accuracy check is just based on word counts
            transcribed_words = transcript.split()
            print(f"Transcribed words: {transcribed_words}")  # Debugging statement
            
            if not transcribed_words:
                print(f"No transcribed words for text: {transcript}")  # Debugging statement
                continue
                
            accurate_words = len(transcribed_words)  # Placeholder for accurate word count
            inaccurate_words = 0  # Placeholder for inaccurate word count
            
            total_accurate += accurate_words
            total_inaccurate += inaccurate_words
            total_words += len(transcribed_words)
            
            accuracy_score = accurate_words / len(transcribed_words) if transcribed_words else 0
            
            results.append({
                "timestamp": timestamp,
                "transcript": transcript,
                "accuracy_score": round(accuracy_score, 2),
                "accurate_words": accurate_words,
                "inaccurate_words": inaccurate_words,
                "duplicated": transcript in duplicates
            })
            
        except Exception as e:
            print(f"Error processing line: {e}")
            continue
    
    if not total_words:
        return {"line_analysis": [], "file_metrics": {"error": "No valid words processed"}}
        
    overall_score = total_accurate / total_words if total_words else 0
    
    return {
        "line_analysis": results,
        "file_metrics": {
            "total_words": total_words,
            "total_accurate": total_accurate,
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
        Tutor: I'm great, thank you.
        
        58.7 --> 61.7
        Tutor: How are you doing?
        
        60.9 --> 70.9
        Student: Good, thank you.
        
        61.7 --> 62.7
        Tutor: Awesome.
        
        62.7 --> 63.7
        Tutor: Amazing.
        """

        analysis = analyze_transcripts(input_text)
        
        if analysis:
            print("Analysis Results:")
            if 'error' in analysis['file_metrics']:
                print(f"Error: {analysis['file_metrics']['error']}")
            else:
                print(f"Total Words: {analysis['file_metrics']['total_words']}")
                print(f"Accurate Words: {analysis['file_metrics']['total_accurate']}")
                print(f"Overall Score: {analysis['file_metrics']['overall_score']}")
    except Exception as e:
        print(f"Error: {e}")
