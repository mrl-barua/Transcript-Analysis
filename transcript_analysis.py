from spellchecker import SpellChecker
import re
import csv

spell = SpellChecker()

def process_text_line_by_line(filename):
    """Process text from a file line by line."""
    text_data = {}
    previous_timestamp = None
    text = ""

    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if '-->' in line:  # Timestamp line
                    if previous_timestamp and text.strip():
                        text_data[previous_timestamp] = text.strip()
                    previous_timestamp = line
                    text = ""
                else:  
                    text += " " + line

            if previous_timestamp and text.strip():
                text_data[previous_timestamp] = text.strip()
    except Exception as e:
        raise IOError(f"Error processing file: {e}")
    
    return text_data

def detect_inaccurate_words(transcribed_words, word_cache):
    """Detect inaccurate words using spelling check with caching."""
    inaccurate_words = []

    for word in transcribed_words:
        word_cleaned = re.sub(r'[^\w\s]', '', word)
        if word_cleaned:
            if word_cleaned in word_cache:
                is_accurate = word_cache[word_cleaned]
            else:
                is_accurate = spell.correction(word_cleaned) == word_cleaned
                word_cache[word_cleaned] = is_accurate

            if not is_accurate:
                inaccurate_words.append(word)
    
    return inaccurate_words

def analyze_transcripts(filename, csv_filename="analysis_results.csv"):
    """Analyze transcripts and write results to a CSV."""
    total_accurate = total_inaccurate = total_words = 0
    word_cache = {} 

    try:
        text_data = process_text_line_by_line(filename)
    except IOError as e:
        print(f"\033[91mError: {e}\033[0m")
        return

    try:
        with open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = [
                'Timestamp', 'Transcript', 'Accurate Words', 'Inaccurate Words',
                'Accuracy Score', 'Accuracy Percentage'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for timestamp, transcript in text_data.items():
                transcribed_words = transcript.split()
                if not transcribed_words:
                    continue

                inaccurate_words = detect_inaccurate_words(transcribed_words, word_cache)
                accurate_words = len(transcribed_words) - len(inaccurate_words)

                total_accurate += accurate_words
                total_inaccurate += len(inaccurate_words)
                total_words += len(transcribed_words)

                accuracy_score = (accurate_words / len(transcribed_words)) if transcribed_words else 0
                accuracy_percentage = accuracy_score * 100

                writer.writerow({
                    'Timestamp': timestamp,
                    'Transcript': transcript,
                    'Accurate Words': accurate_words,
                    'Inaccurate Words': len(inaccurate_words),
                    'Accuracy Score': round(accuracy_score, 2),
                    'Accuracy Percentage': round(accuracy_percentage, 2)
                })

            overall_score = (total_accurate / total_words) if total_words else 0
            overall_percentage = overall_score * 100
            writer.writerow({
                'Timestamp': 'Overall',
                'Transcript': '',
                'Accurate Words': total_accurate,
                'Inaccurate Words': total_inaccurate,
                'Accuracy Score': round(overall_score, 2),
                'Accuracy Percentage': round(overall_percentage, 2)
            })

        print(f"\033[92mAnalysis saved to {csv_filename}\033[0m")
    except Exception as e:
        print(f"\033[91mError writing CSV: {e}\033[0m")

if __name__ == "__main__":
    try:
        input_file = "Transcript.txt"
        output_file = "analysis_results.csv"
        analyze_transcripts(input_file, output_file)
    except Exception as e:
        print(f"\033[91mError: {e}\033[0m")
