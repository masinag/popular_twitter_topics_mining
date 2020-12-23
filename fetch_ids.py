import pandas as pd
import requests
import csv

WRITE_BATCH = 1000
count = 0
def get_id(text):
    global count
    count += 1
    if count % 1000 == 0:
        print("Fetched", count, "ids")
    parts = text.split("… ")
    url = parts[-1]
    if len(parts) > 1 and url.startswith("https://t.co"):
        for _ in range(20):
            try:
                j = requests.get(url).url
                return int(j.split("/")[-1])
            except Exception as e:
                print(e)
        print("Failed", url)
        
    return None

def main(dataset, output):
    with open(dataset, 'r', newline='') as r, open(output, 'w', newline='') as w:
        spamreader = csv.reader(r, delimiter=',', quotechar='"')
        spamwriter = csv.writer(w, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        buffer = [["date", "to_fetch", "text"]]
        for row in spamreader:
            _,_,_,_,_,_,_,_,date,text,_,_,_ = row
            tweet_id = get_id(text)
            if tweet_id != None:
                buffer.append([date, True, tweet_id])
            else:
                buffer.append([date, False, text])
            if len(buffer) >= WRITE_BATCH:
                spamwriter.writerows(buffer)
                buffer.clear()
        spamwriter.writerows(buffer)
        buffer.clear()
        
        # data["id"] = data.text.apply(get_id)
        # data.to_csv(output, columns=("date", "id"), index=False, encoding="utf-8", quoting=csv.QUOTE_NONNUMERIC)

if __name__ == "__main__":
    dataset = "data/covid19_tweets.csv"
    output = "data/date_id.csv"
    main(dataset, output)