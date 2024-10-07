import json
import sys

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
        # For example, {"hello": 52, "foo":"bar"} would be encoded as: d3:foo3:bar5:helloi52ee (note that the keys were reordered). d3:foo3:bar5:helloi52ee -> {"foo":"bar","hello":52}
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
    torrent_length = torrent["info"]["length"]
    torrent_info = decode_bencode(torrent["info"])

    return torrent_url, torrent_length


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
        tracker_url, torrent_length = extract_torrent(file_name)
        print("Tracker URL:", tracker_url)
        print("Length:", torrent_length)
        


if __name__ == "__main__":
    main()
