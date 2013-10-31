from parser import parse


exp = parse("""
            let x = (\\x -> x) x, x = y in (\\x -> x)  y x
            """)
exp = exp.identifyVars()
print(exp)
