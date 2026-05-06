import asyncio
from login import login_user
import time
from playwright.sync_api import sync_playwright

PROFILE_DIR = "./user_profile"

async def automate(page):
        # args = [
        #     "--disable-blink-features=AutomationControlled",
        # ]

        # 1. Launch the browser
        # context = p.chromium.launch_persistent_context(
        #     user_data_dir=PROFILE_DIR,
        #     headless=False,
        #     args=args,
        #     channel="chrome"
        # )
        
        # 2. Create a new browser context
        # page = context.pages[0] if context.pages else context.new_page()

        await page.goto('https://job-portal-frontend-nine-blue.vercel.app')
        time.sleep(2)

        if not await page.get_by_role('button', name="Log Out").is_visible():
            print("Login Required")
            await login_user(page, "jayjoshi1912007@gmail.com", "Jay@1917")
        else:
            print("Already Logged in")
            
        time.sleep(2)

        await page.get_by_text('Browse Jobs').first.click()

        await click_try_again_if_present(page)
        time.sleep(2)

        await page.get_by_role('button', name='UI/UX').click()

        time.sleep(2)

        await page.get_by_role('button', name='Data Science').click()

        await click_try_again_if_present(page)
        time.sleep(2)

        await page.get_by_role('button', name='Software Developer').click()

        await click_try_again_if_present(page)
        time.sleep(2)

        card = page.locator('h2', has_text='DevOps Engineer')

        await card.scroll_into_view_if_needed()
        time.sleep(2)

        await card.click()

        await click_try_again_if_present(page)
        time.sleep(2)
        
        await page.locator('h1', has_text='DevOps Engineer').scroll_into_view_if_needed()
        
        # company_card = page.locator('h2', has_text='Frontend React Developer')

        # company_card.scroll_into_view_if_needed()

        # time.sleep(2)

        # company_card.click()

        # click_try_again_if_present(page)
        # time.sleep(2)

        # click_try_again_if_present(page)
        
        # page.locator('h1', has_text='Frontend React Developer').scroll_into_view_if_needed()

        # input("Script completed. Press Enter to close the browser...")

        # Close the browser
        # browser.close()

async def click_try_again_if_present(page):
    # Target the "Try again" element
    try_again_locator = page.locator('text=Try again')

    # Check if the element is visible on the page
    if await try_again_locator.is_visible():
        print('"Try again" detected. Clicking it now...')
        await try_again_locator.click()

        # Wait for the page to load or content to update after clicking
        await page.wait_for_load_state('networkidle')

# if __name__ == "__main__":
#     automate()