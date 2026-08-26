from core.constants import PLAYLIST_SIZE


def build_playlist_prompt(genre: str) -> str:
    return (
        f"Suggest exactly {PLAYLIST_SIZE} real, existing songs by real artists in the {genre} genre. "
        "Respond with a json object with a single key \"songs\", holding an array of "
        f"exactly {PLAYLIST_SIZE} objects, each with a \"title\" key and an \"artist\" key. "
        "Do not invent songs or artists. "
        "Respond with json only: no markdown code fences, no preamble, no numbering, "
        "no commentary, and no text outside the json object."
    )
