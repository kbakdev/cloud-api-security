import pandas as pd
import matplotlib.pyplot as plt
import os

# List of app files
app_files = [
    'locust_result_app1_stats_history.csv',
    'locust_result_app2_stats_history.csv',
    # TODO: FIX THIS
    # 'locust_result_app3_stats_history.csv',
    'locust_result_app4_stats_history.csv',
    'locust_result_app5_stats_history.csv'
]

# Function to create plots for each app
def create_plots(data, app_name):
    # Convert Timestamp to datetime
    data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='s')

    # Plot Requests and Failures per second
    plt.figure(figsize=(14, 7))
    plt.plot(data['Timestamp'], data['Requests/s'], label='Requests/s', color='blue')
    plt.plot(data['Timestamp'], data['Failures/s'], label='Failures/s', color='red')
    plt.xlabel('Time')
    plt.ylabel('Rate')
    plt.title(f'{app_name} - Requests and Failures per Second over Time')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'{app_name}/requests_and_failures_per_second.png')
    plt.show()

    # Plot Response Time Percentiles over Time
    plt.figure(figsize=(14, 7))
    plt.plot(data['Timestamp'], data['50%'], label='50th Percentile', color='green')
    plt.plot(data['Timestamp'], data['90%'], label='90th Percentile', color='orange')
    plt.plot(data['Timestamp'], data['95%'], label='95th Percentile', color='purple')
    plt.plot(data['Timestamp'], data['99%'], label='99th Percentile', color='brown')
    plt.xlabel('Time')
    plt.ylabel('Response Time (ms)')
    plt.title(f'{app_name} - Response Time Percentiles over Time')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'{app_name}/response_time_percentiles_over_time.png')
    plt.show()

    # Plot Cumulative Requests and Failures
    data['Cumulative Requests'] = data['Total Request Count'].cumsum()
    data['Cumulative Failures'] = data['Total Failure Count'].cumsum()

    plt.figure(figsize=(14, 7))
    plt.plot(data['Timestamp'], data['Cumulative Requests'], label='Cumulative Requests', color='blue')
    plt.plot(data['Timestamp'], data['Cumulative Failures'], label='Cumulative Failures', color='red')
    plt.xlabel('Time')
    plt.ylabel('Count')
    plt.title(f'{app_name} - Cumulative Requests and Failures over Time')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'{app_name}/cumulative_requests_and_failures.png')
    plt.show()

# Process each app file
for app_file in app_files:
    # Load the data
    data = pd.read_csv(app_file)
    
    # Extract app name from file name
    app_name = os.path.splitext(os.path.basename(app_file))[0]
    
    # Create directory for the app if it doesn't exist
    app_dir = f'output/{app_name}'
    if not os.path.exists(app_dir):
        os.makedirs(app_dir)
    
    # Save app specific data to a CSV file in the app's directory
    data.to_csv(f'{app_dir}/{app_name}_stats_history.csv', index=False)
    
    # Generate plots for the app
    create_plots(data, app_dir)
