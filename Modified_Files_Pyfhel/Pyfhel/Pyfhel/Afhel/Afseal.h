






























#ifndef AFSEAL_H
#define AFSEAL_H

#include <iostream>
#include <string>
#include <vector>
#include <thread>
#include <memory>
#include <complex>
#include <math.h>
#include <fstream>
#include <assert.h>
#include <map>

#include "Afhel.h"
#include "seal/dynarray.h"
#include "seal/seal.h"
#include "seal/util/polyarithsmallmod.h"

using namespace std;
using namespace seal;



class AfsealCtxt;
class AfsealPtxt;
class Afseal;
class AfsealPoly;



static map<string, seal::compr_mode_type> compr_mode_map {
    {"none", compr_mode_type::none},
#ifdef SEAL_USE_ZLIB

    {"zlib", compr_mode_type::zlib},
#endif
#ifdef SEAL_USE_ZSTD

    {"zstd", compr_mode_type::zstd},
#endif
};
static map<seal::scheme_type, scheme_t> scheme_map_to_afhel {
   {seal::scheme_type::none, scheme_t::none},
   {seal::scheme_type::bfv,  scheme_t::bfv},
   {seal::scheme_type::ckks, scheme_t::ckks},
   {seal::scheme_type::bgv,  scheme_t::bgv},
};
static map<scheme_t, seal::scheme_type> scheme_map_to_seal {
   {scheme_t::none, seal::scheme_type::none},
   {scheme_t::bfv, seal::scheme_type::bfv},
   {scheme_t::ckks, seal::scheme_type::ckks},
   {scheme_t::bgv, seal::scheme_type::bgv},
};
static map<int, sec_level_type> sec_map{
    {0, seal::sec_level_type::none},
    {128, seal::sec_level_type::tc128},
    {192, seal::sec_level_type::tc192},
    {256, seal::sec_level_type::tc256},
};




class AfsealPtxt: public AfPtxt, public seal::Plaintext{
 public:
  using seal::Plaintext::Plaintext;
  virtual ~AfsealPtxt() = default;
  void set_scale(double new_scale){
    this->scale() = new_scale;
  };
};





class AfsealCtxt: public AfCtxt, public seal::Ciphertext{
public:
  using seal::Ciphertext::Ciphertext;
  virtual ~AfsealCtxt() = default;
  void set_scale(double new_scale){
    this->scale() = new_scale;
  };

};






class AfsealPoly: public AfPoly {
 private:


  seal::parms_id_type parms_id;


  seal::MemoryPoolHandle mempool;


  seal::DynArray<uint64_t> coeff_repr;


  seal::DynArray<uint64_t> eval_repr;



  bool coeff_repr_valid = false;


  size_t coeff_count;


  vector<seal::Modulus> coeff_modulus;


  size_t coeff_modulus_count;


  void generate_coeff_repr(Afseal &afseal);

 public:



  virtual ~AfsealPoly();


  AfsealPoly(const AfsealPoly &other) = default;


  AfsealPoly &operator=(const AfsealPoly &other) = default;




  AfsealPoly(Afseal &afseal);




  AfsealPoly(Afseal &afseal, const AfsealCtxt &ref);





  AfsealPoly(Afseal &afseal, AfsealCtxt &ctxt, size_t index);





  AfsealPoly(Afseal &afseal, AfsealPtxt &ptxt, const AfsealCtxt &ref) {

    throw runtime_error("FUNCTION REMOVED.");
  }




  AfsealPoly(Afseal &afseal, AfsealPtxt &ptxt);





  vector<complex<double>> to_coeff_list(Afhel &afseal);




  complex<double> get_coeff(Afhel &afseal, size_t i);



  void set_coeff(Afhel &afseal, complex<double> &val, size_t i);



  void add_inplace(const AfPoly &other);
  void subtract_inplace(const AfPoly &other);
  void multiply_inplace(const AfPoly &other);

  bool invert_inplace();


  size_t get_coeff_count(){return this->coeff_count;}


  size_t get_coeff_modulus_count(){return this->coeff_modulus_count;}
};







inline AfsealCtxt& _dyn_c(AfCtxt& c){return dynamic_cast<AfsealCtxt&>(c);};
inline AfsealPtxt& _dyn_p(AfPtxt& p){return dynamic_cast<AfsealPtxt&>(p);};

class Afseal: public Afhel {

 private:


  shared_ptr<seal::SEALContext> context = NULL;
  shared_ptr<seal::BatchEncoder> bfvEncoder = NULL;
  shared_ptr<seal::CKKSEncoder> ckksEncoder = NULL;
  shared_ptr<seal::BatchEncoder> bgvEncoder = NULL;

  shared_ptr<seal::KeyGenerator> keyGenObj = NULL;
  shared_ptr<seal::SecretKey> secretKey = NULL;
  shared_ptr<seal::PublicKey> publicKey = NULL;
  shared_ptr<seal::RelinKeys> relinKeys = NULL;
  shared_ptr<seal::GaloisKeys> rotateKeys = NULL;

  shared_ptr<seal::Encryptor> encryptor = NULL;
  shared_ptr<seal::Evaluator> evaluator = NULL;
  shared_ptr<seal::Decryptor> decryptor = NULL;


  friend ostream &operator<<(ostream &outs, Afseal const &af);
  friend istream &operator>>(istream &ins, Afseal const &af);


 public:
  vector<uint64_t> qi;


  Afseal();
  Afseal(const Afseal &otherAfseal);
  Afseal &operator=(const Afseal &assign) = default;
  Afseal(Afseal &&source) = default;
  virtual ~Afseal();



  string ContextGen(
    scheme_t scheme, uint64_t poly_modulus_degree = 1024,
    uint64_t plain_modulus_bit_size = 0, uint64_t plain_modulus = 0,
    int sec = 128, vector<int> qi_sizes = {}, vector<uint64_t> qi_values = {});


  void KeyGen();
  void relinKeyGen();
  void rotateKeyGen(vector<int> rot_steps = {});


  void encrypt(AfPtxt &ptxt, AfCtxt &cipherOut);
  void encrypt_v(vector<shared_ptr<AfPtxt>> &ptxtV, vector<shared_ptr<AfCtxt>> &ctxtVOut);


  void decrypt(AfCtxt &ctxt, AfPtxt &plainOut);
  void decrypt_v(vector<shared_ptr<AfCtxt>> &ctxtV, vector<shared_ptr<AfPtxt>> &ptxtVOut);


  int noise_level(AfCtxt &ctxt);




  void encode_i(vector<int64_t> &values, AfPtxt &plainOut);

  void encode_f(vector<double> &values, double scale, AfPtxt &ptxtVOut);
  void encode_c(vector<std::complex<double>> &values, double scale, AfPtxt &ptxtVOut);

  void encode_g(vector<int64_t> &values, AfPtxt &plainOut);



  void decode_i(AfPtxt &ptxt, vector<int64_t> &valueVOut);

  void decode_f(AfPtxt &ptxt, vector<double> &valueVOut);
  void decode_c(AfPtxt &ptxt, vector<std::complex<double>> &valueVOut);

  void decode_g(AfPtxt &ptxt, vector<int64_t> &valueVOut);


  void data(AfPtxt &ptxt, uint64_t *dest);
  void allocate_zero_poly(uint64_t n, uint64_t coeff_mod_count, uint64_t *dest);


  void relinearize(AfCtxt &ctxt);
  void relinearize_v(vector<shared_ptr<AfCtxt>> ctxtV);



  void negate(AfCtxt &ctxt);
  void negate_v(vector<shared_ptr<AfCtxt>> &ctxtV);


  void square(AfCtxt &ctxt);
  void square_v(vector<shared_ptr<AfCtxt>> &ctxtV);


  void add(AfCtxt &ctxtInOut, AfCtxt &ctxt);
  void add_plain(AfCtxt &ctxtInOut, AfPtxt &ptxt);
  void add_v(vector<shared_ptr<AfCtxt>> &ctxtVInOut, vector<shared_ptr<AfCtxt>> &ctxtV2);
  void add_plain_v(vector<shared_ptr<AfCtxt>> &ctxtVInOut, vector<shared_ptr<AfPtxt>> &ptxtV2);


  void sub(AfCtxt &ctxtInOut, AfCtxt &ctxt);
  void sub_plain(AfCtxt &ctxtInOut, AfPtxt &ptxt);
  void sub_v(vector<shared_ptr<AfCtxt>> &ctxtVInOut, vector<shared_ptr<AfCtxt>> &ctxtV2);
  void sub_plain_v(vector<shared_ptr<AfCtxt>> &ctxtVInOut, vector<shared_ptr<AfPtxt>> &ptxtV2);


  void multiply(AfCtxt &ctxtVInOut, AfCtxt &ctxt);
  void multiply_plain(AfCtxt &ctxtVInOut, AfPtxt &ptxt);
  void multiply_v(vector<shared_ptr<AfCtxt>> &ctxtVInOut, vector<shared_ptr<AfCtxt>> &ctxtV2);
  void multiply_plain_v(vector<shared_ptr<AfCtxt>> &ctxtVInOut, vector<shared_ptr<AfPtxt>> &ptxtV2);


  void rotate(AfCtxt &ctxt, int k);
  void rotate_v(vector<shared_ptr<AfCtxt>> &ctxtV, int k);
  void flip(AfCtxt &ctxt);
  void flip_v(vector<shared_ptr<AfCtxt>> &ctxtV);


  void exponentiate(AfCtxt &ctxt, uint64_t &expon);
  void exponentiate_v(vector<shared_ptr<AfCtxt>> &cipherV, uint64_t &expon);


  void rescale_to_next(AfCtxt &ctxt);
  void rescale_to_next_v(vector<shared_ptr<AfCtxt>> &ctxtV);
  void mod_switch_to_next(AfCtxt &ctxt);
  void mod_switch_to_next_v(vector<shared_ptr<AfCtxt>> &ctxtV);
  void mod_switch_to_next_plain(AfPtxt &ptxt);
  void mod_switch_to_next_plain_v(vector<shared_ptr<AfPtxt>> &ptxtV);


  void vectorize(vector<shared_ptr<AfCtxt>> &ctxtVInOut,
                    function<void(AfCtxt)> f);
  void vectorize(vector<shared_ptr<AfPtxt>> &ptxtVInOut,
                    function<void(AfPtxt)> f);
  void vectorize(vector<shared_ptr<AfCtxt>> &ctxtVInOut,vector<shared_ptr<AfCtxt>> &ctxtV2,
                    function<void(AfCtxt, AfCtxt)> f);
  void vectorize(vector<shared_ptr<AfCtxt>> &ctxtVInOut,vector<shared_ptr<AfPtxt>> &ptxtV2,
                    function<void(AfCtxt, AfPtxt)> f);



  seal::compr_mode_type get_compr_mode(string &mode);
  string get_compr_mode(seal::compr_mode_type &mode);


  size_t save_context(ostream &out_stream, string &compr_mode);
  size_t load_context(istream &in_stream, int sec=128);


  size_t save_public_key(ostream &out_stream, string &compr_mode);
  size_t load_public_key(istream &in_stream);


  size_t save_secret_key(ostream &out_stream, string &compr_mode);
  size_t load_secret_key(istream &in_stream);


  size_t save_relin_keys(ostream &out_stream, string &compr_mode);
  size_t load_relin_keys(istream &in_stream);


  size_t save_rotate_keys(ostream &out_stream, string &compr_mode);
  size_t load_rotate_keys(istream &in_stream);


  size_t save_plaintext(ostream &out_stream, string &compr_mode, AfPtxt &pt);
  size_t load_plaintext(istream &in_stream, AfPtxt &pt);


  size_t save_ciphertext(ostream &out_stream, string &compr_mode, AfCtxt &ct);
  size_t load_ciphertext(istream &in_stream, AfCtxt &pt);


  size_t sizeof_context(string &compr_mode);
  size_t sizeof_public_key(string &compr_mode);
  size_t sizeof_secret_key(string &compr_mode);
  size_t sizeof_relin_keys(string &compr_mode);
  size_t sizeof_rotate_keys(string &compr_mode);
  size_t sizeof_plaintext(string &compr_mode, AfPtxt &pt);
  size_t sizeof_ciphertext(string &compr_mode, AfCtxt &ct);


  long maxBitCount(long poly_modulus_degree, int sec_level);


  double scale(AfCtxt &ctxt);
  void override_scale(AfCtxt &ctxt, double scale);


  bool batchEnabled();
  vector<uint64_t> get_qi();
  vector<uint64_t> get_plaintext_qi(AfPtxt &ptxt);
  vector<uint64_t> get_ciphertext_qi(AfCtxt &ctxt);
  vector<uint64_t> plaintext_to_raw(AfPtxt &ptxt);
  void plaintext_from_raw(vector<uint64_t> &raw, AfPtxt &ptxt);
  size_t get_nSlots();
  uint64_t get_plain_modulus();
  size_t get_poly_modulus_degree();
  scheme_t get_scheme();
  int get_sec();
  int total_coeff_modulus_bit_count();

  bool is_secretKey_empty() { return secretKey==NULL; }
  bool is_publicKey_empty() { return publicKey==NULL; }
  bool is_rotKey_empty() { return rotateKeys==NULL; }
  bool is_relinKeys_empty() { return relinKeys==NULL; }
  bool is_context_empty() { return context==NULL; }


  inline shared_ptr<SEALContext>  get_context();
  inline shared_ptr<Evaluator>  get_evaluator();
  inline shared_ptr<Encryptor>  get_encryptor();
  inline shared_ptr<Decryptor>  get_decryptor();
  inline shared_ptr<BatchEncoder>  get_bfv_encoder();
  inline shared_ptr<CKKSEncoder>  get_ckks_encoder();
  inline shared_ptr<BatchEncoder>  get_bgv_encoder();
  inline shared_ptr<SecretKey>  get_secretKey();
  inline shared_ptr<PublicKey>  get_publicKey();
  inline shared_ptr<RelinKeys>  get_relinKeys();
  inline shared_ptr<GaloisKeys>  get_rotateKeys();
  void setpublicKey(seal::PublicKey &pubKey) { this->publicKey = make_shared<seal::PublicKey>(pubKey); }
  void setsecretKey(seal::SecretKey &secKey) { this->secretKey = make_shared<seal::SecretKey>(secKey); }
  void setrelinKeys(seal::RelinKeys &relKey) { this->relinKeys = make_shared<seal::RelinKeys>(relKey); }


  friend class AfPoly;
  friend class AfsealPoly;


  void add_inplace(AfPoly &polyInOut, AfPoly &polyOther);
  void subtract_inplace(AfPoly &polyInOut, AfPoly &polyOther);
  void multiply_inplace(AfPoly &polyInOut, AfPoly &polyOther);
  void invert_inplace(AfPoly &polyInOut);


  void poly_to_ciphertext(AfPoly &p, AfCtxt &ctxt, size_t i);
  void poly_to_plaintext(AfPoly &p, AfPtxt &ptxt);
  AfsealPoly get_publicKey_poly(size_t index);
  AfsealPoly get_secretKey_poly();


  complex<double> get_coeff(AfPoly& poly, size_t i);
  void set_coeff(AfPoly& poly, complex<double> &val, size_t i);
  vector<complex<double>> to_coeff_list(AfPoly& poly);
};
#endif
