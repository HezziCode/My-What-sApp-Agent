#!/usr/bin/env python3
"""
Test script for the improved contact matching system.
This demonstrates all the features of the enhanced WhatsApp agent.
"""

from load_contacts_csv import load_contacts, find_contact

def test_contact_matching():
    """Test various contact matching scenarios."""
    
    print("🤖 WhatsApp Agent - Enhanced Contact Matching Test")
    print("=" * 60)
    
    # Load contacts and aliases
    contacts, aliases = load_contacts()
    
    print(f"\n📱 Loaded {len(contacts)} contacts with {len(aliases)} aliases")
    
    # Test cases covering different scenarios
    test_cases = [
        # Exact matches
        ("huzaifa", "✅ Exact match"),
        ("mama", "✅ Exact match"),
        ("papa", "✅ Exact match"),
        
        # Case insensitive
        ("HUZAIFA", "✅ Case insensitive"),
        ("MAMA", "✅ Case insensitive"),
        ("Papa", "✅ Mixed case"),
        
        # Aliases
        ("mom", "✅ Alias for mama"),
        ("mother", "✅ Alias for mama"),
        ("ammi", "✅ Urdu alias for mama"),
        ("mummy", "✅ Alias for mama"),
        ("dad", "✅ Alias for papa"),
        ("father", "✅ Alias for papa"),
        ("abbu", "✅ Urdu alias for papa"),
        ("daddy", "✅ Alias for papa"),
        ("aunty", "✅ Alias for khala"),
        ("bro", "✅ Alias for waleed_bhai"),
        
        # Partial matches (clean names)
        ("hunain", "✅ Partial match (hunain_czn)"),
        ("waleed", "✅ Partial match (waleed_bhai)"),
        ("mawiya", "✅ Partial match (mawiya_friend)"),
        ("asim", "✅ Partial match (asim_friend)"),
        ("taha", "✅ Partial match (taha_friend)"),
        ("shahbuddin", "✅ Partial match (shahbuddin_friend)"),
        
        # Fuzzy matches (typos)
        ("huzafa", "✅ Fuzzy match (typo in huzaifa)"),
        ("mamaa", "✅ Fuzzy match (extra 'a' in mama)"),
        ("papaa", "✅ Fuzzy match (extra 'a' in papa)"),
        ("hunian", "✅ Fuzzy match (typo in hunain)"),
        
        # No matches
        ("xyz", "❌ No match"),
        ("unknown", "❌ No match"),
        ("", "❌ Empty string"),
    ]
    
    print("\n🔍 Testing Contact Matching:")
    print("-" * 60)
    
    success_count = 0
    total_tests = len(test_cases)
    
    for query, expected_description in test_cases:
        contact_name, number = find_contact(query, contacts, aliases)
        
        if contact_name:
            result = f"✅ '{query}' → {contact_name} ({number})"
            if "❌" not in expected_description:
                success_count += 1
        else:
            result = f"❌ '{query}' → No match found"
            if "❌" in expected_description:
                success_count += 1
        
        print(f"{result:<50} | {expected_description}")
    
    print("-" * 60)
    print(f"📊 Test Results: {success_count}/{total_tests} tests passed")
    
    if success_count == total_tests:
        print("🎉 All tests passed! Contact matching system is working perfectly.")
    else:
        print(f"⚠️  {total_tests - success_count} tests failed. Please check the implementation.")
    
    return success_count == total_tests

def demo_usage_examples():
    """Show practical usage examples."""
    
    print("\n\n💡 Usage Examples:")
    print("=" * 60)
    
    examples = [
        "Send message to huzaifa: Hello!",
        "Message mama that I'll be late",
        "Send 'How are you?' to mom",
        "Text dad: I'm coming home",
        "Message HUZAIFA: Testing case insensitive",
        "Send to hunain: What's up bro?",
        "Message waleed: See you tomorrow",
    ]
    
    for example in examples:
        print(f"📝 {example}")
    
    print("\n✨ Features:")
    print("• Case-insensitive matching (HUZAIFA = huzaifa)")
    print("• Family aliases (mama = mom = mother = ammi = mummy)")
    print("• Fuzzy matching for typos (huzafa → huzaifa)")
    print("• Clean name matching (hunain → hunain_czn)")
    print("• Multiple language support (ammi, abbu, khala)")

if __name__ == "__main__":
    # Run the tests
    test_passed = test_contact_matching()
    
    # Show usage examples
    demo_usage_examples()
    
    print(f"\n{'🎯 Ready to use!' if test_passed else '⚠️  Fix issues before using'}")
