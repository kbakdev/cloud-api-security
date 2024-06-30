import pandas as pd
import matplotlib.pyplot as plt

def plot_response_time_percentiles(history_file):
    # Load data from CSV file
    history_data = pd.read_csv(history_file)

    # Extract relevant columns for plotting
    timestamps = history_data['Timestamp']
    response_time_50th = history_data['50%']
    response_time_90th = history_data['90%']
    response_time_99th = history_data['99%']

    # Convert timestamps to readable format
    timestamps = pd.to_datetime(timestamps, unit='s')

    # Plotting response time percentiles over time
    plt.figure(figsize=(14, 7))
    plt.plot(timestamps, response_time_50th, label='50th Percentile', marker='o')
    plt.plot(timestamps, response_time_90th, label='90th Percentile', marker='o')
    plt.plot(timestamps, response_time_99th, label='99th Percentile', marker='o')

    plt.xlabel('Timestamp')
    plt.ylabel('Response Time (ms)')
    plt.title('Response Time Percentiles Over Time')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('response_time_percentiles_over_time.png')
    plt.show()

def main():
    # Plot response time percentiles over time
    plot_response_time_percentiles('locust_result_stats_history.csv')

if __name__ == "__main__":
    main()
