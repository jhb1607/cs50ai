import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable in self.domains:
            copied_variable = self.domains[variable].copy()
            for word in self.domains[variable]:
                if len(word) is not variable.length:
                    copied_variable.remove(word)
            self.domains[variable] = copied_variable


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        if self.crossword.overlaps[x, y] is None:
            return False
        
        overlap = self.crossword.overlaps[x, y]
        revised = False
        to_remove = set()
        for word_x in self.domains[x]:
            for word_y in self.domains[y]:
                if word_x[overlap[0]] is not word_y[overlap[1]]:
                    to_remove.add(word_x)
                    revised = True
        for word in to_remove:
            # Check for mistakes!
            self.domains[x].remove(word)
        return revised      
        

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = list(self.crossword.overlaps.keys())
        
        while len(arcs) > 0:
            x, y = arcs.pop()
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x):
                    if z == y:
                        continue
                    arcs.append((z, x))
            return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        keys = list(assignment.keys())
        for var in self.crossword.variables:
             if var not in keys:
                 return False
        return all(assignment[var] is not None and assignment[var] != '' for var in assignment)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Check if values are distinct (no duplicates) and no conflicts between neighboring variables.
        if len(assignment.values()) != len(set(assignment.values())):
            return False
        # Check every value for correct length. 
        for var in assignment:
            if var.length != len(assignment[var]):
                return False
            neighbors = self.crossword.neighbors(var)
            for neighbor in neighbors:
                if neighbor not in assignment.keys():
                    continue
                overlap = self.crossword.overlaps[var, neighbor]
                if assignment[var][overlap[0]] != assignment[neighbor][overlap[1]]:
                    return False
        return True
                

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Counting contraints for each possible value of var. 
        constraints = dict()
        for value in self.domains[var]:
            constraints[value] = 0
        neighbors = self.crossword.neighbors(var)
        for neighbor in neighbors:
            if neighbor not in assignment.keys():
                overlap = self.crossword.overlaps[var, neighbor]
                for value in self.domains[var]:
                    for value_neighbor in self.domains[neighbor]:
                        if value[overlap[0]] != value_neighbor[overlap[1]]:
                            constraints[value] += 1
        return sorted(constraints, key=lambda outruled: constraints[outruled])

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # unassigned = [v for v in assignment.keys() if assignment[v] is None or assignment[v] == ""]
        unassigned = [v for v in self.crossword.variables if v not in assignment.keys()]
        if len(unassigned) == 0:
            return None
        
        remaining_values = dict()
        for var in unassigned:
            remaining_values[var] = len(self.domains[var])
        unassigned = sorted(remaining_values, key=lambda remaining: remaining_values[remaining])
        ties = []
        for var in unassigned:
            if remaining_values[var] == remaining_values[unassigned[0]]:
                ties.append(var)
        ties_neighbors = dict()
        for tie in ties:
            ties_neighbors[tie] = len(self.crossword.neighbors(tie))
        ties = sorted(ties_neighbors, key=lambda neighbors: ties_neighbors[neighbors], reverse=True)
        
        return ties[0]
        

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        
        for value in self.domains[var]:
            assignment_copy = assignment.copy()
            assignment_copy[var] = value
            if self.consistent(assignment_copy):
                if self.assignment_complete(assignment):
                    return assignment
                result = self.backtrack(assignment_copy)
                if result is not None:
                    return result
            assignment_copy.pop(var)
        return None
                
             
            
        


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
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
