import json
import sys

import hashlib
import bencodepy
import requests

import struct
import socket


def decode_bencode(bencoded_value):

    def extract_string(data):
         length, remain = data.split(b":", 1)
         length = int(length)
         return remain[:length], remain[length:]
    
    def decode(data):
        # Instance for string
        if chr(data[0]).isdigit():
            decoded, undecoded = extract_string(data)
            return decoded, undecoded
        # Instance for number
        elif data.startswith(b'i'):
            end = data.index(b'e')
            return int(data[1:end]), data[end + 1:]
        # Instance for list
        elif data.startswith(b'l'):
            data = data[1:] 
            lst = []
            while(not data.startswith(b'e')):
                elem, remain = decode(data)
                lst.append(elem)
                data = remain
            return lst, data[1:]
        # Instance for dictionary
        elif data.startswith(b'd'):
            data = data[1:]
            my_dict = {}
            while(not data.startswith(b'e')):
                key, data = decode(data) # Decode key
                value, data = decode(data) # Decode value
                my_dict[key.decode('utf-8')] = value    # Making sure that the key is in string-format
            return my_dict, data[1:]
        else:
            raise ValueError("Invalid bencoded data")
    
    decoded_value, _ = decode(bencoded_value)
    return decoded_value
        
def extract_torrent(file):
    with open(file, "rb") as torrent_file:
        torrent_content = torrent_file.read()
    torrent = decode_bencode(torrent_content)
    torrent_url = torrent["announce"].decode()
    torrent_piece_length = torrent["info"]["piece length"]
    torrent_piece_hashes = torrent["info"]["pieces"]
    torrent_length = torrent["info"]["length"]
    torrent_info_decoded = torrent["info"]

    
    torrent_info_encoded = bencodepy.encode(torrent_info_decoded)

    info_sha1 = hashlib.sha1(torrent_info_encoded).hexdigest()

    return torrent_url, torrent_length, info_sha1, torrent_piece_length, torrent_piece_hashes.hex()

def send_tracker_response(interval, peers):
    # Create a response dictionary
    response = {
        'interval': interval,  # The update interval in seconds
        'peers': peers,        # A list of peers or a compact representation
    }


def main():
    command = sys.argv[1]

    if command == "decode":
        bencoded_value = sys.argv[2].encode()
        def bytes_to_str(data):
            if isinstance(data, bytes):
                return data.decode()

            raise TypeError(f"Type not serializable: {type(data)}")

        print(json.dumps(decode_bencode(bencoded_value), default=bytes_to_str))
    elif command == "info":
        file_name = sys.argv[2]
        tracker_url, torrent_length, info_hex, piece_length, piece_hashes = extract_torrent(file_name)
        print("Tracker URL:", tracker_url)
        print("Length:", torrent_length)
        print("Info Hash:", info_hex)
        print("Piece Length:", piece_length)
        print("Piece Hashes", piece_hashes)
    elif command == "peers":
        file = sys.argv[2]
        with open(file, "rb") as torrent_file:
            torrent_content = torrent_file.read()
        torrent = decode_bencode(torrent_content)

        tracker_url = torrent["announce"]

        torrent_length = torrent["info"]["length"]
        info = torrent["info"]  
        torrent_info_encoded = bencodepy.encode(info)
        info_sha1 = hashlib.sha1(torrent_info_encoded).hexdigest()
        info_byte = bytes.fromhex(info_sha1)

        print("Tracker url:", tracker_url)
        print("Info Hash:", info_byte)
        print("Length:", torrent_length)

        query_params = {
            'info_hash': info_byte,
            'peer_id': '00112233445566778899',
            'port': 6881,
            'uploaded': 0,
            'downloaded': 0,
            'left': torrent_length,
            'compact': 1,
        }

        request = requests.get(tracker_url, params=query_params)

        raw_content = request.content

        raw_content_decoded = decode_bencode(raw_content)

        print("Raw content:", raw_content_decoded)

        

        


if __name__ == "__main__":
    main()
