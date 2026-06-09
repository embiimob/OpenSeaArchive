from playwright.sync_api import sync_playwright
import os

def run_cuj(page):
    # Get current working directory
    cwd = os.getcwd()

    # Open local file directly
    page.goto(f"file://{cwd}/index.html")
    page.wait_for_timeout(500)

    # Note: we can't fully execute the CUJ because it requires a mock API server or real API key
    # But we can at least take a screenshot of the initial load.

    # Take screenshot at the key moment
    os.makedirs("/home/jules/verification/screenshots", exist_ok=True)
    page.screenshot(path="/home/jules/verification/screenshots/verification.png")
    page.wait_for_timeout(1000)  # Hold final state for the video

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        os.makedirs("/home/jules/verification/videos", exist_ok=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()  # MUST close context to save the video
            browser.close()
