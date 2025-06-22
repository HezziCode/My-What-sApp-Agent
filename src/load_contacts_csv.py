import csv
from difflib import SequenceMatcher
import re


def load_contacts(path='contacts.csv'):
    """
    Reads a CSV with headers 'name' and 'number' and returns a dict.
    Also creates aliases and supports fuzzy matching.
    """
    contacts = {}
    aliases = {}  # Maps aliases to main contact names

    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # strip whitespace just in case
            name = row['name'].strip().lower()
            number = row['number'].strip()
            contacts[name] = number

            # Create common aliases
            aliases.update(create_aliases(name))

    return contacts, aliases


def create_aliases(name):
    """
    Creates common aliases for a contact name.
    """
    aliases = {}
    name_lower = name.lower()

    # Common family aliases
    family_aliases = {
        'mama': ['mom', 'mother', 'ammi', 'mummy'],
        'papa': ['dad', 'father', 'abbu', 'daddy'],
        'khala': ['aunty', 'aunt', 'khala_jaan'],
        'nana': ['grandfather', 'nana_jaan'],
        'nani': ['grandmother', 'nani_jaan'],
        'bhai': ['brother', 'bro'],
        'behen': ['sister', 'sis'],
        'chacha': ['uncle', 'chacha_jaan'],
        'phupho': ['aunt', 'phupho_jaan']
    }

    # Add aliases for family members
    for main_name, alias_list in family_aliases.items():
        if main_name in name_lower:
            for alias in alias_list:
                aliases[alias] = name_lower

    # Add variations of the name itself
    # Remove common suffixes like _friend, _czn, _bhai
    clean_name = re.sub(r'_(friend|czn|bhai|behen|cousin)$', '', name_lower)
    if clean_name != name_lower:
        aliases[clean_name] = name_lower

    return aliases


def find_contact(query, contacts, aliases, threshold=0.6):
    """
    Find a contact using fuzzy matching and aliases.
    Returns (contact_name, phone_number) or (None, None) if not found.
    """
    query_lower = query.lower().strip()

    # 1. Exact match
    if query_lower in contacts:
        return query_lower, contacts[query_lower]

    # 2. Alias match
    if query_lower in aliases:
        main_name = aliases[query_lower]
        return main_name, contacts[main_name]

    # 3. Fuzzy match with contact names
    best_match = None
    best_score = 0

    for contact_name in contacts.keys():
        # Calculate similarity
        similarity = SequenceMatcher(None, query_lower, contact_name).ratio()
        if similarity > best_score and similarity >= threshold:
            best_score = similarity
            best_match = contact_name

    if best_match:
        return best_match, contacts[best_match]

    # 4. Fuzzy match with aliases
    for alias, main_name in aliases.items():
        similarity = SequenceMatcher(None, query_lower, alias).ratio()
        if similarity > best_score and similarity >= threshold:
            best_score = similarity
            best_match = main_name

    if best_match:
        return best_match, contacts[best_match]

    return None, None


if __name__ == '__main__':
    # Test the improved contact matching
    contacts, aliases = load_contacts()

    print("=== Loaded Contacts ===")
    for name, num in contacts.items():
        print(f"{name} → {num}")

    print("\n=== Available Aliases ===")
    for alias, main_name in aliases.items():
        print(f"{alias} → {main_name}")

    print("\n=== Testing Contact Matching ===")
    test_queries = [
        "huzaifa",      # exact match
        "HUZAIFA",      # case insensitive
        "huzafa",       # typo
        "mama",         # exact match
        "mom",          # alias
        "MAMA",         # case insensitive
        "mummy",        # alias
        "hunain",       # partial match (hunain_czn)
        "waleed",       # partial match (waleed_bhai)
        "xyz"           # no match
    ]

    for query in test_queries:
        contact_name, number = find_contact(query, contacts, aliases)
        if contact_name:
            print(f"✅ '{query}' → {contact_name} ({number})")
        else:
            print(f"❌ '{query}' → No match found")
