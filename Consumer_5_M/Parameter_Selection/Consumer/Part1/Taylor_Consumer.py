import numpy as np
from Pyfhel import Pyfhel
import random
import sys
from matplotlib import rc,rcParams
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time
import numpy as np
from Pyfhel import Pyfhel
import random
import sys
from matplotlib import rc,rcParams
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time
import math
from math import comb
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from pathlib import Path


ERROR = .1
bk = 0.276
LAMBDA = 21
ETA = .5

numconsumers = 1405
numsuppliers = 10


d = [6.57312, 3.19614, 9.39501, 3.23684, 7.11644, 9.60693, 7.11762, 5.15677, 8.61886, 7.70245]
eph = [-0.812197, -0.908682, -0.731571, -0.907519, -0.796673, -0.725516, -0.796639, -0.852664, -0.753747, -0.77993]


def F(i, in_NumberOfTerms):
    return sum(comb(n, i) for n in range(i, in_NumberOfTerms))



n_mults = 12

HE = Pyfhel(key_gen=True, context_params={
    'scheme': 'CKKS',
    'n': 2**15,         # For CKKS, n/2 values can be encoded in a single ciphertext. 
    'scale': 2**60,     # Each multiplication grows the final scale
    'qi_sizes': [60]+ [60]*n_mults +[60] # Number of bits of each prime in the chain. 
                        # Intermediate prime sizes should be close to log2(scale).
                        # One per multiplication! More/higher qi_sizes means bigger 
                        #  ciphertexts and slower ops.
})




HE.relinKeyGen()

def PolyFittingSelf(X, Y, degree, alpha, EN_normalized_Values):

    _r = lambda y: np.round(y, decimals=64)

    B = np.polyfit(X, Y, degree)

    # print('Polynomial Fitting with Numpy')
    # print(B, end='\n\n')
    B3_1 =  B.tolist()
    B3 = B3_1[::-1]
    # print(B3)
    # print('\n')

    K_correction = 1.0
    

    allEncryptedParams = getEncryptedValues(EN_normalized_Values, K_correction)
    Final_error = ErrorCorrection(EN_normalized_Values, B3, allEncryptedParams, K_correction)


    FinalInverse_decryted1  = HE.decryptFrac(Final_error)
    finalErrors = _r(FinalInverse_decryted1)

    finalErrors = finalErrors[:1000]

    mean_error3 = np.mean(abs(Y - finalErrors))

    # print('mean_error3 (Encrypted) =', mean_error3)
    # print('\n')

    mse3_EN = np.mean((Y - finalErrors)**2)

    # print('mse3  (Encrypted) =', mse3_EN)
    # print('\n')

    max_error3 = np.max(np.abs(Y - finalErrors))

    # print('max_error3  (Encrypted) =', max_error3)
    # print('\n')


    all_estimated1 = []
    all_estimated2 = []
    all_estimated3 = []
    all_estimated4 = []
    all_estimated5 = [] 

    for i in range(len(X)):

        y_estimated_3 = 0

        for j in range(len(B3)):

            y_estimated_3 = y_estimated_3 + ((pow(X[i], j)) * (B3[j]))

        all_estimated3.append(y_estimated_3)

    mean_error3 = np.mean(abs(Y - all_estimated3))

    # print('mean_error3 =', mean_error3)

    # print('\n')

    mse3 = np.mean((Y - all_estimated3)**2)

    # print('mse3 =', mse3)

    # print('\n')

    max_error3 = np.max(np.abs(Y - all_estimated3))

    # print('max_error3 =', max_error3)

    # print('\n')

    return degree, B3, mse3_EN



def getEncryptedValues(EN_x, in_Constant_K):

    _r = lambda y: np.round(y, decimals=64)

    Constant_K = in_Constant_K

    # HE.rescale_to_next(EN_x)

    EN_x_2_1 = Constant_K * EN_x
    HE.rescale_to_next(EN_x_2_1)
    ~EN_x_2_1

    EN_x_2 =  EN_x * EN_x_2_1
    HE.rescale_to_next(EN_x_2)
    ~EN_x_2

    EN_x_3 = EN_x_2 * EN_x_2_1
    HE.rescale_to_next(EN_x_3)
    ~EN_x_3

    EN_x_4_1 = EN_x_2 * Constant_K
    HE.rescale_to_next(EN_x_4_1)
    ~EN_x_4_1

    EN_x_4 = EN_x_2 * EN_x_4_1
    HE.rescale_to_next(EN_x_4)
    ~EN_x_4

    EN_x_5 = EN_x_2_1 * EN_x_4
    HE.rescale_to_next(EN_x_5)
    ~EN_x_5

    EN_x_6 = EN_x_4 * EN_x_4_1
    HE.rescale_to_next(EN_x_6)
    ~EN_x_6

    EN_x_7 = EN_x_6 * EN_x_2_1
    HE.rescale_to_next(EN_x_7)
    ~EN_x_7

    EN_x_8_1 = EN_x_4 * Constant_K
    HE.rescale_to_next(EN_x_8_1)
    ~EN_x_8_1 

    EN_x_8 = EN_x_8_1 * EN_x_4
    HE.rescale_to_next(EN_x_8)
    ~EN_x_8

    EN_x_9 = EN_x_2_1 * EN_x_8
    HE.rescale_to_next(EN_x_9)
    ~EN_x_9

    EN_x_10 = EN_x_8 * EN_x_4_1
    HE.rescale_to_next(EN_x_10)
    ~EN_x_10

    EN_x_11_1 = Constant_K * EN_x_8
    HE.rescale_to_next(EN_x_11_1)
    ~EN_x_11_1

    EN_x_11 = EN_x_3 * EN_x_11_1
    HE.rescale_to_next(EN_x_11)
    ~EN_x_11

    EN_x_12 = EN_x_8_1 * EN_x_8
    HE.rescale_to_next(EN_x_12)
    ~EN_x_12

    EN_x_13 = EN_x_11_1 * EN_x_5
    HE.rescale_to_next(EN_x_13)
    ~EN_x_13

    EN_x_14 = EN_x_11_1 * EN_x_6
    HE.rescale_to_next(EN_x_14)
    ~EN_x_14

    EN_x_15 = EN_x_11_1 * EN_x_7
    HE.rescale_to_next(EN_x_15)
    ~EN_x_15

    EN_x_16 = EN_x_11_1 * EN_x_8
    HE.rescale_to_next(EN_x_16)
    ~EN_x_16

    EN_x_17 = EN_x_2_1 * EN_x_16
    HE.rescale_to_next(EN_x_17)
    ~EN_x_17

    EN_x_18 = EN_x_4_1 * EN_x_16
    HE.rescale_to_next(EN_x_18)
    ~EN_x_18

    # EN_x_19_1 = EN_x_16 * Constant_K
    # HE.rescale_to_next(EN_x_19_1)
    # ~EN_x_19_1

    # EN_x_19 = EN_x_3 * EN_x_19_1
    # HE.rescale_to_next(EN_x_19)
    # ~EN_x_19

    # EN_x_20 = EN_x_19_1 * EN_x_4
    # HE.rescale_to_next(EN_x_20)
    # ~EN_x_20  

    # EN_x_21 = EN_x_19_1 * EN_x_5
    # HE.rescale_to_next(EN_x_21)
    # ~EN_x_21

    # EN_x_22 = EN_x_19_1 * EN_x_6
    # HE.rescale_to_next(EN_x_22)
    # ~EN_x_22

    # EN_x_23 = EN_x_19_1 * EN_x_7
    # HE.rescale_to_next(EN_x_23)
    # ~EN_x_23

    # EN_x_24 = EN_x_19_1 * EN_x_8
    # HE.rescale_to_next(EN_x_24)
    # ~EN_x_24

    # EN_x_25 = EN_x_19_1 * EN_x_9
    # HE.rescale_to_next(EN_x_25)
    # ~EN_x_25

    EncryptedValues = [EN_x, EN_x_2, EN_x_3, EN_x_4, EN_x_5, EN_x_6, EN_x_7, EN_x_8, EN_x_9, EN_x_10 , EN_x_11, EN_x_12, EN_x_13, EN_x_14, EN_x_15, EN_x_16, EN_x_17, EN_x_18] #, EN_x_19] #, EN_x_20 , EN_x_21, EN_x_22, EN_x_23, EN_x_24, EN_x_25]

    return EncryptedValues



def DIV_HE(EN_x, in_NumberOfTerms, in_Constant_K, EncryptedValues, in_x, in_originalNotNormalized, Scale):
    _r = lambda y: np.round(y, decimals=64)

    NumberOfTerms = in_NumberOfTerms


    Coff_Result = [(-1)**i for i in range(NumberOfTerms)]

    # print(Coff_Result)

    index = 0
    All_Ks = []

    while index < (NumberOfTerms -1):
        index += 1
        K_Index = index - 1
        K_Value = in_Constant_K**K_Index
        All_Ks.append(K_Value)

    # print(All_Ks)

    InverseX = Coff_Result[0]
    Coff_Result_mod = []

    for i in range(1, NumberOfTerms):
        new_Coff_value = Coff_Result[i] / All_Ks[i-1]
        Coff_Result_mod.append(new_Coff_value)

    # print('All Final Coeff: ', Coff_Result_mod)

    numberOfTermsComputed = 0
    eachTermValueHE = []

    # print('Normalized Value: ', in_x)

    for i in range(1, NumberOfTerms):
        valueX = EncryptedValues[i-1]

        Decrypted1  = HE.decryptFrac(valueX)
        Decrypted_List1 = _r(Decrypted1)
        Decrypted_Value1 = Decrypted_List1[0]

        # print('X^i K^(i-1): ', Decrypted_Value1)

        valueTerm = 0
        coffValue = Coff_Result_mod[i-1] 

        # print('(-1)^i/K^(i-1): ', coffValue)

        try:
            valueTerm = valueX * coffValue
            HE.rescale_to_next(valueTerm)
            ~valueTerm

            Decrypted  = HE.decryptFrac(valueTerm)
            Decrypted_List = _r(Decrypted)
            Decrypted_Value = Decrypted_List[0]

            eachTermValueHE.append(Decrypted_Value)

            # print(Decrypted_Value)

            # print('term: ', Decrypted_Value)

            InverseX = InverseX + valueTerm
            numberOfTermsComputed = i

        except Exception as e:
            # print('exception...', e)
            numberOfTermsComputed = i
            break

    Decrypted11111  = HE.decryptFrac(InverseX)
    Decrypted_List11111 = _r(Decrypted11111)
    # Decrypted_Value111111 = Decrypted_List11111[0]


    # in_originalNotNormalized --> list
    # in_x --> list of normalized
    # Decrypted_List11111 ->computed list of normalized inverse

    # errorDiff_withOrg = pow((abs((((1.0)/in_originalNotNormalized)) - Decrypted_Value111111)), 2)
    # errorDiff = pow(((abs(Decrypted_Value111111 - ((1.0)/in_x)))/ Scale), 2)
    # ratio = (((1.0)/in_originalNotNormalized)/Decrypted_Value111111)

    # Calculating errorDiff_withOrg
    errorDiff_withOrg = sum([pow((abs((1.0 / org_val) - dec_val)), 2) 
                            for org_val, dec_val in zip(in_originalNotNormalized, Decrypted_List11111)])

    # Calculating errorDiff
    errorDiff = sum([pow((abs(dec_val - (1.0 / x_val)) / Scale), 2) 
                     for dec_val, x_val in zip(Decrypted_List11111, in_x)])

    # Calculating ratio
    ratio = sum([(1.0 / org_val) / dec_val 
                 for org_val, dec_val in zip(in_originalNotNormalized, Decrypted_List11111)])



    inversed_list = [1.0 / x for x in in_originalNotNormalized]

    Decrypted_List_inverse = Decrypted_List11111

    # errorDiff_noMSE = ([(abs(dec_val - (1.0 / x_val)) / Scale) for dec_val, x_val in zip(Decrypted_List11111, in_originalNotNormalized)])

    # print(inversed_list)
    # print(Decrypted_List_inverse)

    errorDiff_noMSE = [abs(a - b) for a, b in zip(inversed_list, Decrypted_List_inverse)]

    # print(errorDiff_noMSE)

    # Converting results to numpy arrays (optional, if needed)
    errorDiff_withOrg = np.array(errorDiff_withOrg)
    errorDiff = np.array(errorDiff)
    ratio = np.array(ratio)

    # errorDiff_noMSE = np.array(errorDiff_noMSE)

    # Printing results
    # print("errorDiff_withOrg:", errorDiff_withOrg)
    # print("errorDiff:", errorDiff)
    # print("ratio:", ratio)

    return InverseX, numberOfTermsComputed, errorDiff_withOrg, errorDiff, ratio, errorDiff_noMSE, Decrypted_List11111



def ErrorCorrection(in_inverse, FinalBestPossibleCoeff, allEncryptedParamsOfInverse, K):
    _r = lambda y: np.round(y, decimals=64)
    y_estimated = FinalBestPossibleCoeff[0]

    # Create a copy of the coefficients to avoid modifying the original
    adjusted_coeffs = FinalBestPossibleCoeff.copy()

    for i in range(1, len(adjusted_coeffs)):
        adjusted_coeffs[i] /= K**(i-1)


    for j in range(1, len(adjusted_coeffs)):

        try:
            value_iter = allEncryptedParamsOfInverse[j-1] * adjusted_coeffs[j]

            HE.rescale_to_next(value_iter)
            ~value_iter

            y_estimated = y_estimated + (value_iter)
        
        except Exception as e:
            # print('exception...', e)
            break

    return y_estimated


def Step1(Normalized_value, Scale, Intercept, min_val_1, max_val_1, normalized_list_normal, in_originalValues):

    _r = lambda y: np.round(y, decimals=64)

    All_Ks = [.4, .5, .6, .7, .8, .9, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20, 25, 30, 35, 40, 50]

    NumberOfTermsTotal = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]


    Normalized_value_ = Normalized_value - 1

    errordiff_All = []
    errordiff1_All = []
    errordiff2_All = []

    for K in All_Ks:
        allEncryptedParams = getEncryptedValues(Normalized_value_, K)

        errordiff_SameK = []
        errordiff1_SameK = []
        errordiff2_SameK = []

        for NumberOfTerms in NumberOfTermsTotal:
            EN_DenomInverse, NumberOfTermsRequired, errorDiff, errorDiff1, errorDiff2, errorDiff3, allInverses = DIV_HE(Normalized_value, NumberOfTerms, K, allEncryptedParams, normalized_list_normal, in_originalValues, Scale)

            errordiff_SameK.append(errorDiff)
            errordiff1_SameK.append(errorDiff1)
            errordiff2_SameK.append(errorDiff2)

        errordiff_All.append(errordiff_SameK)
        errordiff1_All.append(errordiff1_SameK)
        errordiff2_All.append(errordiff2_SameK)

    # Initialize a 2D numpy array to store cumulative errors for each K and number of terms pair
    cumulative_errors = np.zeros((len(All_Ks), len(NumberOfTermsTotal)))
    cumulative_errors1 = np.zeros((len(All_Ks), len(NumberOfTermsTotal)))
    cumulative_errors2 = np.zeros((len(All_Ks), len(NumberOfTermsTotal)))

    # Sum the errors for each K and number of terms pair
    for i in range(len(All_Ks)):
        for j in range(len(NumberOfTermsTotal)):
            cumulative_errors[i][j] = errordiff_All[i][j]
            cumulative_errors1[i][j] = errordiff1_All[i][j]
            cumulative_errors2[i][j] = errordiff2_All[i][j]

    # Print the individual number-wise errors along with the cumulative errors
    # print("Individual number-wise errors and cumulative errors for all K and number of terms pairs:")
    # for i in range(len(All_Ks)):
    #     for j in range(len(NumberOfTermsTotal)):
    #         print(f"K: {All_Ks[i]}, Number of Terms: {NumberOfTermsTotal[j]}")
    #         print(f"  Cumulative Error: {cumulative_errors[i][j]}")
    #         print(f"  Cumulative Error1: {cumulative_errors1[i][j]}")
    #         print(f"  Cumulative Error2: {cumulative_errors2[i][j]}")
    #         print('*******************************************************************************************************')

    # Find the index of the minimum cumulative error
    min_error_index = np.unravel_index(np.argmin(cumulative_errors), cumulative_errors.shape)
    min_error_index1 = np.unravel_index(np.argmin(cumulative_errors1), cumulative_errors1.shape)
    min_error_index2 = np.unravel_index(np.argmin(cumulative_errors2), cumulative_errors2.shape)

    # Extract the K and number of terms that provide the minimum cumulative error
    best_K = All_Ks[min_error_index[0]]
    best_number_of_terms = NumberOfTermsTotal[min_error_index[1]]

    best_K1 = All_Ks[min_error_index1[0]]
    best_number_of_terms1 = NumberOfTermsTotal[min_error_index1[1]]

    best_K2 = All_Ks[min_error_index2[0]]
    best_number_of_terms2 = NumberOfTermsTotal[min_error_index2[1]]

    # # Output the results
    # print(f"\nThe K value that provides the least cumulative error is: {best_K}")
    # print(f"The number of terms that provides the least cumulative error is: {best_number_of_terms}")
    # print(f"The minimum cumulative error is: {cumulative_errors[min_error_index]}")

    # print(f"\nThe K value that provides the least cumulative error1 is: {best_K1}")
    # print(f"The number of terms that provides the least cumulative error1 is: {best_number_of_terms1}")
    # print(f"The minimum cumulative error1 is: {cumulative_errors1[min_error_index1]}")

    # print(f"\nThe K value that provides the least cumulative error2 is: {best_K2}")
    # print(f"The number of terms that provides the least cumulative error2 is: {best_number_of_terms2}")
    # print(f"The minimum cumulative error2 is: {cumulative_errors2[min_error_index2]}")

    return best_K1, best_number_of_terms1


def Step2(Normalized_value, Scale, Intercept, min_val_1, max_val_1, in_k, in_terms, normalized_list_normal, in_originalValues):

    _r = lambda y: np.round(y, decimals=64)

    All_Ks = []
    NumberOfTermsTotal = []

    All_Ks.append(in_k)
    NumberOfTermsTotal.append(in_terms)


    Normalized_value_ = Normalized_value - 1

    errordiff_All = []
    errordiff1_All = []
    errordiff2_All = []

    for K in All_Ks:
        allEncryptedParams = getEncryptedValues(Normalized_value_, K)

        errordiff_SameK = []
        errordiff1_SameK = []
        errordiff2_SameK = []

        for NumberOfTerms in NumberOfTermsTotal:
            EN_DenomInverse, NumberOfTermsRequired, errorDiff, errorDiff1, errorDiff2, errorDiff3, allInverses = DIV_HE(Normalized_value, NumberOfTerms, K, allEncryptedParams, normalized_list_normal, in_originalValues, Scale)

            errordiff_SameK.append(errorDiff)
            errordiff1_SameK.append(errorDiff1)
            errordiff2_SameK.append(errorDiff2)

        errordiff_All.append(errordiff_SameK)
        errordiff1_All.append(errordiff1_SameK)
        errordiff2_All.append(errordiff2_SameK)


    ratio = ([(1.0 / org_val) / dec_val 
                 for org_val, dec_val in zip(normalized_list_normal, allInverses)])

    ratio_list = (np.array(ratio)).tolist()

    # print(normalized_list_normal)
    # print(allInverses)
    # print(ratio_list)


    return normalized_list_normal, errorDiff3



def Step3(Diff_errors, normalized_Values, EN_normalized_Values):

    _r = lambda y: np.round(y, decimals=64)

    # print(Diff_errors)
    # print(normalized_Values)

    Diff_errors1 = [-x for x in Diff_errors]

    Y = np.array(Diff_errors1)
    X = np.array(normalized_Values)

    degrees = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    alpha = 1e-6

    results = []

    for degree in degrees:
        # print(f'\n-------------------------------------------------- poly Fit (degree = {degree}, alpha = {alpha}) ---------------------------------------------------------------\n')
        results.append(PolyFittingSelf(X, Y, degree, alpha, EN_normalized_Values))

    # Find the degree and coefficients with the least MSE
    best_fit = min(results, key=lambda x: x[2])

    # print(f'\nBest fit degree: {best_fit[0]}')
    # print('Coefficients:', best_fit[1])
    # print('MSE:', best_fit[2])

    return best_fit[0], best_fit[1]


def Step4(Normalized_value, Scale, Intercept, min_val_1, max_val_1, in_k, in_terms, FinalBestPossibleCoeff, normalized_list_normal, in_originalValues):

    _r = lambda y: np.round(y, decimals=64)

    All_Ks = [.4, .5, .6, .7, .8, .9, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20, 25, 30, 35, 40, 50]

    K = in_k

    NumberOfTerms = in_terms

    Normalized_value_ = Normalized_value - 1

    allEncryptedParams = getEncryptedValues(Normalized_value_, K)

    EN_DenomInverse, NumberOfTermsRequired, errorDiff, errorDiff1, errorDiff2, errorDiff3, allInverses = DIV_HE(Normalized_value, NumberOfTerms, K, allEncryptedParams, normalized_list_normal, in_originalValues, Scale)


    ratio = ([(1.0 / org_val) / dec_val 
                 for org_val, dec_val in zip(normalized_list_normal, allInverses)])

    ratio_list = (np.array(ratio)).tolist()

    # print(normalized_list_normal)
    # print(allInverses)
    # print(ratio_list)

    total_errorCorrection_error = []

    finalInverses = []

    for K_correction in All_Ks:

        allEncryptedParamsOfInverse = getEncryptedValues(Normalized_value, K_correction)

        FinalInverse_error = ErrorCorrection(EN_DenomInverse, FinalBestPossibleCoeff, allEncryptedParamsOfInverse, K_correction)

        final_inverse = EN_DenomInverse + FinalInverse_error

        FinalInverse_decryted1  = HE.decryptFrac(final_inverse)
        finalInverses = _r(FinalInverse_decryted1)

        ratio = ([ pow(abs( 1.0 - ((1.0 / org_val) / dec_val)), 2) for org_val, dec_val in zip(in_originalValues, finalInverses)])

        ratio_list = (np.array(ratio)).tolist()

        total_errorCorrection_error.append(sum(ratio_list))

    
        for i in range(0,len(in_originalValues)):
            
            Original_value = in_originalValues[i]

            Normalized_value_v = normalized_list_normal[i]

            normalized_Inverse_Original = ((1.0)/Normalized_value_v)

            normalized_inverse_CKKS = allInverses[i]

            original_inverse_value = ((1.0)/Original_value)

            ComputedInverse_value = finalInverses[i]

            ErrorForNormalized = abs(normalized_Inverse_Original/normalized_inverse_CKKS)

            ErrorForOriginalValue = abs(original_inverse_value/ComputedInverse_value)


            # print("***********************************************************************")
            
            # print("K_Correction           : ", K_correction)

            # print("Value of Input         : ", Original_value)

            # print("Value of Norma Input   : ", Normalized_value_v)
            
            # print("Original Inverse of X' : ", normalized_Inverse_Original)
            
            # print("CKKS Inverse of X'     : ", normalized_inverse_CKKS)

            # print("Error Original vs CKKS : ", ErrorForNormalized)

            # print("Original Inverse       : ", original_inverse_value)
            
            # print("CKKS Inverse           : ", ComputedInverse_value)
            
            # print("Error Original vs CKKS : ", ErrorForOriginalValue)


            # print("***********************************************************************")







    min_error_index = np.argmin(total_errorCorrection_error)
    best_K_correction = All_Ks[min_error_index]
    min_error_value = total_errorCorrection_error[min_error_index]

    # Print the sum of errors for each K_correction
    # print("Sum of errors for each K:")
    # for idx, k_value in enumerate(All_Ks):
    #     print(f"K = {k_value}: Sum of Errors = {total_errorCorrection_error[idx]}")

    # # Output the best K_correction
    # print(f"\nBest K with the least error: K = {best_K_correction}, with Sum of Errors = {min_error_value}")


    allEncryptedParamsOfInverse = getEncryptedValues(Normalized_value, best_K_correction)

    FinalInverse_error = ErrorCorrection(EN_DenomInverse, FinalBestPossibleCoeff, allEncryptedParamsOfInverse, best_K_correction)

    final_inverse = EN_DenomInverse + FinalInverse_error

    FinalInverse_decryted1  = HE.decryptFrac(final_inverse)
    finalInverses = _r(FinalInverse_decryted1)

    finalInverses = finalInverses[:1000]

    allOriginalInverses = [(1.0/x) for x in in_originalValues]

    mse = np.mean((np.array(allOriginalInverses) - np.array(finalInverses)) ** 2)

    ratio = ([(abs(( org_val/ dec_val))) for org_val, dec_val in zip(allOriginalInverses, finalInverses)])

    print(ratio)

    return best_K_correction, min_error_value, mse


def SubMainFunction(Scale, Intercept, filename):


    start_time = time.time()

    min_val_1 = 105000000
    max_val_1 = 105000753


    data = np.load(Path("ParameterSelection") / "Consumer" / "generated_sets" / "set1-1.npy", allow_pickle=False)


    X111111_1 = data.tolist()

    min_val_1 *= 0.95
    max_val_1 /= 0.95

    normalized_list = []

    for value in X111111_1:
        Normalized_value_normal = (Scale * (value - min_val_1) / (max_val_1 - min_val_1)) + Intercept
        normalized_list.append(Normalized_value_normal)


    Price1 = normalized_list
    Price2 = np.array(Price1, dtype=np.float64)
    Price3 = HE.encodeFrac(Price2)
    Normalized_value = HE.encryptPtxt(Price3)

    # print('*************************************** Step 1 Start *****************************************')

    bestK, bestNumberOfTerms = Step1(Normalized_value, Scale, Intercept, min_val_1, max_val_1, normalized_list, X111111_1)

    # print('*************************************** Step 1 End *****************************************')


    data = np.load(Path("ParameterSelection") / "Consumer" / "generated_sets" / "set1-2.npy", allow_pickle=False)

    X111111_1 = data.tolist()

    normalized_list = []

    for value in X111111_1:
        Normalized_value_normal = (Scale * (value - min_val_1) / (max_val_1 - min_val_1)) + Intercept
        normalized_list.append(Normalized_value_normal)


    Price1 = normalized_list
    Price2 = np.array(Price1, dtype=np.float64)
    Price3 = HE.encodeFrac(Price2)
    Normalized_value = HE.encryptPtxt(Price3)


    # print('*************************************** Step 2 Start *****************************************')

    normalized_Values, Diff_errors = Step2(Normalized_value, Scale, Intercept, min_val_1, max_val_1, bestK, bestNumberOfTerms, normalized_list, X111111_1)

    # print('*************************************** Step 2 End *****************************************')

    # print('*************************************** Step 3 Start *****************************************')

    degree, coffs = Step3(Diff_errors, normalized_Values, Normalized_value)

    # print('*************************************** Step 3 End *****************************************')

    data = np.load(Path("ParameterSelection") / "Consumer" / "generated_sets" / "set1-3.npy", allow_pickle=False)

    X111111_1 = data.tolist()

    normalized_list = []

    for value in X111111_1:
        Normalized_value_normal = (Scale * (value - min_val_1) / (max_val_1 - min_val_1)) + Intercept
        normalized_list.append(Normalized_value_normal)


    Price1 = normalized_list
    Price2 = np.array(Price1, dtype=np.float64)
    Price3 = HE.encodeFrac(Price2)
    Normalized_value = HE.encryptPtxt(Price3)

    # print('*************************************** Step 4 Start *****************************************')

    best_K_correction, min_error_value, mse = Step4(Normalized_value, Scale, Intercept, min_val_1, max_val_1, bestK, bestNumberOfTerms, coffs, normalized_list, X111111_1)

    # print('*************************************** Step 4 End *****************************************')

    end_time = time.time()

    elapsed_time = end_time - start_time

    output_string = f"{bestK}, {bestNumberOfTerms}, {degree}, {coffs}, {best_K_correction}, {min_error_value}, {mse}\n"

    # 50, 12, 3, [-2.5021503699567322, 0.927674109467529, 1.7187621077868473, -1.1468652106209127], 2, 0.0003673004506857542, 3.3355761426558514e-23

    with open(filename, 'a') as file:
        file.write(output_string)
        file.write('\n')

    return min_error_value


def main():

    _r = lambda y: np.round(y, decimals=64)

    intercepts = [0.50, 0.60, 0.70, 0.80, 0.90]

    scales_per_intercept = {
        0.50: [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.80],
        0.60: [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.80],
        0.70: [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40],
        0.80: [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40],
        0.90: [0.05, 0.10, 0.15, 0.20]
    }

    results = []

    for intercept in intercepts:
        for scale in scales_per_intercept[intercept]:
            adj_intercept = intercept - (scale / 2.0)
            filename = f'Consumer_TAYLOR_output_{intercept}_{scale}.txt'

            all_errors = []

            for i in range(30):
                error = SubMainFunction(scale, adj_intercept, filename)
                all_errors.append(error)

            mean = np.mean(all_errors)
            stddev = np.std(all_errors)
            min_error = np.min(all_errors)

            results.append({
                'intercept': intercept,
                'scale': scale,
                'adjusted_intercept': adj_intercept,
                'mean_error': mean,
                'stddev': stddev,
                'min_error': min_error,
            })

            print(f"Finished: Intercept={intercept}, Scale={scale}, Mean Error={mean}, Min Error={min_error}, Std Dev.={stddev}")

    best = min(results, key=lambda x: x['min_error'])

    print("\n=== Best Configuration based on Min Error===")
    for k, v in best.items():
        print(f"{k}: {v}")

    best1 = min(results, key=lambda x: x['mean_error'])

    print("\n=== Best Configuration based on Mean Error ===")
    for k, v in best1.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()

