from esc import NUL, CR, LF
import esccsi
import escio
import esclog
from escutil import AssertEQ, AssertScreenCharsInRectEqual, GetCursorPosition, GetScreenSize, knownBug, vtLevel
from esctypes import Point, Rect

class DECCRATests(object):
  """Copy rectangular area."""
  def __init__(self, args):
    self._args = args

  def prepare(self):
    esccsi.CUP(Point(1, 1))
    escio.Write("abcdefgh" + CR + LF)
    escio.Write("ijklmnop" + CR + LF)
    escio.Write("qrstuvwx" + CR + LF)
    escio.Write("yz012345" + CR + LF)
    escio.Write("ABCDEFGH" + CR + LF)
    escio.Write("IJKLMNOP" + CR + LF)
    escio.Write("QRSTUVWX" + CR + LF)
    escio.Write("YZ6789!@" + CR + LF)

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_DECCRA_nonOverlappingSourceAndDest(self):
    self.prepare()
    esccsi.DECCRA(source_top=2,
                      source_left=2,
                      source_bottom=4,
                      source_right=4,
                      source_page=1,
                      dest_top=5,
                      dest_left=5,
                      dest_page=1)
    AssertScreenCharsInRectEqual(Rect(1, 1, 8, 8),
                                 [ "abcdefgh",
                                   "ijklmnop",
                                   "qrstuvwx",
                                   "yz012345",
                                   "ABCDjklH",
                                   "IJKLrstP",
                                   "QRSTz01X",
                                   "YZ6789!@" ])


  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_DECCRA_overlappingSourceAndDest(self):
    self.prepare()
    esccsi.DECCRA(source_top=2,
                      source_left=2,
                      source_bottom=4,
                      source_right=4,
                      source_page=1,
                      dest_top=3,
                      dest_left=3,
                      dest_page=1)
    AssertScreenCharsInRectEqual(Rect(1, 1, 8, 8),
                                 [ "abcdefgh",
                                   "ijklmnop",
                                   "qrjklvwx",
                                   "yzrst345",
                                   "ABz01FGH",
                                   "IJKLMNOP",
                                   "QRSTUVWX",
                                   "YZ6789!@" ])

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  @knownBug(terminal="xterm", reason="Crashes. Bug reported Feb 11, 2015.",
            shouldTry=False)
  def test_DECCRA_destinationPartiallyOffscreen(self):
    self.prepare()
    size = GetScreenSize()

    esccsi.DECCRA(source_top=2,
                      source_left=2,
                      source_bottom=4,
                      source_right=4,
                      source_page=1,
                      dest_top=size.height() - 1,
                      dest_left=size.width() - 1,
                      dest_page=1)
    AssertScreenCharsInRectEqual(Rect(size.width() - 1,
                                      size.height() - 1,
                                      size.width(),
                                      size.height()),
                                 [ "jk",
                                   "rj" ])

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_DECCRA_defaultValuesInSource(self):
    self.prepare()
    esccsi.DECCRA(source_bottom=2,
                      source_right=2,
                      dest_top=5,
                      dest_left=5,
                      dest_page=1)
    AssertScreenCharsInRectEqual(Rect(1, 1, 8, 8),
                                 [ "abcdefgh",
                                   "ijklmnop",
                                   "qrstuvwx",
                                   "yz012345",
                                   "ABCDabGH",
                                   "IJKLijOP",
                                   "QRSTUVWX",
                                   "YZ6789!@" ])

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_DECCRA_defaultValuesInDest(self):
    self.prepare()
    esccsi.DECCRA(source_top=2,
                      source_left=2,
                      source_bottom=4,
                      source_right=4,
                      source_page=1)
    AssertScreenCharsInRectEqual(Rect(1, 1, 8, 8),
                                 [ "jkldefgh",
                                   "rstlmnop",
                                   "z01tuvwx",
                                   "yz012345",
                                   "ABCDEFGH",
                                   "IJKLMNOP",
                                   "QRSTUVWX",
                                   "YZ6789!@" ])

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented", noop=True)
  def test_DECCRA_invalidSourceRectDoesNothing(self):
    self.prepare()
    esccsi.DECCRA(source_top=2,
                      source_left=2,
                      source_bottom=1,
                      source_right=1,
                      source_page=1,
                      dest_top=5,
                      dest_left=5,
                      dest_page=1)
    AssertScreenCharsInRectEqual(Rect(1, 1, 8, 8),
                                 [ "abcdefgh",
                                   "ijklmnop",
                                   "qrstuvwx",
                                   "yz012345",
                                   "ABCDEFGH",
                                   "IJKLMNOP",
                                   "QRSTUVWX",
                                   "YZ6789!@" ])

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_DECCRA_respectsOriginMode(self):
    self.prepare()

    # Set margins at 2, 2
    esccsi.DECSET(esccsi.DECLRMM)
    esccsi.DECSLRM(2, 9)
    esccsi.DECSTBM(2, 9)

    # Turn on origin mode
    esccsi.DECSET(esccsi.DECOM)

    # Copy from 1,1 to 4,4 - with origin mode, that's 2,2 to 5,5
    esccsi.DECCRA(source_top=1,
                      source_left=1,
                      source_bottom=3,
                      source_right=3,
                      source_page=1,
                      dest_top=4,
                      dest_left=4,
                      dest_page=1)

    # Turn off margins and origin mode
    esccsi.DECRESET(esccsi.DECLRMM)
    esccsi.DECSTBM()
    esccsi.DECRESET(esccsi.DECOM)

    # See what happened.
    AssertScreenCharsInRectEqual(Rect(1, 1, 8, 8),
                                 [ "abcdefgh",
                                   "ijklmnop",
                                   "qrstuvwx",
                                   "yz012345",
                                   "ABCDjklH",
                                   "IJKLrstP",
                                   "QRSTz01X",
                                   "YZ6789!@" ])

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_DECCRA_ignoresMargins(self):
    self.prepare()

    # Set margins
    esccsi.DECSET(esccsi.DECLRMM)
    esccsi.DECSLRM(3, 6)
    esccsi.DECSTBM(3, 6)

    esccsi.DECCRA(source_top=2,
                      source_left=2,
                      source_bottom=4,
                      source_right=4,
                      source_page=1,
                      dest_top=5,
                      dest_left=5,
                      dest_page=1)

    # Remove margins
    esccsi.DECRESET(esccsi.DECLRMM)
    esccsi.DECSTBM()

    # Did it ignore the margins?
    AssertScreenCharsInRectEqual(Rect(1, 1, 8, 8),
                                 [ "abcdefgh",
                                   "ijklmnop",
                                   "qrstuvwx",
                                   "yz012345",
                                   "ABCDjklH",
                                   "IJKLrstP",
                                   "QRSTz01X",
                                   "YZ6789!@" ])

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented")
  def test_DECCRA_overlyLargeSourceClippedToScreenSize(self):
    size = GetScreenSize()

    # Put ab, cX in the bottom right
    esccsi.CUP(Point(size.width() - 1, size.height() - 1))
    escio.Write("ab")
    esccsi.CUP(Point(size.width() - 1, size.height()))
    escio.Write("cX")

    # Copy a 2x2 block starting at the X to the a
    esccsi.DECCRA(source_top=size.height(),
                      source_left=size.width(),
                      source_bottom=size.height() + 1,
                      source_right=size.width() + 1,
                      source_page=1,
                      dest_top=size.height() - 1,
                      dest_left=size.width() - 1,
                      dest_page=1)
    AssertScreenCharsInRectEqual(Rect(size.width() - 1,
                                      size.height() - 1,
                                      size.width(),
                                      size.height()),
                                 [ "Xb", "cX" ])

  @vtLevel(4)
  @knownBug(terminal="iTerm2", reason="Not implemented", noop=True)
  def test_DECCRA_cursorDoesNotMove(self):
    # Make sure something is on screen (so the test is more deterministic)
    self.prepare()

    # Place the cursor
    position = Point(3, 4)
    esccsi.CUP(position)

    # Copy a block
    esccsi.DECCRA(source_top=2,
                      source_left=2,
                      source_bottom=4,
                      source_right=4,
                      source_page=1,
                      dest_top=5,
                      dest_left=5,
                      dest_page=1)

    # Make sure the cursor is where we left it.
    AssertEQ(GetCursorPosition(), position)
