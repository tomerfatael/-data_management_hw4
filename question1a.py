def load_data(filename, rank_name):
    with open(filename) as f:
        data = f.readlines()

    ranks = {}
    ordered = []
    for line in data:
        line_data = line.split(",")
        name = line_data[0]
        score = line_data[1]
        ranks[name] = float(score)
        ordered.append(name)

    return dict(ranks=ranks, ordered=ordered, name=rank_name)


def have_k_greater_than_T(seen, k, T):
    cnt = 0
    for num in seen.values():
        if num >= T:
            cnt += 1
    return cnt >= k


def ta_aggregation(files, k, aggregation_func):
    dicts_lst = []
    for file in files:
        dicts_lst.append(load_data(file, file))

    i = 0
    T = -1
    seen = {}
    smallest_seen = {}

    while not (have_k_greater_than_T(seen, k, T)):
        # iterate over all files
        for dict in dicts_lst:
            if i < len(dict["ordered"]):
                dict_name = dict["name"]
                current = dict["ordered"][i]
                all_ranks = [d["ranks"][current] for d in dicts_lst]
                current_val = aggregation_func(all_ranks)
                seen[current] = current_val
                smallest_seen[dict_name] = dict["ranks"][current]

        # update T
        T = aggregation_func(smallest_seen.values())
        i += 1

    # sort seen
    ans = [(name, seen[name]) for name in seen]
    ans.sort(key=lambda tup: tup[1], reverse=True)
    ans = ans[:k]
    return ans

a = ta_aggregation(["rank1.txt", "rank2.txt", "rank3.txt"], 3, lambda x: sum(x)/len(x))
print(a)
