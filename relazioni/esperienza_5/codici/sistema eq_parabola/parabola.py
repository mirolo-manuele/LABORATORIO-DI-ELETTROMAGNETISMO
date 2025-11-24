import numpy as np

def find_parabola_equation(p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    # The system of linear equations is:
    # a*x1^2 + b*x1 + c = y1
    # a*x2^2 + b*x2 + c = y2
    # a*x3^2 + b*x3 + c = y3
    
    # We represent this as the matrix equation A * [a, b, c]T = Y
    
    # A is the coefficient matrix:
    A = np.array([
        [x1**2, x1, 1],
        [x2**2, x2, 1],
        [x3**2, x3, 1]
    ])
    
    # Y is the results vector:
    Y = np.array([y1, y2, y3])
    

    # Use numpy.linalg.solve to find the vector [a, b, c]
    # This is equivalent to finding the inverse of A and multiplying by Y: [a, b, c]T = A^-1 * Y
    coefficients = np.linalg.solve(A, Y)
    
    # Unpack the coefficients
    a, b, c = coefficients
    
    return a, b, c


point1 = (29919.93003, 756)
point2 = (34906.58504, 772)
point3 = (41066.57064, 752)
print(point1, point2, point3)
# Find the coefficients
result = find_parabola_equation(point1, point2, point3)

if result is not None:
    a, b, c = result
    
    # Format the equation for display
    def format_coefficient(coeff, variable):
        if coeff == 0:
            return ""
        abs_coeff = abs(coeff)
        sign = "+" if coeff > 0 else "-"
        
        if variable:
            # For b and a, handle coefficients of 1 or -1
            if abs_coeff == 1 and variable != 'c':
                coeff_str = ""
            else:
                # Use f-string for formatting to a reasonable number of decimal places
                coeff_str = f"{abs_coeff:.8f}"
            
            # For 'a' term, only show sign if positive for subsequent terms
            if variable == 'x^2' and coeff > 0:
                sign = ""
            elif variable == 'x^2' and coeff < 0:
                sign = "-"
            
            return f" {sign} {coeff_str}{variable}"
        else: # For c term
            sign = "+" if coeff >= 0 else "-"
            return f" {sign} {abs_coeff:.4f}"


    # Build the final equation string
    # Start with the 'a' term
    if a != 0:
        equation_str = format_coefficient(a, 'x^2').strip()
    else:
        equation_str = "" # If a=0, it's a line, not a parabola
        
    # Add the 'b' term
    equation_str += format_coefficient(b, 'x')
    
    # Add the 'c' term
    if c != 0:
        equation_str += format_coefficient(c, '')
    
    # Clean up leading signs
    equation_str = equation_str.strip('+ ').strip()
    
    print(f"The coefficients are: a = {a:.8f}, b = {b:.4f}, c = {c:.4f}")
    print(f"The equation of the parabola is: y = {equation_str}")
    

else:
    print("Error: Could not determine a unique parabola. The points may be collinear.")