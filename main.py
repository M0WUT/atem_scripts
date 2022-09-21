from macro_lib import Macro, Source

# Camera definitions
FACE_CAM = Source.CAM2
MONITOR = Source.CAM1
SPECTRUM_ANALYSER = Source.CAM3
VNA = Source.CAM4

# Upstream Keyer uses (note that 1 is put on the bottom and 4 on the top)
USK_INSTRUMENT = 1
USK_FACE = 2
USK_FACE = 3


def add_face_standard_position(macro: Macro):
    macro.add_upstream_key(
        keyNumber=USK_FACE,
        source=FACE_CAM,
        xPos=13,
        yPos=-7,
        xSize=0.2,
        ySize=0.2,
    )


macro1 = Macro(
    0, "Monitor with Face", "Fullscreen monitor with face in standard position"
)
macro1.start_stinger()
macro1.disable_non_stinger_keyers()
macro1.set_input_source(MONITOR)
add_face_standard_position(macro1)
macro1.close_stinger()

macro2 = Macro(
    1,
    "Spectrum Analyser with Face",
    "Fullscreen spectrum analyser with face in standard position",
)
macro2.start_stinger()
macro2.disable_non_stinger_keyers()
macro2.set_input_source(Source.BLACK)
macro2.add_upstream_key(
    keyNumber=USK_INSTRUMENT,
    source=SPECTRUM_ANALYSER,
    xPos=-0.5,
    yPos=-0,
    xSize=1,
    ySize=1,
)
add_face_standard_position(macro2)
macro2.close_stinger()

macro3 = Macro(
    2, "VNA with Face", "Fullscreen VNA with face in standard position"
)
macro3.start_stinger()
macro3.disable_non_stinger_keyers()
macro3.set_input_source(Source.BLACK)
macro3.add_upstream_key(
    keyNumber=USK_INSTRUMENT,
    source=VNA,
    xPos=-3.5,
    yPos=-0,
    xSize=1.5,
    ySize=1.5,
)
add_face_standard_position(macro3)
macro3.close_stinger()

for macro in [macro1, macro2, macro3]:
    macro.print()
