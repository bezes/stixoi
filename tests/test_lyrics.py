import os
import tempfile
import unittest
from stixoi.lyrics import get_n_random_lyrics, \
    clean_lyrics, clean_title, \
    write_n_random_lyrics_to_file


class LyricsTestCase(unittest.TestCase):
    def test_random_lyrics(self):
        # Check wrong inputs
        with self.assertRaises(ValueError):
            get_n_random_lyrics(0)

        three = get_n_random_lyrics(3)
        self.assertIsInstance(three, dict)
        self.assertEqual(len(three), 3)

    def test_clean_lyrics(self):
        lyr = '\r\n   0\r\n1 \r\n\r\n 2     3 \n 4   \n  '
        output = clean_lyrics(lyr)
        expected_output = '0\n1\n2 3\n4'
        self.assertEqual(output, expected_output)

    def test_clean_title(self):
        title = ' My \r\n title  is\nawesome \n'
        cleaned_title = clean_title(title)
        expected_title = 'My title is awesome'
        self.assertEqual(cleaned_title, expected_title)

    def test_write_n_to_file(self):
        with tempfile.NamedTemporaryFile() as f:
            fname = f.name
        try:
            write_n_random_lyrics_to_file(n=1, filename=f.name)
            with open(fname, 'r', encoding='utf-8') as f:
                f.seek(0)
                text = f.read()
                self.assertIsNotNone(text)
        finally:
            if os.path.exists(fname):
                os.remove(fname)


if __name__ == '__main__':
    unittest.main()
