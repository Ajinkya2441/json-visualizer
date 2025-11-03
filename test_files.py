import pandas as pd
import os

# Test all file formats
files_to_test = [
    "sample_data.csv",
    "sample_data.xlsx", 
    "sample_data.parquet",
    "sample_data.tsv"
]

print("Testing file reading capabilities:")
print("=" * 50)

for file_name in files_to_test:
    file_path = os.path.join("c:\\Users\\Ajinkya\\Desktop\\csv_visualization", file_name)
    
    if os.path.exists(file_path):
        try:
            if file_name.endswith(".csv"):
                df = pd.read_csv(file_path)
                print(f"✓ {file_name}: SUCCESS - Shape {df.shape}")
            elif file_name.endswith(".xlsx") or file_name.endswith(".xls"):
                df = pd.read_excel(file_path)
                print(f"✓ {file_name}: SUCCESS - Shape {df.shape}")
            elif file_name.endswith(".parquet"):
                df = pd.read_parquet(file_path)
                print(f"✓ {file_name}: SUCCESS - Shape {df.shape}")
            elif file_name.endswith(".tsv"):
                df = pd.read_csv(file_path, sep='\t')
                print(f"✓ {file_name}: SUCCESS - Shape {df.shape}")
        except Exception as e:
            print(f"✗ {file_name}: FAILED - {str(e)}")
    else:
        print(f"✗ {file_name}: NOT FOUND")

print("=" * 50)
print("Test completed.")