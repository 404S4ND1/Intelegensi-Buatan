from itertools import combinations

# Variabel dan Domain
variables = ['Ani', 'Budi', 'Citra', 'Dedi', 'Eka']
domains = {var: ['K1', 'K2'] for var in variables}

# Constraint fungsi
def is_consistent(assignment, var, value):
    # Tambahkan nilai sementara
    assignment[var] = value

    # 1. Ani ≠ Budi
    if 'Ani' in assignment and 'Budi' in assignment:
        if assignment['Ani'] == assignment['Budi']:
            return False

    # 2. Citra = Dedi
    if 'Citra' in assignment and 'Dedi' in assignment:
        if assignment['Citra'] != assignment['Dedi']:
            return False

    # 3. Eka tidak boleh sendirian
    if 'Eka' in assignment:
        val_eka = assignment['Eka']
        teman = [v for v in assignment if assignment[v] == val_eka and v != 'Eka']
        if len(teman) == 0 and len(assignment) == len(variables):
            return False

    # 4. Minimal 2 per kelompok (diperiksa di akhir)
    if len(assignment) == len(variables):
        group_counts = {'K1': 0, 'K2': 0}
        for v in variables:
            group_counts[assignment[v]] += 1
        if group_counts['K1'] < 2 or group_counts['K2'] < 2:
            return False

    return True


# Heuristic: MRV + Degree
def select_unassigned_var(assignment, domains):
    unassigned = [v for v in variables if v not in assignment]
    # MRV
    mrv = min(unassigned, key=lambda var: len(domains[var]))
    # Degree heuristic (tie-break)
    return mrv


# Forward Checking
def forward_checking(var, value, domains, assignment):
    new_domains = {v: list(domains[v]) for v in domains}
    for other_var in variables:
        if other_var not in assignment and other_var != var:
            for val in domains[other_var]:
                temp_assign = dict(assignment)
                temp_assign[other_var] = val
                temp_assign[var] = value
                if not is_consistent(temp_assign, other_var, val):
                    if val in new_domains[other_var]:
                        new_domains[other_var].remove(val)
    return new_domains


# Backtracking Search
def backtrack(assignment, domains):
    if len(assignment) == len(variables):
        return assignment

    var = select_unassigned_var(assignment, domains)
    for value in domains[var]:
        if is_consistent(assignment.copy(), var, value):
            new_assignment = assignment.copy()
            new_assignment[var] = value
            new_domains = forward_checking(var, value, domains, new_assignment)
            result = backtrack(new_assignment, new_domains)
            if result is not None:
                return result
    return None


# Jalankan algoritma
solution = backtrack({}, domains)

# Cetak hasil
if solution:
    print("Solusi ditemukan:")
    for var in variables:
        print(f"{var} -> {solution[var]}")
else:
    print("Tidak ada solusi yang memenuhi semua constraint.")