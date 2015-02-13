import esccsi
from escutil import AssertEQ, GetCursorPosition, GetScreenSize
from esctypes import Point

class CNLTests(object):
  def __init__(self, args):
    pass

  def test_CNL_DefaultParam(self):
    """CNL moves the cursor down 1 with no parameter given."""
    esccsi.CUP(Point(5, 3))
    esccsi.CNL()
    position = GetCursorPosition()
    AssertEQ(position.x(), 1)
    AssertEQ(position.y(), 4)

  def test_CNL_ExplicitParam(self):
    """CNL moves the cursor down by the passed-in number of lines."""
    esccsi.CUP(Point(6, 3))
    esccsi.CNL(2)
    position = GetCursorPosition()
    AssertEQ(position.x(), 1)
    AssertEQ(position.y(), 5)

  def test_CNL_StopsAtBottomLine(self):
    """CNL moves the cursor down, stopping at the last line."""
    esccsi.CUP(Point(6, 3))
    height = GetScreenSize().height()
    esccsi.CNL(height)
    position = GetCursorPosition()
    AssertEQ(position.x(), 1)
    AssertEQ(position.y(), height)

  def test_CNL_StopsAtBottomLineWhenBegunBelowScrollRegion(self):
    """When the cursor starts below the scroll region, CNL moves it down to the
    bottom of the screen."""
    # Set a scroll region. This must be done first because DECSTBM moves the cursor to the origin.
    esccsi.DECSTBM(4, 5)
    esccsi.DECSET(esccsi.DECLRMM)
    esccsi.DECSLRM(5, 10)

    # Position the cursor below the scroll region
    esccsi.CUP(Point(7, 6))

    # Move it down by a lot
    height = GetScreenSize().height()
    esccsi.CNL(height)

    # Ensure it stopped at the bottom of the screen
    position = GetCursorPosition()
    AssertEQ(position.y(), height)
    AssertEQ(position.x(), 5)

  def test_CNL_StopsAtBottomMarginInScrollRegion(self):
    """When the cursor starts within the scroll region, CNL moves it down to the
    bottom margin but no farther."""
    # Set a scroll region. This must be done first because DECSTBM moves the cursor to the origin.
    esccsi.DECSTBM(2, 4)
    esccsi.DECSET(esccsi.DECLRMM)
    esccsi.DECSLRM(5, 10)

    # Position the cursor within the scroll region
    esccsi.CUP(Point(7, 3))

    # Move it up by more than the height of the scroll region
    esccsi.CNL(99)

    # Ensure it stopped at the bottom of the scroll region.
    position = GetCursorPosition()
    AssertEQ(position.y(), 4)
    AssertEQ(position.x(), 5)

