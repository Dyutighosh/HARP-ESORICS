





















from warnings import warn
from pathlib import Path


import numpy as np
np.import_array()


from numbers import Number, Real


from cython.operator cimport dereference as deref


cimport cython


FLOAT_T = (float, np.float16, np.float32, np.float64)
INT_T =   (int, np.int16, np.int32, np.int64, np.int_, np.intc)


from Pyfhel.utils import _to_valid_file_str
include "utils/cy_utils.pxi"
include "utils/cy_type_converters.pxi"


cdef class Pyfhel:

    def __cinit__(self,
                  context_params=None,
                  key_gen=False,
                  pub_key_file=None,
                  sec_key_file=None):
        self.afseal = new Afseal()
        self._qi_sizes = []
        self._scale = 1
        self._sec = 128

    def __init__(self,
                  context_params=None,
                  key_gen=False,
                  pub_key_file=None,
                  sec_key_file=None):

        if context_params is not None:
            if isinstance(context_params, dict):
                self.contextGen(**context_params)
            elif isinstance(context_params, (str, Path)):
                self.load_context(context_params)
            else:
                raise TypeError("context_params must be a dictionary or a string")
        if key_gen:
            self.keyGen()
        else:
            if pub_key_file is not None:
                self.load_public_key(pub_key_file)
            if sec_key_file is not None:
                self.load_secret_key(sec_key_file)

    def __dealloc__(self):
        if self.afseal != NULL:
            del self.afseal

    def __repr__(self):

        return "<{} Pyfhel obj at {}, [pk:{}, sk:{}, rtk:{}, rlk:{}, contx({})]>".format(
                self.scheme.name,
                hex(id(self)),
                "-" if self.is_public_key_empty() else "Y",
                "-" if self.is_secret_key_empty() else "Y",
                "-" if self.is_rotate_key_empty() else "Y",
                "-" if self.is_relin_key_empty() else f"Y",
                "-" if self.is_context_empty() else                        f"n={self.n}, "                        f"t={self.t}, "                        f"sec={self.sec}, "                        f"qi={self.qi_sizes}, "                        f"scale={self.scale}, ")

    def __reduce__(self):

        context_params={"scheme": self.scheme.name,
                        "n": self.n,
                        "t": self.t,
                        "sec": self.sec,
                        "scale": self.scale,
                        "qi": self.qi,}
        return (Pyfhel, (context_params, False, None, None))

    @property
    def t(self):

        return self.get_plain_modulus()

    @property
    def n(self):

        return self.get_poly_modulus_degree()

    @property
    def sec(self):

        return (<Afseal*>self.afseal).get_sec()

    @property
    def qi(self):

        return self.get_qi()

    @property
    def qi_sizes(self):

        return self._qi_sizes

    @property
    def scale(self):

        return self._scale
    @scale.setter
    def scale(self, value):
        if not isinstance(value, Real) or value < 0:
            raise ValueError("scale must be a real number")
        self._scale = value

    @property
    def scheme(self):

        return Scheme_t(self.afseal.get_scheme())

    @property
    def total_coeff_modulus_bit_count(self):

        return (<Afseal*>self.afseal).total_coeff_modulus_bit_count()





    cpdef string contextGen(self,
        str scheme, int n, int t_bits=0, int64_t t=0,
        int sec=128,double scale=1, int scale_bits=0,
        vector[int] qi_sizes = {}, vector[uint64_t] qi = {}):

        s = to_Scheme_t(scheme)
        assert sec in {0, 128, 192, 256},                "Pyfhel schemes require `sec` to be 0 (unset), 128, 192 or 256"
        if s==Scheme_t.bfv or s==Scheme_t.bgv:
            assert (t_bits>0 or t>0),                "BFV|BGV scheme requires plain_modulus (`t_bits` or `t`) to be set"
            assert (sec>0) or (not qi_sizes.empty()) or (not qi.empty()),                "BFV|BGV scheme requires `sec` or `qi` to be set."
            if (sec>0):
                qi_sizes.clear()
            self._scale = 1
        elif s==Scheme_t.ckks:
            assert (not qi_sizes.empty()) or (not qi.empty()),                "CKKS scheme requires a list of prime sizes (qi_sizes) or primes (qi) to be set"
            if not scale>1 and not scale_bits>0:
                warn("<Pyfhel Warning> initializing CKKS context without default scale."
                     "You will have to provide a scale for each encoding", RuntimeWarning)
            self._scale = 2**scale_bits if scale_bits>0 else scale
            if not qi_sizes.empty():
                available_rescalings = np.cumsum(np.triu(np.tile(qi_sizes, (len(qi_sizes), 1)), k=1), axis=1)
                if <int>np.log2(self._scale) not in available_rescalings:
                    warn("<Pyfhel Warning> qi_sizes {} do not support rescaling for scale {}.".format(qi_sizes, self._scale))
        self._sec = sec
        self._qi_sizes = qi_sizes if not qi_sizes.empty() else                         [<int>round(np.log2(_qi)) for _qi in qi] if not qi.empty() else {}
        return self.afseal.ContextGen(<scheme_t>s.value, n, t_bits, t, sec, qi_sizes, qi)

    cpdef void keyGen(self):

        self.afseal.KeyGen()

    cpdef void rotateKeyGen(self, vector[int] rot_steps ={}):

        self.afseal.rotateKeyGen(rot_steps)

    cpdef void relinKeyGen(self):

        self.afseal.relinKeyGen()



    cpdef PyCtxt encryptInt(self, int64_t[:] arr, PyCtxt ctxt=None):

        if ctxt is None:
            ctxt = PyCtxt(pyfhel=self)
        cdef vector[int64_t] vec
        cdef AfsealPtxt ptxt
        vec.assign(&arr[0], &arr[0]+<Py_ssize_t>arr.size)
        self.afseal.encode_i(vec, ptxt)
        self.afseal.encrypt(ptxt, deref(ctxt._ptr_ctxt))
        ctxt._scheme = scheme_t.bfv
        ctxt._pyfhel = self
        return ctxt

    cpdef PyCtxt encryptFrac(self,
        double[:] arr, PyCtxt ctxt=None,
        double scale=0, int scale_bits=0):

        scale = _get_valid_scale(scale_bits, scale, self._scale)
        if ctxt is None:
            ctxt = PyCtxt(pyfhel=self)
        cdef vector[double] vec
        vec.assign(&arr[0], &arr[0] + <Py_ssize_t>arr.size)
        cdef AfsealPtxt ptxt
        self.afseal.encode_f(vec, scale, ptxt)
        self.afseal.encrypt(ptxt, deref(ctxt._ptr_ctxt))
        ctxt._scheme = scheme_t.ckks
        ctxt._pyfhel = self
        return ctxt


    cpdef PyCtxt encryptComplex(
        self, complex[:] arr, PyCtxt ctxt=None,
        double scale=0, int scale_bits=0):

        scale = _get_valid_scale(scale_bits, scale, self._scale)
        if ctxt is None:
            ctxt = PyCtxt(pyfhel=self)
        cdef vector[cy_complex] vec
        vec.assign(&arr[0], &arr[0] + <Py_ssize_t>arr.size)
        cdef AfsealPtxt ptxt
        self.afseal.encode_c(vec, scale, ptxt)
        self.afseal.encrypt(ptxt, deref(ctxt._ptr_ctxt))
        ctxt._scheme = scheme_t.ckks
        ctxt._pyfhel = self
        return ctxt


    cpdef PyCtxt encryptPtxt(self, PyPtxt ptxt, PyCtxt ctxt=None):

        if (ptxt._ptr_ptxt == NULL or ptxt is None):
            raise TypeError("<Pyfhel ERROR> PyPtxt Plaintext is empty")
        if ctxt is None:
            ctxt = PyCtxt(pyfhel=self)
        self.afseal.encrypt(deref(ptxt._ptr_ptxt), deref(ctxt._ptr_ctxt))
        ctxt._scheme = ptxt._scheme
        ctxt._pyfhel = self
        return ctxt

    cpdef PyCtxt encryptBGV(self, int64_t[:] arr, PyCtxt ctxt=None):

        if ctxt is None:
            ctxt = PyCtxt(pyfhel=self)
        cdef vector[int64_t] vec
        cdef AfsealPtxt ptxt
        vec.assign(&arr[0], &arr[0]+<Py_ssize_t>arr.size)
        self.afseal.encode_g(vec, ptxt)
        self.afseal.encrypt(ptxt, deref(ctxt._ptr_ctxt))
        ctxt._scheme = scheme_t.bgv
        ctxt._pyfhel = self
        return ctxt



    cpdef np.ndarray[object, ndim=1] encryptAInt(self, int64_t[:,::1] arr):
        raise NotImplementedError("<Pyfhel ERROR> encryptAInt not implemented")

    cpdef np.ndarray[object, ndim=1] encryptAFrac(self, double[:,::1] arr, double scale=0, int scale_bits=0):
        raise NotImplementedError("<Pyfhel ERROR> encryptAFrac not implemented")

    cpdef np.ndarray[object, ndim=1] encryptAComplex(self, complex[:,::1] arr, double scale=0, int scale_bits=0):
        raise NotImplementedError("<Pyfhel ERROR> encryptAComplex not implemented")

    cpdef np.ndarray[object, ndim=1] encryptAPtxt(self, PyPtxt[:] ptxt):
        raise NotImplementedError("<Pyfhel ERROR> encryptAPtxt not implemented")

    cpdef np.ndarray[object, ndim=1] encryptABGV(self, int64_t[:,::1] arr):
        raise NotImplementedError("<Pyfhel ERROR> encryptABGV not implemented")

    def encrypt(self, ptxt not None, PyCtxt ctxt=None, scale=None):


        if isinstance(ptxt, (np.ndarray, np.number, Number, list)):
            ptxt = self.encode(ptxt, scale=self.scale if scale is None else scale)


        if isinstance(ptxt, PyPtxt):
            return self.encryptPtxt(ptxt, ctxt)

        raise TypeError('<Pyfhel ERROR> Plaintext type ['+str(type(ptxt))+
                        '] not supported for encryption')


    cpdef np.ndarray[int64_t, ndim=1] decryptInt(self, PyCtxt ctxt):

        if (ctxt._scheme != scheme_t.bfv):
            raise RuntimeError("<Pyfhel ERROR> wrong scheme type in PyCtxt")
        cdef vector[int64_t] vec
        cdef AfsealPtxt ptxt
        self.afseal.decrypt(deref(ctxt._ptr_ctxt), ptxt)
        self.afseal.decode_i(ptxt, vec)
        return np.asarray(<list>vec)

    cpdef np.ndarray[double, ndim=1] decryptFrac(self, PyCtxt ctxt):

        if (ctxt._scheme != scheme_t.ckks):
            raise RuntimeError("<Pyfhel ERROR> wrong scheme type in PyCtxt")
        cdef vector[double] vec
        cdef AfsealPtxt ptxt
        self.afseal.decrypt(deref(ctxt._ptr_ctxt), ptxt)
        self.afseal.decode_f(ptxt, vec)
        return np.asarray(<list>vec)

    cpdef np.ndarray[complex, ndim=1] decryptComplex(self, PyCtxt ctxt):

        if (ctxt._scheme != scheme_t.ckks):
            raise RuntimeError("<Pyfhel ERROR> wrong scheme type in PyCtxt")
        cdef vector[cy_complex] vec
        cdef AfsealPtxt ptxt
        self.afseal.decrypt(deref(ctxt._ptr_ctxt), ptxt)
        self.afseal.decode_c(ptxt, vec)
        return np.asarray(<list>vec)

    cpdef PyPtxt decryptPtxt(self, PyCtxt ctxt, PyPtxt ptxt=None):

        if ptxt is None:
            ptxt = PyPtxt(pyfhel=self)
        self.afseal.decrypt(deref(ctxt._ptr_ctxt), deref(ptxt._ptr_ptxt))
        ptxt._scheme = ctxt._scheme
        return ptxt

    cpdef np.ndarray[int64_t, ndim=1] decryptBGV(self, PyCtxt ctxt):

        if (ctxt._scheme != scheme_t.bgv):
            raise RuntimeError("<Pyfhel ERROR> wrong scheme type in PyCtxt")
        cdef vector[int64_t] vec
        cdef AfsealPtxt ptxt
        self.afseal.decrypt(deref(ctxt._ptr_ctxt), ptxt)
        self.afseal.decode_g(ptxt, vec)
        return np.asarray(<list>vec)



    cpdef np.ndarray[int64_t, ndim=2] decryptAInt(self, PyCtxt ctxt):
        raise NotImplementedError("<Pyfhel ERROR> decryptAInt not implemented")
    cpdef np.ndarray[double, ndim=2] decryptAFrac(self, PyCtxt ctxt):
        raise NotImplementedError("<Pyfhel ERROR> decryptAFrac not implemented")
    cpdef np.ndarray[double, ndim=2] decryptAComplex(self, PyCtxt ctxt):
        raise NotImplementedError("<Pyfhel ERROR> decryptAComplex not implemented")
    cpdef np.ndarray[object, ndim=1] decryptAPtxt(self, PyCtxt ctxt):
        raise NotImplementedError("<Pyfhel ERROR> decryptAPtxt not implemented")
    cpdef np.ndarray[int64_t, ndim=2] decryptABGV(self, PyCtxt ctxt):
        raise NotImplementedError("<Pyfhel ERROR> decryptABGV not implemented")
    def decrypt(self, PyCtxt ctxt, bool decode=True, PyPtxt ptxt=None):

        if (decode):
            if (ctxt._scheme == scheme_t.ckks):
                return self.decryptFrac(ctxt)
            elif (ctxt._scheme == scheme_t.bfv):
                return self.decryptInt(ctxt)
            elif (ctxt._scheme == scheme_t.bgv):
                return self.decryptBGV(ctxt)
            else:
                raise RuntimeError("<Pyfhel ERROR> wrong scheme type in PyCtxt when decrypting")
        else:
            if ptxt is None:
                ptxt = PyPtxt(pyfhel=self)
            return self.decryptPtxt(ctxt, ptxt)



    cpdef int noise_level(self, PyCtxt ctxt):

        if self.scheme != Scheme_t.bfv:
            raise RuntimeError("<Pyfhel ERROR> only bfv scheme supports noise level")
        return self.afseal.noise_level(deref(ctxt._ptr_ctxt))

    cpdef void relinearize(self, PyCtxt ctxt):

        if self.is_relin_key_empty():
            warn("<Pyfhel Warning> relin_key empty, generating it for relinearization.", RuntimeWarning)
            self.relinKeyGen()
        self.afseal.relinearize(deref(ctxt._ptr_ctxt))





    cpdef PyPtxt encodeInt(self, int64_t[::1] arr, PyPtxt ptxt=None):

        if ptxt is None:
            ptxt = PyPtxt(pyfhel=self)
        cdef vector[int64_t] vec
        vec.assign(&arr[0], &arr[0]+<Py_ssize_t>arr.size)
        self.afseal.encode_i(vec, deref(ptxt._ptr_ptxt))
        ptxt._scheme = scheme_t.bfv
        return ptxt

    cpdef PyPtxt encodeFrac(self, double[::1] arr, PyPtxt ptxt=None,
        double scale=0, int scale_bits=0) :

        scale = _get_valid_scale(scale_bits, scale, self._scale)
        if ptxt is None:
            ptxt = PyPtxt(pyfhel=self)
        cdef vector[double] vec
        vec.assign(&arr[0], &arr[0]+<Py_ssize_t>arr.size)
        self.afseal.encode_f(vec, scale, deref(ptxt._ptr_ptxt))
        ptxt._scheme = scheme_t.ckks
        ptxt._pyfhel = self
        return ptxt

    cpdef PyPtxt encodeComplex(
        self, complex[::1] arr, PyPtxt ptxt=None,
        double scale=0, int scale_bits=0):

        scale = _get_valid_scale(scale_bits, scale, self._scale)
        if ptxt is None:
            ptxt = PyPtxt(pyfhel=self)
        cdef vector[cy_complex] vec
        vec.assign(&arr[0], &arr[0]+<Py_ssize_t>arr.size)
        self.afseal.encode_c(vec, scale, deref(ptxt._ptr_ptxt))
        ptxt._scheme = scheme_t.ckks
        ptxt._pyfhel = self
        return ptxt

    cpdef PyPtxt encodeBGV(self, int64_t[::1] arr, PyPtxt ptxt=None):

        if ptxt is None:
            ptxt = PyPtxt(pyfhel=self)
        cdef vector[int64_t] vec
        vec.assign(&arr[0], &arr[0]+<Py_ssize_t>arr.size)
        self.afseal.encode_g(vec, deref(ptxt._ptr_ptxt))
        ptxt._scheme = scheme_t.bgv
        return ptxt


    cpdef np.ndarray[object, ndim=1] encodeAInt(self, int64_t[:,::1] arr):
        raise NotImplementedError("<Pyfhel ERROR> encodeAInt not implemented")

    cpdef np.ndarray[object, ndim=1] encodeAFrac(self, double[:,::1] arr, double scale=0, int scale_bits=0):
        raise NotImplementedError("<Pyfhel ERROR> encodeAFrac not implemented")

    cpdef np.ndarray[object, ndim=1] encodeAComplex(self, complex[:,::1] arr, double scale=0, int scale_bits=0):
        raise NotImplementedError("<Pyfhel ERROR> encodeAComplex not implemented")

    cpdef np.ndarray[object, ndim=1] encodeABGV(self, int64_t[:,::1] arr):
        raise NotImplementedError("<Pyfhel ERROR> encodeABGV not implemented")

    def encode(self, val_vec not None, double scale=0, int scale_bits=0, PyPtxt ptxt=None):

        val_vec = np.array(val_vec)
        if (val_vec.ndim==0):
            val_vec = np.repeat(val_vec, self.n // (1 + (self.scheme==Scheme_t.ckks)))
        if (val_vec.ndim > 2) or            (not np.issubdtype(val_vec.dtype, np.number)):
            raise TypeError('<Pyfhel ERROR> Plaintext numpy array is not '
                            '1D vector of numeric values, cannot encrypt.')
        elif val_vec.ndim == 1:
            if self.scheme == Scheme_t.bfv:
                return self.encodeInt(val_vec.astype(np.int64), ptxt)
            elif self.scheme == Scheme_t.bgv:
                return self.encodeBGV(val_vec.astype(np.int64), ptxt)
            elif self.scheme == Scheme_t.ckks:
                scale = _get_valid_scale(scale_bits, scale, self._scale)
                if np.issubdtype(val_vec.dtype, np.complexfloating):
                    return self.encodeComplex(val_vec.astype(complex), ptxt, scale)
                else:
                    return self.encodeFrac(val_vec.astype(np.float64), ptxt, scale)
        elif val_vec.ndim == 2:
            if self.scheme == Scheme_t.bfv:
                return self.encryptAInt(val_vec.astype(np.int64))
            elif self.scheme == Scheme_t.ckks:
                scale = _get_valid_scale(scale_bits, scale, self._scale)
                if np.issubdtype(val_vec.dtype, np.complexfloating):
                    return self.encryptAComplex(val_vec.astype(complex), scale)
                else:
                    return self.encryptAFrac(val_vec.astype(np.float64), scale)
        raise TypeError('<Pyfhel ERROR> Plaintext could not be encoded')


    cpdef np.ndarray[int64_t, ndim=1] decodeInt(self, PyPtxt ptxt):

        if ptxt._scheme != scheme_t.bfv:
            raise RuntimeError('<Pyfhel ERROR> PyPtxt scheme must be bfv')
        cdef vector[int64_t] output_vector
        self.afseal.decode_i(deref(ptxt._ptr_ptxt), output_vector)
        return vec_to_array_i(output_vector)

    cpdef np.ndarray[double, ndim=1] decodeFrac(self, PyPtxt ptxt):

        if ptxt._scheme != scheme_t.ckks:
            raise RuntimeError('<Pyfhel ERROR> PyPtxt scheme must be ckks')
        cdef vector[double] output_vector
        self.afseal.decode_f(deref(ptxt._ptr_ptxt), output_vector)
        return vec_to_array_f(output_vector)


    cpdef np.ndarray[complex, ndim=1] decodeComplex(self, PyPtxt ptxt):

        if ptxt._scheme != scheme_t.ckks:
            raise RuntimeError('<Pyfhel ERROR> PyPtxt scheme must be ckks')
        cdef vector[cy_complex] output_vector
        self.afseal.decode_c(deref(ptxt._ptr_ptxt), output_vector)
        return np.asarray(output_vector)

    cpdef np.ndarray[int64_t, ndim=1] decodeBGV(self, PyPtxt ptxt):

        if ptxt._scheme != scheme_t.bgv:
            raise RuntimeError('<Pyfhel ERROR> PyPtxt scheme must be bgv')
        cdef vector[int64_t] output_vector
        self.afseal.decode_g(deref(ptxt._ptr_ptxt), output_vector)
        return vec_to_array_i(output_vector)

    cpdef np.ndarray[int64_t, ndim=2] decodeAInt(self, PyPtxt[:] ptxt):
        raise NotImplementedError("<Pyfhel ERROR> decodeAInt not implemented")

    cpdef np.ndarray[double, ndim=2] decodeAFrac(self, PyPtxt[:] ptxt):
        raise NotImplementedError("<Pyfhel ERROR> decodeAFrac not implemented")

    cpdef np.ndarray[complex, ndim=2] decodeAComplex(self, PyPtxt[:] ptxt):
        raise NotImplementedError("<Pyfhel ERROR> decodeAComplex not implemented")

    cpdef np.ndarray[int64_t, ndim=2] decodeABGV(self, PyPtxt[:] ptxt):
        raise NotImplementedError("<Pyfhel ERROR> decodeABGV not implemented")

    def decode(self, PyPtxt ptxt):

        if (ptxt._scheme == scheme_t.ckks):
            return self.decodeFrac(ptxt)
        elif (ptxt._scheme == scheme_t.bgv):
            return self.decodeBGV(ptxt)
        elif (ptxt._scheme == scheme_t.bfv):
            return self.decodeInt(ptxt)
        else:
            raise RuntimeError("<Pyfhel ERROR> wrong scheme in PyPtxt. Cannot decode")





    cpdef PyCtxt square(self, PyCtxt ctxt, bool in_new_ctxt=False):

        if (in_new_ctxt):
            ctxt = PyCtxt(ctxt)
        self.afseal.square(deref(ctxt._ptr_ctxt))
        ctxt.mod_level += 1
        return ctxt

    cpdef PyCtxt negate(self, PyCtxt ctxt, bool in_new_ctxt=False):

        if (in_new_ctxt):
            new_ctxt = PyCtxt(ctxt)
            self.afseal.negate(deref(new_ctxt._ptr_ctxt))
            return new_ctxt
        else:
            self.afseal.negate(deref(ctxt._ptr_ctxt))
            return ctxt


    cpdef PyCtxt add(self, PyCtxt ctxt, PyCtxt ctxt_other, bool in_new_ctxt=False):

        if (ctxt._scheme != ctxt_other._scheme):
            raise RuntimeError(f"<Pyfhel ERROR> scheme type mistmatch in add terms"
                                " ({ctxt._scheme} VS {ctxt_other._scheme})")
        if (in_new_ctxt):
            ctxt = PyCtxt(copy_ctxt=ctxt)
        self.afseal.add(deref(ctxt._ptr_ctxt), deref(ctxt_other._ptr_ctxt))
        return ctxt

    cpdef PyCtxt add_plain(self, PyCtxt ctxt, PyPtxt ptxt, bool in_new_ctxt=False):

        if (ctxt._scheme != ptxt._scheme):
            raise RuntimeError("<Pyfhel ERROR> scheme type mistmatch in add terms"
                                " ({ctxt._scheme} VS {ptxt._scheme})")
        if (in_new_ctxt):
            ctxt = PyCtxt(copy_ctxt=ctxt)
        self.afseal.add_plain(deref(ctxt._ptr_ctxt), deref(ptxt._ptr_ptxt))
        return ctxt

    cpdef PyCtxt cumul_add(self, PyCtxt ctxt, bool in_new_ctxt=False, size_t n_elements=0):

        if self.is_rotate_key_empty():
            warn("<Pyfhel Warning> rot_key empty, initializing it for rotation.", RuntimeWarning)
            self.rotateKeyGen()


        cdef size_t n_slots = self.get_nSlots()
        if (n_elements == 0):
            n_elements = n_slots
        elif (n_elements > n_slots):
            raise RuntimeError(f"<Pyfhel ERROR> n_elements ({n_elements}) > nSlots ({n_slots})")


        if (in_new_ctxt):
            ctxt = PyCtxt(copy_ctxt=ctxt)


        aux = PyCtxt(copy_ctxt=ctxt)


        if self.scheme == Scheme_t.bfv and (n_elements > n_slots // 2):
            self.afseal.flip(deref(ctxt._ptr_ctxt))
            self.afseal.add(deref(ctxt._ptr_ctxt), deref(aux._ptr_ctxt))
            n_elements = n_slots // 2
            aux._ptr_ctxt = make_shared[AfsealCtxt](deref(dyn_cast[AfsealCtxt,AfCtxt](ctxt._ptr_ctxt)))


        cdef int k = 1
        while (k < n_elements):
            self.afseal.rotate(deref(ctxt._ptr_ctxt), -k)
            self.afseal.add(deref(ctxt._ptr_ctxt), deref(aux._ptr_ctxt))
            aux._ptr_ctxt = make_shared[AfsealCtxt](deref(dyn_cast[AfsealCtxt,AfCtxt](ctxt._ptr_ctxt)))
            k *= 2
        return ctxt


    cpdef PyCtxt sub(self, PyCtxt ctxt, PyCtxt ctxt_other, bool in_new_ctxt=False):

        if (ctxt._scheme != ctxt_other._scheme):
            raise RuntimeError("<Pyfhel ERROR> scheme type mistmatch in sub terms"
                                " ({ctxt._scheme} VS {ctxt_other._scheme})")
        if (in_new_ctxt):
            new_ctxt = PyCtxt(ctxt)
            self.afseal.sub(deref(new_ctxt._ptr_ctxt), deref(ctxt_other._ptr_ctxt))
            return new_ctxt
        else:
            self.afseal.sub(deref(ctxt._ptr_ctxt), deref(ctxt_other._ptr_ctxt))
            return ctxt

    cpdef PyCtxt sub_plain (self, PyCtxt ctxt, PyPtxt ptxt, bool in_new_ctxt=False):

        if (ctxt._scheme != ptxt._scheme):
            raise RuntimeError("<Pyfhel ERROR> scheme type mistmatch in sub terms"
                                " ({ctxt._scheme} VS {ptxt._scheme})")

        if (in_new_ctxt):
            ctxt = PyCtxt(ctxt)
        self.afseal.sub_plain(deref(ctxt._ptr_ctxt), deref(ptxt._ptr_ptxt))
        return ctxt


    cpdef PyCtxt multiply (self, PyCtxt ctxt, PyCtxt ctxt_other, bool in_new_ctxt=False):

        if (ctxt._scheme != ctxt_other._scheme):
            raise RuntimeError("<Pyfhel ERROR> scheme type mistmatch in mult terms"
                                " ({ctxt._scheme} VS {ctxt_other._scheme})")

        if (in_new_ctxt):
            new_ctxt = PyCtxt(ctxt)
            self.afseal.multiply(deref(new_ctxt._ptr_ctxt), deref(ctxt_other._ptr_ctxt))
            new_ctxt.mod_level += 1
            return new_ctxt
        else:
            self.afseal.multiply(deref(ctxt._ptr_ctxt), deref(ctxt_other._ptr_ctxt))
            ctxt.mod_level += 1
            return ctxt

    cpdef PyCtxt multiply_plain (self, PyCtxt ctxt, PyPtxt ptxt, bool in_new_ctxt=False):

        if (ctxt._scheme != ptxt._scheme):
            raise RuntimeError("<Pyfhel ERROR> scheme type mistmatch in mult terms"
                                " ({ctxt._scheme} VS {ptxt._scheme})")
        if (in_new_ctxt):
            ctxt = PyCtxt(ctxt)
        self.afseal.multiply_plain(deref(ctxt._ptr_ctxt), deref(ptxt._ptr_ptxt))
        ctxt.mod_level += 1
        return ctxt

    cpdef PyCtxt scalar_prod(self,
        PyCtxt ctxt, PyCtxt ctxt_other,
        bool in_new_ctxt=False,
        bool with_relin=True,
        bool with_mod_switch=True,
        size_t n_elements=0
    ):


        ctxt = self.multiply(ctxt, ctxt_other, in_new_ctxt=in_new_ctxt)
        if (with_relin):
            self.relinearize(ctxt)
        if (with_mod_switch and self.scheme == Scheme_t.ckks):
            self.mod_switch_to_next_ctxt(ctxt)


        return self.cumul_add(ctxt, in_new_ctxt=False, n_elements=n_elements)

    cpdef PyCtxt scalar_prod_plain(self,
        PyCtxt ctxt, PyPtxt ptxt_other,
        bool in_new_ctxt=False,
        bool with_relin=True,
        bool with_mod_switch=True,
        size_t n_elements=0
    ):


        ctxt = self.multiply_plain(ctxt, ptxt_other, in_new_ctxt=in_new_ctxt)
        if (with_relin):
            self.relinearize(ctxt)
        if (with_mod_switch and self.scheme == Scheme_t.ckks):
            self.mod_switch_to_next_ctxt(ctxt)


        return self.cumul_add(ctxt, in_new_ctxt=False, n_elements=n_elements)

    cpdef PyCtxt rotate(self, PyCtxt ctxt, int k, bool in_new_ctxt=False):

        if self.is_rotate_key_empty():
            warn("<Pyfhel Warning> rot_key empty, initializing it for rotation.", RuntimeWarning)
            self.rotateKeyGen()
        if (in_new_ctxt):
            new_ctxt = PyCtxt(ctxt)
            self.afseal.rotate(deref(new_ctxt._ptr_ctxt), k)
            return new_ctxt
        else:
            self.afseal.rotate(deref(ctxt._ptr_ctxt), k)
            return ctxt

    cpdef PyCtxt flip(self, PyCtxt ctxt, bool in_new_ctxt=False):

        if self.is_rotate_key_empty():
            warn("<Pyfhel Warning> rot_key empty, initializing it for rotation.", RuntimeWarning)
            self.rotateKeyGen()
        if (in_new_ctxt):
            new_ctxt = PyCtxt(ctxt)
            self.afseal.flip(deref(new_ctxt._ptr_ctxt))
            return new_ctxt
        else:
            self.afseal.flip(deref(ctxt._ptr_ctxt))
            return ctxt

    cpdef PyCtxt power(self, PyCtxt ctxt, uint64_t expon, bool in_new_ctxt=False):

        if self.is_relin_key_empty():
            warn("<Pyfhel Warning> relin_key empty, generating it for relinearization.", RuntimeWarning)
            self.relinKeyGen()
        if (in_new_ctxt):
            new_ctxt = PyCtxt(ctxt)
            self.afseal.exponentiate(deref(new_ctxt._ptr_ctxt), expon)
            return new_ctxt
        else:
            self.afseal.exponentiate(deref(ctxt._ptr_ctxt), expon)
            return ctxt


    cpdef void rescale_to_next(self, PyCtxt ctxt):

        if self.scheme != Scheme_t.ckks:
            raise RuntimeError("<Pyfhel ERROR> Scheme must be CKKS for rescaling")
        self.afseal.rescale_to_next(deref(ctxt._ptr_ctxt))

    cpdef PyCtxt mod_switch_to_next_ctxt(self, PyCtxt ctxt, bool in_new_ctxt=False):

        new_ctxt = PyCtxt(ctxt) if (in_new_ctxt) else ctxt
        if new_ctxt.scheme in (Scheme_t.ckks, Scheme_t.bgv):
            new_ctxt.mod_level += 1
            self.afseal.mod_switch_to_next(deref(new_ctxt._ptr_ctxt))
        return new_ctxt

    cpdef PyPtxt mod_switch_to_next_ptxt(self, PyPtxt ptxt, bool in_new_ptxt=True):

        new_ptxt = PyPtxt(ptxt) if (in_new_ptxt) else ptxt
        if new_ptxt.scheme in (Scheme_t.ckks, Scheme_t.bgv):
            new_ptxt.mod_level += 1
            self.afseal.mod_switch_to_next_plain(deref(new_ptxt._ptr_ptxt))
        return new_ptxt

    def mod_switch_to_next(self, cipher_or_plain, in_new_obj=False):

        if isinstance(cipher_or_plain, PyCtxt):
            return self.mod_switch_to_next_ctxt(cipher_or_plain, in_new_obj)
        elif isinstance(cipher_or_plain, PyPtxt):
            return self.mod_switch_to_next_ptxt(cipher_or_plain, in_new_obj)
        else:
            raise TypeError("<Pyfhel ERROR> Expected PyCtxt or PyPtxt for mod switching.")


    def align_mod_n_scale(self,
        this: PyCtxt, other: Union[PyCtxt, PyPtxt],
        copy_this: bool = True, copy_other: bool = True,
        only_mod: bool = False,
    ) -> Tuple[PyCtxt, Union[PyCtxt, PyPtxt]]:

        if not((isinstance(other, (PyCtxt, PyPtxt))  and                 (this.scheme in (Scheme_t.ckks, Scheme_t.bgv))  and                 (other.scheme in (Scheme_t.ckks, Scheme_t.bgv)))):
            return this, other
        elif (this.scale == other.scale) and (this.mod_level == other.mod_level):
            return this, other
        else:

            this_ = PyCtxt(copy_ctxt=this) if copy_this else this
            if isinstance(other, PyCtxt):
                other_ = PyCtxt(copy_ctxt=other) if copy_other else other
            else:
                other_ = PyPtxt(copy_ptxt=other) if copy_other else other

            if ((this_.scale != other_.scale) or not only_mod):

                if this_.scale_bits == other_.scale_bits:
                    if 2**this_.scale_bits != this_.scale: this_.round_scale()
                    if 2**other_.scale_bits != other_.scale: other_.round_scale()

                else:

                    (c_rescale, c_mod_switch)  = (this_, other_)                        if (this_.scale_bits > other_.scale_bits) else (other_, this_)
                    scale_bits_diff = c_rescale.scale_bits - c_mod_switch.scale_bits

                    available_rescalings =                        np.cumsum(self.qi_sizes[1+c_mod_switch.mod_level:
                                          1+c_rescale.mod_level])
                    if (scale_bits_diff) not in available_rescalings:
                        warn("Cannot align scales {} and {} (available rescalings: {})".format(this_.scale_bits, other_.scale_bits, available_rescalings))
                        return this_, other_
                    else:
                        n_rescalings = list(available_rescalings).index(scale_bits_diff)+1
                        for _ in range(n_rescalings):
                            self.rescale_to_next(c_rescale)
                            self.mod_switch_to_next(c_mod_switch)
                        c_rescale.round_scale()

            if (this_.mod_level != other_.mod_level):

                (c, c_mod_switch)  = (this_, other_)                    if (this_.mod_level > other_.mod_level) else (other_, this_)

                for _ in range(c.mod_level - c_mod_switch.mod_level):
                    self.mod_switch_to_next(c_mod_switch)
            return this_, other_








    cpdef size_t save_context(self, fileName, str compr_mode="zstd"):

        cdef string f_name = _to_valid_file_str(fileName, check=False).encode()
        cdef ofstream ostr = ofstream(f_name, binary)
        _write_cy_attributes(self, ostr)
        return self.afseal.save_context(ostr, compr_mode.encode())

    cpdef size_t load_context(self, fileName):

        cdef string f_name = _to_valid_file_str(fileName, check=True).encode()
        cdef ifstream istr = ifstream(f_name, binary)
        _read_cy_attributes(self, istr)
        return self.afseal.load_context(istr, self._sec)

    cpdef size_t save_public_key(self, fileName, str compr_mode="zstd"):

        cdef string f_name = _to_valid_file_str(fileName, check=False).encode()
        cdef ofstream ostr = ofstream(f_name, binary)
        return self.afseal.save_public_key(ostr, compr_mode.encode())

    cpdef size_t load_public_key(self, fileName):

        cdef string f_name = _to_valid_file_str(fileName, check=True).encode()
        cdef ifstream istr = ifstream(f_name, binary)
        return self.afseal.load_public_key(istr)

    cpdef size_t save_secret_key(self, fileName, str compr_mode="zstd"):

        cdef string f_name = _to_valid_file_str(fileName, check=False).encode()
        cdef ofstream ostr = ofstream(f_name, binary)
        return self.afseal.save_secret_key(ostr, compr_mode.encode())

    cpdef size_t load_secret_key(self, fileName):

        cdef string f_name = _to_valid_file_str(fileName, check=True).encode()
        cdef ifstream istr = ifstream(f_name, binary)
        return self.afseal.load_secret_key(istr)

    cpdef size_t save_relin_key(self, fileName, str compr_mode="zstd"):

        cdef string f_name = _to_valid_file_str(fileName, check=False).encode()
        cdef ofstream ostr = ofstream(f_name, binary)
        return self.afseal.save_relin_keys(ostr, compr_mode.encode())

    cpdef size_t load_relin_key(self, fileName):

        cdef string f_name = _to_valid_file_str(fileName, check=True).encode()
        cdef ifstream istr = ifstream(f_name, binary)
        return self.afseal.load_relin_keys(istr)

    cpdef size_t save_rotate_key(self, fileName, str compr_mode="zstd"):

        cdef string f_name = _to_valid_file_str(fileName, check=False).encode()
        cdef ofstream ostr = ofstream(f_name, binary)
        return self.afseal.save_rotate_keys(ostr, compr_mode.encode())

    cpdef size_t load_rotate_key(self, fileName):

        cdef string f_name = _to_valid_file_str(fileName, check=True).encode()
        cdef ifstream istr = ifstream(f_name, binary)
        return self.afseal.load_rotate_keys(istr)




    cpdef bytes to_bytes_context(self, str compr_mode="zstd"):

        cdef ostringstream ostr
        _write_cy_attributes(self, ostr)
        self.afseal.save_context(ostr, compr_mode.encode())
        return ostr.str()

    cpdef size_t from_bytes_context(self, bytes content):

        cdef stringstream istr
        istr.write(content,len(content))
        _read_cy_attributes(self, istr)
        return self.afseal.load_context(istr, self._sec)

    cpdef bytes to_bytes_public_key(self, str compr_mode="zstd"):

        cdef ostringstream ostr
        self.afseal.save_public_key(ostr, compr_mode.encode())
        return ostr.str()

    cpdef size_t from_bytes_public_key(self, bytes content):

        cdef stringstream istr
        istr.write(content,len(content))
        return self.afseal.load_public_key(istr)

    cpdef bytes to_bytes_secret_key(self, str compr_mode="zstd"):

        cdef ostringstream ostr
        self.afseal.save_secret_key(ostr, compr_mode.encode())
        return ostr.str()

    cpdef size_t from_bytes_secret_key(self, bytes content):

        cdef stringstream istr
        istr.write(content,len(content))
        return self.afseal.load_secret_key(istr)

    cpdef bytes to_bytes_relin_key(self, str compr_mode="zstd"):

        cdef ostringstream ostr
        self.afseal.save_relin_keys(ostr, compr_mode.encode())
        return ostr.str()

    cpdef size_t from_bytes_relin_key(self, bytes content):

        cdef stringstream istr
        istr.write(content,len(content))
        return self.afseal.load_relin_keys(istr)

    cpdef bytes to_bytes_rotate_key(self, str compr_mode="zstd"):

        cdef ostringstream ostr
        self.afseal.save_rotate_keys(ostr, compr_mode.encode())
        return ostr.str()

    cpdef size_t from_bytes_rotate_key(self, bytes content):

        cdef stringstream istr
        istr.write(content,len(content))
        return self.afseal.load_rotate_keys(istr)


    cpdef size_t sizeof_context(self, str compr_mode="none"):

        return self.afseal.sizeof_context(compr_mode)

    cpdef size_t sizeof_public_key(self, str compr_mode="none"):

        return self.afseal.sizeof_public_key(compr_mode)

    cpdef size_t sizeof_secret_key(self, str compr_mode="none"):

        return self.afseal.sizeof_secret_key(compr_mode)

    cpdef size_t sizeof_relin_key(self, str compr_mode="none"):

        return self.afseal.sizeof_relin_keys(compr_mode)

    cpdef size_t sizeof_rotate_key(self, str compr_mode="none"):

        return self.afseal.sizeof_rotate_keys(compr_mode)




    cpdef long maxBitCount(self, long poly_modulus_degree, int sec_level):

        return (<Afseal*>self.afseal).maxBitCount(poly_modulus_degree, sec_level)

    cpdef vector[uint64_t] get_qi(self):

        return (<Afseal*>self.afseal).get_qi()

    cpdef vector[uint64_t] plaintext_qi(self, PyPtxt ptxt):

        return (<Afseal*>self.afseal).get_plaintext_qi(deref(ptxt._ptr_ptxt))

    cpdef vector[uint64_t] ciphertext_qi(self, PyCtxt ctxt):

        return (<Afseal*>self.afseal).get_ciphertext_qi(deref(ctxt._ptr_ctxt))

    cpdef vector[uint64_t] plaintext_to_raw(self, PyPtxt ptxt):

        return (<Afseal*>self.afseal).plaintext_to_raw(deref(ptxt._ptr_ptxt))

    cpdef void raw_to_plaintext(self, vector[uint64_t] raw, PyPtxt ptxt):

        (<Afseal*>self.afseal).plaintext_from_raw(raw, deref(ptxt._ptr_ptxt))

    def multDepth(self, max_depth=64, delta=0.1, x_y_z=(1, 10, 0.1), verbose=False):



















        raise NotImplementedError("multDepth is not implemented yet")


    cpdef bool batchEnabled(self):

        return (<Afseal*>self.afseal).batchEnabled()


    cpdef size_t get_nSlots(self):

        return (<Afseal*>self.afseal).get_nSlots()

    cpdef uint64_t get_plain_modulus(self):

        return self.afseal.get_plain_modulus()

    cpdef size_t get_poly_modulus_degree(self):

        return self.afseal.get_poly_modulus_degree()

    cpdef scheme_t get_scheme(self):

        return self.afseal.get_scheme()

    cpdef bool is_secret_key_empty(self):

        return (<Afseal*>self.afseal).is_secretKey_empty()

    cpdef bool is_public_key_empty(self):

        return (<Afseal*>self.afseal).is_publicKey_empty()

    cpdef bool is_rotate_key_empty(self):

        return (<Afseal*>self.afseal).is_rotKey_empty()

    cpdef bool is_relin_key_empty(self):

        return (<Afseal*>self.afseal).is_relinKeys_empty()

    cpdef bool is_context_empty(self):

        return (<Afseal*>self.afseal).is_context_empty()







    cpdef PyPoly empty_poly(self, PyCtxt ref):


        return PyPoly(ref=ref)

    cpdef PyPoly poly_from_ciphertext(self, PyCtxt ctxt, size_t i):

        return PyPoly(ref=ctxt, index=i)

    cpdef PyPoly poly_from_plaintext(self, PyCtxt ref, PyPtxt ptxt):

        return PyPoly(ref=ref, ptxt=ptxt)

    cpdef PyPoly poly_from_coeff_vector(self, vector[cy_complex] coeff_vector, PyCtxt ref):

        return PyPoly(coeff_vector, ref=ref)

    cpdef list polys_from_ciphertext(self, PyCtxt ctxt):

        raise NotImplementedError("TODO: Not yet there")


    cpdef PyPoly poly_add(self, PyPoly p, PyPoly p_other, bool in_new_poly=False):

        res_poly = PyPoly(p) if in_new_poly else p
        self.afseal.add_inplace(deref(res_poly._afpoly), deref(p_other._afpoly))
        return res_poly

    cpdef PyPoly poly_subtract(self, PyPoly p, PyPoly p_other, bool in_new_poly=False):

        res_poly = PyPoly(p) if in_new_poly else p
        self.afseal.subtract_inplace(deref(res_poly._afpoly), deref(p_other._afpoly))
        return res_poly

    cpdef PyPoly poly_multiply(self, PyPoly p, PyPoly p_other, bool in_new_poly=False):

        res_poly = PyPoly(p) if in_new_poly else p
        self.afseal.multiply_inplace(deref(res_poly._afpoly), deref(p_other._afpoly))
        return res_poly

    cpdef PyPoly poly_invert(self, PyPoly p, bool in_new_poly=False):

        res_poly = PyPoly(p) if in_new_poly else p
        self.afseal.invert_inplace(deref(res_poly._afpoly))
        return res_poly


    cpdef void poly_to_ciphertext(self, PyPoly p, PyCtxt ctxt, size_t i):

        self.afseal.poly_to_ciphertext(deref(p._afpoly), deref(ctxt._ptr_ctxt), i)

    cpdef void poly_to_plaintext(self, PyPoly p, PyPtxt ptxt):

        self.afseal.poly_to_plaintext(deref(p._afpoly), deref(ptxt._ptr_ptxt))
