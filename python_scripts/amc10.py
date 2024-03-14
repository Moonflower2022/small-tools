# Define the answer key for the AMC test (e.g., AMC 10/12A, 2023)
answer_key = "DDCBBCDADADCBBBCCCDDADCBE"
no_answer_symbol = "N"  # Symbol to denote "didn't answer"

def main():
    print("Welcome to the AMC Test Score Calculator!")
    student_answers = input("Enter your answers (e.g., ABCDEABCEDDAACABDCCD, use 'N' for didn't answer): ").strip()
    
    # Make sure the input is the correct length
    if len(student_answers) != len(answer_key):
        print("Error: The answer string is not the correct length.")
        return
    
    # Initialize variables to track the score
    correct_count = 0
    no_answer_count = 0
    total_questions = len(answer_key)
    wrong_problems = []

    # Compare student answers to the answer key and calculate the score
    for i in range(total_questions):
        student_answer = student_answers[i]
        if student_answer == no_answer_symbol:
            no_answer_count += 1
        elif student_answer == answer_key[i]:
            correct_count += 1
        else:
            wrong_problems.append(i + 1)

    # Calculate the score
    score = (correct_count * 6) + (no_answer_count * 1.5)  # Each correct answer is worth 6 points, each "didn't answer" is worth -1 point

    print(f"Your results: {correct_count}/{total_questions} ({correct_count}/{total_questions - no_answer_count} for questions you answered)")
    print(f"Total score: {score}")

    if wrong_problems:
        print("Wrong problems: {}".format(", ".join(map(str, wrong_problems))))

if __name__ == "__main__":
    main()