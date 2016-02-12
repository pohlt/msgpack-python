#!/usr/bin/env python
# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
import pytest

from msgpack import packb, unpackb, Packer, Unpacker, ExtType, PackException, PackOverflowError, PackValueError
from msgpack import UnpackValueError, UnpackException


@pytest.mark.parametrize("expected_exception", [OverflowError, ValueError, PackOverflowError,
                                                PackException, PackValueError])
def test_integer(expected_exception):
    x = -(2 ** 63)
    assert unpackb(packb(x)) == x
    with pytest.raises(expected_exception):
        packb(x-1)

    x = 2 ** 64 - 1
    assert unpackb(packb(x)) == x
    with pytest.raises(expected_exception):
        packb(x+1)


@pytest.mark.parametrize("expected_exception", [ValueError, PackException, PackValueError])
def test_array_header(expected_exception):
    packer = Packer()
    packer.pack_array_header(2**32-1)
    with pytest.raises(expected_exception):
        packer.pack_array_header(2**32)


@pytest.mark.parametrize("expected_exception", [ValueError, PackException, PackValueError])
def test_map_header(expected_exception):
    packer = Packer()
    packer.pack_map_header(2**32-1)
    with pytest.raises(expected_exception):
        packer.pack_array_header(2**32)


@pytest.mark.parametrize("expected_exception", [ValueError, UnpackValueError, UnpackException])
def test_max_str_len(expected_exception):
    d = 'x' * 3
    packed = packb(d)

    unpacker = Unpacker(max_str_len=3, encoding='utf-8')
    unpacker.feed(packed)
    assert unpacker.unpack() == d

    unpacker = Unpacker(max_str_len=2, encoding='utf-8')
    with pytest.raises(expected_exception):
        unpacker.feed(packed)
        unpacker.unpack()


@pytest.mark.parametrize("expected_exception", [ValueError, UnpackValueError, UnpackException])
def test_max_bin_len(expected_exception):
    d = b'x' * 3
    packed = packb(d, use_bin_type=True)

    unpacker = Unpacker(max_bin_len=3)
    unpacker.feed(packed)
    assert unpacker.unpack() == d

    unpacker = Unpacker(max_bin_len=2)
    with pytest.raises(expected_exception):
        unpacker.feed(packed)
        unpacker.unpack()


@pytest.mark.parametrize("expected_exception", [ValueError, UnpackValueError, UnpackException])
def test_max_array_len(expected_exception):
    d = [1,2,3]
    packed = packb(d)

    unpacker = Unpacker(max_array_len=3)
    unpacker.feed(packed)
    assert unpacker.unpack() == d

    unpacker = Unpacker(max_array_len=2)
    with pytest.raises(expected_exception):
        unpacker.feed(packed)
        unpacker.unpack()


@pytest.mark.parametrize("expected_exception", [ValueError, UnpackValueError, UnpackException])
def test_max_map_len(expected_exception):
    d = {1: 2, 3: 4, 5: 6}
    packed = packb(d)

    unpacker = Unpacker(max_map_len=3)
    unpacker.feed(packed)
    assert unpacker.unpack() == d

    unpacker = Unpacker(max_map_len=2)
    with pytest.raises(expected_exception):
        unpacker.feed(packed)
        unpacker.unpack()


@pytest.mark.parametrize("expected_exception", [ValueError, UnpackValueError, UnpackException])
def test_max_ext_len(expected_exception):
    d = ExtType(42, b"abc")
    packed = packb(d)

    unpacker = Unpacker(max_ext_len=3)
    unpacker.feed(packed)
    assert unpacker.unpack() == d

    unpacker = Unpacker(max_ext_len=2)
    with pytest.raises(expected_exception):
        unpacker.feed(packed)
        unpacker.unpack()



# PyPy fails following tests because of constant folding?
# https://bugs.pypy.org/issue1721
#@pytest.mark.skipif(True, reason="Requires very large memory.")
#def test_binary():
#    x = b'x' * (2**32 - 1)
#    assert unpackb(packb(x)) == x
#    del x
#    x = b'x' * (2**32)
#    with pytest.raises(ValueError):
#        packb(x)
#
#
#@pytest.mark.skipif(True, reason="Requires very large memory.")
#def test_string():
#    x = 'x' * (2**32 - 1)
#    assert unpackb(packb(x)) == x
#    x += 'y'
#    with pytest.raises(ValueError):
#        packb(x)
#
#
#@pytest.mark.skipif(True, reason="Requires very large memory.")
#def test_array():
#    x = [0] * (2**32 - 1)
#    assert unpackb(packb(x)) == x
#    x.append(0)
#    with pytest.raises(ValueError):
#        packb(x)
