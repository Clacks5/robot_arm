import sympy

sympy.init_printing()
# sympy.var('C1, S1, C2, S2, C3, S3, C4, S4, C5, S5, C6, S6, d1, d4, d5, d6, l2, l3')
sympy.var("C1:7")
sympy.var("S1:7")
sympy.var("d1, d4, d5, d6")
sympy.var("l2, l3")

T1 = sympy.Matrix([
	[C1, 0, S1, 0],
	[S1, 0, -C1, 0],
	[0, 1, 0, d1],
	[0, 0, 0, 1]
])
T2 = sympy.Matrix([
	[C2, -S2, 0, l2*C2],
	[S2, C2, 0, l2*S2],
	[0, 0, 1, 0],
	[0, 0, 0, 1]
])
T3 = sympy.Matrix([
	[C3, -S3, 0, l3*C3],
	[S3, C3, 0, l3*S3],
	[0, 0, 1, 0],
	[0, 0, 0, 1]
])
T4 = sympy.Matrix([
	[C4, 0, S4, 0],
	[S4, 0, -C4, 0],
	[0, 1, 0, d4],
	[0, 0, 0, 1]
])
T5 = sympy.Matrix([
	[C5, 0, S5, 0],
	[S5, 0, -C5, 0],
	[0, 1, 0, d5],
	[0, 0, 0, 1]
])
T6 = sympy.Matrix([
	[C6, -S6, 0, 0],
	[S6, C6, 0, 0],
	[0, 0, 1, d6],
	[0, 0, 0, 1]
])

p6t = sympy.Matrix([0, 0, 0, 1])
p0t = T1*T2*T3*T4*T5*T6*p6t
# print(sympy.pretty(p0t))
print(sympy.pretty(sympy.simplify(p0t)))