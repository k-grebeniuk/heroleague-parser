SUPPORTED_DISTANCES = {
    "1 км",
    "5 км",
    "10 км",
    "21.1 км"
}

def is_supported_distance(distance: str) -> bool:
    """
    Проверяет, используется ли дистанция в анализе.

    Args:
        distance (str):
            Нормализованное название дистанции.

    Returns:
        bool:
            True, если дистанция поддерживается,
            иначе False.
    """

    return distance in SUPPORTED_DISTANCES