# TrainingRecordsAnalyzer
Assessment - Analyzes data (.json) based on three requirements

## Prerequisites

- Python 3.x installed
- trainings.txt

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/KhizerShareef/TrainingRecordsAnalyzer.git
    cd TrainingCompletionAnalyzer
    ```

## Usage

1. Prepare your data file in the specified format (e.g., `trainings.txt`).
2. Ensure the data file adheres to the structure mentioned in the documentation.
3. Modify the `data` variable in `main.py` to include your data or specify the data file path accordingly.
4. Run the application:
    ```bash
    python main.py
    ```

## Output

The application generates three JSON output files:
- `completed_training_count.json`: List of completed trainings with a count of people who completed each training.
- `trainings_completed_in_fiscal_year.json`: Details of people who completed specified trainings in a fiscal year.
- `expired_or_expiring_trainings.json`: Information about people with expired or expiring trainings based on a specified date.

## Repository Structure

- `app.py`: Main Python script containing the application logic.


## Contributors

- Khizer Shareef (@KhizerShareef)
