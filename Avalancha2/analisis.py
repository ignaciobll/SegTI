import random
import string
import client as c

KEY_SIZE = 16
IV_SIZE = 8
TEXT_SIZE = 16

STUDY_SIZE = 10


def random_string(size=16):
    domain = string.ascii_letters + string.digits
    r = [random.SystemRandom().choice(domain) for _ in range(size)]
    return ''.join(r)


def hamming(s1, s2):
    print("{}\n{}".format(s1,s2))
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))


def gen_study_case():
    key = random_string(KEY_SIZE).encode('ascii')
    iv = random_string(IV_SIZE).encode('ascii')
    text = random_string(TEXT_SIZE).encode('ascii')
    return (key, iv, text)


def flip_bit(bytestring):
    b = bytearray(bytestring)
    pos = random.SystemRandom().randint(0, len(b) - 1)  # character position
    index = random.SystemRandom().randint(0, 7)  # bit shift
    b[pos] = b[pos] ^ (1 << index)
    return bytes(b)

def do_analisis(size=STUDY_SIZE):
    histogram = [[0] * 128, [0] * 128, [0] * 128]
    for _ in range(size):
        print("###\t{}\t{}\t{}\t###".format(histogram[0][1], histogram[1][1], histogram[2][1]))
        # Origin
        (k, iv, text) = gen_study_case()
        r = c.cipher(k, iv, text)
        sr = "".join("{0:08b}".format(x) for x in r)  # String response

        # Text flipped
        textf = flip_bit(text)
        rtf = c.cipher(k, iv, textf)  # Response text flipped
        srtf = "".join("{0:08b}".format(x) for x in rtf)

        h = hamming(sr,srtf)
        print("Hamming srtf: {}".format(h))
        histogram[0][h] = histogram[0][h] + 1

        # Key flipped
        kf = flip_bit(k)
        rkf = c.cipher(kf, iv, text)
        srkf = "".join("{0:08b}".format(x) for x in rkf)

        h = hamming(sr,srkf)
        print("Hamming srkf: {}".format(h))
        histogram[1][h] += 1

        # Inital Block Value
        vf = flip_bit(iv)
        rvf = c.cipher(k, vf, text)
        srvf = "".join("{0:08b}".format(x) for x in rvf)

        h = hamming(sr,srvf)
        print("Hamming srvf: {}".format(h))
        histogram[2][h] += 1

        print("===\t{}\t{}\t{}\t===".format(histogram[0][1], histogram[1][1], histogram[2][1]))
    return histogram
