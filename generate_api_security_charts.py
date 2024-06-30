import matplotlib.pyplot as plt

# Data for Chart 1
years = ['2020', '2021']
api_requests = [500, 855]
collections_created = [23, 30]

# Data for Chart 2
attack_years = ['2020', '2021', '2022']
malicious_calls = [12.22, 26.46, 26.46*4]

# Data for Chart 3
vulnerabilities = ['SQL Injection', 'Cross-Site Scripting', 'Broken Object Level Authorization', 'Credential Stuffing']
prevalence = [40, 25, 20, 15]

# Data for Chart 4
breaches = ['3Commas (2022)', 'Dropbox (2022)', 'Optus (2022)', 'Texas Insurance (2022)', 'Twitter (2021)']
records_exposed = [20000000, 130, 9700000, 1800000, 5400000]

# Chart 1
plt.figure(figsize=(14, 7))
plt.subplot(1, 2, 1)
plt.plot(years, api_requests, marker='o', label='API Requests (millions)')
plt.plot(years, collections_created, marker='o', label='Collections Created (millions)')
plt.xlabel('Year')
plt.ylabel('Count (millions)')
plt.title('Growth of API Requests and Collections')
plt.legend()

# Chart 2
plt.subplot(1, 2, 2)
plt.bar(attack_years, malicious_calls, color='orange')
plt.xlabel('Year')
plt.ylabel('Malicious Calls (millions)')
plt.title('Incidence of API Attacks')

plt.tight_layout()
# save the plot as a file
plt.savefig('api_security_charts.png')

# Chart 3
plt.figure(figsize=(10, 5))
plt.bar(vulnerabilities, prevalence, color='green')
plt.xlabel('Vulnerability Type')
plt.ylabel('Prevalence (%)')
plt.title('Common API Security Vulnerabilities')
# save the plot as a file
plt.savefig('api_security_vulnerabilities.png')

# Chart 4
plt.figure(figsize=(10, 5))
plt.barh(breaches, records_exposed, color='red')
plt.xlabel('Records Exposed')
plt.title('API Breaches and Their Impact')
# save the plot as a file
plt.savefig('api_security_breaches.png')


