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

    min_val_1 = 5711.808714232062    #min(X1)
    max_val_1 = 30233.97850331777      #max(X1)


    X111111_1 = [5733.266506823356, 5779.560980172855, 5826.213808214923, 5832.301422613129, 5864.238136409311, 5865.929954792388, 5971.268227321416, 5978.712183765587, 5986.111107430407, 6002.784492634838, 6019.0949975513995, 6031.159669439344, 6040.774345178697, 6041.742296239707, 6105.479457862508, 6127.753999165231, 6164.378348807036, 6165.299197518139, 6180.662625146966, 6206.192903756057, 6215.460614873636, 6232.851882478362, 6255.948374938313, 6258.917515694736, 6295.735976488649, 6343.687629098397, 6358.7269489321125, 6369.254351162378, 6396.6671697336715, 6442.006435250921, 6487.364078368071, 6537.15445212714, 6558.785180221328, 6574.556244303618, 6602.516563752868, 6611.439471069035, 6612.891230394752, 6622.022888855863, 6637.605205224383, 6649.935258870004, 6681.083315953561, 6831.45052177355, 6835.802076532005, 6851.904394662509, 6862.294190076326, 6900.587590838342, 6908.382222436514, 6967.000281208175, 7013.379313316777, 7047.5677057121275, 7059.875814327412, 7064.009163593136, 7069.215699069681, 7110.036346758142, 7120.211306089316, 7135.236552918466, 7239.8979936256965, 7241.515174241493, 7252.39298120049, 7254.6255757564795, 7338.9649615547005, 7382.407782216327, 7420.259525374431, 7451.000109820525, 7477.765679800661, 7484.615323974216, 7487.082200737381, 7503.4857858112855, 7508.632064187393, 7512.845858055447, 7515.388262724564, 7516.207473319604, 7536.4411207990415, 7571.3891938442885, 7571.901517282871, 7587.72340665547, 7588.928385561715, 7602.233532816241, 7680.960869877984, 7693.978366642361, 7719.6176584162295, 7726.958473863094, 7727.986522013133, 7782.361425935094, 7787.497910092035, 7804.669684760218, 7823.397395618158, 7866.945181631019, 7877.775328904975, 7882.694857177166, 7883.490766651119, 7899.163762903386, 7920.234591699542, 7976.127249408303, 7982.534915522632, 7987.385710488902, 7990.035672678676, 8029.2655681506185, 8059.804089488641, 8150.26739372458, 8178.14182698582, 8180.62079594803, 8195.906457669978, 8227.364150021485, 8227.676376130163, 8264.89614268345, 8277.840946084303, 8340.311565530144, 8359.967448202462, 8363.430947893534, 8365.583423283788, 8368.039293729194, 8378.112186104518, 8412.999410379549, 8439.26988994866, 8445.104627108747, 8447.444509559204, 8470.15015055707, 8470.570088434228, 8485.112625722593, 8523.08091749714, 8532.286027961134, 8544.91465785122, 8569.468953258101, 8569.745423005248, 8590.769607758, 8599.885883053557, 8654.45347376142, 8663.745861633639, 8728.838345467298, 8750.465937447458, 8769.725281777537, 8771.764885063472, 8780.310111077462, 8796.668598299562, 8849.957176803107, 8855.445005916585, 8859.555341005269, 8870.717458582787, 8890.252926983192, 8906.55251770703, 8912.471078601606, 8934.5634687011, 8997.934966333607, 9006.681237880739, 9006.834332546674, 9153.098895431265, 9156.0742663114, 9175.949004563809, 9183.807227330559, 9192.227543112382, 9201.836876325178, 9229.805745296344, 9239.329799386222, 9327.81685524536, 9356.260052027523, 9368.30348708105, 9403.059947497066, 9411.75787580503, 9446.299987195052, 9446.39917409584, 9447.892030686315, 9452.323936251887, 9479.769701777494, 9502.875931789376, 9528.992158284349, 9545.774550726173, 9546.245450652797, 9557.218491044103, 9621.23008319334, 9627.795860316855, 9654.568585159668, 9665.98735109809, 9672.80808427401, 9715.034765466226, 9721.264893783788, 9726.074801372342, 9844.383590008207, 9844.553228426435, 9864.929609130286, 9880.943181140126, 9889.922397312881, 9904.70848291477, 9985.958209466764, 9998.830471806505, 10033.597855067295, 10123.457949318043, 10148.073335232157, 10183.815106648968, 10199.497277812741, 10210.37195689517, 10212.975021267554, 10219.503715959552, 10230.365400005048, 10306.43035398586, 10330.631376153093, 10354.899557181527, 10407.5344778123, 10469.799536843817, 10478.993136949146, 10482.658642297989, 10523.687208078867, 10527.819201952103, 10542.409360120624, 10603.439870561688, 10617.106454400004, 10622.677890100364, 10651.719265351187, 10674.756806511952, 10690.085109880649, 10702.630373014741, 10709.769113037817, 10735.704628037682, 10737.843613632383, 10773.15458490127, 10777.20398024135, 10778.185604218303, 10780.919759330176, 10782.135862154482, 10801.595887190644, 10855.5096725377, 10858.782295125346, 10862.813578927515, 10885.060846236516, 10886.333101687404, 10945.223088070508, 11004.375075231153, 11018.205692514231, 11032.12489508238, 11073.238438649578, 11081.09838081636, 11116.445820645466, 11121.350142045405, 11123.925786654323, 11130.277522449092, 11138.995723657936, 11147.097529768947, 11157.95908312254, 11179.298455256245, 11199.46883648018, 11202.539374117736, 11208.833823209263, 11211.067254428755, 11214.806925173845, 11236.88237803125, 11253.868466895972, 11282.81105599674, 11290.294921386658, 11293.984213328666, 11294.569460635093, 11343.772915522157, 11373.716117463686, 11460.097469209257, 11460.42205094653, 11477.827309162696, 11495.451160880597, 11497.505897483781, 11500.933234507032, 11503.791354932631, 11505.300905147247, 11514.551376322892, 11528.031609565387, 11563.470673910648, 11582.653369827873, 11604.452434808587, 11660.247394691996, 11689.344542085528, 11734.493301813869, 11740.546563092845, 11746.077286099175, 11761.841818926396, 11764.497516194828, 11785.446095571635, 11821.142330436312, 11864.786406115549, 11874.415761731392, 11874.799251004255, 11880.161834191818, 11918.747713457495, 11959.094660830477, 12022.628670370163, 12024.454552627645, 12039.937126171433, 12041.415619997424, 12095.975439267664, 12123.487243555677, 12136.988048656684, 12188.240149430716, 12205.885877391256, 12258.30039182893, 12272.76861367801, 12277.367628271515, 12277.953141327089, 12304.199297198582, 12305.972992587358, 12319.74086419178, 12329.589945188945, 12343.123510570014, 12359.871285457704, 12393.898568561792, 12416.438737841389, 12467.786990894449, 12563.529746287371, 12577.024744196504, 12612.317279801955, 12661.060210487965, 12734.685182528483, 12820.7041119494, 12847.662637943624, 12858.554317247572, 12894.7060496308, 12975.714008173505, 13036.001071937673, 13058.753745454025, 13096.56034198319, 13125.722648831106, 13171.99823663805, 13219.646511999688, 13310.684303046615, 13365.462148750124, 13376.280409741248, 13394.862604531925, 13395.90378925837, 13404.607858802694, 13421.650901236271, 13434.789785466002, 13441.526496133203, 13463.948151668408, 13464.00120563765, 13476.701131565322, 13521.939343551956, 13552.600677421731, 13580.039456969453, 13619.894360714785, 13622.173984642488, 13623.78857138384, 13625.5430134957, 13669.086090995803, 13685.781767924176, 13733.871437509402, 13761.007797350863, 13761.442049422414, 13778.662553134995, 13779.64441504223, 13792.700504786848, 13817.902048243834, 13822.071161050511, 13825.731703829264, 13847.69147436845, 13871.6077756726, 13871.993180237183, 13902.676037811383, 13905.008463433936, 13905.102557376, 13977.438146871993, 14002.18573847272, 14009.453655449432, 14040.974815295467, 14062.626608929426, 14097.225299227952, 14142.424200311167, 14160.525529975443, 14180.913644470511, 14201.259985983928, 14264.288821008591, 14317.79445617113, 14322.810054117546, 14353.197583826703, 14384.794095963538, 14446.214666157051, 14485.340256845197, 14485.55357294381, 14511.641803027602, 14528.787902095628, 14595.931844607421, 14636.81142681021, 14640.453943123775, 14696.48581528846, 14730.469355714942, 14768.336563192857, 14779.66522624952, 14782.129024110047, 14819.201318996667, 14827.907224139344, 14832.532020690205, 14917.850263435872, 14938.83362453485, 14959.683627433338, 14973.385359985441, 14980.303128064881, 15000.244534877866, 15026.858237675317, 15032.572810198326, 15036.203764586422, 15042.269142979023, 15092.8731305943, 15120.448120724264, 15206.433488350835, 15250.423382034905, 15273.07343221574, 15299.194027714857, 15304.049294773431, 15331.216431710081, 15345.376848219761, 15357.871837359378, 15389.389779944244, 15421.280067240708, 15454.932296278377, 15480.938645936825, 15507.052360205833, 15567.60441280142, 15582.47851983611, 15588.004917740169, 15600.388103268122, 15614.671364502696, 15648.517593627128, 15650.579842345904, 15673.692769758465, 15674.876961252172, 15677.055784005215, 15679.789462154022, 15695.09446263088, 15715.445459111384, 15741.192363010457, 15751.552204998074, 15753.16603856722, 15827.859681089454, 15833.341541729587, 15853.309401498229, 15935.30997717002, 15964.916940552675, 15989.118738826992, 15991.514104082666, 16016.347436855125, 16023.993986712663, 16065.506050381202, 16124.167103664378, 16247.153589974785, 16250.133902224445, 16251.881119745605, 16263.639570933366, 16266.045757879894, 16278.357752774196, 16287.454368828843, 16331.56063446054, 16339.455314583256, 16340.215948064682, 16342.729018820115, 16348.953799584233, 16352.15232155743, 16397.38419112136, 16424.68070952836, 16459.746277294937, 16493.50348384997, 16513.154269280432, 16532.14486747609, 16582.796249402832, 16615.658467245616, 16679.96500152774, 16727.289059556373, 16738.728440382773, 16772.230825425453, 16842.34050623952, 16849.309460439224, 16869.359247794615, 16869.85272315809, 16884.14745590418, 16903.326320332995, 16903.586898451576, 16911.81532663966, 16947.81283369484, 16951.727748087083, 17095.30093372784, 17106.346491143282, 17121.508454272294, 17123.859493079894, 17137.99651485336, 17167.21909482737, 17168.541208874456, 17232.287005186303, 17233.849615249608, 17262.32103292238, 17264.09432059294, 17321.81297065993, 17332.968336832826, 17359.280127261147, 17394.892390281042, 17416.709911286758, 17425.204740652418, 17439.124628542086, 17473.107151316348, 17503.37394327327, 17519.46249730271, 17534.41944411652, 17545.77352961766, 17551.014732283227, 17553.594464688493, 17555.386033355666, 17557.29165165453, 17576.3426356326, 17580.58954019751, 17584.77575457136, 17608.770117564527, 17629.280092068053, 17683.736906221886, 17683.776046801147, 17710.803893921744, 17773.364712149752, 17864.86738339555, 17876.02913828337, 17887.434856486205, 17900.73613822682, 17917.01926867842, 17924.757743038623, 17941.189733449704, 17967.901968771548, 18005.18380706566, 18014.5630910217, 18015.50865337773, 18027.611401767892, 18081.780896746648, 18122.46608030422, 18169.05648462966, 18222.168276274973, 18257.09239330914, 18258.877341431136, 18272.882015811265, 18304.649415047388, 18337.469918748175, 18346.512144049833, 18354.172670095075, 18357.084976726983, 18364.143936213484, 18365.328348430106, 18420.236352589454, 18422.945113041584, 18453.93098246742, 18462.873902534004, 18472.56725062071, 18543.42968778137, 18580.484682405244, 18597.120221139798, 18602.305313460398, 18621.12123359995, 18631.957758515528, 18681.622290557927, 18742.07697038482, 18783.085739482165, 18798.85600938899, 18801.603544774014, 18836.170221553883, 18861.129416194388, 18865.764273589375, 18881.0570421164, 18890.606227765413, 18893.69409965502, 18908.123945007464, 18928.79791171245, 18973.42701468491, 18992.651840596787, 19051.348745324467, 19104.611349457984, 19127.81413006643, 19146.723587425062, 19175.25079977914, 19191.248202293045, 19191.78334942759, 19201.059642168213, 19233.160303013, 19251.345247274443, 19263.392248141005, 19263.567963643694, 19269.118781304616, 19271.349068965843, 19299.722869519097, 19312.516492396288, 19355.23612762886, 19357.1383276626, 19360.748958114727, 19380.153456553562, 19409.311891922625, 19440.841064580098, 19461.471800473228, 19468.371332995324, 19517.811674258865, 19534.882494653328, 19573.096982267794, 19605.41009781601, 19622.134082209217, 19654.5679287876, 19745.97863970632, 19749.40035726271, 19782.024363895813, 19799.27315531332, 19808.864531509735, 19829.590682926522, 19834.7503036169, 19870.855394848935, 19886.80496762135, 19990.688722592116, 20057.66104518251, 20088.498610409715, 20122.74211834185, 20124.73997106437, 20126.847458305376, 20135.491322064263, 20155.9136502866, 20156.00826585828, 20189.951863870483, 20192.6946753011, 20206.306349936636, 20217.539563460436, 20269.0643524645, 20285.841851209992, 20315.147419329576, 20372.535475384255, 20376.788368256257, 20481.005666191257, 20502.79126730228, 20512.77517756407, 20552.642834645594, 20565.64706213058, 20584.900008928103, 20626.213045899087, 20680.453633714227, 20707.19766786111, 20708.59172963124, 20736.80310730818, 20794.054039388837, 20805.00862544746, 20815.96737405878, 20857.11882696597, 20864.760071695942, 20879.315416405494, 20954.99201306312, 20985.60921223338, 20991.94604435205, 21027.438781348843, 21096.24002790939, 21097.15682071154, 21137.567559846953, 21144.20562111759, 21146.25725372163, 21230.61437205858, 21241.54555147265, 21269.56271710926, 21290.363563029405, 21310.418244422443, 21372.719232617077, 21382.33011859146, 21400.70713949644, 21419.29513697794, 21430.568774376785, 21459.50417088776, 21478.792611757395, 21482.673049462624, 21506.57902566042, 21512.377282557583, 21526.371481859875, 21571.390130097192, 21576.26886496749, 21616.55117633786, 21632.414877167896, 21672.222700080478, 21712.459840838754, 21743.754531354545, 21776.525296400847, 21801.040900500644, 21806.491251089985, 21814.325209878203, 21830.206544993693, 21859.377165300186, 21863.822903749817, 21864.340926118974, 21882.523422458078, 21886.115135188782, 21898.371432413827, 21951.389927136966, 21965.881403313928, 21976.849538321785, 21986.085386222374, 22000.528636284947, 22006.809638302628, 22020.696169501098, 22106.435856578482, 22124.905706618156, 22134.855011076626, 22135.49311388929, 22135.98291385559, 22141.189558523532, 22166.434160594385, 22183.00534295095, 22183.71996466358, 22232.262523161644, 22268.662616483878, 22270.1743293341, 22321.07202823898, 22359.059804937624, 22372.272045767404, 22399.78714804626, 22487.425234653172, 22541.289413515235, 22565.44575624272, 22575.43357668067, 22576.523859819627, 22578.885142617662, 22610.105387411983, 22626.398482335906, 22630.31793484611, 22646.832515656097, 22650.96477495938, 22665.404463704035, 22698.59395641957, 22763.166551119342, 22765.88573454113, 22805.022919907122, 22866.95203402644, 22871.618343497827, 22897.64618158797, 22926.57396872966, 22930.84050040215, 22966.790318333053, 22972.783999169646, 22990.143201301245, 23029.30855137504, 23030.14714152413, 23062.950200995667, 23098.386014319734, 23184.09298522365, 23201.900131276845, 23231.976294859967, 23235.81752404358, 23272.44846136972, 23282.486352695312, 23290.295782303954, 23311.454493453886, 23320.90994083656, 23384.10091539116, 23435.50375985466, 23459.09346837978, 23520.191608964084, 23571.82439879074, 23591.20838126567, 23694.7797271231, 23753.083604543586, 23759.399479963504, 23773.873009402498, 23799.04375309921, 23808.544892319846, 23816.39457367386, 23840.222867459015, 23859.823366487115, 23893.558392925264, 23973.03924877912, 24008.440766322437, 24013.62041099431, 24039.515361611553, 24039.966280878853, 24043.592752238892, 24057.399751457317, 24063.29337754038, 24081.703181096364, 24099.959058373573, 24128.491908906275, 24129.612572490852, 24133.45286056637, 24138.874301742904, 24146.56958693749, 24153.59430976286, 24288.06772735391, 24301.87821017769, 24318.782283073873, 24326.367287608628, 24345.995362229503, 24392.90534646071, 24402.57631774688, 24429.18663744887, 24484.369346794323, 24500.800367399566, 24522.019759910174, 24526.10135155252, 24555.758511173415, 24582.27391391745, 24612.98671170758, 24681.23056129345, 24744.96873260543, 24771.779999903913, 24790.66902433264, 24794.942005331293, 24806.04904264831, 24823.31952438894, 24847.27757825668, 24898.206004419302, 24949.83928826645, 25003.513797887295, 25015.247355068062, 25060.306616110385, 25106.687458318447, 25185.74148051216, 25205.569336352917, 25248.01005263, 25269.526369814066, 25273.974933115536, 25292.153518879008, 25301.0531554588, 25315.75509992915, 25324.640471066738, 25330.04398640671, 25348.59288786773, 25362.098004434865, 25400.842170889842, 25405.442283556826, 25414.322730757536, 25461.19278424264, 25474.447631577255, 25534.765310054063, 25537.503039454277, 25580.858734195852, 25587.15325029202, 25594.30465050402, 25676.246869877137, 25677.986312227324, 25695.610526678407, 25698.37657884004, 25774.171841253865, 25776.252432419173, 25802.246969360964, 25810.261756775213, 25820.407298918166, 25930.936910704633, 25931.70425938785, 25945.18150747845, 25983.62300148573, 25999.88829353914, 26007.97190533804, 26059.695316974317, 26081.90249189119, 26090.373904150223, 26092.865224716625, 26095.888276169862, 26114.996348350945, 26120.078152514536, 26121.363265355416, 26138.514586804453, 26150.148902166213, 26173.091512421455, 26186.542893307214, 26187.211595473018, 26189.81370332254, 26198.335181634855, 26221.56355180578, 26239.47781189668, 26254.3417862786, 26256.059505188972, 26260.477874508386, 26280.327909109965, 26382.282354340314, 26387.991373232875, 26419.4201918569, 26431.846908553318, 26469.36283924777, 26514.270683208404, 26525.64820840193, 26542.73347511317, 26552.011704165903, 26595.93558029543, 26599.541644629255, 26599.93932770436, 26616.27886685574, 26644.720512391457, 26651.867679002757, 26673.957763573013, 26675.892227870936, 26694.704750003064, 26702.374463849173, 26711.65294801722, 26753.370293334647, 26768.747503444567, 26776.933873500653, 26779.87169197426, 26785.299118623974, 26874.47347533131, 26914.529583466658, 26942.91070593611, 26949.161611735395, 26992.320681566824, 27011.34820374383, 27028.981413711692, 27044.145621891406, 27044.399018957884, 27055.059028921452, 27111.996656434832, 27138.181547624572, 27140.310193919515, 27158.400498749186, 27158.857731785247, 27190.379498155504, 27194.120251422824, 27223.17514641075, 27282.868546629834, 27291.02919681175, 27324.397414930318, 27336.5347707749, 27337.844936609898, 27350.92841902406, 27484.65330256858, 27504.203213066037, 27516.161898812705, 27561.843675436146, 27606.68498743015, 27623.839805202024, 27673.036590201173, 27813.420107543, 27848.44042843854, 27882.713020378604, 27907.95840292605, 27997.500399393113, 27999.21274505589, 28007.967153584435, 28063.313725963013, 28120.432168008414, 28132.759070301956, 28144.441630058744, 28156.19243301969, 28208.86640319684, 28230.1403955323, 28234.879376805533, 28239.86130759936, 28250.753141574005, 28274.694185503082, 28307.52021640745, 28315.43442362332, 28321.56842684602, 28334.8660292595, 28415.65807741856, 28416.322414094273, 28422.306530183763, 28471.751344564964, 28511.105743619028, 28525.21020239141, 28601.093812966723, 28613.712643860163, 28646.210322758496, 28670.996559524992, 28779.19857977187, 28781.773509978317, 28820.33544118493, 28845.375222303897, 28889.650831185634, 28901.41791665107, 28909.053623865555, 28914.1156014687, 28922.427866296457, 28964.252394956377, 28969.959881941035, 28971.24970031797, 28999.752002276415, 29008.947513363153, 29045.804184399334, 29063.943332860807, 29110.68410003928, 29115.18517190103, 29144.17166414228, 29188.31559428336, 29189.56373715896, 29203.35882751712, 29227.85428007854, 29245.582178794244, 29265.858697738582, 29269.094202748587, 29429.60828776489, 29440.91390383031, 29448.772704547257, 29454.528867556928, 29458.465084703057, 29466.15940773554, 29468.775669116993, 29481.63079115644, 29486.83685587633, 29558.79476563902, 29560.51066821378, 29562.496455251683, 29618.54673634045, 29648.472838166275, 29683.04031578198, 29685.854638919136, 29762.74014805964, 29864.751675866723, 29866.749612579584, 29867.157272630095, 29876.371768753233, 29883.421887043503, 29891.958851459593, 29893.652186530504, 29903.417951428084, 29927.653613304978, 29973.88314823134, 30104.231366130447, 30147.462047748522, 30175.88787798583]


    
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

    X111111_1 = [5767.381311159836, 5813.819865433673, 5818.441030609147, 5873.83517946938, 5905.637855891687, 5907.33583710289, 5932.454113324146, 5950.6217028395795, 5973.953406080647, 6004.59576617354, 6022.098084589339, 6031.025808967266, 6042.171023015225, 6046.155317300075, 6079.83986873056, 6184.486712002098, 6187.924728801709, 6188.007274337973, 6205.995563154177, 6268.739553761045, 6276.2930554760005, 6297.651218032875, 6307.478807316209, 6309.076200815509, 6358.482030152343, 6370.428189240189, 6381.280981242262, 6404.702021762085, 6416.929450229571, 6439.175725829505, 6443.293855652639, 6499.024445822512, 6531.955525655249, 6568.187016136148, 6643.732812159959, 6644.561295945918, 6665.735065909914, 6695.036250648976, 6698.396300564606, 6723.786180048172, 6748.158044621103, 6755.487415702064, 6759.226751380869, 6799.713807075834, 6834.645415093391, 6837.067605492509, 6839.360589172877, 6852.648252057773, 6866.161494724307, 6887.134222973276, 6919.05193851776, 6945.738722319582, 6945.9244193122495, 6994.856289176008, 7002.911262562056, 7046.458368126722, 7088.115691834526, 7108.811562686086, 7108.999402792914, 7114.816349528546, 7137.357998346938, 7151.852980778427, 7179.379770806394, 7180.921189896111, 7200.771044891274, 7215.629304711985, 7218.726595365452, 7237.694089653136, 7244.572762490832, 7246.156448975997, 7349.664379636273, 7358.5367151380815, 7394.458999640196, 7460.042274606721, 7484.173625675049, 7502.1604518365475, 7520.362561296805, 7538.625127521829, 7548.7281704366105, 7634.029864100587, 7647.034029750546, 7648.392427447154, 7654.742785228855, 7669.124442957296, 7670.509829197088, 7734.959283344493, 7740.877583045533, 7797.653804813366, 7818.021429531145, 7845.167085434803, 7880.7279946396175, 7897.262750245873, 7924.6223608556265, 7979.067963558342, 7987.225065035128, 7999.182840004047, 8065.729153077191, 8110.481544654132, 8123.112427545861, 8140.239670706615, 8153.561495380855, 8167.7439931056515, 8184.858475721581, 8189.661864160444, 8191.137773872637, 8215.054406614956, 8228.179131027378, 8238.464394316572, 8276.556652257765, 8304.371550328447, 8376.587226461459, 8377.153448173965, 8414.016532007656, 8577.248459079627, 8594.802123415604, 8618.792135048534, 8621.094337334214, 8644.980312182322, 8661.367298147978, 8661.951742091964, 8664.744794646012, 8690.30844269761, 8756.080737865585, 8775.033597747251, 8792.989713667946, 8860.815867484333, 8876.0125944243, 8881.611977232116, 8891.81494758466, 8915.381561728627, 8929.644861669554, 9000.5186655997, 9125.509298627869, 9127.254319789765, 9218.186598836859, 9254.816770469897, 9258.924591220333, 9280.772107846171, 9294.941627243119, 9299.088094681665, 9348.45366414758, 9366.137787134958, 9400.590821180072, 9429.504499311723, 9436.598498236737, 9446.572607156242, 9465.59983941946, 9547.54213955821, 9605.090871119353, 9616.922045786925, 9632.219629427727, 9634.599814728797, 9683.816909013747, 9735.518386343894, 9736.03616792855, 9736.581298717958, 9756.064963829504, 9787.356621712283, 9798.180270643663, 9838.596801987205, 9843.982813570172, 9863.87956856699, 9865.971482783736, 9869.719895437622, 9872.283298806768, 9905.489625346334, 9909.318712454664, 9921.3885758304, 9948.87854939364, 9995.215527434852, 10015.6291663983, 10018.016806657892, 10046.66964370065, 10052.809758528034, 10075.665706150343, 10081.669984958036, 10082.876033401146, 10083.740662740165, 10112.750082382743, 10146.635837649133, 10157.864504855137, 10158.781741477054, 10182.723949668783, 10185.635502688747, 10245.022700155543, 10249.083825006503, 10252.596315424016, 10267.74352092029, 10268.244930445591, 10288.79991435075, 10318.569135242065, 10339.632212951889, 10343.992265011013, 10440.085712741095, 10466.484559155306, 10498.116950243482, 10505.499529003619, 10553.34062628791, 10727.147456345567, 10759.527436137223, 10792.050238390155, 10797.122677068739, 10864.636016880968, 10921.071528673261, 10938.742739793204, 10945.393113768383, 10984.705513306963, 10986.584227818377, 11011.181007268067, 11047.457330623774, 11071.93410820839, 11073.27935986307, 11111.161892581129, 11129.372568085057, 11172.534155105597, 11193.26234234564, 11231.53098024588, 11237.436018580636, 11266.454389923696, 11291.844480124968, 11334.100440801962, 11348.212041470557, 11357.17014131382, 11372.438706096662, 11382.25043593387, 11393.617496392164, 11415.225501766236, 11434.72596043105, 11438.771309313455, 11469.561418559548, 11485.217624676252, 11492.575794701484, 11515.497364026895, 11580.080596877582, 11618.140973424266, 11619.282106608349, 11690.909659540572, 11694.08527245405, 11763.240016985917, 11768.1203826645, 11800.134991071538, 11834.403265034032, 11847.282582187872, 11899.13332103724, 11903.369298659887, 11908.481099025383, 11911.084090569142, 11958.127252591923, 11962.589016867492, 11990.868585834378, 12044.224644608275, 12053.598821905383, 12062.879000807941, 12129.407246584971, 12148.093900030206, 12155.797402039803, 12258.838983571011, 12284.70166392569, 12308.129993914856, 12310.809521252231, 12324.30645646033, 12331.023652134569, 12336.125196824873, 12369.319296234347, 12394.262567868125, 12530.007605108818, 12561.414378836154, 12609.949387098557, 12632.886225742928, 12635.867143455962, 12647.025526472327, 12666.17183520797, 12672.03235544304, 12765.668814223642, 12785.711133450179, 12795.949751468672, 12825.803004769365, 12832.4682184054, 12870.623606610983, 12887.14719911067, 12905.571048515496, 12981.141859784326, 13004.19518191959, 13012.934707944838, 13013.76584365159, 13015.682196585385, 13030.212918938556, 13055.745125147536, 13095.058166511702, 13114.247630364669, 13120.846377879647, 13137.83334161968, 13155.189307314839, 13155.48888868635, 13199.510569970218, 13207.270224881504, 13235.358139795317, 13267.247193264873, 13290.577456608677, 13302.864068584935, 13315.732822950591, 13316.171325125491, 13328.403801223114, 13378.169473469305, 13381.520652103613, 13395.340368550056, 13400.7695691685, 13403.74097069601, 13444.923718051987, 13454.270647139478, 13592.095499151728, 13593.62361304065, 13632.347718596644, 13646.410080904934, 13688.215598960654, 13733.37908559664, 13748.808067246284, 13752.613686542927, 13764.127020236923, 13776.69156230858, 13822.486341005217, 13827.336209583482, 13827.783553737667, 13828.703258993504, 13841.955805263005, 13843.313345653607, 13865.7814846303, 13884.342981016027, 13909.399460230881, 13915.038324493536, 13918.791532370491, 13925.760346849602, 13951.484617661508, 13995.427898393795, 14102.140283246224, 14196.580023661769, 14207.971833152595, 14224.611259007965, 14259.12396254448, 14277.965449895668, 14337.30651558993, 14349.35322569625, 14361.753383796195, 14368.937664034023, 14397.480283896051, 14401.831695146318, 14472.517084551935, 14503.31169804052, 14541.615111141291, 14542.777593439994, 14558.38558180597, 14565.714877533848, 14619.99636855218, 14627.395006107145, 14631.948010085991, 14752.698590191147, 14762.563688532255, 14815.645037812676, 14839.66154985719, 14841.61407246693, 14948.251290449401, 14949.18017270648, 14961.29420767701, 15078.440513987798, 15130.221757450749, 15139.311384722349, 15173.781816019487, 15230.039042098811, 15290.478159660974, 15292.519989289287, 15375.692751176075, 15396.637132416668, 15403.059548456482, 15424.664995887066, 15445.397274083996, 15483.642433875486, 15484.838607648693, 15489.75302811545, 15503.567152580357, 15527.151882306574, 15606.324488490596, 15625.656755242258, 15701.163693553252, 15703.76682284946, 15713.492982527647, 15714.863827062802, 15759.519982354434, 15773.974084926569, 15777.459889145382, 15785.356063194675, 15906.180947259549, 15930.77092239969, 15996.389770828737, 16002.756050729553, 16007.100170496607, 16053.811432458191, 16063.397578007873, 16071.143319998739, 16100.677419149784, 16227.740522837377, 16233.337145616004, 16250.525287492246, 16255.185347208375, 16256.734972922028, 16319.688181573132, 16325.244404175019, 16344.10537725475, 16356.180768724416, 16373.611743694233, 16387.85980531163, 16411.243954367157, 16421.558724406263, 16446.74733103325, 16483.31374544106, 16484.585740092585, 16494.267337333607, 16501.667008313223, 16562.456814046003, 16575.172495293085, 16585.497460419283, 16597.20455900525, 16618.966738854433, 16619.41457477615, 16635.605015896464, 16636.638846303926, 16682.459480264843, 16700.141216122964, 16708.110769284773, 16729.11884606768, 16732.47400055702, 16733.418358502866, 16784.48098582244, 16789.29632614321, 16791.413202989403, 16836.93008664232, 16867.791913006982, 16882.005601091994, 16910.72780036636, 16933.653805827103, 16937.030148815495, 16995.48237058423, 17043.352261857945, 17068.617562530468, 17083.175223046168, 17106.453999113357, 17123.675003662956, 17185.061271747334, 17187.460684689337, 17257.763609728452, 17260.536327380985, 17315.932681907074, 17344.44050940519, 17355.692552521927, 17407.036844321086, 17431.628625534522, 17452.371922779137, 17525.099254015506, 17585.427134783633, 17606.46183793123, 17630.56487865471, 17633.05706104027, 17671.05226651564, 17681.102461599236, 17691.200498801758, 17703.6339665283, 17713.7863288035, 17717.144239845766, 17726.947927830828, 17759.934523327458, 17783.16319512009, 17798.273905379545, 17830.949034984857, 17910.844988962235, 17915.385486562554, 17918.640405548947, 17921.521271336198, 17934.63507799977, 17944.69162625595, 17989.289720118682, 18001.226741830476, 18019.60012620879, 18066.20005525373, 18099.084912599857, 18112.063404467022, 18140.600697228743, 18205.796211983303, 18212.54488111604, 18231.486706400443, 18292.196780290276, 18306.38061652442, 18315.29663524295, 18366.776884730934, 18383.665838164034, 18410.802137929066, 18422.197568470772, 18482.690455625358, 18490.872919981375, 18502.21346259663, 18526.155546875678, 18542.232714026064, 18595.206788263316, 18598.180904048633, 18604.526983779637, 18633.024646242666, 18634.792408709163, 18642.99704809991, 18688.854555550246, 18713.430512839797, 18714.28066377168, 18715.07340102366, 18745.566780813853, 18751.217568787324, 18770.21057057324, 18785.10880440232, 18815.089047550166, 18816.55539902982, 18845.017421321238, 18905.252156572584, 18920.983807235127, 18949.330809546456, 18962.43672771648, 18995.73405177485, 19024.168086039495, 19026.40004737841, 19168.557967457793, 19224.555237481833, 19268.07748740489, 19278.76025366126, 19291.95607829658, 19327.10228446835, 19372.204956607296, 19389.99725733813, 19419.569578746836, 19428.36798743014, 19519.30656710348, 19558.99229671566, 19561.360831007383, 19588.73400008015, 19614.991169802997, 19676.530651617337, 19712.08541182854, 19780.70682929286, 19821.656347864715, 19860.747664462695, 19867.876075515233, 19880.35401515697, 19883.40682726754, 19903.51057788876, 19911.878716875617, 19926.99375332758, 19963.290949240276, 19970.86024021671, 19974.879614536632, 19998.414420098565, 20008.16172635301, 20064.95062647321, 20100.783963199643, 20113.250153839934, 20115.70585642715, 20119.805734393398, 20160.11491702327, 20162.95998356989, 20170.622789746216, 20171.04233953348, 20186.194105340357, 20233.07065405875, 20284.38239776641, 20295.07589664839, 20323.631892318313, 20326.42937869822, 20329.503702543418, 20349.23088361274, 20358.8917489691, 20368.258139497673, 20379.47460404226, 20383.8059198018, 20385.339763128737, 20394.530812074696, 20422.80815497884, 20427.28270785891, 20428.58598967229, 20432.577028021267, 20468.729173144748, 20487.09971209807, 20498.861453153433, 20504.78682559178, 20539.624854105423, 20547.257581776987, 20551.413510096234, 20571.15325513409, 20607.7541133938, 20653.669098752063, 20671.763010213414, 20724.593808615577, 20755.685878039112, 20767.713426919683, 20781.657480057103, 20802.15636251044, 20827.161855830534, 20827.400498775336, 20843.28560505701, 20847.29445530202, 20882.87020667229, 20925.845403749932, 20949.195368642017, 20957.885088700168, 20961.394451283413, 21064.048383026064, 21092.727670298715, 21102.147509210936, 21161.201264388124, 21227.455249388382, 21251.429117058928, 21259.11142710491, 21287.45615174476, 21290.37920661215, 21302.284291616495, 21306.625345088876, 21334.249526820127, 21369.500746361977, 21404.28640814394, 21481.307645307443, 21484.658314990666, 21553.341198315215, 21592.453810180872, 21601.826506903977, 21615.632010667912, 21619.53639107511, 21628.79666673528, 21634.80229350466, 21645.46535800056, 21661.299665034618, 21672.578551490988, 21673.202212870736, 21711.831409045684, 21730.149726507632, 21733.243949146337, 21740.998420507283, 21828.206004410633, 21865.186412675073, 21871.060147643417, 21889.184755729388, 21896.28835699797, 21907.35107872178, 21918.705469085307, 21923.87594031899, 21934.892495718574, 21936.898524179887, 21945.108580409727, 21987.170592199058, 22025.604602125684, 22025.92034463891, 22036.765669956076, 22065.994682578374, 22069.020994477578, 22081.8926601531, 22099.979542445464, 22131.222646647166, 22149.016219455814, 22159.850574585307, 22246.823604180507, 22316.46296447013, 22321.217244686573, 22333.79205850653, 22339.89329422822, 22357.27459235616, 22379.85469805999, 22396.846698630965, 22403.00945484269, 22437.576087883976, 22471.372269057716, 22514.57058146302, 22519.952619615597, 22524.25074599067, 22530.52998312025, 22580.605960948007, 22602.15541527939, 22635.580627201885, 22682.82935059629, 22706.05435058936, 22725.782587456622, 22745.36708156911, 22769.78066780626, 22776.944425294398, 22783.901284927146, 22863.61692258844, 22880.43776928408, 22936.892294832272, 22964.323010552573, 22984.72949930586, 22986.326924430025, 23015.394822464943, 23028.17262307388, 23040.057407900007, 23046.075297319032, 23055.777801683776, 23058.11952471948, 23064.17917648261, 23097.411711983532, 23101.668675809142, 23102.45579435862, 23111.31974452768, 23119.137220219043, 23227.42539966132, 23230.766692933095, 23231.390545750222, 23294.767013715187, 23311.376182564993, 23343.097248058555, 23370.00933452665, 23376.35798509418, 23378.05347086262, 23389.197101137706, 23399.983377131957, 23509.375554699207, 23516.58607970195, 23582.975261374788, 23590.648824931992, 23593.877907578215, 23610.980166052752, 23618.665136155927, 23659.637202163558, 23671.783239417513, 23704.588721548575, 23705.7175367782, 23738.951844452367, 23740.53481054123, 23741.093229797607, 23744.844583272803, 23770.0107405896, 23789.484152956902, 23822.792439787307, 23852.081909794368, 23860.74753516723, 23944.83254971526, 23973.98683537539, 23995.7286009612, 24023.4377889701, 24035.008454966275, 24101.019063961336, 24113.47955598283, 24150.869587497487, 24153.836652010265, 24230.187711216204, 24245.465213235973, 24253.90025647231, 24265.420243654364, 24269.536010617092, 24289.872050582173, 24336.105461307532, 24342.339401058936, 24346.492917933883, 24385.152008006786, 24407.249671878602, 24446.680044762652, 24546.85424184883, 24567.582374659934, 24600.963498632733, 24612.84728159538, 24664.09875357097, 24708.29193305571, 24710.43376018756, 24722.59205994283, 24744.771144327948, 24750.037343548047, 24754.59488534562, 24773.559771370205, 24782.700933820266, 24785.817699982086, 24785.981408553886, 24801.030166550107, 24834.59525695692, 24850.905187196924, 24868.188217626113, 24889.43706069664, 24929.589989190194, 24949.72625535059, 24968.183674366774, 25000.982908166607, 25013.914163554942, 25021.871866910376, 25029.60596589207, 25036.322049887724, 25048.948227278106, 25094.322769594564, 25109.5323577133, 25124.984981445443, 25137.46863891948, 25153.264830960237, 25188.095389106777, 25191.190219680982, 25203.366637557974, 25223.08560340003, 25248.417563289127, 25260.103374181075, 25294.183562359314, 25325.799605691976, 25342.56531188846, 25350.55605276107, 25384.38417192646, 25409.751600819534, 25413.093720960598, 25441.658225182575, 25483.982085762644, 25503.918158893546, 25511.741282196395, 25517.205903148297, 25529.118796608323, 25543.43276486817, 25551.953083972654, 25569.571435660044, 25582.361735041653, 25631.266143159744, 25632.6579416797, 25636.619697225105, 25727.575840119887, 25735.06668459459, 25773.552061332386, 25795.837816106214, 25845.20364698526, 25870.714257552365, 25882.065971845626, 25883.165276257703, 25886.25173090462, 25889.1041517265, 25914.55687793474, 25926.33949911435, 25935.808077688213, 25946.990590865378, 25977.79075617884, 26022.670850124883, 26028.034468651305, 26045.921518926196, 26092.78207135496, 26094.999478518057, 26133.921504449187, 26137.82504466435, 26145.945331088256, 26163.24261868081, 26208.463647122728, 26352.369725910037, 26362.63576486788, 26372.88779950243, 26389.0925992836, 26407.47953467163, 26442.788034104156, 26483.855472915424, 26515.931872595324, 26540.925950951932, 26575.981946763575, 26577.88413230816, 26598.658713035973, 26607.506360067902, 26640.3679913819, 26669.671621378402, 26682.812477978525, 26710.172471275735, 26741.849303932497, 26744.97648932006, 26767.628286787512, 26824.19951128571, 26853.769463805107, 26856.945799612608, 26902.415499777228, 26906.968318312665, 26944.696961868867, 27002.125447344, 27015.50861367384, 27058.79124455837, 27066.738214846526, 27083.28121723664, 27088.536516778404, 27119.027822079694, 27162.065375350652, 27164.48719890683, 27197.215888340826, 27226.673756630084, 27240.616774234146, 27254.49681074187, 27286.910772666015, 27287.493019702135, 27311.53528164781, 27319.21401155761, 27323.38599398127, 27356.763575123256, 27385.698384829622, 27391.694686784675, 27397.46214919304, 27431.57724791852, 27455.819918375313, 27477.891884390076, 27512.12219616685, 27515.21208535328, 27593.33823264967, 27601.91743110336, 27605.175428348462, 27626.91192755354, 27628.60247421156, 27656.64349415061, 27707.083941617857, 27714.598680115567, 27721.035148591007, 27745.72825780344, 27804.09929226426, 27832.728460307004, 27931.13825448177, 27960.027638077772, 27973.085955585095, 28009.120094366946, 28026.42306587865, 28031.48111159799, 28038.692482312832, 28056.881270315294, 28106.99469676881, 28189.226824060173, 28203.43734351387, 28206.571250229004, 28216.983301533153, 28248.689912429152, 28273.15129612409, 28288.067697103805, 28297.072378669265, 28312.452000452526, 28347.762212784957, 28359.048444762586, 28395.749848820524, 28406.640309782888, 28444.369460414153, 28451.968822532443, 28488.605191740826, 28499.74869992293, 28526.58112689488, 28529.115414487038, 28561.997247380074, 28576.62733261038, 28594.929830598434, 28612.679587690556, 28633.842116884127, 28673.502757065802, 28684.690197000382, 28786.07506712593, 28811.269759113937, 28827.454612293855, 28863.14908531821, 28882.672047675183, 28891.682537280703, 28915.62488851717, 28920.58243326899, 28992.336266398637, 29018.59144496242, 29033.047392283766, 29074.229265671813, 29079.80113817416, 29090.505683280942, 29153.868327083925, 29258.519917822414, 29264.162909883515, 29272.998178009362, 29286.70103611694, 29298.511790030378, 29312.89290707712, 29342.847561911385, 29344.366866903678, 29347.335790232144, 29391.889574089884, 29393.689470808727, 29419.548602830444, 29450.202626216113, 29493.827668583865, 29496.491821759468, 29514.059655023877, 29552.651618317024, 29607.391204288106, 29617.27101584973, 29669.92331935326, 29738.828849251102, 29752.68623514014, 29771.79832000022, 29789.19069927207, 29792.122141643253, 29866.818579975807, 29879.30069344744, 29881.592850164776, 29883.716418470973, 29900.14395797026, 29914.06787725055, 29974.66279417722, 29999.274970346996, 30003.875729496453, 30017.74381908995, 30048.632926504302, 30055.7661298279, 30056.165257329023, 30080.39703630609, 30093.973972849417, 30099.5392485143, 30135.603378279477, 30136.415649340095, 30139.665962986848, 30145.761661073007]



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

    X111111_1 = [5725.848733738143, 5789.783167656262, 5800.078785353409, 5805.850387447587, 5823.230106679387, 5905.588929397382, 5919.973117178171, 5961.993789237276, 5964.877620209621, 5977.8128230436005, 5994.706547902906, 6016.228120619164, 6065.678784806863, 6077.867822914348, 6097.3716967572855, 6101.843066858212, 6142.167172910099, 6152.7611417693715, 6178.327072682414, 6220.1913086633285, 6225.318591192047, 6228.834554319395, 6235.115693086779, 6243.777441257897, 6252.217573269711, 6306.820465209839, 6355.786173972252, 6362.438496912521, 6375.703739483806, 6410.015553529078, 6410.2699557892975, 6416.551389921356, 6440.951046730538, 6467.302110605134, 6486.87365564811, 6495.507384986203, 6526.367408259545, 6543.670046657086, 6565.326238134279, 6566.967295151663, 6598.027456865417, 6623.946974949584, 6674.369003683938, 6710.827873585728, 6718.921677670353, 6724.778190468341, 6727.006194029139, 6734.674038189162, 6740.818086218631, 6769.113491097911, 6818.372302714578, 6833.395029845021, 6879.175356995232, 6879.733230304377, 6880.904189965211, 6904.528438698066, 6909.896685507501, 6926.131942354332, 6932.093977086463, 6961.544271095727, 7043.823148505693, 7053.452643270018, 7073.188318290405, 7073.709530607233, 7099.883548328645, 7135.7765219614785, 7201.105965494349, 7205.958295618692, 7256.210038938181, 7298.994009298583, 7334.495348115922, 7339.796147164307, 7340.418536223281, 7351.797287475582, 7391.086912359688, 7415.073385937656, 7438.687391886105, 7457.493252262038, 7457.867611349307, 7467.520414406543, 7482.084062893613, 7511.582170508602, 7522.422045094277, 7535.443699100825, 7600.560933029609, 7608.710727315856, 7636.38527299448, 7697.33576153369, 7744.994792471749, 7764.874601160722, 7870.259318007185, 7897.124088564869, 7908.088535754206, 7933.046097549772, 7946.519017701635, 7953.750202603307, 7987.135262876345, 8001.752739667541, 8020.399291861717, 8034.304552412388, 8075.42656257691, 8137.245379197017, 8140.5458698741695, 8186.70401469603, 8218.298941416278, 8288.919712143495, 8294.376200124581, 8311.741708281108, 8323.738714051857, 8333.925147665454, 8337.14638954903, 8368.473120485882, 8385.158849799716, 8430.815494349146, 8431.396535392694, 8440.157336829452, 8453.77972921544, 8463.032093258533, 8475.518005335958, 8486.357493851236, 8537.267107858583, 8551.974059588338, 8626.723754241295, 8661.678898277138, 8707.58951669938, 8717.165127229995, 8727.507590233265, 8783.529589886924, 8792.326970944026, 8851.074558407116, 8867.752859779, 8870.88974413574, 8914.038837583019, 8919.77862990019, 8931.501538410204, 8962.019097006416, 8992.461979094702, 9058.718437245427, 9068.772676414932, 9074.528320852698, 9100.875743807039, 9111.0446028695, 9152.552163061631, 9175.260000376227, 9195.66326370989, 9209.540470671118, 9226.641282981498, 9290.43363384822, 9298.513290748466, 9307.411295260914, 9334.203888447508, 9337.996158654598, 9379.892427276234, 9402.462504801999, 9421.499547282941, 9435.428915727114, 9460.357609056045, 9471.547783777442, 9494.831195764438, 9565.97808000305, 9574.160083507679, 9583.736109912046, 9659.178784303438, 9742.040799598264, 9789.724903718212, 9812.113789461713, 9845.89569009438, 9846.103940604307, 9867.282828192056, 9895.950876720544, 9907.667920772925, 9920.241164101562, 10014.100631860812, 10029.479827346637, 10042.588099429326, 10072.450785176601, 10074.516790850528, 10115.506089817427, 10124.008450008925, 10140.454038395892, 10195.140095660401, 10206.297076106493, 10272.534634626878, 10284.357412653892, 10293.038147749923, 10301.365749278135, 10325.921744558931, 10341.13342065752, 10353.127630798948, 10368.686330492412, 10382.453576057487, 10410.076825190437, 10424.68742847005, 10437.812940115722, 10501.747120565984, 10551.46391613971, 10563.053475320734, 10574.415191916156, 10574.674914530677, 10600.925074860425, 10610.572428116244, 10641.563511450411, 10651.333518553429, 10690.26258292532, 10705.909463686265, 10731.905653369402, 10789.505213334047, 10818.186365946207, 10864.617110153293, 10908.181846152052, 10919.246581818592, 10939.050455950117, 10947.825818159024, 10962.074714663691, 10995.243913594855, 11006.515016648445, 11024.725512700916, 11043.782417376899, 11086.57364014296, 11166.495748302004, 11225.527290082911, 11233.572471211555, 11241.05507327486, 11262.454139741074, 11263.718090025923, 11298.38446267864, 11308.383662843706, 11318.482169811366, 11331.7281850353, 11411.734966548602, 11415.600781999421, 11463.883543592296, 11570.164532590294, 11572.865954595229, 11574.26411650889, 11590.850064722947, 11605.371156241872, 11636.080145872393, 11694.001500481805, 11756.751678875247, 11777.107396584206, 11788.908047530236, 11819.470524781113, 11841.759324218841, 11859.717241455965, 11867.859854969682, 11874.43743892063, 11877.89234575582, 11915.188687270456, 11925.034569004907, 11946.105259737566, 11954.540115534564, 11963.472171968504, 11983.620225149396, 12001.38572045392, 12014.368027643086, 12035.922072798612, 12037.157798545742, 12053.628077685447, 12085.982794628999, 12137.56425944396, 12177.359716054645, 12198.736946398862, 12210.64447106437, 12215.330622831803, 12217.743243953151, 12218.94074078243, 12247.546470020232, 12275.758821857651, 12293.749136258433, 12296.743714181037, 12300.974274322338, 12302.528870279695, 12347.335884213833, 12361.001738061868, 12371.091788478487, 12396.418794545045, 12404.912568298816, 12444.436507743078, 12478.742363220736, 12540.503356300163, 12545.652550577626, 12562.507207672457, 12568.660966971713, 12590.996668210992, 12639.103432230306, 12667.328367784676, 12691.441762748313, 12697.447197684367, 12709.033427284132, 12720.49326873204, 12735.50043717528, 12773.918707403987, 12795.12541248554, 12809.911212460638, 12819.23320435263, 12825.06377461182, 12895.572078832061, 12910.648444977056, 12929.528834278975, 12941.307094398819, 12942.815869076669, 12969.998248376396, 12978.038454052166, 12995.48077931009, 13139.76195042297, 13151.809044926094, 13198.682370302355, 13219.97591583958, 13262.211746768651, 13308.337557399382, 13319.012778208664, 13323.385861135725, 13352.752226471737, 13377.065650480388, 13391.142241327689, 13403.331392052094, 13418.642074972042, 13443.758878872273, 13471.527385732865, 13486.707946739018, 13495.71042257965, 13503.30621631431, 13518.419477379131, 13540.533679336691, 13553.37369351674, 13556.769900107194, 13560.468990911551, 13575.125259933811, 13612.13727120058, 13614.848359688036, 13624.853964993365, 13628.023662714502, 13636.174405102036, 13641.901845251195, 13667.168693017718, 13680.662452753953, 13684.792392135609, 13706.378134839297, 13722.50561521267, 13745.764670969173, 13749.58721688542, 13762.727098081585, 13790.370078936596, 13808.303985078895, 13825.329621042023, 13892.491444414472, 13899.773144294912, 13904.960190721471, 13936.31868421491, 13938.058292110742, 14000.99940601591, 14034.438669834559, 14098.3327088909, 14125.953657334849, 14138.567329799158, 14183.8682259654, 14284.64059639526, 14300.66281527046, 14343.888636489435, 14356.28685237952, 14391.737164514087, 14419.339000280763, 14423.505988228817, 14435.390187133004, 14453.305230312371, 14507.819177428106, 14508.038161742654, 14538.153206288045, 14543.998666672844, 14589.175956708063, 14655.103040860784, 14662.071725996364, 14681.678626394994, 14718.612041455346, 14763.034115864664, 14772.479810650913, 14809.762792328518, 14824.12260153649, 14864.109010783644, 14879.379212114914, 14921.838721828522, 14941.71334465313, 14960.59673073883, 14975.153363201516, 15125.46422871223, 15132.453374745575, 15166.500288968246, 15187.094427773633, 15203.301954689367, 15215.42573320037, 15244.31199322049, 15246.20867106591, 15250.312623909716, 15286.67456708149, 15309.390475351942, 15335.844731525292, 15352.892819357801, 15354.233406064095, 15355.119008119065, 15369.514860490046, 15420.818141106503, 15423.511049711447, 15423.620135810892, 15436.871652429372, 15456.1377923486, 15458.315020346225, 15464.35752289144, 15469.49572947926, 15476.327682868785, 15482.96073194154, 15539.591613856317, 15547.133732864053, 15571.218828661044, 15581.251402841595, 15610.1600389271, 15610.864617748748, 15617.451854751007, 15689.815918638495, 15704.662118615206, 15707.053633111662, 15726.564794615884, 15727.472473345257, 15730.522436427973, 15762.324055999714, 15766.208537332186, 15777.335203007093, 15849.341199215485, 15881.263154809609, 15899.227747941592, 15916.169267804444, 15937.737044294206, 15979.053552394273, 16033.552083960987, 16067.060422599017, 16068.36963231875, 16070.245015439174, 16092.164514359773, 16105.315130535802, 16124.214953074204, 16154.823003648302, 16196.536345252269, 16216.347830681989, 16217.293329976066, 16220.653094289979, 16277.929801181306, 16323.908846533155, 16334.333360560604, 16337.385759849749, 16337.985845572199, 16353.231684073597, 16378.626867461566, 16411.610219984315, 16425.56314501666, 16430.316751195176, 16453.27470337774, 16478.28673356686, 16531.060163860173, 16552.08356067227, 16556.89049444153, 16575.038815005802, 16576.50750689151, 16638.425150091243, 16644.501065629513, 16693.425700821645, 16714.65327456498, 16739.527248888615, 16826.616359765714, 16851.154449071146, 16899.936000583504, 16917.0081275524, 16917.144506178563, 16926.739568318175, 16952.32563999612, 16975.5006971954, 16981.661224472584, 17170.492708840542, 17186.823183350265, 17195.56251502219, 17268.108874965306, 17309.987719888042, 17311.2602065128, 17321.978759484242, 17327.660766110246, 17332.10685146004, 17354.349250993007, 17365.756799896728, 17381.182203235545, 17387.07983063349, 17391.287324821576, 17393.221767098134, 17462.913263988226, 17463.188444926338, 17465.639511325593, 17481.01635816078, 17487.58476853598, 17538.178810816084, 17630.945852729277, 17635.800827562973, 17690.30262889146, 17699.793524820077, 17778.316552242934, 17818.59043097796, 17851.955956207836, 17869.83025529229, 17883.67492972394, 17894.658705558468, 17926.540103006344, 17927.12906579867, 17929.936670405896, 17930.576569663568, 17938.1517853736, 17948.062116755456, 17967.571111325906, 17969.23585689388, 17979.6755795259, 17984.858948282214, 18003.88858205673, 18028.390920833062, 18036.908926736513, 18037.132732086073, 18040.27383304391, 18098.837721560194, 18108.47353893718, 18112.96273232504, 18123.58149284452, 18126.96937809239, 18144.074084275693, 18192.94870885055, 18252.343762981378, 18259.96111453112, 18262.53291131845, 18267.61647661506, 18283.78277263468, 18284.417357576287, 18323.40889323393, 18328.574366092012, 18333.799513710306, 18372.63030693274, 18393.000063679552, 18431.5553689539, 18450.495906223252, 18505.18301591667, 18573.128081910832, 18594.980588033934, 18595.02430407621, 18596.292990104273, 18624.961732718322, 18625.66527603742, 18664.529049268538, 18740.4942233491, 18745.70420647053, 18747.870429214356, 18760.02779144068, 18799.226854977016, 18820.432007857016, 18874.85347685909, 18907.16569714161, 18975.902683085988, 18977.32981448721, 19025.019586751256, 19060.509415970017, 19067.891163979046, 19140.19775994817, 19149.343310140168, 19150.15187442321, 19214.777160567435, 19257.44959241918, 19263.566031247166, 19268.99963732243, 19320.910053400876, 19339.337449391474, 19343.305385688545, 19359.350045404513, 19390.460618889927, 19426.920392203276, 19439.622949403776, 19470.690440674913, 19493.979628731002, 19504.650662564123, 19521.16313667233, 19537.019105977284, 19554.102388344952, 19561.80461985656, 19592.467410247053, 19598.210224146274, 19652.732095725234, 19676.48230838395, 19690.68287993292, 19729.025489150936, 19734.332287020166, 19735.49039803477, 19782.393059371156, 19806.759332593458, 19826.923548763407, 19862.25808954997, 19880.357944233605, 19885.91333439884, 19890.869534827845, 19901.73496875452, 19907.34477847065, 19908.561676916645, 19926.041657440794, 19926.189071983288, 19931.179161846907, 19943.244876477132, 20018.726685554626, 20020.620743394484, 20048.55574062232, 20087.737469299333, 20116.70715867297, 20119.227973352194, 20139.242830285475, 20144.149161174333, 20214.80208492357, 20240.4218270824, 20244.74659507886, 20292.565718114518, 20408.640818123196, 20448.87806483107, 20456.182103731444, 20457.471429088342, 20463.842116903455, 20471.778094018886, 20493.868996045283, 20504.992039913734, 20515.985807568777, 20548.182421989135, 20569.118384135072, 20569.409395913193, 20576.252876313498, 20669.49591638097, 20700.983749023013, 20718.33821204389, 20799.80224235882, 20800.34358984782, 20821.4456220005, 20864.35195362148, 20910.935512050943, 20974.210937451087, 20980.5336872613, 21014.757742247704, 21019.504318692176, 21032.06857790089, 21094.25810190838, 21109.224088826773, 21109.275683669184, 21151.604200708513, 21162.526796066293, 21196.382850209433, 21197.933739409527, 21212.997601570754, 21230.788476320235, 21233.8035786366, 21375.645693257473, 21383.433006780535, 21480.678313330485, 21513.590967931465, 21552.06949931635, 21578.665178851, 21600.34701475239, 21634.006577276203, 21641.56572009482, 21654.377017303756, 21705.177361213806, 21718.212412226363, 21723.923316619628, 21732.384378837487, 21748.466053983626, 21784.183801730036, 21795.57043783214, 21816.947724246893, 21832.86939879643, 21942.9117936656, 22011.08246902057, 22029.502218611236, 22120.99160646526, 22124.19386020657, 22149.953456463736, 22213.125873052388, 22214.816733539163, 22217.652529150142, 22229.838279705877, 22245.311390284784, 22263.105545643786, 22272.28776252093, 22337.950160732904, 22352.570475646615, 22392.39626895898, 22475.92423394329, 22506.39214307269, 22557.17550501763, 22582.34857792868, 22600.691971417302, 22611.939266537705, 22612.111131935493, 22612.720300359404, 22618.4248601619, 22631.07332242527, 22636.732071453953, 22684.328721297297, 22744.39040081067, 22745.98927274691, 22765.135061742087, 22779.511647391297, 22783.078096439873, 22807.910994715126, 22814.19509111807, 22835.69542721341, 22917.368182199934, 22972.93821700456, 23006.74660378876, 23034.11822609903, 23045.591353815787, 23057.303948518373, 23067.08685645914, 23096.32395260154, 23152.016431187567, 23174.053608540144, 23196.56445094284, 23216.052452690532, 23218.30093566124, 23230.93039176186, 23248.000556179486, 23315.848007457487, 23396.872671771813, 23427.814605315714, 23435.168641807766, 23447.176369060755, 23456.928238631786, 23489.79716524854, 23503.40882013054, 23535.943452267744, 23547.928327867976, 23548.17288122879, 23568.639567344493, 23639.56597301952, 23650.361908242252, 23650.967203730925, 23713.312801009455, 23727.1162246329, 23750.50200021043, 23761.8272533205, 23767.26119822328, 23808.160184722256, 23816.484204805158, 23820.50463365641, 23857.215420972992, 23858.899657085796, 23859.66067045391, 23875.481551335142, 23899.100724021515, 23928.530891211005, 23958.730279369713, 23973.183379883812, 24027.47150784489, 24064.895930936476, 24072.932096317396, 24076.042564135143, 24121.273017931577, 24203.56780940043, 24288.99092766956, 24296.847341996105, 24300.267319685256, 24300.501992610207, 24359.204555021133, 24360.01904963366, 24384.837601858646, 24397.001017129638, 24404.514365631316, 24425.442842245866, 24451.89905864562, 24456.6964956194, 24465.84777966393, 24467.17926759083, 24469.414548058892, 24508.372867050784, 24512.61765879155, 24569.868305177362, 24684.91127805994, 24694.822607245187, 24708.516896883662, 24709.353940213678, 24717.520441076944, 24719.539277600674, 24729.015110029104, 24772.227627751618, 24801.496025415956, 24806.057722434598, 24825.509002600807, 24835.337826903356, 24849.530431863117, 24894.656316052173, 24904.258916617004, 24916.345377974743, 24948.046489991422, 25057.240486342194, 25132.373105196166, 25151.24802626569, 25154.00759653718, 25155.701646371042, 25168.43367760573, 25220.359463237837, 25229.747549031523, 25244.12427479691, 25332.622548136158, 25342.80190242572, 25345.319505739826, 25363.75974608773, 25368.91660806966, 25409.29230939969, 25414.659821917638, 25520.08131489136, 25531.194634329575, 25531.55219555331, 25553.438945892747, 25580.9604035218, 25590.32971504825, 25591.51098289693, 25591.91762445393, 25620.514269805564, 25630.134663957295, 25660.433683704887, 25705.820233972143, 25713.50099095688, 25745.371583708016, 25746.67798906446, 25771.097349009637, 25776.80039485444, 25785.494719159684, 25817.314311886264, 25819.81875698217, 25827.145575429928, 25840.483562350153, 25902.12258288349, 25918.798224442817, 25960.204210737942, 26004.673919239525, 26058.9322409378, 26071.441627109634, 26090.527906613293, 26115.42674373372, 26115.959067391428, 26153.41992563996, 26158.91249938069, 26165.527544018223, 26166.458235627557, 26171.565185503503, 26186.90868883108, 26194.40785525915, 26224.315853993827, 26225.21873559195, 26245.1926027793, 26256.122932272676, 26263.364967483583, 26313.543898691656, 26334.598666359605, 26360.077715114643, 26360.258504119385, 26379.066519166372, 26392.747257093954, 26409.483127299063, 26445.44752841877, 26480.37483157179, 26484.431694723662, 26531.895641992574, 26579.02074286286, 26589.901711381473, 26608.81794500539, 26634.09919258376, 26694.913224375705, 26716.9815274802, 26719.6012684636, 26733.49900409709, 26878.27044285712, 26917.994738278532, 26928.392542200283, 26932.941279944593, 26939.101025509233, 26947.724980175422, 26986.560239121696, 27006.561444590116, 27054.980884683442, 27075.939286933757, 27103.660650659513, 27112.530148994345, 27147.464335900688, 27194.38501215545, 27256.757160025543, 27284.91183000962, 27334.241384564164, 27352.374391306705, 27357.881562276903, 27371.006812944077, 27431.939800662734, 27518.777374129797, 27529.607433250538, 27540.911611186064, 27542.749525094296, 27549.900148632496, 27569.133724831598, 27608.840676273383, 27656.326826049783, 27741.388626870288, 27760.125373531202, 27764.601298378428, 27788.81528716858, 27803.785400080364, 27851.29360760802, 27865.27593885703, 27917.919927367864, 27919.47709667559, 27948.75289945396, 27974.910855236692, 28064.124722352983, 28073.605329705377, 28075.030671218014, 28076.217137202213, 28127.778273114403, 28155.685550860613, 28169.245569732393, 28206.666323876096, 28237.022139661083, 28298.577250651262, 28358.42700878226, 28363.868378442316, 28383.75435326686, 28421.298292253075, 28434.096815026955, 28453.759678492912, 28469.704484341786, 28494.66018243136, 28526.77253262889, 28528.490470648045, 28556.928193783897, 28563.188241028234, 28572.095692714094, 28599.252816706532, 28616.12850158588, 28618.38564186661, 28629.272163422258, 28631.458058313725, 28691.033300211806, 28700.366020717498, 28712.093309391286, 28736.731422094053, 28813.727555178946, 28822.49200940547, 28884.640049495683, 28912.184889811644, 28915.741588979497, 28917.92818903537, 29006.338517467575, 29041.425792765054, 29101.622124025285, 29102.94958598579, 29110.249674302228, 29122.288708363263, 29186.104665972245, 29209.223526568294, 29231.99429233976, 29269.328489671338, 29278.30296101643, 29284.287191607713, 29309.278562810527, 29320.195868310435, 29323.839569914748, 29336.652244093526, 29361.389509425873, 29386.779490246525, 29388.452437897784, 29419.390681866902, 29426.900252836193, 29516.05232641354, 29534.76991936217, 29549.473153266455, 29594.090602410735, 29607.41097224813, 29737.032062773233, 29743.246247458606, 29792.73079853615, 29831.836733007734, 29861.77209316741, 29862.931206207326, 29891.639182456132, 29901.27534273146, 29904.912912560616, 29970.086960868466, 29971.580381929165, 29991.360141776746, 30000.32597480223, 30084.62279483322, 30089.870439459308, 30100.738159729317, 30100.95654345676, 30115.755512619682, 30118.123972287063, 30138.622681179993, 30141.551141528966, 30173.375562008827]


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

