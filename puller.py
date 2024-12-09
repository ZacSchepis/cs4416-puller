import requests
import pandas as pd
import numpy as np
import json

# https://github.com/NAIST-SE/DevGPT/raw/refs/heads/main/snapshot_20230727/20230727_200003_commit_sharings.json
repo = "https://github.com/NAIST-SE/DevGPT/raw/refs/heads/main/"
urls = [
    "snapshot_20230727/20230727_200003_commit_sharings.json",
    "snapshot_20230803/20230803_095317_commit_sharings.json",
    "snapshot_20230810/20230810_124807_commit_sharings.json",
    "snapshot_20230817/20230817_131244_commit_sharings.json",
    "snapshot_20230824/20230824_102435_commit_sharings.json",
    "snapshot_20230831/20230831_063412_commit_sharings.json",
    "snapshot_20230907/20230907_110036_commit_sharings.json",
    "snapshot_20230914/20230914_083202_commit_sharings.json",
    "snapshot_20231012/20231012_230826_commit_sharings.json",
]
# url = "https://github.com/NAIST-SE/DevGPT/raw/refs/heads/main/snapshot_20230727/20230727_200003_commit_sharings.json"
# url = repo + urls[i]
def git_pull_data():
  """
    schepis, hill, bliven/webb
     - This function coallesces git commit data from the above git repo into a format ready for use
     - see data-format.json for the structure generated after running this.
  """
  df = pd.DataFrame(columns=["Commit Message", "AuthorAt", "CommitAt", "Prompt", "Answer", "AccessDate"])
  rows = []
  for url in urls:
    response = requests.get(f"{repo}{url}")
    if response.status_code == 200:
      data = json.loads(response.content)
      for source in data.get("Sources", []):
        commit_messages = {"CommitMessage":source["Message"], "AuthorAt": source['AuthorAt'], 'CommitAt': source['CommitAt'], "Conversation": []}
        convrow = []
        for convo in source.get("ChatgptSharing", []):
          for con in convo.get("Conversations", []):
            row = {
                "Prompt": con["Prompt"],
                "Answer": con["Answer"]
            }
            convrow.append(row)
        if len(convrow) > 0:
          commit_messages["Conversation"] = convrow
        rows.append(commit_messages)
  return rows


if __name__ == "__main__":
  commits = git_pull_data()