import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    number_of_pages = len(corpus)
    # Create the dictionary representing the probability distribution over which page a random surfer would visit next
    distribution = corpus.copy()
    for prob in distribution:
        distribution[prob] = 0
    
    # If there are no links found at given page, return uniformed distribution.
    if len(corpus[page]) == 0:
        for prob in distribution:
            distribution[prob] = 1/number_of_pages
        return distribution
    
    # With probability 1 - damping_factor, the random surfer should randomly choose one of all pages in the corpus with equal probability.
    for prob in distribution:
        distribution[prob] += (1-damping_factor) * (1/number_of_pages)
            
    for prob in corpus[page]:
        distribution[prob] += 0.85 * (1/len(corpus[page]))
        
    return distribution

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    if n < 1:
        raise AttributeError("n must be >= 1")
     # Create the dictionary representing the probability distribution.
    distribution = corpus.copy()
    for pagerank in distribution:
        distribution[pagerank] = 0
    
    # Helper dictionaries.
    samples = distribution.copy()
    

    # Get a random page of the corpus to start with.
    page = random.choice(list(corpus.keys()))
    
    
    for i in range(n):
        samples[page] += 1
        transition_probabilities = transition_model(corpus, page, damping_factor)
        # Returns list of size k, therefore indexing at 0.
        page = random.choices(population=list(corpus.keys()), weights=transition_probabilities.values(), k=1)[0]
        
    
    for pagerank in distribution:
        distribution[pagerank] = samples[pagerank] / n
 
    return distribution

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    number_of_pages = len(corpus)
     # Create the dictionary representing the probability distribution, starting uniformly.
    distribution = corpus.copy()
    for pagerank in distribution:
        distribution[pagerank] = 1 / number_of_pages
    
    # Helper dictionaries.
    num_links = distribution.copy()
    for page in num_links:
        num_links[page] = len(corpus[page])
    
    links_to_page = distribution.copy()
    for page in links_to_page: 
        links_to_page[page] = []
        for corp in corpus:
            if page in corpus[corp]:
                links_to_page[page].append(corp)
    
    old_distribution = distribution.copy()
    for pagerank in distribution:
            sum = 0
            for page in links_to_page[pagerank]:
                if num_links[page] == 0:
                    sum += distribution[page] / number_of_pages
                else: 
                    sum += distribution[page] / num_links[page]
            distribution[pagerank] = (1-damping_factor)/number_of_pages + damping_factor*sum


    while not check_values(distribution, old_distribution):
        old_distribution = distribution.copy()
        for pagerank in distribution:
            sum = 0
            for page in links_to_page[pagerank]:
                if num_links[page] == 0:
                    sum += distribution[page] / number_of_pages
                else: 
                    sum += distribution[page] / num_links[page]
            distribution[pagerank] = (1-damping_factor)/number_of_pages + damping_factor*sum

    return distribution
        
def check_values(distribution, old_distribution):
    for pagerank in distribution:
        if abs(distribution[pagerank] - old_distribution[pagerank]) > 0.0001:
            return False
    return True 
    
if __name__ == "__main__":
    main()
