import csv
from transformers import pipeline

# Load the Q&A model from Hugging Face
qa_model = pipeline("question-answering")

# Open the CSV file for reading
with open('entity_data.csv', 'r', newline='', encoding='utf-8') as csvfile:
    # Create a CSV reader
    reader = csv.reader(csvfile)

    # Skip the header row
    next(reader)

    # Open a new CSV file for writing the results
    with open('entity_data_with_answers.csv', 'w', newline='', encoding='utf-8') as outfile:
        # Create a CSV writer
        writer = csv.writer(outfile)

        # Loop through each row in the input CSV file
        for row in reader:
            # Get the context and entity from the row
            context = row[1]
            entity = row[0]

            # Generate a question for the entity and context
            question = f"Describe {entity}?".strip()

            # Generate an answer using the Q&A model
            answer = qa_model(question=question, context=context)

            # Write the original row plus the generated question and answer to the output CSV file
            writer.writerow([question, answer['answer']])
