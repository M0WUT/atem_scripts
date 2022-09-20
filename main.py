from macro_lib import Macro, Source

# Camera definitions
FACE_CAM = Source.CAM1
DESK_CAM = Source.CAM2
MONITOR = Source.CAM3
EFFECTS_CAM = Source.CAM4
SPECTRUM_ANALYSER = Source.CAM5
OSCILLOSCOPE = Source.CAM6
VNA = Source.CAM7

# Upstream Keyer uses
USK_FACE = 1
USK_LOGO = 2
USK_VNA = 3

def add_face_bottom_right(macro: Macro):
    """Adds face cam to bottom right corner"""
    macro.add_upstream_key(
        keyNumber=USK_FACE,
        source=FACE_CAM,
        xPos=13,
        yPos=-7,
        xSize=0.2,
        ySize=0.2,
    )



macro1 = Macro(0, "Monitor with Face", "Fullscreen monitor with face in standard position")
macro1.set_fastest_ftb_speed()
macro1.toggle_ftb()
macro1.disable_all_keyers()
macro1.set_input_source(MONITOR)
add_face_bottom_right(macro1)
macro1.toggle_ftb()
macro1.print()