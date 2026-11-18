
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from model import (
    ROOM_VOLUME,
    AIR_DENSITY,
    AIR_CP,
    HEATER_POWER,
    U,
    AREA,
    AMBIENT_TEMP,
    INITIAL_TEMP,
    SIMULATION_TIME,
    heater_input,
    temperature_derivative,
    steady_state_temperature
)

OUTPUT_DIR = "hasil_simulasi"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_system_diagram():
    """Membuat diagram sederhana sistem pengaturan suhu ruangan."""

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis("off")

    # Ruangan
    ax.add_patch(
        plt.Rectangle(
            (4, 1.5), 4, 3,
            fill=False, linewidth=2
        )
    )
    ax.text(6, 4.7, "RUANGAN", ha="center",
            fontsize=13, fontweight="bold")
    ax.text(6, 3.3, "Udara ruangan\nT(t)",
            ha="center", va="center", fontsize=12)

    # Pemanas
    ax.add_patch(
        plt.Rectangle(
            (0.5, 2.4), 2, 1.2,
            fill=False, linewidth=2
        )
    )
    ax.text(1.5, 3, "Pemanas Listrik",
            ha="center", va="center")

    ax.annotate(
        "", xy=(4, 3), xytext=(2.5, 3),
        arrowprops=dict(arrowstyle="->", linewidth=2)
    )
    ax.text(3.2, 3.35, "P × u(t)",
            ha="center", fontsize=10)

    # Lingkungan
    ax.text(10, 4.1, "Lingkungan luar",
            ha="center", fontsize=11)
    ax.text(10, 3.5, f"Ta = {AMBIENT_TEMP} °C",
            ha="center", fontsize=10)

    ax.annotate(
        "", xy=(8, 2.3), xytext=(9.3, 2.3),
        arrowprops=dict(arrowstyle="->",
                        linewidth=2, color="red")
    )
    ax.text(8.8, 1.8, "Panas keluar\nUA(T - Ta)",
            ha="center", color="red", fontsize=10)

    ax.text(
        6, 0.6,
        "Neraca energi: mcₚ dT/dt = P u(t) - UA(T - Ta)",
        ha="center", fontsize=11
    )

    plt.tight_layout()
    fig.savefig(
        os.path.join(OUTPUT_DIR, "00_diagram_sistem.png"),
        dpi=300,
        bbox_inches="tight"
    )
    plt.close(fig)


def simulate_case(case_name, duration, max_step=2.0):
    """Menjalankan simulasi untuk satu jenis sinyal pemanas."""

    time_points = np.linspace(0, duration, 600)

    result = solve_ivp(
        fun=lambda t, T: [
            temperature_derivative(
                t, T[0], case_name
            )
        ],
        t_span=(0, duration),
        y0=[INITIAL_TEMP],
        method="RK45",
        t_eval=time_points,
        max_step=max_step
    )

    if not result.success:
        raise RuntimeError(
            f"Simulasi {case_name} gagal: {result.message}"
        )

    return result.t, result.y[0]


def plot_steady_state():
    """Grafik suhu keadaan tunak terhadap daya pemanas."""

    control_values = np.linspace(0, 1, 11)
    temperatures = [
        steady_state_temperature(u)
        for u in control_values
    ]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(
        control_values * 100,
        temperatures,
        marker="o"
    )
    ax.set_title("Suhu Keadaan Tunak")
    ax.set_xlabel("Persentase Daya Pemanas (%)")
    ax.set_ylabel("Suhu Ruangan (°C)")
    ax.grid(True)

    fig.savefig(
        os.path.join(OUTPUT_DIR, "01_steady_state.png"),
        dpi=300
    )
    plt.close(fig)


def plot_response(case_name, title, filename, duration):
    """Grafik respons suhu dan sinyal pemanas."""

    time, temperature = simulate_case(
        case_name, duration
    )
    control = np.array([
        heater_input(t, case_name)
        for t in time
    ])

    fig, axes = plt.subplots(
        2, 1, figsize=(10, 7), sharex=True
    )

    axes[0].plot(time, temperature)
    axes[0].set_title(title)
    axes[0].set_ylabel("Suhu (°C)")
    axes[0].grid(True)

    axes[1].plot(time, control)
    axes[1].set_xlabel("Waktu (detik)")
    axes[1].set_ylabel("Input Pemanas (0–1)")
    axes[1].set_ylim(-0.1, 1.1)
    axes[1].grid(True)

    plt.tight_layout()
    fig.savefig(
        os.path.join(OUTPUT_DIR, filename),
        dpi=300
    )
    plt.close(fig)

    print(
        f"{case_name.upper():10s} | "
        f"Suhu awal: {temperature[0]:.2f} °C | "
        f"Suhu akhir: {temperature[-1]:.2f} °C | "
        f"Suhu maksimum: {np.max(temperature):.2f} °C"
    )


def run_simulation():
    print("\n=== PROSES SIMULASI ===")

    save_system_diagram()
    plot_steady_state()

    plot_response(
        "step",
        "Respons Suhu terhadap Sinyal Step",
        "02_step_response.png",
        SIMULATION_TIME
    )

    plot_response(
        "impulse",
        "Respons Suhu terhadap Pulsa Pendek (Pendekatan Impulse)",
        "03_impulse_response.png",
        SIMULATION_TIME
    )

    plot_response(
        "ramp",
        "Respons Suhu terhadap Sinyal Ramp",
        "04_ramp_response.png",
        SIMULATION_TIME
    )

    plot_response(
        "sinusoidal",
        "Respons Suhu terhadap Sinyal Sinusoidal",
        "05_sinusoidal_response.png",
        SIMULATION_TIME
    )

    print("\nSemua grafik berhasil disimpan di folder:")
    print(OUTPUT_DIR)
