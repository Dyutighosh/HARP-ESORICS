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

    min_val_1 = 1036.7924815238125     #min(X1)
    max_val_1 = 9989.980278468911     #max(X1)


    X111111_1 = [1042.0499750997237, 1042.716518425699, 1055.6129354051848, 1061.6464090591853, 1070.184222619446, 1074.5604107423806, 1134.2785289579315, 1134.9927323453906, 1141.883410093307, 1150.7825990254516, 1152.146411239277, 1152.7442751584551, 1152.7970459172059, 1164.1482421642559, 1165.467972475432, 1166.1557530748898, 1186.1968136772498, 1191.1682662376843, 1201.4910529256138, 1206.161685940308, 1208.557552275978, 1212.9656164169885, 1235.0815781504748, 1248.679438134358, 1251.477187782571, 1265.943010624199, 1266.3830566526876, 1274.511624280457, 1274.7268176090993, 1276.7936249465067, 1277.8162407403438, 1278.0361548579783, 1289.1258788128682, 1294.9175423933457, 1296.1064085801422, 1338.3989402579805, 1357.1814537231744, 1370.9125386344351, 1376.7638086622483, 1387.9225074480328, 1392.4772402418328, 1393.3783378863423, 1397.8931351883705, 1404.820647822969, 1421.6872333899296, 1423.579649496401, 1431.2344267898382, 1453.7316583203446, 1466.1598948972412, 1475.0599862489298, 1495.4039946389848, 1500.864707987807, 1518.9529967760607, 1523.1972750183368, 1528.3508248360524, 1543.97130232642, 1549.0775718762616, 1552.6396751226534, 1559.3019700215564, 1560.9876052677307, 1571.530532963235, 1579.154592933136, 1581.8769607004265, 1583.9874773285305, 1593.606948687531, 1595.144049797901, 1600.747093443065, 1602.8104426256878, 1614.0167121612187, 1615.6229670139064, 1615.8721048562693, 1623.6392688680762, 1625.3108823831585, 1635.5234005130128, 1643.0127578435254, 1644.2883532313185, 1663.1086834483704, 1685.030084019781, 1703.264374645103, 1733.4311937982725, 1747.4723551328661, 1756.986760633831, 1758.434416815925, 1783.2475835813734, 1784.780475329194, 1786.4633422547563, 1790.3490412633137, 1803.7923821196434, 1804.170020524929, 1815.7194904126945, 1817.4312734240536, 1831.9145081975503, 1840.975540521143, 1847.0376254126925, 1847.6922176364412, 1853.295750407895, 1867.9569536033177, 1883.3785258671498, 1892.9509183346995, 1917.9695742740048, 1919.4197707314815, 1919.8810887879781, 1923.448522792036, 1924.89150145893, 1932.5789692498977, 1945.3538880681706, 1970.883826757061, 1974.906384303728, 1976.5588973287913, 1978.6906740810946, 1985.7702027092016, 1992.463939422968, 1994.7362610208547, 1995.54733670022, 1996.1340309222533, 2030.0451738041625, 2033.7886007428192, 2049.556413348866, 2057.5548567102105, 2070.0469450960018, 2080.260902600431, 2084.1560163288814, 2086.4326382522977, 2108.9464205667755, 2117.8755642206884, 2131.0916736932413, 2138.6352152032314, 2140.4820116209253, 2142.516795382409, 2150.8834753182564, 2156.938349129775, 2166.1350880145096, 2176.5709674018462, 2200.2196453968404, 2215.171160107137, 2216.2815643282406, 2216.873213819272, 2233.63195608597, 2235.340243207347, 2244.695561929386, 2256.440636442349, 2259.2067110853127, 2264.920238781485, 2270.1011924833592, 2287.8919856830244, 2307.898837029957, 2311.890361118273, 2313.533311985847, 2329.8666172115745, 2355.3176334785903, 2355.981033541463, 2358.1161822873382, 2370.2036205331533, 2370.938014710264, 2385.530712782212, 2401.3675214897585, 2428.1321250471, 2439.7676085396793, 2442.2645793486063, 2459.1884022734257, 2468.522198944898, 2476.458810494374, 2479.7413630952005, 2516.2646424535214, 2530.479538755965, 2530.525491650081, 2546.614739822052, 2550.8454192338977, 2609.2653603986355, 2609.915067423085, 2612.6587142550306, 2616.1179630847937, 2662.78939972249, 2665.1574823679252, 2672.922017010471, 2691.299431942392, 2693.2860431625327, 2694.9826485896206, 2696.6900155935145, 2705.1678890331264, 2711.5187002244998, 2728.1384837709725, 2737.7770865185366, 2773.018449981691, 2779.227771977199, 2795.2780875301346, 2795.982933728894, 2808.2108932512915, 2824.578421548924, 2831.860731930088, 2834.96363523451, 2838.4880256146093, 2847.3995017270954, 2850.1810517494746, 2866.347198976792, 2883.3234703731932, 2886.4145618593534, 2886.435439617595, 2891.702394272902, 2893.3096798743886, 2893.4205188256724, 2894.335934629248, 2903.8706023390914, 2920.9132968889953, 2921.2807076527456, 2923.6912552221256, 2925.473398976189, 2935.315893093907, 2970.4092185011405, 2973.7064304516334, 2978.863753352896, 2980.751022042793, 2986.8696077680415, 3011.943010519901, 3012.934698304399, 3015.3977431285794, 3030.7996863515564, 3033.109673304769, 3040.1255305884124, 3042.4860616264214, 3050.066477873982, 3055.079181809131, 3059.734769385449, 3065.3596617216135, 3069.955401822178, 3072.693675227646, 3073.9419023374912, 3074.8800651813644, 3080.892256005864, 3096.9994466699145, 3106.345589427945, 3115.443805293993, 3115.8767219563997, 3125.6593404344753, 3141.9652261364113, 3156.012983982669, 3175.5144214968823, 3182.2893437821263, 3203.4012626915805, 3207.500861080778, 3210.0001069265095, 3213.004231232302, 3221.8310188767655, 3224.1209357270677, 3224.790244839091, 3249.6645659018773, 3250.9995825972783, 3270.0609072923294, 3276.2134269769404, 3278.8387627252114, 3280.3991502350564, 3301.945600236751, 3303.76993674368, 3313.4798591774647, 3324.9322874995714, 3343.422838890564, 3382.3917382156455, 3399.544222761173, 3412.0603258721553, 3420.730488492803, 3426.2368000827173, 3434.161711497407, 3438.2873957285187, 3442.012434643258, 3451.700745618321, 3453.481349405102, 3459.94491372577, 3462.4811075817706, 3470.0955864470807, 3477.8031546408174, 3485.5343451888275, 3491.5420026483125, 3507.634369677578, 3509.5747982033486, 3518.6895617192545, 3519.445301811002, 3526.865558942828, 3535.8477602025187, 3565.9025757640848, 3597.5635417668477, 3605.86625336165, 3607.8424189477064, 3610.215378448283, 3621.9676639206536, 3629.9864334916997, 3647.881700972319, 3651.3660674275457, 3658.250424934084, 3671.5581348275678, 3703.035202558943, 3731.7277439350287, 3732.5296209140474, 3733.008457331222, 3735.900725432741, 3747.5708036661754, 3748.8044238345865, 3752.229993505362, 3768.2285125640674, 3775.8793899508196, 3778.999249680229, 3783.7370201969397, 3795.774047027364, 3803.2924971151833, 3809.9150312191864, 3813.400199298898, 3821.581096586143, 3827.1167976131433, 3842.283943847326, 3846.106843080735, 3859.9946016115487, 3868.3906046244592, 3876.5533850820843, 3884.4065490044345, 3891.4256831438724, 3898.3580211229396, 3900.86985412616, 3905.189889347894, 3935.1248884313127, 3946.9711131359386, 3946.9788676410385, 3956.0601997079375, 3962.1175880488317, 3989.6639662208636, 4005.762905612108, 4010.8870629386693, 4024.507672482154, 4024.5248827136247, 4025.4529683915443, 4026.191304740745, 4030.3622496067073, 4060.169893162649, 4066.559114794501, 4073.9136720051038, 4074.1734179588584, 4076.249508042025, 4083.9298556119597, 4097.769937715877, 4112.272694756744, 4117.905710891604, 4120.899695865931, 4128.225841834543, 4133.312127364254, 4134.216620919089, 4139.95335862405, 4142.862493941973, 4145.0475924285965, 4153.156171466859, 4154.71355700532, 4158.051133039833, 4170.696879065301, 4177.479281964794, 4180.4415044013385, 4180.654429497492, 4186.099374643296, 4187.858492425194, 4215.105661197059, 4216.595009980143, 4224.469327675568, 4229.4742769502955, 4249.503271388094, 4271.260047602793, 4272.013540107988, 4272.3589423020985, 4277.926439725541, 4288.8491966040065, 4288.874261328274, 4326.738930820699, 4337.233285209781, 4348.917917575684, 4365.011301548431, 4380.019339565442, 4403.7428371348815, 4423.326076715335, 4433.355114785614, 4434.632919795533, 4436.332182325692, 4437.006698531412, 4443.833841024129, 4446.638052008962, 4448.6352970606595, 4455.240148915675, 4455.323131069252, 4467.984751696084, 4490.193050797416, 4506.20795488908, 4506.50862604345, 4549.749352942697, 4557.8164657464895, 4559.365325160152, 4560.235947859907, 4572.931067481762, 4579.978579978324, 4583.045527426858, 4590.663671744436, 4592.59530109622, 4593.620303227375, 4620.57384587975, 4648.718364171393, 4659.062719017026, 4667.547172907529, 4676.091684666704, 4689.49288919354, 4701.990308356288, 4704.547076210315, 4711.50004420825, 4714.6380992724335, 4716.4394458608, 4737.475211669075, 4758.875428182615, 4760.309116265832, 4762.354069182573, 4771.291076790028, 4782.929382257128, 4812.512524138623, 4839.982949801115, 4848.220689199852, 4863.404299044201, 4879.7502271020785, 4892.223554638382, 4909.949307182356, 4914.853129522527, 4920.26241175177, 4930.926213331491, 4942.395553840878, 4946.956307761323, 4963.606344384372, 4973.664567996412, 4974.7175691668, 4984.083073672635, 4989.7788372239675, 5004.20208133788, 5027.192858243694, 5031.880139106823, 5034.811499595883, 5039.206474831342, 5045.852036574406, 5057.8780571766365, 5063.474229905327, 5083.973823169368, 5087.409240287308, 5089.579608986199, 5111.095642932594, 5120.891236919136, 5145.358198555696, 5179.128224535438, 5180.431903017974, 5188.73709006607, 5195.834519881913, 5205.002646878782, 5207.709021373012, 5240.479023808464, 5248.391404879701, 5249.0243919290315, 5252.494614034369, 5272.682439400574, 5277.251718512807, 5280.388496264137, 5292.265463931433, 5294.47759070567, 5301.515460178291, 5302.933725295521, 5305.351502978998, 5319.016109540749, 5320.069809425628, 5327.897399745134, 5335.272311706223, 5343.567142763739, 5352.407469956948, 5354.994983878461, 5383.062502692992, 5384.788655872575, 5387.398097433059, 5397.860674469601, 5404.674138670271, 5413.651782678768, 5418.864735561678, 5438.7885304274605, 5448.484105747524, 5450.652143758556, 5456.4895532892915, 5457.887046756783, 5472.560168865695, 5479.740612803709, 5487.60174068113, 5501.950314938846, 5503.458990433257, 5512.945984211565, 5517.4370062378675, 5518.582366901395, 5530.110632903317, 5538.739606146579, 5546.54379637441, 5549.454048341237, 5562.816888316069, 5616.7184268580895, 5626.441409335364, 5627.102646870555, 5628.494639377064, 5640.905710476249, 5652.021826227057, 5672.553217806419, 5689.041569060395, 5700.4285147444425, 5716.373076102387, 5717.219909350291, 5734.654462846103, 5745.699985001913, 5747.434796472715, 5747.501205304525, 5748.452607158524, 5752.281156190122, 5752.355385991492, 5762.903182496499, 5766.2325027136485, 5780.748819392611, 5801.898737400315, 5809.9075562748985, 5830.26392098342, 5831.31403259065, 5834.009487806625, 5845.41163862658, 5847.116857630019, 5847.155302862222, 5865.627175254605, 5868.455241004896, 5871.669298029055, 5891.627690391693, 5903.945885451192, 5905.6464092950755, 5913.0084307081415, 5914.043613531367, 5920.636309775324, 5924.248396887055, 5928.275690957924, 5938.740453706168, 5941.0715251449055, 5950.475948214846, 5953.127546043097, 5964.038507896852, 5966.4001673171115, 5974.481744276858, 5976.1838658334855, 5978.556944144988, 5982.430518470279, 5986.114462553427, 5994.148833020017, 6001.48556393282, 6022.839567754501, 6025.917426920641, 6029.471449961866, 6036.378198315882, 6037.961675237382, 6055.503383019513, 6059.45153375187, 6062.260446590228, 6063.012387195282, 6068.636624485325, 6080.957798180159, 6096.065297615003, 6103.1588648281395, 6158.10166827502, 6158.806987776457, 6163.374795938815, 6164.440125537829, 6167.474646717086, 6176.972182848567, 6177.884198749713, 6181.048700294001, 6183.117418384525, 6186.030926268506, 6188.451246345261, 6198.074080432507, 6210.820842199941, 6232.793266927643, 6234.172075412938, 6244.176570003057, 6245.818988248269, 6267.907852529277, 6269.521024848558, 6275.846581949061, 6287.168628621754, 6308.320583841969, 6313.602459091217, 6323.23482980538, 6327.283609812459, 6329.562317897964, 6354.343704291943, 6359.313616926289, 6363.091491898127, 6374.955512323444, 6381.837962214306, 6393.44395480907, 6401.184123413304, 6404.049293013728, 6406.726458027251, 6411.730624069918, 6415.076832681112, 6420.965523116745, 6441.208932088652, 6446.753299753027, 6447.055891005744, 6459.781637985712, 6464.000725311747, 6466.851933261296, 6468.6894783812095, 6473.832241611739, 6478.501923014717, 6505.151471362709, 6507.538275940507, 6511.547064850758, 6514.84698031844, 6524.475868542102, 6555.83575135832, 6558.375454540133, 6560.512839332869, 6560.562966237227, 6563.412766744594, 6568.208844729388, 6569.754062665967, 6575.245072258747, 6586.386469793786, 6625.55887590647, 6634.7696532080445, 6649.95984670992, 6653.24814806376, 6653.71799957244, 6671.058682954183, 6691.43633435552, 6691.731074822903, 6696.906210531057, 6728.1742582330135, 6743.256638722238, 6747.023586168198, 6748.208712137477, 6762.81170455336, 6779.47076112524, 6809.794549605394, 6812.0925487343375, 6819.5871810590925, 6836.767942566734, 6837.132372472413, 6860.525927364566, 6868.694962058797, 6871.813694817778, 6876.758723591209, 6879.478156672161, 6882.134186972031, 6895.129945246708, 6902.7501747809965, 6918.67921356298, 6920.904333475735, 6922.508107049322, 6939.394241715894, 6940.390675540624, 6954.695321072053, 6958.167034383821, 6985.918938735902, 6995.168480619659, 7006.977134548226, 7011.536523269238, 7020.083877801697, 7034.1110533199735, 7042.0861459493335, 7056.636023857904, 7067.427066404429, 7069.042613033518, 7080.042208499506, 7082.51481756539, 7088.28899225607, 7092.627481094049, 7100.843956451108, 7103.079439245959, 7106.39409167074, 7109.279459828915, 7122.578734862802, 7142.5714508422025, 7148.394457605404, 7150.255109086635, 7150.345336255619, 7151.319798445878, 7151.936515462203, 7153.141726066031, 7164.1230813313705, 7164.826690770944, 7180.873463330321, 7182.331654924825, 7184.1639935346775, 7201.947096651704, 7209.88055252813, 7221.613379630822, 7226.985050586523, 7230.679374662694, 7269.086748375063, 7299.559584693367, 7305.066040781163, 7309.08164887879, 7309.225899795505, 7322.959657018455, 7331.782269660913, 7348.517268535063, 7358.053591483735, 7369.039985490745, 7383.371435947523, 7385.965704046086, 7386.860565483166, 7396.377762082055, 7414.677777224286, 7415.020294440157, 7426.0816624760755, 7446.645942181911, 7454.563279588339, 7471.318000418483, 7475.098714701917, 7476.8872443741475, 7484.5488076340735, 7493.010510705935, 7518.463400144499, 7520.0854648245295, 7531.863458588681, 7562.579782329516, 7566.197308000001, 7582.66948200526, 7591.320275623953, 7598.397120847316, 7600.409255174858, 7629.47135839383, 7647.380409435516, 7647.868618669483, 7653.0491189346085, 7653.66951659587, 7656.483477999327, 7660.468237186284, 7679.406191915208, 7696.604830786968, 7697.693904591606, 7697.930761647727, 7698.563436710683, 7699.585273182016, 7701.368779540038, 7708.2253976759985, 7715.856816992182, 7719.396048858587, 7719.606459758723, 7729.393833224696, 7761.071442821465, 7779.168543705999, 7793.801405030195, 7803.776403097365, 7805.451743183674, 7815.2553070567665, 7816.466094932088, 7821.51382339068, 7824.9393784773365, 7825.25105632771, 7828.328382269372, 7831.581998655407, 7845.384954687641, 7875.756571354965, 7875.893446909957, 7876.115091193735, 7895.951205601539, 7910.440643634252, 7910.4753983498085, 7911.806124114382, 7912.5624712849385, 7927.881115250573, 7961.928792151644, 7969.270628689877, 7974.509895894558, 7984.78435631805, 7999.133789730491, 8001.050929308974, 8025.838897784124, 8027.195649151785, 8046.842673408342, 8046.862371650299, 8047.448150074968, 8055.26964896412, 8064.201341432827, 8065.632846030403, 8072.02066309325, 8106.809128132314, 8111.882550966795, 8117.410543061504, 8123.333041522792, 8124.475432965888, 8144.459308443093, 8183.789355848241, 8200.587513741842, 8206.239571590393, 8216.333013957516, 8229.774081833648, 8230.90082585335, 8268.892693017822, 8274.838606302465, 8276.423030794427, 8277.337277671562, 8300.86694316964, 8305.648453848533, 8310.78481776063, 8313.817814970376, 8329.353457946625, 8332.827709891766, 8337.870813483041, 8343.51685738473, 8344.57886695412, 8353.413452419209, 8354.038870615937, 8369.118831052596, 8384.963161887039, 8385.661008788647, 8394.520058180648, 8406.207034154526, 8417.687055769755, 8418.969491922731, 8432.509399871795, 8465.954220787693, 8484.462655982263, 8499.448635302022, 8502.782243988271, 8503.360145722885, 8509.886878966234, 8510.677027456211, 8560.129159250173, 8562.715202217425, 8578.447134603062, 8580.443408758481, 8609.91960934589, 8614.181194168967, 8648.784703827876, 8652.678626891793, 8663.873076180165, 8664.07756232529, 8665.666672735464, 8669.311312799658, 8702.183336872129, 8710.877822433935, 8715.986448930225, 8718.462383970076, 8723.753067876221, 8724.567664708566, 8727.738588515016, 8736.926041103592, 8738.750246272579, 8756.490434118394, 8765.987438752614, 8771.830106352383, 8771.88622371229, 8777.608134744572, 8780.373959613544, 8790.66443251295, 8790.69618375974, 8810.114052505975, 8811.884893869808, 8826.260191284468, 8827.046339385826, 8832.644956686541, 8838.560323605314, 8849.928881718468, 8863.588037681357, 8869.865608299982, 8870.709044431147, 8876.907896265611, 8877.575420048364, 8884.527666275482, 8886.259042456693, 8900.904819028563, 8906.531915391608, 8909.526086148828, 8914.472007012508, 8932.919292265668, 8960.462465019173, 8976.61769211194, 8979.789530960606, 8981.62228613691, 8983.651981281599, 8989.054606895786, 8993.428999691878, 8994.985157403904, 8999.72449671106, 9005.680472632235, 9008.160547976739, 9015.46944233123, 9019.778388398776, 9059.579634568716, 9092.613968614294, 9094.065123549251, 9107.434148639568, 9111.051671442166, 9113.03156652325, 9116.55060333793, 9123.147607169196, 9141.866912870197, 9144.973417790274, 9145.520959309732, 9154.130451908888, 9169.364863793675, 9199.024918725007, 9200.607560990344, 9217.439991365836, 9218.215062384812, 9231.63320875758, 9234.268710154753, 9239.126306981534, 9253.304882322, 9268.689578267562, 9271.97655616314, 9291.732216017932, 9299.54938758413, 9305.959682178505, 9312.82951686671, 9317.038887423685, 9328.87445550071, 9342.980276259615, 9344.930658242709, 9349.28402078401, 9362.472004108224, 9364.62704921064, 9370.003255985166, 9387.725953169334, 9395.021933866887, 9398.755079275465, 9401.664864247025, 9401.730574754301, 9418.37005355364, 9424.014468679403, 9427.876918131848, 9440.719295872852, 9444.448469013683, 9450.376334580538, 9450.437404265984, 9457.58406660539, 9459.040506004863, 9461.296689330724, 9463.005157903304, 9463.052666040981, 9476.8727097131, 9485.949383101053, 9487.908859286117, 9505.89644625763, 9508.51673130959, 9514.201544158035, 9536.026885341731, 9550.889640387526, 9553.520267968257, 9565.303177829284, 9565.613469501894, 9575.090991043668, 9597.129696478674, 9597.221429871533, 9598.06283539263, 9611.553248972557, 9615.759249879884, 9625.217432639285, 9632.771305181888, 9656.748278077752, 9662.024159768396, 9684.008707572873, 9692.614402487026, 9695.511656002638, 9718.234406351115, 9730.39424633583, 9732.992843443426, 9748.252335427542, 9753.456445727259, 9753.563740724205, 9765.257111229419, 9770.313106336802, 9777.973629283617, 9782.84019607843, 9798.327501422424, 9808.635851628967, 9813.824361705249, 9824.353157629765, 9826.663374534843, 9833.8599510853, 9834.989000403744, 9846.34111236208, 9849.233009913292, 9864.204423363557, 9876.497130451808, 9881.337695423856, 9883.53316723503, 9886.551468890353, 9888.162461577844, 9890.883901031273, 9894.72642257642, 9907.945284514728, 9912.31999162643, 9913.620079278438, 9917.88803028915, 9928.241336678646, 9939.630029253365, 9942.01339973118, 9943.810403859694, 9944.658144033274, 9945.26359925259, 9975.256582575596, 9976.217923776005, 9984.073139809776]



    min_val_1 *= 0.95
    max_val_1 /= 0.95

    if(max_val_1 > 9999):
        max_val_1 = 9999


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

    X111111_1 = [1040.0984314091368, 1055.1229900337778, 1073.5076967845116, 1075.310273297247, 1085.872886178114, 1098.0873031354308, 1122.2563873433635, 1130.1718537292145, 1151.434764182638, 1152.5585784189175, 1163.8634867135925, 1170.5461588746039, 1196.1819697811447, 1215.1124008618108, 1216.3985724128363, 1232.2105555886262, 1245.8720452719829, 1250.3974129160224, 1251.378318332203, 1253.380659484509, 1253.5676016700852, 1259.2298820098301, 1260.3042318486032, 1261.073461788659, 1275.439463578187, 1294.3827566824448, 1302.815685964827, 1316.131148089507, 1319.6342494176788, 1327.915151120014, 1329.7035109903043, 1340.8324261760413, 1347.202454435267, 1358.544281028374, 1386.9412400514009, 1394.4077931949819, 1419.3183966748643, 1419.333386186707, 1448.5292771650152, 1471.8668376807238, 1490.9994401291262, 1492.1207198309894, 1497.5802251914567, 1508.6566475074378, 1509.0897493309042, 1511.1170736370507, 1527.244701889074, 1534.7658622249735, 1535.7030282620815, 1540.4853010835864, 1543.124029201319, 1546.6257763867166, 1583.1312726730405, 1608.321229068241, 1610.8970009169643, 1613.3416286804224, 1615.700164764151, 1617.6341653345157, 1630.4898564162454, 1631.4660659837782, 1635.535160106619, 1635.8951730646613, 1650.8813773385707, 1677.711355621898, 1688.2516186259697, 1694.9206354473172, 1727.8049923176582, 1736.0622458949695, 1737.445807792111, 1739.213857671917, 1739.8685638100062, 1744.7295895077364, 1747.731816192924, 1761.3797155171828, 1777.491204543292, 1782.2636908483596, 1785.8609763533839, 1809.67348268947, 1813.3104112834644, 1833.5363572388278, 1835.2136590927814, 1840.6702017842363, 1843.3432090375065, 1862.0315009270023, 1864.3991925380922, 1901.2919903052752, 1908.8035320668546, 1921.9641015193597, 1930.6905772354799, 1933.155603693628, 1933.7193029247069, 1941.1105477454362, 1941.872424090402, 1946.5236855196586, 1957.6050903684268, 1986.737502104915, 1994.932028014874, 1997.838594105213, 2002.730006335375, 2007.9529053746464, 2018.3514678657907, 2020.8695059675424, 2030.3730157940677, 2062.2610179201215, 2063.1129118863855, 2066.4535193481784, 2068.661742400017, 2087.7011256509595, 2104.6053075638015, 2122.5696646107845, 2127.548822429326, 2130.537251366067, 2139.7324587496837, 2148.1215188642323, 2149.017101699793, 2151.332363421644, 2159.460758764756, 2161.945384971207, 2172.612231654851, 2198.3746253225163, 2203.7782786228054, 2229.2933124300666, 2250.100620139982, 2253.2904166708267, 2260.3361551413445, 2262.8430650548316, 2271.176258904804, 2271.1902518173465, 2278.7642768828046, 2281.5351148219747, 2283.8129904673815, 2284.3824090380185, 2287.9163146242267, 2288.48386640907, 2289.354702412841, 2296.9077968706606, 2334.5660187184885, 2343.902820216946, 2346.4434076182615, 2361.3857937710654, 2371.517784642524, 2375.1286488127216, 2389.5749990392346, 2389.7483324041177, 2395.8325850431315, 2397.119418202842, 2401.1912539393243, 2409.3417309002043, 2412.2535039565146, 2417.4749706356606, 2454.969300004859, 2456.250088604511, 2457.3908214918733, 2462.0478633430653, 2464.014283749938, 2487.8948541490754, 2497.9584092971695, 2517.207969767783, 2526.4334619097963, 2528.2749851009708, 2532.2740908443943, 2542.4078134257543, 2543.220567275221, 2556.53668607663, 2568.05680154519, 2593.401436334734, 2595.990540110459, 2601.5918400638566, 2613.711457024274, 2614.1378687781275, 2614.521254305506, 2626.4863451047013, 2626.6669570062395, 2632.5197685668745, 2641.810982661837, 2651.317989839928, 2655.2686847240457, 2667.201625479136, 2668.749259248694, 2669.6128758310924, 2673.8448972027018, 2684.652864103575, 2689.1399129866786, 2704.3639394555667, 2712.7054300493037, 2723.4753872625656, 2766.133794894884, 2770.7400001006454, 2783.83358607253, 2785.0565634323602, 2786.9638090420126, 2799.48179091622, 2800.4298521511537, 2813.6828149518506, 2814.9340354553115, 2815.837671171589, 2823.3324410569303, 2826.353033956637, 2848.71565135651, 2855.4703896368783, 2882.076236569129, 2890.080971943975, 2892.2463716939446, 2898.3880196412947, 2909.54502892671, 2930.7020731823545, 2931.006048613159, 2948.858561255326, 2964.8558754301876, 2973.922112362343, 2984.9922161376326, 3008.47935707898, 3022.2498541365467, 3023.5011037830354, 3026.4183181778653, 3032.855589238515, 3042.6396962734943, 3044.11276297361, 3047.0582586655764, 3047.985601530257, 3054.6230808906607, 3062.8320131791597, 3071.854787299791, 3075.186965883584, 3084.272601790358, 3090.9356579229407, 3091.7704820537324, 3110.3353876753818, 3118.686652392096, 3123.1828797036474, 3128.5516158032665, 3131.72466735649, 3133.1984205054223, 3135.679950300754, 3161.050576809759, 3163.6742638317796, 3167.284220012761, 3197.7223305008033, 3201.336424520659, 3210.8788403189637, 3215.2627157982342, 3225.8974309452583, 3227.885212076263, 3231.012771638665, 3234.799081820868, 3245.0120474980667, 3257.1800090144434, 3269.2576803644524, 3291.132851167778, 3301.020493329465, 3301.554647547944, 3301.9394232734367, 3305.708132025156, 3313.704159118208, 3317.8573205758917, 3333.6003471678605, 3342.468067129039, 3347.880940848265, 3349.6423039084193, 3358.7076195583986, 3359.842349049995, 3361.758410810102, 3365.8066099598223, 3369.0753230263617, 3370.0223917792014, 3375.47162487912, 3392.114188653722, 3397.1572568391193, 3401.336228208235, 3406.106516335349, 3407.66689441998, 3410.772966713659, 3424.4999791754453, 3435.411916401075, 3455.500268752305, 3457.628297534029, 3468.9611116674373, 3473.287037307373, 3491.1476497317153, 3495.092763592743, 3500.3843402348, 3511.3586664709946, 3519.515458938653, 3522.421323132028, 3527.1321216399156, 3539.1685620785174, 3545.3389285024405, 3559.725940031017, 3563.830308376775, 3565.624560869572, 3570.088220636109, 3581.275245551197, 3590.8266819630985, 3595.5324235335984, 3614.59168960277, 3618.1278785286113, 3621.6321063371333, 3628.4531209949077, 3636.3597350193004, 3642.733782196028, 3646.8970284838597, 3649.647880949289, 3652.210411164091, 3653.4201206902803, 3655.900307684307, 3660.166508133082, 3662.190659470934, 3665.390195398813, 3665.7208785017733, 3673.339486712897, 3677.382733262942, 3698.5741920528467, 3703.144530112385, 3709.220897832396, 3750.7562091644045, 3779.332678577427, 3780.641968797066, 3781.3527559736035, 3789.099583712464, 3795.8197659328853, 3800.097849365697, 3800.1658300627355, 3806.3294616713547, 3808.7299084526844, 3811.610559716931, 3815.0021484995773, 3834.809947309017, 3846.5315792477127, 3855.3462643210714, 3868.539067031647, 3877.5331249229844, 3888.872125230987, 3895.6205145155436, 3909.44140561396, 3922.9590544995913, 3945.957032694167, 3947.6519969821047, 3959.062895322435, 3961.6927795293923, 3962.215320836231, 3972.0833096742567, 3988.6235722844394, 4006.4244530645315, 4013.352223464896, 4024.223417329962, 4034.3880363010007, 4046.09244764144, 4047.507291807942, 4056.21198748017, 4066.8923392346182, 4080.690933484209, 4084.242081510468, 4096.805516245446, 4100.384281832372, 4101.512656416029, 4109.9259702516665, 4110.219922273802, 4122.670168635351, 4130.685511094511, 4132.76404299071, 4136.48408831178, 4140.5042781227985, 4142.252061504349, 4157.636763312587, 4167.355746336031, 4180.622058701149, 4182.457000980718, 4182.7277988420265, 4183.014724455608, 4193.782119781814, 4196.15294845223, 4213.091534908852, 4222.011449819167, 4240.088241198919, 4246.611345404901, 4246.859318836235, 4266.4688140008875, 4273.7910183303175, 4281.610910066894, 4301.400853055037, 4305.290520326111, 4314.307470623011, 4314.481648423049, 4322.295407373255, 4327.348476763233, 4331.189519031832, 4351.810828514486, 4356.886431894911, 4373.47541233823, 4382.248330327281, 4383.670254581119, 4400.5461645179785, 4410.702859418858, 4417.302064621748, 4425.111885601406, 4437.728251595314, 4454.472448296283, 4454.974059176401, 4467.712728095851, 4467.825026608192, 4478.134330957535, 4498.223038044083, 4500.351389130237, 4508.438807515105, 4512.325549849477, 4541.65718023741, 4545.368075265554, 4545.762609148666, 4553.2750822831895, 4563.356856670677, 4576.276182398462, 4587.381652779652, 4596.004918648417, 4624.2380415304015, 4628.721754813757, 4630.286813878943, 4638.936775708429, 4642.365369440143, 4645.289850704137, 4651.618841256002, 4656.278552261825, 4662.545942841455, 4672.860175444355, 4675.879409480012, 4677.388565984395, 4692.0044001117785, 4693.523939121593, 4700.631854718535, 4706.99602365536, 4714.514898114336, 4732.390232149211, 4732.997845553805, 4737.265661187129, 4738.207628211139, 4773.812747923923, 4773.981533427461, 4797.065551791021, 4799.457330036479, 4817.687338127684, 4819.648702377848, 4823.718101103008, 4827.54489444809, 4838.407878979779, 4840.962201344373, 4859.523914061132, 4861.197297242186, 4869.594166200834, 4875.944872272743, 4882.6875038698945, 4896.252971411124, 4901.522302128906, 4906.730224786605, 4908.189873290321, 4909.005737894982, 4921.435710985195, 4934.920161689722, 4939.450589715177, 4958.638211997032, 4963.70063955517, 4988.5539508020265, 5010.390887534555, 5017.124095870693, 5044.591704463585, 5048.1906473106355, 5059.194504604844, 5068.757548830457, 5075.931218458186, 5081.357254682091, 5089.371206172167, 5115.541677643048, 5119.266254793522, 5151.233037365208, 5177.274526048022, 5177.312297755572, 5180.908657240398, 5204.104371932095, 5209.6624498094625, 5229.920001289094, 5232.449370089398, 5237.691157929285, 5241.422216166231, 5250.436177018, 5251.848742389175, 5256.629880974686, 5259.050988777617, 5265.267548266798, 5269.748088535289, 5290.500328865588, 5292.986652900861, 5294.86297564409, 5305.5601831607055, 5310.51456846455, 5326.0408210363275, 5327.60914186684, 5329.226962435439, 5334.886394564268, 5335.261317890898, 5338.176192299459, 5351.958046305956, 5364.256106841389, 5383.113893770636, 5383.458918410719, 5390.984147478466, 5391.265708092544, 5397.699391480794, 5428.039431755291, 5428.064130070854, 5430.612130226604, 5437.0167548163045, 5456.473922181212, 5459.5536543732, 5476.282930451307, 5480.020285528613, 5481.038461745053, 5508.427612538637, 5522.8040140179, 5531.373227958209, 5544.177234640598, 5546.95889995946, 5548.844107099367, 5562.089612217771, 5570.345017868747, 5578.051225609346, 5593.60512767633, 5599.455690952114, 5629.0692402955465, 5632.2039508397975, 5638.374067689761, 5644.778498910524, 5651.754352057385, 5660.318123951345, 5664.734853080077, 5670.931853811819, 5681.258226838239, 5685.201347421447, 5696.692343199858, 5699.995239794882, 5708.118947241523, 5720.198730006407, 5724.734906599993, 5724.980391604562, 5731.083133372058, 5735.259589386829, 5739.83347103881, 5750.776632938881, 5778.281971965158, 5785.225991734162, 5804.162549229968, 5811.273069629031, 5838.8403115130495, 5851.820484153679, 5854.9169361094155, 5869.485338835826, 5890.837735822433, 5907.544881684091, 5909.472037555339, 5917.911062901083, 5926.161368834279, 5936.696544339264, 5936.94118055382, 5963.320488412235, 5982.658114020331, 5993.8864794987, 5994.759773360825, 6039.071076771632, 6042.112033983227, 6045.639280593892, 6046.921225047285, 6048.23220362471, 6052.362102404864, 6062.5004892593915, 6067.8559110789465, 6069.725739326732, 6084.224635570987, 6110.283872727094, 6118.343151769586, 6123.036139790494, 6127.104574737054, 6143.898609191761, 6146.48266529636, 6159.092054203771, 6175.263277217804, 6179.748340787881, 6187.601173163899, 6188.820440208845, 6214.066528004618, 6214.445577821107, 6232.445973795, 6236.473701400731, 6237.746088734029, 6250.029950174059, 6265.348404344233, 6279.429740254422, 6282.737056520293, 6292.013568333525, 6302.379873555003, 6315.126292214642, 6316.077511978036, 6323.913698235421, 6324.944842442777, 6331.792647335891, 6344.176787764065, 6358.144386650414, 6371.012467131755, 6375.513207804466, 6401.283977539973, 6402.565771049458, 6403.72081960502, 6414.343104666461, 6423.0235983738585, 6438.924475278724, 6444.13369797522, 6449.927805750647, 6457.572659265406, 6465.874246665717, 6477.327584006942, 6495.631010550089, 6537.196695862132, 6539.022846318196, 6542.79760450237, 6543.418783035157, 6544.7404449561745, 6549.744750789678, 6551.608443688619, 6561.85430066811, 6562.706060038961, 6563.782503766128, 6593.008268228876, 6607.370575228289, 6607.612712475331, 6617.563712084679, 6619.404251385724, 6622.954867422586, 6628.133354103686, 6650.889885718772, 6654.8419645240465, 6667.374115495686, 6667.528860863675, 6676.151240233039, 6695.549620174965, 6698.707418872427, 6709.5171608287, 6719.356664077917, 6726.36281816319, 6728.155446600742, 6729.027728394376, 6738.351333133907, 6752.389636178601, 6767.45469107819, 6778.524369141465, 6799.7085970266035, 6803.80730819581, 6820.169402141253, 6832.232416862009, 6838.370761894041, 6839.303108285203, 6840.917296234416, 6843.863375021128, 6846.3756188165335, 6852.160406665189, 6858.417838042533, 6859.57792886368, 6871.825346642596, 6878.85523691727, 6888.008677113912, 6893.750969835979, 6909.271690677802, 6909.35990139569, 6921.90588920492, 6932.7909916824465, 6940.489803792079, 6945.495621474, 6953.592322760398, 6960.450406432254, 6968.416748243622, 6977.787180284862, 6980.042353338569, 6980.759411593341, 6991.706610989617, 6997.126920713366, 6998.300524772601, 7020.093406560021, 7020.687131168868, 7022.600127158226, 7056.982928431335, 7058.490755390665, 7078.401581975924, 7081.118117351529, 7088.687242970509, 7095.035942035598, 7097.5309894886395, 7097.687385346528, 7109.822065242743, 7112.679594641855, 7113.975758052089, 7120.052905792765, 7121.184462101861, 7124.356467008878, 7126.849488751803, 7133.841689971749, 7139.373817971733, 7143.75821178896, 7143.804044984296, 7146.048091035316, 7147.8119030143225, 7155.9252439406755, 7178.93400008268, 7207.449780740286, 7217.0435292286, 7221.364439851404, 7222.506633137176, 7225.268145528595, 7247.274096963702, 7273.579748255594, 7274.0651261594685, 7275.839571439123, 7306.952217064101, 7314.182471271904, 7319.493575214947, 7334.36195518577, 7336.073395279429, 7339.455619288703, 7343.420867567098, 7354.967480760339, 7358.086515674497, 7365.8041177298055, 7369.850984041652, 7398.974842806498, 7405.76692095145, 7408.217041076969, 7408.568271231845, 7415.251399278286, 7422.515769239433, 7423.949856266599, 7430.3109913033, 7445.824126918331, 7448.125063769923, 7450.110110071859, 7460.801480121821, 7462.3760782267655, 7466.36456246687, 7487.9928653451025, 7509.550623121204, 7534.6337456651945, 7544.3395797019, 7556.747169152097, 7563.826069429782, 7574.5711142324835, 7577.255206838707, 7581.848641217415, 7599.097900199407, 7607.126171940534, 7622.75544308011, 7630.939558955777, 7634.7635590604, 7643.70739637101, 7666.741299771242, 7685.285223005287, 7693.780335900445, 7729.871767570186, 7739.425596833913, 7742.568584333387, 7751.75257768468, 7754.22637118929, 7768.611670272148, 7773.719922886807, 7781.208455579223, 7794.38927855827, 7819.029641999701, 7824.276250926527, 7829.745530465127, 7834.713966951587, 7881.794608672415, 7887.864876419271, 7888.576197408671, 7910.92442570512, 7912.078700381191, 7931.548351740006, 7931.591859572482, 7936.438957392842, 7938.172083533274, 7940.042759474012, 7941.168537692578, 7943.174459293448, 7957.3081327077525, 7957.777565979908, 7979.739666875626, 7997.372984427708, 8005.13404746215, 8006.985638318165, 8007.074785690298, 8021.145301052837, 8051.187372000193, 8062.176989943035, 8072.321842479469, 8075.49920804682, 8097.097468823229, 8099.677208061445, 8104.878569511817, 8115.022363966715, 8144.855062185294, 8159.801449257206, 8188.455148618948, 8189.483639214544, 8191.542220564497, 8199.19143946424, 8201.910803395444, 8204.427083352744, 8209.754855343928, 8213.406952648367, 8226.938447393315, 8248.731950506297, 8253.628008118469, 8258.462073819217, 8261.471951775668, 8267.908115689388, 8267.93588039916, 8272.391100419878, 8284.49381014437, 8289.654795871991, 8307.33932619437, 8340.793984519772, 8345.572386996122, 8350.454063243998, 8385.194670693261, 8400.466784295042, 8408.492432791636, 8408.70192074691, 8409.0364473763, 8411.721862944047, 8434.468659415566, 8455.474069899947, 8462.447860626708, 8465.34176945708, 8481.933661488827, 8482.185767753748, 8489.718890433325, 8495.36729491381, 8497.73184268686, 8501.24305030561, 8508.395588121213, 8510.037299371581, 8519.437511483724, 8561.967295508324, 8563.075989055897, 8574.621028253066, 8577.947680352687, 8600.915522413618, 8605.981981058972, 8613.391890531733, 8615.15960542437, 8616.864150679381, 8635.388647037458, 8644.689353981594, 8648.455666288875, 8658.194436308633, 8672.757137487239, 8688.677319541684, 8690.116656856633, 8691.864326232024, 8692.040499431625, 8705.183476876116, 8709.919121873612, 8710.155164704494, 8713.860618914867, 8714.483418766042, 8720.84152994458, 8726.158626580473, 8758.632275878761, 8771.338462095484, 8788.790087315409, 8789.06161784243, 8798.68195617845, 8798.721076410102, 8820.851296509964, 8822.306797926274, 8840.172377145575, 8845.316027260391, 8845.542616694645, 8858.51573027188, 8873.098032217407, 8884.577543595931, 8885.749292745955, 8893.135252647739, 8899.963082894905, 8902.096765857972, 8913.471713683535, 8915.917141141743, 8938.775299769726, 8940.660081448508, 8965.824982420003, 8967.960738806176, 8988.433769568634, 8990.50155489893, 8998.31402279324, 9004.748527403699, 9008.591280147424, 9014.932046649115, 9022.574894457937, 9028.46723683682, 9034.95804264586, 9037.871711116102, 9041.70665612987, 9066.115162965185, 9080.216673096873, 9083.28412830277, 9085.297715489161, 9092.863635039394, 9094.38867087556, 9096.354888483495, 9097.346838764955, 9099.536406661931, 9116.474095554604, 9116.676146995113, 9118.635983937189, 9119.761663642901, 9136.329122973595, 9146.926738391287, 9157.006404716685, 9163.868001826626, 9164.708509611974, 9172.987021438132, 9184.08258336728, 9186.323274169099, 9186.587182647792, 9188.798954303547, 9197.694051589722, 9213.174854908277, 9221.77571143158, 9233.107160262336, 9237.140058400139, 9242.962677785981, 9244.80413893036, 9245.786273143141, 9245.850029894926, 9258.493656375265, 9266.595933172364, 9272.46150263798, 9278.546385730306, 9293.25023668635, 9333.134403456255, 9337.782128997858, 9350.748422323228, 9361.927155773094, 9371.04982490031, 9385.587218076224, 9418.46423686015, 9419.536432299336, 9456.721696403536, 9469.647781201606, 9473.176576570302, 9478.628015773475, 9481.51046172789, 9505.984939430618, 9514.310077720946, 9525.332404199182, 9537.206241927208, 9539.45310750582, 9553.182218229365, 9554.374952590231, 9563.73881700425, 9570.99178681152, 9571.262846927568, 9584.373607435915, 9598.23554432523, 9598.31174048574, 9599.534170814473, 9602.77472424055, 9617.238475098606, 9626.95298232151, 9631.51238133778, 9657.675666363275, 9660.6432951225, 9676.257354058143, 9677.515315697043, 9708.325876740331, 9740.26720246853, 9746.341468987583, 9747.261931963092, 9762.372175262017, 9766.144147994984, 9767.999376291678, 9777.471885737368, 9817.669482234036, 9820.15281010726, 9825.995996291553, 9833.127692577167, 9843.412896440157, 9875.756475056376, 9880.3057068884, 9913.437689330345, 9925.187862810368, 9936.450418616214, 9936.522359675053, 9937.12282602146, 9949.643678839233, 9962.58697188077, 9972.407867314212, 9985.78857458664, 9988.290501403228]



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

    X111111_1 = [1040.2782525351356, 1048.2548107999287, 1049.854158679528, 1059.888671174875, 1080.1611264954115, 1089.7698570211442, 1091.1508534399313, 1092.7187300183407, 1097.537436352022, 1103.1760658155006, 1106.5666160008698, 1114.2080706000802, 1116.7939802990581, 1119.438961916843, 1125.1938769913518, 1151.256008503551, 1167.241245651981, 1179.9062124150705, 1182.0357693742292, 1196.392775185685, 1214.1419371601978, 1221.1313770626732, 1253.9232717050888, 1257.2544794730875, 1263.1158546362562, 1268.3778475773831, 1269.3019994156216, 1273.5698520238222, 1291.7688331042746, 1312.5161386149573, 1321.24019134254, 1321.4697013020786, 1345.205246949397, 1352.118585693091, 1365.6587727188748, 1398.4419673365865, 1399.5755751926383, 1400.4153899632456, 1406.069369772762, 1421.3007208260392, 1450.689271841579, 1459.1396348836752, 1464.477871647636, 1470.8220534514305, 1470.9435627084024, 1472.6290838577788, 1484.6868141656903, 1496.2280420890909, 1503.1701924431118, 1530.6028576720528, 1536.1436436827566, 1541.1027392180133, 1558.4503509744172, 1563.0168702320557, 1594.9781508608485, 1619.047066097065, 1626.0476539427223, 1636.5957099613645, 1657.0630434884806, 1677.907387876115, 1682.6901736352552, 1687.1864305312843, 1691.2246020145465, 1695.1482286491087, 1698.9138797599298, 1702.1991634422852, 1702.3419618456437, 1718.6660063290328, 1722.153255815825, 1740.844751956442, 1743.4648894504126, 1750.0065298722002, 1753.5920878474253, 1780.2901284572022, 1785.3453995066784, 1793.1286070695382, 1793.9210147986464, 1794.2916498320387, 1802.06162340993, 1802.2448838445043, 1803.550483484422, 1817.3560437502038, 1838.6343895754899, 1839.6605624293838, 1842.8407792793653, 1854.9284131673242, 1855.0475499513852, 1874.9578987529608, 1881.8503091480266, 1884.102765868629, 1886.6646192796827, 1890.1009731249405, 1894.4077207899022, 1894.6979963504173, 1898.416354552668, 1905.988825995895, 1906.0798493567781, 1925.0044801620447, 1925.9439508584085, 1943.825363466719, 1948.263338472129, 1971.9415159372925, 1990.6174089396509, 1996.7035432468713, 1998.1313479821506, 1999.9107902922378, 2038.4357073417134, 2052.071548774654, 2052.803381947944, 2059.501696870392, 2063.2026694780225, 2065.4583382880446, 2069.0875345122913, 2074.6193017525366, 2079.551050456864, 2083.758770532386, 2097.780124190843, 2101.096666570046, 2107.8525775378644, 2113.363071175466, 2123.492240998764, 2124.6198191242133, 2129.102487821855, 2146.939984561765, 2153.799013592704, 2155.6325968093724, 2169.443394183819, 2169.644728705919, 2171.7501312160794, 2171.827878598915, 2180.0552778667616, 2206.381395274865, 2213.248289845378, 2219.900694273877, 2221.366896858081, 2233.017140825146, 2233.516594391511, 2239.904908107513, 2246.563437985263, 2250.685007858726, 2262.2143641778594, 2262.827765462913, 2271.9203552981953, 2279.0253572680303, 2283.4434873054456, 2287.9192607429686, 2291.636455101653, 2299.498806506377, 2316.127717734524, 2322.6434538473914, 2327.2461510518783, 2353.2885475815356, 2375.635505657109, 2379.484958953387, 2396.4334044777684, 2417.182058185219, 2438.403745149227, 2443.1821411820856, 2444.33317093485, 2446.2549722869117, 2450.169590923093, 2458.7343544954883, 2491.809725826527, 2497.6645599730546, 2508.228163689966, 2535.753502810263, 2543.562825767853, 2569.2469790061214, 2570.9452711944514, 2573.1394467355585, 2577.7164136522315, 2599.136436958504, 2599.7139999148785, 2607.802532711462, 2620.2809224751422, 2620.4161676269377, 2626.223525558021, 2636.9325222771495, 2643.45378176388, 2656.644368749191, 2661.614219645514, 2671.905214118519, 2674.3901181892834, 2675.226162412445, 2685.4701332243894, 2690.2364912495705, 2696.6652413494135, 2708.106789829354, 2709.131934624861, 2715.619052571263, 2715.824270426283, 2746.0109297654403, 2759.777386720773, 2783.9094826207406, 2784.003285336861, 2787.829824510993, 2794.1126360799285, 2801.1840367806017, 2815.5354828031304, 2822.3276656374073, 2827.5174492807937, 2828.0302765097845, 2830.6357880974765, 2859.0996324170674, 2862.3827683904283, 2863.651489325908, 2878.090079966192, 2878.3681226500967, 2885.4460647989213, 2887.670660719593, 2889.3638152149774, 2893.4682707261577, 2903.2448733298124, 2928.3316266216743, 2940.8300653625565, 2947.9283804207835, 2954.844806348141, 2959.1856827280235, 2959.3540696288846, 2962.0728404394977, 2969.522822793828, 2977.6993688349585, 2980.537148359045, 2986.3308178264097, 2988.6629599056314, 3001.9260203358467, 3010.8202670422825, 3015.802747459992, 3023.183070240489, 3041.7983274029402, 3047.7922797620586, 3052.667279463133, 3061.7804627748264, 3068.5591639926092, 3080.0149747783116, 3111.288106802673, 3121.156773968948, 3122.035489392384, 3122.5965568127754, 3130.106826655543, 3149.1315631867406, 3156.3304694255903, 3172.222605923822, 3185.1252929179554, 3196.4516888137246, 3202.7293883188054, 3214.4223950400583, 3216.775869889022, 3242.1956796757286, 3253.741988994748, 3256.570420616396, 3267.5998308746407, 3281.911098066211, 3285.262971135633, 3296.6789850789664, 3296.9700693733375, 3316.4168655260446, 3317.091528567242, 3324.716489748808, 3330.2813889966815, 3360.7716667530353, 3368.564177823528, 3383.228960853867, 3385.2547568022837, 3387.997937156657, 3389.5670276298724, 3402.2338420770234, 3405.8431445779756, 3419.921045898109, 3420.848505096264, 3424.774495174048, 3426.9872825131733, 3430.1445650221094, 3447.6797295467604, 3469.598737260627, 3480.8781735404696, 3498.2739748341173, 3499.684677615157, 3500.548143734858, 3514.634654140989, 3514.851314649508, 3520.248592703836, 3521.040840680675, 3522.3275695818984, 3535.17015581215, 3536.113892215858, 3545.267299033791, 3546.3296856080037, 3551.2365249209124, 3552.183498596209, 3555.652479532586, 3567.0630029414765, 3571.4462721812847, 3572.9864013687516, 3573.8569671622513, 3575.5551111339114, 3584.8252863137473, 3603.483915831446, 3608.014371739496, 3615.4327239025697, 3624.7384877834634, 3637.680621256321, 3643.353650862106, 3652.0556591647937, 3653.3769946555394, 3672.946659464128, 3677.213999316828, 3689.7961808081263, 3696.793774860703, 3698.262106162703, 3706.3824741124895, 3710.2716436651776, 3718.1906155172683, 3728.420864116692, 3740.792652666265, 3758.508794607655, 3764.402177265904, 3789.216897054281, 3820.2665520576516, 3824.716203337367, 3829.5764431044763, 3831.031530753805, 3832.8600817999954, 3835.751922775294, 3843.7603460568243, 3868.2858975151207, 3874.028423784269, 3884.25039793768, 3885.213068468523, 3896.150105770733, 3898.2516815893, 3918.794274877527, 3921.6671696400604, 3925.132979358145, 3930.754583378163, 3932.8003774179238, 3950.915535780863, 3963.9441414190574, 3964.481929554441, 3975.6004316958565, 3980.8216961817193, 3985.4330143858447, 3992.3663614267152, 3994.086767593562, 4000.864764724871, 4002.0653373416653, 4012.4290533061585, 4029.005783805847, 4031.288280651932, 4034.4797744884954, 4036.6968246642505, 4045.672579568834, 4047.7955399517814, 4049.073755691418, 4054.0037294552267, 4061.6658841980957, 4064.052698872893, 4086.9523977605018, 4091.264678539975, 4098.7752706068095, 4110.278881372724, 4120.104781269591, 4124.97611106015, 4133.727611817514, 4141.904761574042, 4147.465320899106, 4147.84449904312, 4151.056656448101, 4151.064160752072, 4156.731012420496, 4158.561030743758, 4161.219460342338, 4162.729639068559, 4170.937635406834, 4174.785538040262, 4175.256978433402, 4206.850001126865, 4207.9016845043425, 4227.826423858231, 4241.619556466663, 4255.101756115919, 4261.342145068118, 4264.305453949694, 4271.904548794774, 4277.126410497919, 4292.924195318445, 4296.452087651409, 4304.045869657557, 4311.911732435051, 4318.156088386968, 4322.802092028822, 4344.608798295931, 4349.976536202013, 4351.019031310836, 4380.987541907029, 4383.18810630718, 4401.512928900608, 4421.994528710506, 4424.665677648558, 4428.318964424778, 4445.912073044528, 4453.049396189484, 4465.856391273344, 4550.9962739158245, 4573.3446388750135, 4580.1475593402265, 4583.3752819205065, 4585.958353358871, 4592.639718774712, 4599.692968799175, 4610.972391177194, 4615.079147018094, 4623.382667438127, 4628.648712191808, 4628.728964918426, 4644.363827043697, 4661.495734992155, 4665.018755811227, 4682.590270699535, 4711.714913102116, 4751.475525155876, 4767.311262618299, 4770.618803914576, 4770.732338737737, 4784.07827206815, 4787.688496677746, 4797.941887022405, 4802.275935618522, 4825.807440012204, 4837.9373383500515, 4853.84441940852, 4883.84798068816, 4894.462979921789, 4934.620436692534, 4958.272839783374, 4960.067590291783, 4974.175631912897, 4979.592802984654, 4986.1330497306935, 4992.379127441309, 5012.375024373288, 5017.360622366635, 5025.253528692903, 5035.550614503004, 5049.481619596859, 5054.696904782102, 5057.9442100381675, 5065.180960195465, 5065.379311860828, 5076.008204137546, 5079.772205716068, 5082.272689857482, 5082.752846627822, 5087.304180417264, 5089.7767372872995, 5107.597355201949, 5113.682489957644, 5115.873171427066, 5133.272841514208, 5156.797465086707, 5170.900453056116, 5176.842406509162, 5179.1219968452315, 5181.897773803055, 5182.39739298092, 5183.290850047782, 5197.165446427884, 5209.5736342427335, 5212.757500063784, 5213.685227881617, 5217.629255039954, 5242.038966510268, 5263.3062775464805, 5272.367797318007, 5279.031031013177, 5295.12439825935, 5299.316098462343, 5299.791726849344, 5310.56601334866, 5317.313465163505, 5318.586016591682, 5321.172225004671, 5323.389399219861, 5348.40172239355, 5357.14338369132, 5361.349387202223, 5367.770388655081, 5379.906629675741, 5380.419557807421, 5383.924973438319, 5390.828451680694, 5394.193601738194, 5395.315374475396, 5402.964042652462, 5405.773750226837, 5436.664215358314, 5445.759890991265, 5446.047964390893, 5450.167723432232, 5450.487033315316, 5450.775810163283, 5455.438284557869, 5457.279819330033, 5458.80934975192, 5480.81032983781, 5484.014494076819, 5492.466141709414, 5496.936506895487, 5503.490275241564, 5517.248320987159, 5522.307414506333, 5531.253067737085, 5532.034289719028, 5533.411408888967, 5534.659664513281, 5539.446663491581, 5566.020850598834, 5579.851243576864, 5580.499745826653, 5585.6871810733155, 5603.3891544825, 5603.754414024072, 5617.437044106795, 5620.809947514072, 5631.418429840109, 5641.808795344947, 5648.051316018833, 5649.040380971053, 5652.464393760145, 5673.724581510982, 5676.581765238043, 5681.001666308133, 5702.721769208103, 5705.898637005241, 5707.7472933627705, 5716.089046533651, 5718.998178695039, 5724.254040120062, 5726.677680718056, 5752.5710101368895, 5755.070738030383, 5760.682599724825, 5764.206240335901, 5764.234956773977, 5784.127906077561, 5787.752903558259, 5798.9134971706935, 5802.435506462383, 5807.851515180302, 5821.784419132055, 5847.669990760334, 5864.212653263727, 5867.319670581883, 5880.605675783376, 5882.548279441846, 5882.595146062136, 5907.03154233711, 5910.069781065406, 5912.72915737867, 5913.245656781659, 5916.613679205902, 5924.544754097831, 5928.259634137545, 5931.252585291768, 5940.81772725705, 5941.193083246366, 5951.53557921502, 5972.824331817528, 5972.894363996915, 5981.7828961678115, 5995.85685272561, 6004.274366787897, 6007.020762098995, 6023.430532286015, 6035.606643666295, 6036.4647586644205, 6044.070952735812, 6044.909217194354, 6045.000407240639, 6085.897223245043, 6086.588414854163, 6088.335268714314, 6097.251101356949, 6112.168588425742, 6124.109564456432, 6127.043074629664, 6136.18698502334, 6153.144512341563, 6156.177101468327, 6157.109580614302, 6159.45787261027, 6166.514364576618, 6187.742194336726, 6199.721688335112, 6205.685860434476, 6207.653795616174, 6208.91241038615, 6231.479682577439, 6240.2593001231, 6258.186374710276, 6264.553953322251, 6267.968994678353, 6272.083425922201, 6288.88324908188, 6304.440754458121, 6315.196999042571, 6320.60003497564, 6323.120913118839, 6337.144997130865, 6339.704268664882, 6355.981767199046, 6375.467898132934, 6395.525302858805, 6443.667495902395, 6445.38812720701, 6448.581887193361, 6454.163094080535, 6471.791142550714, 6482.524435359683, 6496.6243965978265, 6515.787797838375, 6517.057999814389, 6522.535278633739, 6523.416726216794, 6536.151057576553, 6538.791256226961, 6540.026845119806, 6558.5133677103695, 6568.634444038322, 6571.6339331319305, 6577.092505062041, 6580.509966088117, 6590.55053537512, 6597.466782321089, 6610.920361676104, 6612.826875881954, 6613.258111077306, 6615.699929603012, 6617.10380516252, 6623.060235840663, 6625.131692853352, 6640.156624901112, 6640.608562489244, 6641.538156053857, 6646.422891725131, 6658.208778130485, 6658.683880238861, 6662.261373706609, 6687.447255391706, 6701.4777131383635, 6714.378454884965, 6718.2917227756225, 6723.881993836661, 6738.752974453544, 6746.709918609073, 6756.995558006471, 6764.381129402562, 6773.302133202209, 6795.302399542621, 6831.487316965979, 6831.554292640038, 6841.99976634934, 6843.416230951887, 6847.356647012812, 6848.432398653711, 6850.768994083999, 6857.327615791275, 6876.4460796414005, 6892.989504678939, 6897.816625401849, 6920.151702356616, 6929.281954189853, 6929.4457313278435, 6930.139326532484, 6934.776285973847, 6981.822382528393, 6990.402774701712, 7002.146208873186, 7006.465670510726, 7016.401732707913, 7021.082013969408, 7035.702432704542, 7065.181590605234, 7073.048049501196, 7087.22115301144, 7091.036985379034, 7091.561460188521, 7098.251448704412, 7105.405465301652, 7107.556421924875, 7110.946299864074, 7118.247972004301, 7137.999130850905, 7153.579701421828, 7155.9872324351945, 7161.917184339123, 7176.622958986503, 7180.9758901970745, 7189.6275806128615, 7207.93903632436, 7256.121171363669, 7267.541115159353, 7272.750237182854, 7281.264112561052, 7300.954205660146, 7308.776422088262, 7320.091146552215, 7333.8119878145135, 7339.22170700813, 7350.080863080264, 7359.369114149287, 7359.8142162798595, 7362.006334117545, 7385.312875095295, 7387.666323637832, 7426.671300114029, 7429.821721407652, 7435.425587906042, 7437.436376840598, 7442.463872545717, 7445.675208186351, 7451.174910587219, 7452.770112558663, 7473.668454690469, 7485.268652715504, 7489.392191175646, 7509.444361053345, 7517.79937501024, 7519.752657293406, 7557.672245524815, 7561.357533870492, 7566.303311212267, 7572.5572163543, 7587.189534125044, 7606.324115565452, 7610.721578331319, 7614.808356621605, 7615.392681792517, 7636.568713584418, 7637.41911826781, 7655.3741307107175, 7656.497232088419, 7672.833226152621, 7685.495919356485, 7698.0735059986255, 7734.042600641176, 7743.867925042761, 7751.296885319796, 7766.870834388379, 7773.783594316654, 7774.372381506893, 7774.915602802041, 7786.421831066809, 7789.013357743837, 7798.033108566551, 7799.900385881996, 7800.927263566671, 7803.439657630048, 7809.807081257251, 7812.265393525811, 7829.528798535795, 7849.920482248941, 7850.19261731701, 7856.061234929728, 7857.1113223664015, 7875.7650509804935, 7875.82505868406, 7877.626846790663, 7888.685973773678, 7904.3902508774845, 7912.647324828093, 7915.958936351459, 7920.469130438612, 7933.708486283338, 7975.998700458918, 7977.687467386086, 7984.652692044023, 7984.980269604159, 7991.2287679314595, 8035.219203334062, 8036.893064934833, 8044.027419347605, 8051.888453063584, 8071.172110175583, 8078.846049691847, 8082.257051871615, 8115.337593235097, 8123.251156581495, 8128.34550778043, 8131.753142306228, 8133.884821157326, 8140.063066273176, 8155.034568244513, 8162.11307259004, 8169.0730385873485, 8170.479917503877, 8178.294126712226, 8188.918359632653, 8214.3563993934, 8244.292308065715, 8279.630994239853, 8298.83504814342, 8315.301496248121, 8319.47196555411, 8325.255843608926, 8336.03495344529, 8336.043733743742, 8339.83223176253, 8349.242479912846, 8365.035123550602, 8381.173739889804, 8383.040443517712, 8383.283503165005, 8386.91799861306, 8392.629802296517, 8428.616577464169, 8437.143009712247, 8443.246062605693, 8456.284605959238, 8490.984964768266, 8503.754076007424, 8520.637052408889, 8523.925197965975, 8545.590972856755, 8562.737410734864, 8577.99520215788, 8586.058726047962, 8588.90559484023, 8605.607359970956, 8610.325436601423, 8615.638419547884, 8638.57739468708, 8638.727173997868, 8673.283034608294, 8685.91863401974, 8688.416635912416, 8691.849072660747, 8701.637655546498, 8725.976011798708, 8746.335716277697, 8746.763422480562, 8748.982745836754, 8756.010792060926, 8759.70806821601, 8760.160773346463, 8769.471817042577, 8769.527560648798, 8792.525608823758, 8812.977378538842, 8817.369277852898, 8818.429651065757, 8819.708254486404, 8824.861918026563, 8852.731264798687, 8857.044749780625, 8861.846447966247, 8880.427954833494, 8880.634191086418, 8883.987708949851, 8888.76834948244, 8900.600722136185, 8903.76326084792, 8907.357893844022, 8914.173284273253, 8938.864685380699, 8942.790198230301, 8950.630620185975, 8951.590777059906, 8960.962725281324, 8969.469335636288, 8969.958433310383, 8980.494730049319, 8987.653825887248, 9002.187666568045, 9021.181310742651, 9035.964927669575, 9036.564509047821, 9049.678994014677, 9068.408970355407, 9070.281514496688, 9070.393997071704, 9087.000703146912, 9097.30843969482, 9109.824243648769, 9114.342866459072, 9156.099314394323, 9181.706092229493, 9186.541499179448, 9188.591709041482, 9197.130513465321, 9205.374945378, 9219.40171651925, 9230.75601765153, 9231.847148728892, 9240.420580250968, 9241.640785887244, 9248.23158450471, 9252.557471708398, 9253.02490221764, 9257.275226534512, 9262.158518814098, 9264.421356885974, 9270.002569944105, 9271.125349392445, 9276.38747353663, 9277.036382282691, 9289.572446234175, 9289.960801970348, 9290.272025806838, 9306.13383362177, 9316.439783598013, 9318.741331980713, 9323.331789504497, 9335.36453531302, 9360.231564336918, 9365.355505222433, 9371.81741440486, 9399.179271587262, 9404.599630319635, 9405.652813309094, 9419.807694570329, 9426.11876390293, 9431.083273901686, 9434.732385776488, 9438.917507514101, 9441.370337995624, 9466.82095872574, 9472.231240382442, 9478.231310950076, 9479.102739588156, 9487.620028635953, 9492.560609500735, 9516.748069094037, 9526.988379141176, 9531.87162109941, 9536.428156105872, 9540.041076216301, 9540.322727822519, 9540.58981968698, 9573.687940612404, 9581.336686061277, 9587.086590896279, 9607.493669628688, 9609.584137982518, 9613.513700311421, 9620.232534961184, 9621.762845973994, 9624.518919720587, 9639.015617889596, 9651.867128127562, 9664.042535740706, 9664.60964041357, 9664.919292178927, 9664.932608052977, 9666.350357235353, 9668.905547095483, 9676.75403351385, 9680.459819238373, 9689.955037592488, 9698.401116396299, 9721.553359042286, 9727.08862315833, 9742.543283987676, 9743.560069178036, 9753.09678575655, 9754.771695447293, 9760.326180057198, 9761.532536522578, 9765.015764402662, 9772.256659609491, 9786.445749743172, 9795.395293151283, 9799.412356513545, 9800.683412172693, 9806.684533248674, 9811.698490235287, 9813.872775125421, 9830.173194087994, 9831.28905636041, 9834.814822986806, 9841.719604403734, 9842.698129791412, 9844.01786459742, 9849.879614376143, 9850.771765534788, 9854.167249783633, 9862.31306910281, 9865.952478940622, 9883.866613785907, 9886.257437328642, 9889.50267171745, 9893.950845396377, 9917.737716326037, 9920.321068093697, 9945.620512277783, 9952.062996758648, 9959.25076997264, 9963.066946349241, 9971.035097763895, 9972.268433542395]

    
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

    for i in range(10):
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

