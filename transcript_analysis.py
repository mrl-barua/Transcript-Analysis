from collections import Counter
from spellchecker import SpellChecker
import re
import csv

spell = SpellChecker()

def process_text(input_text):
    """Process multi-line input text."""
    text_data = {}
    
    lines = input_text.strip().split("\n")
    previous_timestamp = None
    text = ""
    
    for line in lines:
        if '-->' in line:
            if previous_timestamp is not None and text.strip():
                text_data[previous_timestamp] = text.strip()
            previous_timestamp = line.strip()
            text = ""
        else:
            text += " " + line.strip()
    
    if previous_timestamp is not None and text.strip():
        text_data[previous_timestamp] = text.strip()
    
    return text_data

def detect_inaccurate_words(transcribed_words):
    """Detect inaccurate words using spelling check and common error patterns."""
    inaccurate_words = []
    
    for word in transcribed_words:
        word_cleaned = re.sub(r'[^\w\s]', '', word)
        
        if word_cleaned and not spell.correction(word_cleaned) == word_cleaned:
            inaccurate_words.append(word)
    
    return inaccurate_words

def analyze_transcripts(input_text):
    """Analyze transcripts and detect inaccuracies."""
    results = []
    total_accurate = total_inaccurate = total_words = 0
    
    try:
        text_data = process_text(input_text)
    except Exception as e:
        return {"line_analysis": [], "file_metrics": {"error": f"Error processing input text: {e}"}}
        
    for timestamp, transcript in text_data.items():
        try:
            transcribed_words = transcript.split()
            
            if not transcribed_words:
                continue

            inaccurate_words = detect_inaccurate_words(transcribed_words)
            
            accurate_words = len(transcribed_words) - len(inaccurate_words)
            inaccurate_word_count = len(inaccurate_words)
            total_accurate += accurate_words
            total_inaccurate += inaccurate_word_count
            total_words += len(transcribed_words)
            
            accuracy_score = (accurate_words / len(transcribed_words)) if transcribed_words else 0
            accuracy_percentage = (accuracy_score * 100) if total_words else 0
            
            results.append({
                "timestamp": timestamp,
                "transcript": transcript,
                "accurate_words": accurate_words,
                "inaccurate_words": inaccurate_word_count,
                "accuracy_score": round(accuracy_score, 2),
                "accuracy_percentage": round(accuracy_percentage, 2)
            })
            
        except Exception as e:
            continue
    
    if not total_words:
        return {"line_analysis": [], "file_metrics": {"error": "No valid words processed"}}
        
    overall_score = (total_accurate / total_words) if total_words else 0
    overall_percentage = (overall_score * 100) if total_words else 0
    
    return {
        "line_analysis": results,
        "file_metrics": {
            "total_words": total_words,
            "total_accurate": total_accurate,
            "total_inaccurate": total_inaccurate,
            "overall_score": round(overall_score, 2),
            "overall_percentage": round(overall_percentage, 2)
        }
    }

def print_analysis(analysis):
    """Print analysis results in a structured format."""
    if 'error' in analysis['file_metrics']:
        print(f"\033[91mError: {analysis['file_metrics']['error']}\033[0m") 
        return
    
    print("\n\033[1mAnalysis Summary\033[0m:")
    print(f"Total Words: {analysis['file_metrics']['total_words']}")
    print(f"Accurate Words: {analysis['file_metrics']['total_accurate']}")
    print(f"Inaccurate Words: {analysis['file_metrics']['total_inaccurate']}")
    print(f"Overall Accuracy Score: {analysis['file_metrics']['overall_score']} (Percentage: {analysis['file_metrics']['overall_percentage']}%)")
    
    print("\n\033[1mDetailed Line Analysis\033[0m:")
    for line in analysis["line_analysis"]:
        print(f"\nTimestamp: \033[94m{line['timestamp']}\033[0m")
        print(f"Transcript: {line['transcript']}")
        print(f"Accurate Words: {line['accurate_words']}")
        print(f"Inaccurate Words: {line['inaccurate_words']}")
        print(f"Accuracy Score: {line['accuracy_score']} (Percentage: {line['accuracy_percentage']}%)")
    
def save_analysis_to_csv(analysis, filename="analysis_results.csv"):
    """Save the analysis to a file in CSV format."""
    try:
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = [
                'Timestamp', 'Transcript', 'Accurate Words', 'Inaccurate Words', 
                'Accuracy Score', 'Accuracy Percentage'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for line in analysis["line_analysis"]:
                writer.writerow({
                    'Timestamp': line['timestamp'],
                    'Transcript': line['transcript'],
                    'Accurate Words': line['accurate_words'],
                    'Inaccurate Words': line['inaccurate_words'],
                    'Accuracy Score': line['accuracy_score'],
                    'Accuracy Percentage': line['accuracy_percentage']
                })

            writer.writerow({
                'Timestamp': 'Overall',
                'Transcript': '',
                'Accurate Words': analysis['file_metrics']['total_accurate'],
                'Inaccurate Words': analysis['file_metrics']['total_inaccurate'],
                'Accuracy Score': analysis['file_metrics']['overall_score'],
                'Accuracy Percentage': analysis['file_metrics']['overall_percentage']
            })
        
        print(f"\033[92mAnalysis saved to {filename}\033[0m")
    except Exception as e:
        print(f"\033[91mError saving analysis to file: {e}\033[0m")  

if __name__ == "__main__":
    try:
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
        """
        
        analysis = analyze_transcripts(input_text)
        
        if analysis:
            print_analysis(analysis)
            save_analysis_to_csv(analysis)  
    
    except Exception as e:
        print(f"\033[91mError: {e}\033[0m")  # Red color for errors
