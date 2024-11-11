import os
import logging
import shutil
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Custom Exception Classes
class FileNotFoundError(Exception):
    def __init__(self, file_name):
        self.file_name = file_name
        super().__init__(self.file_name)

    def __str__(self):
        return f"File not found: {self.file_name}"

class InvalidInputDataError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class DiskSpaceFullError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

# Set up logging
logging.basicConfig(filename='Lab-6/error_log.log', level=logging.ERROR)

# Function to read file
def read_file(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(file_path)

        with open(file_path, 'r') as file:
            data = file.read()
            if not isinstance(data, str):
                raise InvalidInputDataError("File contains non-string data.")
            return data

    except FileNotFoundError as e:
        logging.error(str(e))
        print(str(e))

    except InvalidInputDataError as e:
        logging.error(e.message)
        print(e.message)

# Function to count words
def count_words(text):
    return len(text.split())

# Function to calculate character frequency
def character_frequency(text):
    frequency = {}
    for char in text:
        if char.isalnum():  # Consider only alphanumeric characters
            frequency[char] = frequency.get(char, 0) + 1
    return frequency

# Function to get available disk space (in bytes)
def get_available_disk_space(directory):
    total, used, free = shutil.disk_usage(directory)
    return free

# Function to estimate the size of the output file
def estimate_output_size(word_count, char_frequency):
    estimated_size = word_count * 10  # Rough estimate: 10 bytes per word
    estimated_size += len(char_frequency) * 10  # Rough estimate: 10 bytes per char frequency entry
    return estimated_size

# Function to save results to a file
def save_results_to_file(output_file, word_count, char_frequency):
    try:
        output_directory = os.path.dirname(output_file) or '.'
        available_space = get_available_disk_space(output_directory)
        estimated_size = estimate_output_size(word_count, char_frequency)

        if available_space < estimated_size:
            raise DiskSpaceFullError("Insufficient disk space to save the file.")

        with open(output_file, 'w') as file:
            file.write(f"Number of words: {word_count}\n")
            file.write("Character frequencies:\n")
            for char, freq in char_frequency.items():
                file.write(f"{char}: {freq}\n")

    except DiskSpaceFullError as e:
        logging.error(e.message)
        print(e.message)
    except IOError as e:  # Catching general IO errors that might occur
        logging.error("Failed to save the file due to I/O error.")
        print("Failed to save the file due to I/O error.")

# Function to generate word cloud
def generate_word_cloud(text):
    wordcloud = WordCloud(width=800, height=400).generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig('Lab-6/wordcloud.jpg')
    plt.show()

# Main processing function
def process_text_file(file_path):
    text = read_file(file_path)

    if text:
        word_count = count_words(text)
        char_frequency = character_frequency(text)
        save_results_to_file('Lab-6/text_processing_output.txt', word_count, char_frequency)
        generate_word_cloud(text)
        print("The inputted text has been processed and the processed data has been saved in files")

# Example usage
if __name__ == "__main__":
    print("Rank Mansi")
    print("22BCP284")

    file_path = input("Enter the file path: ")
    try:
        process_text_file(file_path)
    except FileNotFoundError as e:
        print(f"Error occurred: {e}")
    except InvalidInputDataError as e:
        print(f"Error occurred: {e}")
    except DiskSpaceFullError as e:
        print(f"Error occurred: {e}")