import random
import string
import client as c
import statistics as s
from scipy.stats import skew, kurtosis, binom

KEY_SIZE = 16
IV_SIZE = 8
TEXT_SIZE = 16

STUDY_SIZE = 500


def random_string(size=16):
    domain = string.ascii_letters + string.digits
    r = [random.SystemRandom().choice(domain) for _ in range(size)]
    return ''.join(r)


def hamming(s1, s2):
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


def do_analisis(size=STUDY_SIZE, debug=False):
    histogram = [[0] * 128, [0] * 128, [0] * 128]
    for _ in range(size):

        # Origin
        (k, iv, text) = gen_study_case()
        r = c.cipher(k, iv, text)
        sr = "".join("{0:08b}".format(x) for x in r)  # String response

        # Text flipped
        textf = flip_bit(text)
        rtf = c.cipher(k, iv, textf)  # Response text flipped
        srtf = "".join("{0:08b}".format(x) for x in rtf)

        h = hamming(sr, srtf)

        histogram[0][h] = histogram[0][h] + 1

        # Key flipped
        kf = flip_bit(k)
        rkf = c.cipher(kf, iv, text)
        srkf = "".join("{0:08b}".format(x) for x in rkf)

        h = hamming(sr, srkf)
        histogram[1][h] += 1

        # Inital Block Value
        vf = flip_bit(iv)
        rvf = c.cipher(k, vf, text)
        srvf = "".join("{0:08b}".format(x) for x in rvf)

        h = hamming(sr, srvf)
        histogram[2][h] += 1

    return histogram


############# STATISTICS #################### 


def gen_data(histogram):
    data = []
    for index, value in enumerate(histogram):
        for _ in range(value):
            data.append(index)
    return data


def do_statistics(histogram, latex=False):
    data = gen_data(histogram)

    emean, evar, eskew, ekurt = binom.stats(TEXT_SIZE*8, 0.5, moments='mvsk')
    estd = binom.std(TEXT_SIZE*8, 0.5)

    mean = s.mean(data)
    median = s.median(data)

    # We will use sample versions because we don't have all the population
    stdev = s.stdev(data)
    variance = s.variance(data)

    sk = skew(data)
    ku = kurtosis(data)

    mean_err = abs(emean - mean) / emean
    std_err = abs(estd - stdev) / estd
    var_err = abs(evar - variance) / evar
    kurt_err = abs(ekurt - ku) / ekurt

    print("Media:\t\t{}\t\t\t(Err) {}".format(mean, mean_err))
    print("Mediana:\t{}".format(median))
    print("Desv. Std.:\t{}\t(Err) {}".format(stdev, std_err))
    print("Varianza.:\t{}\t(Err) {}".format(variance, var_err))
    print("Simetría:\t{}".format(sk))
    print("Kurtosis:\t{}\t(Err) {}".format(ku, kurt_err))


if __name__ == "__main__":
    print("""
Encriptemos cositas :D

Los parámetros iniciales son:

- Tamaño de la clave:\t\t{}
- Tamaño de vector inicial:\t{}
- Tamaño de bloque:\t\t{}

- Tamaño de la muestra:\t{}
""".format(KEY_SIZE, IV_SIZE, TEXT_SIZE, STUDY_SIZE))

    histogram = do_analisis()
    print("Análisis estadístico sobre la variación del texto de entrada")
    do_statistics(histogram[0])

    print("Análisis estadístico sobre la variación de la clave")
    do_statistics(histogram[1])

    print("Análisis estadístico sobre la variación del vector inicial")
    do_statistics(histogram[2])

    c.s.close()
