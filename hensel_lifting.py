from sympy import symbols, Poly, ZZ

def hensel_lift(f, p, n):
    """Hensel lifting for p-adic solutions"""
    x = symbols('x')
    sols = [k for k in range(p) if f.subs(x, k) % p == 0]
    
    for i in range(1, n):
        new_sols = []
        mod = p ** (i + 1)
        prev_mod = p ** i
        
        for s in sols:
            df_val = f.diff(x).subs(x, s) % p
            f_val = f.subs(x, s) % mod
            
            if df_val != 0:
                t = (-f_val // prev_mod * pow(df_val, -1, p)) % p
                new_sols.append(s + t * prev_mod)
            elif f_val % mod == 0:
                new_sols.append(s)
                
        sols = new_sols
    
    return [s for s in sols if abs(s - round(s)) < 1e-6]

def check_irrational(k, tol=1e-6):
    """Check if solution is irrational"""
    return abs(k - round(k)) > tol

if __name__ == "__main__":
    # Test polynomial x^3 - 3 in Z_3
    f = Poly(symbols('x')**3 - 3, domain=ZZ)
    sols = hensel_lift(f, 3, 5)
    
    if any(check_irrational(sol) for sol in sols):
        raise ValueError("Non-integer solution detected")
        
    assert len(sols) == 0, "Counterexample found!"
    print("3-adic verification passed")
