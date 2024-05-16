
import unittest
import textlink as tl

example_url  = "https://www.example.com/"
example_name = "example"

example_link_object = tl.TextLink(example_url)

example_xdg_object = tl.FreeDesktop(example_url, example_name)
example_xdg_filepath = "tests/example.desktop"
with open(example_xdg_filepath, "r") as f:
    example_xdg_string = f.read()
spaced_xdg_filepath = "tests/spaced.desktop"
with open(spaced_xdg_filepath, "r") as f:
    spaced_xdg_string = f.read()
app_xdg_filepath = "tests/firefox.desktop"
with open(app_xdg_filepath, "r") as f:
    app_xdg_string = f.read()

example_win_object = tl.WindowsURL(example_url)
example_win_filepath  = "tests/example.url"
with open(example_win_filepath, "r") as f:
    example_win_string = f.read()
spaced_win_filepath  = "tests/spaced.url"
with open(spaced_win_filepath, "r") as f:
    spaced_win_string = f.read()


class TestPrintString(unittest.TestCase):

    def test_textlink(self):
        self.assertEqual(str(example_link_object), example_url)

    def test_freedesktop(self):
        self.assertEqual(str(example_xdg_object), example_xdg_string)

    def test_windowsurl(self):
        self.assertEqual(str(example_win_object), example_win_string)


class TestParseString(unittest.TestCase):

    def test_textlink(self):
        with self.assertRaises(TypeError):
            tl.TextLink(314)

    def test_freedesktop(self):
        xdg = tl.FreeDesktop.read_string(example_xdg_string)
        self.assertEqual(xdg, example_xdg_object)
        xdg = tl.FreeDesktop.read_string(spaced_xdg_string)
        self.assertEqual(xdg, example_xdg_object)
        with self.assertRaises(tl.InvalidDesktopEntryType):
            tl.FreeDesktop.read_string(app_xdg_string)

    def test_windowsurl(self):
        win = tl.WindowsURL.read_string(example_win_string)
        self.assertEqual(win, example_win_object)
        win = tl.WindowsURL.read_string(spaced_win_string)
        self.assertEqual(win, example_win_object)


class TestParseFile(unittest.TestCase):

    def test_freedesktop(self):
        with open(example_xdg_filepath, "r") as f:
            xdg = tl.FreeDesktop.read_file(f)
        self.assertEqual(xdg, example_xdg_object)
        with open(spaced_xdg_filepath, "r") as f:
            xdg = tl.FreeDesktop.read_file(f)
        self.assertEqual(xdg, example_xdg_object)
        with open(app_xdg_filepath, "r") as f:
            with self.assertRaises(tl.InvalidDesktopEntryType):
                tl.FreeDesktop.read_file(f)

    def test_windowsurl(self):
        with open(example_win_filepath, "r") as f:
            win = tl.WindowsURL.read_file(f)
        self.assertEqual(win, example_win_object)
        with open(spaced_win_filepath, "r") as f:
            win = tl.WindowsURL.read_file(f)
        self.assertEqual(win, example_win_object)


class TestConversion(unittest.TestCase):
    name = example_name
    link = example_link_object
    xdg  = example_xdg_object
    win  = example_win_object

    def test_totextlink(self):
        self.assertEqual(self.link, self.link.toTextLink())
        self.assertEqual(self.link, self.xdg.toTextLink())
        self.assertEqual(self.link, self.win.toTextLink())

    def test_tofreedesktop(self):
        self.assertEqual(self.xdg, self.link.toFreeDesktop(self.name))
        self.assertEqual(self.xdg, self.xdg.toFreeDesktop())
        self.assertEqual(self.xdg, self.win.toFreeDesktop(self.name))

    def test_towindowsurl(self):
        self.assertEqual(self.win, self.link.toWindowsURL())
        self.assertEqual(self.win, self.xdg.toWindowsURL())
        self.assertEqual(self.win, self.win.toWindowsURL())


if __name__ == '__main__':
    unittest.main()
