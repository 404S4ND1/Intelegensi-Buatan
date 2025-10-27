import random
import math

MAHASISWA = ['Ani', 'Budi', 'Citra', 'Dedi', 'Eka']

def hitung_biaya(solusi: tuple) -> int:
    biaya = 0
    
    # Batasan 1: Ani (solusi[0]) dan Budi (solusi[1]) tidak boleh bersama
    if solusi[0] == solusi[1]:
        biaya += 1
        
    # Batasan 2: Citra (solusi[2]) dan Dedi (solusi[3]) harus bersama
    if solusi[2] != solusi[3]:
        biaya += 1
        
    # Batasan 4: Setiap kelompok minimal 2 mahasiswa
    jumlah_k1 = solusi.count(0)
    jumlah_k2 = 5 - jumlah_k1
    
    if jumlah_k1 < 2:
        biaya += 1
    if jumlah_k2 < 2:
        biaya += 1
        
    return biaya

def buat_solusi_awal() -> tuple:
    return tuple(random.randint(0, 1) for _ in range(len(MAHASISWA)))

def dapetin_tetangga_acak(solusi: tuple) -> tuple:
    # Pilih satu indeks mahasiswa (0-4) secara acak
    mhs_pindah = random.randint(0, len(MAHASISWA) - 1)
    
    tetangga = list(solusi)
    
    # Pindahkan mahasiswa tersebut ke grup lain
    tetangga[mhs_pindah] = 1 - tetangga[mhs_pindah]
    
    return tuple(tetangga)

def cetak_solusi(solusi: tuple, biaya: int, nama_algoritma: str):
    print(f"\n--- Hasil Algoritma: {nama_algoritma} ---")
    
    if biaya == 0:
        print(f"Solusi optimal ditemukan (Biaya = {biaya})")
        
        kelompok1 = [MAHASISWA[i] for i, grup in enumerate(solusi) if grup == 0]
        kelompok2 = [MAHASISWA[i] for i, grup in enumerate(solusi) if grup == 1]
                
        print(f"Kelompok 1: {', '.join(kelompok1)}")
        print(f"Kelompok 2: {', '.join(kelompok2)}")
    else:
        print(f"Solusi tidak optimal (Biaya = {biaya}).")
        print(f"Solusi terakhir: {solusi}")
    print("-" * 35)


def simulated_annealing(suhu_awal: float = 100.0, laju_pendinginan: float = 0.995, max_iterasi: int = 5000):

    # Mulai dari solusi acak
    solusi_sekarang = buat_solusi_awal()
    biaya_sekarang = hitung_biaya(solusi_sekarang)
    
    # Menyimpan solusi terbaik yang pernah ditemukan
    solusi_terbaik = solusi_sekarang
    biaya_terbaik = biaya_sekarang
    
    suhu = suhu_awal
    
    for _ in range(max_iterasi):
        # Jika solusi optimal ditemukan, hentikan pencarian
        if biaya_terbaik == 0:
            break
            
        # Hentikan jika suhu sudah terlalu rendah (proses pendinginan selesai)
        if suhu <= 0.001:
            break
            
        # Ambil satu tetangga acak
        tetangga = dapetin_tetangga_acak(solusi_sekarang)
        biaya_tetangga = hitung_biaya(tetangga)
        
        # Hitung perbedaan biaya
        selisih_biaya = biaya_tetangga - biaya_sekarang
        
        if selisih_biaya < 0:
            # Jika tetangga lebih baik (biaya lebih rendah), selalu terima
            solusi_sekarang = tetangga
            biaya_sekarang = biaya_tetangga
        else:
            # Jika tetangga lebih buruk (biaya lebih tinggi),
            # terima berdasarkan probabilitas
            probabilitas = math.exp(-selisih_biaya / suhu)
            if random.random() < probabilitas:
                solusi_sekarang = tetangga
                biaya_sekarang = biaya_tetangga
                
        # Perbarui solusi terbaik jika solusi saat ini lebih baik
        if biaya_sekarang < biaya_terbaik:
            solusi_terbaik = solusi_sekarang
            biaya_terbaik = biaya_sekarang
            
        # Melakukan pendinginan (cooling) suhu
        suhu *= laju_pendinginan
        
    return solusi_terbaik, biaya_terbaik


if __name__ == "__main__":
    print("Menjalankan Simulated Annealing...")
    
    solusi, biaya = simulated_annealing()
    
    cetak_solusi(solusi, biaya, "Simulated Annealing")