def make_matrix(rows, cols, fill=0):
    return [[fill] * cols for _ in range(rows)]


def matrix_multiply(a, b):
    rows_a = len(a)
    cols_a = len(a[0])
    cols_b = len(b[0])
    result = make_matrix(rows_a, cols_b)
    for i in range(rows_a):
        for j in range(cols_b):
            total = 0
            for k in range(cols_a):
                total += a[i][k] * b[k][j]
            result[i][j] = total
    return result


def transpose(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    result = make_matrix(cols, rows)
    for i in range(rows):
        for j in range(cols):
            result[j][i] = matrix[i][j]
    return result


def matrix_add(a, b):
    rows = len(a)
    cols = len(a[0])
    result = make_matrix(rows, cols)
    for i in range(rows):
        for j in range(cols):
            result[i][j] = a[i][j] + b[i][j]
    return result


def print_matrix(m, label=""):
    if label:
        print(f"{label}:")
    for row in m:
        print("  ", row)


def determinant_2x2(m):
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def main():
    a = [[1, 2, 3],
         [4, 5, 6]]

    b = [[7, 8],
         [9, 10],
         [11, 12]]

    print_matrix(a, "Matrix A (2x3)")
    print_matrix(b, "Matrix B (3x2)")

    product = matrix_multiply(a, b)
    print_matrix(product, "A x B")

    t = transpose(a)
    print_matrix(t, "Transpose of A")

    c = [[1, 2], [3, 4]]
    d = [[5, 6], [7, 8]]
    print_matrix(matrix_add(c, d), "C + D")

    print("det([[1,2],[3,4]]):", determinant_2x2([[1, 2], [3, 4]]))


if __name__ == "__main__":
    main()
