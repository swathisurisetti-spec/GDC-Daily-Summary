import csv
import os
from datetime import date


# --------------------------------------------------
# Read CSV file
# --------------------------------------------------

def read_csv_file(file_path):
    """Read data from a CSV file and return it as a list of dictionaries."""

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []

    with open(file_path, mode="r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        return list(reader)


# --------------------------------------------------
# Calculate GDC metrics
# --------------------------------------------------

def calculate_metrics(quotes, tenders, approvals, failures, closed_deals):
    """Calculate daily GDC operational metrics."""

    metrics = {
        "quotes_created": len(quotes),
        "active_tenders": len(tenders),
        "pending_approvals": len(approvals),
        "failed_transactions": len(failures),
        "closed_deals": len(closed_deals),
        "closed_deal_value": 0,
        "pipeline_value": 0
    }

    # Calculate closed deal value
    for deal in closed_deals:
        try:
            value = float(deal.get("deal_value", 0) or 0)
            metrics["closed_deal_value"] += value
        except ValueError:
            pass

    # Calculate pipeline value
    for quote in quotes:
        try:
            value = float(quote.get("deal_value", 0) or 0)
            metrics["pipeline_value"] += value
        except ValueError:
            pass

    return metrics


# --------------------------------------------------
# Generate daily summary
# --------------------------------------------------

def generate_daily_summary(metrics):

    summary = f"""
========================================
        GDC DAILY SUMMARY
========================================

Date: {date.today().strftime("%d-%m-%Y")}

----------------------------------------
DEAL ACTIVITY
----------------------------------------

Quotes Created       : {metrics["quotes_created"]}
Active Tenders       : {metrics["active_tenders"]}
Pending Approvals    : {metrics["pending_approvals"]}
Failed Transactions  : {metrics["failed_transactions"]}
Closed Deals         : {metrics["closed_deals"]}

----------------------------------------
FINANCIAL OVERVIEW
----------------------------------------

Closed Deal Value    : ${metrics["closed_deal_value"]:,.2f}
Pipeline Value       : ${metrics["pipeline_value"]:,.2f}

----------------------------------------
OPERATIONAL INSIGHTS
----------------------------------------
"""

    # Pending approvals
    if metrics["pending_approvals"] > 0:
        summary += (
            f"\n- {metrics['pending_approvals']} deal(s) "
            "are currently pending approval."
        )
    else:
        summary += "\n- No pending approvals."

    # Failed transactions
    if metrics["failed_transactions"] > 0:
        summary += (
            f"\n- {metrics['failed_transactions']} "
            "failed transaction(s) require investigation."
        )
    else:
        summary += "\n- No failed transactions identified."

    # Quotes
    if metrics["quotes_created"] > 0:
        summary += (
            f"\n- {metrics['quotes_created']} new quote(s) "
            "were created."
        )
    else:
        summary += "\n- No new quotes were created."

    # Tenders
    if metrics["active_tenders"] > 0:
        summary += (
            f"\n- {metrics['active_tenders']} "
            "tender(s) are currently active."
        )
    else:
        summary += "\n- No active tenders identified."

    # Closed deals
    if metrics["closed_deals"] > 0:
        summary += (
            f"\n- {metrics['closed_deals']} deal(s) were closed "
            f"with a total value of "
            f"${metrics['closed_deal_value']:,.2f}."
        )
    else:
        summary += "\n- No deals were closed."

    summary += """

========================================
       END OF DAILY SUMMARY
========================================
"""

    return summary


# --------------------------------------------------
# Main program
# --------------------------------------------------

def main():

    # Folder containing GDC CSV files
    data_folder = "data"

    # CSV file locations
    quotes_file = os.path.join(data_folder, "quotes.csv")
    tenders_file = os.path.join(data_folder, "tenders.csv")
    approvals_file = os.path.join(data_folder, "approvals.csv")
    failures_file = os.path.join(data_folder, "failures.csv")
    closed_deals_file = os.path.join(data_folder, "closed_deals.csv")

    # Read CSV files
    quotes = read_csv_file(quotes_file)
    tenders = read_csv_file(tenders_file)
    approvals = read_csv_file(approvals_file)
    failures = read_csv_file(failures_file)
    closed_deals = read_csv_file(closed_deals_file)

    # Calculate metrics
    metrics = calculate_metrics(
        quotes,
        tenders,
        approvals,
        failures,
        closed_deals
    )

    # Generate summary
    summary = generate_daily_summary(metrics)

    # Display summary
    print(summary)


# --------------------------------------------------
# Run application
# --------------------------------------------------

if __name__ == "__main__":
    main()
