from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    path_to_extension = "./uBlock0_1.53.0.chromium/uBlock0.chromium"
    user_data_dir = "/tmp/test-user-data-dir"
    browser = playwright.chromium.launch_persistent_context(user_data_dir , headless=False , args=[f"--disable-extensions-except={path_to_extension}",f"--load-extension={path_to_extension}",])
    page = browser.pages[0]
    page.goto("https://lariku.info/")
    page.get_by_role("link", name="Pagasi Run & Ride").click()
    page.get_by_text("01 Oktober 2023", exact=True).click()
    page.get_by_text("Taman GOR Palu – Besusu Tengah, Palu Timur, Kota Palu, Sulawesi Tengah").click()
    page.get_by_text("Fun Activity").click()
    page.get_by_text("Reg. ends 27 Sep 2023").click()

    # ---------------------
    page.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
