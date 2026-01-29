def write_bmp(_name:str = 'default', _width:int = 1920, _height:int = 1080, pixel_map:list = []) -> bool:
    try:
        with open(str(_name) + ".bmp", "wb") as bmp_file:
            string = '424D'
            size = _width*_height*4+54
            hsize = size.to_bytes(4,'little')
            string = bytearray.fromhex(string)
            for byte in hsize: string.append(byte)
            for byte in bytearray.fromhex('000000003600000028000000'): string.append(byte)
            for byte in int(_width).to_bytes(4,'little'): string.append(byte)
            for byte in int(_height).to_bytes(4,'little'): string.append(byte)
            for byte in bytearray.fromhex('0100180000000000'): string.append(byte)
            for byte in int(_width*_height*4).to_bytes(4,'little'): string.append(byte)
            for byte in bytearray.fromhex('130B0000'): string.append(byte)
            for byte in bytearray.fromhex('130B0000'): string.append(byte)
            for byte in bytearray.fromhex('00000000'): string.append(byte)
            for byte in bytearray.fromhex('00000000'): string.append(byte)
            count = 0
            for byte in string:
                bmp_file.write(byte.to_bytes())
            for x in reversed(pixel_map):
                for y in x:
                    y = y[1:]
                    new_y = y[4] + y[5] + y[2] + y[3] + y[0] +y[1]
                    for byte in bytearray.fromhex(new_y):
                        if len(byte.to_bytes()) != 1:
                            raise
                        bmp_file.write(byte.to_bytes())            
        return True
    except:
        return False