import random


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
    # (Ini secara implisit memenuhi Batasan 3: Eka tidak sendirian)
    jumlah_k1 = solusi.count(0)
    jumlah_k2 = 5 - jumlah_k1
    
    if jumlah_k1 < 2:
        biaya += 1
    if jumlah_k2 < 2:
        biaya += 1
        
    return biaya

def buat_solusi_awal() -> tuple:
    return tuple(random.randint(0, 1) for _ in range(len(MAHASISWA)))

def dapetin_semua_tetangga(solusi: tuple) -> list[tuple]:
    list_tetangga = []
    for i in range(len(MAHASISWA)):
        # Konversi tuple ke list untuk modifikasi
        tetangga = list(solusi)
        
        # Pindahkan mahasiswa ke grup lain (flip 0 -> 1 atau 1 -> 0)
        tetangga[i] = 1 - tetangga[i] 
        
        # Konversi kembali ke tuple sebelum ditambahkan
        list_tetangga.append(tuple(tetangga))
    return list_tetangga

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


def hill_climbing(max_percobaan: int = 100):
    solusi_terbaik = None
    biaya_terbaik = float('inf') # Inisialisasi biaya terbaik ke tak terhingga
    
    # Loop untuk Random Restart
    for _ in range(max_percobaan):
        
        # Hasilkan solusi acak baru untuk setiap percobaan
        solusi_sekarang = buat_solusi_awal()
        biaya_sekarang = hitung_biaya(solusi_sekarang)

        # Proses 'mendaki' (mencari biaya terendah)
        while True:
            # Evaluasi semua tetangga
            tetangga_list = dapetin_semua_tetangga(solusi_sekarang)
            
            solusi_lanjut = None
            biaya_lanjut = biaya_sekarang

            # Cari tetangga dengan biaya terendah (terbaik)
            for tetangga in tetangga_list:
                biaya_tetangga = hitung_biaya(tetangga)
                if biaya_tetangga < biaya_lanjut:
                    solusi_lanjut = tetangga
                    biaya_lanjut = biaya_tetangga
            
            # Jika tidak ada tetangga yang lebih baik, pencarian buntu (local minimum)
            if solusi_lanjut is None:
                break
            
            # Jika ditemukan tetangga lebih baik, pindah ke tetangga tersebut
            solusi_sekarang = solusi_lanjut
            biaya_sekarang = biaya_lanjut

        # Bandingkan hasil dari percobaan ini dengan solusi terbaik global
        if biaya_sekarang < biaya_terbaik:
            solusi_terbaik = solusi_sekarang
            biaya_terbaik = biaya_sekarang
        
        # Jika solusi optimal (biaya 0) ditemukan, hentikan pencarian
        if biaya_terbaik == 0:
            break
            
    # Kembalikan solusi terbaik yang ditemukan dari semua percobaan
    return solusi_terbaik, biaya_terbaik


if __name__ == "__main__":
    print("Menjalankan Hill Climbing (Random Restart)...")
    
    solusi, biaya = hill_climbing()
    
    cetak_solusi(solusi, biaya, "Hill Climbing (Random Restart)")