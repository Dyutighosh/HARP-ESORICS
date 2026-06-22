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

    # print(ratio)

    return best_K_correction, min_error_value, mse


def SubMainFunction(Scale, Intercept, filename):


    start_time = time.time()

    min_val_1 = 25039.10669694587     #min(X1)
    max_val_1 = 43535.01033272372      #max(X1)


    X111111_1 = [25049.261262690907, 25054.294705136734, 25062.76028060712, 25074.360625669116, 25076.835963592184, 25088.8279194613, 25096.802111561614, 25182.815571338168, 25183.22706263905, 25209.896495523888, 25210.40217667102, 25239.310770180793, 25247.558851797265, 25269.83404017783, 25281.967605149865, 25288.096914426616, 25338.605572088865, 25339.9945363621, 25346.994429745748, 25356.88725406049, 25362.179175583038, 25386.443078254648, 25407.335031585208, 25440.472755758172, 25504.100138345268, 25556.496023523083, 25561.495105929644, 25618.58299506386, 25661.410021717806, 25682.814196082745, 25731.329477624862, 25739.341982398266, 25791.091776206173, 25794.223060923854, 25810.427071021655, 25842.20078778421, 25858.134487843112, 25864.74166317242, 25901.645766579106, 25922.92374585203, 25939.34598270386, 25944.744062007063, 26007.31214334295, 26084.603365482624, 26086.662773891116, 26128.620773644547, 26141.53870251947, 26180.69453071891, 26182.01767771115, 26189.94086331297, 26225.832592418723, 26247.235204161403, 26274.81596731778, 26290.09071036643, 26304.624192979274, 26308.695471125277, 26339.79880459619, 26341.222416161294, 26359.888336302665, 26391.9423869838, 26394.507959740375, 26414.521789231694, 26417.492147043344, 26419.935554706568, 26423.827474149184, 26425.3787106367, 26428.649320646302, 26448.66450586709, 26472.191484063052, 26482.010474630504, 26553.61958123308, 26562.480770766233, 26576.256861418402, 26627.314160565413, 26661.096156559306, 26672.959129606126, 26688.888349611458, 26693.198403737668, 26694.54308441717, 26746.288064919238, 26754.953760365894, 26759.41358197615, 26759.971095432724, 26779.298656092633, 26783.258419134505, 26783.75782901227, 26807.108058475707, 26808.605959827113, 26838.02803971602, 26851.860622609183, 26918.724112504362, 26936.203717898337, 26948.122634917963, 26998.559600506243, 27012.44731166384, 27013.85828865203, 27034.785981877067, 27061.67645974073, 27080.55354304449, 27096.815625424882, 27099.768405397408, 27106.11551230963, 27176.45645062503, 27195.983901047573, 27288.058126129603, 27293.41014766466, 27312.191605234, 27317.811504603484, 27333.331691765132, 27334.806410778794, 27344.97679762383, 27346.321661760885, 27353.886560049308, 27373.53764501418, 27373.55582868685, 27390.84662250357, 27392.213030060288, 27393.681886975683, 27436.00192439143, 27443.899441327212, 27451.724824173947, 27457.019818871977, 27464.832081918386, 27493.630383191055, 27517.658218043038, 27554.507899584296, 27557.49325303852, 27564.727943761645, 27573.665347239687, 27610.32491477702, 27617.242652013043, 27623.83037985825, 27668.01076421971, 27698.743621073078, 27727.039132284895, 27738.473083628734, 27750.873564266894, 27765.69789675815, 27794.35544892581, 27813.504262823713, 27822.131565658074, 27827.35368244202, 27837.912466989175, 27853.3054358359, 27866.868285918143, 27882.24922317407, 27913.636592225666, 27918.398942391883, 27929.397937249243, 27930.27855285375, 27949.67955988626, 27952.409892799915, 27956.412658455145, 27973.200849595836, 27982.126707913223, 28020.8571908033, 28022.232429620475, 28023.6670876338, 28044.094104509517, 28059.382702485527, 28086.666481817927, 28124.31320149443, 28133.67583979544, 28138.34217158085, 28183.388511022888, 28192.056348125192, 28199.962209992198, 28242.156116628794, 28244.211421876615, 28249.925962655987, 28258.226508389223, 28261.542432237515, 28284.547810959306, 28286.976764628896, 28299.398859260036, 28309.72952211878, 28325.87944473183, 28344.44734197019, 28352.124388330973, 28361.47031227455, 28381.46616455838, 28415.88696127054, 28418.498363219267, 28446.808350174644, 28453.79000348367, 28454.013083233505, 28465.67005612938, 28477.801478651283, 28481.531625163243, 28485.84521189468, 28487.073401810543, 28505.397485686575, 28517.508547821577, 28525.303148473853, 28557.95915320703, 28563.84113109921, 28568.008374826524, 28568.664546015163, 28581.45506014127, 28593.495289187787, 28674.628613124383, 28676.108333612512, 28680.12932797242, 28698.906524584687, 28703.04297424899, 28724.756071749467, 28731.00068851587, 28750.11046118334, 28751.465923079544, 28764.495680828746, 28767.785735294656, 28769.74159728927, 28808.483832022168, 28810.91783547021, 28836.443265411566, 28843.51460734645, 28940.57208880444, 28996.407025643217, 29005.28209897193, 29016.962556908453, 29060.409164736015, 29083.886727782763, 29090.60042195668, 29093.053088650882, 29106.109126783245, 29109.335035531334, 29118.979347122244, 29128.38393715016, 29137.79558840323, 29140.123178351678, 29191.246433276563, 29214.860215401543, 29226.614275981054, 29258.813503588994, 29270.647913127646, 29294.653248174993, 29337.193427527192, 29361.04764583663, 29362.711116096798, 29376.98077169044, 29409.252670862224, 29415.12713457136, 29427.853412846292, 29430.240080143707, 29484.277362988283, 29490.666064980505, 29494.930706503386, 29495.87399775125, 29497.034564811263, 29538.897597586234, 29585.541878230088, 29605.410977887404, 29638.533536088995, 29667.829396079076, 29673.297637924738, 29706.194313226057, 29706.625341343133, 29791.07950384062, 29793.302857130097, 29802.66103256098, 29818.456188240878, 29854.090088761022, 29877.509536033573, 29885.74903533973, 29888.500968790686, 29894.716672789305, 29910.530920049223, 29926.33281327844, 29971.507780136748, 29984.463762998515, 30001.47983836003, 30012.382340249886, 30018.05003502652, 30032.496825966788, 30042.12199231782, 30044.24787669873, 30061.342210867402, 30080.378357867252, 30086.896005365124, 30152.19390890394, 30153.47060185345, 30160.793258617643, 30161.015445414887, 30170.09171743799, 30170.260290532162, 30185.01784519633, 30219.846091024894, 30232.145694460985, 30239.47493891444, 30242.12688291337, 30253.87329404887, 30257.692866085403, 30347.11537319951, 30368.096348597483, 30392.92048685022, 30451.317030253074, 30459.144722590223, 30490.754484089917, 30496.8501808463, 30502.29934661858, 30524.81884621371, 30603.46161611507, 30639.00471466573, 30680.502813942367, 30691.91119098057, 30712.397106111133, 30746.726705442965, 30776.555975671934, 30778.341863782945, 30778.857392659345, 30783.666322407385, 30830.893715105063, 30832.901061576325, 30833.815784522514, 30840.12953686073, 30846.49680052466, 30849.967442279987, 30867.893880251955, 30927.371472822877, 30936.767510337926, 30978.85259325924, 30987.722274577507, 30992.31391351939, 31004.933778722832, 31006.16660516504, 31031.21743185047, 31031.355973555743, 31042.831640719603, 31058.210039419664, 31063.291395911703, 31075.252454252, 31084.185073420886, 31087.63397326837, 31094.112235407814, 31103.68688090423, 31103.761019291433, 31105.060584082836, 31166.056894727284, 31178.9980757707, 31190.568052333812, 31218.806980196132, 31258.325606626408, 31271.382140401354, 31300.11590758695, 31316.176511173595, 31318.95779757365, 31324.71932703615, 31325.835129908814, 31327.823236753746, 31340.648094454373, 31389.120339006928, 31415.710561961827, 31574.10840012428, 31585.750542336744, 31592.157037615812, 31704.204433889554, 31731.713353209627, 31784.639538593525, 31846.41499432142, 31858.316724406097, 31858.46096651859, 31884.70920939692, 31892.905011997154, 31899.791935741836, 31978.737828822705, 31988.74620712526, 32028.82756644966, 32044.585641514986, 32058.836513785674, 32062.22594047774, 32084.503685754473, 32088.431663976095, 32088.922106838232, 32131.389547873943, 32132.56260668418, 32163.04426408353, 32172.908402094512, 32174.113048845476, 32176.281423071654, 32182.488807643706, 32185.372011110754, 32209.0648420653, 32244.92317066115, 32288.65735065038, 32290.41673939571, 32330.296721932627, 32341.78224479622, 32346.936240894145, 32347.33469445607, 32359.783880654704, 32364.992963964236, 32369.93322403144, 32422.25105544311, 32423.869317460823, 32474.055393969615, 32497.81046975389, 32561.547438935435, 32562.352976121976, 32566.580231491575, 32597.900458638032, 32639.17326148049, 32688.03800563609, 32695.703797836384, 32712.23509789199, 32718.6549259908, 32732.253409532135, 32750.80155841136, 32757.711035674503, 32763.937567757162, 32764.3581908568, 32784.137466225664, 32802.87984053475, 32844.0326490512, 32849.431177577906, 32902.42438989572, 32928.37473177813, 32934.47852301762, 32958.915524072116, 32960.40574794448, 32968.461563522054, 32986.22936210697, 33042.108925976965, 33087.049194010906, 33094.204193848505, 33115.020603299614, 33125.40002605718, 33151.72897611814, 33153.58747451906, 33159.05845172673, 33166.75581789475, 33170.39823540024, 33187.33887414713, 33190.08031138179, 33207.832175386815, 33222.20636881952, 33244.33745334598, 33255.60308667203, 33265.44805121498, 33299.06048344903, 33311.88239949176, 33328.02604586184, 33337.49106067966, 33359.82046657598, 33361.27904117607, 33414.34391087641, 33419.169521023985, 33451.77488027621, 33467.43091668642, 33475.25266691869, 33481.834938606364, 33485.09603760761, 33490.74185627971, 33520.82632207551, 33551.52876924624, 33570.000992626046, 33572.17592990702, 33575.400716694974, 33598.942521210185, 33663.030505886774, 33671.90036826757, 33673.35318350101, 33676.73785721472, 33707.33915688163, 33707.62637107738, 33717.42314903776, 33726.218507268146, 33727.65061348134, 33736.772123358096, 33745.906142817104, 33768.20988793722, 33774.86244533716, 33784.494949483924, 33805.705242595075, 33832.28440779606, 33851.72233079065, 33854.483418440395, 33886.78696607428, 33901.30021619015, 33929.19307411542, 33942.87068654177, 33945.81337900317, 33947.78475302459, 33963.62466570921, 33969.44823890636, 33970.209513703405, 34063.88548323176, 34076.60889650279, 34077.216144757665, 34091.5830397752, 34115.26883458169, 34127.674340214195, 34139.413086841014, 34141.32564391047, 34143.57043810358, 34143.738677920825, 34169.64157043148, 34173.50847972875, 34188.99523795488, 34201.41922449002, 34208.20316119348, 34215.26521453078, 34219.00779007041, 34220.69566612615, 34227.28774307319, 34258.561179152595, 34276.72396886764, 34310.27406233715, 34345.75713491856, 34352.67791794268, 34356.65848682085, 34364.9656492364, 34382.26188350095, 34391.23814130122, 34397.68258889272, 34403.08626687108, 34434.28666945399, 34434.87868363611, 34460.90433287839, 34462.838239545206, 34476.72300211509, 34490.6507593372, 34492.38399418224, 34503.02388980413, 34554.97403154579, 34571.260114914556, 34601.30264604679, 34602.79498358116, 34654.42602719544, 34668.570299749, 34669.463514997784, 34675.88207911452, 34707.23065531911, 34708.653085947815, 34715.47702551597, 34737.037225446766, 34778.50103827229, 34820.74842954091, 34835.493531424836, 34840.547635921415, 34849.19141825643, 34869.881978773716, 34898.29764632066, 34910.75727035339, 34935.80229682088, 34945.76372173089, 35023.64490584437, 35031.81041080474, 35051.25255461114, 35051.71275495648, 35070.412906129044, 35074.97112525308, 35080.69634306201, 35097.5475824607, 35105.097176972406, 35121.99781688229, 35122.532489723504, 35123.063545882, 35124.16654095241, 35126.787971766404, 35156.59253314379, 35169.419089032395, 35188.19328731847, 35191.17137630174, 35191.219832702955, 35210.42398463645, 35215.135373002486, 35238.51685681486, 35259.03058343979, 35268.61658710994, 35285.677564329046, 35315.30067751164, 35328.80851535884, 35340.216861197085, 35358.98806755466, 35404.20595601945, 35427.35708083579, 35445.08919657764, 35521.81933362087, 35535.99944333469, 35546.45537341801, 35546.91006184292, 35594.14936233701, 35598.97697352484, 35630.39778279324, 35635.13635874669, 35660.15426175821, 35680.261666755105, 35711.53139906908, 35713.01919730983, 35726.47120146114, 35747.740538436614, 35793.4652646289, 35795.783417191, 35819.88449194216, 35824.668986156874, 35831.082936370665, 35840.902733090465, 35848.189471598664, 35852.91460312487, 35857.99391100884, 35885.152295218955, 35914.65192785558, 35924.072967579545, 35929.307161141405, 35969.25977697692, 35990.4599160192, 36033.71544594613, 36050.07362909439, 36052.2920198824, 36065.36196798715, 36072.361724488816, 36081.19666113198, 36141.83214470822, 36167.79429924941, 36187.55257237502, 36193.4579672625, 36193.85184814382, 36193.88634483536, 36207.88497218463, 36321.77903157562, 36332.33110856072, 36356.95020971042, 36384.47215400513, 36412.562511605465, 36428.83190932434, 36443.50594733478, 36452.78841496081, 36464.3096830056, 36470.67552293277, 36483.52555164574, 36578.40807727482, 36628.214063595806, 36635.30726136531, 36641.56528144033, 36708.392439189985, 36708.56548798472, 36738.725365416634, 36743.19870898647, 36746.629021314766, 36753.54910700907, 36760.31019730328, 36767.58758422737, 36807.01629445199, 36825.594081164294, 36866.43369068803, 36870.87507779525, 36872.06167534691, 36946.77517494456, 36953.07668291854, 36954.55176630746, 36973.19016106729, 36978.81408069255, 37003.71618630262, 37007.344088929334, 37031.83791550562, 37077.13236529444, 37110.53149685987, 37122.462034963464, 37135.402086085654, 37211.05299766349, 37216.04294065641, 37219.7039276952, 37237.86134824172, 37257.28301524176, 37261.31502403068, 37261.7040605247, 37265.55342469385, 37268.65162771017, 37321.166460841465, 37324.51118756451, 37326.33761596329, 37327.38092099894, 37337.1138029453, 37359.24183912203, 37367.845525277095, 37407.610416687465, 37419.90455797575, 37441.607391145604, 37461.29662560707, 37480.41277498871, 37484.38761402906, 37488.0027153065, 37501.8273674385, 37518.14176578753, 37538.29381527558, 37541.03687652676, 37545.36251701676, 37553.82506568975, 37559.6598336119, 37586.32271588413, 37592.700854876864, 37624.47546645509, 37651.47256104601, 37675.22305402484, 37678.082522607816, 37684.755690168684, 37692.92616757681, 37720.471898550626, 37745.23284958443, 37745.9722665298, 37783.555310970725, 37791.621508659424, 37798.57289815478, 37825.11072103557, 37847.63811090614, 37860.675969100535, 37867.94952427111, 37874.199608516945, 37884.60495629779, 37891.0158073485, 37904.13711195609, 37911.57301057401, 37922.60155628308, 37933.45071095199, 37939.323278558266, 37959.835977622504, 37971.091773228116, 37990.752484826065, 38030.52681034281, 38037.07185582925, 38081.5275383614, 38082.91850984359, 38108.751793841526, 38114.4909887343, 38129.87415654974, 38151.41884149413, 38165.65482701741, 38173.51421481219, 38201.26684818888, 38214.25801477313, 38222.47564671704, 38225.26151534195, 38243.11218223859, 38268.548440711646, 38317.4547726683, 38391.43937564106, 38391.85201806582, 38392.644430211, 38421.22589125957, 38435.9802985064, 38441.195350631126, 38510.21628410001, 38537.77586063102, 38562.81020176457, 38629.805103758335, 38655.85286739139, 38657.274651054395, 38668.93175927465, 38673.65082566033, 38686.18050612584, 38706.19800577025, 38740.9220860979, 38768.75768660814, 38772.70731534932, 38780.09586171645, 38792.84339797383, 38810.92323117292, 38828.844867881766, 38834.84096439497, 38837.1200713526, 38869.06752299659, 38885.54729529959, 38889.91196672926, 38899.79549582288, 38935.97539624472, 38965.24619299998, 38966.28241840541, 38972.15769158101, 38983.31851725039, 39024.91716262561, 39057.59162735297, 39100.559877603584, 39125.100693091605, 39148.47083107144, 39152.57419479819, 39193.15069245584, 39194.48193462723, 39215.19357081386, 39215.250601538406, 39228.5750921985, 39233.88732037712, 39248.66281955892, 39249.91395330549, 39252.26092021234, 39265.70996602631, 39268.98769059708, 39324.87572025301, 39330.568003316905, 39344.23527468003, 39356.11685806104, 39382.554083985044, 39390.848916722505, 39412.52587401079, 39443.15389228208, 39451.22748763942, 39513.952628557076, 39523.49734929548, 39534.04199596484, 39534.580032977, 39606.51715575828, 39661.87774135772, 39665.265706861515, 39674.733634178694, 39713.197513191735, 39736.35466081943, 39746.29977394401, 39760.08281380566, 39772.62022861294, 39846.76182780039, 39876.64315520861, 39878.93944344648, 39904.45207589994, 39914.39182241992, 39922.408674513594, 39929.28684866076, 39962.529363312045, 39963.84251112242, 39973.749603630495, 39991.48870417038, 40005.87861308342, 40007.640879767925, 40011.90601922601, 40033.55965957937, 40036.32774997337, 40045.09986407411, 40045.678541556954, 40064.827071176354, 40072.68234240734, 40078.07534618147, 40112.12674733532, 40130.92012040759, 40133.92176407877, 40173.30680448243, 40185.122995487334, 40187.078963570544, 40192.932492200576, 40193.851267329, 40260.36685592062, 40279.695961994556, 40282.711336972076, 40326.342243201456, 40333.89424540111, 40337.59520110379, 40339.61295690631, 40341.4618647046, 40378.872036581066, 40390.271830715945, 40414.47030277325, 40416.943212412545, 40468.53403566189, 40522.563559125265, 40538.156800255834, 40598.82705361548, 40602.99227801557, 40604.51887429365, 40611.35250297857, 40628.47102578162, 40628.77297666006, 40643.54723725864, 40646.98197403075, 40649.61440226749, 40678.72792717392, 40706.32007124386, 40718.602247649964, 40771.64655289599, 40799.94218821411, 40817.574693435155, 40862.224988384136, 40876.71105619568, 40881.262860470255, 40888.129366473484, 40939.873069878486, 40945.91694981049, 40984.33281127487, 40996.90274451788, 41012.74301295572, 41013.622706155555, 41026.505669868784, 41036.29118764538, 41040.15021115254, 41062.73486622569, 41087.9282047834, 41134.853473666095, 41136.42109324139, 41165.15765691758, 41169.29620614527, 41187.69567479349, 41237.54053741354, 41245.847400975195, 41251.86036731815, 41296.058269188106, 41299.37063400579, 41320.23481096, 41331.45766776212, 41333.07158911617, 41380.76059196029, 41399.13463971289, 41418.28580887796, 41444.31006021003, 41455.63569475369, 41475.965316540336, 41489.1855463952, 41494.089302579516, 41511.353331654536, 41547.47230392932, 41555.0129471341, 41574.29192412409, 41589.904333837316, 41589.91928355849, 41619.89069131498, 41626.54062797339, 41657.27731510889, 41668.11302681343, 41689.68379193671, 41703.02599774733, 41709.68065861591, 41803.44262233494, 41817.123463294345, 41903.570801908085, 41935.08038005221, 41946.63276388893, 41959.10907777757, 41992.23726954835, 42013.7645474132, 42030.48082799639, 42030.868406474794, 42052.7840485152, 42064.97022505969, 42077.59778622554, 42091.534284973946, 42091.77425926049, 42100.47741691181, 42105.76402250631, 42119.54739341741, 42125.08937857775, 42127.9682504144, 42133.732999832035, 42164.58918074733, 42186.41770575325, 42247.33586442716, 42259.7539482054, 42306.242503067, 42310.21126072971, 42318.67543458023, 42334.858874600584, 42337.898953936965, 42344.212483405354, 42349.5209471248, 42380.04527724581, 42437.24829187482, 42474.814884936815, 42481.04173179151, 42484.585464521384, 42498.86986610331, 42546.87185803073, 42554.600298587946, 42557.09000832853, 42570.144625103785, 42659.12304793934, 42683.76879341494, 42688.94554503767, 42746.589529599034, 42897.213268591295, 42899.41764410879, 42903.61152931934, 42923.813532118955, 42957.52960997519, 42958.129799735994, 42963.956457676395, 42976.35516756335, 43030.981168246624, 43031.32767242201, 43060.560939603354, 43083.44446731558, 43092.553887092145, 43136.53266719617, 43147.95255965878, 43151.79157659113, 43163.96808758823, 43166.5025489246, 43179.30473115641, 43207.698862893085, 43209.69904981136, 43212.226949094125, 43223.78599086094, 43234.75890725995, 43255.44479371235, 43296.83349641048, 43312.30673724921, 43313.62621449221, 43316.81509978883, 43321.46013823128, 43349.25178519668, 43349.90747400541, 43351.32411227572, 43411.5348709034, 43419.92497840931, 43462.37874974764, 43472.5621475841, 43497.007159651956]

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

    X111111_1 = [25061.03944862844, 25085.17856581437, 25132.923937985357, 25154.345090127066, 25160.579027388554, 25162.466488242007, 25207.05527809651, 25220.103777438202, 25242.213313298682, 25256.387831610726, 25280.181572877627, 25291.45051257151, 25294.94258809781, 25298.02397198324, 25299.638685428843, 25306.98554824716, 25339.70673203458, 25410.36009442161, 25460.116740938334, 25499.12297939025, 25510.216693146947, 25517.813834818742, 25522.80916501398, 25531.08227424455, 25535.238612080448, 25571.434570868743, 25572.013120386706, 25593.3734019136, 25614.269717159797, 25617.822791014903, 25620.898425280728, 25633.85810540389, 25645.48842656057, 25718.679948272937, 25721.054681354577, 25747.432360869137, 25761.408719560928, 25764.489675533594, 25767.273465282822, 25793.441723150085, 25799.356195284243, 25813.894604599485, 25824.025405838616, 25831.48483516794, 25839.229379166056, 25859.131018200227, 25872.8783339299, 25887.324547480603, 25924.5857622474, 25924.82534892423, 25970.059181739194, 26021.63739083807, 26070.31166729064, 26079.49918260272, 26080.35259263131, 26092.091786884084, 26122.259050210432, 26139.471109875416, 26146.142548780022, 26167.479348887744, 26204.370546316222, 26207.336108114825, 26210.177738217553, 26236.803476451452, 26237.724230867618, 26251.67345851838, 26285.90116973525, 26300.72757330904, 26301.420877998196, 26308.600848617694, 26313.97331229254, 26319.75163569873, 26323.10926934582, 26339.169032135236, 26486.65412398948, 26486.819451691466, 26529.927172688116, 26533.458466830405, 26536.393542529422, 26551.518409446173, 26553.669496762574, 26587.50046441224, 26610.73085699518, 26644.039695238527, 26680.119350553363, 26698.294471787376, 26700.033756123496, 26703.607712181536, 26725.03854358168, 26734.38408681514, 26775.05796664234, 26779.559051280707, 26781.319183679687, 26788.293346517305, 26801.224589579673, 26803.643672585884, 26807.406677957413, 26808.923647703115, 26854.17042579299, 26855.28877536812, 26861.420866817676, 26887.871739279883, 26924.411279490872, 26957.647064494362, 27000.999704575966, 27002.385895811825, 27006.367181469093, 27024.87295330923, 27066.594974937307, 27070.069288969815, 27072.96797042326, 27079.79835751307, 27083.31840369176, 27087.87560792011, 27102.44178212753, 27112.89243035888, 27175.512210670324, 27221.904724635544, 27236.493413014563, 27236.66536523213, 27248.62573674779, 27268.1776281605, 27268.24655944582, 27292.294822244316, 27297.67481902198, 27305.01856323564, 27319.52860225738, 27333.498823752318, 27365.461942795657, 27389.197229792022, 27402.70647358278, 27415.79769981193, 27417.41248421099, 27432.45865524547, 27453.388352535265, 27466.758244450008, 27497.575850602625, 27501.564037094682, 27505.865360197713, 27544.127779073468, 27550.95505594378, 27562.57111848088, 27571.190413055476, 27611.949961476857, 27620.52233175426, 27705.302084733903, 27734.13178449355, 27746.348303873136, 27770.208370801418, 27775.95086775968, 27798.318232668687, 27809.747031516403, 27859.52556768031, 27874.713008756982, 27883.98642247127, 27889.374208668105, 27890.200023301484, 27953.579555030825, 27979.088021992782, 27984.566376000334, 28007.10482384823, 28028.38953923114, 28038.677741471893, 28076.73015109254, 28079.404415549932, 28093.36082808627, 28099.168359147014, 28100.493172483548, 28117.95815476268, 28134.327834625525, 28146.109992923946, 28149.351328595672, 28202.37438715543, 28219.991129513168, 28230.46371297131, 28230.91874175194, 28230.95880255908, 28250.230957049727, 28255.529698441936, 28257.692254159036, 28261.186244650155, 28266.824505872682, 28284.375660115256, 28354.041304496965, 28361.46145520421, 28378.08367668895, 28418.30955237522, 28423.564051180852, 28436.40706454912, 28453.36698398426, 28497.28612777692, 28550.455152820483, 28555.807123075916, 28593.363738789125, 28597.391629320442, 28615.669550874256, 28632.48368685694, 28649.288394790754, 28669.425922938666, 28695.31784579705, 28712.97567332153, 28759.756017812244, 28810.399319676988, 28857.390574637524, 28881.322849278906, 28885.003053609635, 28934.633914247486, 28944.921830604002, 29018.26822214944, 29024.738403287363, 29044.557005910392, 29074.668453282713, 29089.61504701405, 29150.24875753909, 29160.043615102157, 29170.112688493795, 29207.82769593205, 29220.57871730518, 29234.020108316607, 29242.914939510818, 29246.28546725626, 29273.57595815714, 29276.68420661329, 29287.617618640666, 29309.87166319697, 29349.058880881683, 29352.46445279379, 29360.23359425446, 29361.834592891715, 29363.018037045673, 29372.811004615254, 29373.124888374143, 29400.648908840638, 29411.449575040882, 29423.975206037187, 29442.528433984895, 29449.13028527073, 29473.64835772216, 29529.001230174483, 29561.504253333074, 29628.633336482064, 29672.630811410956, 29684.43811588202, 29711.88536271113, 29723.51960046248, 29736.765455783923, 29765.03366849984, 29784.237682818417, 29785.677086065174, 29788.499601228163, 29793.152505538677, 29793.63090000917, 29799.20189617683, 29805.50859817888, 29805.61875880344, 29810.05707169067, 29837.427774368814, 29869.020882373272, 29902.360900219606, 29905.288118315613, 29906.36065931589, 29908.54041096977, 29923.021992101938, 29941.60960755728, 29947.90777704262, 29952.53318522588, 29970.001778331534, 29971.314006814187, 29973.930662407125, 30002.49150644621, 30004.16158574533, 30062.7337569443, 30065.03214926739, 30069.080588465382, 30077.153787167394, 30097.933940901676, 30138.80861952451, 30159.436550891653, 30177.01027046587, 30201.81992405076, 30206.735897927374, 30224.37085540182, 30226.369551587726, 30242.450056838752, 30266.284148955452, 30281.16390504402, 30290.47344636691, 30322.747289490362, 30336.149499186886, 30361.17949413105, 30365.800694699523, 30386.017917801004, 30386.793905968072, 30388.247076469972, 30437.965714467624, 30449.680432768644, 30486.442109019645, 30500.549473403233, 30505.315091526125, 30510.204341874676, 30514.886023875217, 30515.124677245058, 30536.77726235178, 30558.907593216714, 30609.76723492604, 30623.001842893125, 30648.41979049242, 30675.619904833336, 30684.093054825495, 30722.875712983474, 30754.279255010908, 30811.89441198176, 30819.75723478225, 30862.86065630889, 30863.615267307097, 30904.63684497372, 30978.71140175443, 30981.9488780446, 31012.979989146228, 31027.569861089225, 31028.17664320744, 31044.581514740315, 31065.88878647559, 31094.923256226248, 31164.971833726835, 31174.57161994747, 31196.038635603545, 31211.61718665602, 31234.079685529054, 31252.98919327873, 31259.32040778152, 31281.659277199204, 31288.128472472228, 31289.80310853434, 31297.744101397006, 31298.88851358768, 31303.477525103215, 31306.59123775653, 31307.090307489063, 31312.777145874137, 31319.519601493485, 31321.87714774666, 31326.587025859575, 31361.678929578473, 31366.26048046052, 31369.11650375241, 31373.0118332231, 31398.51892545203, 31412.87474428583, 31414.922321677703, 31423.054295627375, 31486.3357652582, 31495.107552252495, 31504.891323027376, 31517.785616673085, 31553.157870279443, 31583.777326449126, 31611.372996789985, 31657.40647617892, 31665.241911317364, 31719.344522906773, 31782.319622221494, 31806.160829822336, 31806.736877139883, 31820.275867277043, 31827.261493006063, 31836.001052566688, 31863.648957677615, 31916.61016105445, 31945.72413973373, 31948.852593101183, 31951.417761923134, 31977.346670074934, 32015.60870188916, 32055.22773599364, 32056.659908150723, 32085.822250417998, 32086.631414131407, 32104.60811280956, 32133.173686113634, 32134.49102172794, 32186.674104748494, 32206.789560183195, 32260.901707632293, 32262.347947899394, 32278.748939101235, 32303.41210027858, 32310.254942907537, 32312.77506479547, 32331.884540624567, 32359.027577143424, 32359.624518734174, 32426.231081118105, 32447.23485223686, 32450.842089348043, 32526.648564664738, 32528.891558936637, 32557.429057756977, 32558.799006260342, 32575.329910298722, 32577.373284581554, 32593.093571615333, 32608.33576204604, 32609.639971989836, 32614.937894832383, 32615.082062054484, 32626.9038563593, 32636.690896584223, 32654.9487840173, 32660.853070102887, 32672.45556736525, 32700.00506196077, 32746.80486438334, 32780.20791464662, 32787.36710406077, 32787.69075721066, 32822.74391769319, 32830.66662689678, 32842.77129926084, 32870.33210966663, 32945.109587587256, 32947.910621236035, 33007.80872023168, 33048.16300924138, 33079.99516257288, 33085.42901945478, 33108.81520582616, 33156.79338099458, 33178.40311199431, 33178.70537826969, 33183.02302289566, 33214.2369014856, 33281.096372234984, 33296.87910308865, 33309.543511840355, 33312.13634675929, 33351.06427727621, 33355.261192611295, 33383.71317656421, 33399.854648746375, 33407.857233580406, 33440.03816778286, 33459.596342941295, 33481.723267494395, 33498.06060003827, 33503.08601904818, 33512.95043744328, 33520.054254788956, 33543.741403312866, 33545.61473143937, 33575.78305575838, 33579.09866738709, 33593.63340658861, 33603.780437341, 33614.02606559302, 33614.74385820538, 33679.468581289955, 33702.12239680467, 33722.43093574946, 33759.588728399765, 33762.635252304535, 33763.11805098373, 33797.260476435134, 33798.170723003066, 33800.277664492285, 33811.99326575165, 33825.87428184914, 33874.065389368516, 33878.3803875849, 33927.04296819238, 33932.84058444335, 33938.351109414914, 33949.474079076, 33955.31382012363, 33970.20526412431, 33977.51411602345, 34042.25693047645, 34066.44080203622, 34077.53350594637, 34099.63661673749, 34100.24564023224, 34111.61049936731, 34130.4071705347, 34136.803511139755, 34139.06987265517, 34158.285173392134, 34172.7391841794, 34182.869507283554, 34203.71038902771, 34212.09719721668, 34230.55199076961, 34234.36028759574, 34241.81821109708, 34290.30208365713, 34319.61056748142, 34383.63543060962, 34394.883464433835, 34398.630273625524, 34458.376083165596, 34469.787492142874, 34487.93209400775, 34489.88544617719, 34528.253245069354, 34563.201052380544, 34578.99580637065, 34602.228568108396, 34676.54278369791, 34709.00052215562, 34813.658191648625, 34841.95265533433, 34843.792481716664, 34850.90733719985, 34851.15205137328, 34851.87909136454, 34855.95070612078, 34888.01639053284, 34912.32762316817, 34914.470689038244, 34921.62046871288, 34934.52257920778, 34940.30386068954, 34974.44234819241, 34992.348908120635, 35001.74394250565, 35005.9238217821, 35022.80137362631, 35023.38924127634, 35033.61878918329, 35033.8382456447, 35044.69085765247, 35050.664154830454, 35050.86065746682, 35089.197075756456, 35112.617135356966, 35119.35735539069, 35159.87676554919, 35167.3137671198, 35174.64199009638, 35185.95163394878, 35224.492763708346, 35229.67225146036, 35239.58389596913, 35286.12172374863, 35294.10670645292, 35302.52907180953, 35308.52308082471, 35311.91012360455, 35325.400626899704, 35380.30173048532, 35391.28794283813, 35416.14324975105, 35419.96667121213, 35428.63875224058, 35428.9369792719, 35449.554732201475, 35461.774983661795, 35466.50974298048, 35470.37148562288, 35481.35810757834, 35491.559772926965, 35501.41216543443, 35508.818198714376, 35518.5689850071, 35527.833256873884, 35535.51583460822, 35556.33298534661, 35559.18914234554, 35635.986964890006, 35647.42806124704, 35699.458293767064, 35758.81401971403, 35788.54971566088, 35803.34996420065, 35807.47118321329, 35880.5966315211, 35902.38679862579, 35910.53251956594, 35920.90251215278, 35921.155122964716, 35925.00423310076, 35925.58830430675, 35975.117797685976, 36020.36170926819, 36021.268367372584, 36065.79555745365, 36067.65642856711, 36155.691796592, 36178.69364856682, 36184.95154655476, 36206.42400293866, 36263.70478883937, 36270.19432256592, 36292.45586517472, 36311.43587949015, 36311.87880317858, 36330.00726920484, 36358.00247263309, 36378.4651091644, 36406.98248681967, 36434.624178958555, 36459.786174421504, 36466.57916358765, 36470.308824172134, 36485.261078674426, 36497.38052180238, 36547.58735781119, 36565.29937575354, 36574.87874353064, 36581.39040057153, 36587.958454789914, 36606.61834533438, 36631.26335335923, 36651.049606565044, 36749.33106942696, 36751.652727414825, 36767.145694502, 36768.12174334231, 36786.26984164528, 36810.632108580365, 36817.575295109855, 36828.066109829844, 36857.94883211703, 36888.33439447836, 36889.66259287183, 36907.2828486095, 36920.49242092584, 36949.927543076745, 36960.043693508225, 36964.06299837844, 36986.845223899945, 37000.21469192882, 37019.83033707887, 37037.62361252723, 37066.41873894342, 37099.82344310329, 37100.57911908372, 37111.598155280255, 37118.855102532165, 37125.71369241443, 37210.74929483366, 37241.74405537759, 37257.40051290854, 37257.73950309158, 37263.189797529994, 37274.04220171117, 37278.287679681365, 37330.26065372587, 37374.86091958291, 37394.65258287083, 37417.975196191444, 37438.95993278133, 37466.614936118334, 37476.28569264195, 37478.897214213604, 37505.22185660376, 37509.50294444803, 37514.35386515572, 37575.324602792345, 37579.66420979006, 37580.291014794304, 37600.30486888238, 37611.34757204339, 37614.36759895783, 37668.23457325099, 37681.27351848854, 37695.50583820954, 37705.13665728572, 37781.80596187097, 37865.18586529171, 37868.217819426856, 37869.28878425414, 37875.27530040191, 37921.45103917847, 37922.932223088894, 37927.880892500274, 37933.05871428793, 37967.62768400943, 38018.368506831364, 38032.9049318314, 38063.74347671546, 38063.78766438364, 38079.47415697651, 38091.89440246495, 38121.92030837817, 38129.869885038854, 38133.385574621374, 38141.96256463095, 38148.23953234761, 38154.721796395796, 38157.817782825645, 38192.39172284011, 38233.049449854116, 38238.06526860343, 38302.94782070667, 38307.540918657476, 38314.946237994394, 38324.91789940724, 38331.2246742162, 38338.53104466718, 38347.636576148136, 38362.77503754395, 38386.34033171615, 38392.40047150984, 38467.16001423845, 38480.12976627681, 38492.876896158916, 38494.33730133975, 38502.64537398833, 38527.38590393507, 38547.00263790764, 38576.15964565595, 38578.48298454511, 38592.50669253708, 38601.22357814868, 38683.76851115064, 38710.13824338871, 38737.12859956713, 38750.50192212598, 38781.88220184158, 38792.43847114415, 38793.1216349922, 38804.66874714373, 38816.04163616587, 38853.7404833304, 38859.14345605385, 38865.51154545434, 38869.64805609993, 38900.859883965255, 38900.941584830325, 38914.95397505351, 38922.95275882205, 38927.223214502694, 38928.74023598948, 38931.1202252505, 38977.85083888688, 39015.14875017534, 39015.415754927715, 39021.74682594622, 39060.190730024085, 39072.82576278184, 39074.30813741454, 39076.28599106037, 39076.85764290495, 39087.04721761698, 39108.1368927623, 39120.075916179434, 39138.99406671493, 39148.26463958182, 39167.21124214708, 39192.84893275809, 39194.92763424445, 39201.56722789304, 39223.44060486044, 39229.42767572393, 39243.0608246451, 39248.102739985334, 39257.6753264787, 39269.34763053061, 39300.103918894165, 39320.58440833281, 39358.76722953421, 39369.85913735158, 39371.42006242993, 39386.72633027582, 39395.29209066883, 39442.53552527168, 39445.88701165187, 39458.450631454485, 39465.53001722501, 39492.809462459416, 39498.218796157365, 39517.68235840572, 39519.45545656416, 39545.115095989546, 39559.859618115996, 39590.717818714475, 39613.0707812686, 39636.61127480898, 39674.044947280854, 39679.146368157715, 39691.062061680124, 39692.31249022456, 39693.050011736814, 39718.543415637534, 39772.987306342475, 39797.04770711221, 39808.79805216554, 39808.987130983245, 39842.97074398485, 39877.94768464463, 39878.85065492561, 39880.423117070066, 39942.65825687002, 39954.81882737856, 40004.66943086746, 40089.05602599574, 40090.65035081284, 40110.96463531381, 40116.48252560219, 40122.92775087712, 40125.81555854562, 40133.09702466449, 40150.95273650404, 40162.60155387993, 40198.34563517962, 40221.64651737352, 40243.41804680009, 40250.16435574517, 40265.24981537116, 40285.018087221695, 40286.1635136685, 40293.025625461916, 40343.08063542284, 40346.10726202546, 40365.18216992428, 40375.18002557929, 40418.17197995789, 40425.17390328091, 40449.942682765366, 40455.76377783359, 40461.09474658575, 40475.24319188599, 40492.92718219846, 40495.31213680529, 40504.48092369747, 40551.801844777954, 40559.66701302108, 40564.31338652613, 40572.05227998373, 40618.291940096766, 40619.998943584265, 40621.80004359259, 40625.738685030905, 40633.3052771143, 40665.77521374437, 40682.654661327644, 40690.66699063453, 40708.76163158958, 40721.664730530676, 40733.876131657256, 40751.23348583417, 40759.623073861476, 40783.90999737888, 40805.91336485751, 40818.100343646474, 40840.15124425234, 40841.10165105228, 40850.253679806956, 40860.620631068705, 40884.09681896749, 40892.05870992416, 40929.501808478046, 40933.343417388314, 40975.37268579607, 41004.64593184531, 41037.77081292796, 41046.57911612098, 41059.92720478092, 41073.727869746515, 41075.87916220141, 41121.18890745564, 41124.063494978254, 41139.22061207291, 41140.915096617544, 41154.46929717275, 41158.69549762146, 41179.697023712855, 41203.8709882134, 41215.592176542414, 41271.994074517126, 41275.21142523551, 41292.011892418566, 41298.3766624348, 41304.29959164916, 41310.773218509494, 41318.749683821836, 41326.95195003363, 41344.72402515413, 41384.25421776647, 41402.97731887509, 41406.03665545182, 41415.712093817645, 41427.9426248229, 41439.90888682769, 41442.54750763636, 41462.873536487285, 41481.411546970245, 41486.00292704691, 41491.811901705914, 41506.13238931587, 41506.17593545167, 41515.591609914, 41523.996253270285, 41555.083750965176, 41562.94751170041, 41660.70286059404, 41666.646704817234, 41692.29741727544, 41721.683366613506, 41744.11437222549, 41754.7986622289, 41759.534160119525, 41804.04035037949, 41845.41330477348, 41860.95839300769, 41869.403800379034, 41903.576602838606, 41908.911704109225, 41935.40755097429, 41939.66530531913, 41943.10410083393, 41945.93320435517, 41951.7536661881, 41959.3680611247, 41993.939006849076, 41999.29658355298, 42004.50412890426, 42007.46092641804, 42027.433907458995, 42036.97182258263, 42042.708168702404, 42087.469383469695, 42087.51748598901, 42093.028877854085, 42145.14648374393, 42163.73558560519, 42170.037775288845, 42173.75220502437, 42190.907302812004, 42217.71110648288, 42232.626424989394, 42263.72064186532, 42281.08857180794, 42288.530969646745, 42289.552738326995, 42292.67958028054, 42294.89366622189, 42295.83582169837, 42300.94555439465, 42311.302982567824, 42333.24360815924, 42336.66144996087, 42369.31045794104, 42373.13366485833, 42407.06673645014, 42425.56735268773, 42486.59917109393, 42487.54203500433, 42501.527305795025, 42532.845390828705, 42537.18841133386, 42540.1638200577, 42546.37166316971, 42615.79522454366, 42635.539561567, 42640.92682200253, 42643.00968019721, 42643.89681393963, 42653.326188414416, 42701.85151757418, 42723.14655843971, 42742.47964812875, 42785.165779146715, 42807.377641223575, 42808.451296377985, 42858.432316589075, 42859.634617965945, 42896.74942208704, 42897.244301212726, 42903.37220350543, 42936.117940884826, 42961.498995355214, 42970.31587952821, 42974.85867433906, 42988.26428539226, 42995.38969276372, 43006.92033538362, 43027.07807998553, 43031.820046731984, 43053.373460984294, 43058.71219422761, 43069.615899309174, 43075.12773056216, 43137.30753058294, 43139.59710270451, 43144.59789267963, 43155.30444993755, 43187.225590699396, 43307.3764397241, 43321.90649294939, 43373.26935961268, 43393.11398286105, 43410.447106498235, 43410.902837547605, 43415.416665739, 43491.22126751686, 43520.7609214099, 43524.68261544825, 43527.72828586506, 43529.818383891674]

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

    X111111_1 = [25054.837050228223, 25058.31039754799, 25066.40314404476, 25086.267120495984, 25088.247899224883, 25091.2273248538, 25103.260008429395, 25108.012235259863, 25110.742339053657, 25124.63808826976, 25124.72209888537, 25141.06669137948, 25146.220937294907, 25149.2431642879, 25181.54490936354, 25209.085135430032, 25209.54853908821, 25222.032738409634, 25244.92186887837, 25251.156675625018, 25254.77010018513, 25257.81195403743, 25276.58898228365, 25288.39532948029, 25309.868375651447, 25335.125073015002, 25349.201913925317, 25351.976613243085, 25369.54304724419, 25382.746781133177, 25456.00717477854, 25519.781174849588, 25536.37306176829, 25537.277622430374, 25555.477003844248, 25599.700686205182, 25604.84510933294, 25623.70556273254, 25627.68437050024, 25671.68915332637, 25696.135868257516, 25696.42214859175, 25697.440108301704, 25705.87936113606, 25708.148078553095, 25713.588133180252, 25715.719483179728, 25721.971303962437, 25729.186355694303, 25755.600613445145, 25758.302687656433, 25787.596254493532, 25788.96490130142, 25826.26790601019, 25827.338288188766, 25829.451721026366, 25856.514276943337, 25856.981651071, 25906.155572811942, 25923.102926374508, 25931.074791243005, 25935.639447162972, 25937.01813804048, 25940.75383326114, 25978.60853275037, 25997.837764127336, 26006.986214769924, 26014.49521134095, 26029.368721044546, 26029.629226923047, 26065.5229818927, 26085.461095120936, 26118.894505252294, 26142.691725173565, 26150.903438383244, 26151.053100609934, 26200.305683643623, 26231.3018954934, 26232.036378813966, 26257.187719901554, 26277.43179628671, 26383.8687754051, 26384.901438654568, 26399.54133806725, 26461.10510605014, 26463.696102755905, 26472.343613593406, 26489.49318736889, 26518.436790561092, 26526.588839482087, 26537.04540475856, 26537.24366569235, 26541.22771935122, 26546.05161752796, 26586.002331223794, 26607.42769354249, 26623.167358714356, 26687.438844718912, 26723.27474018615, 26731.091598544223, 26731.50429902759, 26734.20918890346, 26764.166977151497, 26772.936437450502, 26842.49913603557, 26870.274616433137, 26875.754479926494, 26877.685674719018, 26879.344708458473, 26888.254329790954, 26924.303709039425, 26927.715347008332, 26963.58911558318, 27009.45736946542, 27025.587192786603, 27046.532312143445, 27057.477310587663, 27091.971793667213, 27092.49058400348, 27092.625301488286, 27160.43110859192, 27162.669131946055, 27170.474034385934, 27230.68108778874, 27249.383547318383, 27256.68609533161, 27266.90461833288, 27307.03748288265, 27309.089417532596, 27309.626942506315, 27322.502207046815, 27325.35959823338, 27327.60519458419, 27342.019694822116, 27362.486613733417, 27364.142980515182, 27378.97032087627, 27383.96002101079, 27390.82253510431, 27401.04467857747, 27417.049319361744, 27451.13628310755, 27462.29400268, 27506.745876745663, 27522.244063915296, 27524.662165329486, 27545.599913242277, 27580.165869442044, 27584.955407415946, 27604.947540890826, 27617.61737715145, 27622.50795728301, 27650.334642977108, 27655.398401356175, 27713.72602576174, 27734.465942100287, 27769.88631196701, 27782.8987005852, 27788.026266007397, 27801.551804230457, 27807.813361180397, 27838.06776315678, 27841.040777986407, 27902.717138725202, 27904.873956979216, 27913.69321766628, 27944.633533854423, 27961.690763971805, 27968.100348695934, 27968.823226555123, 28046.41976675634, 28066.772826822376, 28075.62579412443, 28106.984114529787, 28157.6713511866, 28181.009242758395, 28187.942236332525, 28210.874901564675, 28216.84220794481, 28270.74802446574, 28289.442465396423, 28310.6862636986, 28332.822636883306, 28386.862646526475, 28389.956319286946, 28398.12140315789, 28403.457961563854, 28427.57374760534, 28459.80548791577, 28507.72280671191, 28559.55187220891, 28573.000808853383, 28588.40026417691, 28599.555162356715, 28604.838787596367, 28616.198272536865, 28618.63600562594, 28631.180851544916, 28631.865763686168, 28640.411427683845, 28648.455032779013, 28714.0080814579, 28715.70605250793, 28741.383358287545, 28761.994551918142, 28766.33659466923, 28829.15757866981, 28848.864755489125, 28854.781982456607, 28872.474210985412, 28875.569588754624, 28900.215872298522, 28911.75525783801, 28916.335153952212, 28924.51537462735, 28948.379081408755, 28953.902628554322, 28956.291062002998, 28969.566681338434, 28975.30319736195, 28980.991355431783, 29004.0335137483, 29004.844605587452, 29020.63485270395, 29029.380624224945, 29038.079204381986, 29042.22984346239, 29068.44719367774, 29070.296499498312, 29106.822973108, 29115.395521323655, 29120.184015733514, 29149.917400970422, 29181.352157271907, 29207.05486867746, 29217.895842355123, 29247.753427279436, 29278.819395539293, 29287.601818063253, 29307.915646284477, 29335.210390609467, 29348.332607563036, 29383.838177669884, 29386.040215033565, 29407.58450862988, 29453.369059987876, 29462.568410855718, 29473.617531566888, 29476.942715349207, 29513.08987869638, 29527.203316356736, 29564.485572303776, 29567.906165407578, 29588.482397640502, 29591.83057758464, 29625.40934724619, 29628.967301455756, 29645.955982059822, 29653.758694575932, 29654.704475105245, 29688.09128268009, 29690.950282741916, 29739.282192770737, 29746.752582265253, 29751.282077181393, 29762.5648786185, 29816.077973471656, 29845.423100297703, 29885.688145331565, 29904.946277684394, 29906.087662512076, 29914.617965820624, 29933.703638370345, 29952.708916108662, 29953.74432153875, 29959.15773538716, 29965.099424590142, 29973.844178251307, 29974.26293469174, 30026.113808720755, 30046.910067876757, 30107.993109600655, 30120.274129873982, 30133.12891421735, 30227.896642359465, 30236.684378762533, 30282.17560860636, 30301.056614296893, 30328.030322858485, 30333.080026069754, 30345.91132880098, 30363.390097668456, 30369.493995083976, 30370.570489775077, 30390.17015463863, 30392.524179757635, 30400.83008338626, 30448.91428285739, 30469.199974418487, 30497.634408459486, 30531.330868202607, 30536.680401119196, 30589.618585096767, 30712.36655029788, 30720.18154495519, 30720.949557121494, 30738.897921998017, 30748.43616833352, 30768.753160954435, 30795.45351420615, 30803.24865938938, 30804.230706571558, 30813.514259383817, 30816.85320768082, 30822.819112569014, 30877.59785021351, 30883.257451962098, 30888.195921099195, 30933.78302742741, 30963.991454789164, 30988.63244608487, 31103.230318027112, 31126.231698647876, 31137.509804941787, 31145.190261905445, 31153.945851283966, 31159.658251110963, 31217.588931002916, 31315.646726458104, 31354.86383129543, 31361.056194011966, 31366.32541335098, 31391.93350288364, 31422.929175285182, 31432.12117217549, 31432.51512518439, 31444.10780157181, 31455.922069114327, 31472.918287422184, 31501.535166572667, 31537.745483659448, 31548.89160457192, 31559.692445623594, 31565.01540964508, 31597.000502157243, 31607.835416073256, 31636.037827602693, 31657.354999187286, 31658.55757630671, 31664.384537019134, 31699.668596345833, 31704.38723048878, 31724.026988930193, 31745.299828653046, 31775.482902058106, 31786.647297038086, 31831.152664430087, 31835.376380424223, 31852.918250471113, 31865.433359061877, 31889.44701391609, 31892.48397922767, 31911.73204523313, 31911.867138302547, 31954.446863734738, 32000.83691894951, 32016.78039736361, 32065.0382580686, 32098.51392555773, 32188.77183218798, 32190.4248999869, 32218.063524870493, 32225.440771370784, 32229.808903345933, 32231.563804890866, 32241.784265150043, 32249.920913752627, 32312.172418845414, 32321.404905782398, 32376.016410817323, 32376.895100833142, 32382.54758234512, 32384.55315082908, 32390.35861289774, 32395.576417854394, 32424.051616479897, 32434.49691237114, 32445.995623739058, 32447.657221787966, 32464.875407210508, 32476.522518540933, 32500.425346728345, 32512.155115524565, 32544.568996978123, 32554.379557948134, 32568.167745203296, 32585.83525632665, 32590.147815510856, 32605.36777423716, 32609.98836757047, 32615.60847672764, 32656.07821909515, 32664.126926714423, 32702.757112616993, 32738.60027662201, 32815.61336213332, 32819.17450239307, 32883.917659760125, 32888.443889790215, 32888.601188052024, 32895.19729670286, 32950.85996607861, 32967.5255206345, 32980.408136390295, 32985.63213537964, 33006.396810666905, 33010.318101897785, 33075.00650871799, 33097.59209786312, 33107.30767660146, 33138.93845497409, 33155.696642256225, 33157.73061489886, 33170.22776299383, 33173.71481293556, 33179.66739736167, 33194.12984330832, 33197.1390158695, 33198.1440492396, 33219.93285753234, 33229.03502825745, 33287.89371736744, 33309.62000980654, 33408.64246858567, 33410.788771186446, 33428.95622291327, 33434.076179058226, 33443.03635843462, 33447.9935642848, 33456.9830786096, 33467.089243586466, 33484.04590012852, 33505.34595557843, 33560.61761018456, 33568.958135337925, 33582.62929405094, 33600.94540260129, 33672.99827259112, 33702.27631982815, 33713.350336676616, 33716.26386530943, 33718.56332144784, 33763.36462876627, 33763.98605526632, 33766.75253297201, 33789.92349453131, 33843.16890611886, 33843.760766477964, 33877.63087386232, 33936.58965927173, 33937.88785282591, 33964.672288216374, 33988.20619104782, 33995.047907035405, 33997.149298190234, 34084.97622729361, 34095.15202112849, 34170.94265720992, 34171.36593496659, 34211.24851297546, 34215.660157034814, 34230.018484403496, 34230.79744532763, 34231.708030851754, 34234.35952099871, 34247.23584688023, 34275.67002818036, 34283.87538117364, 34287.876736834725, 34309.14382614894, 34344.208632256705, 34367.851517416195, 34369.98399737537, 34370.985088131434, 34379.02649081604, 34411.98044319586, 34422.00409767952, 34493.18693298467, 34495.592980715235, 34511.54824265147, 34514.8122837477, 34514.9943380559, 34520.908683426715, 34578.02702696264, 34613.49799566521, 34614.6437176684, 34624.13401420822, 34626.133333304955, 34656.72009775384, 34663.175911670594, 34686.313105747635, 34691.92579066032, 34703.28405086669, 34740.596958251954, 34749.89691107361, 34760.588640549315, 34781.61672113594, 34801.21549288949, 34835.927240700585, 34842.71723293813, 34876.886825280235, 34893.09178273492, 34900.48995193804, 34908.408139404855, 34927.46891139122, 34932.37774190865, 34937.47799770591, 34950.02641790755, 34966.61641717794, 35002.504068928596, 35005.04069798402, 35034.842981191796, 35038.83486443643, 35050.31908031553, 35057.90461208376, 35064.65564118808, 35074.99338494028, 35101.303241280744, 35116.40886766839, 35159.87371733856, 35191.61107584158, 35232.09238608185, 35265.11021520762, 35267.21980385276, 35272.39363037738, 35273.80146253491, 35346.74855250642, 35373.0514745906, 35405.33061359642, 35424.65314562359, 35424.684164640064, 35474.74556084972, 35480.502272970494, 35497.90069109662, 35510.579598081895, 35551.85931493271, 35559.608952937146, 35589.55108335333, 35633.43810979326, 35647.078531822466, 35656.77567662763, 35690.31412778729, 35736.52288872489, 35737.79743470745, 35751.86838035826, 35768.19778327433, 35770.80567794244, 35783.500157997085, 35798.9076963871, 35876.68565183034, 35905.58586175318, 35930.431292511894, 35931.081926372426, 35938.132573113624, 35956.69706018048, 35964.72561414451, 35987.27764356954, 35997.948024837, 36026.7585178477, 36035.98379599585, 36040.86894985917, 36119.06927724353, 36122.534154998066, 36124.5632445353, 36150.52611957054, 36166.758975007564, 36179.68230087042, 36190.611327536506, 36195.58717131539, 36211.958179173416, 36244.878855765426, 36255.29856344459, 36257.94727529342, 36262.03958692395, 36268.981202687224, 36274.21499601722, 36290.17275172575, 36338.1778061775, 36338.98074701197, 36353.546301059156, 36371.05840427901, 36383.51524495313, 36388.74678667714, 36395.74834282768, 36472.46752412965, 36479.75933985635, 36520.00182829811, 36565.77575490427, 36629.58916364101, 36680.14462602649, 36689.11750600267, 36701.07911030004, 36710.85348953141, 36717.93754016682, 36718.1532091486, 36720.00647853031, 36789.934150835965, 36794.17105831759, 36834.71119204924, 36843.73280726596, 36844.457294749736, 36847.08164310406, 36853.84862635676, 36856.51924401071, 36865.70115220165, 36892.06054671365, 36895.29776547548, 36930.77272289831, 36985.84624025613, 36993.92997449149, 37001.712560943175, 37038.16089916684, 37045.8851453447, 37064.21092802592, 37065.15166448342, 37105.47406930226, 37135.20813061121, 37143.48427568306, 37162.81010021697, 37167.611012121895, 37174.28803215468, 37179.98510358772, 37182.72453397419, 37191.904194339266, 37206.83802468116, 37212.30350068143, 37230.18921373023, 37376.11722933003, 37378.86756834761, 37396.31279256308, 37407.624506341235, 37422.53048850874, 37431.704296327705, 37435.89212969784, 37446.68099188027, 37462.19218337821, 37493.59160996029, 37499.59701010037, 37507.60753993408, 37554.57839038472, 37593.02495488273, 37605.19496622843, 37606.0424443695, 37607.39226507285, 37640.98278807192, 37651.34217997534, 37667.13828371745, 37678.59989159444, 37699.87927098504, 37715.38629800507, 37733.55377742073, 37749.34908404091, 37752.033700234504, 37798.85909254679, 37799.83916095608, 37826.75667072874, 37844.33317493256, 37859.0538904172, 37867.37829607804, 37872.948856001836, 37905.761211954305, 37940.821686365234, 37955.66301550926, 37969.14147678917, 37969.973650968, 37978.698962505114, 37986.082458067736, 37991.751860954326, 38000.52822318961, 38018.029285928955, 38053.05103888103, 38053.60761023448, 38064.91177942345, 38067.029011688835, 38075.36696960764, 38106.21268604648, 38110.75429034984, 38161.42646038326, 38199.292349032025, 38243.59808994492, 38256.1494807171, 38258.87577684065, 38270.92041171223, 38277.82054529771, 38289.34625268139, 38299.28317190127, 38312.75819481888, 38313.559731948975, 38313.579888642125, 38316.794229809915, 38317.04725150541, 38336.38833079073, 38351.94410351978, 38368.74204993511, 38382.272232793985, 38387.68964179392, 38436.55856664051, 38443.4462662898, 38443.63718331305, 38444.70254568495, 38449.982403121205, 38494.30632957017, 38494.958005405075, 38515.64275778006, 38523.19547341884, 38524.301380510115, 38534.20734716194, 38541.4183547549, 38548.774923022516, 38555.161213409665, 38568.77588660116, 38591.3560686172, 38598.04619784231, 38601.23634916216, 38648.27486681542, 38692.62235270956, 38711.32527462871, 38743.48318085388, 38749.58164502755, 38760.31556510249, 38773.46325312971, 38785.565206672545, 38792.47200143867, 38800.32272584266, 38808.30882298069, 38825.87851062097, 38866.67796006349, 38883.98615785815, 38889.03918234243, 38890.529925808754, 38907.71555155623, 38954.809859564644, 38967.8258263516, 38970.27248993241, 38981.16240753289, 39017.84181226514, 39028.44466272684, 39031.79491219645, 39071.163173654415, 39080.82650014812, 39084.57251017262, 39090.18661878888, 39098.78785758071, 39112.1882459996, 39115.839579030944, 39118.64302564901, 39127.77535561243, 39240.744230802964, 39266.28564027675, 39309.78283510836, 39365.04240457597, 39397.868258709874, 39434.452369709325, 39477.78897827344, 39488.54804378415, 39492.043561792016, 39500.10416928276, 39507.33106304073, 39523.9239993833, 39533.53296141407, 39541.61343558632, 39558.82409140187, 39581.55399159313, 39581.9099976981, 39610.55629630032, 39627.104619802965, 39647.267280307264, 39689.66038560362, 39689.71014297852, 39754.250265560666, 39760.42705962896, 39767.36003034314, 39775.5409986154, 39806.96962097851, 39814.62579808372, 39844.771280622954, 39869.320897181766, 39920.83470848075, 39928.64963674029, 39946.21092530303, 39951.16296611993, 39991.90213806339, 40003.28528251893, 40030.9830070255, 40037.60239465443, 40064.531714981036, 40091.99913258676, 40099.05777378475, 40101.36915827101, 40103.076164071994, 40107.3693783984, 40132.61509812092, 40149.18691387611, 40151.678590975076, 40186.10546528754, 40191.73314350132, 40216.35071009815, 40241.037855833776, 40248.31892035882, 40263.64394464258, 40264.71181077394, 40278.19693991763, 40299.717841962265, 40313.414893675275, 40318.73695001245, 40320.092612090426, 40355.318395344846, 40362.07483969924, 40438.22303948322, 40448.938983691245, 40463.24818861043, 40465.23221048326, 40473.98618887686, 40497.9654861038, 40510.91900420971, 40526.470011546306, 40528.578082682325, 40532.87360992509, 40538.95495440277, 40543.85789111527, 40557.56531330406, 40564.11440046334, 40567.306900620366, 40567.94774167698, 40601.094681239454, 40615.94696787231, 40618.233544771625, 40653.05815379607, 40753.09801553121, 40761.91797765334, 40773.1135614261, 40792.650831304476, 40798.948547295615, 40801.795323901286, 40807.05930932017, 40821.64540446066, 40830.9886487627, 40842.49657206003, 40845.03258262437, 40871.25045755537, 40926.59259604566, 40927.51616114061, 40930.55789946981, 40931.05467348345, 40934.04713061264, 40946.36229341336, 40948.48245026453, 40954.61451716556, 40976.637003196374, 40978.84425433485, 40983.42335393275, 41022.891871771935, 41043.377697816904, 41053.759640747725, 41072.06532870044, 41097.16935144464, 41169.474198278316, 41170.55583477054, 41175.41324883218, 41175.581038043325, 41213.07006902835, 41221.713728884824, 41227.963276504954, 41229.48038224386, 41287.85802571081, 41316.94975927251, 41338.86040251308, 41384.14920548262, 41398.31978785936, 41405.06487519302, 41407.27087695485, 41425.75609411967, 41434.39478031933, 41435.42422526881, 41435.699024111804, 41436.9409862319, 41443.061626897055, 41458.85075698055, 41536.41500320565, 41581.47612838195, 41593.72991341635, 41639.190878891764, 41666.34915050042, 41667.24530707697, 41692.66946352395, 41716.13819684378, 41723.69452312318, 41727.678608120186, 41745.882313191505, 41758.87471101803, 41759.304185236586, 41762.53497698343, 41762.791961618466, 41808.30061766083, 41819.05989691584, 41834.00081392791, 41849.06659906273, 41853.451179099575, 41887.13902706531, 41903.077539545615, 41919.17379348933, 41938.80460973525, 41956.10883553188, 41964.76160962113, 41970.14723656196, 41971.97973850171, 41993.06995576473, 42004.346645954334, 42034.135116280726, 42069.767131180866, 42074.04409791352, 42096.096475927465, 42103.05344529921, 42117.31796033204, 42129.972909270786, 42166.85677911514, 42168.71473106077, 42172.42940520315, 42192.2989922349, 42194.87388754301, 42195.65362914337, 42198.358086959364, 42213.76739779653, 42238.23086797538, 42256.38228141638, 42268.35732430602, 42280.860570688004, 42287.84326538441, 42302.039923890814, 42327.25454687016, 42328.31583196467, 42338.572814782674, 42353.6190558587, 42408.9405781931, 42414.85035690838, 42425.63277114199, 42444.36342363678, 42444.966479860566, 42469.341534768595, 42475.978855194524, 42483.58007134934, 42488.59343613626, 42488.92068877812, 42500.01031053542, 42511.857738556966, 42569.504300959714, 42633.43771410079, 42688.65254074264, 42698.33221321281, 42707.97952323008, 42779.86258608423, 42792.67940654799, 42814.815866799814, 42824.97416285271, 42854.95885541365, 42874.62294837531, 42890.715462971326, 42896.10903219563, 42897.81271397059, 42906.5605848133, 42940.67500604653, 42946.392640687445, 42998.69363854095, 43011.72046341882, 43019.232824599785, 43038.541370794715, 43062.29569706571, 43082.57860167487, 43082.91906800216, 43090.99093266111, 43116.95803786539, 43126.2794209322, 43126.918556215765, 43135.67812993625, 43145.873573027144, 43176.91727818399, 43183.10337320427, 43232.036664194806, 43233.13449330909, 43273.98901419143, 43286.50960075471, 43317.07110142971, 43325.979273479184, 43366.19821355928, 43397.05768016302, 43461.80025441213, 43463.80439771536, 43483.605477012345, 43504.45905079156, 43527.450258228026]

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

    for i in range(50):
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

