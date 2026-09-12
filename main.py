import pandas as pd

# Load job dataset
jobs = pd.read_csv("jobs.csv")


# Normalize skill names
def normalize_skill(skill):
    return skill.strip().lower()


# Get student skills
student_input = input(
    "Enter your skills separated by commas: "
)

student_skills = set(
    normalize_skill(skill)
    for skill in student_input.split(",")
)


# Display available jobs
print("\n==========================================")
print("          AVAILABLE JOB ROLES")
print("==========================================")

for index, row in jobs.iterrows():
    print(f"{index + 1}. {row['job_role']}")


# Select job
choice = int(input("\nChoose a job number: "))

selected_job = jobs.iloc[choice - 1]

job_role = selected_job["job_role"]

required_skills = set(
    normalize_skill(skill)
    for skill in selected_job["required_skills"].split(",")
)


# Compare skills
matched_skills = student_skills.intersection(required_skills)

missing_skills = required_skills - student_skills


# Calculate match percentage
match_percentage = (
    len(matched_skills) / len(required_skills)
) * 100


# Display result
print("\n==========================================")
print("             SKILL GAP ANALYSIS")
print("==========================================")

print(f"\nJob Role: {job_role}")

print("\nRequired Skills:")
print(", ".join(required_skills))

print("\nYour Matched Skills:")
print(", ".join(matched_skills) if matched_skills else "None")

print("\nMissing Skills:")
print(", ".join(missing_skills) if missing_skills else "None")

print(f"\nSkill Match: {match_percentage:.2f}%")


# Career recommendations
print("\n==========================================")
print("        CAREER RECOMMENDATIONS")
print("==========================================")

recommendations = []

for _, job in jobs.iterrows():

    job_skills = set(
        normalize_skill(skill)
        for skill in job["required_skills"].split(",")
    )

    matched = student_skills.intersection(job_skills)

    percentage = (
        len(matched) / len(job_skills)
    ) * 100

    recommendations.append(
        (job["job_role"], percentage)
    )


# Sort by highest match
recommendations.sort(
    key=lambda x: x[1],
    reverse=True
)


print("\nTop 5 Suitable Careers:")

for i, (role, percentage) in enumerate(
    recommendations[:5], 1
):
    print(
        f"{i}. {role} - {percentage:.2f}% match"
    )


print("\n==========================================")
print("        SKILLS TO LEARN")
print("==========================================")

if missing_skills:
    print(", ".join(missing_skills))
else:
    print("You have all required skills!")

print("\nAnalysis completed successfully! ✅")