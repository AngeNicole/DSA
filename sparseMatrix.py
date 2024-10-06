class Node:
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value
        self.next = None

class SparseMatrix:
    def __init__(self, numRows, numCols):
        self.numRows = numRows
        self.numCols = numCols
        self.head = None

    def add_element(self, row, col, value):
        new_node = Node(row, col, value)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def get_element(self, row, col):
        current = self.head
        while current:
            if current.row == row and current.col == col:
                return current.value
            current = current.next
        return 0

    def set_element(self, row, col, value):
        current = self.head
        while current:
            if current.row == row and current.col == col:
                current.value = value
                return
            current = current.next
        self.add_element(row, col, value)

    def display(self):
        current = self.head
        while current:
            print(f"({current.row}, {current.col}, {current.value})")
            current = current.next

    def add(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrices dimensions do not match for addition.")
        result = SparseMatrix(self.numRows, self.numCols)
        current = self.head
        while current:
            result.set_element(current.row, current.col, current.value)
            current = current.next
        current = other.head
        while current:
            result.set_element(current.row, current.col, result.get_element(current.row, current.col) + current.value)
            current = current.next
        return result

    def subtract(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrices dimensions do not match for subtraction.")
        result = SparseMatrix(self.numRows, self.numCols)
        current = self.head
        while current:
            result.set_element(current.row, current.col, current.value)
            current = current.next
        current = other.head
        while current:
            result.set_element(current.row, current.col, result.get_element(current.row, current.col) - current.value)
            current = current.next
        return result

    def multiply(self, other):
        if self.numCols != other.numRows:
            raise ValueError("Matrices dimensions do not match for multiplication.")
        result = SparseMatrix(self.numRows, other.numCols)
        current = self.head
        while current:
            other_current = other.head
            while other_current:
                if current.col == other_current.row:
                    result.set_element(current.row, other_current.col, result.get_element(current.row, other_current.col) + current.value * other_current.value)
                other_current = other_current.next
            current = current.next
        return result

    @staticmethod
    def from_file(file_path):
        with open(file_path, 'r') as file:
            numRows = int(file.readline().split('=')[1])
            numCols = int(file.readline().split('=')[1])
            matrix = SparseMatrix(numRows, numCols)
            for line in file:
                row, col, value = map(int, line.strip()[1:-1].split(','))
                matrix.add_element(row, col, value)
        return matrix

def main():
    try:
        operation = input("Select operation (add, subtract, multiply): ").strip().lower()
        file1 = input("Enter the path for the first matrix file: ").strip()
        file2 = input("Enter the path for the second matrix file: ").strip()

        matrix1 = SparseMatrix.from_file(file1)
        matrix2 = SparseMatrix.from_file(file2)

        if operation == "add":
            result = matrix1.add(matrix2)
        elif operation == "subtract":
            result = matrix1.subtract(matrix2)
        elif operation == "multiply":
            result = matrix1.multiply(matrix2)
        else:
            raise ValueError("Invalid operation selected.")

        print("Result:")
        result.display()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
