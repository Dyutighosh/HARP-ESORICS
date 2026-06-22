





from libcpp.vector cimport vector
from libcpp.string cimport string
from libcpp.memory cimport shared_ptr, dynamic_pointer_cast
from libcpp.map cimport map as cpp_map
from libcpp.complex cimport complex as c_complex
from libcpp cimport bool


from Pyfhel.utils.iostream cimport istream, ostream, ifstream, ofstream

from libc.stdint cimport int64_t, uint64_t, uint8_t

ctypedef c_complex[double] cy_complex





cdef extern from "seal/plaintext.h" namespace "seal" nogil:
    cdef cppclass Plaintext:
        Plaintext() except +
        Plaintext(const Plaintext &copy) except +
        bool is_zero() except +
        string to_string() except +
        inline bool is_ntt_form()
        double scale() except +


cdef extern from "seal/ciphertext.h" namespace "seal" nogil:
    cdef cppclass Ciphertext:
        Ciphertext() except +
        Ciphertext(const Ciphertext &copy) except +
        int size_capacity() except +
        int size() except +
        double scale() except +




cdef extern from "Afhel.h" nogil:


    cdef enum class scheme_t(uint8_t):
        none,
        bfv
        ckks
        bgv
    cdef cpp_map scheme_t_str[scheme_t, string]


    cdef enum class backend_t(uint8_t):
        none,
        seal,
        palisade
    cdef cpp_map backend_t_str[backend_t, string]



    cdef cppclass AfCtxt:
        pass


    cdef cppclass AfPtxt:
        pass


    cdef cppclass AfPoly:
        AfPoly() except +
        void add_inplace(const AfPoly &other) except +
        void subtract_inplace(const AfPoly &other) except +
        void multiply_inplace(const AfPoly &other) except +
        bool invert_inplace() except +


    cdef cppclass Afhel:

        Afhel() except +



        string ContextGen(scheme_t scheme, size_t poly_modulus_degree,
                        uint64_t plain_modulus_bit_size, uint64_t plain_modulus,
                        int sec, vector[int] qi_sizes, vector[uint64_t] qi) except +
        void KeyGen() except +
        void relinKeyGen() except +
        void rotateKeyGen(vector[int] rot_steps) except +


        void encrypt(AfPtxt& ptxt, AfCtxt& ctxtOut) except +
        void encrypt_v(vector[shared_ptr[AfPtxt]]& plainV, vector[shared_ptr[AfCtxt]]& ctxtVOut) except +


        void decrypt(AfCtxt &ctxtInOut, AfPtxt &plainOut) except +
        void decrypt_v(vector[shared_ptr[AfCtxt]] &ctxtV, vector[shared_ptr[AfPtxt]] &plainVOut) except +


        int noise_level(AfCtxt& ctxtInOut) except +




        void encode_i(vector[int64_t] &values, AfPtxt &plainOut) except +

        void encode_f(vector[double] &values, double scale, AfPtxt &plainVOut) except +
        void encode_c(vector[cy_complex] &values, double scale, AfPtxt &plainVOut) except +

        void encode_g(vector[int64_t] &values, AfPtxt &plainOut) except +



        void decode_i(AfPtxt &ptxt, vector[int64_t] &valueVOut) except +

        void decode_f(AfPtxt &ptxt, vector[double] &valueVOut) except +
        void decode_c(AfPtxt &ptxt, vector[cy_complex] &valueVOut) except +

        void decode_g(AfPtxt &ptxt, vector[int64_t] &valueVOut) except +


        void data(AfPtxt &ptxt, uint64_t *dest) except +
        void allocate_zero_poly(uint64_t n, uint64_t coeff_mod_count, uint64_t *dest) except +


        void relinearize(AfCtxt& ctxtInOut) except +



        void negate(AfCtxt& ctxtInOut) except +
        void negate_v(vector[shared_ptr[AfCtxt]]& ctxtV) except +

        void square(AfCtxt& ctxtInOut) except +
        void square_v(vector[shared_ptr[AfCtxt]]& ctxtV) except +

        void add(AfCtxt& ctxtInOut, AfCtxt& ctxt) except +
        void add_plain(AfCtxt& ctxtInOut, AfPtxt& plain2) except +
        void add_v(vector[shared_ptr[AfCtxt]]& ctxtVInOut, vector[shared_ptr[AfCtxt]]& ctxtV) except +
        void add_plain_v(vector[shared_ptr[AfCtxt]]& ctxtVInOut, vector[shared_ptr[AfPtxt]]& ptxtV) except +


        void sub(AfCtxt& ctxtInOut, AfCtxt& ctxt) except +
        void sub_plain(AfCtxt& ctxtInOut, AfPtxt& plain2) except +
        void sub_v(vector[shared_ptr[AfCtxt]]& ctxtVInOut, vector[shared_ptr[AfCtxt]]& ctxtV) except +
        void sub_plain_v(vector[shared_ptr[AfCtxt]]& ctxtVInOut, vector[shared_ptr[AfPtxt]]& ptxtV) except +


        void multiply(AfCtxt& ctxtInOut, AfCtxt& ctxt) except +
        void multiply_plain(AfCtxt& ctxtInOut, AfPtxt& ptxt) except +
        void multiply_v(vector[shared_ptr[AfCtxt]]& ctxtVInOut, vector[shared_ptr[AfCtxt]]& ctxtV) except +
        void multiply_plain_v(vector[shared_ptr[AfCtxt]]& ctxtVInOut, vector[shared_ptr[AfPtxt]]& ptxtV) except +


        void rotate(AfCtxt& ctxtInOut, int k) except +
        void rotate_v(vector[shared_ptr[AfCtxt]]& ctxtV, int k) except +
        void flip(AfCtxt& ctxtInOut) except +
        void flip_v(vector[shared_ptr[AfCtxt]]& ctxtV) except +


        void exponentiate(AfCtxt& ctxtInOut, uint64_t& expon) except +
        void exponentiate_v(vector[shared_ptr[AfCtxt]]& ctxtV, uint64_t& expon) except +


        void rescale_to_next(AfCtxt &ctxtInOut) except +
        void rescale_to_next_v(vector[shared_ptr[AfCtxt]]& ctxtVInOut) except +
        void mod_switch_to_next(AfCtxt &ctxtInOut) except +
        void mod_switch_to_next_v(vector[shared_ptr[AfCtxt]]& ctxtVInOut) except +
        void mod_switch_to_next_plain(AfPtxt &ptxtInOut) except +
        void mod_switch_to_next_plain_v(vector[shared_ptr[AfPtxt]]& ptxtVInOut) except +



        size_t save_context(ostream &out_stream, string &compr_mode) except +
        size_t load_context(istream &in_stream, int sec) except +


        size_t save_public_key(ostream &out_stream, string &compr_mode) except +
        size_t load_public_key(istream &in_stream) except +


        size_t save_secret_key(ostream &out_stream, string &compr_mode) except +
        size_t load_secret_key(istream &in_stream) except +


        size_t save_relin_keys(ostream &out_stream, string &compr_mode) except +
        size_t load_relin_keys(istream &in_stream) except +


        size_t save_rotate_keys(ostream &out_stream, string &compr_mode) except +
        size_t load_rotate_keys(istream &in_stream) except +


        size_t save_plaintext(ostream &out_stream, string &compr_mode, AfPtxt &plain) except +
        size_t load_plaintext(istream &in_stream, AfPtxt &plain) except +


        size_t save_ciphertext(ostream &out_stream, string &compr_mode, AfCtxt &ciphert) except +
        size_t load_ciphertext(istream &in_stream, AfCtxt &plain) except +


        size_t sizeof_context(string &compr_mode) except +
        size_t sizeof_public_key(string &compr_mode) except +
        size_t sizeof_secret_key(string &compr_mode) except +
        size_t sizeof_relin_keys(string &compr_mode) except +
        size_t sizeof_rotate_keys(string &compr_mode) except +
        size_t sizeof_plaintext(string &compr_mode, AfPtxt &pt) except +
        size_t sizeof_ciphertext(string &compr_mode, AfCtxt &ct) except +



        double scale(AfCtxt &ctxt) except +
        void override_scale(AfCtxt &ctxt, double scale) except +


        vector[uint64_t] get_qi() except +
        vector[uint64_t] get_plaintext_qi(AfPtxt &ptxt) except +
        vector[uint64_t] get_ciphertext_qi(AfCtxt &ctxt) except +
        vector[uint64_t] plaintext_to_raw(AfPtxt &ptxt) except +
        void plaintext_from_raw(vector[uint64_t] &raw, AfPtxt &ptxt) except +
        uint64_t get_plain_modulus() except +
        size_t get_poly_modulus_degree() except +
        scheme_t get_scheme() except +

        bool is_secretKey_empty() except+
        bool is_publicKey_empty() except+
        bool is_rotKey_empty() except+
        bool is_relinKeys_empty() except+
        bool is_context_empty() except+



        void add_inplace(AfPoly &p1, AfPoly &p2) except+
        void subtract_inplace(AfPoly &p1, AfPoly &p2) except+
        void multiply_inplace(AfPoly &p1, AfPoly &p2) except+
        bool invert_inplace(AfPoly &p) except+


        void poly_to_ciphertext(AfPoly &p, AfCtxt &ctxt, size_t i) except+
        void poly_to_plaintext(AfPoly &p, AfPtxt &ptxt) except+






cdef extern from "Afseal.h" nogil:
    cdef cppclass AfsealCtxt(AfCtxt, Ciphertext):
        AfsealCtxt() except +
        AfsealCtxt(const AfsealCtxt &other) except +
        void set_scale(double new_scale)

    cdef cppclass AfsealPtxt(AfPtxt, Plaintext):
        AfsealPtxt() except +
        AfsealPtxt(const AfsealPtxt &other) except +
        void set_scale(double new_scale)

    cdef cppclass Afseal(Afhel):
        Afseal() except +
        Afseal(const Afseal &other) except +
        AfsealPoly get_publicKey_poly(size_t index) except +
        AfsealPoly get_secretKey_poly() except +
        long maxBitCount(long poly_modulus_degree, int sec_level) except +
        bool batchEnabled() except +
        size_t get_nSlots() except +
        int get_sec() except +
        int total_coeff_modulus_bit_count() except +

    cdef cppclass AfsealPoly(AfPoly):
        AfsealPoly(Afseal &afseal, const AfsealCtxt &ref) except+
        AfsealPoly(AfsealPoly &other) except+
        AfsealPoly(Afseal &afseal, AfsealCtxt &ctxt, size_t index) except+
        AfsealPoly(Afseal &afseal, AfsealPtxt &ptxt, const AfsealCtxt &ref) except+

        vector[cy_complex] to_coeff_list(Afseal &afseal) except+

        cy_complex get_coeff(Afseal &afseal, size_t i) except+
        void set_coeff(Afseal &afseal, cy_complex &val, size_t i) except+
        size_t get_coeff_count() except+
        size_t get_coeff_modulus_count() except+