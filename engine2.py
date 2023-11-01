from playwright.sync_api import sync_playwright
from logging import getLogger
import logging
import sys
import json
import time
import time
from datetime import datetime

gte = 120
lte = 144

logger = getLogger("engine.py")
logging.basicConfig(
    stream=sys.stdout,  # uncomment this line to redirect output to console
    format="%(message)s",
    level=logging.DEBUG,
)


with sync_playwright() as pw:
    path_to_extension = "./uBlock0_1.53.0.chromium/uBlock0.chromium"
    user_data_dir = "/tmp/test-user-data-dir"
    browser = pw.chromium.launch_persistent_context(user_data_dir , headless=False , args=[f"--disable-extensions-except={path_to_extension}",f"--load-extension={path_to_extension}",])
    page = browser.pages[0]

    page.goto("https://lariku.info/")  # go to url

    errors_index = []
    data = []

    page.wait_for_selector("xpath=/html/body/div/div[2]/div/div/main/article/div/div/div")  # wait for content to load

    content_base_locator = page.locator("xpath=/html/body/div/div[2]/div/div/main/article/div/div/div")
    per_content = content_base_locator.locator(".larikueventKal")

    total_content = per_content.count()

    print(total_content)

    loopNumber = 0
    try :
        for i in range(gte , lte):
            metadata = {}
            
            try :
                link = per_content.nth(i).locator(".larikueventName").get_by_role("link")
                category = per_content.nth(i).locator(".larikueventCat")
                location = per_content.nth(i).locator(".larikueventLoc")
                organizer = per_content.nth(i).locator(".larikueventOrg")

                cat = category.text_content()
                loc = location.text_content(),
                org = organizer.text_content(),
                link.click()

                page.wait_for_selector("xpath=/html/body/div/div[2]/div/div[1]/div/main/article/div[1]")

                content_base_locator_detail = page.locator("xpath=/html/body/div/div[2]/div/div[1]/div/main/article/div[1]")
                per_content_detail = content_base_locator_detail.locator(".larikuevent")
                metadata_key_locator = per_content_detail.locator(".larikueventki")
                metadata_val_locator = per_content_detail.locator(".larikueventka")

                detail_count = per_content_detail.count()
                for j in range(detail_count):
                    key = metadata_key_locator.nth(j).all_text_contents()[0].lower()
                    value = metadata_val_locator.nth(j).all_text_contents()

                    metadata[key] = value

                title = content_base_locator_detail.locator("xpath=/h2").text_content()
                content = content_base_locator_detail.text_content()

                image_locator = content_base_locator_detail.locator(".myModalimg")

                images = []
                for k in range(image_locator.count()):
                    images.append(image_locator.nth(k).get_attribute("src"))

                time.sleep(.3)

                data.append({
                "crawling_at" : int(time.time() * 1000),
                "source" : "https://lariku.info/",
                "title" : title,
                "category" : cat,
                "location"  : loc,
                "organizer" : org,
                "content" : content,
                "images" : images,
                "metadata" : metadata 
                })

                print(f"Selesai Data Ke {i}")
                loopNumber = i
                page.goto("https://lariku.info/")

            except:
                errors_index.append(i)
                print(f"errorAt : {i}")
                continue

        json_object = json.dumps(data, indent=4)
        print(json_object)

        with open(f"data/sample{gte}-{lte}.json", "w") as outfile:
            outfile.write(json_object)

        error = json.dumps(errors_index, indent=4)
        with open(f"data/error/error{gte}-{lte}.json", "w") as outfile:
            outfile.write(error)

    except KeyboardInterrupt:
        print('you have pressed ctrl-c button.')
    except Exception as e:
        print(e)
        print(f"Error At : {loopNumber}")
        json_object = json.dumps(data, indent=4)

        with open(f"data/sample{gte}-{lte}.json", "w") as outfile:
            outfile.write(json_object)