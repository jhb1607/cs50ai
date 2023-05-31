from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

information = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave)
)

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    information,
    Or(And(AKnight, And(AKnight, AKnave)), AKnave)
    
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    information,
    And(Not(And(AKnave, BKnave)), AKnave),
    Or(BKnight, BKnave)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    information,
    Implication(AKnight, Or(And(BKnight, AKnight), And(AKnave, BKnave))),
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    Implication(BKnight, Or(And(BKnight, AKnave), And(BKnave, AKnight))),
    Implication(BKnave, Not(Or(And(BKnight, AKnave), And(BKnave, AKnight))))
)
    
    

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
   information,
   Biconditional(
       Or(AKnight, AKnave), AKnight),
   Or(And(And(Implication(AKnight, BKnave), Implication(AKnave, BKnight)), BKnight), BKnave),
   
   Implication(BKnight, CKnave), 
   Implication(BKnave, CKnight),
   Implication(CKnight, AKnight),
   Implication(CKnave, AKnave)
    
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
