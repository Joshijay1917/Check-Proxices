import random
import asyncio
import time
from playwright.sync_api import Page

async def human_type(element, text):
    for char in text:
        await element.type(char, delay=random.randint(100, 300))
        await time.sleep(random.uniform(0.1, 0.3))
        
async def login_user(page: Page, email: str, password: str):
    """Handles the login process."""
    print("[*] Running login script from login.py...")

    await page.goto('https://job-portal-frontend-nine-blue.vercel.app/login')
    await time.sleep(2)

    input = await page.locator('input[name="email"]')
    await human_type(input, email)
    await time.sleep(2)

    passw = await page.locator('input[name="password"]')
    await human_type(passw, password)
    await time.sleep(2)

    try:
        await page.locator('button[type="submit"]').click(timeout=20000)
    except TimeoutError:
        print("Try again clicked!")
        await page.locator('button[type="submit"]').click(timeout=10000)
