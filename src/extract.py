from faker import Faker
import random
import string
import pandas as pd
from google.cloud import storage

# Specify number of employees to generate
num_employees = 100

# Create Faker instance
fake = Faker()

# Employee data structure (without PII)
employee_data = []

# Define the character set for the password
password_characters = string.ascii_letters + string.digits + 'm'

for _ in range(num_employees):
    employee = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "job_title": fake.job(),
        "department": fake.job(),
        "email": fake.email(),
        "address": fake.address().replace("\n", ", "),
        "phone_number": fake.phone_number(),
        "salary": fake.random_number(digits=5),  # Generate a random 5-digit salary
        "password": ''.join(
            random.choice(password_characters)
            for _ in range(8)
        )  # Generate an 8-character password with 'm'
    }

    employee_data.append(employee)

# Convert to DataFrame
df = pd.DataFrame(employee_data)

# Save to CSV
csv_file = "employee_data.csv"

df.to_csv(
    csv_file,
    index=False,
    encoding="utf-8",
    sep=",",
    quotechar='"',
    lineterminator="\n"
)

print(f"CSV file created: {csv_file}")

# Upload to GCS bucket
bucket_name = "bukt-employee"

client = storage.Client()
bucket = client.bucket(bucket_name)

blob = bucket.blob(csv_file)
blob.upload_from_filename(csv_file)

print(f"File uploaded to GCS bucket: {bucket_name}/{csv_file}")