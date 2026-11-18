
from model import *
from simulation import run_simulation


def display_project_information():
    print("=" * 65)
    print("TUGAS AKHIR 06 - PEMODELAN DAN SIMULASI")
    print("SISTEM PENGATURAN SUHU RUANGAN MENGGUNAKAN PEMANAS LISTRIK")
    print("=" * 65)

    print("\n1. TUJUAN SIMULASI")
    print(
        "Menganalisis perubahan suhu ruangan akibat penggunaan "
        "pemanas listrik."
    )

    print("\n2. DIAGRAM SISTEM")
    print(
        "Diagram sistem akan dibuat dan disimpan sebagai "
        "00_diagram_sistem.png."
    )

    print("\n3. ASUMSI MODEL")
    assumptions = [
        "Suhu udara dalam ruangan dianggap merata.",
        "Massa dan kalor jenis udara konstan.",
        "Suhu lingkungan luar konstan.",
        "Daya pemanas dianggap konstan saat aktif.",
        "Perpindahan panas mengikuti model linear UA(T-Ta).",
        "Tidak terdapat sumber panas lain.",
        "Tidak terjadi pertukaran massa udara.",
        "Efisiensi pemanas dianggap 100%.",
        "Nilai U dan luas area perpindahan panas konstan."
    ]
    for item in assumptions:
        print("- " + item)

    print("\n4. KETERGANTUNGAN RUANG")
    print(
        "Model tidak memiliki ketergantungan spasial. "
        "Suhu hanya bergantung pada waktu, sehingga menggunakan ODE."
    )

    print("\n5. PERSAMAAN NERACA ENERGI")
    print("m * cp * dT/dt = P * u(t) - U * A * (T - Ta)")

    print("\n6. DERAJAT KEBEBASAN (DOF)")
    print(
        "Terdapat satu variabel keadaan T(t) dan satu persamaan ODE. "
        "Setelah parameter, input, dan kondisi awal ditentukan, "
        "DOF = 0."
    )

    print("\n7. KLASIFIKASI INPUT")
    print("Variabel tetap       : m, cp, P, U, A")
    print("Variabel gangguan    : suhu lingkungan Ta")
    print("Variabel manipulasi  : u(t), yaitu daya pemanas 0 sampai 1")

    print("\n8. KLASIFIKASI OUTPUT")
    print("Variabel keadaan     : T(t)")
    print("Variabel terkendali  : suhu ruangan T(t)")

    print("\n9. PERSAMAAN MODEL")
    print(
        f"m * cp = {AIR_DENSITY * ROOM_VOLUME * AIR_CP:.2f} J/°C"
    )
    print(f"U * A  = {U * AREA:.2f} W/°C")
    print(
        "dT/dt = [P*u(t) - U*A*(T-Ta)] / (m*cp)"
    )

    print("\n10. SIMULASI KEADAAN TUNAK")
    for u in [0, 0.5, 1]:
        temp = steady_state_temperature(u)
        print(
            f"Input pemanas {u * 100:5.1f}% "
            f"-> Suhu tunak {temp:.2f} °C"
        )

    thermal_capacity = (
        AIR_DENSITY * ROOM_VOLUME * AIR_CP
    )
    heat_loss_coefficient = U * AREA
    time_constant = thermal_capacity / heat_loss_coefficient

    print(f"\nKapasitas termal     : {thermal_capacity:.2f} J/°C")
    print(f"Koefisien kehilangan: {heat_loss_coefficient:.2f} W/°C")
    print(f"Konstanta waktu     : {time_constant:.2f} detik")

    print("\n11. SIMULASI SINYAL KONTROL")
    print("Program menjalankan:")
    print("- Step")
    print("- Impulse (didekati menggunakan pulsa 10 detik)")
    print("- Ramp")
    print("- Sinusoidal")


if __name__ == "__main__":
    display_project_information()
    run_simulation()

    print("\nSIMULASI SELESAI.")
