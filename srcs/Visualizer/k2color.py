from math import sin, pi

def N_Linar(k_seq:list[float])->list[int]:
    kmax = max(k_seq)
    kmin = min(k_seq)
    color_seq = []
    for k in k_seq:
        _k = (k-kmin)/(kmax-kmin)
        g = int(255*_k)
        r = 255-g
        color_seq.append(hex(r*0x10000+g*0x100))
    return color_seq

def N_Square(k_seq:list[float])->list[int]:
    kmax = max(k_seq)
    kmin = min(k_seq)
    color_seq = []
    for k in k_seq:
        _k = (k-kmin)/(kmax-kmin)
        _k = (2-_k)*_k
        g = int(255*_k)
        r = 255-g
        color_seq.append(hex(r*0x10000+g*0x100))
    return color_seq

def N_Sin(k_seq:list[float])->list[int]:
    kmax = max(k_seq)
    kmin = min(k_seq)
    color_seq = []
    for k in k_seq:
        _k = (k-kmin)/(kmax-kmin)
        _k = sin(_k*pi)
        g = int(255*_k)
        r = 255-g
        color_seq.append(hex(r*0x10000+g*0x100))
    return color_seq

def N_R_RELU(k_seq:list[float])->list[int]:
    kmax = max(k_seq)
    kmin = min(k_seq)
    color_seq = []
    for k in k_seq:
        _k = (k-kmin)/(kmax-kmin)
        _k = _k*2 if _k < 0.5 else 1
        g = int(255*_k)
        r = 255-g
        color_seq.append(hex(r*0x10000+g*0x100))
    return color_seq

N_dict = {"Linar":N_Linar,
        "Square":N_Square,
        "Sin":N_Sin,
        "R_RELU":N_R_RELU
        }

def A_Next(k_seq:list[float])->list[float]:
    ret = []
    length = len(k_seq)
    for i in range(length-1):
        _k = (k_seq[i]+k_seq[i+1])/2
        ret.append(_k)
    ret.append(k_seq[length-1])
    return ret

def A_Prev(k_seq:list[float])->list[float]:
    ret = []
    length = len(k_seq)
    ret.append(k_seq[0])
    for i in range(1,length):
        _k = (k_seq[i]+k_seq[i-1])/2
        ret.append(_k)
    return ret

def A_Side(k_seq:list[float])->list[float]:
    ret = []
    length = len(k_seq)
    ret.append((k_seq[0]+k_seq[1])/2)
    for i in range(1,length-1):
        _k = (k_seq[i-1]+k_seq[i]+k_seq[i+1])/3
        ret.append(_k)
    ret.append((k_seq[length-2]+k_seq[length-1])/2)
    return ret

A_dict = {"Next":A_Next,
        "Prev":A_Prev,
        "Side":A_Side
        }

def normalizer(k_seq:list[float], normalize_method:str, average_method:str)->list[int]:
    return N_dict[normalize_method](A_dict[average_method](k_seq))