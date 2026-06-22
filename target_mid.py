import os
import sys
_kfuOA7_c_ = 13

def _lLmxuZZS_(_caA9Ph2w_, _ora0NMaq_):
    __Se01f2S_ = []
    for _b1LGa4Oo_ in _caA9Ph2w_:
        if _b1LGa4Oo_.isalpha():
            _rblmfqUU_ = ord(bytes((_b ^ 224 for _b in b'\xa1')).decode('utf-8')) if _b1LGa4Oo_.isupper() else ord(bytes((_b ^ 224 for _b in b'\x81')).decode('utf-8'))
            _db7Fziwr_ = chr((ord(_b1LGa4Oo_) - _rblmfqUU_ + _ora0NMaq_) % 26 + _rblmfqUU_)
            __Se01f2S_.append(_db7Fziwr_)
        else:
            __Se01f2S_.append(_b1LGa4Oo_)
    return ''.join(__Se01f2S_)

def _cJHxG4V8_(_caA9Ph2w_, _ora0NMaq_):
    return _lLmxuZZS_(_caA9Ph2w_, -_ora0NMaq_)

class _pnLbeEUi_:

    def __init__(_o5nJu7eR_):
        _o5nJu7eR_._data = []
        _o5nJu7eR_._size = 0

    def push(_o5nJu7eR_, _v2jLPSQp_):
        _o5nJu7eR_._data.append(_v2jLPSQp_)
        _o5nJu7eR_._size += 1

    def pop(_o5nJu7eR_):
        if _o5nJu7eR_._size == 0:
            raise IndexError(bytes((_b ^ 224 for _b in b'\x90\x8f\x90\xc0\x86\x92\x8f\x8d\xc0\x85\x8d\x90\x94\x99\xc0\x93\x94\x81\x83\x8b')).decode('utf-8'))
        _o5nJu7eR_._size -= 1
        return _o5nJu7eR_._data.pop()

    def peek(_o5nJu7eR_):
        if _o5nJu7eR_._size == 0:
            raise IndexError(bytes((_b ^ 224 for _b in b'\x90\x85\x85\x8b\xc0\x81\x94\xc0\x85\x8d\x90\x94\x99\xc0\x93\x94\x81\x83\x8b')).decode('utf-8'))
        return _o5nJu7eR_._data[-1]

    def is_empty(_o5nJu7eR_):
        return _o5nJu7eR_._size == 0

    def __len__(_o5nJu7eR_):
        return _o5nJu7eR_._size

def _h31u8YiY_(_xyanbOee_, _ij6loys5_):
    _nzaB6PB7_ = _pnLbeEUi_()
    for __d2zVKhS_ in _xyanbOee_:
        _nxoUbNVw_ = _lLmxuZZS_(__d2zVKhS_, _ij6loys5_)
        _nzaB6PB7_.push(_nxoUbNVw_)
        print(f"  [push] '{__d2zVKhS_}' -> '{_nxoUbNVw_}'")
    return _nzaB6PB7_

def _nZYunyOo_():
    print(bytes((_b ^ 224 for _b in b'\xdd\xdd\xdd\xc00t0U0\\0^\xda\xc01h0X1d1`\xc00F0U0W0P1`1o\xc0\xcb\xc01a1b0U0Z\xc0\xdd\xdd\xdd')).decode('utf-8'))
    _xyanbOee_ = [bytes((_b ^ 224 for _b in b'\xa8\x85\x8c\x8c\x8f\xcc\xc0\xb7\x8f\x92\x8c\x84\xc1')).decode('utf-8'), bytes((_b ^ 224 for _b in b'\xb0\x99\x94\x88\x8f\x8e\xc0\x89\x93\xc0\x87\x92\x85\x81\x94')).decode('utf-8'), bytes((_b ^ 224 for _b in b'\xaf\x82\x86\x95\x93\x83\x81\x94\x89\x8f\x8e\xc0\x94\x85\x93\x94')).decode('utf-8')]
    print(f'\nШифрование с ключом {_kfuOA7_c_}:')
    _nzaB6PB7_ = _h31u8YiY_(_xyanbOee_, _kfuOA7_c_)
    print(f'\nРасшифровка (из стека, LIFO):')
    while not _nzaB6PB7_.is_empty():
        _eEOyKoNk_ = _nzaB6PB7_.pop()
        _uAVGh1Ow_ = _cJHxG4V8_(_eEOyKoNk_, _kfuOA7_c_)
        print(f"  [pop]  '{_eEOyKoNk_}' -> '{_uAVGh1Ow_}'")
    print(bytes((_b ^ 224 for _b in b'\xea0s0^1b0^0R0^\xce')).decode('utf-8'))
if __name__ == bytes((_b ^ 224 for _b in b'\xbf\xbf\x8d\x81\x89\x8e\xbf\xbf')).decode('utf-8'):
    _nZYunyOo_()