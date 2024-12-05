import re
from spellchecker import SpellChecker

def tokenize_text(text):
    """
    Tokenizes and validates words in the input text.

    Args:
        text (str): The text to be tokenized.

    Returns:
        dict: Contains lists of valid/invalid words and their counts.
    """
    try:
        # Initialize spell checker
        spell = SpellChecker()
        
        # Split text into words
        words = text.split()
        
        # Separate valid and invalid words
        valid_words = []
        invalid_words = []
        
        for word in words:
            # Remove punctuation
            cleaned_word = re.sub(r'[^\w]', '', word)
            
            # Skip empty strings
            if not cleaned_word:
                continue
            
            # Check if the word is valid using the spell checker
            if spell.correction(cleaned_word.lower()) == cleaned_word.lower() and cleaned_word.lower() in spell:
                valid_words.append(cleaned_word)
            else:
                invalid_words.append(cleaned_word)
        
        stats = {
            'valid_words': valid_words,
            'invalid_words': invalid_words,
            'valid_count': len(valid_words),
            'invalid_count': len(invalid_words),
            'total_count': len(words)
        }
        
        return stats
    
    except Exception as e:
        print(f"Error during tokenization: {e}")
        return {
            'valid_words': [],
            'invalid_words': [],
            'valid_count': 0,
            'invalid_count': 0,
            'total_count': 0
        }

if __name__ == "__main__":
    # Example text with mixed valid/invalid words
    text = "The catched fish was laying on the table, where it waited to be cooked. Its colorful scales were shinning brightly under the lamp. The chef, who had studied cookery in Paris, said that the fish was definatly fresh and would make an excellent soup."
    
    # Process text
    stats = tokenize_text(text)
    
    # Print results
    print(f"Valid Words: {stats['valid_words']}")
    print(f"Invalid Words: {stats['invalid_words']}")
    print(f"Valid Word Count: {stats['valid_count']}")
    print(f"Invalid Word Count: {stats['invalid_count']}")
    print(f"Total Words: {stats['total_count']}")
