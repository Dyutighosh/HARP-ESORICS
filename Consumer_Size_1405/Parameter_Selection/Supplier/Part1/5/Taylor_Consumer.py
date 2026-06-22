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

    min_val_1 = 210.0     #min(X1)
    max_val_1 = 966.9879817143079      #max(X1)


    X111111_1 = [210.0149339424895, 210.86138548088442, 211.632369265792, 211.82656660590968, 212.10545347078806, 212.7810447016314, 214.26494049778347, 215.4915241164557, 215.61639250062007, 216.15117684828448, 216.15670758217934, 216.5012529088368, 216.79575905021807, 217.95453103216985, 218.33287425229457, 218.70823819266758, 220.18832706661414, 220.7800225409855, 221.50692919552904, 221.76179732182754, 221.81282438277688, 221.83867541788666, 221.97134975290646, 223.37890012509556, 223.7072488118657, 224.1493653011236, 226.13121130469625, 227.27852823705402, 227.51075680986185, 228.4500129076322, 228.70891348499669, 229.54111084196796, 229.8931789677581, 230.05973910141617, 230.3237547975056, 230.37790117849525, 230.65269295536086, 231.76946546123114, 232.17884886195597, 233.06041399651735, 233.12986618031545, 233.8377983263616, 235.11142696318515, 237.03856169644723, 237.22292344455525, 237.22638219188113, 237.48212825507764, 237.6021518933485, 239.6079284324481, 240.21379828174685, 240.4488088394985, 240.60263786399616, 240.7654315047821, 240.99592256867123, 241.45878892339894, 242.38209095977706, 242.6194408809755, 243.59240172101968, 244.3077247472483, 244.32895941120572, 244.43520721965308, 244.73863672820406, 245.13196392598354, 245.43884746167961, 245.99475777857558, 246.32735856063394, 246.35602494875585, 247.50754951960914, 248.4781578466509, 250.39264799911007, 252.7414243210712, 253.1038958041708, 254.7657769310607, 255.00322130983722, 258.5113184727094, 258.55061042979764, 259.74905911230013, 260.18087158810613, 260.28388091324865, 260.6850495365802, 261.7536372262572, 262.43904316380474, 264.0706041322726, 264.33300963613874, 265.09224067879273, 265.3082602079835, 266.2676030876923, 267.4112863885964, 268.4081466094292, 268.6010565954691, 268.7457480601659, 269.56497989784737, 270.35051633516053, 270.5251686127459, 271.34172686495424, 271.78600113841514, 272.59457752557853, 272.64016264394553, 272.69606848143167, 272.7668471385215, 273.4833895351831, 273.7142878575045, 273.7835874299701, 274.6374476838936, 274.72158823075756, 276.8871547078834, 277.36227598718415, 277.37755617675083, 277.9881450750519, 278.2348435770212, 279.5365640921511, 281.595632644542, 282.6925665309492, 282.8703433261842, 285.5749369101327, 287.2709620847144, 289.26892830074814, 289.52164738182745, 290.2631242679146, 291.175963019643, 291.8883644409637, 292.45246087752264, 293.9067123985726, 294.4166800332473, 294.85762155579357, 296.27623122912587, 297.0508693168739, 297.2977668804949, 298.29483114671, 299.93124620369207, 301.19624393670176, 301.94983413127466, 302.24359850664354, 302.7921772528176, 303.4231929252577, 303.5096703251753, 303.54868089953345, 303.89494609735976, 305.0123864037657, 305.5377599424695, 307.6947480538583, 308.0286368490297, 309.52189347744263, 310.7123653454595, 311.75153414638896, 312.77216383416663, 314.8991538428819, 315.184831332976, 315.9484277090188, 317.6320956207052, 318.44753236476447, 319.42844472713256, 319.58543369905306, 320.1360388281638, 321.9418267208507, 323.3564485991295, 324.4304021186781, 324.7825261693498, 325.104791123222, 327.3435646986426, 328.0705829202701, 328.1278659153144, 329.3913573900985, 330.113647710877, 331.0212538715568, 331.7385438376357, 332.54535267632554, 337.17927840599293, 337.9913831041705, 338.71444402915205, 338.942293534868, 339.1926192759954, 343.75388559218527, 346.89030710547894, 347.40391543743885, 348.4609212797662, 351.3115034644985, 351.7091185686746, 352.02773827518854, 352.2119887005324, 352.950836034693, 353.2287554750159, 353.897407643634, 354.6211042203396, 356.07701532394594, 356.39895227364383, 356.5794035622524, 356.701072105771, 357.7014277793146, 358.07318816103884, 358.17684812801076, 359.4957532844124, 359.5909862789823, 360.6705834411983, 362.7020039155352, 363.13033850212616, 363.4574345283944, 364.17354972557456, 364.8793756182764, 367.25035937569885, 367.41008798680815, 369.137345440754, 369.66331182091255, 369.7858142337209, 371.2155975688315, 371.27792553753625, 372.42922521901176, 373.0936223141075, 373.09928338333987, 373.33426468532537, 373.86601801644684, 374.21959073438734, 375.69572841768877, 375.8777670781715, 376.33845774468864, 376.38476740700946, 376.3982278230336, 376.63508321681684, 378.3540516891329, 378.5539267236971, 380.21582951422283, 380.24772499972534, 382.27459279886887, 382.8557823239172, 382.92158278132615, 384.0129751960768, 385.09551802950887, 385.579604710621, 385.997787250472, 385.99890406621785, 388.46718806445926, 388.88458292385235, 389.2237619543949, 390.2823398456744, 390.62304360799374, 392.2230725388891, 393.49249128394524, 393.5162835537326, 394.35266533568057, 394.86352521750996, 396.15582944102414, 397.09563366436646, 398.03736124776276, 398.29576202204487, 398.622218711339, 399.2450112850401, 400.4241450893437, 401.02264992133513, 401.2226693882664, 401.8855355720642, 403.37063894342987, 404.08798885621434, 406.0021993814894, 406.8187703301262, 408.1777100290403, 410.4643652057308, 410.8211976802927, 411.19400743534936, 411.6345228923551, 416.1131889393677, 416.48223252953244, 416.640196599005, 417.3448951785459, 417.8074492226243, 418.1116991507391, 418.2732995595996, 418.4105146011102, 419.25973392992677, 419.43453083911453, 420.66241214348054, 421.64389414373363, 422.2851298040193, 422.8959080483604, 423.0478046454733, 423.15894737753797, 424.00774193954646, 424.0215613960235, 424.3942881822379, 426.05729602342865, 427.8145352270947, 429.3988694416083, 430.35223187450913, 430.64179735318237, 433.8045907031791, 434.7171231686721, 434.7806237948278, 434.783113743871, 435.2178196952516, 436.33896520628986, 436.50197907942646, 437.0270123621907, 437.19202279477497, 438.13818005289215, 438.8668204886543, 441.39468441798215, 442.06669848707355, 442.1459453767262, 442.53573953823576, 442.6644477821926, 444.1235115766044, 444.47474145349855, 445.0753912686462, 445.3401694170416, 446.40371597478105, 446.63030187334664, 448.0033539501944, 448.7130662058163, 449.38160238513825, 449.41124747490187, 449.54781422879114, 450.08218440075024, 450.4898174337346, 450.9409681385306, 451.13636886076927, 451.32130899002163, 452.3192824343742, 452.84008874499807, 453.3590643306924, 453.85566282932155, 454.96872387012024, 458.75851518827324, 459.844529617848, 460.60083564945006, 460.7389928083286, 460.93421572402724, 460.99879517871193, 461.18563679174633, 461.3437390230357, 461.8017016497564, 461.91039225104333, 462.7172609009177, 463.1987090415506, 463.8578277625971, 465.52041662298114, 465.63960290776623, 466.3311656767333, 467.57061328018, 467.9841139299687, 469.3458303965428, 469.6382025698858, 471.3071936251463, 473.0174972609299, 473.9401110137438, 475.49597823908715, 475.8592195924317, 476.8808363251371, 477.22024861260087, 477.5396508857514, 479.24956901776136, 479.49841326503423, 479.5804689648925, 479.72857641955756, 480.6643901643961, 480.8358216593733, 481.1802873781925, 481.90804677687424, 481.94213458610477, 482.0322873624754, 483.02052264543846, 483.255767971293, 483.2795356524658, 483.606398553773, 484.45709206384004, 484.8565705147277, 485.67951020387403, 487.37771636852915, 488.1148054409511, 488.3175750534972, 489.2396110886853, 489.8457041543395, 489.8816578527345, 490.9536501482666, 491.1498719333909, 491.4929120176722, 491.50291121280395, 492.1757198007651, 493.79866467699446, 495.01882572529723, 495.127951544222, 498.2139274442601, 498.78120410712444, 499.04561194591366, 499.0542436919679, 499.8202426658033, 501.881256937863, 503.29356182222756, 503.9040592543495, 505.01445954210476, 505.33065556121727, 505.6395627000342, 505.90074575315396, 506.18669876086875, 506.9461890370514, 507.0851340400972, 507.39830537395625, 507.4484505368431, 507.8281732965424, 509.1100072919437, 510.76804750467227, 511.2847033675969, 511.75167349559246, 513.4160390436384, 514.0837883145538, 514.8504245385503, 516.3019009876353, 516.3506795656167, 516.406693782875, 518.402499309266, 518.4743669536258, 518.8670890474659, 521.1557174142995, 523.116403096783, 525.0680222992665, 525.2857402290025, 525.9809682923892, 526.1330019442833, 526.6233182070005, 527.1879674635927, 527.6613511992572, 528.0262163293809, 528.0873425052976, 528.6444275276267, 528.7415831582422, 528.7831609170387, 529.1112910350706, 530.4259634831108, 531.4685030409048, 531.7134797273545, 531.7931979211553, 533.4870002072573, 534.1963837385491, 534.4954735325559, 535.0501977390539, 535.3752734629826, 535.5932294476795, 535.7955627505473, 536.6378523876751, 536.849315059899, 537.1512436069596, 537.2127102835245, 537.7830222422751, 538.1595378198895, 538.5259129509494, 539.9629169977202, 541.0613282319225, 541.8723175184587, 543.2150131157, 543.9672359872844, 544.483016687816, 544.7871919793342, 545.4905719355022, 545.8248722590013, 546.4862781947825, 548.5471265668734, 548.5686079813597, 548.9629535984161, 549.191844328308, 550.0648817794859, 550.1653110963119, 550.3859256730025, 550.7550216911662, 551.8975556070668, 552.1246395364451, 552.4593871967535, 552.8339619130281, 553.1298474012187, 554.1200220104836, 556.4955967928523, 557.668860023058, 558.6508803787663, 558.7365586213616, 558.9795096089771, 559.51063984246, 559.6086673734679, 559.7614060475128, 559.7632984644545, 560.4322614573268, 563.4457762680065, 564.0146040030986, 565.194320048555, 565.7217767645235, 565.8649182774113, 566.1376246760709, 566.4019915559468, 566.7095149860761, 567.4567532807905, 567.6214999481665, 567.6507173557093, 568.2963450965058, 568.296818207138, 568.3015381827879, 568.5674814069886, 569.5576456918932, 569.8100704855409, 573.2741795438413, 573.4890102377556, 574.0876929173191, 575.5197288417833, 575.795097806176, 576.3480521007118, 577.8990020751505, 579.7041585140482, 581.2481618500294, 581.3837521760261, 581.9510735521201, 582.6821418153781, 584.2537019003355, 585.5648035603077, 586.9219484813561, 588.982407154695, 589.0490293758297, 589.304553235838, 590.0551021926506, 591.9220951571742, 592.0174234103754, 593.942461722675, 594.9222987423601, 595.8297151623574, 598.0625429489646, 600.8745260352161, 601.2711911490665, 601.3029043662073, 601.7694437663579, 603.1137043658507, 603.7870019910386, 603.9210331879974, 604.2637348073079, 605.6231909934284, 605.8192696649395, 605.9914704572504, 606.0761662887187, 606.9280458500277, 607.7312727749106, 607.8855404613178, 608.3283889744823, 608.3683673361004, 611.7964071677595, 611.8318344773637, 612.3933166101367, 612.7259383135986, 613.2832244669036, 613.6668776624624, 613.8741755880245, 615.8090695488582, 616.0317772767203, 616.0448684753009, 616.6749089019364, 616.6958876695792, 617.3971715098721, 618.0175351305692, 619.7131859163369, 619.9498696619388, 620.2448631714943, 620.6543306525219, 623.2331823351668, 623.6311740294632, 624.9264276360535, 626.0411914394004, 627.205133506876, 627.2974718303415, 627.355471176212, 628.0010111285816, 628.2296088216428, 629.6133193381245, 629.8580846986517, 630.7708245926385, 631.493505481059, 632.6615781284158, 633.3236536628024, 633.5083641519393, 634.6342119184737, 634.8091961807961, 635.7880228584099, 636.4480352180983, 637.7484532062106, 641.2450868454287, 642.4013197134353, 643.0905547349932, 645.6708370507195, 645.9570782638365, 647.0655414702373, 647.7531630341432, 649.3573069133611, 650.4072903165586, 650.6036375998733, 650.7925480720617, 650.7940560231734, 654.0144082070422, 654.0355026691502, 654.9408739315058, 655.0001343403206, 655.4625575712005, 657.8485174632829, 660.0365049413856, 660.200688129004, 660.5447967115264, 660.5769735292092, 660.6590592977702, 661.1499931181281, 661.4986163805663, 661.6129536394417, 664.0274071812607, 664.4374729174137, 665.3339750208654, 666.6406904593355, 666.6579432947831, 666.8296123527095, 668.2760369008067, 668.6580909518264, 669.3719826714996, 669.5879627568244, 670.1379586649093, 670.2700753012605, 670.6915055321745, 671.1320735288689, 671.3347114829335, 671.3387083623007, 671.5153445287099, 671.7694393457456, 672.342720318343, 673.3327405519346, 674.3230661902123, 675.8529264677795, 676.0946568704856, 676.1765312056879, 676.6556341305405, 676.8049143327138, 678.1599056707983, 678.3340038270399, 678.6140923145103, 679.824383500518, 682.5170665427319, 682.6581813434489, 683.1789574635629, 683.4447336752437, 683.9326774584354, 684.2735784239221, 684.7681553725375, 684.9147208250276, 687.6470311681198, 687.6824400250046, 688.3357671174839, 688.9067324350644, 689.4679614839637, 689.9174532154159, 692.3479905315058, 695.0121995400476, 695.2095821211028, 695.8115934665434, 696.0183357018974, 698.0809681150974, 698.09731916634, 698.3490676298466, 698.7950476746817, 702.523291173078, 702.6772851518851, 702.8728646208627, 703.5371331217775, 704.9983687406558, 705.2522527916333, 705.2804182836313, 705.4089727961982, 706.1244254304842, 707.3862414690705, 708.0056486983606, 708.2870069782688, 708.4414102325059, 709.099146396098, 709.669131252853, 710.0274576699967, 710.0387245799807, 711.332462392762, 711.6766205653907, 713.4841226316207, 715.1605983060033, 715.7379924918611, 715.8332893540966, 715.9123125289457, 716.5733428321937, 716.7592213026609, 717.0759087704613, 718.0481908191493, 718.5799705947377, 720.2091051916611, 721.4370339861119, 721.8239710105302, 722.0485114421638, 722.1650162249103, 722.617485551463, 723.104931894909, 724.6261892249809, 725.3614377209689, 726.9695475327121, 727.6683646609075, 727.8871296590896, 728.1856163830676, 730.7292391465027, 732.5186261122674, 732.7823662454259, 732.8073096368116, 735.8515235456201, 736.1609369732765, 736.236425604807, 737.2965490095726, 738.814190695552, 739.2184610834075, 739.2729296954184, 739.5075711665053, 739.7506598918767, 740.6537953405408, 742.4296951330759, 742.8238040304251, 743.5536602475105, 744.1439684782526, 745.4411253946374, 745.4621477982444, 746.3931179160851, 746.8957697565577, 747.1002142735126, 748.7910376119976, 752.3193015263761, 752.4676487879849, 753.729836510078, 755.0674128180781, 756.2151082710682, 757.1534246955935, 757.3127623302103, 758.8043364761672, 759.4361298588268, 759.5319709687492, 760.2429283086675, 760.7526807511363, 761.2134599346609, 761.4466498991374, 762.0131996644822, 762.2093520448178, 762.6853230763818, 763.736871933428, 764.2246508787795, 764.36617031825, 764.6623856196844, 765.0295726296287, 766.9979899820813, 768.4014919692123, 768.8257806910716, 771.527509667296, 772.3715168209183, 773.1740269991102, 774.0756877772907, 774.4743054322547, 775.1367375364492, 775.3026160475414, 778.6719090287514, 779.744627953759, 780.1866593278818, 781.1648740595645, 781.2660843435875, 782.195873164435, 782.2612029900586, 782.3628643770912, 783.7966192977741, 784.4888089407754, 784.6367881843358, 784.7359038309914, 784.7384779951171, 785.2495966870318, 787.9855715726871, 790.2773220154539, 790.312609935038, 790.4378365667152, 790.533757057437, 791.1019776157076, 791.3799240960219, 792.7896912133468, 792.9311368761721, 793.3658128950452, 793.4168993291433, 793.7173823989064, 795.7159271657723, 796.0813440544954, 796.1570467850001, 796.1872898157641, 796.3514789978611, 796.4175259995656, 797.0646931205439, 797.2201158653692, 797.2218763906096, 797.5723007766065, 797.7258374628436, 797.992519489982, 798.6862168339599, 799.6254697534515, 800.0814993180624, 800.2288859023639, 800.7138498613135, 800.7776106002617, 800.9354327295686, 802.1596109558749, 802.2376373634349, 802.6879030822666, 803.2081850392542, 805.7278633955336, 806.0643387630344, 807.4044895382432, 808.3958213518914, 809.2198714944394, 812.1676376827128, 812.4864295794731, 814.1931852058801, 814.8803224202546, 814.9409263199512, 814.9967380038099, 815.244941567678, 815.6051724726686, 816.2660890102237, 818.0898681915935, 819.1972252449845, 819.314865340113, 821.0134323230512, 822.1895412121238, 822.2635662287636, 823.527238392914, 824.3141803588763, 824.5892025381839, 824.8026214447174, 824.8712800378476, 829.6239635465207, 829.696867023555, 831.1805343683822, 833.4069026608929, 834.742318414061, 834.9016003644626, 835.5887197279225, 836.3374721697777, 836.5785909506478, 836.8209673563863, 837.2414050292272, 837.6201056414725, 837.7173106746827, 837.7426338499342, 839.8990487227758, 840.8763607568036, 841.31536497874, 841.6385475168275, 841.9737123907339, 842.1473852398024, 842.5669491555927, 842.9155690186717, 843.0592523003774, 844.2357457168579, 848.5563138598892, 849.2506285921608, 849.7332200055868, 850.218731870914, 850.8544409124546, 851.2466750264825, 851.4898439719984, 852.9115081161016, 853.9223930121552, 854.7038478128267, 855.7957261658904, 856.2329213546789, 858.4997983908892, 860.3600750976127, 860.7205726664843, 861.6320226650068, 861.9232615347162, 862.1889119524099, 862.5124929976074, 863.2854077539968, 863.4334217559193, 863.9341360282878, 864.4377385169787, 864.656111790225, 865.9037014445146, 866.3547569072404, 868.3069855238806, 869.1566506727098, 869.9955184958358, 870.0616574155923, 870.3995972681026, 870.4028500992796, 870.8345494056705, 871.4465438589181, 872.3462970792556, 872.6214834092573, 873.1802533874799, 873.7768798531117, 875.0522791988559, 875.3520881778251, 876.1822313666199, 876.3188141840683, 878.8771842143183, 879.2131921166709, 880.7731565893689, 881.4491082068566, 881.7600368200692, 882.0924606450212, 882.338693544639, 882.7049659864641, 883.0144836495965, 883.1813582715436, 883.3075114587731, 883.9675456971742, 884.9317733997099, 886.5788135205339, 887.1483106721446, 887.2110353230129, 887.3300028379059, 887.9617278073378, 888.9310367014771, 890.0341730776804, 890.4802825200352, 893.0181633960732, 893.6810870615675, 895.175449348045, 895.5241879341336, 898.6569081659702, 900.4195453649799, 901.4641304889727, 905.5201820992414, 906.3527102093524, 906.5465143384044, 907.1606292943288, 908.325592012075, 910.4007245545044, 911.111873515755, 911.2998138977796, 912.0506763282228, 912.5818151791874, 912.7519577371679, 913.8341046511171, 914.2922624716222, 914.2929439878413, 914.3100552932756, 914.8109256734062, 916.7035440560377, 917.3084146635078, 917.3392738491972, 917.3733576015433, 919.2430565071687, 919.293290891946, 920.154268592484, 921.0184001127301, 921.2583357797571, 923.2008249916636, 923.3489428869212, 924.3743931637216, 925.2878831192512, 926.4389406152452, 927.3434386023088, 928.2882760014884, 929.1839901292752, 929.3380940019314, 929.7730817587902, 929.8473828684914, 930.8566262883473, 930.8841374095116, 932.588192905297, 932.5936968815431, 932.7731858193306, 932.9970401391797, 934.3288711408294, 936.621967874822, 937.4031923309539, 938.0395563474985, 938.8274958907775, 938.912122571657, 939.5184830993677, 940.6059543521525, 942.2748600771329, 943.0848965821784, 944.934942407123, 946.6766259606885, 947.2691183866075, 948.6086526537363, 948.7419774117725, 949.659371343866, 949.7508427829139, 950.6753214421501, 951.1032237162037, 951.6001830279797, 952.185099948305, 952.4553058815558, 952.5868969149827, 952.6542255457633, 955.299443713126, 955.5432714235559, 956.0906359246492, 956.7315515861872, 956.8712560781119, 957.6904874658034, 958.8007752563166, 959.5786439450524, 960.6463154291858, 961.563561395951, 961.5728530444469, 963.7067045766493, 964.2771852809054, 964.6539019135179]



    min_val_1 *= 0.95
    max_val_1 /= 0.95

    if(max_val_1 > 999):
        max_val_1 = 999


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

    X111111_1 = [210.48432676406958, 213.51586216114333, 214.47096000524036, 216.35435766510696, 216.4500838381623, 218.71935369918356, 219.4272832361907, 219.69217794993872, 220.84868690861745, 221.11970675361923, 221.31065504877358, 223.7243342819152, 227.58076896826165, 229.15750862725736, 229.92844654133057, 232.09081608799693, 233.27116446891253, 233.29244773523806, 234.2003785912968, 234.31167882527748, 234.99116070316003, 236.23418553117708, 237.46715394262577, 237.5312533294313, 238.5472565250611, 238.95646927254802, 240.01379309294208, 240.1934878247808, 240.55537404103586, 240.55816952468643, 241.58453386242545, 242.65649555506963, 243.62259971138636, 244.25877943357807, 245.21661865911597, 245.65512629765996, 246.00182172130616, 247.10797823977975, 248.73508349064835, 249.28876841935505, 250.1050709546722, 250.82886141070088, 251.82878276665076, 252.1080847585391, 253.30351005555204, 254.90208726426494, 255.73695481714276, 258.4252990810967, 258.8948777276561, 260.1265550270457, 260.7526277886931, 261.37158471468354, 261.49516940468095, 261.934843304085, 263.24510572897753, 263.7193442167134, 264.55660566897564, 264.6873045618218, 264.8416093033134, 265.44491923721785, 266.1305219305673, 266.32446188900775, 267.4305570832379, 267.63063430070946, 268.62594419586617, 269.53900613646226, 269.93070238514935, 273.09287779813644, 273.4812762626415, 274.0057854731185, 275.36981873777745, 277.35653118758063, 277.6900492757917, 278.1664183775395, 278.67564254542526, 278.8161276578246, 278.9617171727355, 279.89509838234903, 280.53214900100767, 280.59333407479534, 281.1313170796051, 281.1512796860575, 281.27028318102384, 281.28752225250133, 283.05099620226844, 283.6148079840549, 283.6170723353184, 283.6699757083875, 283.95403863147345, 285.22915120134843, 285.43427891840724, 286.3186895576996, 286.5437511277553, 287.05623783420344, 287.4529727144327, 287.56523748652, 288.03273381468216, 288.3373993380699, 288.3524748469039, 288.5335035932487, 290.0675399187886, 291.1469975602904, 291.49648391503484, 291.85413907397214, 292.3854733704921, 292.98159661453224, 293.0142843036417, 294.5070546159206, 294.55702292708645, 295.9946351427337, 296.4006169926857, 296.55690272675486, 298.53336677428473, 298.79723090165464, 299.0991261765858, 299.1102073202916, 299.9192875491773, 300.1034495909238, 300.7632501753934, 301.2822416256235, 301.7127667935668, 302.5973513183022, 302.64748192684635, 303.49440101215515, 304.3723536992859, 304.8505027457496, 305.1778637190591, 305.35460771776815, 306.8229128893185, 308.71303579714356, 311.3158439817637, 311.3649752683129, 312.58505576403854, 312.8273407646611, 312.9835946336285, 313.0584739721244, 313.79933060798396, 314.5257123628386, 314.89862275985826, 315.539636577793, 315.60742905190943, 317.10587756079315, 319.5097719434261, 319.59002187585276, 319.9686367049761, 321.4992951334453, 321.81960099768696, 321.82154509997207, 323.4645845435851, 323.97323446358075, 325.25440848285825, 325.91323248843435, 326.1516338716654, 326.35188293230084, 326.58037000409405, 326.9686215087762, 329.1249137959808, 330.86058270988485, 331.1917758529404, 331.97742187188646, 332.3281886570737, 332.75493402938355, 333.77368175622024, 333.80304678411403, 335.91076484264113, 336.8926144417801, 336.9741918091706, 340.7214080178659, 341.48790297308506, 342.2783722025984, 342.47837158183063, 345.0061857823347, 345.0799713316579, 345.3919526190882, 345.46346617254267, 346.79011363165034, 347.7673973970425, 348.37463528662823, 349.5098910671335, 349.6467361684345, 350.09583065391064, 350.67789085299546, 350.73435383194624, 352.21036698226783, 352.3490766742482, 354.360320255236, 355.0805016572688, 357.1070891015528, 357.2780394495194, 357.386222773153, 358.51806585352233, 359.96299583524865, 360.6925651287461, 363.30705578570496, 363.4721861280677, 364.68677430781406, 364.7752585310248, 366.4838926730329, 366.68193499812685, 368.8250543820998, 371.81564849986023, 372.90826027218134, 373.410644084684, 374.74646660527077, 375.15016032796143, 375.88741810294863, 376.0292839206388, 376.70543943620635, 380.0058539736302, 380.25523119915715, 381.04851261257625, 382.8357712226873, 384.3144553786149, 385.5696716810909, 386.39478154768835, 386.69624060132537, 387.0156763459398, 388.64434354997593, 388.777780307438, 388.85883625221607, 389.09092710219096, 389.6628638596542, 389.7080933371669, 390.4012747098607, 392.1614102822319, 394.42206494780646, 395.07457733729547, 396.4676043733426, 396.96559076226947, 398.2159719553898, 399.7199982591194, 399.75605009857105, 400.8003903720032, 401.5552056733209, 402.7120149430392, 402.97117845532875, 403.09300750674953, 403.86432394777665, 404.9007090158155, 405.04136273169064, 405.3291477873406, 405.5474898188627, 406.2198863972367, 408.1448047473902, 408.3616970013027, 410.54053469192297, 411.1384162794095, 411.87111436309806, 411.9034722554291, 412.7924057055228, 412.83571920582176, 414.9685988474474, 415.3477637682969, 416.8181367249354, 418.1855355827722, 419.3636046777225, 420.4014785826155, 420.41284547088253, 420.9107192672123, 422.11961546850904, 422.2954056308274, 423.15591815427047, 423.2440972829919, 423.37594232736126, 423.66228677366433, 425.06966081287294, 425.1579880617489, 426.17204897462295, 429.6580319682419, 430.1977956974533, 430.3413619148115, 430.98869311913097, 431.25699595814854, 431.6401816398208, 431.8306324680255, 432.5591266681621, 432.8000968642068, 432.83531772654254, 432.8752109345194, 433.0449856484114, 434.21429194722293, 434.59682663300373, 434.61131833626683, 434.77237665751363, 438.1115726184664, 438.131597848357, 439.867168634897, 442.0314222738581, 442.42071882454434, 442.65127947056794, 443.663426402319, 444.44666442850485, 444.89446742706167, 445.32626332970096, 446.10612274117676, 446.1119276516788, 446.2780902314988, 448.1146858971526, 449.9848996711745, 450.35174826464186, 451.5496966445154, 452.4684350618794, 452.54970412781324, 452.7450520980397, 453.93142873183683, 454.34346944813217, 454.48379507043234, 457.0510677246415, 457.07242322539423, 457.3206916901938, 457.3452698570833, 458.1133449963352, 458.98106632496155, 459.4932492556181, 459.6255069064223, 461.32536115807386, 462.18031013705234, 464.22700230682835, 464.4480190841865, 464.8509715391692, 465.1826018559191, 465.7785287228854, 466.469434790515, 467.2813967000575, 469.3564268498777, 469.78559661237256, 470.5002581900529, 471.1242094963546, 471.4556800982558, 471.6447892457944, 471.8818839546323, 472.9268920216276, 473.23832905926105, 475.21211982500876, 475.31357700290306, 475.42981668368606, 475.4715690577715, 477.3582775012727, 478.3515481458368, 479.01128795168586, 479.59794621699564, 480.4812376533807, 481.3796820293792, 483.7061021588524, 485.4141473361344, 485.82320021719164, 486.8419390115843, 487.3400816092393, 488.294815942367, 488.3524259315689, 489.6771965320093, 490.57287460054266, 492.3902663890389, 493.08678522726, 496.25105830041076, 496.48079642513846, 500.9815197357752, 501.4391590862301, 501.4748861426461, 502.15708946979066, 502.2333826049468, 502.76834889158, 503.0579344373788, 504.256928147442, 504.6479668979448, 504.7741549258486, 504.92070063854715, 504.9510049585889, 506.17210539605344, 507.87233210992446, 509.95347305450406, 510.2095678798626, 511.12146500871836, 513.0983838132624, 515.1353089184659, 517.506806288272, 517.9135764846258, 518.5824935596177, 520.2227827859546, 520.5408769222768, 523.0839332636347, 524.0526634430763, 524.8076503344341, 529.0167801769303, 529.0183865447593, 529.8415337339967, 530.040175250874, 531.1961063291942, 531.2328971572713, 531.9617861564975, 532.7522792078304, 535.5085687517724, 535.843411537392, 536.3690677731934, 537.1028767765845, 538.0317770311303, 538.4508567532148, 539.2787303301511, 539.398960167757, 539.4449917125469, 539.460111319599, 540.7619019893609, 541.7948053030213, 544.8457033418058, 544.9443004573479, 545.3490066341419, 545.8544917397263, 546.110926378889, 547.4257320837385, 547.809233271056, 547.9445902772379, 549.6530554793205, 551.3651402592432, 552.3780162854838, 552.8096185906413, 556.2979072048938, 556.4273270929428, 557.9645181129348, 558.2526900610383, 559.1258923720735, 559.1291744375596, 559.541815398343, 559.8731006610897, 559.9340870170141, 561.0828466481048, 561.6720695475274, 561.8798515672238, 563.2040110266865, 564.9044088453538, 565.1359294150072, 565.3861745283398, 565.6459031899299, 565.7734453268243, 566.998363644161, 567.8627002882785, 570.2648823408131, 571.0814176348002, 572.120812972389, 572.421981934823, 572.660706392001, 572.7024439979609, 576.7770163978325, 578.8869144010416, 579.7123727404278, 579.971721681437, 580.7193382564226, 580.9081904016787, 581.0814840101463, 581.8681116890493, 583.4433399631992, 584.8833817159439, 585.6703519772097, 586.061250347838, 588.0068279658758, 588.4011699716787, 589.663639338556, 589.9233515286362, 590.3656610692162, 590.4365166534349, 590.5961993503818, 591.8803551238591, 593.3457913379407, 594.775027905915, 595.283094644892, 595.3985123876649, 595.8754821973507, 596.2841133050147, 597.3253208042881, 598.0455153325089, 599.3143557318651, 599.9863145192439, 600.4816516293766, 601.1270716879329, 601.3796574715197, 601.4703459804132, 603.9806006513429, 604.3453547590545, 604.623126904359, 605.8730311053978, 608.022990120452, 608.2908768146931, 608.6792926477892, 609.225464491431, 609.6929187534781, 610.1426595773024, 610.299191354459, 611.523029078377, 611.5595167944518, 611.6851398783904, 611.7587551839313, 611.8025560275775, 611.9676398260758, 613.1190915241184, 613.8368302373756, 614.3636498715334, 615.0256192122862, 615.0308576603788, 615.4408456289057, 615.87683407702, 617.5401244073876, 617.9787263396289, 618.1479896311437, 618.9134407469332, 618.9231306761922, 619.1338873563982, 619.4264033778943, 619.833702780242, 620.9261615564867, 622.383459803053, 622.6618347374321, 623.3143011358529, 623.5383624423262, 623.8162770396075, 624.0534000884993, 624.3325060194024, 625.2492912098213, 625.3352159166741, 625.6870924555186, 626.3733420179335, 627.7732834984935, 627.8891239542868, 627.9978667976726, 628.0557538818399, 628.2177141806839, 628.2632869888498, 629.4284423532392, 629.5450417419582, 629.570438490276, 629.8335480706434, 630.0510560320756, 631.6171404253797, 632.0273372069348, 632.5863510622662, 633.1667935942321, 633.8308898341708, 637.0180626092229, 637.6276247344416, 639.289670955196, 641.9163494806824, 642.5770450317156, 642.9996782592006, 643.6029654564809, 643.9695976989543, 644.2987883218997, 644.4023826508501, 644.4906804913659, 645.2134817813437, 645.5270283384714, 646.6986950594375, 646.9310132187469, 647.0153827909371, 647.4699252088456, 648.3784124095532, 648.4799307313394, 649.5509855946983, 650.815159290506, 650.9590678501088, 651.742682295694, 654.1510475874177, 656.6655409512068, 656.6702726550806, 656.7883698586704, 657.4760517806417, 658.6813678058468, 659.984191565974, 660.0367345353345, 660.0429068744904, 661.1602857567052, 662.9913336266725, 663.7787008807122, 664.0094511742292, 664.12457580141, 665.3792363849684, 666.017094294275, 667.5409500913274, 668.0058741698299, 668.5318718738001, 670.3574526461007, 670.9286604666363, 671.3315476783212, 671.6477095129844, 674.2230365181842, 674.3384102033702, 674.9990678000225, 675.2806059817628, 675.7668805780834, 676.1232073265953, 676.5040440929336, 677.0384381106653, 677.2869595841162, 677.4585605993307, 677.4733601751077, 677.9534431558882, 678.1233787491379, 678.4959698033385, 678.5395435752392, 678.6821828722277, 679.9043895832381, 680.4227976909697, 680.796275561124, 680.9104133353005, 680.9326558693315, 680.9370633178655, 681.0009252750576, 683.3930645424689, 685.1388105031755, 685.8909223225705, 686.7162191807361, 687.5542271577585, 687.7031301612212, 688.0274160153934, 688.8852973039626, 689.4850834231714, 689.964145550337, 690.2497174118344, 692.459712879829, 693.2148171272898, 693.9157442340518, 695.006076260609, 696.1744750971661, 696.718155639006, 697.1062481570125, 697.8260953880324, 697.8547625858232, 697.88513328369, 701.879177200176, 703.0417987423781, 703.2748184233556, 703.3928253415044, 703.7496260298071, 703.8101482017912, 704.0317126193711, 706.8962180759901, 708.0123928753599, 708.0222063287117, 709.754511924566, 711.6243669079471, 716.1672076008126, 716.2992275426369, 717.1991173250578, 718.3347058514922, 721.5318969138126, 721.8201309813787, 722.3963266974255, 722.820286750921, 724.3414880458917, 724.4354165798834, 726.1567249747714, 726.3296025115983, 726.6482390959076, 729.5736592289279, 729.6283520324051, 730.6945562178196, 730.7563278929135, 731.0000266121117, 733.7698226461506, 735.5085939872923, 735.6937152816347, 735.8395721415509, 737.3613243964303, 738.5763436711374, 739.0410749566672, 739.0854603683003, 739.7089664963702, 739.7347602290865, 739.7376253263363, 739.9658153438558, 740.656112438347, 741.7668103757516, 741.8435435654582, 742.9603464611733, 743.6605440006425, 743.7065504038168, 744.3131423491284, 744.6970855159515, 744.8929785085469, 745.1033964777434, 745.8911109042624, 746.431811724115, 747.5952540315701, 747.9280959980953, 749.0448448898709, 749.6103971211301, 751.2161485827252, 751.7471109649063, 752.4210825929557, 752.4903604142762, 752.959574253643, 753.1939216126423, 753.2442083469515, 755.2019883700405, 755.8376480869422, 756.4682356315597, 756.9432021223562, 757.8027612795572, 758.0655048892462, 758.7793451327052, 758.8784774670614, 759.0602601660339, 760.1613678589905, 760.3248987418641, 760.5215900735657, 760.9070865684115, 763.0769098685497, 763.5157776942378, 764.9338660037668, 765.5362037788852, 765.8800563943335, 766.0872167747334, 766.1232186346216, 766.3551087021791, 767.8510197189061, 768.6966863940033, 769.6391269605745, 770.3099295365893, 771.914117572288, 772.7994955878576, 773.6188796428094, 774.1472081791941, 774.397333175722, 774.8663072461707, 776.124634782428, 776.445883284418, 776.4636895606096, 776.5279868141682, 776.7755921497007, 777.3531907595728, 777.9267120856032, 778.4949949327125, 779.1673959000885, 779.3896120562827, 780.0140328278865, 780.103584314634, 780.4879882763685, 780.7637818654031, 781.1752584468259, 781.3036132975857, 782.0752211545512, 782.2380050700966, 783.8937798777941, 784.4754091788183, 784.9952216994094, 785.8099425942718, 786.4656057010259, 786.6945215661493, 786.7581396583353, 787.2470591825895, 787.2521572031254, 789.5474809242784, 789.9429570905968, 790.1945069229675, 791.6253197277257, 791.7121358759017, 792.294024919671, 792.731294133699, 795.6599672329273, 797.4877182490019, 801.1238307503025, 803.972012794242, 804.7124412768604, 805.1567662267001, 806.3514271800652, 808.126191162975, 808.3099075557303, 808.4215540654894, 808.7814323742876, 809.8592080582298, 810.6979999006749, 810.8976114032164, 811.0568156472331, 811.956164658502, 811.9871292783606, 812.1914129019522, 812.7623337515873, 813.2271378801312, 814.2467918927165, 814.7351137340671, 815.3664483639188, 815.5854755686365, 816.623451606627, 818.4104096050633, 820.1030365711326, 822.2031600327236, 822.761620401863, 823.3744957270155, 826.5647496348773, 826.6235742912139, 827.5666587638323, 827.9839283124137, 828.1828444975964, 830.9388366056475, 831.0784533616085, 831.1811973317529, 832.8898775759324, 833.1750044735157, 833.1766034890869, 835.0099845487564, 835.6457473859508, 837.3404508950041, 837.3611416235917, 838.185409826544, 838.6053150727198, 838.7845621461067, 838.931934289862, 839.91380324448, 840.1667403358158, 841.688787613145, 841.9617874047495, 842.0154582603376, 843.3659562037204, 843.9498996950837, 844.2218307476846, 845.4903748665089, 845.655523381409, 849.7659662682114, 850.6186957119335, 851.9839291577491, 853.2938712277382, 853.7548123460648, 854.6183594983543, 854.6546189723949, 855.2301573527087, 856.0876831394081, 856.1115585892117, 856.1775840028993, 857.8782959551471, 858.3281751144048, 858.3618808924277, 858.5577844504563, 858.6336971382832, 859.2982178472861, 859.7365066641485, 860.1086140762116, 861.0847710015058, 861.307523138121, 861.5949264526048, 861.5985162882437, 861.6317839289956, 861.8697660520996, 862.5354502503833, 864.7418635359335, 866.8167708202204, 869.1808401971377, 869.1986770605869, 869.409136231873, 869.9555193375842, 870.4155754665331, 870.751208776312, 872.5397604658206, 872.5763996114777, 874.361278584624, 874.7586041775336, 875.3072278900534, 876.5302475838208, 876.9631081173128, 877.3480333377757, 877.6331653242188, 880.0451088633753, 880.6675278287813, 880.918707654935, 880.9963936276298, 881.4056087334762, 881.8989846730918, 882.1641464696548, 882.3784527561513, 882.7169355395164, 883.1572072422157, 883.6172443620289, 883.6572890452636, 883.9226907850164, 884.131983835522, 884.6126770423613, 885.238735490818, 885.6883636876835, 885.846259316691, 886.1980381414178, 887.4526436482209, 888.0933819707557, 888.1477531428401, 888.8538648557784, 889.0448675658474, 889.3693244055717, 889.8155496303278, 891.4584112129436, 894.2102669440751, 894.393230998684, 895.7343939986914, 896.4401118241337, 897.1833139805743, 897.1960142294921, 897.7043340804222, 897.9778598020445, 898.8282124723584, 898.8944325705896, 899.7968160398785, 900.4484825553677, 900.816932274468, 901.1400980851777, 901.3730750628632, 902.03202096792, 902.5367142994139, 902.5657318758754, 904.3213054963442, 906.2535836102358, 906.2957739813862, 906.4882750645588, 907.0843887422682, 907.9384187087758, 908.2539797700806, 908.2837616696697, 908.3010912122473, 908.4016509127584, 908.69900978563, 908.9697660524566, 910.2738836818771, 910.2893671912121, 911.0245506695964, 912.1216537799716, 912.6175936366553, 914.1475195952637, 914.5545484793108, 914.8770317411494, 915.0021858417367, 915.3550575931744, 915.3980758813912, 915.4935463871199, 915.7421440357889, 916.4589888764008, 916.6480100090088, 916.8431877214798, 916.912249527566, 917.1371096754506, 917.9058358229433, 918.8110385254562, 918.9607357732637, 920.18979782574, 920.9242764292935, 920.9969916578946, 921.7766984644237, 923.5330001378005, 925.3319501664748, 925.4307983974333, 925.4847415331236, 926.0979821437772, 929.780723046824, 931.237056652275, 931.2378113700842, 931.2384943843214, 931.5311254089103, 933.0976805317232, 933.1287506660541, 933.1534797620671, 934.7545670174746, 934.9981707383481, 935.3515160321077, 935.4598377150274, 936.926845000565, 937.8973842546615, 938.3865520084169, 938.5574713892531, 939.7541793782879, 940.5966551623595, 940.8904852078961, 941.2270532517174, 941.3649386803422, 941.453515708015, 941.5122108943788, 941.9156351909186, 943.4276309342962, 943.583624628676, 945.6617395083803, 946.1770536828673, 949.4470993258044, 950.9350773825744, 951.2078347069639, 953.1106642243727, 953.3569941524787, 953.9889223606012, 954.2138133113676, 954.7777240316514, 954.9665198043787, 957.513868883085, 957.5155825521274, 958.0849924210428, 958.3680415328317, 958.4536118820527, 959.0496025929555, 959.3114628767532, 959.9527129952081, 961.3470123354052, 962.266264517929, 962.3367387777812, 962.3693941695911, 962.8272180352403, 963.4084760519015, 964.534271128186, 964.624802888813, 964.9749003233663, 966.3989906981373, 966.6224624030664]



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

    X111111_1 = [210.08534919432182, 210.3659345386396, 211.05211166281998, 211.63269433562465, 211.80466644529452, 212.2701200585845, 212.89390655017203, 215.21071323809895, 217.45678001488767, 220.1452938562889, 220.7001306206381, 221.58282117441692, 222.75374135069578, 225.27269596410932, 225.59891330915136, 227.13582178349264, 230.6634670159716, 230.75703236938807, 232.09717694112499, 233.10311881149175, 235.87264501544212, 236.0842826952682, 237.92662043913944, 238.1468390802392, 238.3089443920236, 239.00546403462246, 240.69023190983344, 241.51466430353105, 242.06176819098357, 243.0326474395464, 243.17042453391497, 244.0415542868397, 244.245097502552, 245.0744678190057, 245.3765627309641, 245.73517990802435, 246.28817192221712, 246.5632475737478, 247.77199133410195, 248.3114077312658, 248.73476661399008, 249.0442735577572, 249.3047910931238, 250.6238362068524, 250.69936142461574, 250.80831339195063, 252.03772429782111, 252.35350632261864, 253.79502210455843, 254.20305745112395, 255.0383706811827, 255.09099432034213, 255.35398716522852, 255.71520701617337, 257.22928523010427, 257.6744267923547, 257.7229870339983, 257.9032553212039, 258.0393404390427, 258.1771033304387, 258.32225946669786, 259.78433953793194, 259.8933990448384, 260.42057973013976, 261.374926307334, 262.1554775151828, 262.79732003105846, 262.8833383661341, 262.8855087530387, 263.82447697089464, 264.4017117828731, 265.41816802424535, 266.5251692661695, 266.57091732945804, 266.8758698679691, 267.44698046674273, 268.6273522458863, 269.4492315265053, 271.25522846820485, 271.786410387857, 273.00603646838505, 274.08449542542917, 275.7173857225983, 276.30226382474166, 276.6600451470703, 276.8719719926995, 277.00063076496167, 277.3936706600625, 277.52769353737875, 277.5412836598422, 278.78477711565426, 279.09637795113383, 279.2281802933993, 280.9170169754957, 282.523508411549, 285.0069559185676, 285.22323002427055, 285.6076265685389, 287.142934943182, 287.4498346213131, 288.13948271914165, 288.2043579281458, 289.9010580198301, 293.74974637315626, 293.78912390870494, 294.17984519778287, 294.21014296517785, 294.93401160914664, 296.434276791211, 296.4861419408265, 298.10790840208995, 298.99885894708456, 299.23310081110884, 299.8332475340553, 300.7748002847293, 300.82573220086016, 300.84658298446845, 302.28349668311347, 303.4769131850594, 303.4935800641846, 303.95998582744846, 304.50854158122166, 306.073197587414, 306.3145371406965, 306.9697282793526, 307.52759588712337, 310.82768779612746, 315.61918390560646, 315.6596770727155, 316.4561919533782, 316.77453747995344, 317.09220610204807, 318.32311637154527, 319.330338378004, 323.15382126803866, 323.4881747058207, 324.9621689298308, 325.4702794542462, 325.57922890141896, 325.66755533278445, 326.06433631380025, 326.26438211696814, 327.0868890456138, 327.1401501749772, 327.16625904412973, 327.1813158334835, 327.5785612841734, 327.7167786986563, 327.8161617471995, 328.66981315464966, 331.9515437670968, 332.36714154227064, 334.0352914786808, 334.05040155245297, 334.34751086657667, 335.19143821123714, 336.95599026079304, 337.19549777417944, 337.2832947257938, 337.5447194611822, 338.73388666895437, 339.712212156845, 341.05955938420243, 341.4319071662866, 342.64151667850615, 342.8306575816101, 342.84981825737543, 343.5803919480003, 343.64902035520106, 345.25198085703005, 346.58890499807535, 346.8135537971027, 348.1011874528988, 348.202232174737, 348.36118736408514, 349.9631553871118, 350.7343051765199, 351.7480532256334, 354.5415481762158, 354.65870691555494, 355.52478313899405, 355.8266504668934, 355.9183449394445, 356.15837886130953, 356.60753959390513, 357.8228961315782, 358.0764595745593, 359.078863740306, 359.8199586356975, 359.9272741056943, 359.9679385092361, 361.0970456167357, 362.3391919738583, 363.02972068479244, 363.06487792562365, 363.509628548271, 363.63917551359134, 365.62122741548706, 366.1017962079959, 366.8358784573253, 368.11823493388493, 368.1758479993775, 368.191443802923, 368.6912583326822, 369.5942208864219, 369.7753570103143, 370.0662358896867, 370.42630581416734, 371.3047979260764, 373.74832925610906, 374.02769130235134, 374.1530667915541, 376.15056219721794, 376.27899657239414, 377.13389324585916, 377.237527198594, 377.91236926289434, 378.0877458382612, 378.2133799221212, 379.94834390831136, 381.4981884427798, 384.3477592148513, 384.4578863645954, 385.3025281471796, 386.6533514462842, 386.6633930472236, 387.5401755288485, 388.0820901844621, 389.96770070397713, 391.6317838129397, 394.61413804168717, 395.6843606719666, 396.1612164904543, 396.22174235404145, 396.3788633303446, 398.4016618986029, 399.17476800302404, 400.17618188950553, 400.65710860533795, 400.7139791968912, 402.35479327744054, 403.55257090013475, 403.72921342689506, 404.3605080321039, 404.8105199839556, 405.0523728117439, 408.22581190890344, 408.6100604698489, 408.80052611194566, 409.0706867053535, 409.5529658742788, 410.14765068863824, 410.5388058718309, 410.89128015879993, 411.6400616243752, 412.27871591632476, 412.4679493586707, 412.80871915138067, 412.88173805496086, 414.9715247620258, 415.04745424426585, 415.4665044670123, 416.4675811048104, 416.73688290747805, 416.82085268517574, 419.81272629622765, 421.12344798911977, 422.3091937615119, 422.42980525017856, 422.99297694104087, 423.36699362911463, 423.51514701778825, 424.114148122204, 425.00859513789874, 425.0753967175942, 425.15155452717283, 426.0501339943214, 426.56980629252905, 426.715715354018, 428.330699655797, 428.6832218312551, 429.05839446642494, 429.15909985005203, 430.5151724404244, 430.5447422846971, 431.29164471449855, 431.3465919609048, 433.3083496791679, 433.6519227970482, 433.6964727732492, 434.07206534217835, 434.2217880946888, 435.23958944372214, 435.617785920099, 436.5728163857631, 436.80581560572216, 437.64241668760883, 439.20639727412095, 439.44306849902233, 439.65308643601685, 441.34934481111384, 442.84891843946275, 443.4689843321842, 444.5140173134312, 444.75944793232713, 445.31200848948595, 445.34724998869336, 445.7537856818911, 447.88536494917315, 447.9998373117743, 448.13803535793886, 448.30809236455923, 448.86193968445144, 449.28764095930853, 451.0926942486796, 452.0982179251957, 452.41732917911355, 452.4446924923619, 452.60343343522845, 453.8260211903453, 455.0350496441482, 456.2667918833481, 457.05034423518816, 457.31042773837964, 458.0692820785051, 458.10767902525197, 458.2641595890311, 459.76383268157963, 460.3798189530072, 460.5569113022095, 460.67790652958473, 461.2653570638195, 462.67355327298793, 462.74280338984886, 463.9357227259012, 464.15670778317866, 464.38011680676345, 464.6217934093247, 464.7566233554396, 465.34552985711923, 465.6873965151407, 465.9428775645529, 466.2479032830097, 466.4779993901619, 468.5337292871019, 469.50130814260325, 471.30394016453005, 471.3051081056243, 471.6363354750842, 473.157628832573, 473.5722839613832, 474.30349055158104, 474.4395364036093, 476.02592469293705, 476.19491870623085, 476.6437024087837, 476.89816982073904, 477.9788534945082, 478.27954027469065, 479.25570356798727, 480.5383981087665, 482.1767246625813, 483.62709795404044, 484.0849060170188, 484.18087202402387, 484.2588393208526, 485.0563463446042, 485.6675390503076, 487.26542332239654, 487.5960478313175, 487.74067975236045, 488.7593164940361, 488.8557909529131, 489.2023835045914, 490.10863852376247, 492.5854553565642, 493.30307674147804, 494.02221386103975, 495.85296010511473, 496.46319296401447, 497.6304857129632, 497.7573859074503, 498.24865077832436, 498.50731729312616, 498.5287553965822, 499.8853482042867, 500.1459782063261, 500.40631385637624, 500.91593174891824, 501.8098962870043, 501.8915758161026, 502.2958126369127, 502.34691761531826, 505.12391807187004, 505.24920524433486, 506.55368068228677, 507.4756965024331, 508.4903015317188, 508.55445024240197, 508.55611901065777, 510.1208434557306, 510.13101587086624, 512.5370687408417, 513.6047599042138, 513.6586099744611, 514.068006439395, 515.0214472445505, 515.1003729451816, 516.5748713506357, 517.850896181644, 517.9811783015659, 518.3957214121706, 519.356129601443, 522.0368046353867, 522.2859937202574, 523.1769620630412, 524.5975463836173, 525.1520671739548, 526.0260770029385, 526.4867297646338, 526.4955265191162, 526.8623595070396, 527.4122213483402, 528.166114818066, 529.627263758568, 530.8042123923735, 531.3248151971595, 531.551537309668, 531.7037635749743, 532.3922066459912, 532.4455822128366, 532.6815677078221, 533.2655400406882, 534.1292087316449, 535.3618645362797, 539.0195683184909, 539.247545013191, 539.2831815843658, 540.3009166933055, 540.9120813666251, 541.1428809215956, 541.8398220561745, 543.2884740673303, 543.4518832897511, 543.6707433611775, 543.8105483075188, 544.3053187668089, 544.7997230146052, 547.1327219321527, 547.6475074377313, 547.6697251963147, 547.7973270656231, 548.1166591721444, 548.775849189778, 549.0237881701435, 549.140258998842, 549.5743852006002, 549.8691894176079, 551.0728199080922, 551.2528810250076, 551.6583703884589, 551.9190018556759, 552.4686641826289, 552.8682087673858, 553.5232955035965, 554.3254988297372, 555.398649063307, 557.7528799985596, 560.065685352735, 560.9721856607182, 560.9867904124038, 561.475637621644, 561.8046339101569, 562.2105589741082, 563.0569899444391, 563.59516074834, 563.7432588372783, 567.572663212833, 567.9687497959084, 568.9865832046767, 569.1065863879907, 569.2706804313618, 569.7849162174743, 570.9375025232881, 571.6267015834792, 571.8619887292994, 572.0208010133099, 572.8058101020723, 574.2244881048321, 574.6677419499475, 574.7751379379533, 575.7957088872196, 576.294935848444, 576.9705372555045, 577.1317885082308, 577.2117675149686, 577.8293358347541, 579.9290922178914, 580.0872409894747, 581.1819109530998, 581.3019337302052, 581.6258689312193, 581.6312226628274, 581.7969015860219, 582.4512848513164, 582.5810706200145, 582.9810175481274, 583.8174038124844, 584.1805010563949, 584.6486442652342, 585.5587207087314, 585.941059840842, 586.3757852632782, 586.4405472888758, 586.6567149174748, 586.6631404887662, 587.3912181130713, 588.7595466837081, 589.4984544527924, 590.0198365755393, 590.2810843343025, 591.2067107202043, 591.7107164846899, 592.7245074940633, 592.9170195382878, 595.0132430236101, 595.3712813741006, 596.2597720994382, 596.6340208480008, 597.0657675590076, 597.6924118742793, 598.6542726862808, 600.0983936621911, 600.2052151074525, 601.4700443549586, 603.1790560246412, 603.8733903514008, 604.2199314269662, 604.6030338084224, 605.0306160984005, 605.1170951404221, 607.5767459257027, 610.2664845905899, 614.7207804018649, 614.851639948404, 615.2984173609511, 615.433709244541, 616.8526852356432, 617.2700477613535, 617.7783382257122, 618.6530628055104, 618.9980093015477, 619.3001153033473, 620.2760159761851, 621.0072553450693, 621.1790125995842, 621.2601562708885, 621.8665691984846, 622.7155512406943, 622.9693886779969, 623.5894646396446, 623.6089506567491, 623.9507453954005, 624.4490287331793, 626.971566785109, 627.2169487135686, 627.4731342684995, 627.6251745932959, 629.1808779183025, 630.1251764851604, 630.2687181483121, 631.6217395684491, 631.8404717360168, 632.1352224529732, 632.1663303076054, 632.6832583267676, 634.4385886994255, 634.8485213805615, 635.3451216912122, 635.6393760876122, 636.1883480084089, 636.9675096850228, 637.6806031677149, 637.7458185447967, 638.1341010763284, 640.2754785263345, 640.5045868108701, 641.9243768125668, 643.048799703138, 645.6761689171934, 646.8765016583073, 647.1646905541159, 649.8963362818663, 649.9068644896056, 650.176006762857, 650.2191472024247, 650.7558333614841, 650.8895678528562, 651.7772390032748, 652.3422741821939, 653.4170122447812, 653.7547998957543, 653.8781139179805, 656.462809614142, 658.0734813957537, 658.300733949218, 658.7258529501687, 659.1756758649676, 659.3760551098978, 659.7776582156879, 660.3967458745674, 661.3542127352764, 661.8516923760287, 662.4253525267891, 663.9901053143152, 664.0960364715988, 664.4175800050855, 665.4605845255755, 666.5823202666734, 666.9612253485873, 667.1016699462228, 670.1684846124734, 670.1737646543496, 670.2883444949941, 670.3967767282352, 672.8166798540683, 672.8977557278622, 673.3978388962792, 674.080035415886, 674.4166882350781, 674.5703399733345, 674.7448452590068, 675.0418081865087, 675.8275852427189, 677.2498862771381, 677.8248352347898, 678.4625763583363, 679.2724751524515, 679.2956843854598, 681.0959599915701, 681.5035833437844, 682.7447565118907, 683.1781574494381, 683.3515585138668, 684.2758565538545, 684.4239282357776, 684.8857886827619, 686.4128882425126, 687.627079191136, 688.7533360233759, 689.4466204067603, 689.8004912586898, 691.3594540866534, 694.3144255309406, 695.6008759492729, 696.4066247925034, 696.4940811419485, 697.1763410212473, 697.990219758937, 699.2134453204478, 699.2145478339706, 699.5036738892309, 699.9284920192457, 702.1432619941937, 702.1568614818316, 702.4132426580916, 702.4232739285301, 702.5712536339223, 703.483908878382, 704.5670567326117, 705.6304404474517, 707.8655120472303, 707.8892331852797, 708.0653655384688, 708.2099510565804, 708.4497345618067, 708.6665334201372, 710.666423396086, 710.8088196132447, 711.2270341512258, 711.3726233540709, 711.8630406491072, 712.3358914182004, 712.4208996932739, 713.0603778637578, 714.2647140411286, 714.5277847095479, 714.8384562647814, 715.054728065797, 716.1479351063417, 716.4026972077227, 716.6092679953383, 719.5474609426878, 719.6143055918178, 719.9259173853867, 720.0538984773411, 720.1587628194796, 720.192750121017, 720.2434095949457, 720.3920396526823, 722.2640759299188, 722.5526612224741, 723.0094721840104, 723.627220973301, 723.642424588917, 724.1633263601582, 724.8394114627072, 724.8944229375187, 724.950986727578, 725.8728089384354, 726.270243809199, 727.1415678472044, 727.273829646221, 727.9644479881678, 727.977698143513, 731.2744653351241, 733.40153886324, 733.4297626188608, 733.9779942465303, 735.6389788791275, 735.7339391611094, 736.0748310871354, 737.0147297238005, 737.1850062368646, 737.8427896814326, 737.9421187207522, 738.2874829873027, 739.2038270557573, 739.2386051119349, 743.1511012043219, 744.0256058186363, 744.8140769063555, 745.0366398942423, 745.0759703683768, 745.8705065084016, 746.217611812422, 748.4712269278017, 749.8951765738608, 750.4069434906671, 750.9799703115174, 751.56175134361, 753.1569052203139, 754.2039546724839, 755.3499154225872, 756.2562895952788, 756.2995571103253, 757.2771116517288, 757.6517864862434, 758.0494421988819, 758.7248219325814, 759.6939082606526, 759.7520833998485, 759.8627007135694, 759.8766379320377, 760.6511658818642, 762.289582037562, 763.295856882916, 763.8047556708319, 763.8676753023689, 766.8631386250681, 767.4664062625584, 767.7117712782715, 768.0168108839705, 768.7245658302281, 768.7507008791288, 770.1742590245317, 770.488762667405, 770.7374313891897, 771.119065963881, 771.845297173231, 772.2676394003197, 772.4714377990255, 772.7286047015879, 773.4226700355364, 773.7650594217353, 773.830193617578, 774.0812844815462, 774.5012454312223, 777.7120547643075, 779.5524273434069, 780.7501101495419, 781.7880139750256, 782.1713312543684, 782.8677658837047, 784.0927987118156, 786.0265316263136, 786.248267015004, 786.5373774098017, 787.0801960034983, 787.6796579465471, 788.571647982673, 788.9617361429048, 789.5470055972321, 790.4228799055853, 791.6665038373598, 792.8132957390476, 794.34019524585, 794.7276769712129, 795.159538850883, 795.3082390856334, 795.611788684099, 795.8512297822355, 797.284006023878, 798.3012720475856, 798.7162794818429, 798.9067547737013, 800.3501785809894, 800.7700956347187, 802.8376551730468, 806.1389956208161, 806.3581316559685, 806.5092892294906, 806.6969564244374, 806.7617712571639, 808.3069796057767, 808.9920476693894, 809.4280744828269, 809.5130525966323, 811.275049793049, 811.4436091490458, 812.1199527660523, 812.6919273128731, 812.8593507140085, 813.4196114066455, 814.9909280646382, 815.5409345585164, 817.3188599336286, 818.9902775752128, 819.1179873684658, 819.5892553349781, 819.9356624380179, 820.1482536673371, 820.9563918718053, 821.9143870101545, 822.7233599889236, 823.5456536405651, 826.4650524910154, 827.7260391942206, 827.7709941641153, 831.4371381873264, 831.4862959983243, 834.2974259978661, 836.2022389470546, 837.9573108825414, 838.4783037326041, 839.3961875816416, 839.5751826443743, 839.9329192256021, 840.0163449454476, 840.0487916503264, 840.5587976937252, 841.190403648205, 841.6098004810407, 841.8755781558319, 843.4836740202475, 844.0040313482151, 844.3235925990319, 845.3668527577571, 846.5064252319777, 847.2854540271993, 847.5815977188461, 848.4252216318653, 849.1463033870589, 849.7042020389807, 849.9178785897819, 850.2782032207064, 851.3077996033526, 852.3210575541385, 852.996774218654, 855.8396642055304, 856.395653102387, 857.7417300334906, 858.2923169515374, 858.2997800084548, 859.066465335135, 860.1283162250361, 860.568899221588, 860.979039117796, 864.3185237246688, 864.589702565606, 864.8946076548074, 865.1290606115675, 866.798809928993, 869.6870527951826, 870.6878801284098, 871.964645346542, 872.5472626324273, 874.8685715109067, 875.496143465026, 875.9468912697907, 876.1798466516976, 876.2436297480335, 876.5786965776388, 876.9956214183034, 877.5973231372096, 877.8653902538568, 878.0537836625061, 878.3312817710555, 879.3154484189989, 880.7614879834426, 882.0684786044494, 882.4379453118923, 882.8641673532413, 883.7809124223115, 883.8247844221411, 884.0250140575268, 884.4496364789101, 884.9192270507112, 885.3859059514747, 887.0656511657653, 887.6218383861067, 888.089312361411, 888.2918259282552, 888.3360299966803, 888.736937892446, 889.3238036297707, 889.7178375134985, 890.0716666459707, 890.9043979061123, 891.2207837941531, 892.1606748573632, 892.72005283491, 893.6719154228822, 894.330362246463, 896.5771571709009, 897.6449079051841, 900.2416424091309, 900.604925668945, 901.6352475019062, 902.0527877839148, 902.865330257192, 903.4422444436251, 904.1329550007325, 904.4359087214006, 904.4456829089962, 905.2118138868683, 905.6679057354211, 908.178790903529, 910.0995082702807, 913.6354556898552, 914.2868682633524, 914.6625646825688, 916.9945600007453, 917.6054201317218, 917.97372328239, 918.1294261610896, 919.1625981395923, 919.8234837993734, 919.8534118205698, 920.173344971596, 920.4660964460568, 921.6930447050162, 923.2322564266663, 923.4877068522983, 924.4712311334612, 924.7532436542073, 925.4317209992657, 926.6802561538325, 927.8799502091101, 927.9295812444661, 928.3164079791176, 928.6642576744551, 928.6949524192308, 928.7109338886413, 931.3911771147523, 931.5055376877707, 934.2829983488366, 935.3163624492694, 935.4728269887195, 936.8444826191856, 937.3025029331604, 938.7116015589498, 940.8592728724809, 942.0258394907743, 943.5567754291934, 944.1650636293255, 944.7934151373414, 946.6448142835677, 947.713382344738, 948.2892794100221, 948.5531956718173, 950.2720805971755, 952.29846055656, 952.3689145955525, 952.5427796418996, 953.3910845522372, 956.0202658329711, 956.338724486195, 957.3735245920217, 957.7339096161604, 960.1180605370075, 961.312969831961, 961.503253107624, 962.1750795252589, 965.1448720181497, 965.1977159255804, 965.7315817565025, 966.0573065038562, 966.0972199747075, 966.7791267880427]


    
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

