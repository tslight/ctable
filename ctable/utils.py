def get_longest_list_in_dict(dictionary):
    """
    Return the longest list in a dictionary of lists.
    """
    lengths = [len(v) for k, v in dictionary.items()]
    return max(lengths)


def list_of_dicts_to_dict_of_lists(list_of_dicts, key_order):
    """
    Transform a list of dictionaries into a dictionary of lists.
    """
    keys = list(set().union(*(list(d.keys()) for d in list_of_dicts)))
    columns = {}

    for key in keys:
        columns[key] = [d[key] for d in list_of_dicts if key in d]

    return {k: columns[k] for k in key_order}
