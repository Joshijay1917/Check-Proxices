import csv
import requests
import concurrent.futures
import os
import glob

def test_proxy(proxy_url):
    proxies = {"http": proxy_url, "https": proxy_url}
    try:
        res = requests.get("http://ip-api.com/json", proxies=proxies, timeout=5)
        if res.status_code == 200:
            data = res.json()
            if data.get("status") == "success":
                print(f"[SUCCESS] {proxy_url} -> {data.get('countryCode')}")
                return proxy_url
    except Exception:
        pass
    return None

def main():
    proxies_to_test = set()
    folder_path = r"e:\AdityaWorkspace\Nexovate Technology\Visa Slot Automation\Proxy\Check-Proxices"
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    
    for csv_path in csv_files:
        print(f"Reading from: {os.path.basename(csv_path)}")
        try:
            with open(csv_path, mode='r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Common proxy csv format parsing
                    ip = row.get('ip', '').strip().replace('"', '')
                    port = row.get('port', '').strip().replace('"', '')
                    if not ip or not port:
                        continue
                        
                    protocols = row.get('protocols', '').strip().replace('"', '').split(',')
                    proto = "socks5" if "socks5" in protocols else (protocols[0] if protocols[0] else "http")
                    
                    if "socks4" in protocols: proto = "socks4" # prioritizes socks4 over http
                    if "socks5" in protocols: proto = "socks5" # favors socks5
                    
                    proxy_url = f"{proto}://{ip}:{port}"
                    proxies_to_test.add(proxy_url)
        except:
            pass
            
    test_list = list(proxies_to_test)
    print(f"Extracted {len(test_list)} unique total proxies. Starting high-performance concurrent testing...")
    
    working_proxies = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
        future_to_proxy = {executor.submit(test_proxy, p): p for p in test_list}
        for future in concurrent.futures.as_completed(future_to_proxy):
            result = future.result()
            if result:
                working_proxies.append(result)
                
    print("\n--- ULTIMATE VERIFIED WORKING LIST ---")
    formatted = ',\n'.join([f'        "{p}"' for p in working_proxies])
    print(f"[\n{formatted}\n]")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
