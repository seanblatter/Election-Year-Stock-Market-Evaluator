import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Initialize the ticker for SPY
spy = yf.Ticker("SPY")

# List of U.S. election dates (last 8 elections, on or around early November) and corresponding president and party
election_info = [
    {"date": "1992-11-03", "president": "Bill Clinton", "party": "Democrat"},
    {"date": "1996-11-05", "president": "Bill Clinton", "party": "Democrat"},
    {"date": "2000-11-07", "president": "George W. Bush", "party": "Republican"},
    {"date": "2004-11-02", "president": "George W. Bush", "party": "Republican"},
    {"date": "2008-11-04", "president": "Barack Obama", "party": "Democrat"},
    {"date": "2012-11-06", "president": "Barack Obama", "party": "Democrat"},
    {"date": "2016-11-08", "president": "Donald Trump", "party": "Republican"},
    {"date": "2020-11-03", "president": "Joe Biden", "party": "Democrat"},
]

# Function to calculate percentage change
def calculate_percent_change(start_price, end_price):
    return ((end_price - start_price) / start_price) * 100

# Get historical market data for the week before and after each election
election_results = []

for election in election_info:
    election_date = pd.to_datetime(election["date"])

    # Define the week before and week after the election
    start_before = (election_date - pd.Timedelta(days=7)).strftime('%Y-%m-%d')
    end_before = election_date.strftime('%Y-%m-%d')
    start_after = election_date.strftime('%Y-%m-%d')
    end_after = (election_date + pd.Timedelta(days=7)).strftime('%Y-%m-%d')

    # Get historical data for the week before and after
    data_before = spy.history(start=start_before, end=end_before)
    data_after = spy.history(start=start_after, end=end_after)

    # Ensure there's enough data for the calculations
    if len(data_before) > 0 and len(data_after) > 0:
        # Calculate percent change for the week before
        percent_change_before = calculate_percent_change(data_before['Close'].iloc[0], data_before['Close'].iloc[-1])

        # Calculate percent change for the week after
        percent_change_after = calculate_percent_change(data_after['Close'].iloc[0], data_after['Close'].iloc[-1])

        # Append results
        election_results.append({
            "Election Date": election_date.strftime('%Y-%m-%d'),
            "President": election["president"],
            "Party": election["party"],
            "Week Before Change (%)": percent_change_before,
            "Week After Change (%)": percent_change_after
        })

# Print Results
for result in election_results:
    print(f"Election Date: {result['Election Date']}")
    print(f"  President: {result['President']}")
    print(f"  Party: {result['Party']}")
    print(f"  Week Before Change (%): {result['Week Before Change (%)']:.2f}")
    print(f"  Week After Change (%): {result['Week After Change (%)']:.2f}\n")

# Plot Results
election_dates = [result['Election Date'] for result in election_results]
week_before_changes = [result['Week Before Change (%)'] for result in election_results]
week_after_changes = [result['Week After Change (%)'] for result in election_results]
colors = ['blue' if result['Party'] == 'Democrat' else 'red' for result in election_results]

plt.figure(figsize=(10, 6))

# Plot week before changes
plt.plot(election_dates, week_before_changes, marker='o', linestyle='-', color='purple', label='Week Before Change (%)')
for i, (x, y) in enumerate(zip(election_dates, week_before_changes)):
    plt.scatter(x, y, color=colors[i])

# Plot week after changes
plt.plot(election_dates, week_after_changes, marker='o', linestyle='-', color='orange', label='Week After Change (%)')
for i, (x, y) in enumerate(zip(election_dates, week_after_changes)):
    plt.scatter(x, y, color=colors[i])

plt.xlabel('Election Date')
plt.ylabel('Percentage Change (%)')
plt.title('SPY Percentage Change Before and After U.S. Elections')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()



