from pagerank import *

def test_transition_model():
    """Test transition model"""
    corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
    page = "1.html"
    damping_factor = 0.85
    assert transition_model(corpus, page, damping_factor) == {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}


corpus2 = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
# corpus = corpus2.copy()
# for page in corpus:
#     corpus[page] = 0
# print(corpus)
# print(len(corpus2["1.html"]))
# # print(len(corpus2))

# import random

# random_key = random.choice(list(corpus2.keys()))

# print("Random key:", random_key)
distribution = corpus2.copy()
number_of_pages = len(corpus2)
for pagerank in distribution:
    distribution[pagerank] = 1 / number_of_pages

links_to_page = distribution.copy()

for page in links_to_page: 
    links_to_page[page] = []
    for corp in corpus2:
        if page in corpus2[corp]:
            links_to_page[page].append(corp)
print(links_to_page)
# print(corpus2["1.html"])
# print("2.html" in corpus2["1.html"])
# for corp in corpus2:
#     print("2.html" in corp)
# for corp in corpus2:
#     print(corpus2[corp])
for page in links_to_page["3.html"]:
    print(page)