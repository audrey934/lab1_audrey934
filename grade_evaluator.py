import csv
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists, 
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")

    # Check if file exists
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
    else:
        print(f"The file: '{filename}' exists")

    assignments = []


    # Check if file has content and includes all necessary data
    required_fields = ['assignment', 'group', 'score', 'weight']

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            first_line = file.readline()
            if not first_line:
                print("Error: CSV file is empty.")
                sys.exit(1)

            file.seek(0)

            reader = csv.DictReader(file)

            # Check for missing columns
            missing_columns = [field for field in required_fields if field not in reader.fieldnames]
            if missing_columns:
                print(f"Error: Missing required column(s): {', '.join(missing_columns)}")
                sys.exit(1)

            # Data integrity check
            rows_exist = False
            for row in reader:
                rows_exist = True

                # Check missing values
                for field in required_fields:
                    if not row[field] or row[field].strip() == '':
                        print(f"Error: Missing value for '{field}' in row: {row}")
                        sys.exit(1)

                # Score and weight must be numeric
                try:
                    score = float(row['score'])
                    weight = float(row['weight'])
                except ValueError:
                    print(f"Error: Score or weight is not numeric in row: {row}")
                    sys.exit(1)

                # Group must be valid
                group = row['group'].strip().lower()
                if group not in ['formative', 'summative']:
                    print(f"Error: Invalid group '{row['group']}' in row: {row}")
                    sys.exit(1)

                # All checks passed → add to assignments
                assignments.append({
                    'assignment': row['assignment'].strip(),
                    'group': group,
                    'score': score,
                    'weight': weight
                })

            if not rows_exist:
                print("Error: CSV file does not have data rows.")
                sys.exit(1)

        return assignments

    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)
    

# Function to format numbers without unnecessary decimals(3.00 to 3)
def format_number(n):
    if n == int(n):
        return str(int(n))
    else:
        return str(round(n, 2))

def evaluate_grades(data):
    """
    Implement your logic here.
    'data' is a list of dictionaries containing the assignment records.
    """
    print("\n--- Academic Grade Evaluation ---")
    
    # Part I: Score Validation
    invalid_scores = [a for a in data if not (0 <= a['score'] <= 100)]
    if invalid_scores:
        print("\n[VALIDATION ERROR] The scores must be between 0-100:")
        for a in invalid_scores:
            print(f"  - {a['assignment']}: {a['score']}")
        sys.exit(1)
    print("The scores are valid")
 
    # Part II: Weight Validation
    total_weight = sum(a['weight'] for a in data)
    formative_weight = sum(a['weight'] for a in data if a['group'] == 'formative')
    summative_weight = sum(a['weight'] for a in data if a['group'] == 'summative')
 
    weight_errors = []
    if total_weight != 100:
        weight_errors.append(f"Total weight is {total_weight}, Weight must be 100. Please make sure you've correctly recorded everything.")
    if formative_weight != 60:
        weight_errors.append(f"Formative weight is {formative_weight}, Weight must be 60. Please sure you've correctly recorded everything.")
    if summative_weight != 40:
        weight_errors.append(f"Summative weight is {summative_weight}, Weight must be 40.Please make sure you've correctly recorded everything.")
 
    if weight_errors:
        print("\n[VALIDATION ERROR] Weight validation failed:")
        for err in weight_errors:
            print(f"  - {err}")
        sys.exit(1)
    print("Weight validation passed (Total=100, Formative=60, Summative=40).")
 
    # ── Part III Calculate grades and GPA
    formative_weighted = 0             
    summative_weighted = 0             
    formative_total_weight = 0         
    summative_total_weight = 0
    formative_weighted_score_sum = 0   
    summative_weighted_score_sum = 0   

    for a in data:
        # Calculate final weight for table/GPA display
        a['final_weight'] = a['score'] * (a['weight'] / 100)

        group = a['group']

        if group == 'formative':
            formative_weighted += a['final_weight']           
            formative_total_weight += a['weight']            
            formative_weighted_score_sum += a['score'] * a['weight']  
        elif group == 'summative':
            summative_weighted += a['final_weight']
            summative_total_weight += a['weight']
            summative_weighted_score_sum += a['score'] * a['weight']

    # Calculate percentage scores for pass/fail
    
    formative_percentage = formative_weighted_score_sum / formative_total_weight
    summative_percentage = summative_weighted_score_sum / summative_total_weight

    # Calculate overall GPA based on weighted totals
    total_weighted = formative_weighted + summative_weighted
    gpa = (total_weighted / 100) * 5

    # Transcript Display
    print("\n--- Transcript ---")
    print(f"{'Assignment':<40} {'Category':<12} {'Grade %':>6} {'Weight':>7} {'Final weight':>15}")
    print("-" * 85)
    for a in data:
        print(f"{a['assignment']:<40} {a['group']:<12} {format_number(a['score']):>6} "
              f"{format_number(a['weight']):>7} {format_number(a['final_weight']):>10}")
    print("-" * 85)
    print(f"\n{'Formatives(60):':<35} {format_number(formative_weighted):>43}")
    print(f"{'Summatives(40):':<35} {format_number(summative_weighted):>43}")
    print(f"{'GPA:':<35} {format_number(gpa):>43}")

    # Part IV: Pass/Fail
    passed_formative = formative_percentage >= 50
    passed_summative = summative_percentage >= 50
    passed_overall = passed_formative and passed_summative

    # Part V: Resubmission
    formative_assignments = [a for a in data if a['group']== 'formative']
    failed_formative = [a for a in formative_assignments if a['score'] < 50]

    resubmit_candidates = []
    if failed_formative:
        max_weight = max(a['weight'] for a in failed_formative)
        resubmit_candidates = [a for a in failed_formative if a['weight'] == max_weight]

    # Printing STATUS and RESUBMISSIONS
    if passed_overall:
        print()
        print(f"{'STATUS:':<35} {'PASSED':>43}")
    else:
        print(f"{'STATUS:':<35} {'FAILED':>43}")
        cause = []
        if not passed_formative:
            cause.append(f"Formative score {format_number(formative_percentage):}% is below 50%")
        if not passed_summative:
            cause.append(f"Summative score {format_number(summative_percentage):}% is below 50%")
        for r in cause:
            print(f"  → {r}")

    if failed_formative:
     print("\nFormative assignments available for resubmission:")
     for a in resubmit_candidates:
         print(f"  - {a['assignment']}")
    if not passed_summative:
        print("You may resubmit, but your overall status remains FAILED due to summative performance.")
            

if __name__ == "__main__":
    #Loading the data and activating features
    course_data = load_csv_data()
    evaluate_grades(course_data)

