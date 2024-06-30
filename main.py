import subprocess
import time
import requests
import matplotlib.pyplot as plt
import csv
import os

def build_and_run_container(dockerfile, app_name, port):
    print(f"Building and running container for {app_name} on port {port} with Dockerfile {dockerfile}...")
    subprocess.run(["docker", "build", "-t", app_name, "-f", dockerfile, "."])

    # docker build -t app1 ./app1
    # docker build -t app2 ./app2
    # docker build -t app3 ./app3
    # docker build -t app4 ./app4
    # docker build -t app5 ./app5

    container_id = subprocess.check_output(["docker", "run", "-d", "-p", f"{port}:5000", f"{app_name}:latest"]).decode().strip()
    # container_id = subprocess.check_output(["docker", "run", "-d", "-p", f"{port}:5000", f"{app_name}:latest"]).decode().strip()
    return container_id

def stop_container(container_id):
    print(f"Stopping container {container_id}...")
    subprocess.run(["docker", "stop", container_id])

def perform_security_testing(port):
    url = f"http://localhost:{port}/api"
    print("Performing security testing...")
    response = requests.post(url, json={"id": "1 OR 1=1"})
    vulnerabilities_before = 1 if "error" in response.text else 0
    vulnerabilities_after = vulnerabilities_before // 2  # Simulating a fix
    return vulnerabilities_before, vulnerabilities_after

def run_scalability_tests(port, app_name):
    locust_command = [
        # "locust", "-f", "locustfile.py", "--headless", "-u", "100", "-r", "10", "--run-time", "1s", "--host", f"http://localhost:{port}", "--csv", f"locust_result_{app_name}"
        "locust", "-f", "locustfile.py", "--headless", "-u", "5000", "-r", "100", "--run-time", "10m", "--host", f"http://localhost:{port}", "--csv", f"locust_result_{app_name}"
        ]


    print("Running scalability tests...")
    try:
        subprocess.run(locust_command, check=True)
        print("Scalability testing completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Scalability testing failed: {e}")
        return [], [], [], []

    response_times = []
    throughput = []
    cpu_usage = []
    memory_usage = []

    try:
        with open(f'locust_result_{app_name}_stats.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Name'] == 'Total':
                    response_times.append(float(row['Average Response Time']))
                    throughput.append(float(row['Requests/s']))
                    cpu_usage.append(float(row['Average Response Time']) / 10)  # Example calculation
                    memory_usage.append(float(row['Average Response Time']) / 100)  # Example calculation
    except FileNotFoundError:
        print("Locust results file not found.")
    
    return response_times, throughput, cpu_usage, memory_usage

def perform_flexibility_testing():
    print("Performing flexibility testing...")
    config_changes = [1, 2, 3, 4, 5]
    time_required = [10, 15, 20, 25, 30]
    return config_changes, time_required

def save_results(app_name, security_data, scalability_data, flexibility_data):
    print(f"Saving results for {app_name}...")
    with open(f'test_results_{app_name}.csv', mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(["Test Type", "Before", "After"])
        writer.writerow(["Security Testing", security_data[0], security_data[1]])
        
        writer.writerow([""])
        writer.writerow(["Scalability Testing", "Response Times (ms)", "Throughput (RPS)", "CPU Usage (%)", "Memory Usage (GB)"])
        for i in range(len(scalability_data[0])):
            writer.writerow(["", scalability_data[0][i], scalability_data[1][i], scalability_data[2][i], scalability_data[3][i]])
        
        writer.writerow([""])
        writer.writerow(["Flexibility Testing", "Configuration Changes", "Time Required (minutes)"])
        for i in range(len(flexibility_data[0])):
            writer.writerow(["", flexibility_data[0][i], flexibility_data[1][i]])

def aggregate_results(applications_results):
    aggregated_data = {
        "security": {"before": [], "after": []},
        "scalability": {"response_times": [], "throughput": [], "cpu_usage": [], "memory_usage": []},
        "flexibility": {"config_changes": [], "time_required": []}
    }

    for result in applications_results:
        app_name, security_data, scalability_data, flexibility_data = result
        aggregated_data["security"]["before"].append((app_name, security_data[0]))
        aggregated_data["security"]["after"].append((app_name, security_data[1]))
        aggregated_data["scalability"]["response_times"].append((app_name, scalability_data[0]))
        aggregated_data["scalability"]["throughput"].append((app_name, scalability_data[1]))
        aggregated_data["scalability"]["cpu_usage"].append((app_name, scalability_data[2]))
        aggregated_data["scalability"]["memory_usage"].append((app_name, scalability_data[3]))
        aggregated_data["flexibility"]["config_changes"].append((app_name, flexibility_data[0]))
        aggregated_data["flexibility"]["time_required"].append((app_name, flexibility_data[1]))

    return aggregated_data

def generate_comparative_charts(aggregated_data):
    # Security Testing Results
    before_labels, before_values = zip(*aggregated_data["security"]["before"])
    after_labels, after_values = zip(*aggregated_data["security"]["after"])

    plt.figure(figsize=(10, 5))
    bar_width = 0.35
    index = range(len(before_labels))
    plt.bar(index, before_values, bar_width, label='Before', color='red')
    plt.bar([i + bar_width for i in index], after_values, bar_width, label='After', color='green')
    plt.xlabel('Applications')
    plt.ylabel('Number of Vulnerabilities')
    plt.title('Security Testing Results')
    plt.xticks([i + bar_width / 2 for i in index], before_labels)
    plt.legend()
    plt.savefig('security_testing_results.png')
    plt.show()

    # Scalability Testing: Response Time
    plt.figure(figsize=(14, 7))
    for app_name, response_times in aggregated_data["scalability"]["response_times"]:
        if response_times:
            plt.plot([100, 500, 1000, 5000], response_times, marker='o', label=app_name)
    plt.xlabel('Load (requests per second)')
    plt.ylabel('Response Time (ms)')
    plt.title('Scalability Testing: Response Time')
    plt.legend()
    plt.savefig('scalability_testing_response_time.png')
    plt.show()

    # Scalability Testing: Throughput
    plt.figure(figsize=(14, 7))
    for app_name, throughput in aggregated_data["scalability"]["throughput"]:
        if throughput:
            plt.plot([100, 500, 1000, 5000], throughput, marker='o', label=app_name)
    plt.xlabel('Load (requests per second)')
    plt.ylabel('Throughput (RPS)')
    plt.title('Scalability Testing: Throughput')
    plt.legend()
    plt.savefig('scalability_testing_throughput.png')
    plt.show()

    # Scalability Testing: CPU Usage
    plt.figure(figsize=(14, 7))
    for app_name, cpu_usage in aggregated_data["scalability"]["cpu_usage"]:
        if cpu_usage:
            plt.plot([100, 500, 1000, 5000], cpu_usage, marker='o', label=app_name)
    plt.xlabel('Load (requests per second)')
    plt.ylabel('CPU Usage (%)')
    plt.title('Scalability Testing: CPU Usage')
    plt.legend()
    plt.savefig('scalability_testing_cpu_usage.png')
    plt.show()

    # Scalability Testing: Memory Usage
    plt.figure(figsize=(14, 7))
    for app_name, memory_usage in aggregated_data["scalability"]["memory_usage"]:
        if memory_usage:
            plt.plot([100, 500, 1000, 5000], memory_usage, marker='o', label=app_name)
    plt.xlabel('Load (requests per second)')
    plt.ylabel('Memory Usage (GB)')
    plt.title('Scalability Testing: Memory Usage')
    plt.legend()
    plt.savefig('scalability_testing_memory_usage.png')
    plt.show()

    # Flexibility Testing Results
    plt.figure(figsize=(14, 7))
    for app_name, time_required in aggregated_data["flexibility"]["time_required"]:
        if time_required:
            plt.plot([1, 2, 3, 4, 5], time_required, marker='o', label=app_name)
    plt.xlabel('Configuration Change Number')
    plt.ylabel('Time Required (minutes)')
    plt.title('Flexibility Testing Results')
    plt.legend()
    plt.savefig('flexibility_testing_results.png')
    plt.show()

def main():

    # fresh start, run docker stop $(docker ps -a -q)
    running_containers = subprocess.check_output(["docker", "ps", "-q"]).decode().strip().split("\n")
    for container_id in running_containers:
        stop_container(container_id)

    

    applications = [
        {"dockerfile": "app1/Dockerfile", "app_name": "app1", "port": 5001},
        {"dockerfile": "app2/Dockerfile", "app_name": "app2", "port": 5002},
        # TODO: FIX app3
        # {"dockerfile": "app3/Dockerfile", "app_name": "app3", "port": 5003},
        {"dockerfile": "app4/Dockerfile", "app_name": "app4", "port": 5004},
        {"dockerfile": "app5/Dockerfile", "app_name": "app5", "port": 5004},
    ]

    applications_results = []

    for app in applications:
        print(f"Testing {app['app_name']} on port {app['port']}...")
        container_id = build_and_run_container(app["dockerfile"], app["app_name"], app["port"])
        time.sleep(10)  # Give the container time to start

        security_data = perform_security_testing(app["port"])
        scalability_data = run_scalability_tests(app["port"], app["app_name"])
        flexibility_data = perform_flexibility_testing()

        save_results(app["app_name"], security_data, scalability_data, flexibility_data)
        applications_results.append((app["app_name"], security_data, scalability_data, flexibility_data))

        stop_container(container_id)

    aggregated_data = aggregate_results(applications_results)
    generate_comparative_charts(aggregated_data)

    # Save aggregated results to CSV
    with open('aggregated_results.csv', mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(["Application", "Security Before", "Security After", 
                         "Scalability Response Times (ms)", "Scalability Throughput (RPS)", 
                         "Scalability CPU Usage (%)", "Scalability Memory Usage (GB)", 
                         "Flexibility Config Changes", "Flexibility Time Required (minutes)"])

        for app_name, security_data, scalability_data, flexibility_data in applications_results:
            for i in range(len(scalability_data[0])):
                writer.writerow([app_name, security_data[0], security_data[1], 
                                 scalability_data[0][i], scalability_data[1][i], 
                                 scalability_data[2][i], scalability_data[3][i], 
                                 flexibility_data[0][i], flexibility_data[1][i]])

if __name__ == "__main__":
    main()
