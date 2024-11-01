
import yfinance as yf
import pandas as pd

msft = yf.Ticker("SPY")

# List of weeks you want to collect data for
weeks = [
    ("2020-10-27", "2020-11-04"),

]

# Get historical market data for all specified weeks
hist = pd.DataFrame()  # Start with an empty DataFrame

for start, end in weeks:
    weekly_data = msft.history(start=start, end=end)
    hist = pd.concat([hist, weekly_data])  # Append the weekly data to the hist DataFrame

# Drop duplicate rows (if any), to ensure there's no overlap
hist = hist[~hist.index.duplicated(keep='first')]

# Calculate the percent change for each column
percentage_change = hist.pct_change()

# Calculate the percent change for each week
weekly_changes = []

for i in range(0, len(hist), 5):  # Assuming each week has approximately 5 trading days
    if i + 4 < len(hist):
        weekly_change = (hist.iloc[i + 4]['Close'] / hist.iloc[i]['Close'] - 1) * 100
        weekly_changes.append(weekly_change)

# Print Results
print("Daily Percentage Change:")
print(percentage_change)
print("\nWeekly Percentage Changes:")
print(weekly_changes)
print("\nWeek Data")
print(hist)






