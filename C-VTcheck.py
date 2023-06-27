
import requests

# Replace 'YOUR_API_KEY' with your actual VirusTotal API key
API_KEY = 'YOUR_API_KEY'

# Function to check the hash in VirusTotal
def check_hash(hash):
    url = f'https://www.virustotal.com/api/v3/files/{hash}'
    headers = {
        'x-apikey': API_KEY
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

def split_hash(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()
        hashlist = []
        for index in lines:
            h = index.split("	")
            hashlist.append(h[2])

        return hashlist


# Main function
def main():
    # Prompt the user to enter the file path
    file_path = input("Enter the path to the text file containing hashes: ")

    # Read hashes from the file
    hashes = split_hash(file_path)

    # List of Suspicious Hashes
    suspicious_list = []

    # Check each hash in VirusTotal
    for hash in hashes:
        data = check_hash(hash)

        # Print the scan results
        if "data" in data:
            score = data['data']['attributes']['last_analysis_stats']['malicious']
            if score >= 1:
                suspicious_list.append(hash)

        else:
            continue

    return suspicious_list

if __name__ == '__main__':
    print(main())
