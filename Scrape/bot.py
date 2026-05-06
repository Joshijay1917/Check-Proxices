import asyncio
from playwright.async_api import async_playwright

# Replace this with your actual API token from the Scrape.do dashboard
API_TOKEN = "583bfa1603754ec9b05d47ecc5ba15dd00d6052be80"

async def run_with_scrape_do():
    print("Applying Scrape.do Proxy Mode (Structured)...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox"
            ]
        )
        
        # Pass the server, username, and password in separate fields
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            proxy={
                "server": "http://proxy.scrape.do:8080",
                "username": API_TOKEN,
                "password": "geoCode=bd&super=true"
            }
        )
        
        page = await context.new_page()
        
        try:
            print("Connecting through proxy and navigating to IP checker...")
            await page.goto("http://ip-api.com/json", wait_until="domcontentloaded", timeout=15000)
            
            ip_data = await page.content()
            print(f"IP Verification Info: {ip_data}")
            
        except Exception as e:
            print(f"Failed to connect using the proxy: {e}")
            
        finally:
            await context.close()
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run_with_scrape_do())