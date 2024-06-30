import json
import os
from tqdm import tqdm
import shutil

json_file_path = "json_files/forwardsfromgrandma/hot.json"


def read_json_file(json_file_path):
    try:
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as f:
                data = json.load(f)
            return data
        else:
            return []
    except Exception:
        print("Error reading json file")
        return []

def write_json_file(json_file_path, data):
    try:
        with open(json_file_path, 'w') as f:
            json.dump(data, f)
    except Exception:
        print("Error writing json file")

def dedupe_data(list_of_dicts: list[dict], key = "submissionId") -> list[dict]:
    # Create a dictionary to track the first occurrence of each unique key value
    unique_dict = {}
    for i in tqdm(range(len(list_of_dicts))):
        d = list_of_dicts[i]
        unique_dict[d[key]] = d

    # Extract the values back into a list
    deduplicated_list = list(unique_dict.values())
    return deduplicated_list

def merge_and_deduplicate_images(parent_folder, new_folder_name):
    # Create a new folder for merged images
    new_folder_path = os.path.join(parent_folder, new_folder_name)
    os.makedirs(new_folder_path, exist_ok=True)
    
    # Set to store unique filenames
    unique_filenames = set()

    # Iterate through each subfolder
    for subdir in os.listdir(parent_folder):
        subdir_path = os.path.join(parent_folder, subdir)
        if os.path.isdir(subdir_path):
            for filename in os.listdir(subdir_path):
                file_path = os.path.join(subdir_path, filename)
                
                # Check if the filename is unique
                if filename not in unique_filenames:
                    try:
                        shutil.copy(file_path, new_folder_path)
                    except shutil.SameFileError:
                        pass
                    unique_filenames.add(filename)

    print(f"Merged and deduplicated images are saved in {new_folder_path}")

if __name__ == "__main__":
    SUBREDDIT_NAME = "rareinsults"

    categories = ["top", "hot", "new", "controversial", "rising"]
    res = []
    print("Deduplicating and merging JSON......")
    for category in categories:
        json_file_path = f"json_files/{SUBREDDIT_NAME}/{category}.json"
        subs = read_json_file(json_file_path)
        res.extend(subs)
    deduped_subs = dedupe_data(res)
    output_path = f"json_files/{SUBREDDIT_NAME}/{SUBREDDIT_NAME}.json"
    write_json_file(output_path, deduped_subs)

    print("Deduplicating and merging medias.....")
    parent_folder_path = f"media_files/{SUBREDDIT_NAME}"
    new_folder_name = SUBREDDIT_NAME
    merge_and_deduplicate_images(parent_folder_path, new_folder_name)

    print(f"\n\tResult JSON file created.\n\tMerged and deduplicated for subreddit: {SUBREDDIT_NAME}\n\tTotal number of submissions before deduplication: {len(res)}\n\tTotal number of submissions after deduplication: {len(deduped_subs)}")