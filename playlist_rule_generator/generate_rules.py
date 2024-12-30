import pandas as pd
import pickle
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import association_rules
import sys
import unicodedata
import string
import os


def normalize_track_name(track_name):
    track_name = track_name.lower()
    track_name = unicodedata.normalize('NFC', track_name)
    track_name = track_name.strip()
    track_name = track_name.translate(
        str.maketrans('', '', string.punctuation))
    return track_name


def generate_ass_rules(db_path, min_support=0.05,
                       metric="confidence", min_threshold=0.5):
    df = pd.read_csv(db_path)

    df["track_name"] = df["track_name"].apply(normalize_track_name)
    itemsets = df.groupby('pid')['track_name'].apply(list).reset_index()
    te = TransactionEncoder()
    te_ary = te.fit(itemsets["track_name"].values).transform(
        itemsets["track_name"].values)
    itemsets = pd.DataFrame(te_ary, columns=te.columns_)

    frequent_itemsets = fpgrowth(
            itemsets, min_support=min_support, use_colnames=True)
    rules = association_rules(
            frequent_itemsets, metric=metric, min_threshold=min_threshold)
    print(len(rules))
    return rules


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit("Error: Too few arguments. \
        Please provide the path to the database file.")

    db_path = sys.argv[1]
    rules_path = sys.argv[2]
    rules = generate_ass_rules(db_path)
    
    # Ensure the path for the output model exists (use the PVC mount path)
    os.makedirs(os.path.dirname(rules_path), exist_ok=True)
    pickle.dump(rules, open(rules_path, "wb"))
    print("All right")
