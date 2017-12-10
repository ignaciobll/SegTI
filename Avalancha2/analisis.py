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
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))


def gen_study_case():
    key = random_string(KEY_SIZE)
    iv = random_string(IV_SIZE)
    text = random_string(TEXT_SIZE)
    return (key, iv, text)


def flip_bit_in_string(s):
    b = bytearray(s)
    pos = random.SystemRandom().randint(0, len(b))  # character position
    index = random.SystemRandom().randint(0, 7)  # bit shift
    b[pos] = b[pos] ^ (1 << index)
    return bytes(b)


def analisis(size=STUDY_SIZE):
    histogram = [0] * 128
    for _ in range(size):
        (k, iv, text) = gen_study_case()
        r = c.cipher(k, iv, text)
        bintext = bytearray(text.encode('ascii'))
        h = hamming(bintext, r)
        histogram[h] += 1
    return histogram


a = analisis()
c.s.close()
