import pandas as pd
import numpy as np


def clean_student_data(file_path):
    """
    Import and clean student preference data into a dictionary structure.

    Args:
        file_path (str): Path to the CSV file

    Returns:
        dict: Dictionary with student data
    """
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Initialize the student dictionary
    students = {}

    # Process each row
    for _, row in df.iterrows():
        student = row["student"].strip()  # Remove any whitespace

        # Get preferences (all columns that start with 'preferences')
        pref_cols = [col for col in row.index if col.startswith("preferences")]
        preferences = [p for p in row[pref_cols] if pd.notna(p)]

        # Get blocks (all columns that start with 'blocks')
        block_cols = [col for col in row.index if col.startswith("blocks")]
        blocks = [b for b in row[block_cols] if pd.notna(b)]

        # Determine commitment level
        if pd.notna(row["1"]):
            commitment = 1
        elif pd.notna(row["2"]):
            commitment = 2
        elif pd.notna(row["3"]):
            commitment = 3
        else:
            commitment = None

        # Add to dictionary
        students[student] = {
            "preferences": preferences,
            "blocks": blocks,
            "commitment": commitment,
        }

    return students


def export_to_csv(student_data, output_file):
    """
    Export the student data dictionary back to CSV format

    Args:
        student_data (dict): Dictionary containing student data
        output_file (str): Path to save the CSV file
    """
    # Find maximum number of preferences and blocks
    max_prefs = max(len(data["preferences"]) for data in student_data.values())
    max_blocks = max(len(data["blocks"]) for data in student_data.values())

    # Create column names
    pref_cols = [
        f"First preference,{i}" if i > 0 else "First preference" for i in range(max_prefs)
    ]
    block_cols = [f"First block,{i}" if i > 0 else "First block" for i in range(max_blocks)]

    # Create empty DataFrame with all necessary columns
    df = pd.DataFrame(columns=["code", "name", "cateogry"] + pref_cols + block_cols)

    # Fill in data for each student
    for student, data in student_data.items():
        row_data = {"code":"", "name": student, "category":""}

        # Fill in preferences
        for i, pref in enumerate(data["preferences"]):
            row_data[pref_cols[i]] = pref

        # Fill in blocks
        for i, block in enumerate(data["blocks"]):
            row_data[block_cols[i]] = block

        df = pd.concat([df, pd.DataFrame([row_data])], ignore_index=True)

    # Save to CSV
    df.to_csv(output_file, index=False)
    return df


def get_non_blocked_same_commitment(data, commitments, black_list=[]):
    non_blocked_same_commitment = []

    for same_commitment_student in commitments[data["commitment"] - 1]:
        if not same_commitment_student in data["blocks"] and not same_commitment_student in black_list:
            non_blocked_same_commitment.append(same_commitment_student)

    return non_blocked_same_commitment


def split_same_commitment_by_preference(data, same_commitment):
    preferred = []
    non_preferred = []
    for same_committed_student in same_commitment:
        if same_committed_student in data["preferences"]:
            preferred.append(same_committed_student)
        else:
            non_preferred.append(same_committed_student)
    return preferred, non_preferred


# Example usage
if __name__ == "__main__":
    input_file_path = "Copy of Anonymized Data for Harrison - Preferences #2.csv"
    output_file_path = "processed_preferences.csv"

    black_list = ["EFGH"]

    student_data = clean_student_data(input_file_path)

    commitments = [[] for _ in range(3)]  # idx 0 is 1, idx 1 is 2, idx 2 is 3

    for student, data in student_data.items():
        commitments[data["commitment"] - 1].append(student)

    for student, data in student_data.items():
        non_blocked_same_commitment = get_non_blocked_same_commitment(data, commitments, black_list=[student, *black_list])
        print(student in non_blocked_same_commitment)
        preferred, non_preferred = split_same_commitment_by_preference(
            data, non_blocked_same_commitment
        )
        new_preferred = [*preferred, *non_preferred]
        for preferred_student in data["preferences"]:
            if (
                not preferred_student in preferred
                and not preferred_student in non_preferred
                and not preferred_student in [student, *black_list]
            ):
                new_preferred.append(preferred_student)
        student_data[student]["preferences"] = new_preferred

    for black_listed_student in black_list:
        del student_data[black_listed_student]

    print(student_data)
    export_to_csv(student_data, output_file_path)
