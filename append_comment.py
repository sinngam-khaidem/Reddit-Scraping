# For appending comments
import json
from tqdm import tqdm
import os


def append_comment(json_file_path, output_json_file_path):
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as f:
            data = json.load(f)

        res = []
        for i in tqdm(range(len(data))):
            item = data[i]
            submission_title = item.get('submissionTitle')
            comments = item.get("comments")

            if len(comments)>0 and comments[0].get("commentBody") != "[deleted]" and comments[0].get("commentBody") != "[removed]":
                submission_title += "\n"
                submission_title += comments[0].get("commentBody")
            
            item["submissionTitle"] = submission_title
            res.append(item)

        with open(output_json_file_path, 'w') as f:
            json.dump(res, f)
        print("Comments appended.")

if __name__ == "__main__":
    SUBREDDIT_NAME = "trippinthroughtime"

    json_file_path = f"json_files/{SUBREDDIT_NAME}/{SUBREDDIT_NAME}.json"
    output_json_file_path = f"json_files/{SUBREDDIT_NAME}/{SUBREDDIT_NAME}-with_comment.json"
    append_comment(json_file_path, output_json_file_path)
