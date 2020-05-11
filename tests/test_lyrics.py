import os
import tempfile
import unittest
from stixoi.lyrics import yield_n_random_lyrics, clean_lyrics, \
    write_n_random_lyrics_to_file


class LyricsTestCase(unittest.TestCase):
    def test_random_lyrics(self):
        # Check wrong inputs
        with self.assertRaises(AssertionError):
            for _ in yield_n_random_lyrics(0):
                pass

        with self.assertRaises(AssertionError):
            s = '2'
            for _ in yield_n_random_lyrics(s):
                pass

        for one in yield_n_random_lyrics(3):
            self.assertIsNotNone(one)

    def test_clean_lyrics(self):
        lyr = '0\n1 \r\n  2 \n\n\r\n3 \r\n4 \n 5\n\n '
        output = clean_lyrics(lyr)
        expected_output = '\t'.join([str(i) for i in range(6)])
        self.assertEqual(output, expected_output)

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
