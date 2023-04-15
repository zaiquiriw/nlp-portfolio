import openai
import csv

openai.api_key = "open-ai-key"

data = []

with open("entity_data.csv", "r") as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        data.append((row[0], row[1]))

print(data)

with open("output_file.csv", "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    for entity, context in data:
        prompt = f"Generate a question and answer pair about the entity {entity} using the context: \"{context}\". The question should be in the form of \"What is {entity}?\" and the answer should be formed from the context."

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            temperature=0.5,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        print(response.choices[0].text.strip())

        # Write the generated question and answer pairs to a new CSV file
        question, answer = response.choices[0].text.strip().split('?', 1)
        csv_writer.writerow([question.strip(), answer.strip()])
