tlisp -vt ./core/*.twl
tlisp -vt ./*.twl
clisp ./compile-core.lisp
clisp ./twinlisp.lisp ./tests/test-core
clisp ./twinlisp.lisp ./tests/test-copy
