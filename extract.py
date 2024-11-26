from faker import Faker
import pandas as pd
from google.cloud import storage

def generate_employee_data(num_employees=100):
    """Generates employee data using Faker library, including last name, department, and passwords.

    Args:
        num_employees (int, optional): Number of employees to generate. Defaults to 100.

    Returns:
        pandas.DataFrame: DataFrame containing employee data.
    """

    fake = Faker()
    employees = []

    for _ in range(num_employees):
        employee = {
            'First Name': fake.first_name(),
            'Last Name': fake.last_name(),
            'Job Title': fake.job(),
            'Email': fake.email(),
            'Phone Number': fake.phone_number(),
            'Address': fake.address().replace('\n',' '),
            'Hire Date': fake.date_between(start_date='-5y', end_date='today'),
            'Salary': fake.random_int(min=30000, max=100000),
            'Department': fake.job(),  # Using job as a placeholder for department
            'Password': fake.password(length=10, special_chars=True)
        }
        employees.append(employee)

    df = pd.DataFrame(employees)
   
    return df

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to Google Cloud Storage.

    Args:
        bucket_name (str): The name of the bucket.
        source_file_name (str): The path to the source file.
        destination_blob_name (str): The name of the destination blob.
    """

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

if __name__ == '__main__':
    num_employees = 10
    employee_data = generate_employee_data(num_employees)
    

    #  Save to CSV
    csv_file = 'employees_data.csv'
    employee_data.to_csv(csv_file, index=False,)

    # Upload to GCS
    bucket_name = 'college_admissions'  # Replace with your bucket name
    destination_blob_name = 'employee_data.csv'
    project_name = 'centering-rider-337916'
    upload_to_gcs(bucket_name, csv_file, destination_blob_name)