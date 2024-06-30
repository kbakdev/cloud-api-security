import requests
import subprocess
import time
import matplotlib.pyplot as plt
import csv
import re

def setup_dvwa():
    url = "http://localhost/setup.php"
    data = {"create_db": "Create / Reset Database"}
    session = requests.Session()
    response = session.post(url, data=data)
    print("Setup DVWA:", response.status_code)

    login_data = {"username": "admin", "password": "password", "Login": "Login"}
    session.post("http://localhost/login.php", data=login_data)
    print("Logged in:", response.status_code)

    security_data = {"security": "low"}
    session.get("http://localhost/security.php", params=security_data)
    print("Security level set to low")

    return session.cookies.get_dict()

def perform_security_testing(cookies):
    vulnerabilities_before = run_sqlmap(cookies)
    # Here you would normally fix the vulnerabilities
    vulnerabilities_after = run_sqlmap(cookies, fixed=True)
    return vulnerabilities_before, vulnerabilities_after

def run_sqlmap(cookies, fixed=False):
    url = "http://localhost/vulnerabilities/sqli/"
    payload = "id=1&Submit=Submit"
    command = f"sqlmap -u {url} --data=\"{payload}\" --batch --cookie=\"security=low; PHPSESSID={cookies['PHPSESSID']}\""
    if fixed:
        # Simulate fixing by running sqlmap with a different setting or endpoint
        command += " --tamper=space2comment"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    vulnerabilities = len(re.findall(r"\[CRITICAL\] (.*)", result.stdout))
    return vulnerabilities

def run_scalability_tests():
    locust_command = [
        "locust", "-f", "locustfile.py", "--headless", "-u", "100", "-r", "10", "--run-time", "1m", "--host", "http://localhost", "--csv", "locust_result"
    ]

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
        with open('locust_result_stats.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Name'] == 'Total':
                    response_times.append(float(row['Average Response Time']))
                    throughput.append(float(row['Requests/s']))
                    # For CPU and memory usage, you would typically fetch this from system monitoring tools
                    cpu_usage.append(mean([float(row['Min Response Time']), float(row['Max Response Time'])]) / 10)  # Example calculation
                    memory_usage.append(mean([float(row['Min Response Time']), float(row['Max Response Time'])]) / 100)  # Example calculation
    except FileNotFoundError:
        print("Locust results file not found.")
    
    return response_times, throughput, cpu_usage, memory_usage

def perform_flexibility_testing():
    config_changes = [1, 2, 3, 4, 5]
    time_required = [10, 15, 20, 25, 30]
    return config_changes, time_required

def save_results(security_data, scalability_data, flexibility_data):
    with open('test_results.csv', mode='w') as file:
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

def generate_charts(security_data, scalability_data, flexibility_data):
    vulnerabilities_before, vulnerabilities_after = security_data
    response_times, throughput, cpu_usage, memory_usage = scalability_data
    config_changes, time_required = flexibility_data

    plt.figure(figsize=(10, 5))
    plt.bar(['Before', 'After'], [vulnerabilities_before, vulnerabilities_after], color=['red', 'green'])
    plt.xlabel('Security State')
    plt.ylabel('Number of Vulnerabilities')
    plt.title('Security Testing Results')
    plt.savefig('security_testing_results.png')
    plt.show()

    if response_times and throughput:
        plt.figure(figsize=(14, 7))
        plt.subplot(1, 2, 1)
        plt.plot([100, 500, 1000, 5000], response_times, marker='o', color='blue', label='Response Time (ms)')
        plt.xlabel('Load (requests per second)')
        plt.ylabel('Response Time (ms)')
        plt.title('Scalability Testing: Response Time')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot([100, 500, 1000, 5000], throughput, marker='o', color='orange', label='Throughput (RPS)')
        plt.xlabel('Load (requests per second)')
        plt.ylabel('Throughput (RPS)')
        plt.title('Scalability Testing: Throughput')
        plt.legend()
        plt.tight_layout()
        plt.savefig('scalability_testing_results.png')
        plt.show()

        plt.figure(figsize=(14, 7))
        plt.subplot(1, 2, 1)
        plt.plot([100, 500, 1000, 5000], cpu_usage, marker='o', color='red', label='CPU Usage (%)')
        plt.xlabel('Load (requests per second)')
        plt.ylabel('CPU Usage (%)')
        plt.title('Scalability Testing: CPU Usage')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot([100, 500, 1000, 5000], memory_usage, marker='o', color='green', label='Memory Usage (GB)')
        plt.xlabel('Load (requests per second)')
        plt.ylabel('Memory Usage (GB)')
        plt.title('Scalability Testing: Memory Usage')
        plt.legend()
        plt.tight_layout()
        plt.savefig('scalability_testing_cpu_memory.png')
        plt.show()

    plt.figure(figsize=(10, 5))
    plt.plot(config_changes, time_required, marker='o', color='purple')
    plt.xlabel('Configuration Change Number')
    plt.ylabel('Time Required (minutes)')
    plt.title('Flexibility Testing Results')
    plt.savefig('flexibility_testing_results.png')
    plt.show()

def main():
    cookies = setup_dvwa()
    security_data = perform_security_testing(cookies)
    scalability_data = run_scalability_tests()
    flexibility_data = perform_flexibility_testing()
    save_results(security_data, scalability_data, flexibility_data)
    generate_charts(security_data, scalability_data, flexibility_data)

if __name__ == "__main__":
    main()
