import os
import unittest
import tempfile
from count_downloads import count_files_in_downloads

class TestCountDownloads(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_downloads_path = tempfile.mkdtemp()
        self.original_downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        self.original_listdir = os.listdir

        # Mock the os.listdir to point to the temporary directory
        os.listdir = lambda path: self.original_listdir(self.test_downloads_path) if path == self.original_downloads_path else self.original_listdir(path)

    def tearDown(self):
        # Restore the original os.listdir
        os.listdir = self.original_listdir

        # Clean up the temporary directory
        for file in os.listdir(self.test_downloads_path):
            file_path = os.path.join(self.test_downloads_path, file)
            os.remove(file_path)
        os.rmdir(self.test_downloads_path)

    def test_count_files(self):
        # Create dummy files in the temporary directory
        for i in range(5):
            with open(os.path.join(self.test_downloads_path, f'test_file_{i}.txt'), 'w') as f:
                f.write('This is a test file.')

        # Capture the output of the function
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output
        count_files_in_downloads()
        sys.stdout = sys.__stdout__

        # Check if the output is correct
        self.assertIn("The number of files in the Downloads folder is: 5", captured_output.getvalue())

if __name__ == "__main__":
    unittest.main()