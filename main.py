import os
import praw
from praw.models import MoreComments
import json
import pprint
import requests
from typing import List
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

load_dotenv()

# CREDENTIALS
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Creating an authorized reddit isntance
reddit = praw.Reddit(
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    user_agent = USER_AGENT,
    username = USERNAME,
    password = PASSWORD
)

category_map = {
    "controversial": 0,
    "gilded": 1,
    "hot": 2,
    "new": 3,
    "rising": 4,
    "top": 5
}

def append_to_json_file(new_items, json_file_path):
    """
        Parameters:
        new_item: dictionary of each submission to be wriiten to the json file
        json_file_path: path of the json file
    """
    try:
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as file:
                existing_data = json.load(file)
        else:
            existing_data = []
        
        existing_data.append(new_items)
        with open(json_file_path, 'w') as file:
            json.dump(existing_data, file)
        print("JSON items appended successfully")
    except Exception as e:
        print(f"Error: {e}")

def get_subreddit_submissions(subreddit_name: str, category: int, limit: int|None = 100):
    subreddit = reddit.subreddit(subreddit_name)
    # Creating a ListingGenerator that contains as many submissions as possible from 'all' time from any category.
    if category==0:
        results = subreddit.controversial(time_filter='all', limit=limit)
    elif category==1:
        results = subreddit.gilded(limit=limit)
    elif category==2:
        results = subreddit.hot(limit=limit)
    elif category==3:
        results = subreddit.new(limit=limit)
    elif category==4:
        results = subreddit.rising(limit=limit)
    elif category==5:
        results = subreddit.top(time_filter='all', limit=limit)
    return results

def download_and_save_image(url:str,id:str ,media_files_path:str) -> bool:
    """
    Parameters:
        url(str): the URL of the submission
        id(str): the ID of the submission
        media_files_path(str): the path where we want to save the images e.g., PeopleFuckingDying/hot/ 

    Saves and download the image associated with the URL and saves it to the media_fils_path with the id as its name.
    Returns True if the image is successfully saved, else False.
    """
    try:
        # Some websites block requests that don't have a proper User-Agent header, suspecting them as automated scrapers.
        headers = {
            'User-Agent': USER_AGENT,
            'Accept': 'application/json'
        }
        # Create a session to manage cookies
        session = requests.Session()
        response = session.get(url, timeout=5, headers=headers)
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type')
            if content_type and content_type.startswith("image/"):
                if content_type.split('/')[1] != 'gif':
                    filename = id +".png"

                    # Open the image with Pillow
                    image = Image.open(BytesIO(response.content))
                    image.thumbnail((500,500), Image.LANCZOS)
                    image.save(f"{media_files_path}/{filename}", format='PNG')
                    return True
    except Exception as err:
        print(f"There was an error downloading image: {err}")
    return False        


def extract_submission_infos(results, media_files_path, json_file_path, category, start_index=0) -> List:
    count = 0
    # Iterate through the result and extract required informations
    for i in range(start_index, len(results)):
        submission = results[i]
        if submission.is_video == False and submission.over_18 == False:
            # Extracting URL of the submission
            url = submission.url
            # print(url)
            # Extracting title/caption of the submission
            title = submission.title
            # Extracting ID of the submission. This will help in deduplication.
            id = submission.id

            imageSaved = download_and_save_image(url, id, media_files_path)

            if imageSaved:
                comments = []
                for top_level_comment in submission.comments:
                    if isinstance(top_level_comment, MoreComments):
                        continue
                    comments.append(top_level_comment)

                # Sorting all top-level comments based on its number of upvotes in the descending order
                sorted_comments = sorted(comments, key = lambda com: com.ups, reverse=True)
                # Slice the 10 most-upvoted comments
                sorted_comments = sorted_comments[:10]
                # Convert each of the comment into a dictionary containing body, upvotes and comment ID.
                sorted_comments = [{"commentBody": com.body.lower(), "commentUpvotes": com.ups, "commentId": com.id} for com in sorted_comments]
                sub = {
                    "submissionId": id,
                    "submissionTitle": title.lower(),
                    "submissionURL": url,
                    "comments": sorted_comments
                }
                print("\n\n")
                pprint.pprint(json.dumps(sub, indent=2))
                append_to_json_file(sub, json_file_path)

                count += 1
                print(f"\nCategory: {category}\n\tNumber of submissions collected, k: {count}\n\tNumber of submissions iterated, i: {i+1}\n\tTotal number of submissions returned, T: {len(results)}\n")
    return count

if __name__ == "__main__":
    # WARNING!! Do not forget to change these values.
    SUBREDDIT_NAME = "rareinsults"
    CATEGORY = "controversial"
    START_INDEX = 0
    LIMIT = None
    #-------------------------------------------------------------------------------------------------------------------------------------------
    json_files_dir  = f"json_files/{SUBREDDIT_NAME}"
    json_files_path = f"{json_files_dir}/{CATEGORY}.json"
    media_files_path = f"media_files/{SUBREDDIT_NAME}/{CATEGORY}"
    os.makedirs(json_files_dir, exist_ok=True)
    os.makedirs(media_files_path, exist_ok=True)
    try:
        results = list(get_subreddit_submissions(SUBREDDIT_NAME, category_map[CATEGORY], limit = LIMIT))
        print("Number of submissions returned: ", len(results))
        count = extract_submission_infos(results, media_files_path, json_files_path, start_index=START_INDEX, category=CATEGORY)
    except Exception as e:
        print(f"There is an error connecting reddit: {e}") 
    


