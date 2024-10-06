class SparseMatrix:
    def __init__(self, matrixFilePath=None, numRows=None, numCols=None):
        self.matrix = {}
        if matrixFilePath:
            self.load_from_file(matrixFilePath)
        else:
            self.numRows = numRows
            self.numCols = numCols

    def load_from_file(self, matrixFilePath):
        with open(matrixFilePath, 'r') as file:
            self.numRows = int(self._parse_line(file.readline()))
            self.numCols = int(self._parse_line(file.readline()))
            for line in file:
                row, col, value = self._parse_tuple(line.strip())
                self.matrix[(row, col)] = value

    def _parse_line(self, line):
        return line.split('=')[1]

    def _parse_tuple(self, line):
        line = line[1:-1]  # Remove parentheses
        return tuple(map(int, line.split(',')))

    def getElement(self, currRow, currCol):
        return self.matrix.get((currRow, currCol), 0)

    def setElement(self, currRow, currCol, value):
        if value != 0:
            self.matrix[(currRow, currCol)] = value
        elif (currRow, currCol) in self.matrix:
            del self.matrix[(currRow, currCol)]

    def add(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrices dimensions do not match for addition")
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)
        for (row, col), value in self.matrix.items():
            result.setElement(row, col, value + other.getElement(row, col))
        for (row, col), value in other.matrix.items():
            if (row, col) not in self.matrix:
                result.setElement(row, col, value)
        return result

    def subtract(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrices dimensions do not match for subtraction")
        result = SparseMatrix(numRows=self.numRows, numCols=self.numCols)
        for (row, col), value in self.matrix.items():
            result.setElement(row, col, value - other.getElement(row, col))
        for (row, col), value in other.matrix.items():
            if (row, col) not in self.matrix:
                result.setElement(row, col, -value)
        return result

    def multiply(self, other):
        if self.numCols != other.numRows:
            raise ValueError("Matrices dimensions do not match for multiplication")
        result = SparseMatrix(numRows=self.numRows, numCols=other.numCols)
        for (row, col), value in self.matrix.items():
            for k in range(other.numCols):
                result.setElement(row, k, result.getElement(row, k) + value * other.getElement(col, k))
        return result

def main():
    print("Select the matrix operation you want to perform:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    choice = input("Enter your choice (1/2/3): ")

    file1 = input("Enter the path for the first matrix file: ")
    file2 = input("Enter the path for the second matrix file: ")

    matrix1 = SparseMatrix(matrixFilePath=file1)
    matrix2 = SparseMatrix(matrixFilePath=file2)

    if choice == '1':
        result = matrix1.add(matrix2)
    elif choice == '2':
        result = matrix1.subtract(matrix2)
    elif choice == '3':
        result = matrix1.multiply(matrix2)
    else:
        print("Invalid choice")
        return

    print("Resultant Matrix:")
    for (row, col), value in result.matrix.items():
        print(f"({row}, {col}, {value})")

if __name__ == "__main__":
    main()
