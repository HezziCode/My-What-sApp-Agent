import csv

def load_contacts(path='contacts.csv'):
    """
    Reads a CSV with headers 'name' and 'number' and returns a dict.
    """
    contacts = {}
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # strip whitespace just in case
            name = row['name'].strip().lower()
            number = row['number'].strip()
            contacts[name] = number
    return contacts

if __name__ == '__main__':
    # quick test
    contacts = load_contacts()
    for name, num in contacts.items():
        print(f"{name} → {num}")
