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

    min_val_1 = 10004.634986842146     #min(X1)
    max_val_1 = 64249.394545970434      #max(X1)


    X111111_1 = [10006.30704230171, 10011.854561033842, 10083.60460125709, 10094.874915304716, 10101.873655458961, 10154.103978440065, 10202.309179384265, 10300.653592863639, 10308.542113648444, 10348.325724709935, 10395.683093123092, 10400.643012273342, 10486.792515304774, 10590.555198768063, 10602.101428694392, 10668.387380026023, 10725.734025608625, 10770.291914470896, 10862.78679775398, 10891.978662865065, 10911.043980404042, 10919.66912620726, 10954.829548692032, 10980.367646469684, 10988.63272347355, 11007.657359930787, 11053.142844156553, 11109.929689052879, 11132.004860899093, 11139.899442268212, 11150.757620560733, 11157.675931627522, 11208.54085755878, 11267.927309364135, 11361.950607182263, 11384.823641859088, 11408.253367850157, 11461.023860144864, 11500.958479539164, 11551.078453233808, 11644.162134495076, 11657.51944004176, 11661.783932765195, 11694.24714754348, 11703.38174835711, 11812.122027189911, 11923.01298771134, 11971.23208716444, 12014.804767032743, 12090.339366439875, 12196.817489175708, 12229.904040843961, 12265.480016009857, 12289.371537034041, 12312.225904822857, 12312.418019843, 12470.492314775789, 12558.950174093674, 12660.796595606544, 12663.5519651166, 12675.726032575, 12749.939933980115, 12787.741681930613, 12836.20610250266, 12857.660217654828, 12903.25737418792, 12904.387822546869, 12906.565560854087, 12917.864492244018, 12967.713420639238, 12975.98002428656, 13064.048394905554, 13093.231907425365, 13096.724457774588, 13225.65917268652, 13254.157312604304, 13475.880080265251, 13502.289637023758, 13511.411682416523, 13534.40355431913, 13603.627739202799, 13634.422770990457, 13812.652815577305, 13860.723758431463, 13873.37942972405, 13948.57339008529, 13975.250344560689, 13997.47660838961, 14163.438481468584, 14168.092397911369, 14233.610370002914, 14235.940813951816, 14260.982060409337, 14311.858609274792, 14351.833064185124, 14411.939362018638, 14424.469584100952, 14467.110548538729, 14479.461851714448, 14484.501053484457, 14506.306020847005, 14512.416984207754, 14516.844763002922, 14553.399317189102, 14570.297566376688, 14708.844112221694, 14714.942739509934, 14760.471139786303, 14858.734651936615, 14878.471563981057, 14903.361971122686, 14944.18731380273, 15073.800772542814, 15114.603231958827, 15164.452718094108, 15167.296716731915, 15198.498842045035, 15313.556294423799, 15329.057436229064, 15424.560178520793, 15424.58573383898, 15447.33940569705, 15498.782204199353, 15542.411435082333, 15664.54766144395, 15695.196500205493, 15717.562714125841, 15769.100932537523, 15796.58913499273, 15818.679218275112, 15829.119952123485, 15838.449676356531, 15900.331119812872, 15980.123605145121, 16005.597245059485, 16058.724326585721, 16065.364178586653, 16084.021077295289, 16086.883473615533, 16171.600620206968, 16346.907541480516, 16480.36273712953, 16484.783957684773, 16613.577581462436, 16632.447780314513, 16730.581656624865, 16774.334385801718, 16858.707919052948, 16912.081408093567, 16923.966905521076, 16925.098744353712, 16925.29025031301, 16981.42959021979, 17042.639029693317, 17068.165366612946, 17114.69194782579, 17135.42473814257, 17161.527347770992, 17171.73352292038, 17182.70913613924, 17193.45217258954, 17213.137039998423, 17236.007577327924, 17352.872232116806, 17389.368280141116, 17434.21788667285, 17512.917096920224, 17547.676130069816, 17551.225470838406, 17565.756536899662, 17570.052147284612, 17571.86017446947, 17572.06359317436, 17582.483532422037, 17604.849393019467, 17655.88772527522, 17842.80053757784, 17848.973363442714, 17882.94893687388, 17986.245762259143, 17990.108045417277, 18056.39944101314, 18067.89280639758, 18106.045353290836, 18137.976956493476, 18203.60311702128, 18223.06234813755, 18226.283114129736, 18370.254260044712, 18401.448493261443, 18481.090258189135, 18532.182720871613, 18547.80113548074, 18559.271182295808, 18830.06292826014, 18926.50403610285, 18939.469996114953, 18981.288565719755, 19144.03415887479, 19277.039798514717, 19377.49577691126, 19385.38605429874, 19425.20741577612, 19484.262974206453, 19509.69886552568, 19578.799763035582, 19851.629067557893, 19885.09317151335, 19921.90542439669, 20005.168054687874, 20034.679781164334, 20122.26945648253, 20135.652796860682, 20140.423624620104, 20314.3695473923, 20314.595658147577, 20315.50873510595, 20388.173720618324, 20437.9039933448, 20454.750171646265, 20506.38149570919, 20565.547246110873, 20579.706830786585, 20662.201549959165, 20728.389394632748, 20863.12873305835, 20865.40674298688, 20950.06027566911, 20975.158527092848, 20984.538553380662, 21089.39093219157, 21110.417062845256, 21151.20064936969, 21175.76816724895, 21364.58386043519, 21410.977889597772, 21443.967619832147, 21444.728622998227, 21500.654753826377, 21505.397567074746, 21513.64264549009, 21637.415795126297, 21649.019988005075, 21660.437369225052, 21827.512611021917, 21875.411814318824, 21881.482487321333, 21938.515266255497, 21977.527064613365, 22019.96662694862, 22045.33719374093, 22189.852356614123, 22191.36873208292, 22287.737519845883, 22368.694446967405, 22423.728037277335, 22469.743650269316, 22547.355229949775, 22548.520494441684, 22580.902818475886, 22680.78221015556, 22716.467543779054, 22749.64501769325, 22813.831637729258, 22865.181304033737, 22882.322054725555, 22958.651573741976, 23014.05705130448, 23025.86659472633, 23194.096752718615, 23249.3221203696, 23312.829276772616, 23373.584030337857, 23451.0235309572, 23482.637129015264, 23500.780407881175, 23502.08328505415, 23560.581325813742, 23611.259408476726, 23705.984664725373, 23776.560598501397, 23826.020652407882, 23830.95654566263, 23859.685337890332, 23886.53046451699, 23923.360325799957, 23957.44998969628, 23967.18243023254, 24042.02987972593, 24163.18423745571, 24224.818020034167, 24256.346807682254, 24269.47677503957, 24389.315729010617, 24427.972485455783, 24448.648253295956, 24452.509257228645, 24468.431900079133, 24529.549035809257, 24618.3285832204, 24636.96024284087, 24641.429171536318, 24683.438705089426, 24720.414267986438, 24743.79014413937, 24865.20217595179, 24881.93102034601, 24899.1214922479, 24996.599528422517, 25180.765605914028, 25202.532177757203, 25241.015436044276, 25273.789885262784, 25308.96760377758, 25340.1614521163, 25489.046419140323, 25501.209858922244, 25559.02564239005, 25586.872642264767, 25915.03631480382, 26005.747099912347, 26066.631295153245, 26128.665938302307, 26311.685754407794, 26343.99796373863, 26361.01774079586, 26426.835992134584, 26512.18498646191, 26523.874381218677, 26574.202295922027, 26612.903617640928, 26615.257712635634, 26648.361331208125, 26662.750741516444, 26713.08094403652, 26799.740537735663, 26852.779593285562, 26907.900263349617, 27060.958151770796, 27076.580030980498, 27169.614038525815, 27212.80658095256, 27482.9217491822, 27532.483371751452, 27563.670977381105, 27589.0249044423, 27596.180521768434, 27693.548464610976, 27772.604838180625, 27796.66046697078, 27833.152963642024, 27846.924959073465, 27902.596244181525, 27984.203834787513, 28040.13470203778, 28053.042119202168, 28198.827030346703, 28219.37190605869, 28278.83089047578, 28307.868929717144, 28309.631087963695, 28364.911257183754, 28367.895271089994, 28375.70952247336, 28414.778461576538, 28435.12790316136, 28464.709060411522, 28551.345981217037, 28632.170416965695, 28642.420008473928, 28728.26857213777, 28867.47581493854, 28896.152487897532, 28944.127340648996, 28997.64413891269, 29026.554582899065, 29140.951971628016, 29173.621647982887, 29175.415778437913, 29231.825390267542, 29254.84017357336, 29327.627205890985, 29435.345348053605, 29487.163320175718, 29491.294087578113, 29518.766575830254, 29559.471614343456, 29574.726012523613, 29615.65442856647, 29635.359947961337, 29637.390742322812, 29677.86958858476, 29725.31359800732, 29819.35600460228, 29821.77524919492, 29873.465747290105, 29877.03340398924, 29883.099188734217, 29907.14684753851, 29967.776868348024, 29975.166391563045, 29994.788625902944, 30127.25121654253, 30219.29375906494, 30452.204713090716, 30465.902853900465, 30584.84238774994, 30602.64494497961, 30621.1268761266, 30679.680705573104, 30688.735420180048, 30777.876636143643, 30779.919410399394, 30786.14882839035, 30859.5314632692, 30959.01874813935, 31065.22162834314, 31131.050137551047, 31132.093031794157, 31178.13355736323, 31233.716636868787, 31236.465955218457, 31415.228887978064, 31455.67196858908, 31468.261070413857, 31478.387744872474, 31723.254252488492, 31756.658138407667, 31778.357995530423, 31856.994529531403, 31884.58690993902, 31934.541975933473, 31949.742391237243, 31955.666644824312, 31998.81955201957, 32023.56273889193, 32154.256909372132, 32205.08839487727, 32260.69941099392, 32298.91828325545, 32334.980577148748, 32338.60566097173, 32591.065981027517, 32686.911400947447, 32733.88904647286, 32850.276484801645, 32880.00689004981, 32920.94582477595, 32932.29807752439, 32951.75177891922, 33058.30909320105, 33142.2438487835, 33217.090797218574, 33276.28481815374, 33394.6187411098, 33449.331600379366, 33454.16456729798, 33468.04551271162, 33489.61049595924, 33506.4370295478, 33600.82261301497, 33609.637336851076, 33632.92133337333, 33638.13195745347, 33642.34738884865, 33718.59084623127, 33781.39004290373, 33858.703998410536, 33871.44899088539, 33923.185820575265, 33998.189055161376, 34104.16772432363, 34120.301840546745, 34177.89871614019, 34182.14136884481, 34302.69690357445, 34323.733687436674, 34338.13915487383, 34375.50882257544, 34427.50767269729, 34433.353501474936, 34487.633839548595, 34543.278536780075, 34564.2851913126, 34710.14176000033, 34788.213067106706, 34809.50563829062, 34824.13962178062, 34847.23886303519, 34865.79735509406, 34909.94757960175, 34968.29906957326, 34989.01287929608, 35003.69600611231, 35027.22784439362, 35041.74136840973, 35066.96721220427, 35131.84180669964, 35194.90705238965, 35218.03570775673, 35301.345675416, 35310.977539576605, 35321.851505624734, 35440.37475207391, 35468.20502708022, 35509.665095543765, 35583.11548686265, 35675.84826274942, 35691.5418561916, 35702.28802363052, 35777.79538811079, 35877.400149417066, 35931.72782750064, 36000.701707426466, 36008.05563619911, 36009.39782134923, 36014.57593522962, 36036.88347183954, 36045.306427736825, 36150.29280378159, 36166.7935071246, 36335.50749748562, 36364.910005581965, 36482.57856501008, 36683.165944556284, 36723.778024632775, 36731.36732659601, 36746.06163755736, 36748.885302044524, 36758.91428951778, 36769.938160327816, 36833.75174702502, 36866.288342668515, 36943.71242948805, 36956.44733167149, 37060.05649805903, 37093.47557588651, 37111.174543648434, 37222.06815604654, 37277.21273203615, 37299.215335395216, 37439.738453955506, 37459.76526895909, 37607.12552026086, 37656.93581598276, 37800.05912278753, 37824.74649704357, 37850.37221773305, 37994.511288905574, 38019.54053997702, 38129.774362653465, 38185.22193271773, 38208.745341807706, 38217.88956852806, 38363.598148058954, 38425.4649613433, 38461.546104682566, 38519.06441451637, 38667.83294712573, 38691.44102443499, 38694.589216352724, 38796.78236817004, 38888.788293810445, 38907.27503949215, 38965.44089208037, 38966.01826499802, 38978.62064940464, 39029.75754890227, 39120.11677716326, 39164.03147518884, 39202.54698374958, 39422.770049610524, 39426.47830398223, 39441.51923821251, 39573.347385483445, 39692.700144467235, 39851.39433166079, 39985.8641376923, 40052.359933848755, 40058.89572942351, 40062.805946583496, 40095.2939846824, 40188.15179118788, 40188.91979381944, 40274.82682178706, 40346.85777665361, 40386.00024586682, 40405.78320428074, 40407.80993426705, 40554.276957652546, 40700.90660083704, 40880.61931114179, 40894.849297035435, 40963.73701279567, 40974.36377779053, 41043.98229933623, 41138.25467181575, 41244.455243169214, 41270.23479775607, 41393.656860940406, 41399.3691972501, 41409.67779919732, 41496.361940859104, 41649.625473914755, 41908.73376297609, 42000.50943472605, 42035.000522559625, 42043.90854610093, 42093.98362062295, 42094.5834492227, 42104.103042529125, 42152.73745958919, 42281.0499192143, 42451.97196315767, 42650.9542638741, 42655.41151740162, 42719.7253269547, 42737.33233124108, 42757.5612934457, 42769.64779214178, 43103.626377356246, 43245.46279647328, 43292.78388881735, 43324.92195125049, 43372.283016169684, 43450.75888688778, 43501.47958913427, 43599.39018650692, 43674.30897187039, 43836.96959272802, 44001.84804312065, 44106.370791011956, 44207.58699559342, 44307.91166024046, 44358.48081047252, 44371.754438621836, 44457.72051791137, 44480.691680210904, 44484.89638346531, 44549.08695562309, 44550.76440234168, 44556.96970608416, 44667.46688415636, 44711.329738908564, 44743.95088811152, 44849.14954039703, 44918.39339097362, 44977.96914960306, 45382.66918796363, 45463.453978756566, 45564.14573572165, 45570.6403046655, 45630.342786358786, 45635.86550447722, 45735.269337636135, 45754.6956178547, 45879.69200499884, 45957.92902127731, 46004.84739221239, 46089.96142069371, 46161.83668257144, 46223.23161693382, 46242.95780522485, 46286.75911822695, 46293.679224921405, 46431.1673942214, 46470.90429956667, 46566.318167523794, 46783.24982516443, 46815.13029101669, 47010.0044827478, 47140.38424958298, 47189.75652052446, 47207.63260117792, 47211.42094578954, 47227.08426144514, 47257.82672421552, 47360.3084065125, 47361.4618878325, 47454.663572907986, 47487.61617409795, 47511.501815737756, 47557.66068536569, 47580.53672795056, 47581.195453135486, 47659.4979719745, 47684.938416822406, 47745.563804449615, 47746.07167909189, 47810.29770383088, 47874.33394469646, 47980.82158662064, 47992.56985154973, 48030.467494356075, 48061.565536079215, 48076.91307018186, 48130.91640242822, 48159.70945579018, 48168.649883192775, 48219.72375797872, 48297.014756464654, 48313.65576578405, 48465.06301427846, 48514.303903200096, 48525.6954035784, 48571.70897345097, 48835.941459325164, 48840.769694817776, 48842.06904361325, 48969.26781826784, 48971.287913618056, 49006.48212503155, 49017.071530106216, 49124.38100725023, 49238.03172375081, 49291.29678789811, 49351.91605930424, 49494.827509244315, 49519.917513903405, 49598.1097015167, 49687.99953862005, 49828.2258773654, 49868.71482668799, 49923.49068997845, 49951.97502547103, 50032.23845278319, 50033.5761145885, 50056.442453905234, 50083.93666869898, 50106.58585997318, 50135.65024867735, 50206.86608937266, 50552.26320259589, 50613.53407456085, 50624.068274045574, 50644.51825723496, 50660.43547563388, 50670.20397648679, 50762.56953315729, 50795.67573171803, 50851.177691968864, 50863.32425206927, 50880.20103243268, 51063.75576546742, 51093.25666236143, 51151.04691756606, 51153.022757621104, 51166.83609777031, 51342.06924416902, 51388.39674050986, 51392.075041377524, 51419.22100597223, 51479.0848272803, 51524.65579911908, 51561.77411669564, 51597.39609954912, 51603.22775731551, 51671.523825175595, 51785.40052933228, 51830.20979736067, 51947.41909517782, 51966.06655864244, 51972.215794861426, 52072.43272839249, 52085.76822619119, 52132.19838123288, 52136.61288897092, 52185.0535904896, 52326.510081835615, 52338.77941817141, 52349.07977844363, 52372.70976807833, 52374.38872155404, 52376.312268544025, 52403.0105865736, 52428.47007347922, 52436.25143623741, 52495.67671279011, 52583.92558887028, 52589.85904217404, 52603.85410524525, 52633.51812691133, 52790.88472899868, 52858.67020510973, 52980.84834871375, 53033.70579552944, 53056.13846281865, 53128.32657874974, 53140.085883991196, 53155.39320630756, 53185.17536538678, 53211.28859512033, 53280.75692581799, 53283.892788433935, 53388.895490355826, 53434.84698730112, 53442.40392355498, 53468.47589210371, 53656.72882571462, 53699.89820742638, 53714.85599342611, 53756.73923286516, 53779.51251480009, 53925.487275496416, 54139.2293682743, 54147.84629319535, 54171.70677974657, 54185.654352366284, 54281.32897587529, 54291.13204488504, 54309.11038467692, 54321.36383022955, 54330.28351252496, 54644.55262075191, 54714.988414944, 54736.372165619134, 54828.77550814803, 55032.14323785728, 55041.78400982438, 55090.56054342652, 55103.25372295925, 55104.44693074762, 55110.680010955955, 55170.22185167929, 55203.63352326361, 55277.80648929104, 55280.33065693262, 55356.5654630547, 55387.391385260235, 55392.55225151428, 55487.59278463283, 55494.246378921016, 55576.97689419499, 55646.397878264834, 55817.66474872337, 55826.93077820438, 55829.237862551505, 55866.729806414696, 55886.83590031023, 55915.4048403171, 55928.32206952924, 55934.41910748553, 55937.951959452694, 55966.89072488489, 56002.583455269676, 56141.40485513467, 56330.15969040254, 56334.60215569477, 56340.05987732515, 56379.61029445296, 56459.42447670654, 56530.827647878235, 56565.527596880274, 56577.28621568734, 56603.88806026114, 56606.4693044345, 56615.74564234599, 56617.79024208644, 56746.07492234873, 56788.42645856097, 56902.94444832678, 56925.981596900725, 56958.607636257315, 56997.582485246756, 57009.78496893059, 57048.224143232146, 57079.90842215803, 57104.22853307983, 57114.634368944666, 57147.929774420045, 57168.74416839676, 57283.34853053503, 57343.635068094336, 57396.07935144919, 57416.251956069245, 57477.06521850795, 57569.114924589754, 57700.73710536431, 57956.15200002021, 58169.558524588814, 58237.263250784614, 58247.100318851466, 58334.41541276554, 58422.49242323826, 58491.150883213064, 58523.59157908078, 58548.56889414785, 58566.972043379596, 58596.23532630946, 58613.22117563371, 58654.26877698118, 58674.87725017479, 58675.051960362274, 58690.59835096145, 58702.92284993246, 58837.14913102326, 58839.61543102454, 58869.934907479466, 58923.66551045549, 58976.29948287991, 58977.27694461903, 59126.31685144218, 59248.42209561682, 59253.35635234088, 59289.75714012267, 59347.479751975065, 59358.482369811005, 59365.22797821072, 59398.64872046851, 59450.3268479923, 59480.09628949999, 59485.47937833339, 59495.03396696176, 59501.56911792074, 59753.06453009469, 59753.59169188891, 59758.638551432596, 59869.735398294935, 60018.88563074457, 60041.6699090711, 60070.55739541901, 60205.11179684378, 60237.07002518282, 60296.54553596132, 60322.18804782806, 60331.85604945697, 60337.84546649888, 60390.15547952478, 60427.72503693366, 60428.98123390383, 60432.88181915467, 60466.04131125634, 60580.24032062104, 60768.625199633214, 60795.325350878666, 60888.249273131965, 60942.168154564475, 60954.21573066107, 61128.74240596031, 61148.10471642012, 61188.47844263343, 61193.07449653289, 61199.479915177675, 61225.174275073, 61233.34916765144, 61286.10217560165, 61303.32631245164, 61341.28228452723, 61347.019652563155, 61373.65902851691, 61459.742963075616, 61504.00242389495, 61512.066356308715, 61569.75127224405, 61689.88674040178, 61739.01780943619, 61801.86610070198, 61847.07285081582, 61887.23680539804, 61961.71483968872, 61989.267461411706, 62051.06414572221, 62052.983212422354, 62068.948653011066, 62218.22286967, 62263.44551115574, 62278.01330868566, 62378.29734214925, 62459.410953699284, 62623.26406152529, 62638.43893883919, 62763.093032301585, 62798.156995424964, 62812.91548203439, 62814.999367978635, 62881.181461571505, 62955.823107513796, 62987.03710479718, 63054.23178688857, 63061.35176035324, 63083.97119294321, 63112.110233286985, 63267.53407440049, 63287.53787211865, 63364.82650250827, 63455.66397822204, 63520.10674964886, 63589.9414512879, 63640.85342223038, 63688.326166292194, 63709.954800798005, 63727.18012205119, 63787.62897643059, 63885.24919971106, 64033.1332596129, 64165.165875180275, 64166.14004116533, 64211.83611139919, 64214.996647327556, 64245.12464621427]



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

    X111111_1 = [10018.966404141795, 10042.11580963805, 10090.858173239392, 10219.495390897551, 10241.652256028698, 10312.787070862092, 10401.993631399746, 10433.663308789306, 10435.459477523775, 10593.186965491963, 10599.828891836276, 10647.359036732483, 10658.908089789458, 10661.863948766844, 10663.55998722123, 10760.301160332487, 10779.902897403783, 11162.445089257606, 11175.628890787142, 11219.326808505175, 11344.881292680257, 11417.930384243546, 11500.984305918544, 11518.428391101239, 11635.313089743659, 11644.1762619814, 11683.573448508414, 11868.272110020787, 11909.416212582524, 11968.72066394056, 12116.91125854586, 12235.544642643226, 12248.45943706593, 12314.66083741117, 12442.551282510396, 12529.247750600614, 12537.89798964484, 12555.296519778796, 12705.648477098499, 12785.144258864648, 12816.374228242472, 12886.365608906344, 12910.561433426168, 12999.649388521366, 13009.893351745843, 13064.657720093724, 13128.977166997054, 13183.939826524032, 13185.775582211209, 13197.243823418294, 13208.078713634372, 13266.748977008492, 13288.050374226936, 13299.80300166996, 13332.323543744133, 13465.426814019174, 13482.868919907745, 13497.25938089734, 13542.106093893817, 13545.368947936578, 13545.890601118597, 13636.749426123864, 13641.614436094018, 13677.03710544165, 13708.563012155168, 13709.411987136726, 13720.106344483915, 13735.36005652455, 13751.668131882052, 13773.344423375034, 13807.784242888763, 14091.789758102723, 14115.146778461887, 14125.965743069693, 14137.32042023031, 14291.046785809214, 14304.659582130591, 14506.836450267929, 14545.951715668172, 14576.283223638547, 14695.209198711664, 14695.649564922598, 14769.765712335078, 14791.053187839516, 14842.040556154487, 14881.861165722948, 14892.488994878553, 14995.928191010726, 15027.190979962848, 15056.658677224068, 15181.734356356752, 15187.121555501077, 15216.286983640915, 15250.171548117276, 15275.871390697213, 15342.712293871118, 15426.97109828803, 15480.881206233484, 15569.676952877522, 15672.008614356968, 15695.625577366336, 15722.122752051007, 15774.052367121509, 15775.750409277098, 15786.828184497837, 15800.549956734336, 15830.446808166758, 15857.494846275964, 15932.648957798112, 15935.16104444745, 16022.974965139925, 16059.648339626325, 16170.716574006186, 16174.124300092957, 16191.233466523106, 16196.894516890537, 16205.822271555051, 16310.940500859542, 16364.687708119125, 16440.887326562377, 16452.00814360751, 16457.674895693995, 16487.19261366976, 16510.0525055073, 16546.507063352783, 16579.21620495156, 16615.231848423602, 16631.64142879903, 16640.591847626354, 16647.275987469107, 16768.5427980239, 16793.35508475364, 16805.706260843923, 16827.184931281496, 16832.560221299213, 16878.914240241054, 16890.326556152195, 16912.727457440098, 16975.485140347588, 16975.844047288243, 16998.256457345404, 17001.897010015047, 17018.121039061483, 17040.529294732445, 17064.82430616484, 17294.058073098455, 17311.18736371737, 17327.120008447117, 17350.893288735046, 17429.540197633727, 17495.72788207361, 17525.513977194823, 17618.070821463614, 17719.003632259828, 17723.21760951142, 17786.918412775995, 17809.33714863812, 17860.04356260593, 18101.385415086614, 18158.63128068703, 18249.610639999148, 18353.253302579596, 18373.4312658831, 18400.290434391856, 18408.064435726134, 18417.437644583693, 18484.370479519206, 18493.62462978188, 18587.822496265042, 18684.164230276292, 18686.58270705395, 18734.109483620414, 18773.968001217123, 18790.12422078659, 19108.885247592876, 19109.812201241137, 19188.64837467561, 19196.691056970467, 19281.61923080324, 19580.017342855128, 19677.71414580218, 19844.289405484073, 19924.54161384452, 20049.033207740824, 20050.99344756677, 20150.968346094913, 20167.137943664842, 20208.775105580746, 20303.940458007346, 20357.47527234631, 20434.59252900775, 20467.812672461994, 20554.398863379414, 20732.653884957577, 20777.17365617442, 20777.588861008386, 20838.703220534422, 20844.424199890003, 20852.194972447898, 20869.373436184163, 20923.839814697847, 20992.74132439494, 21087.474375609112, 21118.89083905588, 21155.533904727476, 21184.74684992063, 21191.554111051966, 21228.894325741327, 21275.065587907335, 21291.312185422597, 21299.726299905884, 21302.912323357305, 21383.869975180583, 21406.845612705787, 21410.33650878524, 21423.028074789396, 21434.366944903195, 21469.02647629148, 21519.75992003553, 21546.059875237956, 21548.013507662872, 21604.01223845899, 21606.196696399435, 21651.23484470038, 21715.746963414895, 21803.972885982388, 21900.07496638375, 21956.597329163327, 21988.251656543023, 21995.84865992501, 22052.327854309562, 22131.158428875606, 22135.23762177739, 22148.308333402292, 22247.814896983837, 22266.644428973013, 22441.284915625183, 22452.71423439346, 22551.640399317395, 22598.853715426834, 22626.78836868813, 22633.896937449197, 22726.453266389035, 22899.4261128832, 22950.6029995039, 22997.202778276504, 23019.71554194169, 23051.66018164558, 23177.448916327085, 23244.10136224744, 23287.611540923106, 23290.630494180263, 23443.59756428577, 23505.05688502071, 23593.819050492228, 23616.54774771704, 23716.26799485909, 23762.827605165534, 23765.624763577187, 23816.26928245886, 23876.520790412076, 23900.108120144003, 23932.593955820834, 24092.346638610015, 24107.66418042613, 24121.72942924408, 24197.967445742976, 24258.764356782067, 24392.723414468743, 24422.225416027475, 24475.805767208283, 24524.369593418916, 24553.171290996877, 24600.262165349224, 24694.247656510495, 24725.23808713642, 24739.56183164986, 24764.09818895853, 24832.852579390885, 24888.08405324415, 24912.89218753499, 24944.917294032668, 24970.48608355535, 25088.996768328634, 25101.036407691372, 25185.241803300152, 25250.226246841426, 25307.07484017688, 25342.305687582688, 25355.596704929038, 25526.193285582525, 25570.893011789434, 25648.0565369737, 25762.287903441174, 25773.349308605677, 25919.03458192743, 25945.42374099108, 26044.568643527447, 26092.154034214484, 26093.61801184994, 26133.49359720624, 26173.396353798722, 26217.579326630726, 26233.086312420168, 26268.21760739501, 26402.445316620975, 26410.933670806207, 26432.416062099262, 26507.487727134852, 26516.958651246518, 26577.83812033104, 26584.463163806646, 26628.919886015574, 26660.20533718063, 26734.547604602365, 26766.609650737526, 26840.4261677548, 26924.24377538171, 26965.530701160405, 27004.512916871274, 27031.685385594174, 27098.56173619675, 27311.09208976176, 27356.275487044208, 27464.551280947257, 27483.302182897347, 27496.137085920185, 27560.637905740863, 27647.484824164574, 27833.77219151431, 27873.39806824708, 27877.217820599133, 27931.013065317027, 28027.12980145533, 28074.984365989214, 28101.41149679448, 28113.876108298078, 28137.674806097166, 28169.036961442704, 28287.395313807585, 28289.637109432802, 28294.65704961141, 28339.48390806943, 28418.18165276111, 28458.735597611718, 28491.84062282298, 28722.786879021867, 28887.876948653065, 28896.827031611298, 28908.463001036722, 28972.749545323648, 28999.083939895638, 29106.650931711527, 29136.34473869762, 29166.26115615828, 29217.28481779632, 29317.109704312585, 29335.241459188226, 29336.785320176066, 29359.67921414634, 29380.644898582632, 29409.781096730017, 29516.550103949387, 29578.40677343983, 29615.786771641295, 29728.93989298308, 29769.187488413605, 29840.311019458466, 29873.56676608948, 29881.242583695966, 29970.87654836525, 30136.44229808632, 30195.087397810566, 30225.73699652363, 30338.19926924787, 30376.577566447315, 30435.82169782139, 30571.86972947143, 30616.208090762528, 30652.407885537363, 30681.040366548554, 30715.510602853017, 30739.156545656653, 30772.376768940572, 30773.071768054608, 30777.862460592718, 30789.412628319744, 30866.83958598544, 30906.791718486213, 30909.25913321901, 30911.55461167414, 30916.5964956967, 30962.292735808278, 30963.07691195067, 31062.703146500873, 31161.102316696437, 31169.263119560885, 31222.536490553757, 31282.537847921692, 31301.19955353743, 31343.05457817242, 31351.688096912643, 31389.989334593676, 31398.717011729117, 31518.059746768333, 31641.88359202644, 31667.10424417156, 31718.48643991417, 31799.54263295599, 31811.041261142407, 31815.10037654936, 31819.93697609554, 31874.517115833478, 31933.784008783812, 31933.921666091777, 31958.87207791622, 32100.673178033092, 32128.25732293046, 32178.426182048956, 32203.724096843296, 32213.232877592014, 32216.75503589556, 32231.403350793655, 32326.097290110854, 32416.261660152657, 32443.517063817355, 32478.942370925277, 32480.098984632088, 32514.586100316363, 32571.322560637687, 32907.69795367696, 33044.176875181896, 33051.493036629094, 33053.46949553618, 33063.693317371246, 33126.512104483045, 33133.429948062025, 33177.59720633742, 33191.8528771612, 33298.03972836629, 33400.885455891585, 33417.828124152526, 33437.77711602058, 33496.05779102372, 33546.88517429927, 33576.82750581069, 33580.597508394494, 33628.07722611152, 33887.86026774725, 33891.86702873824, 33929.02710663647, 33955.7866593012, 33958.20552029407, 34108.96803509773, 34136.580789600055, 34179.973076401126, 34303.56750471775, 34336.87456728508, 34381.09347162585, 34459.282815856364, 34592.36589412758, 34604.876150186785, 34611.43599770119, 34681.08828911777, 34726.695456639616, 34793.579785228794, 34795.83274897083, 34808.08082649728, 34816.425398965235, 34887.19105547451, 34890.624274671194, 34898.66114696555, 34911.132943634395, 34917.65792984973, 34918.15128550178, 34963.39911590055, 35058.83346680147, 35197.01381656609, 35236.7830065744, 35251.092654520064, 35263.40789982268, 35274.16891546932, 35364.69443250388, 35372.63719303267, 35464.04171702414, 35472.258563721305, 35475.25456274488, 35482.30029635946, 35506.95255684978, 35570.85856209514, 35572.395481756845, 35646.992116679874, 35652.28325921246, 35714.49939029985, 35732.43952811136, 35833.45688977532, 35889.556348819286, 35892.73348543557, 35915.613181044246, 35921.73233683835, 35927.97660101819, 36184.84311964732, 36189.143280089025, 36208.97042164359, 36320.225719602946, 36341.67387491262, 36375.10925897308, 36387.528165172494, 36429.99989433393, 36531.77227875894, 36541.69055071777, 36550.156716836194, 36572.303549526754, 36580.84867219927, 36719.045412434345, 36727.21049808084, 36952.291122989525, 37108.77002239197, 37113.92740847973, 37146.74089786863, 37154.901495446335, 37229.71640927797, 37260.77079669741, 37312.35342541478, 37329.97223609235, 37407.43914123685, 37422.12835093172, 37451.3710679981, 37475.34129890954, 37495.94433050735, 37500.03185183667, 37554.35386967017, 37609.56351581664, 37737.598506623886, 37757.809443491715, 37935.94966418695, 37949.300359980174, 38208.5950881097, 38286.64609643513, 38311.164148124844, 38444.87561110275, 38488.77196743908, 38524.58333830268, 38572.77165929976, 38645.83955562892, 38649.689815346195, 38803.03174671252, 38821.57666821612, 38885.001157660576, 38918.24335871695, 38936.46050875663, 39085.267594225224, 39104.54689856825, 39179.793606038875, 39187.109025310405, 39217.29080926893, 39246.61318604744, 39315.026057180075, 39343.553264338785, 39355.82765617412, 39373.352478786095, 39388.94125939613, 39394.33223165545, 39553.190709153685, 39574.75720062261, 39585.05947032207, 39604.955616811334, 39618.52314405082, 39705.502783842225, 39726.3669421261, 39764.68229642656, 39771.573600102754, 39913.36000586138, 39934.19410393503, 39948.24880484186, 39984.32795106385, 40260.07666116861, 40314.15266486339, 40407.574446869476, 40419.46436105408, 40422.21065247417, 40427.025672222866, 40517.885980205654, 40562.566705761594, 40616.434581723785, 40707.75187852958, 40760.777604795134, 40821.56047323042, 40887.35870779292, 40939.43116622372, 40941.62704021449, 40967.97201345483, 41040.349194982424, 41095.25567899521, 41122.29141316584, 41133.03814213732, 41243.84883013503, 41248.80299936073, 41256.9730472987, 41307.185473560574, 41461.72620857443, 41505.303523172115, 41630.52138649388, 41648.75173207988, 41664.632544418026, 41671.58587633387, 41674.27728110482, 41716.3416929361, 41729.18850812457, 41735.012980713545, 41790.90116618876, 41811.4192787552, 41832.83029204712, 41842.75834072205, 42038.25237668006, 42091.97424687066, 42114.03657094322, 42224.54648915082, 42300.29460109951, 42311.649548994406, 42333.44916174641, 42335.43632090568, 42378.61659136202, 42392.975801144414, 42434.78102224651, 42530.26526879909, 42606.20225734113, 42631.20403491425, 42728.75545094935, 42871.89799203116, 42874.19779683743, 42951.96921027724, 42961.971671015, 42997.37056175739, 43003.464266304116, 43005.46263713006, 43151.06094200915, 43245.52780446414, 43287.40974348537, 43378.760319163914, 43450.14034112742, 43463.995520716155, 43665.9250227943, 43676.69656195641, 43680.1132410141, 43841.86969732626, 43848.33545885455, 43962.54176551542, 44062.334227822554, 44069.06390436865, 44071.14635028677, 44113.511873960226, 44117.13364046127, 44140.552913566404, 44316.34277456634, 44354.526887323955, 44414.991733377654, 44440.75533325517, 44455.9780584778, 44467.33096599195, 44665.69130619413, 44768.021693531606, 44780.540473546476, 44833.19280970956, 44884.5372086768, 44915.75592216284, 44962.47250265756, 45110.76940677898, 45112.76627281262, 45162.81135643267, 45206.00870032786, 45210.8317970917, 45284.69197740929, 45386.617351802466, 45551.78768434342, 45628.642411986926, 45646.89637432279, 45683.3833749322, 45717.56918340243, 45740.05737354916, 45804.09737467422, 45864.15325237013, 45965.32881935594, 45980.3601086188, 46076.83566725136, 46106.26513356856, 46142.54718238077, 46187.121708876475, 46398.851222563164, 46437.57897542588, 46574.78199718631, 46600.37043799895, 46622.53873856499, 46639.379787123544, 46641.02608506561, 46644.38723751811, 46710.82610378119, 46716.8526578806, 46740.20936289897, 46836.00094386953, 46891.04070331628, 47002.32491718449, 47043.06271708506, 47248.292429858644, 47255.30894036293, 47268.12503871396, 47356.696498000645, 47396.28176009399, 47414.485309872354, 47429.24772060991, 47508.733239633024, 47510.26698458372, 47520.02807030003, 47608.043386326084, 47673.983623692846, 47758.03968232119, 47765.925723006265, 47830.75876011998, 47831.3849400169, 47874.47218596852, 47892.41793559609, 47897.050347174045, 47903.82994655785, 47970.670680552816, 47988.767060260965, 48007.18513396297, 48010.54652376134, 48064.46843848917, 48198.49094646224, 48288.22927110006, 48418.84175520711, 48496.96411245035, 48591.74815253564, 48671.689886807064, 48692.694101141555, 48797.54608376998, 48845.32765370155, 48973.914612067434, 48991.26557455558, 49091.374926998535, 49108.362386279914, 49108.57672133164, 49133.29187863156, 49304.96150951092, 49342.006684417036, 49373.44895882476, 49441.29599692989, 49465.93587333668, 49480.6432824286, 49510.42036443692, 49556.10197458167, 49638.78742148674, 49877.76184247105, 50012.566434364824, 50181.08935328512, 50226.54357218369, 50315.738170429584, 50327.88960008037, 50445.28694009511, 50618.37488637558, 50744.74997757673, 50757.44086995626, 50940.37590171998, 50985.66611931466, 51067.89158583164, 51114.4768033655, 51166.470270146085, 51299.24197108536, 51329.58527951958, 51414.53732272935, 51414.92766986274, 51548.23504889919, 51601.520586218605, 51700.70884634356, 51723.82339342964, 51796.442237931304, 51820.77222698758, 51827.85710518233, 51857.099192814254, 51859.83673790537, 51885.34590388032, 51915.522272296985, 51931.880195039834, 51964.188145328495, 52039.353084706396, 52062.48040217423, 52100.1675691011, 52125.42966700368, 52272.963694820195, 52301.27539021695, 52305.777529833955, 52349.69880936644, 52386.26087869167, 52456.44382920719, 52472.43565206139, 52533.025474123664, 52580.675930245416, 52632.60036140141, 52704.346272145565, 52720.22921268181, 52743.95780140525, 52765.81089896755, 52806.68683229039, 52825.99938913787, 52886.75432317136, 52908.67592906872, 52960.90810560199, 53012.57637061461, 53023.50430569729, 53062.510148544105, 53071.42961363768, 53108.270516301614, 53119.85699742828, 53140.77230150597, 53215.62011885645, 53278.88024290071, 53390.90980938576, 53392.38564051323, 53443.50587622687, 53452.50580668905, 53481.908997888386, 53505.16775065039, 53516.465042198644, 53579.38755035589, 53594.16710133979, 53647.284749834434, 53680.73589270551, 53749.77586531725, 53809.27878771179, 53986.99447702077, 54026.060339715754, 54099.59879453776, 54142.41968089916, 54232.345628814975, 54233.38811562771, 54327.197909350885, 54344.78744745049, 54425.957596724744, 54682.7054520015, 54728.43271783265, 54805.36860515752, 54928.48921407384, 55076.04512963524, 55078.15642248611, 55080.9287407456, 55194.70481760654, 55257.92239179331, 55282.06789918223, 55282.72237905278, 55304.43164812768, 55313.88550317784, 55324.48774068164, 55361.097098296035, 55449.22366919274, 55488.05011255023, 55564.515740597635, 55587.14048051173, 55660.34609381013, 55670.92175761201, 55706.03469379258, 55792.37760401652, 55892.219776787126, 55897.49692633643, 55918.37103101651, 55972.06841759726, 56002.05016232773, 56071.484509313894, 56116.52692934758, 56213.357125144204, 56242.253555974065, 56263.48118621568, 56268.17720695765, 56277.924768806406, 56377.479221057954, 56394.16394057053, 56417.75627414226, 56449.22419613637, 56538.049096266455, 56554.59097855802, 56631.73344713027, 56659.46442069846, 56666.24448420036, 56707.507629428495, 56710.24794713027, 56767.80942188929, 56783.54781705645, 56787.58653184597, 56817.5270802679, 56864.44409291316, 56877.23351120623, 56891.033783927145, 57035.40539048462, 57049.84601170334, 57131.813037700646, 57149.58902329305, 57191.32611878526, 57318.940918669476, 57338.41575031753, 57365.26643293919, 57442.73794839341, 57550.3079773614, 57579.09310098676, 57668.541326653845, 57681.42234962136, 57836.45852870188, 58039.97108598851, 58200.62613860612, 58229.1328194893, 58238.574813650484, 58290.27359946107, 58383.90826080363, 58385.63447082479, 58394.45398453474, 58419.14267451884, 58584.0108818977, 58708.214431991124, 58796.10209568661, 58834.33654426352, 58877.6796824971, 59017.191520206004, 59149.303420058626, 59245.951124338055, 59255.99588989216, 59262.30016889482, 59364.49621492798, 59431.13102625919, 59441.595273898834, 59450.70422691655, 59489.273190565305, 59584.45590404623, 59616.54070658811, 59653.3302869108, 59674.60694986968, 59717.83077080696, 59725.64861090721, 59776.82759692792, 59799.07220308082, 59844.48632422653, 59961.527166682274, 60014.4161038386, 60146.84017844598, 60214.135031863036, 60325.767296468824, 60343.34134827859, 60344.788074908836, 60435.04143355317, 60505.041572404945, 60580.41426908121, 60663.303303918, 60963.787864358375, 60999.80796343152, 61070.925203560735, 61080.28999989357, 61157.56760863932, 61173.182851320846, 61205.86755785691, 61237.824164999554, 61270.18101420664, 61295.96382393049, 61359.33144731632, 61359.656214207396, 61435.30478546411, 61445.94916133754, 61525.39272381884, 61585.92655346671, 61631.107863326615, 61641.10375024655, 61662.9509527295, 61699.41209136697, 61757.00665418111, 61758.76766959225, 61901.36447645487, 61991.395770854746, 61995.82903934646, 61998.13319687983, 62029.79016947621, 62054.9223749736, 62078.47318857187, 62272.62108465646, 62377.521801232666, 62474.88955896459, 62513.101469927424, 62540.01163961064, 62598.28564590398, 62614.82033079048, 62806.4480812973, 62924.978074251914, 62943.5136334954, 63100.98054555621, 63266.16998126976, 63323.18935555813, 63369.76452859209, 63374.826066980844, 63885.11679165121, 63925.685049864485, 63959.26156694034, 63966.027069840646, 64006.99213149387, 64069.2634826727, 64220.92563787635]

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

    X111111_1 = [10030.303917450206, 10163.469845053987, 10178.932867575386, 10256.246206815633, 10299.902139450369, 10303.743989902709, 10305.081545314719, 10494.219198004896, 10496.454994717651, 10501.599593912597, 10506.562829104148, 10521.749081114827, 10525.454480609076, 10546.440396294212, 10557.776448897428, 10563.731711369568, 10594.100389924635, 10618.558722918742, 10662.745016789311, 10679.915031774357, 10742.716200805891, 10834.95638773858, 10854.872960112663, 10944.869814779118, 11018.479066773007, 11030.30549002857, 11035.706776909265, 11108.05607459339, 11203.563609023615, 11260.530777021058, 11359.807738698422, 11449.213548258109, 11612.241689535505, 11625.658513369855, 11635.97867537403, 11727.414952496356, 11744.977480116388, 11815.564567574665, 11824.83875246294, 11835.372973402726, 11923.778653754827, 11926.808145427813, 11934.040755198228, 11997.726912328257, 12029.129480918366, 12055.841769695462, 12058.404586863162, 12160.613497009554, 12326.582273703245, 12394.767726741815, 12430.592035698159, 12454.830643116118, 12477.409519436502, 12619.345768991967, 12625.373622984429, 12651.844540774782, 12662.887444365822, 12672.386358437741, 12691.288323229459, 12734.287187773873, 12767.102029612128, 12816.822601334257, 12896.551332790625, 12959.560136815868, 13063.737358961349, 13147.36030941772, 13212.277707172268, 13234.742832213622, 13303.070977381118, 13315.656265320718, 13343.19861681497, 13408.598487740092, 13441.721567349026, 13483.849990361894, 13550.328174269729, 13579.963038546071, 13618.854580348981, 13686.419163933595, 13718.012123206407, 13754.362290647357, 13794.138282710184, 13797.313251276053, 13803.404551793252, 13980.106368118582, 14139.623645655414, 14157.601307415891, 14193.751035173456, 14216.153219805929, 14240.010454518806, 14254.753969903199, 14263.136851532065, 14285.314235206744, 14307.563874296582, 14343.514669070313, 14410.310723902945, 14464.016248627977, 14567.474798407431, 14590.486151901976, 14670.321167583972, 14728.425900751445, 14826.905344792878, 14911.515611985635, 15109.990160102077, 15212.348746176183, 15264.275562389961, 15292.348484027298, 15428.738922648037, 15611.241243150535, 15701.824561162082, 15723.847825141072, 15928.621338576599, 16025.712543391226, 16069.911914068558, 16071.604859793006, 16079.00517991059, 16095.812805311896, 16111.618849024791, 16204.458675805337, 16297.741877205564, 16364.9590780722, 16415.09851430406, 16416.42257598817, 16552.05072177791, 16606.01320795693, 16628.326740776356, 16708.926486739667, 16726.20501798041, 16766.03245274653, 16803.747675723254, 16861.34131044096, 16919.476589054888, 17064.29392793632, 17222.399869537057, 17257.20334871457, 17281.847014941657, 17314.123569538096, 17329.27078842124, 17332.572810011123, 17392.85203028629, 17495.26122882066, 17501.03083247483, 17544.307156546078, 17754.988626355684, 17770.785843826547, 17924.926793547973, 17976.732904829325, 18025.70484323873, 18052.847156975815, 18072.996024572112, 18138.108702227895, 18163.621938481985, 18180.6161038046, 18257.76894796524, 18410.39663320106, 18475.508617710006, 18579.408683393627, 18610.78247673629, 18664.789689551588, 18803.12250578363, 19074.961915121552, 19110.24867636671, 19220.868707126137, 19226.75589727972, 19245.96598567588, 19364.645880978922, 19385.36809151948, 19417.48295339286, 19423.592581293044, 19432.171098302555, 19496.249265367875, 19533.921799655036, 19545.672882775136, 19568.139633734852, 19600.561085127785, 19643.409734949273, 19655.771338012994, 19672.256215443515, 19725.458454581858, 19785.321738849914, 19791.649959876813, 19813.637243550045, 19889.46207230197, 19891.8599317815, 19937.821571003333, 19938.410995909282, 19946.78296983755, 19951.83149114923, 19982.786444162117, 20028.26081342592, 20163.922599437723, 20221.420757066506, 20223.421865818567, 20235.243142999338, 20244.28355129926, 20259.557355876146, 20293.310551073737, 20314.17943751799, 20333.965884187506, 20349.817960169108, 20371.204636788818, 20388.47046420385, 20393.18376334195, 20553.201091231345, 20653.68691529127, 20719.1794604401, 20732.26421433934, 20785.296066464653, 20907.57974981985, 21050.46104435341, 21107.137262103548, 21135.138992765736, 21216.953831678173, 21232.5399321259, 21301.601313458385, 21318.880465109658, 21338.873637368008, 21346.126436520506, 21355.616018442237, 21472.0180383789, 21506.662648465368, 21632.078656258913, 21724.952318791184, 21781.071401194953, 21837.553937620025, 21888.885630214336, 22020.400940426873, 22070.77419511355, 22081.227931964982, 22118.54573176502, 22130.97087000025, 22142.83718042472, 22234.03842981391, 22242.999008895356, 22252.156928531767, 22380.589229979618, 22399.022824981188, 22495.771987626053, 22576.535318295933, 22646.069193049756, 22825.38116048195, 22902.91053467917, 22979.730742212338, 23099.42843966851, 23162.194408176576, 23196.128223171625, 23198.57261608856, 23226.822803292565, 23273.3178612454, 23314.654524047826, 23337.80602511426, 23475.34361065259, 23501.290872805243, 23525.08850255194, 23529.178173857537, 23529.819362625803, 23597.13644740796, 23705.345701080874, 23710.55264867936, 23717.29832190228, 23845.646055915626, 23946.01578907899, 24003.893310363826, 24035.821318300055, 24049.93285001462, 24056.74986567051, 24122.689812279285, 24157.686494709942, 24164.96197579585, 24235.15327848767, 24278.173903420808, 24337.423471974813, 24460.210803615526, 24463.011948242987, 24498.70326147193, 24524.819936304815, 24553.192130139323, 24562.317211843067, 24573.55025838955, 24632.189953263678, 24754.591063234446, 24755.964890625946, 24791.14069683551, 25123.47448022131, 25132.90690470575, 25163.637781017234, 25258.948074259068, 25313.355634898544, 25321.381946092915, 25402.519851216475, 25422.9129199495, 25730.339481628696, 25731.27932579413, 25853.970403086343, 25869.282817804626, 25875.857261283694, 25904.395186338945, 25990.331345838735, 25994.49011939409, 25998.259968842758, 26052.38256307847, 26260.114820662497, 26428.152817034632, 26514.112826226385, 26538.472502401048, 26570.090656938268, 26617.718014514467, 26674.7781697217, 26776.551920665162, 26838.622967297124, 26950.962861985103, 26987.330825345165, 26989.34144478591, 27085.229759644026, 27107.802403895905, 27184.703416315664, 27195.590936756475, 27250.228340823778, 27332.161175976005, 27358.09088561745, 27371.950177820825, 27402.37098039492, 27425.35711911404, 27453.079902261263, 27490.125429368614, 27514.388295642617, 27689.309908524625, 27691.907800520254, 27709.966648505793, 27724.88802616761, 27758.60753948175, 27791.04769152006, 27841.50840008997, 27907.246253804147, 27909.46294315572, 27910.20963457665, 28050.57704366147, 28081.780097249462, 28112.93753873618, 28266.036614692242, 28308.34699485741, 28366.972294577467, 28455.35818295209, 28482.09829616641, 28531.93667001912, 28553.858453598576, 28558.83557384922, 28639.482661730173, 28704.733165639143, 28828.785705670096, 29007.811880012527, 29010.522204454042, 29084.310105874167, 29154.075295992585, 29193.895954615793, 29233.22360577579, 29269.64271583363, 29299.85168334247, 29316.832792830835, 29371.983898024293, 29402.136286958237, 29445.677285700458, 29628.131855377123, 29632.547554966095, 29662.042347659106, 29823.945540536086, 29902.77218769355, 29950.762933145543, 29965.287709506534, 29980.75666216076, 30049.87223156792, 30128.017409312022, 30173.761753425926, 30258.191306982488, 30465.72176162794, 30590.844325120484, 30592.54434073975, 30699.938004225114, 30807.537191928972, 30826.795168179815, 30848.916194346482, 30894.96993824104, 30952.092782973326, 30992.23449494999, 31005.708874295455, 31014.172280890132, 31014.993763051756, 31051.123443872144, 31074.96681058915, 31079.956803109853, 31252.6091322139, 31484.44796714896, 31556.012445068132, 31613.741378212326, 31731.709098879935, 31766.959226885363, 31784.53854759816, 31846.68127718428, 32005.93510439871, 32020.303263936887, 32042.404328981076, 32113.85146568305, 32126.65561794797, 32129.958356093917, 32205.148427655695, 32205.941400071202, 32232.606216395485, 32243.51255365478, 32245.68821612995, 32270.593411355236, 32283.681117730182, 32292.541896209827, 32442.44357656977, 32444.417293417242, 32624.238314240436, 32624.653757551438, 32660.030823960984, 32764.692045790125, 32844.98094998319, 32920.64589662664, 32988.14609333448, 33035.82639657165, 33037.1162241008, 33086.74231147471, 33152.319754574375, 33227.08591705705, 33254.688410208604, 33292.35389892895, 33319.204086084894, 33359.84852581717, 33499.265266133705, 33557.43186625648, 33562.3373268545, 33594.610659529586, 33597.96830186106, 33608.56714050929, 33641.02782992067, 33730.06036867137, 33753.249502804385, 33775.57082871306, 33794.07922359386, 33937.83944334058, 34126.18653912233, 34185.66636191882, 34249.23135040568, 34262.31896517669, 34263.091234720894, 34313.073335917776, 34324.07719884744, 34331.41881822875, 34418.30791036559, 34455.810578532255, 34460.24891134987, 34640.436224064826, 34643.07887745842, 34714.87773475655, 34727.466360445185, 34764.28527122333, 34794.27552544017, 34830.584074958584, 34866.10786714527, 34879.65380745831, 34888.64229812062, 34893.969241182705, 34943.84004665667, 34980.27061832564, 34990.1118580693, 35079.81625623438, 35159.51260199132, 35177.71677621409, 35361.08752919597, 35379.74110369281, 35559.85122596715, 35570.65005040935, 35594.939824491, 35613.9925736819, 35782.42714668765, 35943.3452590511, 35982.859508623835, 35995.71374990865, 36066.39669604487, 36085.28968354955, 36129.762963924615, 36271.23304023053, 36279.10219485451, 36334.730897675414, 36353.6499391682, 36414.78985869943, 36425.39108343153, 36436.87673595793, 36475.82465026468, 36479.74293591059, 36619.32532981243, 36697.8536668316, 36745.201902752844, 36814.03909048751, 37045.03387584849, 37054.430712562775, 37172.65091463034, 37236.55626521552, 37272.38621969985, 37397.01321855793, 37449.751922639785, 37579.81999987134, 37599.22089127265, 37709.93317713398, 37726.939449224985, 37840.964061668186, 37893.4609293771, 37968.37617264147, 37988.92519290092, 38093.73649018649, 38117.91484893085, 38159.32618398887, 38168.68468733846, 38171.00185332356, 38264.69832537645, 38288.838689136785, 38404.59287785558, 38408.111478049046, 38432.394293851234, 38449.96955064632, 38462.60335826854, 38480.59572227553, 38506.74063279559, 38516.480881088544, 38527.843965378066, 38541.717287819265, 38562.88785267898, 38635.70232705813, 38740.95418856836, 38745.05279642018, 38771.907348535926, 38849.80500232965, 38863.69163332208, 38873.441569477145, 38972.6176025456, 39005.72316215529, 39057.63859062953, 39204.268055407214, 39423.224466467465, 39491.432421905636, 39492.37177628736, 39577.1663325349, 39605.93296186134, 39706.858371569535, 39721.48608265346, 39723.63518405522, 39738.39321283655, 39789.85362304932, 39876.25244127965, 39934.96700913203, 40001.32581360321, 40046.364911034325, 40098.99197023448, 40138.45031914601, 40236.99704885838, 40248.30879981201, 40267.36495554983, 40337.740986861965, 40455.72748536724, 40457.2701873599, 40468.72584207825, 40588.10541157954, 40595.721553044015, 40608.46458109676, 40627.34720460765, 40679.452414376516, 40698.65995735578, 40704.95778877755, 40739.26629587462, 40759.1490241489, 40763.981509012854, 40783.065069558805, 40796.01295879396, 40862.574811981656, 40926.02629035384, 40941.56847982168, 40952.02392655759, 40961.571594719135, 40977.91256066748, 40989.201509710874, 40994.59561626852, 41026.37418179881, 41039.14307394641, 41049.1196940022, 41071.90053500377, 41104.099002375675, 41116.30408849422, 41220.42278547684, 41239.78966522609, 41255.08781679383, 41393.006862849215, 41431.816081824494, 41470.65985568876, 41494.9541941404, 41562.23176845923, 41601.806497851, 41648.77377989969, 41652.24018461353, 41675.21511472833, 41712.70398823055, 41771.781441303494, 41835.51530590497, 41863.03653936411, 41937.76532068159, 41999.863301410536, 42018.76000900364, 42170.70991146831, 42306.64056082643, 42336.57816797974, 42431.29804958838, 42552.25905932741, 42632.704910770975, 42636.969274595496, 42665.93453337799, 42751.55523448775, 42846.59306069315, 42874.6494274155, 42916.369640175944, 43043.58281982704, 43100.58175602718, 43116.04177125028, 43134.98977855469, 43176.76134882256, 43216.97696936242, 43221.3447839564, 43279.77848484841, 43314.15933203964, 43360.896858323824, 43462.64713395041, 43481.102313927, 43483.786802727176, 43557.85094045744, 43586.29778889035, 43593.08559414698, 43627.55476691279, 43680.0813550374, 43730.72600884793, 43739.29026437729, 43867.0857815423, 43944.397195055026, 44019.24529574979, 44251.8292787472, 44373.87342196104, 44410.71018136253, 44420.97938072899, 44556.23218134298, 44557.83112409702, 44604.9910266866, 44655.09660313233, 44710.453184603284, 44748.31413094501, 44749.545860470374, 44865.11650110187, 44875.523255499866, 44883.6693158679, 44895.652232451546, 44931.93592804958, 44997.9222813523, 45066.833110008316, 45079.368761853366, 45131.374430362186, 45164.882772670055, 45254.46091911507, 45371.917361009015, 45403.7601578724, 45448.40830054501, 45450.234306371414, 45466.83989830206, 45555.92913771447, 45692.279057969834, 45788.14024755343, 45788.33505432735, 45805.4056998552, 45823.73457073646, 45879.851233279776, 46025.99839648208, 46061.975153495354, 46063.98667063645, 46245.34782387562, 46371.34286670859, 46401.404813965535, 46405.5386824578, 46557.567009569226, 46613.13682772807, 46670.04784400399, 47185.35608580944, 47219.364043944384, 47240.39013654051, 47295.5763253633, 47301.91470906185, 47316.74906572135, 47331.49916666494, 47408.08995938915, 47442.179728514726, 47456.040104431166, 47540.69164551449, 47603.486668618716, 47702.34507812263, 47723.857927267214, 47728.346795803314, 47794.88411725256, 47811.88190185092, 47891.208099580996, 47958.86368784335, 48078.79816095945, 48103.33390026837, 48235.97817758124, 48276.437898274395, 48290.58614671164, 48359.812550590614, 48411.28708604183, 48440.95531322879, 48479.49303493494, 48586.83247205297, 48613.1656347152, 48650.468972771254, 48754.5889848983, 48767.91557872893, 48784.35628233764, 48979.0626771842, 48991.20164413406, 49030.12626396816, 49160.00215098125, 49195.583472865364, 49225.63059909319, 49244.18554489215, 49256.80577263648, 49321.195417699615, 49381.15933190032, 49388.852488177006, 49402.40425355058, 49435.211780205274, 49556.00866464246, 49661.69864510901, 49661.78354405859, 49707.517121928, 49727.82960552626, 49797.84039244026, 49894.93310702872, 49940.4199086432, 49942.29589297684, 50064.924343524064, 50070.67967926387, 50164.00790043551, 50281.952144935174, 50298.675876294976, 50323.41256006692, 50348.75714708606, 50351.52486948079, 50399.83685207222, 50487.14382657095, 50542.08844631972, 50687.46258047829, 50688.052579283234, 50828.13238891885, 50831.345627015886, 50842.368234972935, 50844.44863100594, 50857.08397994469, 50866.40797996915, 50896.358334349396, 50912.14159036556, 50967.14560052731, 50979.051964195045, 51037.58764279172, 51076.35636315742, 51085.12388767499, 51159.55676671285, 51200.565575632325, 51212.44544336352, 51278.405059596225, 51451.56975077481, 51473.24982245191, 51494.575704978924, 51545.00601767187, 52131.51539269268, 52237.82022144467, 52356.711345286916, 52384.51492102918, 52415.723983360665, 52510.07648077332, 52587.65704992206, 52613.15513650874, 52657.06508185415, 52668.10111631909, 52730.42877851168, 52801.32532870789, 52816.40123298175, 52831.53716629107, 52875.54894342708, 52890.44913740973, 52948.49372506984, 52962.99035001158, 52967.4362495497, 52976.95704624219, 53146.57338001901, 53168.36122644244, 53245.52424901949, 53263.86375886307, 53492.857607541155, 53565.657539732645, 53673.00401203666, 53733.2655307993, 53759.291096490175, 53850.44435617114, 53892.465826546286, 53905.676257817846, 54064.42310836753, 54232.468231749146, 54262.65360509212, 54339.87046662817, 54465.127901691456, 54479.201484108744, 54489.244153214866, 54602.8455784486, 54618.35755780565, 54644.036761810516, 54679.9396671815, 54724.60159189995, 54746.36085785797, 54747.305941095256, 54760.10574643633, 54762.35814127563, 54814.52124175891, 54861.665706918655, 54880.681934063614, 54911.42396088654, 54978.19844500338, 54999.33792458627, 55027.1325981619, 55130.12062275543, 55138.78276497916, 55241.971445525276, 55488.142420545206, 55581.16562738528, 55677.880126003176, 55688.55753716031, 55799.53574059296, 55806.36073795472, 56015.79309269766, 56072.48206238301, 56261.196187036665, 56264.11661216926, 56326.23993273693, 56333.81861606662, 56426.976532743865, 56470.48409300241, 56496.58954233124, 56507.57552397642, 56592.5962261949, 56617.45244559242, 56704.91146951382, 56836.64640740256, 56852.869128237005, 56858.64376772172, 56919.54138333529, 56934.00230162276, 57002.615729300705, 57074.5061775086, 57119.22155729149, 57148.5702157998, 57232.02851299742, 57239.153350241824, 57327.10933885658, 57352.838462587104, 57462.22507968735, 57472.553220776084, 57481.28801253837, 57524.85371787617, 57580.864374267774, 57612.92310112063, 57625.38316521707, 57721.17040124579, 57734.2625103321, 57782.895158495645, 57959.781516800125, 58135.720882152404, 58205.676432323446, 58322.383056875675, 58402.22011896366, 58413.61171695753, 58446.76916517028, 58544.72701967151, 58782.292526600504, 58794.72461318206, 58883.71212338932, 59079.55487527013, 59090.91296948488, 59092.22548300943, 59103.94720001122, 59134.84880565322, 59161.989326132665, 59371.19507016237, 59385.639890264574, 59407.893339835085, 59428.031183780724, 59430.46139167201, 59435.21243905448, 59435.32646173714, 59458.11909862778, 59501.58188119464, 59585.20936648389, 59590.89293985254, 59666.00905895116, 59689.2044371887, 59798.154264557874, 59829.55326402787, 59837.21491666172, 59857.25947542329, 59895.101215571034, 59899.42008929666, 59921.16624051424, 59929.64050347621, 59932.052246718435, 59955.70937864478, 60021.76740622366, 60109.203990272734, 60146.47884152727, 60192.98625855842, 60254.37605829977, 60262.97576471513, 60274.07995170766, 60282.46842850764, 60293.99056944351, 60301.77531671357, 60356.95578628245, 60426.577836207514, 60453.49450095955, 60484.064845992674, 60525.130108627105, 60527.05885902662, 60547.46372023504, 60589.70294350774, 60593.15028387097, 60598.6173684173, 60634.936797191614, 60688.81580613083, 60726.955287813566, 60865.66719824258, 60866.12243085787, 60918.1032308503, 61009.08207519235, 61018.913430977605, 61066.914438006475, 61115.987636230864, 61158.25196608, 61283.33951422996, 61292.182802318355, 61324.22238334015, 61339.11542221393, 61401.98590810163, 61511.94058384691, 61546.889204901694, 61582.98138737718, 61686.789671941464, 61887.662845059305, 61895.09920035934, 61947.33308305836, 61956.217316525595, 62144.59812222922, 62260.324867856616, 62263.37993782137, 62275.42825326773, 62307.50932480561, 62337.568272350516, 62345.17434076026, 62369.56471082035, 62772.36778588279, 62818.086049825106, 62840.26138054068, 62845.28274813386, 62860.95559713014, 62884.73185042591, 62975.79514393221, 62992.24316309694, 63005.66436538167, 63100.137358768814, 63133.871110795175, 63184.276350147156, 63222.66611010167, 63241.25675841398, 63254.59511502783, 63297.5689374984, 63311.296283797805, 63328.326673663214, 63359.85668190096, 63403.49549810931, 63469.7667722407, 63473.13487626382, 63559.78211106369, 63607.48061229057, 63669.27562684823, 63965.96705721443, 64090.44203307259, 64157.90760478836, 64175.850296903256, 64190.10185596501, 64217.97765885662, 64232.35943137311]

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

