from generate import *
from os import path

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    # print(creator.domains)
    # print(creator.domains[Variable(4, 1, "across", 4)][0])
    # for variable in creator.domains:
    #     print(creator.domains[variable])
    #     copied_variable = creator.domains[variable].copy()
    #     for word in creator.domains[variable]:
    #         if len(word) is not variable.length:
    #             copied_variable.remove(word)
    #             print(f"removed {word}")
    #     creator.domains[variable] = copied_variable
    #     print(creator.domains[variable])
    
    
    # creator.enforce_node_consistency()
    # print(creator.ac3())
    # print(len(creator.crossword.overlaps.keys()))
    # print(creator.select_unassigned_variable(dict()))
    
    dicto = {"yo": 5, "no": 9, "what": 2, "hmm": 3}
    ordered = sorted(dicto, key=lambda num: dicto[num])
    print(ordered)
    
    
if __name__ == "__main__":
    main()