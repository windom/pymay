from may.parser import parse


exp = parse("""
            \\x y z -> y z x
            """)
exp = exp.identifyVars()
print(exp)
print(exp.curry())
