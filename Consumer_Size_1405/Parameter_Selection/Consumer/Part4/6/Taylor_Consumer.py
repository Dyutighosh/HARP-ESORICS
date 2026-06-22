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

    min_val_1 = 39299.634986842146     #min(X1)
    max_val_1 = 93544.39454597165      #max(X1)


    X111111_1 = [39367.18866514047, 39465.230251557376, 39512.575410722595, 39548.375569168544, 39579.19143956507, 39588.13205432956, 39605.1912681311, 39616.7615898708, 39628.44438980622, 39683.18106685337, 39857.4744973445, 39893.8444986634, 39907.89281593306, 40115.25209222511, 40164.86574251466, 40243.44440451838, 40244.87751269431, 40252.163920784726, 40297.76109878083, 40330.9033536369, 40351.46301281057, 40384.861027908024, 40421.06690635246, 40439.8904562388, 40552.07845874081, 40754.70231580101, 40811.19361083067, 40864.43953142186, 40889.38580472697, 40982.230949439225, 41013.4014551358, 41025.76431136384, 41074.615763831796, 41095.49238710593, 41101.22744525451, 41109.89586877696, 41156.571327042926, 41163.12416586755, 41166.99095874097, 41199.79125218654, 41225.48427452624, 41225.70551007474, 41312.92539113914, 41313.624487028545, 41365.47984297572, 41406.17330732688, 41420.0789921293, 41453.440558539114, 41520.831303521234, 41554.12164619889, 41632.15761294764, 41707.346942263684, 41766.98455536212, 41799.924316149714, 41910.418215284386, 41936.980971597346, 41962.67661829686, 41988.190301794464, 42012.08243932501, 42118.923631384234, 42129.99372894059, 42159.10480443378, 42243.52102741252, 42270.427896308625, 42271.54957518014, 42275.26799221828, 42384.58006148369, 42450.64926935109, 42528.725483809234, 42564.282173544, 42591.529126048976, 42613.18492685544, 42670.05354579002, 42689.646863852766, 42795.74229018327, 42927.65728544754, 42943.86746965814, 42992.75156573798, 43003.38514820407, 43019.848145219796, 43046.42816533626, 43051.933227168236, 43065.221677587666, 43088.983593746256, 43156.84556575236, 43180.56660967155, 43200.96573984332, 43216.638504853254, 43235.69074667733, 43278.23817954303, 43322.514827945066, 43343.60779804919, 43349.897953107255, 43381.71760566607, 43428.57984877644, 43456.5882034258, 43584.55539215687, 43652.89330520848, 43676.400381446976, 43735.4558925463, 43749.125726262195, 43766.61423353386, 43964.4404705441, 43997.997635333566, 44004.770384136915, 44023.69895999077, 44149.9951648528, 44163.63434793971, 44189.82461192796, 44200.92530689115, 44248.3448502542, 44297.11378311593, 44342.02979633298, 44372.21693491025, 44387.08716718844, 44401.199566680225, 44492.43208941495, 44530.58301341065, 44557.06995876893, 44557.52328226547, 44615.866978339196, 44822.804036448, 44924.005910052496, 44939.95304137115, 45083.967894415444, 45099.27312560016, 45166.74958721813, 45219.247164922475, 45270.50121996335, 45399.73797530553, 45457.03679591376, 45687.29911918756, 45845.88980747956, 46025.21781976897, 46148.96649739754, 46209.67775825055, 46254.86688605284, 46293.059913783, 46320.8957008377, 46486.38742480898, 46521.11764490281, 46636.19439774325, 46648.71132018547, 46657.77527787434, 46784.05493321732, 46863.348257406215, 46913.7566318955, 46923.53164921249, 46941.50447503535, 46963.646587119714, 46989.60130858902, 47037.36609168061, 47054.67841031525, 47146.553534607505, 47178.74273212135, 47203.647046171754, 47233.44540154814, 47255.714199828646, 47278.48352878159, 47360.39158412974, 47372.726173590236, 47386.32450332645, 47396.049146997095, 47431.5380864538, 47454.246350332956, 47469.49994326117, 47533.24373849159, 47539.25386261033, 47595.88798378663, 47617.250638888465, 47648.23337336158, 47664.03389520063, 47693.66202655977, 47784.69995299817, 47791.08592281194, 47879.78376184762, 47889.998786705175, 47948.66219065287, 47982.697809587495, 48127.280750388774, 48201.71659653889, 48211.22147539843, 48365.08241859374, 48442.77772736651, 48481.96039598189, 48495.40780043723, 48556.06474058744, 48566.9819484184, 48685.219937326045, 48689.8667427583, 48849.83222352508, 48854.068243170754, 48978.62941682384, 49065.63255984683, 49110.94573372447, 49183.355196852244, 49240.94600530784, 49291.07707479316, 49304.63937409274, 49358.33167729352, 49410.70892957918, 49442.430141855126, 49486.40603017374, 49509.09736256206, 49525.76796837894, 49554.50479554492, 49652.08806354142, 49662.11068895833, 49741.13962200547, 49766.79144250283, 49792.00362668575, 49839.23204898177, 49991.46292163069, 50011.9032792309, 50024.82880652614, 50072.1748007135, 50118.95923205559, 50125.2074117091, 50132.00920679535, 50197.62682499601, 50198.65302590468, 50274.90653409557, 50277.455310370824, 50397.203389413175, 50412.111110073434, 50422.63460389523, 50433.23780417825, 50504.63096582501, 50526.2152712699, 50569.36353813591, 50597.64339286202, 50602.11085909679, 50674.05592633388, 50698.332443161424, 50782.03637142957, 50817.485171982014, 50846.3103833231, 50933.669356099155, 50945.3713580553, 50960.0155672761, 50992.20085137529, 51023.62348016632, 51119.11023821965, 51180.049115534675, 51204.556595417074, 51219.35210668863, 51273.075226755594, 51652.10855263601, 51741.4915144234, 51769.620118969906, 51842.5579732449, 51878.27705949388, 52103.19330118683, 52120.324969643116, 52144.75561499834, 52260.25260123699, 52328.354572885255, 52366.435572726754, 52423.163827645236, 52454.90949288284, 52509.150225533034, 52510.4597068895, 52578.826190049935, 52606.38775996079, 52768.88904991828, 52769.98104655951, 52818.47445896277, 52842.02784864765, 52853.04376996779, 53100.403055056064, 53163.090454973055, 53169.62997838829, 53253.22319100428, 53288.588907781435, 53291.33570532176, 53343.46127048075, 53422.63302495432, 53423.52609730989, 53446.94682375695, 53461.24817748774, 53566.183198802886, 53671.90158295879, 53693.99744517876, 53758.31309741539, 53809.513371828885, 53830.37174035855, 53908.03792588795, 53991.61080823197, 54030.968936398305, 54036.79997535969, 54136.11510207811, 54141.33266490381, 54193.10143696645, 54217.00976547457, 54254.47035438532, 54370.885522905235, 54416.20382600977, 54563.035226933236, 54592.094187283845, 54637.43403614429, 54736.09214520671, 54744.34392357755, 54764.061337013685, 54805.53392015827, 54874.26212025944, 54890.22830752381, 54964.115554348486, 54990.99328376188, 55127.44944280664, 55136.13479216443, 55209.41276593738, 55277.214171152584, 55568.67113216815, 55569.94797113925, 55595.49306529577, 55755.34439444942, 55758.445707820036, 55774.41882969534, 55820.49370000599, 55878.86292705567, 55895.265972046356, 55932.37605277165, 55974.10334644381, 55990.36892154591, 56172.69078494627, 56205.33522782998, 56243.335691559805, 56297.40213978899, 56385.75305148733, 56460.23197897528, 56501.11473517325, 56581.63871162145, 56621.281139137514, 56731.87305244351, 56770.06932128052, 56804.545996864326, 56814.40304689612, 56859.73854862122, 56864.820960375226, 56877.434388121685, 56959.0477628149, 57424.16422206274, 57563.64363774512, 57608.2735612977, 57620.70801925266, 57770.30090382477, 57934.4287659551, 57946.77979023046, 57981.14149674983, 57992.50784018493, 57995.51949232179, 58042.112898217245, 58221.45943846537, 58326.556943636126, 58413.97993301347, 58434.12438025545, 58604.098224608606, 58661.7776736929, 58667.47606307166, 58687.46195162038, 58737.46895942809, 58774.298617556065, 58819.853146545895, 58907.425160760584, 58920.229814782295, 58932.014319991285, 58945.48128139622, 58962.67111421284, 59030.59252235324, 59059.86846058423, 59124.53267432002, 59246.837713834575, 59297.58644131302, 59426.5136199445, 59512.9196973682, 59607.94123329829, 59623.29746796716, 59735.04444724161, 59777.27563303015, 59806.822328770395, 59817.6910240184, 59878.04691011787, 59902.91604923501, 60028.59867523021, 60076.27669015172, 60146.85962305336, 60261.54725674295, 60284.71401250352, 60306.5017900166, 60312.75636993727, 60450.18593653616, 60526.95413202891, 60557.06622801218, 60639.72192570628, 60694.577223928325, 60695.29927467137, 60775.08042171557, 61061.38797407871, 61101.6773590546, 61110.50499389328, 61142.78772205196, 61183.24309388691, 61196.51875284387, 61445.683995162006, 61491.97015938349, 61553.56991599008, 61588.37731834761, 61654.702125841155, 61739.61849450183, 61747.6264085524, 61863.10572000873, 61892.34623213983, 61958.76923969381, 62014.55118064761, 62027.676973441616, 62042.15050486717, 62069.58967410237, 62076.743226860286, 62077.8207025903, 62109.656552068875, 62116.402572480016, 62118.23422568094, 62129.01342471765, 62139.99027765072, 62238.39409755374, 62343.833849594506, 62362.72646276482, 62371.87680109032, 62564.12759929518, 62643.30142683476, 62756.93900989494, 62797.77918178323, 62853.251398918386, 62856.76461639402, 62907.65594194214, 63049.063189193526, 63101.258934349666, 63184.80078799987, 63198.020322441866, 63220.666045092454, 63254.13091708789, 63262.995874582535, 63269.98727068914, 63273.40862847716, 63308.13962705982, 63331.33344689275, 63351.279917784464, 63399.90681826234, 63451.26277361663, 63487.27907275263, 63698.170101759846, 63725.39423774994, 63768.93759829081, 63804.48491686101, 63818.737561444286, 63861.50640575937, 63882.20954713592, 64190.62029127398, 64300.53054735918, 64488.56472266895, 64506.02577126361, 64585.8842221404, 64589.84643461781, 64611.21620259997, 64716.18178413417, 64771.02315516211, 64784.252498535745, 64817.71084199489, 64864.18973931002, 64898.90590997397, 64923.961791559705, 64985.7277697638, 65008.77959964497, 65069.50003815652, 65133.68810177975, 65165.311843321484, 65231.9341734407, 65262.08465105404, 65349.87528157619, 65380.27809826322, 65415.03361063644, 65415.44043048519, 65416.131710378446, 65508.07291519949, 65513.973478879154, 65547.95283337664, 65663.69162401377, 65670.85238878476, 65696.93717844522, 65707.37137344382, 65721.97097691553, 65749.176254589, 65848.7825114507, 65853.27004142803, 65858.63092959116, 65870.0431743781, 65872.49225556642, 65907.69533681964, 66005.17514255202, 66010.67338126572, 66014.4037512474, 66083.2384064165, 66124.19239886217, 66199.2685716632, 66224.38623069349, 66268.27288794085, 66271.26091411467, 66446.93829692766, 66482.90145809129, 66621.92602648224, 66666.03778771353, 66671.71921661933, 66817.23781870975, 66845.47833269765, 66860.60515189651, 66869.9769728756, 66971.92654454622, 66988.3669671002, 67013.51612313729, 67044.03419798054, 67179.85159914101, 67263.19288162835, 67302.72609316962, 67353.61711723988, 67552.97320504101, 67579.64331044706, 67606.09855281904, 67653.6525378203, 67775.23949229227, 67932.29866747673, 67940.1647718556, 67954.8357645029, 68009.1456517861, 68012.11396529904, 68084.82328987058, 68114.92881448436, 68156.33356281475, 68177.48399507189, 68209.93706826115, 68279.86062129182, 68296.5087825919, 68326.96778640167, 68379.52326317213, 68399.86580789374, 68569.9377768758, 68742.60794498939, 68745.48606258821, 68760.35187293608, 68764.69375224202, 68767.09580165277, 68801.68224058881, 68874.74192352181, 68912.81987924073, 68975.2795647292, 68991.66322607221, 69004.73604238848, 69049.80113419128, 69253.34856444801, 69296.65404508178, 69336.57984541162, 69404.58673685548, 69514.41008815379, 69536.69428956596, 69548.75667657028, 69579.80323728899, 69694.95725787048, 69819.38901630935, 69841.0662291351, 70052.95401579612, 70062.22962934748, 70160.48235587981, 70221.15893963948, 70264.29646437432, 70282.43126034341, 70306.59080242197, 70342.27413780687, 70472.07308175252, 70516.49214908444, 70568.13968651189, 70569.95786965502, 70585.63581754477, 70616.94789161903, 70715.22888388824, 70894.73845786748, 70918.78937743042, 70927.1057522278, 70953.49324807285, 71111.55775186917, 71135.45318784569, 71181.69934214858, 71194.23088076526, 71218.15617382167, 71289.20609634183, 71325.0132487745, 71364.29441933232, 71406.18032994622, 71414.43312451664, 71448.18446390802, 71502.82593317906, 71521.72004318431, 71575.49531021147, 71627.09502296243, 71655.43708377055, 71675.00669851215, 71679.19430383448, 71805.7726050349, 71831.53118591238, 71890.80574883713, 71934.30899642347, 72098.50023853, 72101.18012188855, 72106.68221911791, 72153.5235697637, 72236.05493553833, 72291.55952450707, 72314.54238997387, 72530.30991131591, 72590.28079653796, 72643.74210613515, 72685.43800316223, 72776.97838858391, 72849.82338104463, 72855.35238055352, 72898.01608614226, 72904.32085254163, 72970.09529014293, 73112.62371932098, 73122.83053614091, 73366.96387481614, 73375.5742806962, 73459.86064005416, 73491.95687885155, 73501.84847987042, 73566.6487703467, 73734.25160553216, 73738.09758821574, 73855.54317073271, 73926.12267588623, 73996.97639630598, 74056.5421100235, 74079.51688418217, 74150.61049360473, 74191.35718723627, 74200.74351381927, 74284.4867454633, 74300.3566898169, 74334.5228423019, 74339.24112000011, 74394.38868205869, 74635.72120295659, 74653.39964151458, 74674.64151297064, 74685.81877798772, 74788.85263817245, 74808.00743994775, 74825.42155345113, 74879.82818634144, 74915.30461296778, 74930.23596435954, 75062.83966129768, 75173.87446928796, 75192.44355430079, 75197.53559210408, 75260.10536879982, 75329.93584903982, 75330.6044906489, 75470.87984090085, 75759.870395428, 75821.46730319204, 75890.95725627025, 75895.29896136068, 76007.5472333387, 76072.0918060157, 76331.44041426468, 76354.7326567604, 76382.45008059357, 76390.69269965772, 76445.24593181504, 76653.15947990696, 76769.47202215099, 76793.05760095519, 76920.20190066562, 76942.48449229653, 76957.3218915957, 76982.25891162499, 77091.96159826741, 77112.41141467297, 77254.76633845882, 77291.16161591127, 77328.46376079474, 77332.442595565, 77333.14362243484, 77354.89464905267, 77431.29520039176, 77438.1503031996, 77483.9140584828, 77511.01607169991, 77523.28745288953, 77645.44694060527, 77652.84934735627, 77664.6399912804, 77776.40807337078, 77779.08676433354, 77798.82654594266, 77861.5506751666, 77866.73307306724, 77868.87195608429, 77914.22423020519, 77944.57305047777, 78056.77778433476, 78073.26548967868, 78191.84856530714, 78248.62765643987, 78255.40857535673, 78295.78117010847, 78365.10154879407, 78412.58691186336, 78486.02937004634, 78499.15506704662, 78528.10233915091, 78748.02078729036, 78796.59485789211, 78931.56874571269, 79040.50478796808, 79066.41420181308, 79073.63479373461, 79090.42968875899, 79140.06358058075, 79258.60500325907, 79276.47520169838, 79306.76699196605, 79338.02398965223, 79449.32878516839, 79489.29808095221, 79512.10318906301, 79538.01127814468, 79610.63042456069, 79663.17376267305, 79755.40982950867, 79917.7047506565, 80033.9537788551, 80036.94782026892, 80159.79469602024, 80198.28358433314, 80222.65712831331, 80259.30124163894, 80284.16796047366, 80328.25525861703, 80344.74188506317, 80375.8725667585, 80403.69856190907, 80450.93027189857, 80665.47860861928, 80856.16640431737, 80959.89066340547, 80991.42124122175, 81110.70497844469, 81309.02469295246, 81325.87917472467, 81349.72121453189, 81354.94769093554, 81376.45870887778, 81394.41944426845, 81402.18479822855, 81625.99121340754, 81704.05806520271, 81744.67872059734, 81843.87731214619, 81879.5918441712, 81942.11898969932, 81948.16414418645, 81958.20879166087, 81969.51917052818, 81973.00902370106, 82021.4122426502, 82086.4777475993, 82132.56992864847, 82194.39378483563, 82289.92165785862, 82317.62218546151, 82340.95149650292, 82374.6145994885, 82404.44244792093, 82464.24113478788, 82630.53583725751, 82656.57155233054, 82698.82066278148, 82744.33100178937, 82765.23380650146, 82784.08984158712, 82809.23358247586, 82887.88614098798, 82913.58758830735, 82920.63155628131, 82960.12683802922, 82960.65730685255, 83010.15985558886, 83027.30493954063, 83036.5365556867, 83048.81695874679, 83184.31569981587, 83206.80047930221, 83296.32063891264, 83334.87944073637, 83355.50306194914, 83414.92112444254, 83437.24024794623, 83474.3608435995, 83502.99990869428, 83503.42807506824, 83515.7338087764, 83525.36925012249, 83564.97444673679, 83609.05089949539, 83615.03311177107, 83663.40860018363, 83664.2559404888, 83675.16385962174, 83707.98971566337, 83826.02494317645, 83840.48334042566, 83882.29666797628, 83891.90232479804, 83930.20586782444, 84020.67083360124, 84022.23040262598, 84155.48894855613, 84238.25749313945, 84287.53249157271, 84335.06729995206, 84360.06524442346, 84367.7213588004, 84444.96641992399, 84463.85674507107, 84463.89405179513, 84473.83268108152, 84531.90330756718, 84577.39556237121, 84585.70924791145, 84595.13870870345, 84617.95548147016, 84619.82711000177, 84646.6729272769, 84658.23997692676, 84698.74342323882, 84834.78247194327, 85039.81966250417, 85120.81642530234, 85394.56446911207, 85489.50459164463, 85536.13133992866, 85689.90562083153, 85819.49339882827, 85819.86070676663, 85826.4100116816, 85838.9897401795, 85881.51936838074, 85894.0588277736, 85895.58497892588, 85907.97756746433, 85925.95401775105, 85937.50963160969, 85947.17207485129, 85991.40050514729, 86049.15191364032, 86089.65255697747, 86135.91542135461, 86158.62957720691, 86185.5663164728, 86224.39814745222, 86260.7821641193, 86265.33138055762, 86364.71697870495, 86401.87051034384, 86449.67151485328, 86460.31573340317, 86490.0394366587, 86526.84433185047, 86570.36109310054, 86825.45324703115, 86913.74597772092, 86927.74161714372, 86937.57949385558, 86971.24274599543, 86971.96445320651, 87029.85177553467, 87115.18621701651, 87183.92796762261, 87253.88593983577, 87296.49031472186, 87302.61422508053, 87336.82613944334, 87350.47034841779, 87360.83363355655, 87379.35712847371, 87416.84098503736, 87491.42643926133, 87537.1414172952, 87574.58843529245, 87618.81902238696, 87674.10167846238, 87765.73247353501, 87818.87953467696, 87820.76192644774, 87897.7016075525, 87898.77474636529, 87964.61175907077, 88042.5741213942, 88077.91965286474, 88173.05434835918, 88255.31540571127, 88296.1173885118, 88320.09209232611, 88357.90616556664, 88528.58279330569, 88547.97653434981, 88582.69760902143, 88696.80680531156, 88701.36386299957, 88710.03118862593, 88793.70038261631, 88802.15692970678, 88804.39757207946, 88974.24773330674, 88977.07566958526, 89003.72643577983, 89034.63780244035, 89049.84241362925, 89113.11514798045, 89138.64543542269, 89265.52347459426, 89277.22093253741, 89308.68627507455, 89620.64141951657, 89691.57811809069, 89704.32176347222, 90038.05896003706, 90208.00554475632, 90268.02428152694, 90282.05675431312, 90342.60018362504, 90347.59039672559, 90381.93112913548, 90400.0761924193, 90485.91836877876, 90532.17240916096, 90595.29519725677, 90739.49397241842, 90785.78934919575, 90788.31362234522, 90793.0611886452, 90873.57473336958, 90879.25658093182, 91100.19866133499, 91154.0450246667, 91190.31695366316, 91227.41355425309, 91248.33004951588, 91252.71332011887, 91252.94268320699, 91267.5704550604, 91319.12353564982, 91333.31440576112, 91335.74963032697, 91365.70151036643, 91523.41972021236, 91586.10441458305, 91634.03259693668, 91646.59193102192, 91656.66570568895, 91676.20523075198, 91797.66562795368, 91955.95705683045, 91981.66228746925, 92021.70835553054, 92026.52726633704, 92160.19830284656, 92180.21449617602, 92182.70086426448, 92249.82945987271, 92359.14577925659, 92368.10727012508, 92561.15815471593, 92784.1426391165, 92805.31254480022, 92845.29650293634, 92892.48196742716, 92915.9484358991, 92944.39502870676, 92980.32560183469, 93018.56067694604, 93049.29942995752, 93220.15838252749, 93273.28293680886, 93353.35356922494, 93420.35506610751, 93429.72460196409, 93471.18333722476, 93472.69745518184, 93531.22890271219]

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

    X111111_1 = [39668.81784952324, 39682.30483986663, 39762.67083754392, 39767.95503576786, 39786.016845033824, 39812.51700249689, 39866.59570861191, 39902.675660027366, 39940.30112273082, 39976.915097190315, 39986.97145265145, 40011.14162274302, 40174.9695273246, 40217.61432401995, 40301.15479646929, 40366.84638108922, 40372.462886844114, 40561.827260618935, 40568.317051299, 40689.382353070025, 40720.581745731695, 40750.42978962185, 40768.24915627424, 40843.05185779852, 40847.18322630708, 41079.34596377991, 41141.79375796083, 41162.193199763045, 41206.30182508088, 41250.71005788573, 41268.27152907384, 41308.718794743196, 41343.24263876429, 41449.18373865425, 41486.632914878996, 41594.078127283574, 41647.643001302604, 41671.32515349831, 41690.90257415642, 41697.95520654819, 41703.87238806463, 41725.857217760866, 41797.114362157234, 41806.4968549501, 41867.23759574495, 41873.70519916925, 41881.224301421964, 41920.48606932809, 41921.47825477516, 41963.602124188474, 41976.1115499602, 42034.19048893272, 42047.368459328354, 42051.23495776265, 42109.77073936905, 42123.296471787624, 42154.86964173155, 42171.18705656492, 42171.69748845509, 42265.7558671954, 42271.887890113285, 42387.987253532694, 42469.975805357164, 42554.097343214045, 42651.443856993435, 42666.58942116819, 42686.65134341264, 42724.23699672477, 42743.88355906668, 42757.976262865915, 42920.64375180433, 42922.780182927774, 43073.44019232067, 43074.046130268136, 43130.6884195694, 43169.03451197976, 43177.232452244076, 43247.15545667303, 43453.758559603266, 43482.99598238647, 43552.11482685772, 43722.52640710163, 43764.088746704765, 43819.79083576325, 43820.61553524601, 43868.96830293794, 43900.54445181481, 43908.85710548995, 43992.14544127451, 43992.754763320474, 44086.62261654145, 44190.97492906414, 44205.669497766445, 44290.837497151035, 44300.04179066869, 44328.72542364653, 44339.247005491576, 44381.22327690663, 44417.8417422451, 44441.09611390385, 44560.55840722839, 44599.51450702615, 44639.67428930417, 44752.1210939984, 44836.392916397344, 44973.18434080423, 44999.52795287507, 45016.949878610176, 45108.894255277, 45121.51710417518, 45123.6987687594, 45151.304799493446, 45236.04058599318, 45325.07287747052, 45329.89762154313, 45433.664181497195, 45447.05552209597, 45487.20766362972, 45614.15956523911, 45617.56778407389, 45625.21504166156, 45631.0163019801, 45637.92625575173, 45688.77098802959, 45735.03680409543, 45790.01793854995, 45950.355164001114, 46282.053375833566, 46308.6571236071, 46392.02890277816, 46438.309190577216, 46597.43125878949, 46620.4289031471, 46785.82568901707, 46792.39121952887, 46835.29644218993, 46910.63557935593, 47049.30923102079, 47070.02772676698, 47185.56439732056, 47198.022596432085, 47298.83242940452, 47397.758631586876, 47411.285248517284, 47433.970445963336, 47455.66311004693, 47545.3612563225, 47669.04855104707, 47681.06515511294, 47745.7683294955, 47771.072947996865, 47780.07552948717, 47839.97595317265, 47887.850215695624, 48002.17339319375, 48139.904726159475, 48170.25136294173, 48177.18111933675, 48324.20899856635, 48348.07943904188, 48476.56824041418, 48505.36864318708, 48509.445384284685, 48583.74758884895, 48597.640410652966, 48657.37049540262, 48744.9968221035, 48993.65138583692, 49003.3331285055, 49060.12881421332, 49128.47537327511, 49137.29278247701, 49411.87691672302, 49455.01827425962, 49459.700166790695, 49526.08094575108, 49784.478093721475, 49843.245262108394, 49885.924343125036, 49891.44904066426, 49953.94350693305, 49977.28325731504, 50099.368432411706, 50109.33484425932, 50147.78324434299, 50158.753415191386, 50309.19865361604, 50429.64127586958, 50515.45976327253, 50557.852594334836, 50583.39905311952, 50733.10770420815, 50754.493024293115, 50902.2431011586, 50931.3532766693, 51107.709894368316, 51140.037690433746, 51210.81742983218, 51286.6587598247, 51299.93384223324, 51315.50812553818, 51342.183387697696, 51363.749121669534, 51379.74694383778, 51447.78140969462, 51482.93345237031, 51508.60906657402, 51579.08173846044, 51626.60366778534, 51640.956929845604, 51682.23380394107, 51737.407063854036, 51747.7769040328, 52000.82221173695, 52032.02830166788, 52069.950387434954, 52111.51034323779, 52145.297209309014, 52215.24612809686, 52248.14364995289, 52283.15483321558, 52299.62229576274, 52307.39242710005, 52595.527776940726, 52666.052394469865, 52700.8215019825, 52747.99805119138, 52889.53917611064, 52927.36236544988, 52973.41018853294, 52977.469501885105, 53038.82519844611, 53127.829594878334, 53162.410198134574, 53254.564730270824, 53255.13981398451, 53287.1421849396, 53296.96992681993, 53345.21354272976, 53361.39433159401, 53361.70412207194, 53403.3419701267, 53429.85095878697, 53668.2750421527, 53669.693094802926, 53853.248897185316, 53951.75268116977, 53967.159707066305, 54020.054764126704, 54075.51005203446, 54130.679970509824, 54143.47234359502, 54230.86274960095, 54237.206626123036, 54273.73636654669, 54316.4528489169, 54345.8696006532, 54367.801640518315, 54383.868541509684, 54433.90738795137, 54435.38520077461, 54459.669009768746, 54459.995657594794, 54529.606940637765, 54578.413898348066, 54597.25799242404, 54630.728003951815, 54659.41555047586, 54719.78735632775, 54739.40952092293, 54807.436046570445, 54893.61004595953, 54912.993300641, 54928.93896801509, 54962.92862799992, 55285.70549863651, 55295.259371004206, 55333.795661942924, 55379.86610067991, 55476.78620122257, 55584.38560779702, 55592.138993265144, 55628.704929375315, 55632.72720048539, 55633.88626014361, 55662.82576449902, 55732.67431167862, 55816.05699241397, 55865.47962292163, 55882.35478661875, 55920.20417191349, 55926.35827852826, 56046.00962770525, 56072.55537275302, 56138.19262096073, 56140.23764024411, 56276.06425211353, 56302.276013075476, 56392.960786955446, 56406.108093771196, 56437.8047659759, 56510.83270685378, 56516.293574038864, 56522.54901803515, 56621.66533330393, 56629.30595441562, 56646.38756577381, 56787.65542513934, 56861.392323097345, 56925.71777440651, 56955.66711223872, 56957.417606571005, 56988.2988870235, 57022.54145059986, 57115.461682353256, 57159.31405844001, 57223.91264748621, 57262.6724990863, 57382.04720898902, 57386.99559780191, 57411.927350252394, 57521.55768975635, 57529.91893696705, 57565.735080434955, 57687.21970357353, 57687.640828766554, 57707.27853346769, 57819.46810479663, 58160.07332876469, 58169.01926055106, 58192.23468644261, 58212.20087442083, 58352.86681262968, 58419.93441469637, 58440.57643729987, 58483.83448805986, 58508.629785256366, 58531.264026755365, 58540.24094681778, 58714.352964835074, 58809.44607968032, 58999.39160729754, 59026.73834779432, 59155.89505559334, 59281.43872093557, 59344.36086355723, 59349.2843736278, 59367.484400463014, 59414.930091194285, 59421.42220285683, 59457.241669496216, 59522.46488728629, 59528.465844260456, 59544.73592174359, 59585.14735376107, 59650.87409669314, 59700.84374713023, 59715.30475990007, 59803.517387317595, 59805.36480674021, 59944.37054955003, 60070.52653263594, 60112.388246920156, 60286.44428509545, 60401.029900364956, 60462.62824180996, 60507.35422357581, 60595.463496839584, 60611.39947542046, 60612.83851230431, 60665.70533011768, 60685.757309474095, 60766.64959635267, 60971.09151191047, 60976.78267588976, 60996.76508392565, 61048.8080608474, 61168.07963572524, 61179.70467583905, 61214.24169678466, 61300.00264495995, 61345.47579353822, 61445.372721184904, 61456.04141023078, 61477.04000391018, 61479.25793516943, 61501.16466368977, 61808.06806632456, 61896.707015785156, 61917.24972788889, 62006.14431086193, 62046.990533259144, 62138.32749892163, 62210.928857550876, 62272.32523770817, 62274.436207858256, 62286.920897782395, 62293.59674753377, 62321.131794953704, 62354.85975343047, 62379.155078111406, 62387.35177460138, 62457.43410213248, 62496.40243348986, 62498.09130793756, 62605.083195635, 62740.65779657757, 62897.699859456436, 62904.94568012362, 62906.42782550894, 62947.01457356496, 62969.98299384958, 63023.990930836604, 63230.32268644659, 63234.0116875719, 63314.26058052971, 63375.18901508176, 63421.62286416495, 63507.40090544926, 63555.95212015863, 63564.01645257298, 63596.47429996001, 63677.83076229165, 63702.9531891475, 63712.19476639226, 63723.173438688216, 63730.00177312471, 63733.365645633276, 63744.37685128345, 63751.67020263335, 63794.51988601065, 63885.08975871958, 63896.42552559795, 64025.67131989412, 64074.556492158306, 64096.810486222144, 64161.81797776515, 64238.352160451526, 64291.94335715129, 64301.15227128944, 64319.6003452323, 64344.97499877012, 64474.897302004065, 64482.15413559062, 64489.76892319834, 64576.25155031169, 64590.96646306275, 64660.957011503684, 64661.66838670168, 64665.46888124299, 64741.1224362682, 64772.64244008537, 64806.614391158524, 64824.19943097682, 64976.270028501895, 65031.66085173164, 65125.383775208735, 65132.863892573834, 65134.14560834662, 65139.21606197208, 65140.24859980462, 65158.90180529948, 65164.937042491285, 65175.56831114914, 65239.746669542204, 65241.315180941136, 65282.17094061829, 65493.09876059132, 65561.8407413162, 65616.65419816272, 65646.17705864103, 65711.4475379029, 65734.35887234198, 65748.4410061583, 65753.68487906629, 65779.1677153036, 65811.93423885063, 65861.675157906, 65966.68887903981, 65983.03996324322, 65986.2930177504, 65991.4164612438, 65993.39914663445, 65994.41388684037, 66044.87535122343, 66088.61044310377, 66098.02576664064, 66105.81447536618, 66150.88482211494, 66158.85177878408, 66247.49702618636, 66318.75835052133, 66343.21943784406, 66434.66283773578, 66502.79617944227, 66612.464524402, 66744.51138878941, 66780.63600378059, 66782.69443940249, 66801.60424348828, 66827.55016513196, 67023.65079111067, 67027.61040387982, 67040.3360464515, 67073.88503354305, 67081.96154037297, 67142.78603014434, 67182.77930153809, 67215.82473882192, 67288.80145684743, 67300.65460765362, 67334.60211018656, 67383.29573557284, 67482.18205655133, 67603.23957989799, 67688.16465385337, 67698.88936437467, 67793.65606449093, 67796.07002058797, 67810.54350420315, 67927.95060331761, 67944.43266574063, 67962.42169660912, 68000.02764311385, 68134.75620252968, 68139.92213998163, 68188.2105315093, 68207.86158205192, 68351.60885883203, 68425.77804435487, 68428.97048545233, 68434.62383144011, 68482.62694943504, 68499.2007873438, 68609.93139122777, 68623.60469791293, 68631.50702304186, 68684.41132079318, 68697.0461531031, 68753.82558765824, 68758.64874482734, 68777.4300520676, 68787.84749041082, 68807.57134653583, 68893.35486562739, 69050.04558390731, 69115.0418656498, 69186.7737983972, 69212.24707981487, 69214.08740557477, 69273.86084770209, 69350.5534594511, 69379.51618749913, 69382.12849957787, 69400.44498024938, 69438.24758495501, 69482.18857581886, 69498.29900404334, 69503.580826938, 69507.23151890698, 69539.36749397374, 69802.67437042246, 69930.98502028956, 69937.73065927817, 69965.43330051894, 69969.03744188127, 69996.2314159656, 70065.27827713586, 70080.32140564993, 70123.07617426076, 70144.34984972862, 70151.7150074792, 70176.73782393333, 70186.02748097236, 70193.27175529469, 70227.44142519955, 70249.28551864608, 70277.90716050287, 70289.27831164749, 70332.12368101254, 70365.7462500903, 70374.8788507065, 70394.24363695117, 70487.66051432467, 70548.64659606505, 70659.76094386878, 70685.05262106947, 70750.64760671923, 70844.43241520648, 70872.4384932804, 70874.4858816584, 70903.12945734482, 70920.01347488686, 70946.94304129678, 70998.24980983086, 71020.98616909176, 71027.86785746318, 71093.06039760017, 71096.17179156598, 71126.68580591984, 71141.30514805358, 71216.17772364178, 71235.72753439865, 71263.55127131249, 71322.40134171254, 71397.02859049065, 71557.0092686676, 71577.87804164653, 71600.51637727945, 71621.76972926574, 71625.7144676302, 71760.43709345123, 71783.09523732602, 71808.17727088828, 71941.33791618698, 72047.5381355079, 72096.02278647656, 72282.95608268373, 72308.88806837631, 72314.01770047059, 72320.34263337153, 72348.31642360498, 72351.5233821566, 72420.61074115141, 72564.87534705787, 72832.4150123463, 73022.52277845505, 73072.09828324524, 73135.2464255561, 73161.93759624056, 73281.92592881774, 73289.33170891323, 73355.50001796754, 73429.23789229427, 73540.70186244402, 73553.59309366427, 73558.08972751789, 73565.71307223171, 73579.06879719204, 73596.01733508718, 73603.07393405345, 73634.32018252967, 73645.66750419907, 73676.21090420216, 73760.86766269956, 73833.53260188329, 73863.49077862219, 73877.23887629816, 73921.32062437029, 73946.68525756465, 74005.45954350047, 74073.1617616647, 74203.54342706298, 74243.39167694017, 74245.8905322244, 74248.83865380113, 74248.89173411606, 74256.35586145482, 74266.17778335388, 74332.87804670364, 74531.19969832848, 74570.95618717832, 74702.45092464655, 74951.27070033277, 75051.06061007777, 75178.58847889707, 75189.10630430262, 75210.4548746103, 75257.0902273037, 75372.6486548436, 75478.20744583203, 75493.28403877407, 75502.48159301761, 75538.1189159413, 75586.81821618539, 75609.25775868558, 75708.7541379068, 75902.68153886317, 75927.11533772448, 75929.3040936265, 75949.26957614055, 76199.18404155708, 76326.45165933087, 76330.8337950817, 76410.94346451195, 76442.50678080728, 76443.57971412268, 76451.01771635484, 76503.9856831049, 76521.47779672741, 76531.5342924993, 76565.0538796624, 76624.7453286022, 76646.98270656615, 76735.8951430126, 76762.87407640333, 76900.34971078235, 76965.53138703537, 77084.9092085785, 77108.64846599475, 77133.22672120272, 77146.73672739475, 77205.46382857833, 77359.54959802676, 77399.2986765146, 77430.03775181343, 77484.16009561256, 77550.00866511559, 77587.21658229774, 77645.44809946493, 77660.23960939783, 77701.39907447438, 77708.4717696163, 77723.1970740569, 77741.81072285635, 77778.58813594937, 77786.17459327685, 77855.51519658243, 77887.83851360276, 77927.09740738367, 77982.96223308961, 78052.61201668743, 78088.42031492025, 78091.4840105193, 78134.40346874595, 78198.79586812109, 78201.87257662177, 78207.74581838996, 78256.09983865311, 78349.3461264666, 78405.6195570693, 78427.6741385446, 78468.7835087815, 78507.35441454753, 78594.15787532221, 78708.80277928177, 78710.38456823622, 78807.29449200683, 78816.54661419668, 78861.99139172217, 78940.60664461434, 78961.55251130852, 78983.29332414157, 79005.18360468972, 79007.65389136519, 79072.92919290563, 79091.01138629392, 79363.05282755067, 79394.35305252386, 79440.70861700096, 79459.08196610023, 79494.38226797403, 79524.3121965048, 79654.77682036957, 79769.69988192368, 79843.52151882835, 79916.8489642275, 79972.70096963411, 80062.32495596688, 80083.68548147446, 80114.74420367932, 80270.06239769806, 80293.20433830426, 80295.67142619405, 80504.27419788518, 80562.19958192846, 80586.06034297052, 80647.9429255558, 80673.63380710746, 80769.65533282657, 80777.99428062979, 80782.39529811309, 80879.75228798448, 81151.56896543104, 81159.9817523862, 81267.40285431572, 81290.70209264016, 81323.16361782915, 81342.82339001517, 81466.49530203313, 81514.98952354534, 81605.27309728312, 81625.29071521704, 81707.56770230149, 81725.8701030907, 81804.80914958943, 81837.42331049322, 81911.16611597317, 81929.93915284626, 81942.41386948909, 81992.59356238072, 82023.02728267397, 82119.35878775684, 82136.1596780403, 82153.00753145549, 82172.54239939869, 82399.7644425318, 82403.70310369175, 82414.36637530147, 82421.2288538418, 82427.07754608219, 82434.01449006563, 82468.78115806796, 82477.07072599955, 82538.29153572422, 82574.70702530784, 82601.64310286137, 82649.88038678672, 82735.70039516225, 82877.3681817188, 82903.84938835955, 82942.66471819716, 83016.47348607145, 83076.75257758843, 83094.78870154571, 83166.48724511755, 83263.67460402891, 83271.53537509315, 83342.67798476337, 83450.78699090602, 83539.08624855384, 83551.47440732765, 83560.39002066705, 83655.47253528741, 83870.63189447529, 83879.73626652901, 83919.8272659773, 83932.43837576477, 83962.74120027041, 83966.35068439326, 84052.43240056038, 84057.60690521798, 84202.02538238268, 84203.63923343335, 84214.1289776767, 84362.55116741982, 84392.73625787265, 84617.67595325527, 84651.27658662619, 84688.48048243675, 84697.37522300758, 84728.83156814895, 84742.60110017972, 84758.77007786241, 84795.47882224504, 84811.70567601631, 84845.27631477441, 84887.90544597126, 84996.3228488401, 85053.25982409973, 85056.06894894104, 85056.83426098655, 85117.7765933967, 85178.63798069562, 85308.70426808631, 85320.09877034996, 85330.7545219399, 85339.94675786947, 85361.71358331505, 85362.24200974044, 85380.07370192127, 85473.45423585098, 85569.80885720404, 85575.54990806535, 85628.90620862838, 85669.12075503325, 85837.18405656797, 85850.76790855199, 85869.68747229627, 85891.72893301869, 85916.35549374677, 86072.83270895985, 86138.58472999885, 86175.59907116221, 86263.22791255025, 86317.92189857212, 86330.49870061636, 86362.1868205904, 86428.67213912777, 86437.21011143111, 86649.65796730877, 86704.07215332007, 86773.98110998965, 86803.9776268788, 86861.80190914104, 86968.27303992331, 86983.09128359566, 87114.38680407715, 87312.55457397919, 87323.51826934211, 87331.4602299734, 87342.02971638544, 87350.38376896363, 87536.70552184065, 87583.8072497944, 87640.78795474865, 87665.76696707116, 87752.55671290358, 87829.81779429199, 87845.34610148527, 87849.81812126611, 87878.81943456715, 87916.37107871319, 87924.2980469499, 88022.25953977634, 88042.77908930826, 88086.90248151377, 88154.84808114136, 88188.59314544954, 88213.67570161515, 88346.01224312352, 88380.34756147928, 88381.0187776586, 88392.03269038099, 88475.41244574988, 88531.91958503833, 88641.85134935004, 88754.03910795924, 88775.9354654928, 88950.32244914462, 88975.70418732113, 89021.81870067224, 89129.9125501228, 89171.5412899617, 89236.86530114552, 89359.02813176817, 89369.17102371113, 89397.58775103434, 89561.91740323161, 89574.92273231884, 89733.03407883554, 89788.8641509923, 89798.37708009258, 89934.71267652512, 90054.9410919463, 90128.84469534585, 90142.82571125287, 90333.46624021447, 90350.81804589435, 90391.31459772254, 90392.00452827432, 90717.60785681613, 90752.35255726802, 90916.79269171291, 90979.19403631758, 91035.54177813925, 91056.1537710944, 91103.33820213393, 91125.50240795127, 91215.1883364435, 91246.19571686219, 91267.93258638348, 91285.66498767474, 91298.89714460267, 91390.17058486002, 91514.21590267669, 91522.21951470345, 91529.54656325365, 91535.74718708034, 91543.8073577664, 91621.45385615826, 91634.72905257734, 91652.07401453998, 91654.04900136072, 91656.62607958663, 91782.93527221377, 91805.12571890188, 91890.21350962158, 91897.8106167749, 92047.59946949081, 92116.97822850605, 92175.67325569765, 92197.4000214709, 92210.35514599236, 92250.57351671028, 92268.78242733548, 92271.97360779619, 92314.11214267305, 92325.94776035091, 92389.75189168332, 92429.65927771182, 92518.55132831555, 92534.8624643804, 92615.99679708626, 92655.95168052336, 92685.27265145129, 92691.79123250619, 92702.85000997306, 92711.07603536066, 92798.54755144315, 92893.56906347992, 92899.68312778146, 92980.37166995081, 92997.9175258425, 93095.57506858828, 93122.24527248694, 93304.4673520228, 93437.2574049249, 93480.25345534232, 93536.48882405502]

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

    X111111_1 = [39308.71014203647, 39327.973760101624, 39424.26226937722, 39459.59953697595, 39484.64190808078, 39520.846649782754, 39537.765643599065, 39661.31101067977, 39721.015344632084, 39782.66362567632, 39813.99175383313, 39820.65103172622, 39878.553361390506, 39915.385071494806, 39920.62227045753, 40058.66946035278, 40084.50443265132, 40124.43361564056, 40170.862865096424, 40197.06040125394, 40209.68322402971, 40224.74076015881, 40240.07553943351, 40263.42098061106, 40287.85011650691, 40314.02171008786, 40353.294221787124, 40375.1582464688, 40437.882571110604, 40439.95386945322, 40636.3302691047, 40650.50749834436, 40650.75560192231, 40650.76498618839, 40761.682901682565, 40790.47030129951, 40865.01610974372, 40903.136338511395, 40914.22123929637, 40922.03092061217, 40937.50235606635, 40983.83239959522, 41003.466231425875, 41013.72884940091, 41062.02834368133, 41330.05934567244, 41375.94702334658, 41383.417329128344, 41390.058242417166, 41482.22649139352, 41588.27282365888, 41616.40868488357, 41674.21513785147, 41702.391879863564, 41703.67878294314, 41821.923317295106, 41825.37997624217, 41898.92022108077, 41932.967203101565, 42002.058323486606, 42026.72770159753, 42045.05590248122, 42178.35451394568, 42213.61335863114, 42286.25305067936, 42306.6531084228, 42327.22459677668, 42411.47163479831, 42441.87661518057, 42460.16211633279, 42621.686288704586, 42629.74792335357, 42640.424999029354, 42716.130731515725, 42729.37339697726, 42748.901493746445, 42764.91825352361, 42823.971369048384, 42881.70908243856, 42946.11569709429, 42961.129845677264, 43053.03283917017, 43086.627367069974, 43094.28167886853, 43215.19431383789, 43411.38939876223, 43416.82648257054, 43435.11762645615, 43466.67852752238, 43715.62705217409, 43751.34993199048, 43838.40163858909, 43971.67277341932, 43985.21638709578, 44028.596628307525, 44056.294671393174, 44149.03194329752, 44176.358250121324, 44180.25733707933, 44204.712338119694, 44262.96662141724, 44290.896443776626, 44302.70114069194, 44316.578758680225, 44397.19665856761, 44413.27917745001, 44459.61519251925, 44530.45734190275, 44619.31351357112, 44679.85029475837, 44706.161550166464, 44763.68662615485, 44810.167534263055, 44811.20452345503, 44827.82258911213, 44950.578674949036, 45080.36647031775, 45135.22565436298, 45193.05667118566, 45255.77266654382, 45301.374813950526, 45618.34218139142, 45665.30855519318, 45701.5131021908, 45710.83272964945, 45727.9966089985, 45796.86295676023, 45799.51649290519, 45825.62557128725, 45847.54616296228, 45855.147921727345, 45856.47714234456, 45890.599220997196, 45903.67889979228, 45963.08685818054, 46092.253588960666, 46094.00999923036, 46120.77151705186, 46156.04840604063, 46186.827557930716, 46368.67057438654, 46412.745260347765, 46437.244373479596, 46470.11177814647, 46472.65547107109, 46789.161300731386, 46855.23497572087, 46859.057113081304, 46869.81332498562, 46871.799725414974, 46945.04754001067, 46978.255835803255, 47017.64023603036, 47055.98138524437, 47097.15567041079, 47102.8830492314, 47133.144717358424, 47163.33330917151, 47197.39563357855, 47198.46301250058, 47370.102873660806, 47377.08071978448, 47478.01457620907, 47556.38154093067, 47600.419746771135, 47683.7082529316, 47772.107615571476, 47779.93552543631, 47829.3569541033, 47854.10084698578, 47885.57523511431, 47996.18869928352, 48088.54501122976, 48168.043707683835, 48276.41783845218, 48282.01177381379, 48298.28902843914, 48375.850407330814, 48456.71455886177, 48462.85617665322, 48508.2182078943, 48526.64706253976, 48570.698944649026, 48604.37700844846, 48615.363641174525, 48784.39311729249, 48855.75325672066, 48875.2866045905, 48875.71561583219, 48879.98156222187, 48912.381459223296, 48933.95830352203, 48991.82639774684, 48998.73255226105, 49072.53001120035, 49073.92801710019, 49147.5257233523, 49157.93549607893, 49160.6756493299, 49300.69805884348, 49345.189921282625, 49385.79462017231, 49618.373825984396, 49618.780002565276, 49619.88683291005, 49658.817007579266, 49788.267482849435, 49790.35796561578, 50032.85738605489, 50075.99894634255, 50140.14184952617, 50175.27816935131, 50200.46680023873, 50288.09239602189, 50308.6187653747, 50329.015581300315, 50343.31883409698, 50361.851867494726, 50393.13072005659, 50542.266184265274, 50544.659637372264, 50635.88557123606, 50653.201911527474, 50669.44841003006, 50689.66590032967, 50702.05190935808, 50780.42955241917, 50813.1551597888, 50821.39094452012, 50828.78079345432, 50841.32960818442, 50853.187937479546, 50881.09792707393, 50941.59333248586, 50943.17744397625, 50965.41189160255, 51019.75067583888, 51044.59087551832, 51056.3977744579, 51069.64829131668, 51103.623921103295, 51122.80149674622, 51167.60501158083, 51355.067334921376, 51529.76413956754, 51551.01355291924, 51561.562963162214, 51750.5113754194, 51898.47613556952, 51915.2719902095, 52033.50559173483, 52173.001981585236, 52293.17555918645, 52346.2139308488, 52394.31643146013, 52492.178472377826, 52505.97697068529, 52527.29033961702, 52543.72783104798, 52552.4443953547, 52564.67302283002, 52591.43709808836, 52593.60077942394, 52692.951995373274, 52714.67819142877, 52789.94831241458, 52871.94248200912, 52987.951388732145, 53024.50813522702, 53030.29363397188, 53065.877188945604, 53143.11318387064, 53272.134268347174, 53287.527508400344, 53295.52363836444, 53328.05840829179, 53469.464356824836, 53530.444992040764, 53548.60729925665, 53548.90242758252, 53584.68613156125, 53672.9251063534, 53706.408636770495, 53724.02094127949, 53730.26550678555, 53742.00943207301, 53755.24311761178, 53823.452269729256, 53847.846910221735, 53976.943727430065, 53992.83090848644, 54056.12663865891, 54062.14247898623, 54151.30740292909, 54246.333008291855, 54310.42219710066, 54351.35224998737, 54357.96037074672, 54458.814065975304, 54489.34629529985, 54564.042496149865, 54709.1933258941, 54712.13160529245, 54725.09706723673, 54735.32346270945, 54746.915599980886, 54775.63485549463, 54818.87850812755, 54977.83365463994, 55049.20309153109, 55050.78942681699, 55083.94550041801, 55097.514519790915, 55210.8035162694, 55242.39730445909, 55262.82217796178, 55286.96351901758, 55308.05916459663, 55313.54037086811, 55329.00433366122, 55339.28915033497, 55468.35233285577, 55613.62542485176, 55661.28281296823, 55758.33357568484, 55816.11419924276, 55898.57846478972, 56011.44854864466, 56084.18778467713, 56095.94694027328, 56125.03939474469, 56221.87974400304, 56337.94310009577, 56360.91535426382, 56499.16680875961, 56576.19020163226, 56612.28272186492, 56633.72299619588, 56689.6186499676, 56808.52416321817, 56851.504235692446, 56903.72385818345, 56930.563676764155, 56933.44962029031, 57004.97346314759, 57065.27813862944, 57131.12502424616, 57140.03631997705, 57157.15071931162, 57232.599011733735, 57316.05571433294, 57345.13024143229, 57431.92418042979, 57506.75078024803, 57578.325043657605, 57607.25779358358, 57622.33405459407, 57663.728067383156, 57679.56096844685, 57816.987330547905, 57818.760928806965, 57891.36337303305, 57909.88793623864, 57949.14232365346, 58007.99694865437, 58072.8986611702, 58097.078434143164, 58155.67965799279, 58224.0527974493, 58269.12089877369, 58462.528591974435, 58473.45773809906, 58725.018865939026, 58772.340007417064, 58806.516396005456, 58932.2376037607, 59074.53264574229, 59094.01036878256, 59096.79245327534, 59099.7585260928, 59149.162220401246, 59211.91458184909, 59232.77807641433, 59277.40538398973, 59497.94824411222, 59592.31403063309, 59627.471085752055, 59781.03652627188, 59836.67499931055, 59858.50754713212, 59908.419907053685, 59916.13331697216, 59962.00774938837, 60156.119902921324, 60212.41680426926, 60315.91397275805, 60337.20575116836, 60362.502409095345, 60366.86132483433, 60475.79095362485, 60491.14201850648, 60588.56725904126, 60779.50819430124, 60820.377069387396, 60990.75216315873, 61029.18742885079, 61112.777485884966, 61127.616262743984, 61136.12850478387, 61178.7407920312, 61309.46372069695, 61404.95677676755, 61410.79031469158, 61456.43232366026, 61492.84623774281, 61563.78927849364, 61589.570601609594, 61645.15413597984, 61645.82776008185, 61664.14283891207, 61664.86307174853, 61665.84675117352, 61708.14433907902, 61773.231804018724, 61774.793539050006, 61872.23851853667, 61886.56200350074, 61907.164159351494, 61914.0788421457, 61928.98061977279, 62057.697815317326, 62073.95374563117, 62108.73398299211, 62212.13466489827, 62335.654923223985, 62447.96923040552, 62455.56413445303, 62485.540724436745, 62499.929482392545, 62527.004064827415, 62621.5194142536, 62728.73984518407, 62744.12347319994, 62798.32025284726, 62853.997276198184, 62883.499126806055, 62978.00011431564, 63131.28014970162, 63132.28329664287, 63164.38539922741, 63243.08583752588, 63404.527327487645, 63441.95817879717, 63490.156985684014, 63513.162319415365, 63534.73694810747, 63606.10180905428, 63733.748467217185, 63777.54424946747, 63777.76806484157, 63780.99477239337, 63873.18794785653, 63878.516784070205, 63995.10349171446, 63998.93752105042, 64049.848629813074, 64067.3946086393, 64095.699502489646, 64260.82399054742, 64287.474133275005, 64363.569151501695, 64375.01393093904, 64375.661978885284, 64433.024573388044, 64442.608323070206, 64461.28854924222, 64484.028880240876, 64588.863594879345, 64593.9205948543, 64612.34604211979, 64633.815000746225, 64667.58989466406, 64745.12823983563, 64772.37043836076, 64823.14335480577, 64901.83147538295, 64936.305020004176, 64938.77231569355, 64986.0688898471, 65001.90461227657, 65076.22462829713, 65203.126420722394, 65228.899823883796, 65266.45841512509, 65272.38950179385, 65315.86493995693, 65414.67489199666, 65416.29836462739, 65428.57436373821, 65467.79512185255, 65497.02860840556, 65500.50894569735, 65670.43020115864, 65977.06517034616, 66126.49495507508, 66218.94765545089, 66270.08369352474, 66288.24351949792, 66410.75471282878, 66459.8748964073, 66542.75258199821, 66570.79474429312, 66632.7981842845, 66650.2870964972, 66794.01709060992, 66928.6129444274, 66937.72950005466, 67006.68968378699, 67130.26807057208, 67157.68566739418, 67169.63817573214, 67209.29938056791, 67261.40212561752, 67266.93464139677, 67331.33486789523, 67379.70586926861, 67477.36881406246, 67486.57106513472, 67582.05780124161, 67603.3602126062, 67618.32414495244, 67914.94977028103, 67944.08591707012, 67968.59272526418, 67991.2135167681, 68153.7464426308, 68196.29641381296, 68201.88580443627, 68308.93753962437, 68335.31607566083, 68405.46137233562, 68417.98351850169, 68591.37191632896, 68611.95862496072, 68669.35352195393, 68685.15408298637, 68691.67392319246, 68719.47788880265, 68755.95402769459, 68901.1922623837, 68936.01029847693, 68947.82277227903, 68957.41106644529, 69095.15180543874, 69202.75230072645, 69264.79141530288, 69276.89843883175, 69288.6221028756, 69361.44869224605, 69396.02216800326, 69515.89451183986, 69521.07515039945, 69548.71022920546, 69578.99365543041, 69581.37860355552, 69623.67152848656, 69703.17493748986, 69728.17835605145, 69791.67599142918, 69811.64119226136, 69868.79669615562, 69879.11025315203, 69997.4901541782, 70035.54061689645, 70183.30200966606, 70196.19784127474, 70229.43899964061, 70310.55460409273, 70320.07940516893, 70333.71352057552, 70610.96533171133, 70637.37332220841, 70703.84906022783, 70847.8203251482, 70883.84050694204, 70903.17080291764, 70974.37016019378, 71014.47182867104, 71108.50160364438, 71138.84449127091, 71149.60071656467, 71254.6983453887, 71260.42109592969, 71313.08645413037, 71369.1430158763, 71465.96910071155, 71513.590740669, 71566.04208991345, 71627.41758194432, 71815.41988790654, 71819.64207873684, 72194.81212965073, 72263.43960603468, 72282.16514335759, 72472.52375505274, 72563.64386374471, 72620.1781743012, 72640.3454903596, 72655.2997841191, 72665.40743306608, 72733.75887944963, 72758.8087633194, 72808.64088916843, 72827.81354084641, 72829.16993576265, 72841.55516175178, 72852.86989766965, 73020.23435668195, 73150.24110484913, 73251.18335379266, 73271.50909898308, 73313.50435808778, 73373.19869983166, 73485.3046867917, 73824.31241932286, 73879.79615788552, 73894.9920002209, 73917.92720020247, 73957.53275244008, 73994.45939495655, 73998.67339624581, 74022.1428452856, 74075.25929307114, 74092.03342714638, 74133.84129043376, 74359.54320813333, 74498.94143873315, 74529.94028604061, 74552.30283334965, 74586.39536008143, 74590.9475324796, 74628.91417647063, 74639.53422720805, 74646.70086448542, 74648.10212469735, 74685.97407527363, 74705.49619416287, 74714.00645877185, 74738.23177257596, 74748.12697148777, 74777.70023676202, 74958.46300635036, 74986.35639499806, 74997.26391686106, 75152.87802868165, 75154.44328244678, 75175.62948653026, 75196.76747476801, 75219.75166841203, 75322.22643860533, 75370.70428078197, 75494.90565355268, 75515.88090738821, 75604.49466976509, 75627.47302839233, 75638.10202481256, 75667.4923176198, 75725.21622312602, 75844.65780978985, 75875.34971233978, 75943.67207918793, 75963.74664536785, 76065.46411627225, 76066.00829534931, 76082.40679914292, 76102.6419653295, 76136.45630624902, 76166.49679656606, 76185.80571268755, 76191.69815386133, 76255.44824190487, 76288.26150683183, 76399.12228691595, 76530.20466622667, 76531.39294660074, 76591.19147567463, 76617.13659812113, 76678.44519606236, 76786.95943767982, 76792.43503979518, 76796.40545786818, 76862.17687108953, 76918.35728475223, 76978.08828408617, 77010.98591565849, 77034.02024058884, 77097.573142548, 77166.01518963015, 77216.28012587811, 77252.8892243728, 77271.66268658423, 77350.31474869102, 77383.68017296234, 77397.95235845845, 77462.04502914203, 77473.15602785384, 77507.41622135937, 77597.54113315421, 77600.70813863826, 77626.58253978456, 77684.1324610452, 77712.64105532895, 77753.87129595313, 77871.06208644182, 77874.76037411386, 77988.0233089968, 78060.29061553476, 78081.48113913367, 78185.66934075783, 78228.67059576754, 78230.97160356684, 78451.58308289589, 78473.24814311482, 78506.90240515934, 78525.00933385044, 78549.11910856815, 78590.603412834, 78702.2632845768, 78715.85739401547, 78735.42625249975, 78821.38640530134, 78884.06287547082, 79090.86069063353, 79116.47147950684, 79159.14439649446, 79296.84659307197, 79297.3163459106, 79397.65029971351, 79416.68202768137, 79451.0449525524, 79680.00759272181, 79822.09344223916, 79875.90689320775, 79893.8538829365, 79979.02240672309, 80047.76358410508, 80076.36107314946, 80083.64562235822, 80122.53975938178, 80207.966294607, 80267.22426137223, 80291.40193734862, 80292.03968915214, 80308.93477154904, 80341.08897509423, 80482.76029085666, 80486.16647046307, 80494.07209711336, 80525.27609952178, 80580.41090821155, 80657.56782521696, 80715.23087711819, 80740.8707595942, 80753.81236060837, 80904.89855053806, 80967.10542970583, 80984.74603729139, 81323.75189719535, 81334.53102216095, 81337.0113619247, 81398.83240426474, 81420.48074408786, 81495.79749679934, 81601.54762718173, 81604.34602048571, 81642.14629937094, 81738.6495587164, 81756.72845104389, 81795.64464613618, 81827.36965165238, 81828.58389986372, 81842.31286588887, 81922.36194179562, 81957.93896767116, 81961.93449290693, 82191.82011675225, 82200.43414496962, 82252.64029161484, 82341.31230766585, 82492.73243861352, 82539.15812216216, 82548.34826566731, 82591.456543529, 82616.98507241659, 82665.19100421472, 82699.02192031572, 82716.05039658751, 82772.63648167808, 82846.75754156036, 82851.10262414961, 82948.44731986594, 83050.13564561296, 83090.69166314614, 83242.13589882539, 83250.15327722924, 83272.44926812887, 83352.45282847114, 83372.0188775618, 83408.57584652166, 83434.8329073175, 83447.49932744735, 83464.1561525548, 83558.25727166452, 83578.58807662858, 83612.10676824054, 83663.385917121, 83928.02391494226, 83995.23514049278, 84063.50760290978, 84235.8592650134, 84242.88755612787, 84275.1083310508, 84275.99398220837, 84336.79750301727, 84361.2469621193, 84408.24252452923, 84439.10587159896, 84517.43778964848, 84521.41146958228, 84560.86236703818, 84662.65754297905, 84748.21341787733, 84757.948820954, 84795.96190397904, 84817.19986079764, 85011.34837598927, 85046.40895099011, 85092.47244351343, 85209.18268442611, 85363.77740061816, 85386.86215033603, 85404.76588015538, 85428.33546934972, 85429.86812907041, 85471.13683355946, 85479.74001470415, 85519.72464547094, 85531.58391463602, 85555.28096907758, 85692.72992169936, 85714.63229248932, 85819.78950062042, 85970.32104295852, 86084.76335673139, 86101.4734300191, 86533.31056414775, 86547.49488667048, 86641.09887860893, 86650.12280513954, 86747.77522771774, 86755.73758946228, 86759.03576630267, 86811.14727942992, 86814.96888507046, 86854.69091068729, 86952.16794164269, 86964.59944614972, 87061.73970447844, 87106.02593814039, 87200.28021375833, 87219.02411915394, 87292.60995650518, 87315.91964945487, 87412.45976320072, 87442.86550137258, 87474.40715228877, 87642.44634581506, 87695.30179586484, 87698.86280666967, 87725.07861335656, 87800.44836707701, 87859.90402386084, 87891.91364692754, 87895.56333225951, 87923.86413616603, 88044.34175971281, 88054.96506741262, 88147.41981483791, 88149.0868162234, 88185.88431624678, 88304.25610552283, 88333.30510036384, 88386.96323968904, 88400.11778777555, 88415.55979367519, 88424.93066482188, 88427.40272559934, 88481.33423782347, 88531.46239446034, 88551.22465401056, 88638.20220346471, 88641.16100293485, 88761.74786135386, 88842.76187446645, 88853.8219338451, 88867.8073387846, 88915.47519994044, 89067.21964877407, 89196.98737349446, 89213.67413652549, 89220.40582490919, 89270.60724328304, 89279.21354890708, 89369.19572367451, 89376.14347253757, 89476.85179498102, 89546.53052606697, 89613.04475099286, 89698.28334079767, 89746.34866382432, 89832.84327669247, 89834.31068003346, 89858.43299221926, 89900.59103619351, 89921.18714045173, 90045.96575797608, 90177.04259384578, 90209.89049284214, 90255.08118141537, 90293.34365578397, 90318.33954540017, 90335.53165131592, 90338.96340438696, 90343.58392855327, 90402.60520373381, 90433.531161011, 90444.4621124961, 90502.42672539988, 90559.9111815986, 90629.98459292675, 90671.06794135933, 90680.00616272728, 90681.46142150037, 90694.57138254476, 90834.7157047136, 90906.09634749324, 90921.01552810817, 90953.74215499856, 90976.34083856526, 91130.50872290708, 91149.42032232165, 91156.40412180198, 91192.60703540474, 91387.42590688058, 91397.72232245497, 91404.06279569311, 91419.21761866851, 91431.49295152917, 91686.04445366026, 91731.792171055, 91759.20532782511, 91764.63387901348, 91805.45525755393, 91891.95517283375, 91934.72847483074, 91948.00400691133, 91965.37953643859, 92071.22023214228, 92163.13598452101, 92193.41703572568, 92354.83454118337, 92444.54767428245, 92459.17584901294, 92481.20568891455, 92492.85909929287, 92556.27279210772, 92575.78563178156, 92658.46153738866, 92673.63959176448, 92770.26712749497, 92803.57270200495, 92854.24556706504, 92865.81945692372, 92956.46977336369, 92973.69578591458, 92985.45179962588, 93064.22497243938, 93108.02279156559, 93194.3578555382, 93204.94950601505, 93218.11290523899, 93260.1791004081, 93283.85485310317, 93289.6063990549, 93341.20298452894, 93362.3779975312, 93391.71295107622, 93393.70618464166, 93401.66220625104, 93424.2867437955]

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

