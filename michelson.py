# Exercise Michelson.1
# Write a Michelson Smart Contract that takes a pair of integers (a,b)
# as parameter, and replaces its storage with the value of this expression:
# a * (2b + 3a)

parameter (pair (int:a) (int:b)) ;
storage int ;

code {              # (a,b), storage
    UNPAIR ;        # (a,b); storage
    UNPAIR ;        # a; b; storage;
    DIG 2 ;         # storage; a; b;
    DROP ;          # a; b
    DIG 1;          # b; a
    PUSH int 2;     # 2; b; a
    MUL ;           # 2b; a
    DIG 1;          # a; 2b
    DUP ;           # a; a; 2b
    PUSH int 3;     # 3; a; a; 2b
    MUL ;           # 3a; a; 2b
    DIG 2;          # 2b; 3a; a
    ADD ;           # 2b + 3a; a
    MUL ;           # (2b + 3a) * a
    NIL operation ; # []; (2b + 3a) * a
    PAIR            # [], (2b + 3a) * a
    }
