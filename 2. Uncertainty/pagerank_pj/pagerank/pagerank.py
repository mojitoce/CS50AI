import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 100


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(corpus)

    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    print(sum([v for k,v in ranks.items()]))
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
    links = corpus.get(page)
    pages = corpus.keys()
    n_pages = len(pages)

    tm = {k:1 for k in pages}

    if len(links) == 0:
        prob = 1 / n_pages
        return {k:prob for k in pages}
    else:
        r_prob = (1 - damping_factor) / n_pages
        tm = {k:r_prob for k in pages}
        l_prob = damping_factor / len(links)

        for l in links:
            tm[l] += l_prob

        return tm


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Sample initial page
    n_pages = len(corpus)

    p0 = random.sample(corpus.keys(), 1)[0]

    p = p0
    page_samples = {k:0 for k in corpus.keys()}

    for s in range(SAMPLES):
        tm = transition_model(corpus, p, damping_factor)
        print(p)
        print(tm)
        pages = []
        probs = []
        for page, prob in tm.items():
            pages.append(page)
            probs.append(prob)

        next_page = random.choices(population = pages, weights = probs)[0]

        page_samples[next_page] += 1

        p = next_page

    page_rank = {k:(v/SAMPLES) for k, v in page_samples.items()}

    return page_rank




def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    n_pages = len(corpus)
    page_rank = {k:1/n_pages for k in corpus.keys()}

    changes = {k:1 for k in page_rank.keys()}

    while all(c > 0.0001 for k, c in changes.items()):
        for page in corpus.keys():
            old_prob = page_rank[page]

            # (1 - d) probability
            r_prob = (1 - damping_factor) / n_pages

            # d probability
            s_prob = 0
            for p, l in corpus.items():
                if page in l:
                    s_prob += page_rank[p] / len(l)
                elif len(l) == 0:
                    s_prob += page_rank[p] / n_pages

            s_prob *= damping_factor

            new_prob = r_prob + s_prob

            page_rank[page] = new_prob
            changes[page] = abs(new_prob - old_prob)

    return page_rank



if __name__ == "__main__":
    main()
