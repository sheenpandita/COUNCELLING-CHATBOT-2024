import pandas as pd
import matplotlib.pyplot as plt

# Sample data (replace with actual data source)
data = {
    "Career": ["Data Scientist", "Software Engineer", "Cybersecurity Analyst", "Marketing Manager", "Registered Nurse"],
    "Job Openings": [150000, 200000, 100000, 80000, 120000]
}

# Create Pandas DataFrame
df = pd.DataFrame(data)

# Calculate percentages (optional, for visual emphasis)
total_openings = df["Job Openings"].sum()
df["Percentage"] = (df["Job Openings"] / total_openings) * 100

# Create a bar chart
plt.figure(figsize=(8, 6))
plt.bar(df["Career"], df["Job Openings"])
plt.xlabel("Career")
plt.ylabel("Job Openings (Estimated)")
plt.title("Popularity of Selected Careers")
plt.xticks(rotation=45)  # Rotate x-axis labels for readability

# Save the plot as an image
plt.tight_layout()
plt.savefig("career_popularity.png", dpi=300)  # Adjust DPI for image quality