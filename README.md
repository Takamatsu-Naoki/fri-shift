# Questioner–Presenter Pairing Tool

Welcome to the **Questioner–Presenter Pairing Tool**! 🎉  
This tool generates fair and balanced pairings of *questioners* and *presenters* based on your input.

It reads from CSV files containing member and group information, then outputs both human-readable and CSV-format results for easy use in your workflow.

---

## Getting Started

You can set up the development environment using either **Nix** (recommended) or **Poetry**.

### Option 1: Using Nix (Recommended)

#### Method A: With `nix-direnv`
If you have [`nix-direnv`](https://github.com/nix-community/nix-direnv) installed:
```bash
direnv allow
```

#### Method B: Manual
Without `nix-direnv`, manually enter the environment:
```bash
nix develop
```

---

### Option 2: Using Poetry

Make sure you have Python installed. Then:

```bash
pip install poetry
poetry install
```

---

## Usage

1. Prepare your input CSV files inside a `data/` directory:
   - `data/member_table.csv`: Member IDs and names
   - `data/group_assignment.csv`: Group names and member lists

   You can start by copying and editing the provided examples:
   ```bash
   cp data/member_table.example.csv data/member_table.csv
   cp data/group_assignment.example.csv data/group_assignment.csv
   ```

2. Run the program:
```bash
poetry run python ./src/main.py
```

---

## Example Input

### `data/member_table.csv`
```csv
member_id,name
0,John Smith
1,Jane Doe
2,Emily Johnson
3,Michael Brown
4,Sarah Davis
5,David Martinez
6,Laura Wilson
```

### `data/group_assignment.csv`
```csv
group_id,member_list
A,"[2, 3]"
B,"[0, 5]"
C,"[1, 4, 6]"
```

---

## Example Output

### Format 1: Questioner → Presenters
```
questioner: 'John Smith', presenters: ['Jane Doe', 'David Martinez']
questioner: 'Jane Doe', presenters: ['Michael Brown', 'Emily Johnson']
questioner: 'Emily Johnson', presenters: ['David Martinez', 'Sarah Davis']
questioner: 'Michael Brown', presenters: ['Sarah Davis', 'Laura Wilson']
questioner: 'Sarah Davis', presenters: ['Emily Johnson', 'Laura Wilson']
questioner: 'David Martinez', presenters: ['Jane Doe', 'Michael Brown']
questioner: 'Laura Wilson', presenters: ['John Smith', 'John Smith']
```

```csv
John Smith,Jane Doe,David Martinez  
Jane Doe,Michael Brown,Emily Johnson  
Emily Johnson,David Martinez,Sarah Davis  
Michael Brown,Sarah Davis,Laura Wilson  
Sarah Davis,Emily Johnson,Laura Wilson  
David Martinez,Jane Doe,Michael Brown  
Laura Wilson,John Smith,John Smith  
```

---

### Format 2: Presenter ← Questioners
```
presenter: 'Jane Doe', questioners: ['John Smith', 'David Martinez']
presenter: 'David Martinez', questioners: ['John Smith', 'Emily Johnson']
presenter: 'Michael Brown', questioners: ['Jane Doe', 'David Martinez']
presenter: 'Emily Johnson', questioners: ['Jane Doe', 'Sarah Davis']
presenter: 'Sarah Davis', questioners: ['Emily Johnson', 'Michael Brown']
presenter: 'Laura Wilson', questioners: ['Michael Brown', 'Sarah Davis']
presenter: 'John Smith', questioners: ['Laura Wilson', 'Laura Wilson']
```

```csv
Jane Doe,John Smith,David Martinez  
David Martinez,John Smith,Emily Johnson  
Michael Brown,Jane Doe,David Martinez  
Emily Johnson,Jane Doe,Sarah Davis  
Sarah Davis,Emily Johnson,Michael Brown  
Laura Wilson,Michael Brown,Sarah Davis  
John Smith,Laura Wilson,Laura Wilson  
```

---

## License

This project is licensed under the MIT License.

---

Happy pairing! 🎤✨
