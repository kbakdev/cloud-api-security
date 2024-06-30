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

def plot_get_post_percentiles(stats_file):
    # Load data from CSV file
    stats_data = pd.read_csv(stats_file)

    # Extract data for GET, POST, and Aggregated from stats data
    get_data = stats_data[(stats_data['Name'] == '/api') & (stats_data['Type'] == 'GET')]
    post_data = stats_data[(stats_data['Name'] == '/api') & (stats_data['Type'] == 'POST')]
    aggregated_data = stats_data[stats_data['Type'].isnull()]

    # Plotting response time percentiles for GET, POST, and Aggregated
    percentiles = ['50%', '66%', '75%', '80%', '90%', '95%', '98%', '99%', '99.9%', '99.99%', '100%']
    get_percentiles = get_data[percentiles].values[0]
    post_percentiles = post_data[percentiles].values[0]
    aggregated_percentiles = aggregated_data[percentiles].values[0]

    plt.figure(figsize=(14, 7))
    plt.plot(percentiles, get_percentiles, label='GET /api', marker='o')
    plt.plot(percentiles, post_percentiles, label='POST /api', marker='o')
    plt.plot(percentiles, aggregated_percentiles, label='Aggregated', marker='o', linestyle='--')

    plt.xlabel('Percentiles')
    plt.ylabel('Response Time (ms)')
    plt.title('Response Time Percentiles for GET and POST Requests')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('response_time_percentiles_get_post.png')
    plt.show()

def plot_total_response_times(history_file):
    # Load data from CSV file
    history_data = pd.read_csv(history_file)

    # Extract relevant columns for plotting
    timestamps = history_data['Timestamp']
    total_median_response_time = history_data['Total Median Response Time']
    total_avg_response_time = history_data['Total Average Response Time']
    total_min_response_time = history_data['Total Min Response Time']
    total_max_response_time = history_data['Total Max Response Time']

    # Plotting total response time over time for Aggregated data
    plt.figure(figsize=(14, 7))
    plt.plot(timestamps, total_median_response_time, label='Median Response Time', marker='o')
    plt.plot(timestamps, total_avg_response_time, label='Average Response Time', marker='o')
    plt.plot(timestamps, total_min_response_time, label='Min Response Time', marker='o')
    plt.plot(timestamps, total_max_response_time, label='Max Response Time', marker='o')

    plt.xlabel('Timestamp')
    plt.ylabel('Response Time (ms)')
    plt.title('Total Response Times Over Time (Aggregated)')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('total_response_times_over_time_aggregated.png')
    plt.show()

def generate_comparative_charts(aggregated_results_file):
    aggregated_data = pd.read_csv(aggregated_results_file)

    # Security Testing Results
    plt.figure(figsize=(10, 5))
    bar_width = 0.35
    index = range(len(aggregated_data))

    plt.bar(index, aggregated_data['Security Before'], bar_width, label='Before', color='red')
    plt.bar([i + bar_width for i in index], aggregated_data['Security After'], bar_width, label='After', color='green')

    plt.xlabel('Applications')
    plt.ylabel('Number of Vulnerabilities')
    plt.title('Security Testing Results')
    plt.xticks([i + bar_width / 2 for i in index], aggregated_data['Application'])
    plt.legend()
    plt.tight_layout()
    plt.savefig('security_testing_results.png')
    plt.show()

    # Scalability Testing: Response Time
    plt.figure(figsize=(14, 7))
    for app_name in aggregated_data['Application'].unique():
        app_data = aggregated_data[aggregated_data['Application'] == app_name]
        plt.plot(['100', '500', '1000', '5000'], app_data['Scalability Response Times (ms)'].tolist(), marker='o', label=app_name)

    plt.xlabel('Load (requests per second)')
    plt.ylabel('Response Time (ms)')
    plt.title('Scalability Testing: Response Time')
    plt.legend()
    plt.tight_layout()
    plt.savefig('scalability_testing_response_time.png')
    plt.show()

    # Scalability Testing: Throughput
    plt.figure(figsize=(14, 7))
    for app_name in aggregated_data['Application'].unique():
        app_data = aggregated_data[aggregated_data['Application'] == app_name]
        plt.plot(['100', '500', '1000', '5000'], app_data['Scalability Throughput (RPS)'].tolist(), marker='o', label=app_name)

    plt.xlabel('Load (requests per second)')
    plt.ylabel('Throughput (RPS)')
    plt.title('Scalability Testing: Throughput')
    plt.legend()
    plt.tight_layout()
    plt.savefig('scalability_testing_throughput.png')
    plt.show()

    # Scalability Testing: CPU Usage
    plt.figure(figsize=(14, 7))
    for app_name in aggregated_data['Application'].unique():
        app_data = aggregated_data[aggregated_data['Application'] == app_name]
        plt.plot(['100', '500', '1000', '5000'], app_data['Scalability CPU Usage (%)'].tolist(), marker='o', label=app_name)

    plt.xlabel('Load (requests per second)')
    plt.ylabel('CPU Usage (%)')
    plt.title('Scalability Testing: CPU Usage')
    plt.legend()
    plt.tight_layout()
    plt.savefig('scalability_testing_cpu_usage.png')
    plt.show()

    # Scalability Testing: Memory Usage
    plt.figure(figsize=(14, 7))
    for app_name in aggregated_data['Application'].unique():
        app_data = aggregated_data[aggregated_data['Application'] == app_name]
        plt.plot(['100', '500', '1000', '5000'], app_data['Scalability Memory Usage (GB)'].tolist(), marker='o', label=app_name)

    plt.xlabel('Load (requests per second)')
    plt.ylabel('Memory Usage (GB)')
    plt.title('Scalability Testing: Memory Usage')
    plt.legend()
    plt.tight_layout()
    plt.savefig('scalability_testing_memory_usage.png')
    plt.show()

    # Flexibility Testing Results
    plt.figure(figsize=(14, 7))
    for app_name in aggregated_data['Application'].unique():
        app_data = aggregated_data[aggregated_data['Application'] == app_name]
        plt.plot(['1', '2', '3', '4', '5'], app_data['Flexibility Time Required (minutes)'].tolist(), marker='o', label=app_name)

    plt.xlabel('Configuration Change Number')
    plt.ylabel('Time Required (minutes)')
    plt.title('Flexibility Testing Results')
    plt.legend()
    plt.tight_layout()
    plt.savefig('flexibility_testing_results.png')
    plt.show()

def main():
    # Plot response time percentiles over time
    plot_response_time_percentiles('locust_result_stats_history.csv')

    # Plot response time percentiles for GET and POST requests
    plot_get_post_percentiles('locust_result_stats.csv')

    # Plot total response times over time for Aggregated data
    plot_total_response_times('locust_result_stats_history.csv')

    # Generate comparative charts from aggregated results
    generate_comparative_charts('aggregated_results.csv')

if __name__ == "__main__":
    main()
