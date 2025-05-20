# 🧠 BTC Address Labeling with Forum Profiles

This project automates the labeling of Bitcoin addresses found in Bitcointalk forum posts using GPT-4 or GPT-3.5. It enriches forum messages with profile metadata to enable better ownership classification and purpose prediction.

---

## 📦 Installation

Create a new Python environment (recommended) and install dependencies:

```bash
pip install -r requirements.txt
```
## 🔧 Configuration
Update conf.yaml with your OpenAI API key

## 🔧 Configuration

### 1. Set topic_id in your notebook or script:
```python
topic_id = 203
```
### 2. Scrape forum posts
```python
from get_posts_from_topic import process_topic
posts = process_topic(topic=topic_id, driver=driver)

with open(f"BitcoinTalkThreads/raw_posts_topic{topic_id}.json", "w") as f:
    json.dump(posts, f)
```
### 3. Get address with Regularization
```python
from get_address_from_user import get_address_from_user

# Store results here
filtered_posts = []

for post in posts_list:
    user_id = int(post["poster_id"])
    addresses = get_address_from_user(driver, user_id)

    if not addresses:
        continue

    for addr in addresses:
        filtered_posts.append({
            "floor": post["floor"],
            "username": post["username"],
            "poster_id": post["poster_id"],
            "address": addr,
            "post_content": post["post_content"]
        })

print(f"✅ Found addresses in {len(filtered_posts)} posts.")

for post in filtered_posts:
    print(f"User ID: {post['poster_id']}")
    print(f"username: {post['username']}")
    print(f"Address: {post['address']}")
    print("-" * 40)
```
### 4. Merge user profile with post
```python
from get_user_profile_raw import get_raw_profile_from_user
# for each poster_id, scrape raw profile HTML
# then write to: data/merged_posts_with_profiles_topic{topic_id}.json

### 5.Run GPT-based labeling
```python
python extract_address_with_chatgpt.py

## 📄 GPT Output Format
```json
{
  "msg_id": "2",
  "username": "laszlo",
  "results": [
    {
      "address": "1ABC...",
      "location_found": "post",
      "ownership": "self",
      "purpose": "donation",
      "linked_entity": "none",
      "confidence": "high"
    }
  ]
}
```