# my_ubinascii.py

PAD = '='

# Base64 decoding table
table_a2b_base64 = [
  -1,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1,
  -1,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1,
  -1,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,62, -1,-1,-1,63,
  52,53,54,55, 56,57,58,59, 60,61,-1,-1, -1,-1,-1,-1, # Note PAD->-1 here
  -1, 0, 1, 2,  3, 4, 5, 6,  7, 8, 9,10, 11,12,13,14,
  15,16,17,18, 19,20,21,22, 23,24,25,-1, -1,-1,-1,-1,
  -1,26,27,28, 29,30,31,32, 33,34,35,36, 37,38,39,40,
  41,42,43,44, 45,46,47,48, 49,50,51,-1, -1,-1,-1,-1,
  -1,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1,
  -1,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1,
  -1,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1,
  -1,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1,
  -1,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1,
  -1,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1,
  -1,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1,
  -1,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1, -1,-1,-1,-1,    
]

table_a2b_base64 = ''.join(chr(n if n != -1 else 255) for n in table_a2b_base64)

# Base64 encoding table
table_b2a_base64 = (
  "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
)

# Hexlify function
def hexlify(data):
  return ''.join(f"{byte:02x}" for byte in data).encode('ascii')

# Unhexlify function
def unhexlify(data):
  if len(data) % 2 != 0:
    raise ValueError("Odd-length string")
  return bytes([int(data[i:i+2], 16) for i in range(0, len(data), 2)])

# Base64 decode function
def a2b_base64(ascii_data):
  res = []
  quad_pos = 0
  leftchar = 0
  leftbits = 0
  last_char_was_a_pad = False

  for c in ascii_data:
    if c == ord(PAD):
      if quad_pos > 2 or (quad_pos == 2 and last_char_was_a_pad):
        break
      last_char_was_a_pad = True
    else:
      n = ord(table_a2b_base64[ord(c)])
      if n == 255:
        continue
      quad_pos = (quad_pos + 1) & 3
      leftchar = (leftchar << 6) | n
      leftbits += 6

      if leftbits >= 8:
        leftbits -= 8
        res.append((leftchar >> leftbits).to_bytes(1, 'big'))
        leftchar &= ((1 << leftbits) - 1)

      last_char_was_a_pad = False
  else:
    if leftbits != 0:
      raise ValueError("Incorrect padding")

  return b''.join(res)

# Base64 encode function
def b2a_base64(bin_data):
  newlength = (len(bin_data) + 2) // 3
  newlength = newlength * 4 + 1
  res = []

  leftchar = 0
  leftbits = 0
  for c in bin_data:
    leftchar = (leftchar << 8) | c
    leftbits += 8
    res.append(table_b2a_base64[(leftchar >> (leftbits-6)) & 0x3f])
    leftbits -= 6
    if leftbits >= 6:
      res.append(table_b2a_base64[(leftchar >> (leftbits-6)) & 0x3f])
      leftbits -= 6

  if leftbits == 2:
    res.append(table_b2a_base64[(leftchar & 3) << 4])
    res.append(PAD)
    res.append(PAD)
  elif leftbits == 4:
    res.append(table_b2a_base64[(leftchar & 0xf) << 2])
    res.append(PAD)
  res.append('\n')
  return ''.join(res).encode('ascii')
