import math
from math import sqrt
import numbers

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I

def dot_product(vector_one, vector_two):
    """
    Returns the dot product of two vectors
    """
    dot_prod = 0
    for i in range(len(vector_one)):
        dot_prod += vector_one[i]*vector_two[i]
    return dot_prod
    
class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################
 
    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
        
        if self.h == 1:
            return self[0][0]
        
        return (self[0][0])*(self[1][1]) - (self[0][1])*(self[1][0])

    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")

        trace = 0
        for i in range(self.h):
            trace = trace + self[i][i]
        
        return trace

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")
        
        inverse = []
        det = self.determinant()
        
        if self.h == 1:
            inverse = [[1/det]]
            return Matrix(inverse)

        inverse = [[0, 0],[0,0]]
        inverse[0][0] = (self[1][1])/det
        inverse[0][1] = (-1 * (self[0][1]))/det
        inverse[1][0] = (-1 * (self[1][0]))/det
        inverse[1][1] = (self[0][0])/det
            
        return Matrix(inverse)

    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        transposed = []
        for i in range(self.w):
            row = []
            for j in range(self.h):
                row.append(self[j][i])
            transposed.append(row)
        return Matrix(transposed)

    def is_square(self):
        return self.h == self.w

    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same") 
        result_matrix = []
        for i in range(self.h):
            row = []
            for j in range(self.w):
                row.append(self[i][j] + other[i][j])
            result_matrix.append(row)
        
        return Matrix(result_matrix)
    
    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        negative_matrix = []
        for i in range(self.h):
            row = []
            for j in range(self.w):
                row.append(self[i][j] * (-1))
            negative_matrix.append(row)
        
        return Matrix(negative_matrix)

    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        return self + (-other)

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        multiplied_matrix = []

        other_transposed = other.T()
    
        for i in range(self.h):
            row_result = []
            for j in range(other_transposed.h):
                row_result.append(dot_product(self.g[i],other_transposed.g[j]))
            multiplied_matrix.append(row_result)
                
        return Matrix(multiplied_matrix)

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        if isinstance(other, numbers.Number):
            scaler_multiplied_matrix = []
            for i in range(self.h):
                row = []
                for j in range(self.w):
                    row.append(other * self[i][j])
                scaler_multiplied_matrix.append(row)
            return Matrix(scaler_multiplied_matrix)
            