# test.py

import unittest
from main import decode_bencode  

class TestBencodeDecoder(unittest.TestCase):

    def test_single_string(self):
        result = decode_bencode(b"5:hello")
        print(f"test_single_string: {result}")
        self.assertEqual(result, b"hello")
    
    def test_integer(self):
        result = decode_bencode(b"i42e")
        print(f"test_integer: {result}")
        self.assertEqual(result, 42)

    def test_list(self):
        result = decode_bencode(b"l5:helloi52ee")
        print(f"test list: {result}")
        self.assertEqual(result, [b"hello", 52])
    
    def test_dict(self):
        result = decode_bencode(b"d3:foo5:mango5:helloi52ee")
        print(f"test dict: {result}")
        self.assertEqual(result, {"foo":b"mango","hello":52})

    def test_decode_bencode_from_file(self):
        # Read the bencoded data from a file
        with open('C:\Users\oskar\codecrafters-bittorrent-python', 'rb') as f:  # Use 'rb' for binary mode
            bencoded_torrent_data = f.read()
        
        # Expected output after decoding the bencoded data
        expected_output = {
            'announce': 'http://bittorrent-test-tracker.codecrafters.io/announce',
            'created by': 'mktorrent 1.14',
            'info': {
                'length': 92063,
                'name': 'sample.txt',
                'piece length': 32768,
                'pieces': bytes([0xe8, 0x76, 0xf6, 0x7a, 0x2a, 0x8e, 0x8b, 0xe8, 0xb3, 0x8b, 0x0a, 0x67, 0x26, 0xc3, 0x8f, 0x0e, 0xa1, 0x9b, 0x03, 0x02, 0x2d, 0x6e, 0x22, 0x75, 0xe6, 0x04, 0x20, 0x76, 0x66, 0x56, 0x73, 0x6e, 0x81, 0xff, 0x10, 0xb5, 0x52, 0x04, 0xad, 0x8d, 0x35, 0xf0, 0x0c, 0x9c, 0x7a, 0x02, 0x13, 0xdf, 0x19, 0x92, 0xbc, 0x8d, 0x09, 0x72, 0x27, 0xad, 0x9a, 0x90, 0x9a, 0x49, 0x17])
            }
        }

        # Call the function with the test data
        result = decode_bencode(bencoded_torrent_data)

        # Check if the result matches the expected output
        self.assertEqual(result, expected_output)
if __name__ == "__main__":
    unittest.main()
