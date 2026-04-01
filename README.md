# Grade Evaluator & File Organizer

This project processes student grade data from a CSV file to determine academic standing and uses a shell script to organize grade files.

The project includes two components:

- **grade_evaluator.py** : A Python script that processes a CSV file of grades, validates the data, calculates GPA, determines pass/fail status, and checks resubmission eligibility.

- **organize.sh** : A shell script that archives the current CSV file and prepares a fresh workspace.

---

## Requirements

- Python 3 installed
- A terminal (Command Prompt, PowerShell, or Bash)
- A CSV file containing grade data (e.g., `grades.csv`)


## CSV Format

The CSV file must follow this structure:

assignment,group,score,weight
Quiz,Formative,85,20
Group Exercise,Formative,40,20
Functions and Debugging Lab,Formative,45,20
Midterm Project - Simple Calculator,Summative,70,20
Final Project - Text-Based Game,Summative,60,20

## Grade Evaluator Features and Operations
The Python script(grade_evaluator.py) has the following features:

1. **File validation and data loading**: The program prompts user to  enter the name of csv filename. It confirms that the file exists and i   s not empty.

2. **Data validation and error handling**: The program ensures that  data is complete and valid. i.e: all required columns, rows, and fields   are present, necessary type casting is done. In  case of a problem, an explanatory error message is displayed and the program terminates.

3. **Score and weight validation**:
   - Scores must be within the range of 0-100
   - The total weight of assignments must be 100
   - Total weight of formative assessments must be 60
   - Total weight of summative assessments must be 40
   When any condition is not met, an explanation is displayed and the   program stops execution.

4. **Grade Calculation**: 
   - Calculates contribution of each assignment to weight
   - Calculates student's grades into formatives(out of 60) and summatives(out of 40)
   - Calculates percentage for each category(Summative and formative)   - Calculates overall grades and converts into a GPA out 5

5. **Status and Resubmission**:
   - The student **only** PASSES if (formative score ≥ 50% and summative score ≥ 50%)
   
   - Program fins the formatives with scores below 50%. The ones with highest weight are presented as eligible for resubmission. If two assignments have the same highest weight, they are both shown and student can select one.

   **NOTE**: If students failed due to summmative performnce but is still eligible for some formative resubmission, the program clarifies th   at resubmission may raise GPA, but the status remains FAILED. This may be relevant for students who may want tob switch schools and need    a slightly greater GPA.

## File Organizer Features and Operations

The file organizer.sh has the following operations

- Bash script to archive your CSV grade file (grade.csv) with a timestamp.
- Ensures an archive directory exists, creating it if necessary.
- Moves the current CSV into archive and renames it with the current date and time.
- Creates a fresh, empty CSV for the next run.
- Logs each archive operation in organizer.log.

## Enabling execution and running
- grade_evaluator.py can be run with the command python3 grade_evaluator.py
- organizer.sh is made executable with chmod +x organizer.sh and run with either ./organizer.sh or bash organizer.sh
