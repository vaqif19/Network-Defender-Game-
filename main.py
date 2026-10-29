"""Giriş nöqtəsi: python main.py

Mövzu 2: daxiletmə/çıxarış (input, print), sətir metodları, dilimləmə.
Mövzu 7: modulun idxalı, if __name__ == "__main__".
"""
import sys

from network_defender import GameApp
from network_defender.utils import log


def ask_player_name():
    """Konsoldan oyunçu adını alır. Boş buraxılsa 'Player' olur."""
    try:
        name = input("Oyunçu adı (Enter = Player): ").strip()
    except EOFError:               # konsol yoxdursa (məs., IDE-də input bağlıdırsa)
        name = ""
    return name[:12] or "Player"   # maksimum 12 simvol


def main():
    log("Python", sys.version.split()[0], "| Network Defender starting")
    app = GameApp(player_name=ask_player_name())
    app.run()


if __name__ == "__main__":
    main()
