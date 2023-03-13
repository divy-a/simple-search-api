from fuzzywuzzy import fuzz as __fuzz__, process as __process__
import spacy as __spacy__
nlp_md = __spacy__.load("en_core_web_md")


def get_unique_indices(data):
    unique_indices = []
    seen_indices = []

    for index in data:
        if index not in seen_indices:
            unique_indices.append(index)
        seen_indices.append(index)
    return unique_indices


def print_values(indices, data):
    for index in indices:
        print(data[index])


def print_indices_with_values(indices, data):
    for index in indices:
        print(index, ':', data[index])


def get_best_matches(query: str, data: list[str], max_results=10, case_sensitivity=False, fuzzy_search=True, nlp_search=False) -> list[int]:
    '''
    Note : When `fuzzy_search` is set `True` then `case_sensitivity` must be set to `False`.
    '''

    search_results = []

    # Checks
    if case_sensitivity and (fuzzy_search or nlp_search):
        raise Exception(
            'case_sensitivity can be only set to True when fuzzy_search and nlp_search is set to False')

    if max_results <= 0:
        return []

    if not case_sensitivity:
        query = query.lower()

    # Start-withs and contains
    starts_with_indices = []
    contains_indices = []
    for index, element in enumerate(data):
        if len(starts_with_indices) == max_results:
            break

        if not case_sensitivity:
            element_for_search = str(element).lower()
        else:
            element_for_search = str(element)

        if element_for_search.startswith(query):
            starts_with_indices.append(index)

        elif query in element_for_search:
            contains_indices.append(index)

    search_results = (starts_with_indices+contains_indices)[:max_results]

    if len(search_results) == max_results:
        return search_results

    # Fuzzy Search
    if (fuzzy_search):
        fuzzy_indices = []

        fuzzy_search_results = __process__.extract(
            query, data, scorer=__fuzz__.token_sort_ratio, limit=max_results)

        for element in fuzzy_search_results:
            fuzzy_indices.append(data.index(element[0]))

        search_results = get_unique_indices(
            search_results+fuzzy_indices)[:max_results]

        if len(search_results) == max_results:
            return search_results

    # Nlp Search
    if (nlp_search):
        query_doc = nlp_md(query)
        similarities = []
        for element in data:
            element_doc = nlp_md(element)
            similarity = query_doc.similarity(element_doc)
            similarities.append(similarity)

        nlp_indices = list(range(len(data)))
        nlp_indices.sort(key=lambda i: similarities[i], reverse=True)

        search_results = get_unique_indices(
            search_results+nlp_indices)[:max_results]

        if len(search_results) == max_results:
            return search_results

    return search_results


if __name__ == "__main__":
    print(get_best_matches(
        data=['mom' , 'hi'], query='hi', fuzzy_search=False
    ))
    pass