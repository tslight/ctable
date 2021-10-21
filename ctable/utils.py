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


def dict_from_list_of_dicts(list_of_dicts, dictionary):
    """
    Check a list of dictionaries to see if another dictionary is a subset of
    any of those dictionaries.

    If it is, return the dictionary from the list (ie. the larger dictionary).
    """
    for d in list_of_dicts:
        # https://stackoverflow.com/a/41579450
        if dictionary.items() <= d.items():
            return d


def length_of_strings_or_ints(element):
    return len(str(element))
