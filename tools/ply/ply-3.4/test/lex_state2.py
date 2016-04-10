# lex_state2.py
#
# Bad state declaration

import sys
if ".." not in sys.path: sys.path.insert(0,"..")

import ply.lex as lex

tokens = [ 
    "PLUS",
    "MINUS",
    "NUMBER",
    ]

states = ('comment','example')

t_PLUS = r'\+'
t_MINUS = r'-'
t_NUMBER = r'\d+'

# Comments
def t_comment(t):
    r'/\*'
    t.lexer.begin('comment')
    print("Entering comment state")

def t_comment_body_part(t):
    r'(.|\n)*\*/'
    print("comment body {0!s}".format(t))
    t.lexer.begin('INITIAL')

def t_error(t):
    pass



lex.lex()


