from selenium.webdriver.common.by import By


def get_raw_profile_from_user(driver, user_id: int) -> dict:
    """
    Retrieve the raw profile text and URL for a given Bitcointalk user ID.

    Args:
        driver: Selenium WebDriver instance.
        user_id (int): Bitcointalk user ID.

    Returns:
        dict: A dictionary containing user_id, profile URL, and raw profile text.
    """
    # Construct the profile page URL
    url = f"https://bitcointalk.org/index.php?action=profile;u={user_id}"

    # Load the profile page
    driver.get(url)

    # Try to extract the entire body text
    try:
        body_text = driver.find_element(By.TAG_NAME, "body").text
    except:
        body_text = ""

    # Return the raw profile data as a dictionary
    return {
        "user_id": user_id,
        "url": url,
        "raw_text": body_text.strip()
    }