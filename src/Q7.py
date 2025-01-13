import sympy

sympy.init_printing()
# sympy.var('C1, S1, C2, S2, C3, S3, C4, S4, C5, S5, C6, S6, d1, d4, d5, d6, l2, l3')
sympy.var("C1:7")
sympy.var("S1:7")
sympy.var("d1, d4, d5, d6")
sympy.var("l2, l3")

A = sympy.Matrix([
	[l3*C3 + l2, -l3*C3],
	[l3*S3, l3*C3 + l2]
])

# Gram-Schmidtを用いてQR分解を実装
def qr_decomposition(A):
	m, n = A.shape
	Q = sympy.Matrix.zeros(m, m)
	R = sympy.Matrix.zeros(m, n)

	# Gram-Schmidt プロセス
	for j in range(n):
		v = A.col(j)
		for i in range(j):
			q = Q.col(i)
			R[i, j] = q.dot(v)
			v -= R[i, j] * q
		R[j, j] = v.norm()
		Q[:, j] = v / R[j, j]

	return sympy.simplify(Q), sympy.simplify(R)

# QR分解を実行
Q, R = qr_decomposition(A)

# 結果を表示
print("Q:")
print(Q)
print("R:")
print(R)

# 検算: Q * R が元の行列 A に等しいか確認
print("Q * R:")
print(sympy.simplify(Q * R))
