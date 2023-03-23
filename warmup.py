## get to know Z3

from z3 import *

bar = "-" * 30

''' Example 1:
    
    Suppose all variables are booleans. 
    Is the following formula satisfiable? 
    That is, is there an assignment to the 
    variables that make the entire formula
    evalute to true?

    p /\ (q \/ ~r)
'''

def example1():
    print(bar)
    
    print("Example 1: is p /\ (q \/ ~r) satisfiable?")

    p = Bool('p')
    q = Bool('q')
    r = Bool('r')
    formula = And(p, Or(q, Not(r)))
    
    s = Solver()
    s.add(formula)
    res = s.check()
    if (res == sat):
        print("Yes: ")
        m = s.model();
        p_val = m.evaluate(p)
        q_val = m.evaluate(q)
        r_val = m.evaluate(r)
        print(f'p = {p_val}, q = {q_val}, r = {r_val}')
        
    else:
        print ("No/Not Sure")


''' Example 2: 

    Suppose all variables are booleans. Is 
    
    ~ (p /\ q)

    always equivalent to

    ~p \/ ~q?

    (This is also known as De Morgan's law). 
    
    To "prove" this, we ask the solver to find 
    an assignment to variables where ~ (p /\ q)
    and ~p \/ ~q do not evaluate to the same value. 
    
    If it is unsatisfiable, we have proven this always holds
'''

def example2():
    print(bar)

    print("Example 2: is ~(p /\ q) equivalent to (~p \/ ~q)?")

    p, q = Bools('p q')

    ## ~(p /\ q)
    formula1 = Not(And(p, q))

    ## ~p \/ ~q 
    formula2 = Or(Not(p), Not(q))
   
    ## is it possible for formula1 to be true 
    ##  but formula2 to be false, or vice versa?
    to_check = And(formula1, Not(formula2))
    
    s = Solver()
    s.add(to_check)
    res = s.check()

    if (res == unsat):
        print("Yes!")

    elif (res == sat):
        print("No, they are not equivalent in the following case: ")
        m = s.model();
        p_val = m.evaluate(p)
        q_val = m.evaluate(q)
        print(f'p = {p_val}, q = {q_val}')
        
    else:
        print ("Not Sure")


''' Example 3:
   
    The program verification example from
    lecture 7 (page 25)
'''

def example3():
    print(bar)
    
    print("Example 3: Does the program assertion (lecture 7, page 25) hold?")

    x = Bool('x')
    y, z, w = Ints('y z w')

    ## formulas modeling the program

    formula_y = y == 8
    formula_z = And(Implies(x, z == y - 1), Implies(Not(x), z == 0)) 
    formula_w = And(Implies(x, w == 0), Implies(Not(x), w == y + 1)) 

    program_model = And(formula_y, formula_z, formula_w)

    ## property
    prop = Or(z == 5, w == 9)

    to_check = And(program_model, Not(prop))
    
    s = Solver()
    s.add(to_check)
    res = s.check()

    if (res == unsat):
        print("Yes!")

    elif (res == sat):
        print("No, the assertion is violated in the following case: ")
        m = s.model();
        x_val = m.evaluate(x)
        y_val = m.evaluate(y)
        z_val = m.evaluate(z)
        w_val = m.evaluate(w)
        print(f'x = {x_val}, y = {y_val}, z = {z_val}, w = {w_val}')
        
    else:
        print ("Not Sure")
   
   
if __name__ == "__main__":
    example1()
    example2() 
    example3()
