import json
import csv


def json_to_csv(json_file, csv_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Open CSV file for writing
    with open(csv_file, 'w', newline='') as csvfile:
        # Define the column names
        fieldnames = ['question', 'answer', 'reference']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Process each question in the JSON file
        for question_data in data.get('questions', []):
            # Extract the question body
            question = question_data.get('body', '')

            # Extract the exact answer
            answer = question_data.get('exact_answer', '')

            # Concatenate all snippet texts for the reference
            snippets = question_data.get('snippets', [])
            reference = " ".join(snippet.get('text', '') for snippet in snippets)

            # Write the row to the CSV file
            writer.writerow({'question': question, 'answer': answer, 'reference': reference})

    print(f"Data has been successfully saved to {csv_file}")


# Replace 'input.json' with the path to your input JSON file
# Replace 'output.csv' with the desired output CSV file name
json_to_csv('/Users/ahhyun/Downloads/BioASQ-training12b/yesno_questions.json', '/Users/ahhyun/Downloads/BioASQ-training12b/output.csv')
