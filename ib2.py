# --- Representasi Knowledge Base (Aturan) ---
knowledge_base = {
    'R1': {'if': ['Mesin Mati Total'], 'then': 'Cek Kelistrikan', 'priority': 1},
    'R2': {'if': ['Mesin Berputar Lambat'], 'then': 'Aki Lemah', 'priority': 2},
    'R3': {'if': ['Lampu Redup'], 'then': 'Aki Lemah', 'priority': 2},
    'R4': {'if': ['Aki Lemah', 'Tidak ada Karat pada Terminal'], 'then': 'Ganti Aki', 'priority': 3},
    'R5': {'if': ['Suara Klik saat Start'], 'then': 'Aki Lemah', 'priority': 2},
    'R6': {'if': ['Mesin Mati Total', 'Tidak ada Suara'], 'then': 'Fungsi Kelistrikan Terputus', 'priority': 3},
    'R7': {'if': ['Aki Lemah'], 'then': 'Mesin Sulit Start', 'priority': 1},
    'R8': {'if': ['Cek Kelistrikan', 'Terjadi Konsleting'], 'then': 'Isolasi Kelistrikan', 'priority': 4},
}

# --- Representasi Fact Base (Fakta Awal) ---
initial_facts = {'Mesin Mati Total', 'Suara Klik saat Start', 'Tidak ada Karat pada Terminal'}

# --- Implementasi Forward Chaining ---
def solve_forward_chaining(rules, facts):
    """
    Melakukan inferensi Forward Chaining berdasarkan aturan dan fakta.
    Juga menerapkan Conflict Resolution sesuai spesifikasi.
    """
    current_facts = set(facts)
    rules_fired = set()
    new_facts_derived = []
    simulation_log = []
    
    iteration = 1
    while True:
        conflict_set = [] # Kumpulan aturan yang dapat dieksekusi

        # 1. Matching
        for rule_id, rule_data in rules.items():
            if rule_id not in rules_fired:
                all_conditions_met = True
                for condition in rule_data['if']:
                    if condition not in current_facts:
                        all_conditions_met = False
                        break
                
                if all_conditions_met:
                    specificity = len(rule_data['if'])
                    conflict_set.append((rule_id, rule_data['priority'], specificity))

        # 2. Conflict Resolution
        if not conflict_set:
            simulation_log.append("\n== Selesai: Tidak ada aturan baru yang bisa dieksekusi. ==")
            break

        # Urutkan berdasarkan Prioritas (desc) lalu Spesifisitas (desc)
        conflict_set.sort(key=lambda x: (x[1], x[2]), reverse=True)
        
        best_rule_id = conflict_set[0][0]
        
        # 3. Action (Act)
        new_fact = rules[best_rule_id]['then']
        rules_fired.add(best_rule_id) # Menerapkan Refractoriness

        log_entry = f"\n--- Iterasi {iteration} ---"
        log_entry += f"\nConflict Set (Aturan yang bisa dieksekusi): {[r[0] for r in conflict_set]}"
        log_entry += f"\nResolusi Konflik (Rule Order > Spesifisitas): Memilih {best_rule_id} (Prioritas: {conflict_set[0][1]}, Spesifisitas: {conflict_set[0][2]})"
        
        if new_fact not in current_facts:
            current_facts.add(new_fact)
            new_facts_derived.append(new_fact)
            log_entry += f"\nTindakan: Aturan {best_rule_id} dieksekusi. Fakta baru ditambahkan: '{new_fact}'"
        else:
            log_entry += f"\nTindakan: Aturan {best_rule_id} dieksekusi. Fakta '{new_fact}' sudah ada."

        simulation_log.append(log_entry)
        iteration += 1

    return new_facts_derived, current_facts, simulation_log

# --- Implementasi Backward Chaining ---
backward_trace = [] # Global var untuk menyimpan jejak rekursi

def solve_backward_chaining(rules, facts, goal, indent=""):
    """
    Melakukan inferensi Backward Chaining secara rekursif untuk membuktikan goal.
    """
    global backward_trace
    if not indent: # Reset trace jika ini panggilan awal
        backward_trace = []

    backward_trace.append(f"{indent}Mencoba membuktikan goal: '{goal}'")
    
    # Base Case 1: Goal ada di fakta awal
    if goal in facts:
        backward_trace.append(f"{indent} -> SUKSES: Goal '{goal}' ditemukan di fakta awal.")
        return True

    # Recursive Step: Cari aturan yang menghasilkan goal ini
    applicable_rules = []
    for rule_id, rule_data in rules.items():
        if rule_data['then'] == goal:
            applicable_rules.append((rule_id, rule_data['if']))

    if not applicable_rules:
        backward_trace.append(f"{indent} -> GAGAL: Tidak ada aturan yang menghasilkan '{goal}'.")
        return False

    # Coba setiap aturan yang berlaku
    for rule_id, sub_goals in applicable_rules:
        backward_trace.append(f"{indent}Mencoba aturan {rule_id}: IF ({' AND '.join(sub_goals)}) THEN {goal}")
        all_sub_goals_proven = True
        
        for sub_goal in sub_goals:
            # Panggil rekursif untuk setiap sub-goal
            if not solve_backward_chaining(rules, facts, sub_goal, indent + "  "):
                all_sub_goals_proven = False
                backward_trace.append(f"{indent} -> GAGAL: Aturan {rule_id} gagal karena sub-goal '{sub_goal}' tidak terbukti.")
                break 
        
        if all_sub_goals_proven:
            backward_trace.append(f"{indent} -> SUKSES: Semua sub-goal untuk aturan {rule_id} terbukti. Goal '{goal}' terbukti.")
            return True

    # Base Case 2: Semua aturan yang berlaku sudah dicoba dan gagal
    backward_trace.append(f"{indent} -> GAGAL: Semua aturan untuk membuktikan '{goal}' telah gagal.")
    return False

# --- Skrip Utama untuk Simulasi ---
if __name__ == "__main__":
    print("==========================================================")
    print("🏁 MEMULAI SIMULASI FORWARD CHAINING (TUGAS 1 & 3)")
    print("==========================================================")
    print(f"Fakta Awal: {initial_facts}")
    
    derived_facts, all_facts, fc_log = solve_forward_chaining(knowledge_base, initial_facts)
    
    for log_entry in fc_log:
        print(log_entry)
        
    print(f"\nKesimpulan Akhir (Fakta Baru yang Ditemukan): {derived_facts}")
    print(f"Database Fakta Final: {all_facts}")

    print("\n\n==========================================================")
    print("🏁 MEMULAI SIMULASI BACKWARD CHAINING (TUGAS 2)")
    print("==========================================================")
    goal_to_prove = "Ganti Aki"
    print(f"Fakta Awal: {initial_facts}")
    print(f"Goal: Membuktikan '{goal_to_prove}'")
    print("--- Jejak Inferensi (Trace) ---")

    is_proven = solve_backward_chaining(knowledge_base, initial_facts, goal_to_prove)
    
    for trace_line in backward_trace:
        print(trace_line)
        
    print("--- Hasil Akhir ---")
    if is_proven:
        print(f"Hasil: Goal '{goal_to_prove}' BERHASIL dibuktikan.")
    else:
        print(f"Hasil: Goal '{goal_to_prove}' GAGAL dibuktikan.")
