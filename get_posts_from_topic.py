
import time
import datetime
import numpy as np
from selenium.webdriver.common.by import By


def process_page(driver) -> dict:
    """This functions processes all the posts of a single page.
    """

    # find each individual post
    ws = driver.find_elements(By.CLASS_NAME, "windowbg") + \
    driver.find_elements(By.CLASS_NAME, "windowbg2")

    script_to_be_executed = """
        var element = document.getElementsByClassName("quote"), index;
        for (index = element.length - 1; index >= 0; index--) {
            element[index].parentNode.removeChild(element[index]);
        }
        var element = document.getElementsByClassName("quoteheader"), index;
        for (index = element.length - 1; index >= 0; index--) {
            element[index].parentNode.removeChild(element[index]);
        }
        """

    driver.execute_script(script_to_be_executed)

    # dictionary where the posts will be collected
    new_posts = dict()

    # iterate over the posts
    for w in ws:

        # find the poster of the post
        poster_info = w.find_elements(By.CLASS_NAME, "poster_info")
        if len(poster_info) != 1:
            continue
        poster_info = poster_info[0]

        # pseudonym of the poster
        name = poster_info.find_elements(By.XPATH, "./b/a")
        if len(name) != 1:
            continue

        # unique id of the poster
        poster_id = name[0].get_attribute("href").split(";u=")[1]
        poster_id = int(poster_id)
        name = name[0].text

        # find the header of the post, where we can find the date of the post
        header_post = w.find_elements(By.CLASS_NAME, "td_headerandpost")
        if len(header_post) != 1:
            continue
        header_post = header_post[0]
        header = header_post.find_elements(By.XPATH, "./table/tbody/tr/td")
        if len(header) != 3:
            continue
        date = header[1].find_elements(By.CLASS_NAME, "smalltext")
        if len(date) == 0 or len(date) > 2:
            continue
        date = date[0].text
        if len(date) == 0:
            continue

        # isolate the date and convert it into a datetime
        date = date.split("\nLast edit:")[0]
        date = date.replace("Today at", datetime.date.today().strftime("%B %d, %Y,"))
        date = datetime.datetime.strptime(date, "%B %d, %Y, %I:%M:%S %p")
        message_num = header[2].find_elements(By.CLASS_NAME, "message_number")
        if len(message_num) != 1:
            continue
        message_num = int(message_num[0].text.replace("#", ""))

        # get the text of the post
        post = header_post.find_elements(By.CLASS_NAME, "post")
        if len(post) != 1:
            continue
        post = post[0].text

        # save the post in the dictionary
        new_posts[message_num] = {"poster": name, "date": date, "post": post, "poster_id": poster_id}

    return new_posts


def process_topic(topic: int, driver) -> dict:
    """This functions processes all the posts of a single topic.
    """

    # dictionary that will contain all posts for this topic
    posts = dict()

    # page index
    i = 0

    # iterate over the pages
    while True:

        start = time.time()

        # url of the i-th page for the topic of interest
        path = f"https://bitcointalk.org/index.php?topic={topic}.{20 * i}"

        # go to the path
        driver.get(path)
        time.sleep(0.05)

        # collect all the posts of the page
        new_posts = process_page(driver)

        # if there is no post, we can stop the iteration
        if len(new_posts) == 0:
            break

        # each post has an index, get the last post of the page
        last_num = list(new_posts.keys())[-1]

        # if the last post has already been processed in the last iteration, we can stop the iteration
        if last_num in posts:
            break
        posts.update(new_posts)

        # sleep
        duration = time.time() - start
        sleep = max(0., 1.2 - duration)
        time.sleep(np.random.choice([2 * sleep, sleep]))

        # process the next page in the new iteration
        i += 1

    return posts
