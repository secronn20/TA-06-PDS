
import numpy as np

# ==========================================
# PARAMETER SISTEM
# ==========================================

ROOM_LENGTH = 3.0
ROOM_WIDTH = 3.0
ROOM_HEIGHT = 3.0

ROOM_VOLUME = ROOM_LENGTH * ROOM_WIDTH * ROOM_HEIGHT

AIR_DENSITY = 1.2       # kg/m3
AIR_CP = 1005.0         # J/(kg C)

HEATER_POWER = 1000.0   # Watt

U = 2.5                 # W/(m2 C)
AREA = 20.0             # m2

AMBIENT_TEMP = 25.0     # Derajat Celsius
INITIAL_TEMP = 25.0     # Derajat Celsius

SIMULATION_TIME = 10000 # Detik

# ==========================================
# PARAMETER TURUNAN
# ==========================================

AIR_MASS = AIR_DENSITY * ROOM_VOLUME

THERMAL_CAPACITY = AIR_MASS * AIR_CP

HEAT_LOSS_COEFFICIENT = U * AREA

TIME_CONSTANT = (
    THERMAL_CAPACITY / HEAT_LOSS_COEFFICIENT
)

# ==========================================
# FUNGSI INPUT PEMANAS
# ==========================================

def heater_input(t, signal_type):
    """
    Menghasilkan nilai input pemanas antara 0 sampai 1.
    """

    if signal_type == "step":
        return 1.0

    elif signal_type == "impulse":
        # Pendekatan impulse berupa pulsa 10 detik
        return 1.0 if 0 <= t <= 10 else 0.0

    elif signal_type == "ramp":
        # Input meningkat dari 0 ke 1 selama 2000 detik
        return min(max(t / 2000.0, 0.0), 1.0)

    elif signal_type == "sinusoidal":
        # Gelombang sinus dengan periode 4000 detik
        return 0.5 + 0.5 * np.sin(
            2 * np.pi * t / 4000.0
        )

    else:
        raise ValueError(
            f"Jenis sinyal tidak dikenal: {signal_type}"
        )


# ==========================================
# PERSAMAAN DIFERENSIAL
# ==========================================

def temperature_derivative(t, temperature, signal_type):
    """
    Menghitung laju perubahan suhu ruangan.
    """

    u = heater_input(t, signal_type)

    heat_input = HEATER_POWER * u

    heat_loss = (
        HEAT_LOSS_COEFFICIENT
        * (temperature - AMBIENT_TEMP)
    )

    dT_dt = (
        heat_input - heat_loss
    ) / THERMAL_CAPACITY

    return dT_dt


# ==========================================
# SUHU KEADAAN TUNAK
# ==========================================

def steady_state_temperature(u):
    """
    Menghitung suhu keadaan tunak berdasarkan
    tingkat penggunaan pemanas.
    """

    return (
        AMBIENT_TEMP
        + (HEATER_POWER * u)
        / HEAT_LOSS_COEFFICIENT
    )
