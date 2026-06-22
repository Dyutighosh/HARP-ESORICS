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

    min_val_1 = 30331.79248152376     #min(X1)
    max_val_1 = 39284.98027846861     #max(X1)


    X111111_1 = [30332.238751161767, 30339.236369274462, 30343.788870028457, 30346.37541830313, 30355.897755895367, 30366.759556934056, 30371.995659840923, 30372.482106490435, 30380.861072764535, 30384.63094920355, 30388.57314844173, 30388.69364525863, 30389.28555952006, 30398.581880166632, 30417.620622942435, 30433.759562220734, 30438.340619456125, 30440.43660536398, 30447.896540480047, 30453.060176394185, 30465.266805258805, 30469.408878107228, 30470.834012248415, 30479.56595232743, 30489.511198222262, 30496.706337934025, 30546.8977930717, 30565.240611403704, 30566.81622987803, 30572.994964305504, 30575.54970331282, 30590.377493927732, 30601.509767878215, 30603.364324710266, 30605.82558970562, 30608.501362579347, 30614.428522408096, 30615.105438881976, 30619.886504918482, 30626.384068414838, 30638.891403464913, 30646.215757676895, 30647.187815603436, 30661.633456253978, 30666.690296816025, 30669.55666114848, 30684.710751379826, 30696.559095487395, 30697.361375551976, 30702.597972749576, 30704.76875994725, 30707.689063087993, 30707.90583060782, 30711.85935953118, 30714.84111770226, 30718.348760449662, 30724.24737468587, 30732.34274965142, 30746.288382696064, 30753.724312884566, 30768.79689655082, 30770.841714172562, 30783.102332684168, 30796.481764060125, 30805.920982357093, 30806.62383866525, 30807.208298769012, 30810.474046877265, 30814.354065809457, 30815.035881205207, 30827.67841219394, 30834.37316798081, 30845.98624518408, 30855.881598698048, 30861.486110098886, 30880.32799454459, 30881.505941602467, 30882.695718511917, 30894.17006083224, 30899.585755194883, 30901.02753088293, 30906.972726916596, 30918.516073512026, 30928.86680324032, 30931.227688341245, 30938.127664859367, 30939.36397439111, 30944.507998854257, 30948.06532698513, 30968.027727795714, 30970.029747035416, 30980.499786772267, 31004.096629533477, 31005.164231497405, 31026.894866714723, 31035.762768110817, 31041.086186060813, 31044.363205599147, 31048.17129040399, 31052.58060074039, 31053.038649923506, 31057.97358121341, 31058.66720058584, 31064.7380154994, 31076.83061421477, 31084.07348349789, 31106.902642811554, 31122.796178480752, 31130.884153629922, 31132.111002240705, 31136.717664197364, 31155.363346131955, 31163.694910756374, 31170.523285264106, 31177.299948621247, 31179.50273674713, 31180.726016298075, 31182.136342212394, 31199.95798966897, 31202.168332834797, 31220.00190203256, 31240.219961793333, 31244.436043570688, 31250.21726931781, 31252.801132287263, 31259.773017323037, 31281.704665032055, 31284.21739124865, 31288.506282910825, 31289.44896117333, 31289.975892776307, 31305.413026522474, 31306.3568320417, 31309.071435725902, 31310.32148593121, 31349.206393215907, 31365.485944939093, 31365.60562191735, 31377.157317843623, 31378.30401206725, 31382.675414927377, 31387.636149954316, 31401.953619405715, 31413.390744453398, 31414.726792889494, 31437.081692039705, 31464.43132556436, 31477.085696075635, 31482.194234297793, 31489.08254087142, 31492.852266536473, 31493.289528537116, 31524.518497907753, 31532.668588264216, 31538.18771765224, 31591.647229967373, 31592.867685501456, 31611.99698725622, 31614.97666934855, 31624.899809696177, 31629.0478544343, 31634.484198953618, 31674.851153391613, 31684.07715554397, 31702.614044252743, 31711.1867200275, 31724.28932819297, 31728.21673648537, 31730.93616537185, 31739.055341200645, 31740.016333396055, 31749.88823484131, 31769.569919912017, 31770.789450631964, 31772.117691992717, 31789.40873109054, 31796.086039251233, 31812.385110670482, 31812.868858301503, 31820.27697995924, 31826.01301883347, 31833.567058734145, 31839.09222232583, 31846.303743009372, 31853.34021900701, 31877.730611497922, 31880.850141521845, 31890.88216505612, 31902.05762801766, 31907.226245543723, 31912.97134156169, 31916.87630932943, 31920.0045597739, 31933.891275500187, 31942.722241701766, 31946.9750354153, 31970.823488090504, 31987.077011320183, 31988.793140699046, 32004.335958540545, 32028.14479336274, 32030.092739199972, 32062.80932959512, 32072.446873066765, 32097.55489832146, 32101.274376620022, 32104.113885303443, 32108.5216143174, 32109.23764007783, 32109.846882667483, 32137.312066588176, 32147.9317667401, 32157.5829118444, 32164.729472885305, 32172.224025476466, 32180.404986324524, 32188.135751744558, 32191.92068758809, 32200.86147649761, 32205.28700454538, 32208.702079719566, 32212.7650540163, 32238.959332044687, 32247.01910959952, 32251.030983007386, 32274.324776767786, 32278.57721787948, 32279.441181787133, 32295.64055716911, 32298.337631466955, 32312.803385428964, 32331.6334675645, 32332.292278191126, 32338.773616378458, 32340.523243552474, 32341.649737867552, 32356.872852738594, 32357.185001719303, 32375.092835093714, 32388.685678293117, 32389.541317081905, 32411.10934069229, 32420.547704706012, 32429.53828903789, 32431.347941150383, 32442.40075751046, 32444.25452514875, 32445.17632765883, 32448.20613173387, 32450.45306304433, 32453.94465290584, 32458.62517302744, 32459.001203578442, 32473.135234014182, 32474.738138186327, 32481.153237700713, 32483.677644455554, 32484.625549941586, 32497.343297661566, 32499.142857596125, 32505.66937908658, 32518.43533617315, 32541.992176532807, 32550.087460465817, 32554.291440163193, 32557.584470750942, 32564.338554748458, 32581.13008423145, 32598.99723099866, 32603.41490915469, 32610.417588267825, 32615.887654621292, 32627.749659250087, 32629.576058121325, 32639.53732743056, 32640.68306709364, 32642.450450458873, 32649.123037948833, 32654.71159142322, 32655.88573652786, 32672.975085908292, 32674.284332901927, 32680.728041592003, 32694.13730113894, 32700.27209795165, 32701.817005389512, 32705.45397644927, 32706.596453218608, 32723.836767971257, 32725.802530762357, 32727.327410931102, 32730.182026762166, 32730.917979684615, 32748.856272033794, 32750.872322834766, 32775.83861132865, 32783.975692807166, 32789.194925397365, 32791.10599133479, 32801.036839324, 32801.53063973873, 32802.334709270894, 32811.999470957264, 32823.40681627061, 32862.405263600085, 32876.21803839985, 32877.46918090557, 32887.084901277216, 32905.38536400608, 32907.52636675834, 32910.69972946422, 32921.29403480434, 32925.392415895505, 32931.82788774062, 32938.16533705665, 32941.46303165152, 32946.89281479982, 32958.54837031227, 32987.228948802454, 32988.82553806059, 32992.40176725224, 33004.523532629486, 33008.44767146704, 33020.590023184915, 33038.655973494504, 33044.95861713537, 33046.47292467924, 33049.564539013314, 33051.05511575111, 33055.403493789454, 33061.719280846824, 33069.59917576539, 33094.97177515912, 33102.13549416789, 33106.755257523124, 33119.07807250416, 33125.76152942409, 33130.711635930864, 33132.05215268403, 33140.49040736349, 33141.750251737496, 33153.41388475794, 33178.8895713506, 33186.4533919722, 33189.31999356229, 33199.65348476938, 33202.43943851699, 33204.11539444721, 33204.28384841898, 33208.026377300164, 33215.66009307577, 33243.54219354823, 33244.27786815562, 33247.90333690676, 33250.30728242834, 33251.64254448548, 33261.482502199004, 33266.23219932773, 33303.16701941257, 33321.57996827526, 33322.39983263884, 33325.28587804898, 33329.46354565982, 33336.77314586259, 33348.88390414586, 33372.6967831484, 33378.082230443135, 33394.92691555686, 33399.718011344536, 33410.54062901174, 33410.80786813391, 33424.22665618154, 33427.8887586982, 33434.627769610284, 33446.21724599949, 33450.19031164046, 33451.93131166639, 33472.27503896255, 33476.311750844055, 33477.05675771619, 33492.01705615453, 33494.58925480526, 33525.95320937185, 33527.723359091484, 33545.99066291932, 33578.02098643986, 33578.02158386608, 33581.765355232215, 33584.248862499146, 33586.88990758872, 33587.86200317961, 33603.77480232685, 33604.169495442045, 33630.72077979858, 33644.018893432316, 33644.63245248175, 33646.14768709275, 33649.32920333583, 33658.95333279067, 33679.259986099736, 33680.63471702283, 33696.85447962617, 33756.7511751069, 33765.65585658567, 33769.37526059796, 33771.71563238858, 33773.86474651926, 33794.89413558537, 33797.97313953784, 33803.635860069895, 33812.11593534277, 33822.3757503735, 33841.78931241057, 33849.4695743909, 33862.16242874638, 33910.80024644525, 33911.21850961263, 33972.89786943295, 33985.23260755257, 33986.087074428215, 34005.51911591859, 34046.44238504196, 34052.56148521441, 34054.49363246694, 34063.89848982623, 34082.61344434162, 34113.55444345779, 34115.844847491215, 34119.90102440249, 34120.14798244998, 34120.179120312045, 34126.087555988444, 34145.48921363189, 34150.918213066805, 34153.03936660736, 34173.724540829164, 34178.89451771905, 34181.9023980546, 34198.578174203074, 34248.94590868188, 34258.17077292107, 34260.10490492806, 34261.45986161912, 34271.05821391542, 34291.7216853981, 34293.03154020015, 34295.81610082036, 34317.478025663106, 34319.98417609664, 34321.104280687665, 34323.22476403367, 34324.50858619352, 34327.89433731204, 34333.9661647941, 34335.38648717377, 34342.32947841079, 34360.535501526494, 34361.471538939215, 34366.90515335632, 34368.246925916814, 34373.996444897806, 34383.006938590894, 34400.992247573195, 34406.896116990145, 34425.41901819745, 34450.09879639984, 34453.68106272283, 34481.09672030428, 34496.315043376955, 34507.59135059173, 34510.741393657314, 34513.285943789466, 34517.46029923164, 34525.94043628517, 34534.723959512645, 34535.721811247466, 34536.987200251264, 34542.97385511682, 34547.19273418546, 34553.77333943841, 34554.14433370753, 34558.97104185577, 34573.84345365899, 34579.862539903195, 34593.384616970565, 34612.75559971659, 34612.93505340991, 34618.38399241728, 34618.73122407593, 34625.268364457195, 34632.08675465896, 34642.19382065636, 34643.69226923393, 34649.26179388166, 34663.42583059501, 34668.31038158569, 34668.64661078696, 34690.182368201014, 34691.31332297026, 34699.13027708102, 34721.55144967481, 34726.02932859135, 34751.9619586627, 34761.892441810356, 34771.059795224995, 34779.83732164815, 34791.83230827118, 34793.75217175503, 34794.81443950905, 34820.09663050315, 34820.2317026411, 34823.827627137885, 34825.12024119508, 34836.18422936596, 34849.80554414529, 34857.79239565434, 34857.84036902781, 34869.412291091045, 34870.95836642799, 34874.79356270756, 34878.68322831031, 34881.24526840671, 34920.19557143918, 34924.74000006969, 34925.57894685221, 34947.924444181466, 34963.57556505482, 34966.59812436189, 34971.64435387366, 34972.98192392901, 34986.351817211784, 34986.490877675875, 34995.32704994053, 35017.00747438596, 35017.261675771646, 35031.38088999177, 35040.263025508124, 35053.968759722826, 35064.9406731047, 35075.92604614886, 35077.90573535154, 35093.13789008705, 35101.94073034882, 35120.94063936973, 35126.237799313334, 35142.889502317084, 35154.25661477982, 35159.47243605518, 35162.238144641946, 35164.96088584298, 35196.25931864418, 35202.66996907454, 35208.171669428084, 35221.49190947684, 35222.110336345366, 35236.415392092014, 35263.96740130365, 35274.503190917385, 35293.1642468307, 35298.90403147317, 35304.054759219536, 35305.74453614876, 35306.26183664844, 35320.033045996825, 35321.75753986452, 35324.852723887634, 35338.76921041375, 35343.006150519504, 35344.37899491793, 35351.32198275339, 35357.96398901552, 35374.26583530193, 35375.77710291601, 35378.91987972138, 35386.10235857187, 35388.68702255083, 35396.27604304999, 35399.29507728867, 35407.131898736196, 35415.5941593229, 35415.82810085564, 35429.20678891918, 35430.94088023301, 35440.69823613626, 35441.357871253465, 35446.73638720026, 35450.46930578441, 35452.27726695498, 35470.881976786695, 35485.13135610918, 35508.54717268555, 35511.666178155465, 35512.69054951505, 35521.460904860294, 35525.857709594435, 35528.36589360299, 35540.09939012272, 35552.06411580287, 35553.65729185518, 35571.4666283288, 35588.52622312952, 35605.78218483841, 35612.96608295856, 35628.57836177943, 35637.549753984465, 35655.58954032922, 35658.36467802392, 35680.5040261042, 35680.54743109789, 35687.14006626069, 35688.61837010059, 35699.412174471116, 35702.6548428788, 35702.87588730093, 35705.73149478416, 35712.133206316445, 35716.447155112655, 35719.231929099056, 35741.76285647531, 35765.77146787608, 35772.812398811984, 35773.09600818754, 35775.02441939076, 35778.30864292048, 35809.754790185136, 35822.02771350569, 35830.1895991413, 35835.26619508788, 35853.93886564005, 35859.87374874992, 35868.723264572356, 35885.216377266974, 35894.32781065648, 35894.362579094464, 35900.87759224434, 35900.90229563536, 35914.4312738944, 35918.119498477805, 35924.96803632162, 35927.98327722722, 35929.49821262177, 35967.036757989954, 36011.8859248596, 36018.23734664166, 36035.41902847277, 36042.61566653199, 36061.891926800454, 36065.015669483124, 36065.183428722405, 36069.08333044697, 36070.11267319517, 36082.71581450778, 36084.61786950778, 36088.61039159646, 36095.680984471015, 36125.27735887983, 36135.26304642969, 36162.27916946993, 36169.13342950857, 36171.76663331507, 36173.09828481118, 36183.881726558466, 36187.344291543166, 36187.46136920862, 36188.05000896085, 36193.15241117132, 36202.49957830425, 36202.747245189894, 36212.995158571735, 36214.70102285607, 36217.136847504175, 36229.38654676631, 36247.93898429834, 36283.39943102787, 36283.93239756685, 36287.7735521279, 36296.97907639462, 36299.905839351086, 36303.48506727247, 36310.32594635881, 36324.76176107473, 36338.35274594219, 36342.631630251046, 36345.18176337526, 36351.502352992204, 36353.30965120328, 36360.868498026124, 36367.96574711897, 36381.014671610625, 36384.31241978126, 36388.97050052755, 36395.006191287015, 36396.86559403729, 36401.04566170942, 36402.714847830066, 36407.992485799834, 36411.415898549654, 36417.80208426847, 36423.204603301616, 36508.78395898337, 36536.7641114408, 36541.64858569916, 36542.94179421598, 36545.84173944067, 36548.27488301882, 36549.59500068325, 36563.32101434993, 36574.92998739176, 36589.93954038445, 36608.14434799716, 36648.24914630016, 36649.18757569791, 36657.24068653879, 36670.29387335287, 36671.673162783234, 36682.09306823401, 36686.95895586785, 36698.462269463875, 36707.23437529467, 36710.454090400104, 36715.97645140236, 36722.319941671034, 36730.36148450961, 36731.74591917172, 36755.784545078386, 36775.64983326674, 36776.55563716827, 36778.68965380793, 36786.22670399136, 36813.19420305501, 36822.61966012694, 36823.3646745438, 36823.65408259422, 36830.34606324968, 36834.6485674975, 36841.05701858783, 36856.52439616442, 36860.086215113886, 36868.11030970141, 36875.53589906463, 36881.76458053232, 36892.3493952156, 36903.029655983184, 36921.404633406026, 36921.4180463808, 36928.44721016632, 36944.15361850122, 36954.713562444646, 36983.87374025413, 36986.775192620065, 36987.520698510765, 37003.24525035716, 37003.368905908894, 37003.960052698916, 37009.70506218537, 37028.36438441449, 37043.83128996706, 37048.96658246502, 37058.65599977265, 37062.560434960236, 37068.21999642883, 37072.93341988269, 37081.53865953996, 37082.58825163728, 37087.51784991267, 37094.69450028618, 37104.33439042257, 37112.741203374455, 37114.73992900412, 37116.91024801293, 37128.021144381615, 37160.826801183095, 37198.01718377404, 37222.16563823902, 37227.189484276794, 37229.939736373606, 37234.2315553064, 37260.93895799093, 37268.69560607463, 37276.00584252419, 37293.21835199151, 37308.90498517814, 37313.76875907343, 37317.82581750542, 37318.94579372697, 37331.96849788486, 37418.512454165604, 37429.202010014844, 37429.3374179716, 37462.110216947825, 37462.89405027019, 37474.23967640458, 37478.78011432642, 37479.41065889032, 37495.95439971579, 37522.742836999576, 37529.78196278651, 37545.482658412344, 37546.38301669345, 37550.59080292724, 37550.59867834028, 37561.87266549396, 37564.887136961115, 37573.857989361655, 37574.9297435952, 37587.541988523044, 37599.33714772154, 37614.58863470051, 37618.44549617189, 37619.15941515069, 37624.60282270669, 37625.657300500476, 37639.73735751822, 37650.12292838891, 37654.79059216043, 37658.574036120095, 37661.48606599564, 37663.50178202034, 37669.12290850096, 37674.54510866612, 37687.02727160487, 37696.33011034998, 37706.13683082731, 37709.1296512243, 37716.567512561574, 37729.16883465666, 37740.83975956331, 37748.91953078623, 37753.80013635801, 37761.13392649685, 37764.477876739, 37768.42566563505, 37776.834057440516, 37781.73103952486, 37784.557340522995, 37786.664045034806, 37792.19603752506, 37811.087202602605, 37816.18085537092, 37843.7734296487, 37856.375436172086, 37858.62989300318, 37885.251964143456, 37891.63551922272, 37913.3782632083, 37923.781545789134, 37944.07195616276, 37944.92451229477, 37958.3299166153, 37958.40734516654, 37971.997832594876, 37984.509233852456, 37987.40053159547, 37987.44842100385, 38007.655743289426, 38013.018385747135, 38024.68761868512, 38024.958516214465, 38047.07824112294, 38056.965692048194, 38057.023421968006, 38075.158581020514, 38117.27959089127, 38138.18685447067, 38155.28701265542, 38160.44541210757, 38170.33642868738, 38171.865708259465, 38172.14499133932, 38176.145660924936, 38182.52221027491, 38184.55600304737, 38204.45255749902, 38206.80575945818, 38209.714289610696, 38209.78970141485, 38219.29856305533, 38232.65620031589, 38234.79509464713, 38253.35386857122, 38258.287533811905, 38275.9533800019, 38290.108071945586, 38291.99682493951, 38300.24537331602, 38321.3621197125, 38323.737332436736, 38347.31240109006, 38350.29936340368, 38352.91726775762, 38355.00551916861, 38370.53625306245, 38370.94496305451, 38382.9419958885, 38393.5226244917, 38407.09449800109, 38409.04031283749, 38409.93387105845, 38414.00805507951, 38414.09524049256, 38416.948163620335, 38420.449223024385, 38424.265011900265, 38432.161754212335, 38440.279584123906, 38453.577085008255, 38463.969387383695, 38476.98382737431, 38481.2749466241, 38481.326023343805, 38486.85050690096, 38488.345340477936, 38492.787993171056, 38516.64454718585, 38532.07873707455, 38544.47444699267, 38544.96736467798, 38547.3645285643, 38554.44760837615, 38595.12384251384, 38605.02412980895, 38624.67537870369, 38629.813705776636, 38634.26034765835, 38640.04523811532, 38646.80558136306, 38646.973974954584, 38671.41282125181, 38727.0821567492, 38727.178928087415, 38740.13271685793, 38745.70344502434, 38751.03282636129, 38754.61831273553, 38757.70656028064, 38769.97258387431, 38783.83028756372, 38788.558377055255, 38809.38649286483, 38820.52479162994, 38830.262871750965, 38831.3626499753, 38833.1472543341, 38841.38742623892, 38844.07678845617, 38848.944188624584, 38855.7893333887, 38872.99344560139, 38918.01133492433, 38923.570362529426, 38939.08640538892, 38942.736267370754, 38947.81322504694, 38950.902476280986, 38963.028400060546, 38972.06003142283, 38978.778045332365, 38978.98218413401, 38995.97399113406, 38999.30822227929, 38999.448541693404, 39033.72031632425, 39039.23721100915, 39049.32623238634, 39051.4003791545, 39052.69372687513, 39056.750777046465, 39067.06062519573, 39067.19644450191, 39068.27767627772, 39070.61510036521, 39073.42139764192, 39075.16409608611, 39078.43137158053, 39081.63766098492, 39082.66175076598, 39098.92977177292, 39108.2418037953, 39109.785474456585, 39132.72837505141, 39134.75956598867, 39146.24312806883, 39147.73721616756, 39148.32981832956, 39152.042168847154, 39160.33496127341, 39163.24107438511, 39167.08515722595, 39175.91469532697, 39206.17369711839, 39211.21101666166, 39214.511965161924, 39217.58190571623, 39222.429966239186, 39231.70799188713, 39242.866877990615, 39263.39751192355, 39267.7461246852, 39271.06780523882, 39281.75479080288]

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

    X111111_1 = [30346.179366430253, 30354.744580204682, 30356.65835459968, 30358.046089680633, 30361.489583954586, 30369.984568927244, 30384.542932995868, 30401.33482966591, 30402.69623014414, 30419.76240831004, 30430.45129997227, 30452.42189885568, 30454.597041942565, 30458.091576048297, 30469.437317336426, 30470.031094690763, 30477.523681297087, 30480.533607634967, 30493.166451966983, 30499.41936369921, 30523.605000068415, 30541.09659312541, 30546.465197839905, 30560.505524164608, 30568.78664846531, 30584.986834603962, 30600.999084379655, 30602.620198727967, 30612.641525236973, 30615.457753718398, 30621.05398176345, 30638.922704428896, 30640.646875266717, 30640.769944459837, 30645.99219060284, 30650.09893638166, 30663.247465960725, 30680.08163213618, 30681.508628105486, 30700.035588918934, 30715.714960346715, 30716.15429001965, 30717.61467191304, 30717.825399398876, 30724.83280875143, 30728.256722654576, 30734.105775002172, 30735.65379012174, 30738.354009030576, 30757.05228455091, 30780.5254939812, 30781.736118058485, 30789.36723549925, 30790.41475838803, 30790.5655822297, 30792.63507651996, 30808.72133792738, 30811.090754579887, 30825.122405582588, 30870.67658422212, 30881.951705946987, 30882.20810837279, 30916.652202584053, 30924.91960063205, 30935.07988998235, 30935.907530091616, 30941.46954267568, 30949.57027030199, 30950.973831899482, 30957.736737207313, 30973.0685994077, 30989.810510879317, 31002.20249285059, 31006.87656279347, 31012.461401245753, 31033.179590567142, 31055.78922782221, 31076.212432561522, 31086.957245965637, 31098.57641359593, 31099.959001422867, 31104.532167039393, 31105.149329655032, 31120.753732883288, 31135.136392247747, 31136.743982997257, 31136.793590641122, 31147.39380142417, 31149.97488250598, 31158.4361286413, 31167.915799702103, 31183.103895452485, 31215.450258755554, 31223.96576859964, 31279.5690450955, 31284.622691666547, 31284.78843921843, 31291.40821556855, 31314.532763980566, 31314.771891124736, 31327.76352325414, 31335.40046870645, 31341.703965496094, 31355.330686185847, 31356.897067148606, 31368.894988920332, 31370.725249597926, 31382.7498489059, 31387.73363209016, 31393.536696837684, 31396.81739414525, 31408.524157288073, 31409.76860232641, 31421.454672201893, 31441.357692379548, 31444.19828739876, 31444.52862864619, 31446.098289508584, 31482.85570889038, 31504.73781837882, 31520.719714819683, 31527.828773039804, 31531.010902192855, 31553.956792706304, 31554.20394318936, 31555.332242264227, 31559.186007059143, 31563.295844578526, 31565.575808229067, 31568.13917678649, 31571.035887940507, 31580.419459163702, 31584.9413443489, 31596.319202395698, 31606.702900038847, 31616.2087580555, 31624.200350612973, 31643.467423368817, 31644.734265090963, 31659.83687020851, 31680.26406623108, 31684.958331723108, 31685.693993279812, 31687.595951494943, 31688.888660351608, 31701.263449876667, 31703.42095990721, 31710.5612277444, 31710.86228939947, 31711.38924395048, 31715.53195476614, 31739.90579400578, 31748.4604263962, 31750.57212126889, 31762.94277883255, 31767.526448721623, 31771.203382156506, 31774.436463083384, 31776.85615600533, 31790.457003609044, 31792.196117003605, 31793.02326434397, 31795.419872479964, 31802.71088578754, 31804.46643389741, 31809.81363693566, 31815.791479499498, 31829.011682490585, 31829.99754079237, 31836.724465952822, 31836.85225429371, 31854.617062513506, 31874.98180856143, 31881.338393996048, 31881.4758574584, 31881.766464379703, 31886.93725785087, 31897.922849325678, 31907.589241197784, 31913.955031191388, 31915.997723547654, 31924.368268314644, 31928.335831200944, 31934.48671109178, 31941.22154489252, 31953.31727297862, 31959.716928515245, 31980.298167755685, 31985.255664932054, 31998.6158751954, 32009.39748453381, 32011.16752096743, 32013.106663952804, 32030.89883151388, 32039.541206082322, 32042.536916623772, 32044.220735420105, 32075.995312450035, 32083.846289460733, 32084.339061847975, 32086.21799849768, 32095.07122237346, 32098.086910776685, 32105.60378074807, 32113.41578089187, 32116.476407991417, 32129.35803033813, 32131.141012455955, 32136.36209793145, 32141.67366540353, 32142.207211748384, 32149.333612489234, 32154.717739684984, 32164.95400882109, 32196.196978074975, 32212.040063403372, 32212.47603139871, 32221.23426440063, 32224.98753588391, 32239.910031798827, 32243.396211259966, 32252.299107231618, 32257.45645962895, 32258.818750355247, 32260.414321695207, 32272.018282091554, 32273.875194362226, 32309.323401372796, 32325.82177216765, 32336.783599447834, 32337.756429608446, 32348.071546325344, 32348.502856114465, 32351.291767084713, 32376.695146482638, 32384.96399360676, 32390.725295102166, 32390.910456215006, 32396.107075394448, 32397.879619269, 32404.282943780578, 32406.73284425359, 32415.207812223493, 32415.85164577428, 32419.904921848494, 32427.851975933547, 32440.38470861832, 32440.88277874662, 32450.77008657987, 32452.306558897195, 32487.264679692584, 32493.032315486682, 32504.101233696725, 32522.099515184775, 32526.939687916674, 32527.440404339213, 32532.673136803853, 32553.881227989863, 32554.608252420192, 32554.762806508938, 32558.92121551645, 32561.68115319078, 32562.67224714001, 32575.324747274222, 32581.945266285908, 32586.437834602802, 32590.309977167613, 32608.226014816522, 32619.641462285457, 32620.0735866184, 32623.55626119756, 32627.441133402335, 32649.000316756334, 32659.381063276458, 32666.97022494962, 32687.52619348043, 32692.993303616797, 32714.02003911087, 32729.409484620763, 32733.341237958877, 32736.857273987825, 32754.820260680077, 32756.116169074478, 32761.076656338028, 32764.157049878093, 32766.44822801595, 32777.9571245148, 32809.72417328346, 32815.60830844488, 32818.307004410584, 32831.0818984021, 32831.135079783424, 32859.58718733141, 32865.21023166165, 32887.8429091602, 32894.753826679094, 32896.92010410518, 32904.92222630019, 32908.588098656655, 32910.29643025927, 32911.62951586817, 32929.86446588651, 32932.59289140749, 32940.44708360567, 32951.750338738624, 32967.900126273285, 32978.75946242283, 32987.36898171557, 32988.89352977389, 33014.38124096023, 33049.9608352714, 33057.64834316587, 33070.42475031255, 33072.2776877948, 33080.49782189366, 33088.93348909599, 33117.616285025695, 33142.46533805729, 33145.43609339127, 33167.489890471945, 33170.96804365933, 33181.83232755333, 33182.058206781614, 33183.23561766326, 33184.19606932351, 33185.580554213935, 33189.993009811944, 33202.70597709072, 33203.02360074447, 33212.88276077138, 33230.35905092499, 33232.328919793465, 33245.43368114341, 33247.12951494647, 33258.55779073048, 33260.58052049517, 33274.264904589494, 33276.25287312033, 33280.58819044308, 33289.00554930523, 33293.38111484942, 33313.27249150007, 33322.59234174894, 33327.302679330955, 33348.83384835241, 33362.304320677664, 33384.65490392156, 33386.433125380376, 33420.58254863067, 33429.15796371146, 33440.0136091231, 33442.571089943005, 33450.302589139246, 33454.253346063044, 33459.54003876394, 33472.83810768841, 33479.67279590396, 33480.283702425084, 33488.01023190749, 33498.13973984931, 33503.075982465205, 33503.67368856963, 33506.102948587184, 33511.98597166633, 33514.33419794047, 33518.409570434254, 33522.81606962176, 33532.41348931067, 33540.003937133915, 33545.217942366624, 33610.125379501675, 33612.64746910641, 33621.7324278948, 33627.27167215744, 33627.61531872043, 33629.62194332103, 33630.36917450458, 33640.57065608045, 33643.28726464215, 33646.811201410856, 33650.177829531174, 33651.95347555811, 33660.785412644305, 33663.385326031705, 33664.6483980483, 33671.89335201938, 33682.338054950655, 33683.99298951897, 33688.45065709844, 33693.411015746526, 33716.41705477642, 33734.830380782725, 33745.63792060052, 33778.3527723548, 33804.14630539448, 33805.76244650676, 33810.03297693693, 33811.74108422741, 33814.32520768738, 33831.050432465745, 33837.16283829179, 33838.19431504625, 33856.25613579547, 33857.704926248705, 33862.29097160022, 33879.79869269387, 33887.23860188941, 33908.30614708411, 33914.73016823338, 33926.2140281118, 33941.336069200865, 33943.807274145496, 33957.26049607633, 33963.74378930288, 33984.69994762394, 34009.82360031916, 34011.258080201565, 34013.12947766688, 34032.09769046986, 34033.87539341604, 34035.736353965796, 34035.80255459763, 34036.748577696715, 34040.564401102114, 34044.186725279025, 34056.86204736173, 34063.62419088333, 34065.42985408542, 34072.43554529063, 34072.9863276415, 34075.82426036977, 34091.324146248124, 34092.41756512599, 34099.292370421965, 34101.45476785844, 34103.14044063333, 34107.294171154324, 34110.88088233613, 34115.36204012517, 34135.03065158147, 34140.4025429314, 34149.66480920219, 34168.54843634821, 34168.591544774674, 34170.83435987346, 34172.223385082085, 34185.85650585542, 34188.52470742319, 34191.931817081204, 34199.21029711292, 34212.48498135598, 34219.74781820349, 34227.28395792486, 34233.44431002839, 34235.880945229546, 34239.10405800455, 34280.71625798198, 34281.30624153267, 34291.14378231134, 34292.07685034975, 34313.67470548856, 34343.530052608614, 34356.840314592264, 34407.01928831381, 34409.46924563818, 34428.00603994963, 34445.37725398737, 34450.21955990674, 34455.98147677801, 34459.97599582094, 34490.08404884307, 34495.27862400072, 34500.77677724318, 34504.56972733861, 34506.95210754589, 34506.98949824027, 34508.949407339736, 34514.49388628335, 34525.17073746789, 34529.03788788004, 34534.12214450941, 34534.59806100202, 34539.410002494085, 34540.08922648242, 34542.70629456232, 34565.375147283165, 34574.88052833765, 34578.88486477062, 34588.07942936771, 34591.726914996674, 34602.63906620006, 34624.46137009161, 34625.22969918727, 34637.363300474084, 34638.3052428879, 34641.569200655955, 34655.06781461681, 34685.61591811924, 34713.479096873176, 34717.19352507598, 34717.72424968386, 34721.07770836666, 34725.86154637293, 34732.68152382966, 34752.8463967681, 34761.8355829428, 34805.0914899756, 34807.34848182157, 34810.679527342756, 34812.980830699686, 34818.41282090809, 34820.594946743695, 34837.82252159969, 34840.0979795175, 34840.46773720928, 34842.12362887405, 34846.38856150151, 34855.90231351394, 34856.645243342646, 34858.592192105854, 34864.84999586568, 34865.90345955665, 34866.551804412564, 34870.54235329428, 34871.64247972339, 34892.04359789862, 34900.48442612258, 34907.663836488486, 34908.025397689824, 34920.47319736889, 34951.960684404745, 34956.44861612505, 34964.5331724874, 34965.22181796513, 34991.04281855715, 35000.03422572976, 35000.9927091006, 35001.48068272032, 35012.448563650716, 35017.69448062092, 35023.10303569026, 35025.520474388104, 35025.582166850414, 35027.59219083201, 35046.61052024592, 35049.70885714169, 35051.866493847905, 35052.965261171776, 35062.02278260427, 35069.320253089296, 35081.428549365555, 35098.0559037699, 35128.083116560825, 35129.40766426337, 35154.18404720027, 35174.50196211668, 35190.007737783264, 35200.4999606681, 35205.396813552376, 35222.747874705114, 35223.91077942052, 35225.35793416368, 35225.677569490756, 35235.0431630159, 35242.6442531548, 35246.452087315265, 35255.35270703878, 35258.47891872818, 35264.91916344124, 35265.27112328454, 35266.21149461468, 35268.081841140156, 35274.89228441666, 35282.60777700533, 35283.42739656285, 35286.98933201256, 35287.753988225035, 35288.24522482503, 35296.48608615396, 35302.58682245275, 35308.7567529767, 35311.42535885003, 35320.48755553018, 35321.11989227642, 35336.321479609265, 35355.04764216742, 35370.844067356586, 35371.84587500708, 35377.47942530961, 35378.59612814815, 35379.37959351243, 35380.60253541065, 35389.42303279334, 35402.97060939033, 35421.72914746857, 35422.24784408298, 35444.69640059803, 35447.850870020484, 35449.79767294024, 35455.92908903828, 35460.551752077765, 35482.15559928745, 35488.76984074688, 35500.10258730321, 35503.28836466971, 35508.241095297155, 35524.06261119057, 35524.98910611235, 35526.89671007403, 35531.693840321226, 35540.98566094045, 35555.34151998341, 35560.498692618574, 35582.06746019668, 35584.978188980866, 35592.60688115851, 35598.45778987315, 35639.255483266585, 35640.29946620755, 35657.275657882376, 35659.84980718452, 35668.76804599217, 35676.26197195011, 35685.53893210646, 35733.83040090734, 35738.387752666604, 35756.268508113724, 35756.97711058051, 35786.19234079949, 35786.43428895784, 35790.47478251766, 35810.69825466579, 35842.58878569059, 35846.735391629, 35856.025860147354, 35856.6435261781, 35857.37600018814, 35864.83402501411, 35869.992643589176, 35887.938600475914, 35896.71387005461, 35916.98641031424, 35926.05525201965, 35931.89989645345, 35942.82461762354, 35956.15298276976, 35970.08030979767, 35988.81593134224, 36002.28159926244, 36016.046205137325, 36020.70859295783, 36021.009805777016, 36026.869849013194, 36038.505099099995, 36046.62677951972, 36050.46640614347, 36051.86511721021, 36060.613840934886, 36068.271960408594, 36093.128070594874, 36095.872459316546, 36101.708198076034, 36110.118592166305, 36150.21118128193, 36151.55476579858, 36178.42986368365, 36183.5627635058, 36185.32782097919, 36209.93990371172, 36231.76755292389, 36241.15980918587, 36248.89061534518, 36257.78550528745, 36288.46220740959, 36295.90188846644, 36303.737866416035, 36327.86910785483, 36347.47418809482, 36362.03263321676, 36364.12704002958, 36364.22812671751, 36371.262977895574, 36380.35427351392, 36385.05367354404, 36396.32982775132, 36398.48876905958, 36412.69496119445, 36413.49177436705, 36416.45683600761, 36424.6621385293, 36426.69434140467, 36434.342072983876, 36437.314946104, 36448.57451413012, 36457.08291037442, 36468.56121491926, 36485.72374852429, 36486.54398540342, 36488.68994251536, 36502.3289585187, 36507.46581065581, 36515.14695870143, 36518.66426101594, 36521.060422010225, 36538.63640967226, 36559.71865326692, 36570.90173026258, 36575.09515666831, 36579.103682211804, 36583.90951045076, 36654.785965760435, 36663.51692996686, 36693.29826040329, 36699.9548787708, 36718.389707779344, 36723.81965906077, 36724.09239089863, 36732.928348170004, 36745.42198716781, 36750.50875015099, 36761.68175653853, 36769.64764822238, 36781.40833025506, 36784.896631474054, 36789.65922792123, 36817.12449444971, 36833.810123571624, 36849.21661743431, 36859.249744796696, 36859.60114207002, 36862.860904552705, 36882.054564312464, 36900.899389964296, 36903.4820165093, 36931.2185142699, 36938.77487990486, 36952.93170129569, 36969.27908666639, 36977.64620662513, 36981.032530772434, 36993.156772318776, 36998.487223883996, 37000.44572465304, 37010.32182498654, 37028.982195891855, 37031.19161369273, 37033.27287939873, 37040.19276987093, 37047.63632298524, 37049.43119761433, 37055.05686334768, 37057.4419008089, 37068.650134878946, 37069.183173289515, 37130.48726217101, 37132.29411065064, 37140.32254466919, 37148.27531605687, 37166.902622643414, 37181.51774941021, 37210.44054744789, 37212.38100674374, 37217.05918138661, 37217.293928821295, 37219.84383348492, 37222.34132143162, 37235.349036688785, 37244.33049011636, 37251.85768352985, 37255.920269300506, 37257.58838475756, 37264.08748426477, 37272.15251265253, 37277.511452323335, 37301.939190791614, 37304.14549682941, 37307.4204411783, 37311.83885745588, 37328.25468724488, 37328.72346707691, 37349.92678860373, 37357.55201274277, 37361.230163224165, 37363.58597046776, 37365.34653950437, 37366.16634352726, 37367.98528644637, 37381.752193083106, 37385.76168952725, 37412.31352581503, 37417.479437556205, 37419.69298560668, 37432.16302661435, 37444.26430852435, 37450.65831850282, 37455.42992852883, 37457.530492800404, 37461.12638286935, 37465.708601429964, 37467.458378946845, 37472.08215257845, 37494.48903492662, 37498.65009620188, 37530.27805414115, 37535.97171219214, 37558.737052921155, 37586.47766837533, 37590.88617025968, 37595.303861381486, 37603.86052967166, 37641.70444168869, 37665.957551050946, 37672.67122359904, 37680.81441249258, 37683.32542521695, 37687.13147603438, 37689.7937676607, 37699.502439358395, 37720.5379113379, 37721.504393752206, 37734.594260263, 37746.68255239783, 37752.211217215096, 37752.969501626845, 37762.22971734775, 37763.115905951854, 37770.0120795419, 37779.313195322495, 37781.709253020425, 37785.22173744278, 37792.90301241846, 37806.60823583171, 37808.75884180698, 37810.96456294894, 37825.52639795773, 37834.413706766034, 37841.192897250425, 37850.122304088356, 37854.574031288954, 37866.73638838252, 37872.64083861374, 37877.217516962635, 37883.40566311918, 37886.92156720032, 37913.98777732239, 37973.0279555936, 37984.35342444996, 37988.42464896692, 38002.19646075593, 38012.16321240015, 38037.85174711129, 38041.22145170862, 38047.1888946993, 38049.6782677895, 38064.18228843558, 38085.29304514167, 38092.61253470393, 38125.424661301506, 38126.363994385916, 38127.86128672979, 38128.44634271125, 38130.353774015355, 38138.686915685095, 38140.479849857875, 38143.0645963758, 38145.0508784527, 38146.39571750765, 38148.772157839354, 38159.998271707416, 38182.6531762914, 38192.36634234385, 38195.371018798, 38207.17996031426, 38215.9613188683, 38219.51589755904, 38230.29717780266, 38238.01374777645, 38246.202560869344, 38270.73568505177, 38278.622695445614, 38314.83496555393, 38319.275596685846, 38330.95835792327, 38335.12047261261, 38336.59567842431, 38343.96798606431, 38347.9274881071, 38352.98192099676, 38354.058758803265, 38359.16547634141, 38371.50710364876, 38374.34742497801, 38385.99821232944, 38397.87513507326, 38398.964399754055, 38407.06556562284, 38416.97165025651, 38421.38199924066, 38436.00975694159, 38444.697311935255, 38457.54802765675, 38460.77556867573, 38477.51789423176, 38478.19613539554, 38480.32749377635, 38497.714189101855, 38497.875048713744, 38503.27240811518, 38522.05777416769, 38530.62611322885, 38531.454840858256, 38533.26394459392, 38537.589744233985, 38542.91284053807, 38542.99508962204, 38551.98864427076, 38553.17175813262, 38583.11517595954, 38583.44755550744, 38586.35640073896, 38588.96133300918, 38589.402785347425, 38606.76458571616, 38622.93412467149, 38629.61384813981, 38632.36583238836, 38633.77135138015, 38643.93041437464, 38650.92992258563, 38655.08576666648, 38672.776255922, 38685.76878590022, 38692.873915407916, 38693.13571993557, 38694.878224821805, 38699.25240706357, 38721.96659597941, 38723.83533668801, 38725.35098995903, 38727.04505126555, 38745.07525051675, 38745.8476495958, 38779.296499272525, 38783.30777274251, 38786.00121830779, 38803.88172060362, 38813.50255429607, 38828.88670713048, 38846.58626295773, 38862.789495639096, 38863.4134694136, 38865.06158739962, 38872.126946034135, 38873.28910835343, 38878.54326945912, 38894.178690904344, 38899.80860160415, 38904.73857194254, 38918.47151365911, 38930.872560663156, 38933.57997283798, 38937.7147299566, 38945.555292463825, 38949.769801629904, 38950.88506137831, 38973.49072680314, 38976.84611710906, 38981.97710350468, 38988.21108095745, 39021.772872183865, 39040.27456493155, 39056.49614157646, 39058.956095320995, 39065.15465306514, 39081.25212207727, 39089.217826780885, 39106.120238343006, 39116.77512400145, 39120.661298998195, 39123.29610795897, 39130.24223839814, 39133.532442167605, 39133.9715313096, 39159.77020678067, 39166.74116760535, 39171.91201818842, 39175.45701009246, 39180.99200718443, 39187.00260184491, 39211.02708414654, 39214.43442245046, 39221.28632230398, 39233.492554221935, 39235.56347317161, 39247.83856960393, 39251.87439198224, 39254.92040497437, 39255.38514693217, 39269.65168879185, 39273.4550199781]

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

    X111111_1 = [30334.60420021434, 30341.37345514279, 30350.260010498016, 30370.95050402994, 30386.85515357222, 30389.91626457677, 30394.531397216753, 30401.319281244327, 30410.30479703814, 30419.31256940751, 30428.279212745383, 30430.870430202263, 30446.002726733284, 30447.141180010407, 30460.18482679667, 30482.721500675794, 30503.33376453623, 30504.377452520635, 30532.981927788103, 30537.66395750215, 30553.524539949387, 30562.97344893605, 30564.70684062667, 30565.982664434996, 30581.42435178448, 30583.63626877573, 30587.705390982883, 30593.988185081456, 30617.106105703864, 30644.23154688727, 30657.314002588897, 30662.619302113693, 30666.217173393223, 30689.403004697277, 30701.50091021537, 30703.979347885084, 30718.83484926953, 30719.267591139265, 30733.510360941033, 30733.993371821216, 30751.387355662915, 30760.165248802547, 30761.977747348206, 30773.900948009756, 30774.07975577262, 30779.440704511824, 30786.901304350507, 30788.244385902264, 30789.27085248325, 30796.697467273127, 30801.618656201535, 30807.50705217233, 30823.60178218412, 30826.162107972596, 30828.997315705605, 30831.83009452934, 30831.986164683916, 30833.231699827415, 30835.29119401927, 30835.96133425129, 30844.945213711468, 30847.619782550577, 30870.205403768112, 30871.085795623887, 30873.99166758253, 30875.136794295784, 30890.334816591327, 30896.6706144561, 30907.338455977766, 30921.523722563754, 30928.858657571687, 30947.294308561803, 30951.275595709667, 30971.99737154756, 30974.031230540622, 30975.305873821635, 30981.043702835635, 30989.42904312938, 31000.934751892044, 31002.13588492091, 31015.085620166006, 31022.72949256848, 31026.699789110167, 31045.76244374787, 31069.04151973914, 31079.767905799305, 31081.000837680585, 31089.11231630164, 31089.785213447103, 31090.940427477013, 31091.893624779375, 31110.953545311313, 31138.455889173776, 31158.95422322878, 31169.797408862738, 31171.290333743447, 31173.625586156555, 31177.7889131826, 31181.754940921324, 31187.822018573446, 31196.155481894897, 31198.22485139315, 31200.31512237859, 31223.303958219036, 31232.456130342336, 31253.518796592278, 31259.742903008257, 31279.19876402988, 31296.738773977893, 31297.87978263703, 31302.277411241146, 31304.081082884688, 31308.687930896656, 31320.979827015242, 31350.428107650616, 31368.93866866877, 31379.09295778801, 31380.09326401297, 31391.097904094695, 31408.17509219334, 31412.214477540085, 31425.943219879977, 31430.601680335567, 31434.66930212605, 31440.37588931079, 31448.793343283756, 31449.120247072515, 31461.19928309918, 31463.78005702248, 31467.752438868843, 31499.81173888625, 31511.477412927856, 31514.586618928508, 31524.950282810474, 31528.250655961, 31540.3070732518, 31543.128449615775, 31549.622496540032, 31563.57946379366, 31572.601076495535, 31590.879930174684, 31593.56972105513, 31607.6064658948, 31619.42918317986, 31625.945769334645, 31627.47301842212, 31644.21206710978, 31659.277512676894, 31660.007908776824, 31673.75819093806, 31674.826208351362, 31701.57056021186, 31703.74593252746, 31713.721432550417, 31721.193718721748, 31723.867269193885, 31732.49380832903, 31750.007906969495, 31763.767892459095, 31768.54326984729, 31774.44974311666, 31782.136914509883, 31783.478566117265, 31796.65213246218, 31814.61345262303, 31817.118348763554, 31831.658803879043, 31858.91928547194, 31859.240063761747, 31863.87955701303, 31866.932565723433, 31871.15437688465, 31877.487259975864, 31895.460567863676, 31895.978937322318, 31899.037456153765, 31908.990607366133, 31937.440018203273, 31950.798063186565, 31970.945407534204, 31975.76599402763, 31984.763816979645, 31985.556855129777, 32017.81659521324, 32027.14453580584, 32051.003163017544, 32060.31033874318, 32065.314112129676, 32075.33500999889, 32082.59964942211, 32090.77657077698, 32106.168378479306, 32136.562552391035, 32136.98960573524, 32141.74131223155, 32146.329922823326, 32150.366750980753, 32159.799785548646, 32160.247879040453, 32162.284337331705, 32175.36787898648, 32178.13919096514, 32187.163054828245, 32195.83812834415, 32208.478118776176, 32214.18284421425, 32214.7920460566, 32215.55034363819, 32222.847458456883, 32233.791179356343, 32241.01923335471, 32243.249842674708, 32249.948707434243, 32265.6983920747, 32268.441671822075, 32274.46441428514, 32278.955642894376, 32296.771319883, 32301.321918074333, 32338.455866317097, 32345.02586695395, 32345.078292258906, 32345.80682656154, 32349.941218317552, 32363.086608276342, 32368.59469308106, 32369.41367919376, 32371.743385167516, 32386.44826299034, 32396.215265891136, 32399.3591129142, 32406.02388556178, 32406.7410954239, 32416.705361218515, 32436.73744276051, 32453.245161117815, 32455.29774315968, 32456.595197535225, 32460.17453441899, 32467.208444167485, 32468.556756418027, 32483.215871073535, 32484.563308017907, 32485.47515926214, 32499.998851256623, 32506.679168693656, 32533.54573666955, 32540.40880252047, 32542.22189885781, 32553.779175396314, 32560.108278764023, 32571.541413558345, 32572.62479812019, 32573.518277698004, 32577.475538740648, 32585.377032900833, 32600.768924773474, 32619.683557200176, 32620.051474478765, 32644.61690843425, 32661.392998597938, 32669.038534950396, 32671.174664085618, 32677.122610475064, 32681.23177829974, 32705.869418499435, 32708.886595299213, 32716.25912589046, 32738.117228253694, 32763.786550230117, 32779.966461446194, 32788.86570284691, 32791.925846638755, 32825.12581110566, 32825.51243815169, 32829.28360390313, 32845.641008531304, 32848.1393136391, 32860.23936944403, 32863.809507578655, 32864.57861529254, 32875.76196534525, 32888.169578196925, 32894.283485348504, 32934.30312486269, 32945.0393232352, 32950.67248548654, 32967.927120897555, 32979.6277473628, 32982.339397945325, 32985.642831004385, 32987.30115740873, 32995.209109678304, 33000.37177797932, 33002.69604391241, 33030.37120594848, 33033.45842693435, 33034.43188089882, 33037.46692567836, 33042.87209512264, 33070.393805329644, 33071.5286661221, 33083.838967431875, 33086.79890921804, 33093.90825531243, 33113.81063175352, 33118.605762893654, 33127.30600562615, 33138.00293273369, 33138.3092078988, 33147.653887278386, 33148.51723213138, 33150.54935848374, 33156.44842565654, 33159.67350443855, 33168.85351362496, 33178.42627825215, 33185.65461383583, 33189.12256741039, 33189.24606363788, 33198.45242432137, 33214.980918155576, 33217.149387606056, 33218.38385054453, 33220.43923118898, 33220.631682980005, 33223.67554363322, 33225.85176865397, 33227.92744495721, 33232.4205224118, 33236.823555697694, 33244.16564782632, 33252.00686823772, 33260.376404583585, 33264.0921582623, 33279.870742942614, 33288.023616142294, 33295.45541198076, 33310.24631663209, 33318.34160427755, 33330.5896518201, 33333.029264568824, 33338.54948394698, 33344.05413736465, 33362.947758938884, 33365.161584145644, 33367.93558326521, 33370.48056784519, 33371.1721599158, 33411.77065446033, 33440.953605269475, 33441.96706160523, 33457.48102370326, 33477.43986121707, 33482.08695458299, 33486.52524183688, 33489.736460844535, 33490.983197196736, 33517.38752076439, 33519.21175279679, 33520.736575752926, 33522.68296477204, 33523.41285310335, 33527.87554938137, 33529.14196209151, 33530.23240855563, 33547.345802410484, 33555.79362944509, 33577.488045432605, 33585.13687382823, 33589.97846874941, 33604.10554030311, 33607.38602943838, 33610.14144765765, 33611.93625991209, 33638.12545986564, 33653.52247107068, 33694.880471304656, 33695.996905265616, 33700.44468573204, 33701.23560927154, 33710.11142294806, 33723.33905749971, 33729.00116814982, 33740.699587124145, 33747.809396580284, 33758.14511321907, 33766.34943095896, 33790.310516071644, 33830.3514146817, 33844.776615598006, 33853.512026521894, 33859.12606322278, 33883.3036430146, 33887.749603239245, 33900.769914032215, 33912.510361357265, 33931.48805859762, 33935.4300047164, 33938.675747300804, 33940.398841249844, 33964.00304112799, 33972.55247932043, 33992.291068709645, 34001.43175799557, 34002.14909449926, 34002.86890343018, 34005.077647490536, 34007.137488039974, 34012.24649273305, 34019.12485756981, 34028.03145795176, 34028.84315007725, 34030.29408113163, 34033.22742517576, 34054.89992764551, 34064.21866107285, 34064.42463282839, 34072.75978383878, 34082.2865916541, 34101.445409723514, 34103.07998230845, 34110.305759087896, 34114.798865690806, 34116.008475531475, 34119.55626426335, 34121.468906498725, 34145.3320618025, 34147.59404209252, 34166.69156092628, 34170.9875620764, 34208.813728108275, 34213.53482401474, 34235.14657655785, 34238.61179158599, 34241.58654174281, 34245.06369908982, 34245.11930446582, 34252.01508085211, 34254.53397039635, 34255.330354697995, 34276.24537828374, 34291.14033656084, 34297.0473092482, 34346.81820215387, 34358.26421881843, 34359.05995215883, 34384.03133488788, 34392.03703734197, 34395.627009739655, 34400.87103605623, 34404.34203035311, 34405.52657807203, 34413.80667219089, 34414.53548701038, 34443.025585839474, 34447.74261431674, 34448.66767496415, 34449.16622700248, 34464.83208001998, 34485.07846947673, 34486.323832077636, 34494.664290426226, 34502.3535299538, 34518.01439215354, 34518.35461686212, 34518.93970875083, 34519.19441173835, 34520.85207229386, 34532.43520007458, 34541.37695623804, 34549.81857332751, 34593.02122203641, 34600.292876587, 34605.29103238552, 34616.72389414235, 34625.30728754375, 34628.88943853889, 34629.33296772447, 34633.509949658146, 34654.184870620236, 34661.83432692121, 34662.06592819436, 34662.22876469861, 34689.01817921857, 34690.23394606878, 34694.75098311869, 34701.74246221032, 34705.833135837885, 34731.938456468204, 34738.43948876305, 34738.48120783354, 34749.97822738169, 34758.9712120537, 34768.78925840433, 34776.101768870925, 34798.13819304148, 34803.642859442116, 34806.09146103595, 34806.976645112234, 34812.965200580475, 34817.16534830806, 34829.69204670729, 34830.96995987017, 34868.455564386466, 34880.925518720906, 34883.48310641557, 34885.09500619516, 34892.45167427028, 34901.9982915137, 34908.58781246244, 34909.67245519767, 34921.30129812191, 34921.49966674285, 34925.925461834966, 34936.81909557087, 34936.91019599151, 34940.50934262078, 34962.648536050474, 34964.87293789955, 34966.09645790501, 34992.5219893988, 35002.323103493836, 35015.16342860977, 35018.143929693855, 35018.49900357784, 35038.68107494206, 35041.919410934024, 35061.63229649907, 35075.20661723847, 35075.631715052965, 35108.90100503827, 35122.485227870166, 35139.646778814575, 35147.37490225846, 35149.02441172866, 35149.951629435134, 35159.506332508325, 35176.003456601706, 35181.03330396576, 35195.150695084994, 35202.19617739554, 35211.89270076475, 35212.934092022355, 35224.5403531752, 35231.805139534714, 35235.98489369994, 35239.69219518319, 35249.546544893296, 35267.08150595467, 35267.53774889002, 35281.227394225934, 35283.452986695826, 35284.46248679113, 35297.30567833195, 35312.81040044929, 35319.17654232085, 35330.79989649294, 35334.715826767184, 35337.37006130925, 35347.945042815954, 35354.99027619884, 35405.59624308543, 35409.186765823215, 35410.532383630096, 35420.04549521643, 35444.568345882646, 35462.80840523557, 35471.43423129713, 35485.447745196725, 35499.62692774586, 35516.85496510615, 35526.36686756176, 35529.39689928275, 35540.93093574389, 35541.184987056025, 35553.82312722412, 35556.7452679948, 35557.815670881006, 35560.56205202716, 35566.318936574455, 35571.68512482999, 35582.54639118715, 35593.67964586184, 35600.16441946094, 35621.94436732528, 35630.64811519769, 35640.677911873245, 35643.482650828686, 35668.994601493716, 35686.22358333352, 35688.69760239893, 35693.913578652115, 35711.05759324923, 35712.899865409, 35714.06167815512, 35721.81551460381, 35723.289540926504, 35765.04917717726, 35781.81606241377, 35784.17120638807, 35792.5859437001, 35799.7824914788, 35838.51125218007, 35843.35765186517, 35843.74492490073, 35859.30212343334, 35871.967373342944, 35890.91607629644, 35894.40749900796, 35896.32534271432, 35906.948873992435, 35910.30394937869, 35922.12711545036, 35933.46476180759, 35943.534287319184, 35954.02685099778, 35965.83294695265, 35974.54150211736, 35985.16045746428, 35992.68682369247, 36018.13803124128, 36019.34680854819, 36022.06341175841, 36024.2702037601, 36034.62376334984, 36038.331159912545, 36038.40609065551, 36049.84701693115, 36051.93338608841, 36063.70233272351, 36064.979077535376, 36070.27512158077, 36074.290099121135, 36086.0158118856, 36086.07713120616, 36086.76205373722, 36089.97999298566, 36106.813203143494, 36134.47077247181, 36135.92992432467, 36136.333742707735, 36141.28516707799, 36144.50348684874, 36157.6813861995, 36168.74885224959, 36185.04461417121, 36192.19335345842, 36207.48990085658, 36209.68757098039, 36215.66915277777, 36234.0280325647, 36237.83589332499, 36238.68583148611, 36241.55573230667, 36243.86648293113, 36261.21853319198, 36294.19537929252, 36295.8733411097, 36301.72700808974, 36325.32396915466, 36325.485363418775, 36325.71199529308, 36330.543783955945, 36330.74879494204, 36332.38871210546, 36333.358647912064, 36348.81624045373, 36355.520583241145, 36359.131806241756, 36361.54941920968, 36364.34595005255, 36370.45449702146, 36376.23598800038, 36382.85185857111, 36396.200267823326, 36411.76707295465, 36418.456231743905, 36456.6048638339, 36470.98660374852, 36479.99244030191, 36486.04316789137, 36486.572493508036, 36487.539808203015, 36493.833124518635, 36497.22407973369, 36499.82630605912, 36507.58203277492, 36509.23094146859, 36513.03133816693, 36517.719703539486, 36531.95401510055, 36555.49601258198, 36569.881772786335, 36581.30776084253, 36582.16865907646, 36582.36236413543, 36583.60035002257, 36587.18062734847, 36596.46578051367, 36609.0246111454, 36615.74104408745, 36622.044325412884, 36625.380914505025, 36664.70449382283, 36668.917961511834, 36675.757595518575, 36682.753169075455, 36682.82215922589, 36688.54644094918, 36690.678026014815, 36709.12648304704, 36721.69553796162, 36729.626339618764, 36741.781498806115, 36747.44003443215, 36748.03260366232, 36750.56127020488, 36752.41638269596, 36771.88639486961, 36772.4861293824, 36773.11748755955, 36784.035089690195, 36800.68705612472, 36800.70742701878, 36843.77713301201, 36845.323243111765, 36850.597478919786, 36854.095700344034, 36855.905849121875, 36871.53812435156, 36883.486919570154, 36890.31900910892, 36914.09806887918, 36918.45293503208, 36927.98303481044, 36941.83094512988, 36952.00755470909, 36969.60725488496, 36976.62812338842, 36978.441441959025, 36984.38987576577, 36990.59602377518, 36991.40430016664, 36993.25344621721, 36993.578850525926, 37001.42087975747, 37019.70634718757, 37028.375558383734, 37039.21592755561, 37043.82792095747, 37106.78670568515, 37114.25979101342, 37116.3362073454, 37116.81227693544, 37124.68871751873, 37148.2506130361, 37163.12998599255, 37167.49966798758, 37180.31643634947, 37187.294436691656, 37190.57629471112, 37191.422211968464, 37193.01149645627, 37208.065935039136, 37211.658678656495, 37224.561555865264, 37241.04698368124, 37288.161561888264, 37291.43771613091, 37298.01887061747, 37306.65303152609, 37327.41971925738, 37333.67232482859, 37342.55704645539, 37364.848207241725, 37368.85874424702, 37375.753741225875, 37390.02220351549, 37392.05517736129, 37394.48270015427, 37420.37503623988, 37421.36111029862, 37428.654642432826, 37461.66953301939, 37465.93541744791, 37481.261223067275, 37481.33978270861, 37498.92338314798, 37506.11094467285, 37508.626296820796, 37529.51109154468, 37533.57772004317, 37533.779175669915, 37546.221456992425, 37549.23836332961, 37558.62982238635, 37566.89998662779, 37567.02842911945, 37567.22055098324, 37568.63229273786, 37587.29902646122, 37589.9458036844, 37593.82769934711, 37596.3591811323, 37634.41887280635, 37651.29915023084, 37655.704962142765, 37663.11026943123, 37665.41764733352, 37675.19745392901, 37685.75181329108, 37706.73056924659, 37723.276718899426, 37727.919861560564, 37743.29605801048, 37747.91446132553, 37755.95226500072, 37768.1286621608, 37774.1519834892, 37787.281797393174, 37787.33003131709, 37791.80845575495, 37797.708397215494, 37804.038929434486, 37805.08333385006, 37847.09441074606, 37853.95597606382, 37862.484504973, 37875.673678397, 37889.048302137344, 37910.82129724982, 37928.82902242013, 37929.35464723415, 37931.43007569333, 37931.58963751456, 37945.98896094991, 37956.57521892797, 37959.72060972337, 37962.24803363024, 37964.26133241681, 37964.94462697538, 37965.51582405557, 37969.170314913, 37970.21783820317, 37972.06083470896, 37976.47242329888, 37987.16893865891, 37989.71832372007, 37996.251959119356, 38008.679013221146, 38021.18919396416, 38024.97298704005, 38036.23567639761, 38046.57405214883, 38052.14698822064, 38054.10840435879, 38055.49131056722, 38061.30717687569, 38062.15046976263, 38076.24428290543, 38076.824318340456, 38099.71898919322, 38101.89211839853, 38112.94043025821, 38119.891469049566, 38123.64937336961, 38135.00999111168, 38135.4825267485, 38141.05146733585, 38149.416105639706, 38170.95157848543, 38183.66133409005, 38189.264246194376, 38194.13299995929, 38196.75494144906, 38216.47924698522, 38223.041649605264, 38223.38891162539, 38226.47870215944, 38231.988982122464, 38249.740689951184, 38251.128560635116, 38254.17405236844, 38269.48913066925, 38269.96079378638, 38273.27627581694, 38281.45922500979, 38289.110013979895, 38301.3592253692, 38303.058585312014, 38306.61340696942, 38312.079397649, 38317.37926180518, 38323.563235506925, 38342.09518759012, 38345.360870882614, 38362.06441079952, 38363.25733707202, 38363.8182355579, 38364.84057063512, 38371.942763498635, 38389.95160275075, 38390.48384426393, 38392.01378483621, 38420.01101821196, 38420.18355934718, 38434.23565284049, 38451.32725094932, 38476.230180531405, 38486.503774788296, 38487.45403789288, 38520.94670585774, 38534.708990697996, 38539.3708336049, 38544.60864101683, 38555.77723673379, 38563.76501784651, 38564.700599814605, 38570.87498944646, 38585.46783613015, 38590.12070435493, 38626.64192591776, 38627.27381029778, 38636.10800418697, 38656.60620622178, 38670.86128367879, 38678.66649374914, 38687.61740855166, 38692.16456581908, 38705.00231396626, 38709.657834010366, 38728.283587426355, 38739.55535602689, 38762.29440865255, 38769.18980843998, 38773.430986705476, 38779.82944969142, 38786.41235459996, 38790.23897915649, 38790.922082910605, 38796.248071593465, 38798.11196096544, 38804.77634258637, 38811.61131101396, 38816.228327708675, 38826.21601011903, 38837.688021805094, 38871.792230318024, 38890.269813366125, 38903.6373954927, 38916.60753722815, 38929.193045680644, 38947.03893782232, 38951.219263243736, 38971.087688686785, 38975.73207833785, 38980.38135378268, 38986.20489210205, 38989.733217685425, 38990.01624469657, 38992.121648929766, 38994.808120257265, 38994.943072823386, 38997.76444024644, 39011.242436058616, 39023.058157540116, 39023.570209998106, 39038.304537868215, 39057.319404166585, 39067.30187599041, 39077.0237866399, 39077.20928117092, 39082.79923464433, 39086.49905828726, 39091.55102069022, 39092.80854602807, 39093.73866166164, 39119.93177422565, 39119.953361559456, 39125.39323435624, 39127.45401029568, 39127.49205423146, 39139.25212561101, 39169.25273028399, 39192.40177165436, 39198.44267825961, 39202.9482261071, 39206.61316726006, 39208.98962009725, 39218.11643872187, 39219.54737345115, 39238.11269401368, 39238.85309357404, 39247.07949400204, 39258.353508568835, 39266.94341892532, 39275.37808605231, 39276.55917149753, 39278.968373367024]

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
    Scale = float(sys.argv[1])
    Intercept = float(sys.argv[2])
    main(Scale, Intercept)

