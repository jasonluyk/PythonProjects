import subprocess
import shlex
import wx
from PIL import ImageFont



def _fc_match_file(family: str, bold: bool, italic: bool, oblique: bool = False) -> str | None:
    """
    Use fontconfig's fc-match to resolve (family + weight + slant) to a real font file.
    Returns a file path or None.
    """
    # fontconfig "slant" values: roman=0, italic=100, oblique=110
    slant = 0
    if italic:
        slant = 100
    elif oblique:
        slant = 110

    # fontconfig "weight": regular=80, bold=200 (common values)
    weight = 200 if bold else 80

    # Build a fontconfig pattern
    # Example: "DejaVu Sans:weight=200:slant=100"
    pattern = f"{family}:weight={weight}:slant={slant}"

    try:
        # -f prints only the file path
        cmd = ["fc-match", "-f", "%{file}\n", pattern]
        out = subprocess.check_output(cmd, text=True).strip()
        return out if out else None
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None

def wxfont_to_pilfont(wx_font: wx.Font) -> ImageFont.FreeTypeFont:
    """
    Convert a wx.Font -> PIL ImageFont by resolving the selected face/weight/slant to a real file via fontconfig.
    """
    family = wx_font.GetFaceName()  # face/family name
    size = wx_font.GetPointSize()

    # wx weight/style
    bold = (wx_font.GetWeight() >= wx.FONTWEIGHT_BOLD)
    style = wx_font.GetStyle()
    italic = (style == wx.FONTSTYLE_ITALIC)
    oblique = (style == wx.FONTSTYLE_SLANT)

    font_file = _fc_match_file(family, bold=bold, italic=italic, oblique=oblique)

    # Fallbacks if exact face name doesn't resolve well (some faces are aliases)
    if not font_file:
        # Try with family name from font family enum if face fails
        # (wx sometimes returns empty face names depending on platform)
        font_file = _fc_match_file("sans-serif", bold=bold, italic=italic, oblique=oblique)

    if not font_file:
        raise RuntimeError(
            f"Couldn't resolve '{family}' (bold={bold}, style={style}) to a font file. "
            f"Make sure fontconfig is installed and fc-match works in WSL."
        )

    return ImageFont.truetype(font_file, size)

def choose_pil_font_with_wx() -> ImageFont.FreeTypeFont | None:
    """
    Shows wx FontDialog and returns a PIL ImageFont (or None if cancelled).
    """
    app = wx.App(False)  # if you already have a wx.App, remove this line and reuse it
    dlg = wx.FontDialog(None, wx.FontData())
    pil_font = None

    if dlg.ShowModal() == wx.ID_OK:
        wx_font = dlg.GetFontData().GetChosenFont()
        pil_font = wxfont_to_pilfont(wx_font)

    dlg.Destroy()
    return pil_font
