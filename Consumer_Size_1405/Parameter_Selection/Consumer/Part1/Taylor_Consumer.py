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

    min_val_1 = 29505.0     #min(X1)
    max_val_1 = 30261.98798171424      #max(X1)


    X111111_1 = [29505.83176651079, 29507.33657153264, 29507.43557289929, 29510.61039351077, 29511.47457971253, 29513.95524728368, 29513.958218267402, 29514.352599508446, 29515.16662132623, 29515.612887405117, 29517.505593258113, 29517.536631466344, 29518.136958577154, 29518.179368705143, 29518.536214620686, 29525.570489424685, 29525.74726455694, 29525.87552268137, 29527.168377621485, 29527.364506789647, 29527.599695641544, 29527.983926993933, 29528.146738273073, 29528.64183948179, 29529.14059447351, 29531.019256784268, 29533.124893300886, 29533.645518585443, 29533.90474943732, 29534.023576530548, 29534.131191746394, 29536.574871471046, 29536.76137907452, 29538.226152114494, 29538.232213631487, 29538.278996405956, 29538.42099216345, 29539.004996903972, 29540.49051840946, 29541.164848691555, 29541.24415634381, 29543.434063852874, 29544.27267308167, 29545.10688507292, 29545.232491125294, 29546.227696726863, 29547.629959867732, 29548.548784501232, 29550.537612228476, 29550.86641431989, 29551.867659276126, 29551.87730421143, 29553.305775539637, 29555.353092717392, 29555.518447447997, 29557.08141013196, 29557.189403797292, 29559.737538590252, 29559.796344985138, 29560.305596109647, 29561.480341147362, 29562.758438717367, 29564.012770919297, 29564.289478465867, 29564.613622537643, 29564.73205165507, 29564.740763391404, 29565.807094409356, 29565.909267097242, 29566.054842524452, 29566.361675022512, 29567.414391955503, 29567.45005286397, 29568.32216422642, 29568.424584045064, 29568.477854826204, 29568.561162681613, 29568.88352910096, 29570.632387228834, 29570.949318801748, 29572.68503372603, 29572.830455303712, 29573.530245593633, 29574.917913343485, 29575.670474412553, 29576.611748138475, 29576.759355506256, 29576.77908251752, 29577.13338415554, 29577.684321865527, 29577.68974094171, 29577.92110449205, 29578.26434159246, 29578.71830381949, 29581.173525466795, 29581.89865319097, 29582.35320635075, 29582.913886104525, 29584.199862133464, 29584.47477854782, 29586.624962144186, 29586.930503348118, 29587.111914652753, 29587.40263582995, 29588.490428791945, 29588.555723675512, 29589.282473522366, 29589.369264833917, 29590.982240125955, 29591.17895825879, 29591.758335558126, 29593.070297304068, 29593.567810152177, 29593.625436903236, 29593.97785563201, 29594.575147639494, 29595.225530284282, 29595.65996388293, 29595.87843375115, 29598.108810921643, 29599.858169344556, 29600.10655507312, 29600.387151647228, 29601.303356240307, 29601.42399243181, 29602.9439357757, 29603.4328134453, 29604.834822121178, 29605.831943258065, 29606.429733612596, 29606.638501881844, 29608.715316868813, 29608.78398823579, 29608.987227610414, 29609.72746259127, 29610.250838674037, 29610.545553790886, 29610.881637659455, 29611.050537680097, 29611.71109471582, 29612.76338406898, 29614.664688754423, 29614.99204285844, 29615.330094436256, 29617.059203607227, 29618.787588973886, 29619.18004621033, 29619.741356210245, 29619.86060223508, 29619.89584569133, 29620.743860351766, 29621.035227128887, 29621.936368506293, 29623.268470160918, 29623.331176159714, 29624.15614884604, 29624.399008872988, 29625.06116576536, 29626.11476634226, 29627.42153970699, 29627.504344278328, 29627.52599363751, 29629.69916155052, 29631.23053211607, 29631.42563001717, 29632.321510888036, 29633.311061689245, 29634.570682454643, 29634.722161798225, 29634.790596228893, 29635.080137295252, 29635.124421556517, 29635.68607958882, 29635.856738406324, 29636.555784341173, 29636.6273096909, 29639.062428866062, 29640.358287616487, 29641.874367404205, 29642.598214865884, 29642.823804688476, 29643.754586077168, 29644.373012116674, 29644.57852352833, 29645.279140302882, 29645.64986093, 29646.12462508836, 29646.329295417454, 29646.977136094898, 29647.373160835752, 29647.912629363836, 29648.277137259094, 29649.423520501103, 29649.49742338227, 29650.507700848502, 29651.316076859723, 29654.176657626493, 29654.42970011428, 29654.460074395298, 29654.93977625761, 29655.572991259432, 29656.48266834666, 29658.9078119159, 29659.805424330974, 29661.931508158144, 29664.017050908613, 29664.89795626946, 29666.241026461477, 29667.672132582742, 29668.216241852107, 29668.28633426214, 29668.454034671187, 29668.543654792345, 29668.92970818781, 29669.592302407244, 29672.24297861304, 29674.264195560267, 29675.476301001818, 29675.927532420068, 29676.020756933758, 29676.378944900378, 29676.592569786244, 29677.442230147484, 29678.707074565944, 29679.812463921386, 29680.487518929942, 29680.646399826124, 29680.844885952523, 29681.403638775522, 29682.16951622832, 29682.55917549582, 29682.8129053828, 29683.04491260263, 29683.390815246697, 29684.21275461853, 29687.002746676197, 29688.26205747681, 29688.595467617062, 29688.697053834585, 29689.53468061213, 29690.095074089146, 29690.98500284245, 29693.23247381514, 29693.46771115688, 29694.127122316804, 29694.717654502652, 29696.670256143272, 29697.62431162195, 29698.75434507219, 29699.376696699197, 29699.813008667013, 29699.9831366684, 29700.314417515998, 29700.54151575476, 29701.245850997548, 29701.516478959955, 29701.736365607154, 29702.48403467011, 29703.672953824942, 29704.33743476131, 29705.996017500816, 29707.180071477982, 29708.295381220632, 29709.11138089253, 29709.70116766402, 29710.03322942975, 29710.203701081726, 29710.38765751806, 29710.86367514099, 29712.262009274997, 29712.612650781226, 29713.01313362235, 29713.139501153706, 29713.28894578098, 29714.604201274426, 29715.35891734511, 29715.857720867527, 29715.906318149107, 29716.799911990427, 29717.07453248399, 29718.018332538504, 29718.31726431612, 29718.955575706084, 29719.400231367214, 29720.02898026788, 29720.36151197406, 29722.05749525925, 29723.213698487147, 29723.87354498802, 29724.56885787544, 29725.207655944123, 29726.03502533877, 29727.00433963152, 29727.271688411616, 29727.451171415694, 29727.592814445798, 29727.80451173053, 29728.92370153345, 29729.278612422047, 29729.299024924894, 29729.43595879034, 29729.672879413327, 29731.93239799669, 29732.284629081743, 29733.18159679303, 29734.664953129148, 29737.373312975134, 29739.15729894759, 29739.969192897326, 29740.550450147206, 29741.791160382734, 29741.8602993983, 29742.99395930372, 29745.493916670395, 29746.81840833121, 29747.89985943898, 29747.968644544068, 29748.928985912647, 29749.255296947736, 29749.304422223155, 29749.318106170653, 29749.595551733008, 29750.231340142935, 29750.397127302982, 29750.858361935207, 29751.72419956506, 29751.86418312469, 29752.436547020978, 29752.523837369474, 29752.571484988264, 29753.732068691603, 29754.237023197536, 29754.505972762767, 29755.585605587694, 29757.584667272877, 29759.20575871778, 29759.54573902678, 29761.03540754653, 29761.902121596664, 29763.18501011547, 29766.541501887714, 29766.75023095527, 29766.80818265802, 29766.962775592485, 29767.90282566903, 29768.0920402516, 29768.372656190513, 29768.64662016269, 29768.71982556518, 29768.92570590891, 29768.98101496997, 29769.818706546706, 29770.420781577654, 29771.208897699144, 29772.66568175464, 29772.79780483793, 29772.92032352228, 29774.00760293628, 29774.38618643692, 29774.58859778914, 29774.74130678969, 29775.756696880002, 29776.35605906744, 29776.66037996877, 29776.756548644036, 29777.392444622492, 29779.152435743403, 29779.56056678924, 29779.9110920258, 29780.316700416948, 29780.6612113713, 29781.353610512502, 29784.594687887944, 29785.730001399712, 29786.87269747734, 29786.902458788223, 29786.965256401127, 29788.478349534667, 29789.73937542943, 29789.868303833162, 29790.345914132617, 29791.973305452342, 29792.900729532208, 29793.24575536644, 29793.517229364807, 29795.914636341666, 29796.060949935472, 29797.145087083733, 29797.151753245915, 29798.658759303704, 29799.18253041721, 29799.65862786315, 29799.660208295103, 29801.708874894448, 29801.744478466055, 29802.69511172786, 29805.50334368444, 29806.00512386011, 29806.39880365029, 29806.41170009383, 29806.41407180355, 29807.481921269162, 29808.396116661894, 29809.089914200835, 29809.35952769393, 29811.203024256338, 29811.783959366392, 29811.888425227982, 29812.44036105998, 29813.456054493814, 29813.581137459674, 29814.354225921812, 29814.756688580972, 29815.664052157448, 29815.83409058701, 29816.428466527464, 29818.675931786453, 29818.780190074664, 29819.047239622207, 29819.82200771969, 29820.113745196802, 29821.17906772795, 29821.299270397805, 29822.739196274262, 29824.746971668596, 29825.68099299142, 29826.13902742027, 29827.896951827173, 29830.973851556002, 29830.99976009705, 29832.768493013526, 29833.046000180897, 29835.116636061393, 29836.22303408077, 29836.85729237663, 29839.08446139655, 29839.377134293754, 29840.51903679962, 29840.75205329892, 29840.75680936235, 29841.905674200476, 29842.485459939642, 29843.63440681974, 29844.28031411216, 29846.38839802098, 29847.329696888723, 29847.544922981768, 29849.049087165797, 29850.48447052892, 29850.542637094706, 29850.680453623856, 29850.868163938394, 29852.10840180962, 29853.956792902874, 29854.420727572688, 29856.788110803856, 29856.900627577856, 29857.597049020034, 29858.54936867057, 29860.826533961826, 29861.25607443316, 29861.394476990867, 29863.254248097135, 29864.949444138136, 29865.001998044838, 29867.876510476588, 29868.609421459474, 29869.067696362734, 29869.802568842133, 29872.35931252888, 29874.00351767591, 29875.674117246763, 29875.719057712005, 29876.3548941372, 29876.600683873672, 29876.879844523075, 29876.900299403107, 29877.192357479456, 29878.685293558545, 29880.316591501865, 29880.61483749345, 29881.991946981114, 29885.314171358055, 29885.3973718081, 29887.115208144296, 29888.06269808568, 29888.249458245173, 29888.463314689314, 29889.1143148581, 29889.696127041745, 29889.933706178123, 29890.30177894884, 29890.668824893975, 29890.748246388393, 29891.163815111864, 29891.82431357849, 29892.549753480547, 29892.946520116708, 29898.65831757747, 29898.913962090464, 29900.869009077793, 29903.033571860822, 29903.363380571333, 29903.461264689566, 29903.62229341115, 29903.665525129312, 29905.172214160535, 29905.526693377153, 29906.536625754823, 29908.280480786656, 29909.765696387454, 29909.852075537587, 29910.952036269817, 29911.316598972066, 29911.31672335364, 29911.403123047916, 29912.4399918061, 29912.892394053386, 29913.300952627345, 29913.61054330096, 29913.998101382207, 29914.145773596683, 29914.358739818566, 29915.74833633266, 29917.216388043256, 29917.24885591131, 29917.757052225053, 29919.2648439213, 29921.52943378482, 29921.656626752923, 29922.89753542926, 29924.1392615414, 29924.341440877513, 29924.9854834632, 29925.4802243302, 29925.83756298928, 29927.319838224535, 29928.80650352138, 29929.56504656295, 29929.61316513288, 29932.00222055703, 29934.750295020214, 29934.97512962106, 29935.25835016483, 29935.31891958964, 29935.736326822484, 29935.88283123271, 29936.24737743141, 29937.013518446933, 29937.510851197447, 29938.92640786481, 29939.685247086567, 29940.217810204933, 29940.41833640664, 29941.382183278845, 29944.704598297725, 29948.010518419887, 29949.69297394369, 29950.394815408945, 29951.159620946335, 29951.475390636653, 29953.107101240144, 29953.184567871995, 29954.235556562573, 29956.83546580221, 29957.238560855352, 29957.408333059037, 29957.885855159646, 29958.75839056334, 29960.021774070112, 29961.24532648215, 29961.82240098204, 29961.926889656854, 29962.95724557221, 29964.445692697824, 29965.147823939973, 29965.27343425503, 29966.21522605837, 29966.326726449795, 29966.532262276804, 29967.1616619902, 29967.74195357559, 29969.07800955412, 29969.574291382367, 29970.638083660066, 29970.641635467844, 29970.80393229869, 29973.01606453344, 29974.033956803833, 29974.877910287345, 29975.586208532142, 29975.723939490083, 29976.735823968538, 29978.443073607938, 29978.686681513565, 29979.34771982959, 29979.3975520509, 29979.41922317023, 29979.759346605268, 29981.80693373036, 29982.415611877077, 29982.702742740403, 29982.823762207903, 29983.242679885458, 29983.958261890548, 29984.80904062505, 29986.602519324733, 29987.429505239994, 29987.499198386628, 29987.58797062237, 29988.157490193385, 29989.10764834806, 29989.953623292207, 29990.398320946137, 29990.907000085663, 29992.386007124067, 29992.722367130133, 29994.400244016615, 29994.874308008137, 29995.109885270358, 29995.196964358034, 29995.20401508069, 29995.44517460989, 29998.39911723171, 29999.282523723436, 29999.65438627555, 30001.608019597432, 30001.75233958421, 30002.2211903458, 30002.570757208257, 30002.77291776425, 30002.825712966212, 30003.499231689704, 30003.888302657033, 30004.88496480553, 30004.964469338356, 30005.25813397288, 30006.99397419476, 30008.27900861533, 30008.424946589068, 30008.663878481773, 30009.154184505674, 30010.611457706837, 30013.920107214406, 30015.047421296367, 30016.631450285426, 30016.715859367734, 30017.95933562906, 30019.488831314025, 30020.786578124724, 30020.906829987733, 30022.15696256711, 30022.33737715455, 30023.605116330084, 30023.92785558996, 30024.101693119483, 30024.64273933592, 30024.90709915463, 30026.08806232371, 30026.34121749938, 30027.129573945876, 30027.228678593307, 30027.274876491792, 30027.499887218437, 30028.02757407914, 30028.1217410526, 30028.47597781506, 30028.64546978495, 30030.165366519857, 30030.44061792415, 30030.753060210485, 30031.931874219783, 30032.109350984, 30032.202815336525, 30032.555891074477, 30033.87360778579, 30034.03460234868, 30034.34544586126, 30035.298654128193, 30035.90455339, 30037.401409090442, 30038.024108513513, 30038.801774258583, 30039.9628358171, 30040.08118340693, 30040.565806711176, 30041.332915735195, 30041.348592175455, 30041.583913515886, 30041.761750266094, 30042.505273186005, 30043.04957709924, 30044.35858285474, 30045.261437196354, 30046.91044958712, 30047.270104450992, 30047.338692464087, 30047.69411783748, 30047.81410323132, 30047.9263901737, 30048.603638816785, 30050.73587713065, 30051.498430934513, 30051.717013955018, 30051.831689924496, 30051.986000196077, 30052.27494617294, 30052.323925487777, 30053.299864629997, 30053.5974734754, 30053.827953896194, 30055.22123425, 30058.053566349543, 30058.20476863449, 30059.262304580872, 30060.487823423962, 30062.017241947724, 30062.54774543925, 30063.52500294408, 30063.71528364212, 30064.06723115499, 30064.438496173236, 30064.862583562837, 30065.488195957987, 30065.629127495078, 30065.823005000206, 30066.497811782036, 30066.649155650655, 30067.214226682092, 30067.74566827295, 30068.031105755843, 30068.17780329223, 30068.478196284526, 30068.56633476422, 30069.725993116102, 30071.29637619362, 30071.473475676874, 30071.507192262176, 30071.767243067086, 30071.822512381714, 30072.693550723983, 30072.837079778063, 30073.34436080242, 30073.43660748151, 30074.197552639012, 30074.34228306577, 30075.483904401062, 30076.06244008618, 30077.809638641636, 30077.865057056257, 30078.835852995217, 30080.468929460752, 30080.79244209551, 30081.774154877516, 30082.050407274284, 30083.89472835561, 30084.04042343341, 30084.553179219158, 30085.292893903097, 30086.253115692347, 30087.72826490816, 30087.783152278986, 30088.908916933826, 30089.26986972524, 30089.420215547143, 30090.23916108814, 30091.109488645536, 30091.334231807505, 30091.567586357112, 30091.587885651566, 30091.772333486926, 30093.23815798906, 30093.66756959525, 30093.818805711882, 30094.13218190572, 30094.60659460685, 30095.837625825417, 30095.9509351067, 30096.260735981305, 30097.01601958649, 30097.563897621243, 30098.193253172187, 30098.82747951754, 30099.452727088497, 30099.586352617567, 30101.593544749943, 30102.2305392279, 30103.314011250386, 30105.60296824432, 30105.786401349927, 30106.02985557855, 30106.490494483784, 30106.94867973635, 30107.630536486566, 30108.968464861468, 30110.20087998083, 30110.80907529086, 30111.60419694332, 30111.96322759593, 30113.623625678334, 30114.349432358074, 30114.608218404, 30114.771866654704, 30115.056768866823, 30115.462978926324, 30115.46775541022, 30115.939245955124, 30117.2979612511, 30117.695697399762, 30118.651476766558, 30118.756927816758, 30118.77529236019, 30119.33740890638, 30120.408536804458, 30121.597825403005, 30122.360223540607, 30123.128826249886, 30124.86144880212, 30125.29904421834, 30126.022430535613, 30126.781512225287, 30126.85442161104, 30127.76525131833, 30128.37890908947, 30130.55977273127, 30130.681552350423, 30131.18714210075, 30131.451703685412, 30131.490697682064, 30131.523830246166, 30131.810695204622, 30131.92185258403, 30131.982964809704, 30132.03333561038, 30132.4533705225, 30135.27859166573, 30135.784957048858, 30135.938180244135, 30136.55094774412, 30136.69968368193, 30138.02374925913, 30140.1973927221, 30140.89146441784, 30140.957941100813, 30140.99387696445, 30141.684446139352, 30142.91646905868, 30145.038111886537, 30145.990854993, 30146.281834290698, 30146.787497979287, 30147.8267691887, 30148.697234117888, 30149.16720220145, 30150.305308107967, 30150.574799481943, 30151.223269264563, 30151.551007569076, 30152.40135324989, 30152.629236330555, 30154.014424017867, 30154.36953701082, 30154.464776004956, 30154.634671542248, 30155.86880306391, 30156.237943803506, 30156.988780787964, 30157.192017145015, 30157.567606244567, 30157.771273896586, 30158.09357948621, 30158.15578530243, 30158.864226681773, 30158.94660397353, 30159.33338763367, 30160.58085780938, 30161.760452947252, 30162.658644011604, 30163.548074497376, 30164.007482118257, 30164.321991181652, 30164.564730883867, 30170.44579229273, 30171.410584925365, 30171.686100830513, 30171.742079898147, 30171.85602111624, 30172.496016169647, 30174.64718998206, 30176.720495281483, 30177.988363579516, 30178.835365419298, 30178.93154632258, 30181.24425188412, 30181.53728127347, 30182.579125203665, 30182.98768756467, 30183.33543699939, 30183.897150005065, 30183.984474301957, 30184.90816105908, 30185.570491576567, 30186.062462828155, 30188.292455220573, 30190.397589549062, 30191.116410831506, 30191.26205194716, 30191.543590338035, 30191.628177305905, 30192.09954891284, 30194.91175907933, 30198.406088882042, 30198.952620899287, 30199.43002895084, 30199.487904297213, 30199.568548328894, 30199.680773399283, 30200.377498624755, 30201.124745721587, 30202.39367551783, 30202.580001961884, 30202.80510078901, 30202.876527909437, 30203.320429926767, 30203.646807094647, 30204.383200512428, 30206.883908680153, 30207.097343813683, 30207.205011175163, 30208.187937893013, 30208.769240061505, 30209.558616341517, 30210.01254871261, 30210.183155340237, 30210.697023183176, 30210.79226117638, 30211.335915013533, 30211.345720870046, 30211.70101817276, 30211.747752973126, 30213.739483478203, 30214.37790005515, 30214.96690669119, 30215.08666810968, 30216.27207313349, 30216.56324157958, 30216.748559395182, 30219.3792455749, 30219.537782821648, 30219.804208639933, 30219.995767066128, 30220.618150617607, 30221.82651999667, 30222.884374031833, 30223.241065508202, 30223.526236052952, 30223.534692552174, 30224.502173185825, 30225.976111375498, 30226.207968966533, 30229.033062471055, 30229.072815557036, 30229.995112508863, 30230.044156559667, 30230.061873642288, 30231.96040347035, 30231.98025712697, 30232.559680672584, 30233.030329392255, 30233.514042279377, 30233.604060795937, 30233.64914913548, 30237.936109998514, 30238.977892347848, 30242.732671576814, 30242.901335720646, 30243.69917616169, 30245.669107482914, 30246.63745978479, 30247.114765913873, 30248.17326661559, 30248.31483848667, 30248.842510446742, 30248.931430749148, 30250.175860001043, 30250.71473694739, 30251.044210450833, 30251.375644310952, 30251.45167679106, 30251.747980974735, 30252.020103639185, 30252.278581454026, 30252.57523618185, 30253.661381665683, 30254.35139794535, 30257.441988784212, 30257.49739912508, 30257.856725420257, 30258.48668604269, 30261.91365584451]

    min_val_1 *= 0.95
    max_val_1 /= 0.95

    if(max_val_1 > 99999):
        max_val_1 = 99999


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

    # random_floats = list(np.random.uniform(min_val_1, max_val_1, 70))
    # X111111_1 = sorted(random_floats)

    X111111_1 = [29505.529413247972, 29506.93048064106, 29507.432748658306, 29509.265261910667, 29509.74287419493, 29510.330101825988, 29510.43056392098, 29510.776335536604, 29511.009799022886, 29511.145188364953, 29514.902452636306, 29516.790315451126, 29517.82156832211, 29518.162947663277, 29518.78740645031, 29519.270628565275, 29520.68608193243, 29522.248016679878, 29522.33121675391, 29522.535772611358, 29522.624338676935, 29525.729620909322, 29525.95260268193, 29527.420753394144, 29528.725558441045, 29528.868889294936, 29530.022293832586, 29530.284742695865, 29531.566959135365, 29535.081524025023, 29536.102840100455, 29536.372813441794, 29536.670713479394, 29538.39840356732, 29538.848625316794, 29539.36997480695, 29539.797125992794, 29540.01595716233, 29540.04523841869, 29540.133284657793, 29540.221933817567, 29541.18744285064, 29541.206928231957, 29541.695043163592, 29542.377535455045, 29544.006697984205, 29544.1667498119, 29544.36479765491, 29544.414404995296, 29546.82764872228, 29547.7665964329, 29547.960361190904, 29548.21502246625, 29549.153209639335, 29549.35532896892, 29549.47195332059, 29549.678770095965, 29549.897201825588, 29551.386029978272, 29551.533006989695, 29552.272794277065, 29553.221264934793, 29553.532477903336, 29553.58565746353, 29554.152123705884, 29554.517049629907, 29557.140080186164, 29557.508715489494, 29557.567140800165, 29557.570661699934, 29558.095896584964, 29558.19480966924, 29559.01263182434, 29559.969962539275, 29560.39949230502, 29561.756948681832, 29562.469025649207, 29563.50823645219, 29565.201592603993, 29567.731989428765, 29568.367796597184, 29569.25578039707, 29569.453782852244, 29571.78798558258, 29573.34741733316, 29574.512188179517, 29574.883829679435, 29576.113193585552, 29576.976536588933, 29577.492613174487, 29577.511805937982, 29579.49774547095, 29580.781960443197, 29581.472291814243, 29582.256346153525, 29582.468628616352, 29583.194718684495, 29583.29596285488, 29585.214034171997, 29587.763001218573, 29588.483932406118, 29588.596481711797, 29588.7463294089, 29589.14333757618, 29589.50912139401, 29590.924079882552, 29591.97004626341, 29592.962601509254, 29593.36844756771, 29593.581907891785, 29593.93920616597, 29593.96707531869, 29595.412211820654, 29596.063798369163, 29596.282365318428, 29597.13708662633, 29597.564939807, 29599.32224213847, 29599.374052213112, 29600.753247223427, 29602.2800857651, 29602.35896816225, 29605.849675247773, 29606.185496395818, 29606.362815227792, 29606.99491147527, 29607.099810673222, 29608.127788552898, 29608.932370062874, 29610.208717155274, 29610.21130934115, 29610.80658219118, 29611.136563307966, 29611.755822217732, 29617.212527581873, 29617.714416695195, 29620.485562411315, 29621.415495147925, 29623.612842118815, 29623.744905455198, 29624.37926408666, 29624.94178808028, 29625.88076330012, 29626.17184802044, 29627.66704443749, 29629.79670386508, 29631.85564082037, 29632.60114892299, 29633.48570312736, 29635.12625819939, 29635.98862421663, 29636.83042577647, 29637.641653688665, 29638.97970097336, 29639.73266627757, 29642.099454515857, 29642.13955101821, 29642.74722446532, 29643.10259062667, 29643.458700119758, 29643.656016457, 29643.942005734214, 29644.308230197166, 29644.391264055917, 29645.386752267503, 29647.08065537946, 29647.502051018462, 29647.592735514645, 29648.04199089788, 29648.523164583272, 29648.569016819143, 29649.115255172193, 29650.00371517038, 29650.268197681635, 29650.411136555722, 29650.51129059253, 29650.53006349854, 29651.068487946326, 29651.594438081025, 29651.861961564195, 29652.280377359333, 29652.56171768678, 29653.93433224726, 29654.0306655168, 29654.118642773614, 29654.31046586957, 29654.67829675932, 29655.20681667831, 29655.869872714302, 29656.087382290785, 29656.351036010437, 29656.357275282135, 29656.38214924499, 29656.667506528138, 29657.430395287916, 29658.500755176286, 29658.73494030366, 29658.941127760947, 29659.608812503764, 29660.340128466778, 29660.701546908644, 29661.85544017152, 29662.0795597113, 29663.674831446748, 29664.407564389938, 29664.46581992409, 29664.769475550085, 29665.032836701183, 29665.21981210186, 29665.878656979035, 29666.615326132476, 29666.908606324774, 29667.63001707083, 29668.282826085655, 29671.319872270422, 29671.378317186198, 29671.754569280383, 29672.316133532757, 29673.54422224614, 29673.83226335877, 29676.219235560224, 29676.933630148244, 29677.529450622304, 29677.602762152277, 29678.210618686804, 29678.67941452174, 29679.927102793445, 29680.008726634747, 29680.437436922966, 29680.45080072666, 29680.583246053164, 29681.83968475118, 29684.58735417179, 29685.121382268837, 29686.675093864193, 29686.945801356625, 29687.994425551216, 29688.273174714315, 29688.35897015214, 29688.85143327893, 29689.967336095477, 29690.044431433846, 29691.243095803766, 29692.051552356832, 29692.816707313756, 29692.946811201262, 29693.17901973726, 29693.32406308487, 29695.13283772241, 29695.235035020432, 29695.63298210928, 29695.868702276974, 29696.26840714283, 29696.811420034675, 29697.80957034719, 29698.393081489958, 29699.92527454458, 29703.49184307272, 29703.764767614593, 29704.03158608124, 29704.77627180476, 29705.374965542145, 29708.307024393045, 29708.362940453884, 29708.82675450904, 29709.904787404335, 29710.14779030639, 29710.17156987299, 29710.416560534555, 29710.549116042337, 29710.8087266096, 29711.322863142883, 29716.10610542169, 29716.155525662325, 29716.972360265918, 29717.024631758293, 29718.783361390997, 29719.52554286626, 29719.997822599464, 29720.34706890014, 29720.650916145507, 29720.880011741952, 29720.906422569944, 29720.9872248577, 29721.06140792503, 29721.396755505775, 29723.32185972518, 29724.30431456059, 29725.16748453687, 29725.704466002375, 29726.049264469762, 29727.346295741863, 29728.389487229204, 29729.02316667964, 29730.417565330103, 29730.9458626949, 29731.90187063074, 29732.11607582727, 29732.50537768203, 29732.872001495994, 29733.258885550054, 29733.49150618101, 29734.047716302925, 29734.21566878314, 29734.821391139263, 29736.661477371887, 29736.947765726334, 29737.419574074156, 29738.183086868834, 29738.777045552724, 29740.975702896583, 29741.393066350345, 29741.872009914397, 29743.274471517438, 29744.275072694156, 29745.594922068358, 29745.960564495348, 29748.372736542264, 29748.60852809665, 29748.814195251416, 29749.00430006155, 29749.372725585778, 29749.385783251844, 29749.576907870443, 29751.34375700723, 29752.53651560482, 29752.813917380623, 29752.877742790937, 29753.467849409604, 29754.13774701189, 29754.44631984535, 29754.65594372406, 29754.966282823087, 29755.32990812549, 29755.929589200365, 29755.936377021724, 29756.722545151064, 29757.522174687936, 29758.226975583002, 29759.211598889644, 29760.128365368877, 29761.059879800076, 29761.962164305656, 29762.46529145235, 29763.383253145144, 29765.071473338805, 29766.34827478244, 29767.133845141758, 29767.77596953819, 29768.1027836652, 29768.125913833144, 29768.590355429413, 29769.36311997563, 29770.44163981305, 29772.02683812015, 29772.54835957339, 29773.962977135576, 29774.719039786032, 29775.681355579618, 29779.01065568976, 29779.529533121302, 29779.697681376172, 29779.903864018386, 29780.583787787287, 29780.95656437605, 29781.429619640225, 29782.783078502853, 29783.16677354104, 29783.778016255423, 29784.916227350983, 29787.215414994113, 29788.334813721238, 29788.909892283024, 29789.935711286846, 29790.147014105485, 29790.376485748704, 29791.78510342279, 29791.797401940097, 29792.30299625259, 29792.68882741924, 29792.79557437291, 29793.49042409111, 29793.628798420217, 29794.26617177038, 29796.63308687243, 29798.20321951877, 29798.226901512553, 29798.265506516433, 29800.31319535224, 29800.493463491814, 29800.590958604473, 29801.297369461747, 29801.53648166441, 29802.586057245826, 29802.97019399335, 29803.633404101583, 29803.8190427343, 29804.35473991322, 29804.81395258361, 29805.708544191795, 29806.147005700364, 29806.416584029183, 29806.993672475437, 29807.916473150653, 29808.274841805385, 29808.348287137225, 29808.57341036582, 29808.78121286363, 29808.852000133993, 29808.976134363525, 29809.975498399333, 29811.453166272473, 29811.75814897003, 29814.214246247248, 29814.291400093825, 29814.399381539104, 29814.775047720304, 29815.19845421242, 29815.455626132734, 29816.9891514029, 29817.571764727512, 29818.36819328398, 29818.739248417154, 29819.447800822916, 29821.070240575948, 29821.112112207436, 29822.5228233212, 29823.097109540675, 29823.278748234992, 29823.94599941508, 29825.410498023746, 29826.50388297243, 29826.67154258674, 29826.68093204506, 29827.181984086455, 29827.74412345101, 29829.18232663083, 29829.341668546043, 29829.95609942828, 29830.476114317615, 29830.69605300375, 29830.91729857595, 29831.15650135784, 29831.60427261255, 29831.777551294603, 29832.920675828445, 29833.62325256733, 29833.883998275975, 29836.28624691023, 29836.295991924904, 29836.393561773497, 29838.371328521207, 29839.055734556783, 29840.28827924067, 29842.767347816418, 29843.35112087808, 29846.274826856905, 29846.492857948637, 29846.531571707674, 29846.927926295146, 29847.063825860365, 29847.171624320705, 29848.004042204528, 29848.107535397685, 29848.30145978142, 29848.3548065195, 29848.422782536207, 29848.82462642645, 29849.91321140078, 29850.680795515946, 29850.94168160561, 29851.090191327687, 29851.954370709307, 29852.245997236096, 29852.362668581587, 29853.905929815843, 29854.693442536674, 29855.666563027407, 29856.336122650795, 29856.738757803567, 29857.586837189287, 29857.648242044834, 29858.67955505994, 29859.97026866852, 29860.373810419853, 29860.649443463662, 29861.197911014755, 29862.1515670536, 29862.53887762458, 29863.33245347861, 29863.410742670487, 29863.709222043854, 29864.882795908252, 29865.659072719063, 29865.680415365052, 29866.20821182943, 29867.22490249576, 29868.31043568846, 29868.627193046483, 29869.601458800233, 29869.82080344134, 29870.632374387482, 29871.22809338038, 29873.09128250544, 29873.970521183164, 29874.17726592139, 29875.06323838942, 29875.168873828865, 29876.315126894857, 29876.646147715433, 29877.21668182562, 29877.63363854252, 29877.847703199222, 29877.86910466939, 29877.92884170531, 29878.130678949634, 29878.81548251138, 29879.81218110457, 29880.414049336323, 29881.31162663252, 29881.832987313275, 29882.289089029648, 29883.694760901035, 29884.523121111695, 29884.713641992854, 29885.36979112203, 29886.15308112644, 29886.879577968954, 29887.21172849736, 29887.878081437055, 29887.908935974083, 29888.14851056286, 29888.27722960759, 29888.45348623995, 29888.506057025697, 29888.779378644613, 29889.32304297746, 29890.181951676608, 29890.21516997191, 29890.389659340224, 29890.56421056149, 29891.3937363439, 29892.707430687828, 29893.066750749203, 29894.376159850064, 29894.7699393904, 29896.893282380395, 29898.66624688892, 29898.976365249102, 29899.467969912188, 29900.24488480241, 29900.376116457468, 29902.42617589662, 29903.095566634925, 29903.697539114615, 29903.893769445753, 29905.898942166838, 29906.647648325797, 29906.902800025666, 29907.797118331586, 29908.878881073655, 29908.988860833448, 29909.864596611067, 29909.96120936322, 29910.165149895434, 29910.401668620347, 29914.336632431918, 29915.040660783947, 29915.240030123274, 29915.51840731883, 29916.191043557923, 29916.972758044616, 29917.26160098949, 29917.697957540226, 29918.04711775149, 29919.313276604913, 29919.625501837294, 29920.31952461631, 29922.020035473477, 29922.3140635679, 29922.400057438077, 29922.400901791923, 29923.35251316685, 29923.383123139272, 29923.859809636993, 29926.373191408158, 29926.84972120934, 29927.569274610014, 29929.45966526465, 29930.82955840762, 29932.307875643903, 29932.685858855526, 29933.09498252675, 29933.13675646762, 29933.384661807006, 29933.971864598963, 29934.355383098144, 29934.884198892785, 29935.461219331355, 29936.00850948147, 29936.086270433134, 29937.612185127957, 29940.112798642822, 29940.294569174348, 29940.365265771667, 29940.795256571153, 29940.959291939493, 29941.447520328085, 29941.524856475236, 29942.34851238213, 29942.584576932477, 29943.11405082584, 29943.83814369036, 29946.656199966386, 29949.192781196245, 29951.19948992203, 29952.480893671942, 29953.538583411424, 29955.988066506616, 29956.119611634254, 29956.992898877885, 29958.81143152656, 29958.95721368269, 29959.412349706254, 29960.076973763513, 29961.204049915894, 29963.204043414236, 29963.559908934287, 29963.789526421537, 29964.987827639918, 29965.015509143916, 29966.770390514524, 29967.204904842893, 29967.95835216718, 29969.34126664186, 29970.53979305066, 29971.52504019991, 29972.817360449248, 29973.017037083926, 29974.890937234242, 29979.76434870962, 29980.674468174904, 29980.747925981086, 29980.798552213884, 29981.537159634667, 29982.059850143676, 29983.277617210806, 29983.363899469055, 29983.372100215693, 29983.4428299161, 29985.900719457408, 29986.095954815068, 29986.839223742532, 29988.046059732078, 29988.375317259986, 29988.650681618823, 29988.719313796766, 29988.93937371472, 29989.50447201296, 29989.822951399405, 29991.110354922774, 29992.1456642498, 29992.415085629516, 29993.602879309143, 29993.93170043614, 29994.866046159746, 29995.512738090827, 29996.365542675707, 29997.545844650333, 29998.939220687276, 29999.533124473623, 29999.581934031667, 30001.59006297668, 30002.282111338875, 30002.46480604038, 30002.490749712044, 30002.494412291344, 30003.97986195321, 30005.440969480103, 30010.023991870137, 30010.849164706062, 30011.146403862687, 30012.2310081775, 30012.45259587952, 30012.461533566257, 30013.025471886755, 30014.276991898627, 30015.781874944474, 30016.924473612926, 30017.096892334008, 30017.83895532085, 30019.415060307536, 30021.403848795733, 30022.220166738647, 30023.00169167134, 30023.73148880522, 30023.974711489413, 30024.319284239173, 30025.69573555182, 30027.692423480887, 30027.782886976016, 30027.949876325794, 30028.73227279428, 30028.811386061905, 30029.396704268092, 30029.622563702596, 30029.893356875848, 30030.174201125647, 30032.51028700279, 30032.67186569171, 30035.173439025704, 30035.899400061026, 30036.582880588427, 30037.48936707479, 30037.536152048586, 30038.220509112936, 30038.826337428116, 30039.77670815089, 30040.006269424586, 30040.74101933684, 30042.0055246178, 30042.097938324605, 30043.735794955635, 30043.846125725777, 30045.078623803332, 30045.51168134038, 30045.784736747013, 30048.605190703638, 30048.941226878993, 30049.336459163736, 30050.053765374098, 30050.548150475523, 30051.068845329286, 30053.044085697, 30053.063391811844, 30053.347676802805, 30054.07714941152, 30054.0866233768, 30055.65445646408, 30055.824662997435, 30056.981247579486, 30057.844688466354, 30057.926386667823, 30058.691344488587, 30059.375645972796, 30059.42254944505, 30059.929437763145, 30060.74455456234, 30061.3986989833, 30062.49790533394, 30064.437420587434, 30064.488460519453, 30065.05583429448, 30065.29045169749, 30066.21416882873, 30066.588654846095, 30066.872370295045, 30067.16307681823, 30067.689104636152, 30068.78632927472, 30069.017768185193, 30069.374177176753, 30069.632291446665, 30070.826999520843, 30071.399323924143, 30072.160307875154, 30073.311630139593, 30074.21150128956, 30075.631849974987, 30076.488428957113, 30077.98979860671, 30078.661562273493, 30084.38856570024, 30085.21340255947, 30085.400780141095, 30086.337732073527, 30087.129107976514, 30088.671740092363, 30089.25561301907, 30089.909456788784, 30089.91641629221, 30090.094044909918, 30090.93244608385, 30091.195016268914, 30093.277153310035, 30093.46125432748, 30094.224690879586, 30094.392974855735, 30094.74323502281, 30095.039833468316, 30096.143967877782, 30098.796232517318, 30099.06488421176, 30099.303842665668, 30100.559690899983, 30100.866770983506, 30101.883745624877, 30102.101007196186, 30102.82587330739, 30102.897294288203, 30108.123730256495, 30108.97631417851, 30109.950035099268, 30109.955208077718, 30110.375224051197, 30110.444177171874, 30110.833811594133, 30111.282155331406, 30111.707509124888, 30113.419115663153, 30113.477268510793, 30114.407286149963, 30114.689987561294, 30116.70043180247, 30117.148114995733, 30117.26409507123, 30117.61562536066, 30118.859509408943, 30120.009089670493, 30120.64539838564, 30121.55223148331, 30122.36228261977, 30122.462838194064, 30123.34781981589, 30127.154968190665, 30127.363657901227, 30127.77260575396, 30128.56219280054, 30128.7909154676, 30129.262282325948, 30130.447655967142, 30133.731031571042, 30133.766386306455, 30136.418873136838, 30137.05143619689, 30137.432128367367, 30138.12110235336, 30139.75167299462, 30140.599547339745, 30140.66473359053, 30140.879578683423, 30141.333191011287, 30141.86751801759, 30144.062391907846, 30144.499165991157, 30145.137140957006, 30145.377076978086, 30146.41133793159, 30149.231464341778, 30149.8957669365, 30150.003486900114, 30150.92707467772, 30151.114734278635, 30152.02038744123, 30152.24061620066, 30153.080231403193, 30154.096531703537, 30154.998505516818, 30159.704836163175, 30159.86255296045, 30160.670918354797, 30162.210841728687, 30162.953993842606, 30163.478960966586, 30163.551624016876, 30164.05621553842, 30166.186709308426, 30167.414569945548, 30167.517917900903, 30167.95070786569, 30168.029726314424, 30168.521111460424, 30168.564113170596, 30168.724668747152, 30169.552493017363, 30169.560323644022, 30169.89510622822, 30170.214326490954, 30171.011473953808, 30172.886733397212, 30173.02627867698, 30174.78329913183, 30176.085758676956, 30176.229471784958, 30177.036498995258, 30177.606144845107, 30179.181863350164, 30179.228440009476, 30180.72502651626, 30180.780233490965, 30181.277292414954, 30181.388399279083, 30181.586980710683, 30182.717314786358, 30182.746280560154, 30182.98028711813, 30183.962269209133, 30184.420102520995, 30184.72119141565, 30185.045485775285, 30185.287334720575, 30186.080898221542, 30186.437771603367, 30186.574204961893, 30187.596451975558, 30188.266297572303, 30188.428279665626, 30189.863725197512, 30189.998284404774, 30191.03259975677, 30192.447143635214, 30193.468842978527, 30193.96887658459, 30193.97790064512, 30194.855824221086, 30195.13964942603, 30196.64307626775, 30199.331048594548, 30199.730736839334, 30200.265401354194, 30201.55644256874, 30202.77632665661, 30203.052766609177, 30203.919680850213, 30204.431228501722, 30204.440963701345, 30204.50226012359, 30204.544571470247, 30204.82645608393, 30205.699540896785, 30206.155710441188, 30206.652945247304, 30206.72762482561, 30207.13178842665, 30207.243062004938, 30209.62602575096, 30209.841325651523, 30209.990666930837, 30210.355596871912, 30211.281543383247, 30211.354801093115, 30211.557103532738, 30211.995586912526, 30213.37497500063, 30213.75514351644, 30213.765110201784, 30214.403596874945, 30215.374024940116, 30215.91636005688, 30218.952105032633, 30219.01406448147, 30219.478136103327, 30220.985728380852, 30221.663476426795, 30222.445759743576, 30224.41479477682, 30224.796888474757, 30225.721141995695, 30226.011352187605, 30227.68319134785, 30227.86335867209, 30227.97136180568, 30230.982916528043, 30231.668463171318, 30232.76768705647, 30233.419172317772, 30235.24072058866, 30235.351818071624, 30235.88096290737, 30236.192806049658, 30237.479872442822, 30238.64985735313, 30238.971702981362, 30240.486028433068, 30240.62605073339, 30241.113225747784, 30241.512994375447, 30242.70339611229, 30243.48973822821, 30244.854540141558, 30244.883170884397, 30245.38030253898, 30246.393286418333, 30247.38940978769, 30248.193764433312, 30248.530614195402, 30248.616439507776, 30249.429905775047, 30250.473530954674, 30252.21107923231, 30252.35849849474, 30252.934874168317, 30254.315041241334, 30254.42197745066, 30256.48281318187, 30258.54098162068, 30259.65985030317, 30261.27119641433, 30261.285518160592, 30261.825916771257]

    # X111111_1 = X111111[:100]

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

    X111111_1 = [29505.200377711237, 29505.488563502964, 29505.503568623288, 29506.935199095136, 29507.568858427978, 29507.67233250641, 29508.449818219582, 29508.753973397153, 29508.932514975764, 29510.994390245738, 29511.06099975447, 29511.550243919497, 29511.77431283564, 29515.052602270047, 29515.430170360094, 29515.73175442012, 29516.443764850927, 29516.45512312267, 29516.67585202982, 29516.83347763569, 29519.461207257267, 29519.483003738704, 29520.378875737668, 29521.12551933724, 29522.345544069383, 29523.43141195545, 29524.435126044293, 29524.774233270513, 29525.61685195844, 29527.103970622276, 29527.545088882547, 29527.686965219633, 29529.074031038457, 29529.753612803095, 29530.023687926285, 29530.474787770698, 29531.782796750496, 29532.83676239816, 29533.09499652632, 29533.687309521974, 29533.87819384058, 29536.45889819682, 29537.357807633623, 29539.153066264298, 29542.83200511856, 29543.59964873175, 29544.306918720125, 29544.91011001689, 29547.395328299568, 29547.80900166393, 29548.284199840615, 29549.698232689585, 29549.790420970137, 29553.014944669605, 29553.13247494664, 29554.48892342402, 29555.931226833793, 29556.09970736713, 29556.49555822643, 29556.684781673015, 29556.68940019439, 29558.352424353743, 29558.6694940866, 29558.75588938419, 29559.476649007105, 29560.154246360817, 29562.84295894107, 29565.7758513471, 29565.815478917048, 29566.835255544618, 29567.01120136662, 29567.269144939888, 29569.033347612258, 29571.526833284857, 29571.7429211811, 29571.871645900035, 29572.00266725394, 29572.96430340313, 29574.562049372907, 29575.596765160644, 29576.001632163276, 29576.134214254103, 29576.322106235, 29576.338691510322, 29577.360298171374, 29578.906183563613, 29580.967980565314, 29582.21385770823, 29584.09242799194, 29584.962416405222, 29585.09831607334, 29585.189376216164, 29587.240552249055, 29588.17424317689, 29589.323752066215, 29590.3714416476, 29590.806766205857, 29591.378224302673, 29592.432777019538, 29593.35699746775, 29593.39710923724, 29593.452713191542, 29594.391990335876, 29594.42482468182, 29594.595240585368, 29596.397729353044, 29596.45511775047, 29596.731158613362, 29597.555653524643, 29598.303863282963, 29598.932885308375, 29599.818974271922, 29600.522254577427, 29600.536423493275, 29600.90134952106, 29600.923996675596, 29600.930066949662, 29601.261783653445, 29602.42352070647, 29604.209708991864, 29604.326724427916, 29604.59198281132, 29604.83326414049, 29606.428394415358, 29607.08048998242, 29608.142988250693, 29608.841855584975, 29609.25419281211, 29609.37109682628, 29609.50110511702, 29609.635394059926, 29610.68697229818, 29610.693023688866, 29611.011162129347, 29611.184359141174, 29611.342847015792, 29612.453334041096, 29614.800330725302, 29615.37539739427, 29615.58076831305, 29616.712916420434, 29617.38485010862, 29619.48698264938, 29619.693674332324, 29621.390594661403, 29622.782139682706, 29624.15369897409, 29624.670260208346, 29625.445363858536, 29626.786215112756, 29627.17884763719, 29628.551485208372, 29628.8315592309, 29629.768067136276, 29629.99824599699, 29630.792250379087, 29630.807541122733, 29631.641100299672, 29631.67722337694, 29633.429838834654, 29636.07361254186, 29636.463032416767, 29636.530251322736, 29638.519862755766, 29639.162389508394, 29639.376139520544, 29639.708793753092, 29641.557155909733, 29642.14017615526, 29644.649533008065, 29645.018991163357, 29645.037130452063, 29645.490273795844, 29647.904189308523, 29648.165990923444, 29649.08078244724, 29651.072438538962, 29651.12780317519, 29651.628230142236, 29651.91302331822, 29652.53463577034, 29652.81132348691, 29653.090615067485, 29653.59856493123, 29654.61957429163, 29656.215872947072, 29656.370049401885, 29656.657995283735, 29657.083851770905, 29658.87346875505, 29660.025645731566, 29660.550431541942, 29661.48668222227, 29664.1398922221, 29664.511414146786, 29666.019890781656, 29667.194322390176, 29668.642535396302, 29669.647895195572, 29672.855883843316, 29673.555019743395, 29674.889989785897, 29675.60618944005, 29676.78394295587, 29677.33426443452, 29677.59190721795, 29677.859952404415, 29678.224547073085, 29678.919524545363, 29679.26171058302, 29679.386670054377, 29679.77392443473, 29681.32177749472, 29681.681598484396, 29682.561564496395, 29682.595766322163, 29683.641551674682, 29684.496704803263, 29684.956509926196, 29685.794553151638, 29688.96209265627, 29689.49855487375, 29689.804336443933, 29690.09764120071, 29691.31757158509, 29691.507477920568, 29691.768959667254, 29691.787698324562, 29692.348718632238, 29693.897406276268, 29694.61748507513, 29694.916754135047, 29695.073760199917, 29695.392951819063, 29696.007278823294, 29696.255884590235, 29696.499191531537, 29697.854474460324, 29697.940891352984, 29698.220269108173, 29700.198670305843, 29700.63149132691, 29700.790428453245, 29701.016282177898, 29701.03337770745, 29701.84791073565, 29701.867631509496, 29702.169716025528, 29702.59762324481, 29702.737076433332, 29704.018415628063, 29704.046657507515, 29704.239499544743, 29704.29371717545, 29704.875446565227, 29705.60166066159, 29705.890786597, 29706.502082145747, 29708.35385401003, 29709.015550134616, 29709.308500571202, 29709.314351791665, 29709.744576659723, 29711.41554331261, 29712.78539015495, 29713.485234732656, 29714.062068043248, 29714.07256346073, 29714.67191782045, 29717.909166221412, 29719.201612075925, 29719.43357255159, 29719.43762937224, 29719.889373093392, 29721.48300849977, 29723.230787505545, 29723.38812551087, 29723.75622674797, 29723.959599711485, 29725.159679584278, 29725.17783321466, 29726.89714430345, 29727.204644789013, 29729.087761244722, 29729.560007411586, 29729.811869061225, 29730.294397450045, 29731.164237360605, 29731.21680336167, 29731.429367287798, 29732.356623584157, 29733.882483621113, 29735.873759143007, 29736.142998289233, 29736.756332271925, 29742.193509416837, 29742.904804879847, 29744.480436028814, 29745.724121265193, 29745.742106635444, 29746.512300447834, 29747.41139242041, 29747.921197598385, 29748.355992638702, 29748.990798848958, 29749.065161053266, 29749.379002398207, 29749.42992603876, 29749.614563981995, 29750.07043394162, 29750.33001875163, 29751.583044523388, 29751.617195966974, 29751.691922870345, 29751.940486595216, 29752.20985831229, 29752.37019287677, 29752.69861088993, 29754.14141849646, 29754.925047252276, 29755.035526735795, 29755.087548109455, 29755.84484471074, 29756.09123838296, 29756.30009281169, 29756.560607377403, 29759.95633739477, 29760.347591911137, 29760.88950053448, 29764.188340924688, 29764.371780879068, 29765.022773701603, 29765.048470389556, 29765.251323275104, 29767.065038088247, 29767.158079336747, 29768.039972159062, 29768.18011747738, 29768.4224240379, 29769.44159170755, 29769.44820997617, 29769.682679991733, 29770.217177175324, 29770.488698202884, 29771.07276187385, 29772.26274694019, 29772.7448007027, 29772.92172903887, 29774.155433868684, 29774.700379075966, 29774.99853125262, 29775.44323182004, 29775.539597231305, 29775.733607815706, 29775.885539087696, 29776.28062627285, 29776.63608263835, 29776.671635189137, 29778.362477719213, 29778.491791403714, 29779.547562070693, 29784.415914209098, 29784.976014086333, 29787.696246258467, 29788.348449347504, 29788.936053307312, 29789.98164719662, 29790.939995772333, 29791.954970377486, 29793.527818018905, 29793.95206888501, 29794.168115375924, 29794.920080207947, 29795.478999039653, 29795.982392397545, 29796.273354136163, 29799.697276378556, 29799.916903517213, 29800.87189624263, 29801.173856650574, 29802.344353807934, 29803.031199541307, 29804.794877753353, 29805.525044086102, 29806.491126021367, 29806.505701666665, 29806.792086442816, 29807.190369233464, 29807.495092640766, 29808.368104006604, 29808.515825793074, 29809.795983232172, 29809.826027925603, 29810.261211414178, 29810.464351317954, 29810.75426994854, 29811.111907352068, 29813.424561042702, 29813.546681379015, 29813.655597267672, 29814.3462474952, 29815.166107959507, 29816.578178303695, 29817.346758606993, 29818.093793102435, 29818.306623051027, 29818.968033104127, 29818.982609531038, 29819.207494326005, 29820.206318337423, 29820.650207735584, 29825.056152132693, 29826.33990403864, 29828.103413340414, 29829.222752752663, 29829.81562138944, 29829.9039762408, 29832.137224559636, 29833.880499893883, 29834.030303811574, 29834.56201858595, 29837.14245367956, 29837.394425789407, 29838.18037492359, 29840.29809324374, 29842.541642686552, 29842.93166353501, 29842.941410295196, 29843.428915951805, 29845.28893544043, 29847.072928346715, 29847.42189752459, 29847.630203076656, 29847.90944364314, 29848.978518059044, 29849.504132822574, 29849.964155671172, 29850.382385102646, 29850.65795346007, 29851.790612041244, 29852.6768803682, 29854.380935046684, 29854.42152215575, 29855.257162524373, 29855.938501075434, 29856.618195316925, 29857.210857739574, 29858.531271805754, 29858.76465644574, 29858.79718095585, 29858.93771002645, 29860.71599236332, 29860.72159702945, 29860.860217418092, 29861.233328371705, 29861.998717257335, 29862.064562065792, 29862.082322727885, 29862.36948087484, 29862.394144477585, 29864.18501576995, 29864.65284410308, 29866.29078936091, 29866.57446426098, 29867.177174157012, 29867.258277075143, 29867.804481081715, 29867.83151501796, 29867.947469640658, 29868.78369166986, 29868.820116721738, 29869.528567709633, 29869.542398452933, 29870.389377270396, 29871.035771762927, 29871.296653063924, 29871.57082349971, 29872.992681963446, 29874.587476757657, 29874.73891807756, 29874.831047544707, 29876.53270631828, 29878.480882952725, 29879.217035115842, 29879.778597327382, 29880.282383639733, 29880.904950591615, 29881.78301298036, 29881.94307495343, 29882.02769330735, 29882.84507762031, 29883.819461986557, 29884.134760266294, 29884.33228651247, 29884.96119539416, 29885.35447170746, 29887.59586831393, 29888.617589822068, 29888.626643485022, 29889.6146760973, 29890.143722860004, 29890.303750957602, 29890.663053543914, 29893.292631802713, 29893.967194955265, 29894.024850883237, 29894.56880333808, 29895.496301451185, 29895.69165028936, 29895.845929821786, 29896.02882388911, 29896.139273505054, 29897.38386212758, 29897.460963828595, 29897.60599112506, 29898.125551790807, 29898.802230177436, 29899.033896670408, 29900.77789616422, 29901.06915681231, 29901.136470332523, 29901.21454501499, 29901.738088121612, 29901.741951583575, 29904.342119407043, 29904.856040568076, 29906.317297570276, 29906.572304716217, 29906.706218208103, 29907.333875780125, 29907.845969736907, 29908.014792885806, 29908.22648822844, 29909.0937867185, 29909.534790034704, 29910.57704564294, 29911.184331401848, 29912.825584594684, 29913.066046089454, 29913.56729546194, 29914.759276718753, 29915.988203492656, 29916.224503492376, 29917.483133655755, 29919.019905134002, 29919.149910630593, 29919.426792094135, 29920.767122960588, 29920.85538176397, 29921.188322438542, 29921.2808615243, 29922.803823571383, 29924.02781421761, 29924.114377288286, 29924.249685198956, 29924.95706361705, 29925.87615013026, 29926.395110193796, 29926.7975599519, 29926.851954512593, 29926.92939578732, 29927.026423502983, 29928.348484351074, 29928.353280879102, 29929.44412967938, 29929.54007183903, 29930.891899440445, 29931.177333306325, 29931.4050797205, 29931.649844439115, 29931.752963692412, 29931.853526648814, 29932.672717403802, 29933.148044894595, 29934.903932843627, 29935.139975057533, 29935.49141571288, 29936.49078810932, 29936.515619651207, 29936.993163020077, 29937.932715189785, 29938.086253118578, 29939.698274156697, 29940.40972608193, 29942.999731545384, 29943.285825245774, 29943.76299471352, 29943.84112158393, 29943.984763289176, 29945.489238690472, 29947.966142110497, 29948.18045426266, 29948.243803125668, 29948.306964459858, 29948.47867004399, 29948.99590430799, 29949.084515929775, 29949.821400378667, 29950.355642872037, 29950.74281879569, 29950.755296368323, 29951.47363085737, 29952.263550872445, 29953.062766833486, 29954.671440200527, 29954.78510750622, 29956.089053543066, 29956.488244361673, 29956.723211263077, 29957.296065229468, 29957.64759689655, 29957.873528253425, 29959.09915952923, 29961.550955135892, 29962.077331127162, 29964.46674133935, 29964.54619204539, 29965.01531836132, 29965.68309150163, 29967.50913233767, 29968.437914535538, 29968.68167932572, 29969.416413917264, 29969.80058961399, 29970.2363339413, 29970.38603518208, 29971.713996882077, 29971.790734815673, 29972.018834783954, 29974.163144875907, 29975.08795600147, 29975.316581790095, 29976.258935767808, 29976.75825831061, 29977.21368218726, 29977.28193760314, 29978.06433572063, 29978.530412301527, 29979.032890730523, 29979.40697982948, 29979.4630972516, 29980.136363582267, 29982.123588709364, 29982.300012386953, 29982.59157313572, 29984.108446225637, 29984.137668436222, 29984.251209516693, 29984.770232285944, 29985.779354697526, 29986.65422896921, 29986.683324263693, 29987.97190179458, 29988.060139673442, 29988.68941725585, 29989.232578143983, 29991.285591679618, 29991.420149685684, 29991.53986076294, 29991.879356120815, 29992.269677417597, 29992.618916519474, 29994.042234323937, 29994.924455717075, 29995.553467841073, 29996.731734992154, 29997.472219914063, 29998.371279548646, 29998.425800167046, 29998.783272050234, 29999.5850838883, 30000.718594625883, 30001.687121171883, 30005.17161437813, 30005.87563999963, 30007.037945980708, 30007.067417344162, 30009.232036747355, 30010.298142383115, 30010.707455823038, 30011.227269758456, 30011.40845846758, 30011.515429349303, 30011.784205513315, 30012.620384244652, 30013.40619329468, 30014.059883447666, 30014.173568591137, 30014.401446369742, 30014.613249844744, 30014.780098322233, 30016.680304464076, 30017.644933503398, 30018.11187871569, 30020.910715618356, 30022.13169911584, 30024.45458329768, 30025.046529059855, 30025.338062526724, 30026.996217579937, 30027.30594331038, 30029.315678419716, 30029.450089880265, 30029.575913310346, 30031.430781969782, 30032.832830904717, 30033.272181216016, 30033.375560314755, 30034.155340483198, 30034.334673485835, 30034.973157588163, 30036.353594902885, 30037.47242207254, 30038.04619017479, 30038.251009958607, 30038.450085557553, 30039.715038223683, 30040.461608706093, 30043.01424423427, 30043.457913538754, 30043.559327498566, 30043.750724429105, 30044.669339966098, 30045.067581442687, 30046.967656633802, 30047.628381246992, 30047.70725205942, 30048.70440405252, 30049.81793054221, 30050.57044888264, 30050.916528352132, 30051.09281146043, 30051.996203506886, 30052.357565964787, 30052.845929133655, 30053.24364231239, 30053.3704121235, 30053.43503636956, 30053.573794118336, 30054.44402386817, 30055.940488440516, 30056.88583314725, 30056.980920314203, 30057.06079965631, 30057.46297090358, 30057.471573506788, 30058.097674793094, 30058.303177871472, 30060.33127348915, 30060.782715807305, 30062.5024096475, 30062.819218275938, 30064.689595295127, 30066.462719858988, 30067.157774746254, 30068.50550017754, 30069.539257851746, 30069.730032818552, 30069.857645300093, 30070.839439367777, 30073.78921679554, 30075.83044638092, 30077.394514527285, 30078.88794041546, 30079.17855125125, 30079.67467651658, 30081.352619295227, 30082.95175492342, 30084.68045435203, 30084.788224403164, 30084.90512007453, 30085.637995386005, 30085.988931663578, 30086.109799737977, 30086.347546928224, 30086.428457196653, 30086.854522213293, 30087.342671128277, 30087.366786313432, 30087.911233185117, 30087.921085887014, 30088.36466304827, 30089.341076554512, 30089.562436596883, 30089.615255479344, 30091.43789652462, 30091.498848336898, 30093.42786320298, 30093.44897344, 30094.929189039198, 30095.985213634976, 30097.118731719136, 30097.646805034496, 30097.71236367927, 30101.20429903482, 30101.870018723755, 30102.494520694116, 30102.519393099068, 30102.861617354272, 30103.04484509476, 30103.084810198678, 30104.038041836415, 30104.7348834671, 30104.983836884476, 30105.4648490492, 30108.47589704796, 30109.44178108847, 30110.272617410097, 30110.499265435865, 30110.950867761843, 30112.569416437236, 30112.614853075418, 30115.10691022289, 30116.83339517212, 30117.87571649352, 30119.36721700324, 30119.4046465111, 30119.49289545588, 30120.21450540164, 30121.952966548837, 30122.027846639514, 30124.410609766262, 30125.006918186733, 30126.017781333372, 30126.373189234848, 30128.949964128464, 30129.51253504282, 30130.546215100072, 30131.316802223257, 30131.86116904201, 30132.659768002937, 30132.6649384118, 30133.107035261208, 30133.79314637737, 30135.2432024987, 30136.41367005959, 30136.53305003991, 30136.5838644058, 30136.959520118988, 30137.342537915738, 30137.53890894986, 30138.002717727384, 30138.878593563586, 30139.073864745267, 30141.338449910578, 30142.226894171177, 30142.61256734433, 30143.537721741228, 30144.032580217146, 30146.316111457298, 30147.05310469204, 30148.047480786827, 30148.098424912503, 30148.353695128106, 30149.472184334874, 30149.616320729725, 30150.390927611446, 30150.883367544764, 30153.388265162306, 30154.110149432414, 30155.984851597445, 30157.048163495976, 30157.770553348386, 30158.645124365503, 30159.110658423935, 30159.185240580064, 30159.22909754983, 30159.648252520274, 30160.94087500725, 30162.93833673989, 30163.152081771917, 30165.628858361957, 30166.969747505755, 30167.193032208797, 30170.609636774905, 30171.40610887243, 30172.194904258522, 30172.673111281325, 30173.70002108867, 30174.23999698675, 30174.800427087353, 30176.633730396705, 30176.897668668887, 30177.9686472128, 30178.029839461567, 30179.64280377237, 30182.345993379786, 30182.49481109772, 30182.81065971733, 30183.214638525773, 30184.580647829298, 30184.920139230155, 30185.06082413865, 30185.077271496084, 30186.379932097247, 30187.313999554128, 30187.40814012302, 30187.715759739258, 30188.73961516023, 30189.149943428285, 30190.137139037222, 30190.31166552305, 30190.81266391502, 30191.685957416237, 30195.21883847646, 30196.242325209987, 30198.21253651442, 30198.335444776058, 30200.148511328418, 30200.594680619557, 30200.606633031144, 30200.86596988595, 30201.255218543036, 30201.447163096822, 30202.31016315624, 30202.890903567823, 30203.702729480792, 30203.90121232265, 30204.009345900588, 30204.42366058679, 30204.585907325083, 30205.078021762136, 30206.080592292503, 30206.70363598034, 30208.727369640965, 30208.949480753196, 30209.612253494026, 30210.781047295495, 30211.51421714973, 30211.578358852646, 30212.515070435416, 30212.873818156524, 30213.857423642366, 30214.621954319686, 30215.152626945026, 30215.904103605528, 30216.024376794016, 30216.330532455482, 30216.95916526836, 30217.029174858155, 30218.149775063386, 30218.865351410757, 30219.571221459824, 30219.993242877335, 30220.196927061555, 30221.502785040633, 30221.828888582662, 30222.89108125665, 30223.53058769324, 30223.934380973897, 30225.42822392154, 30226.461926587242, 30226.584016998997, 30227.723129579874, 30228.042455751773, 30228.61120373776, 30228.799782896967, 30229.103714108423, 30230.18605649934, 30232.71867848772, 30233.723705012908, 30233.773724274102, 30233.822503587966, 30234.414073505533, 30234.418862417348, 30234.662189787057, 30234.720419223326, 30236.17537832662, 30236.903451766833, 30237.641108303487, 30239.95924053407, 30240.164291676483, 30242.150960708477, 30242.920034164235, 30243.51039922422, 30244.104444018038, 30244.12324213039, 30245.543883899267, 30246.074038422837, 30246.760290292255, 30248.11301795467, 30248.76564606342, 30249.442108603616, 30251.38511790867, 30253.242762754246, 30254.52825249476, 30254.64554875541, 30254.726919755572, 30254.830608518303, 30256.038824375697, 30256.572636764675, 30256.734864401285, 30256.926856687798, 30257.12133071022, 30257.704214745543, 30258.179993755875, 30258.545125989796, 30260.666473836092, 30260.679389424746, 30261.343023464593]

    # X111111_1 = X111111[:100]

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

    # print(f"Time taken to execute the program: {elapsed_time} seconds")

    output_string = f"{bestK}, {bestNumberOfTerms}, {degree}, {coffs}, {best_K_correction}, {min_error_value}, {mse}\n"

    with open(filename, 'a') as file:
        file.write(output_string)
        file.write('\n')  # Write a new line after the output string

    return min_error_value


def main(in_Scale, in_Intercept):

    _r = lambda y: np.round(y, decimals=64)

    Scale = in_Scale
    Intercept = in_Intercept - (Scale/2.0)
    filename = 'Consumer_TAYLOR_output-' + str(Intercept) + '-' + str(Scale) +'.txt' 

    allErrors = []

    for i in range(30):
        error = SubMainFunction(Scale, Intercept, filename)
        allErrors.append(error)

    print(allErrors)
    
    mean = np.mean(allErrors)
    stddev = np.std(allErrors)

    print('MEAN: ', mean)
    print('stddev: ', stddev)


if __name__ == "__main__":
    Scale = sys.argv[1]
    Intercept = sys.argv[2]
    main(Scale, Intercept)

