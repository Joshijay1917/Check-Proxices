from automation import automate
import asyncio
import requests
from playwright_stealth import Stealth
from playwright.async_api import async_playwright

# Import your function from the external file
# (Replace 'automation_script' with the actual name of your .py file)

def is_proxy_working(proxy_string):
    """Tests a single proxy before launching the browser context."""
    proxies_dict = {"http": proxy_string, "https": proxy_string}
    
    try:
        print(f"Testing proxy: {proxy_string}...")
        response = requests.get("http://ip-api.com/json", proxies=proxies_dict, timeout=3)
        
        if response.status_code == 200:
            print(f"-> Success! Found working proxy: {proxy_string}")
            return proxy_string
            
    except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, 
            requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        print(f"-> Failed: {proxy_string}")
        
    return None

async def run_with_stealth_proxy():
    proxy_list = [
        "socks5://119.148.7.10:22122",
        "socks5://223.27.82.91:1080",
        "socks4://124.6.225.124:1088",
        "socks4://202.74.243.182:228",
        "socks5://103.30.29.49:1080",
        "socks4://202.72.232.254:1080",
        "socks5://103.118.85.144:1080",
        "socks4://202.40.179.18:4145",
        "socks5://119.148.51.30:22122",
        "socks5://163.47.37.190:1080",
        "socks5://43.251.86.65:1080",
        "socks4://121.200.60.122:4153",
        "http://123.200.3.125:2314",
        "socks4://103.124.251.164:1080",
        "http://123.200.26.38:5555",
        "socks5://27.147.255.146:1080",
        "socks5://103.189.218.76:6969",
        "socks4://121.200.60.122:4153",
        "socks5://123.136.24.161:1080",
        "socks5://103.155.184.51:9898",
        "socks4://103.42.228.19:1080",
        "socks5://115.127.112.34:1080",
        "socks5://103.118.85.144:1080"
    ]
    
    # Remove duplicates
    proxy_list = list(dict.fromkeys(proxy_list))
    
    print(f"Testing {len(proxy_list)} provided proxies concurrently...")
    
    browser = None
    working_count = 0
    tasks = [asyncio.to_thread(is_proxy_working, proxy) for proxy in proxy_list]
    
    async with Stealth().use_async(async_playwright()) as p:
        for coro in asyncio.as_completed(tasks):
            working_proxy = await coro
            
            if working_proxy is not None:
                if browser is None:
                    print(f"\nFound working proxy! Launching browser...")
                    browser = await p.chromium.launch(
                        headless=False,
                        args=[
                            "--disable-blink-features=AutomationControlled",
                            "--no-sandbox",
                            "--disable-setuid-sandbox"
                        ]
                    )
                    
                working_count += 1
                print(f"\n[Context {working_count}] Applying proxy server: {working_proxy}")
                
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
                    proxy={"server": working_proxy}
                )
                
                page = await context.new_page()
                
                try:
                    # print(f"[Context {working_count}] Navigating to appointment system...")
                    # await page.goto("http://ip-api.com/json", wait_until="domcontentloaded", timeout=15000)
                    
                    # ip_data = await page.content()
                    # print(f"IP Verification Info [Context {working_count}]: {ip_data}")
                    # await page.goto('https://job-portal-frontend-nine-blue.vercel.app')
                    # time.sleep(2)
                    
                    # --- CALL YOUR EXTERNAL FUNCTION HERE ---
                    await automate(page)
                    
                except Exception as e:
                    print(f"Failed to connect page in context {working_count}: {e}")
                    await context.close()
                    continue
                    
                if working_count >= 10:
                    break
                    
        if browser is None:
            print("\nCould not find any active working proxies from the list.")
            return
            
        print("\n----------------------------------------------------")
        print("All pages are open. Browser will remain open. Press Ctrl+C in the terminal to close.")
        print("----------------------------------------------------")
        await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(run_with_stealth_proxy())