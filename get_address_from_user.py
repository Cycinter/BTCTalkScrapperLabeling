
import re
import base58
import bech32

from selenium.webdriver.common.by import By

BASE58_PATTERN = "[1,3][123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz]{25,34}"
BECH32_PATTERN = "bc1q[a-z0-9]{38}"


def get_address_from_user(driver, user_id: int) -> list:

    # go to the user's profile page
    path = f"https://bitcointalk.org/index.php?action=profile;u={user_id}"
    driver.get(path)

    # html body text
    body_text = driver.find_element(By.TAG_NAME, "body").text

    addresses = set()

    # look for base58 Bitcoin addresses
    for address in re.findall(BASE58_PATTERN, body_text):
        try:
            decoded_address = base58.b58decode_check(address)
            addresses.add(address)
        except:
            continue

    # look for bech32 Bitcoin addresses
    for address in re.findall(BECH32_PATTERN, body_text.lower()):
        decoded = bech32.bech32_decode(address)
        if decoded[1] is not None:
            addresses.add(address)

    return list(addresses)
