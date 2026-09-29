import csv
import os
import random
from datetime import date


# --------------------------------------------------
# Read GDC CSV file
# --------------------------------------------------

def read_csv_file(file_path):
    """Read GDC data from CSV file."""

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []

    with open(file_path, mode="r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        return list(reader)


# --------------------------------------------------
# Greeting
# --------------------------------------------------

def get_greeting():
    """Return a friendly greeting."""

    greetings = [
        "Hello! 👋 How can I help you with GDC data today?",
        "Hi! 😊 Hope you're having a great day. How can I assist you?",
        "Hello! 🌟 Ready to help you with your GDC data.",
        "Hi there! Have a productive day! How can I help you today?",
        "Hello! ☀️ Wishing you a great day ahead. What GDC details would you like to know?"
    ]

    return random.choice(greetings)


# --------------------------------------------------
# Display quote details
# --------------------------------------------------

def display_quotes(quotes, title):
    """Display quote details in a readable format."""

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    if not quotes:
        print("\nNo matching quotes were found.")
        return

    print(f"\nTotal records found: {len(quotes)}\n")

    for index, quote in enumerate(quotes, start=1):

        print(f"Quote {index}")
        print(f"  Quote Number    : {quote.get('Quote_Number', '')}")
        print(f"  Name            : {quote.get('Name', '')}")
        print(f"  Quote Status    : {quote.get('Quote_Status', '')}")
        print(f"  Approval Status : {quote.get('Approval_Status', '')}")
        print("-" * 70)


# --------------------------------------------------
# Approved quotes
# --------------------------------------------------

def get_approved_quotes(data):
    """Return quotes with Approved approval status."""

    approved_quotes = []

    for row in data:

        approval_status = (
            row.get("Approval_Status", "")
            .strip()
            .lower()
        )

        if approval_status == "approved":
            approved_quotes.append(row)

    return approved_quotes


# --------------------------------------------------
# Pending approval quotes
# --------------------------------------------------

def get_pending_quotes(data):
    """Return quotes that are pending approval."""

    pending_quotes = []

    for row in data:

        approval_status = (
            row.get("Approval_Status", "")
            .strip()
            .lower()
        )

        if approval_status in [
            "pending",
            "pending approval",
            "awaiting approval"
        ]:
            pending_quotes.append(row)

    return pending_quotes


# --------------------------------------------------
# Completed deals
# --------------------------------------------------

def get_completed_deals(data):
    """Return completed deals."""

    completed_deals = []

    for row in data:

        quote_status = (
            row.get("Quote_Status", "")
            .strip()
            .lower()
        )

        if quote_status == "completed":
            completed_deals.append(row)

    return completed_deals


# --------------------------------------------------
# Process user question
# --------------------------------------------------

def process_question(user_input, data):

    question = user_input.lower().strip()

    # ----------------------------------------------
    # Approved quotes
    # ----------------------------------------------

    if (
        "approved" in question
        and "quote" in question
    ):
        approved_quotes = get_approved_quotes(data)

        display_quotes(
            approved_quotes,
            "APPROVED QUOTES"
        )

        return

    # ----------------------------------------------
    # Pending approval quotes
    # ----------------------------------------------

    if (
        "pending" in question
        or "pending approval" in question
    ):
        pending_quotes = get_pending_quotes(data)

        display_quotes(
            pending_quotes,
            "PENDING APPROVAL QUOTES"
        )

        return

    # ----------------------------------------------
    # Completed deals
    # ----------------------------------------------

    if (
        "completed" in question
        and "deal" in question
    ):
        completed_deals = get_completed_deals(data)

        display_quotes(
            completed_deals,
            "COMPLETED DEALS"
        )

        return

    # Also understand "completed quotes"
    if "completed" in question:
        completed_deals = get_completed_deals(data)

        display_quotes(
            completed_deals,
            "COMPLETED DEALS"
        )

        return

    # ----------------------------------------------
    # Help
    # ----------------------------------------------

    if "help" in question:

        print("""
I can help you with the following GDC information:

1. Approved quotes
2. Pending approval quotes
3. Completed deals

Example questions:

- Show me approved quotes
- Give me pending approval quotes
- Show completed deals
""")

        return

    # ----------------------------------------------
    # Unknown question
    # ----------------------------------------------

    print("""
I can currently help you with:

- Approved quotes
- Pending approval quotes
- Completed deals

Try asking something like:
"Show me approved quotes"
""")


# --------------------------------------------------
# Main chatbot
# --------------------------------------------------

def main():

    # ----------------------------------------------
    # GDC CSV file path
    # ----------------------------------------------

    data_file = os.path.join(
        "data",
        "data",
        "data.csv"
    )

    # ----------------------------------------------
    # Read GDC data
    # ----------------------------------------------

    data = read_csv_file(data_file)

    if not data:
        print("No GDC data found.")
        return

    # ----------------------------------------------
    # Start bot
    # ----------------------------------------------

    print("=" * 70)
    print("             GDC DAILY SUMMARY BOT")
    print("=" * 70)

    print("\nBot:", get_greeting())

    print("""
You can ask me about:

- Approved quotes
- Pending approval quotes
- Completed deals

Type 'exit' to close the bot.
""")

    # ----------------------------------------------
    # Chat loop
    # ----------------------------------------------

    while True:

        user_input = input("\nUser: ")

        # Exit
        if user_input.lower().strip() in [
            "exit",
            "quit",
            "bye"
        ]:

            print(
                "\nBot: Goodbye! 👋 "
                "Have a great day!"
            )

            break

        # Greeting
        if user_input.lower().strip() in [
            "hi",
            "hello",
            "hey",
            "good morning",
            "good afternoon",
            "good evening"
        ]:

            print("\nBot:", get_greeting())

            continue

        # Process question
        print("\nBot: Let me check the GDC data...")

        process_question(
            user_input,
            data
        )


# --------------------------------------------------
# Run application
# --------------------------------------------------

if __name__ == "__main__":
    main()
