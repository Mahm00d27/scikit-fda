from skfda import FDataGrid, FDataBasis
from skfda.datasets import fetch_weather
from skfda.misc.operators import LinearDifferentialOperator
from skfda.misc.regularization import TikhonovRegularization
from skfda.preprocessing.dim_reduction.projection import FPCABasis, FPCAGrid
from skfda.representation.basis import Fourier
import unittest

import numpy as np


class FPCATestCase(unittest.TestCase):

    def test_basis_fpca_fit_attributes(self):
        fpca = FPCABasis()
        with self.assertRaises(AttributeError):
            fpca.fit(None)

        basis = Fourier(n_basis=1)
        # check that if n_components is bigger than the number of samples then
        # an exception should be thrown
        fd = FDataBasis(basis, [[0.9]])
        with self.assertRaises(AttributeError):
            fpca.fit(fd)

        # check that n_components must be smaller than the number of elements
        # of target basis
        fd = FDataBasis(basis, [[0.9], [0.7], [0.5]])
        with self.assertRaises(AttributeError):
            fpca.fit(fd)

    def test_discretized_fpca_fit_attributes(self):
        fpca = FPCAGrid()
        with self.assertRaises(AttributeError):
            fpca.fit(None)

        # check that if n_components is bigger than the number of samples then
        # an exception should be thrown
        fd = FDataGrid([[0.5], [0.1]], sample_points=[0])
        with self.assertRaises(AttributeError):
            fpca.fit(fd)

        # check that n_components must be smaller than the number of attributes
        # in the FDataGrid object
        fd = FDataGrid([[0.9], [0.7], [0.5]], sample_points=[0])
        with self.assertRaises(AttributeError):
            fpca.fit(fd)

    def test_basis_fpca_fit_result(self):

        n_basis = 9
        n_components = 3

        fd_data = fetch_weather()['data'].coordinates[0]
        fd_data = FDataGrid(np.squeeze(fd_data.data_matrix),
                            np.arange(0.5, 365, 1))

        # initialize basis data
        basis = Fourier(n_basis=9, domain_range=(0, 365))
        fd_basis = fd_data.to_basis(basis)

        fpca = FPCABasis(n_components=n_components,
                         regularization_parameter=1e5,
                         regularization=TikhonovRegularization(
                             LinearDifferentialOperator(2)))
        fpca.fit(fd_basis)

        # results obtained using Ramsay's R package
        results = [[0.92407552, 0.13544888, 0.35399023, 0.00805966, -0.02148108,
                    -0.01709549, -0.00208469, -0.00297439, -0.00308224],
                   [-0.33314436, -0.05116842, 0.89443418, 0.14673902,
                    0.21559073,
                    0.02046924, 0.02203431, -0.00787185, 0.00247492],
                   [-0.14241092, 0.92131899, 0.00514715, 0.23391411,
                    -0.19497613,
                    0.09800817, 0.01754439, -0.00205874, 0.01438185]]
        results = np.array(results)

        # compare results obtained using this library. There are slight
        # variations due to the fact that we are in two different packages
        for i in range(n_components):
            if np.sign(fpca.components_.coefficients[i][0]) != np.sign(
                    results[i][0]):
                results[i, :] *= -1
        np.testing.assert_allclose(fpca.components_.coefficients, results,
                                   atol=1e-7)

    def test_basis_fpca_regularization_fit_result(self):

        n_basis = 9
        n_components = 3

        fd_data = fetch_weather()['data'].coordinates[0]
        fd_data = FDataGrid(np.squeeze(fd_data.data_matrix),
                            np.arange(0.5, 365, 1))

        # initialize basis data
        basis = Fourier(n_basis=9, domain_range=(0, 365))
        fd_basis = fd_data.to_basis(basis)

        fpca = FPCABasis(n_components=n_components)
        fpca.fit(fd_basis)

        # results obtained using Ramsay's R package
        results = [[0.9231551, 0.1364966, 0.3569451, 0.0092012, -0.0244525,
                    -0.02923873, -0.003566887, -0.009654571, -0.0100063],
                   [-0.3315211, -0.0508643, 0.89218521, 0.1669182, 0.2453900,
                    0.03548997, 0.037938051, -0.025777507, 0.008416904],
                   [-0.1379108, 0.9125089, 0.00142045, 0.2657423, -0.2146497,
                    0.16833314, 0.031509179, -0.006768189, 0.047306718]]
        results = np.array(results)

        # compare results obtained using this library. There are slight
        # variations due to the fact that we are in two different packages
        for i in range(n_components):
            if np.sign(fpca.components_.coefficients[i][0]) != np.sign(
                    results[i][0]):
                results[i, :] *= -1
        np.testing.assert_allclose(fpca.components_.coefficients, results,
                                   atol=1e-7)

    def test_grid_fpca_fit_result(self):

        n_components = 1

        fd_data = fetch_weather()['data'].coordinates[0]

        fpca = FPCAGrid(n_components=n_components, weights=[1] * 365)
        fpca.fit(fd_data)

        # results obtained using fda.usc for the first component
        results = [
            [-0.06958281, -0.07015412, -0.07095115, -0.07185632, -0.07128256,
             -0.07124209, -0.07364828, -0.07297663, -0.07235438, -0.07307498,
             -0.07293423, -0.07449293, -0.07647909, -0.07796823, -0.07582476,
             -0.07263243, -0.07241871, -0.0718136, -0.07015477, -0.07132331,
             -0.0711527, -0.07435933, -0.07602666, -0.0769783, -0.07707199,
             -0.07503802, -0.0770302, -0.07705581, -0.07633515, -0.07624817,
             -0.07631568, -0.07619913, -0.07568, -0.07595155, -0.07506939,
             -0.07181941, -0.06907624, -0.06735476, -0.06853985, -0.06902363,
             -0.07098882, -0.07479412, -0.07425241, -0.07555835, -0.0765903,
             -0.07651853, -0.07682536, -0.07458996, -0.07631711, -0.07726509,
             -0.07641246, -0.0744066, -0.07501397, -0.07302722, -0.07045571,
             -0.06912529, -0.06792186, -0.06830739, -0.06898433, -0.07000192,
             -0.07014513, -0.06994886, -0.07115909, -0.073999, -0.07292669,
             -0.07139879, -0.07226865, -0.07187915, -0.07122995, -0.06975022,
             -0.06800613, -0.06900793, -0.07186378, -0.07114479, -0.07015252,
             -0.06944782, -0.068291, -0.06905348, -0.06925773, -0.06834624,
             -0.06837319, -0.06824067, -0.06644614, -0.06637313, -0.06626312,
             -0.06470209, -0.0645058, -0.06477729, -0.06411049, -0.06158499,
             -0.06305197, -0.06398006, -0.06277579, -0.06282124, -0.06317684,
             -0.0614125, -0.05961922, -0.05875443, -0.05845781, -0.05828608,
             -0.05666474, -0.05495706, -0.05446301, -0.05468254, -0.05478609,
             -0.05440798, -0.05312339, -0.05102368, -0.05160285, -0.05077954,
             -0.04979648, -0.04890853, -0.04745462, -0.04496763, -0.0448713,
             -0.04599596, -0.04688998, -0.04488872, -0.04404507, -0.04420729,
             -0.04368153, -0.04254381, -0.0411764, -0.04022811, -0.03999746,
             -0.03963634, -0.03832502, -0.0383956, -0.04015374, -0.0387544,
             -0.03777315, -0.03830728, -0.03768616, -0.03714081, -0.03781918,
             -0.03739374, -0.03659894, -0.03563342, -0.03658407, -0.03686991,
             -0.03543746, -0.03518799, -0.03361226, -0.0321534, -0.03050438,
             -0.02958411, -0.02855023, -0.02913402, -0.02992464, -0.02899548,
             -0.02891629, -0.02809554, -0.02702642, -0.02672194, -0.02678648,
             -0.02698471, -0.02628085, -0.02674285, -0.02658515, -0.02604447,
             -0.0245711, -0.02413174, -0.02342496, -0.022898, -0.02216152,
             -0.02272283, -0.02199741, -0.02305362, -0.02371371, -0.02320865,
             -0.02234777, -0.0225018, -0.02104359, -0.02203346, -0.02052545,
             -0.01987457, -0.01947911, -0.01986949, -0.02012196, -0.01958515,
             -0.01906753, -0.01857869, -0.01874101, -0.01827973, -0.017752,
             -0.01702056, -0.01759611, -0.01888485, -0.01988159, -0.01951675,
             -0.01872967, -0.01866667, -0.0183576, -0.01909758, -0.018599,
             -0.01910036, -0.01930315, -0.01958856, -0.02129936, -0.0216614,
             -0.0204397, -0.02002368, -0.02058828, -0.02149915, -0.02167326,
             -0.02238569, -0.02211907, -0.02168336, -0.02124387, -0.02131655,
             -0.02130508, -0.02181227, -0.02230632, -0.02223732, -0.0228216,
             -0.02355137, -0.02275145, -0.02286893, -0.02437776, -0.02523897,
             -0.0248354, -0.02319174, -0.02335831, -0.02405789, -0.02483273,
             -0.02428119, -0.02395295, -0.02437185, -0.02476434, -0.02347973,
             -0.02385957, -0.02451257, -0.02414586, -0.02439035, -0.02357782,
             -0.02417295, -0.02504764, -0.02682569, -0.02807111, -0.02886335,
             -0.02943406, -0.02956806, -0.02893096, -0.02903812, -0.02999862,
             -0.029421, -0.03016203, -0.03118823, -0.03076205, -0.03005985,
             -0.03079187, -0.03215188, -0.03271075, -0.03146124, -0.03040965,
             -0.03008436, -0.03085897, -0.03015341, -0.03014661, -0.03110255,
             -0.03271278, -0.03217399, -0.0331721, -0.03459221, -0.03572073,
             -0.03560707, -0.03531492, -0.03687657, -0.03800143, -0.0373808,
             -0.03729927, -0.03748666, -0.03754171, -0.03790408, -0.03963726,
             -0.03992153, -0.03812243, -0.0373844, -0.0385394, -0.03849716,
             -0.03826345, -0.03743958, -0.0380861, -0.03857622, -0.04099357,
             -0.04102509, -0.04170207, -0.04283573, -0.04320618, -0.04269438,
             -0.04467527, -0.04470603, -0.04496092, -0.04796417, -0.04796633,
             -0.047863, -0.04883668, -0.0505939, -0.05112441, -0.04960962,
             -0.05000041, -0.04962112, -0.05087008, -0.0521671, -0.05369792,
             -0.05478139, -0.05559221, -0.05669698, -0.05654505, -0.05731113,
             -0.05783543, -0.05766056, -0.05754354, -0.05724272, -0.05831026,
             -0.05847512, -0.05804533, -0.05875046, -0.06021703, -0.06147975,
             -0.06213918, -0.0645805, -0.06500849, -0.06361716, -0.06315227,
             -0.06306436, -0.06425743, -0.06626847, -0.06615213, -0.06881004,
             -0.06942296, -0.06889225, -0.06868663, -0.0678667, -0.06720133,
             -0.06771172, -0.06885042, -0.06896979, -0.06961627, -0.07211988,
             -0.07252956, -0.07265559, -0.07264195, -0.07306334, -0.07282035,
             -0.07196505, -0.07210595, -0.07203942, -0.07105821, -0.06920599,
             -0.06892264, -0.06699939, -0.06537829, -0.06543323, -0.06913186,
             -0.07210039, -0.07219987, -0.07124228, -0.07065497, -0.06996833,
             -0.0674457, -0.06800847, -0.06784175, -0.06592871, -0.06723401]]

        results = np.array(results)

        # compare results obtained using this library. There are slight
        # variations due to the fact that we are in two different packages
        for i in range(n_components):
            if np.sign(fpca.components_.data_matrix[i][0]) != np.sign(
                    results[i][0]):
                results[i, :] *= -1
        np.testing.assert_allclose(
            fpca.components_.data_matrix.reshape(
                fpca.components_.data_matrix.shape[:-1]),
            results,
            rtol=1e-6)

    def test_grid_fpca_regularization_fit_result(self):

        n_components = 1

        fd_data = fetch_weather()['data'].coordinates[0]

        fd_data = FDataGrid(np.squeeze(fd_data.data_matrix),
                            np.arange(0.5, 365, 1))

        fpca = FPCAGrid(n_components=n_components, weights=[1] * 365,
                        regularization_parameter=1)
        fpca.fit(fd_data)

        # results obtained using fda.usc for the first component
        results = [
            [-0.06961236, -0.07027042, -0.07090496, -0.07138247, -0.07162215,
             -0.07202264, -0.07264893, -0.07279174, -0.07274672, -0.07300075,
             -0.07365471, -0.07489002, -0.07617455, -0.07658708, -0.07551923,
             -0.07375128, -0.0723776, -0.07138373, -0.07080555, -0.07111745,
             -0.0721514, -0.07395427, -0.07558341, -0.07650959, -0.0766541,
             -0.07641352, -0.07660864, -0.07669081, -0.0765396, -0.07640671,
             -0.07634668, -0.07626304, -0.07603638, -0.07549114, -0.07410347,
             -0.07181791, -0.06955356, -0.06824034, -0.06834077, -0.06944125,
             -0.07133598, -0.07341109, -0.07471501, -0.07568844, -0.07631904,
             -0.07647264, -0.07629453, -0.07598431, -0.07628157, -0.07654062,
             -0.07616026, -0.07527189, -0.07426683, -0.07267961, -0.07079998,
             -0.06927394, -0.068412, -0.06838534, -0.06888439, -0.0695309,
             -0.07005508, -0.07066637, -0.07167196, -0.07266978, -0.07275299,
             -0.07235183, -0.07207819, -0.07159814, -0.07077697, -0.06977026,
             -0.0691952, -0.06965756, -0.07058327, -0.07075751, -0.07025415,
             -0.06954233, -0.06899785, -0.06891026, -0.06887079, -0.06862183,
             -0.06830082, -0.06777765, -0.06700202, -0.06639394, -0.06582435,
             -0.06514987, -0.06467236, -0.06425272, -0.06359187, -0.062922,
             -0.06300068, -0.06325494, -0.06316979, -0.06296254, -0.06246343,
             -0.06136836, -0.0600936, -0.05910688, -0.05840872, -0.0576547,
             -0.05655684, -0.05546518, -0.05484433, -0.05465746, -0.05449286,
             -0.05397004, -0.05300742, -0.05196686, -0.05133129, -0.05064617,
             -0.04973418, -0.04855687, -0.04714356, -0.04588103, -0.04547284,
             -0.04571493, -0.04580704, -0.04523509, -0.04457293, -0.04405309,
             -0.04338468, -0.04243512, -0.04137278, -0.04047946, -0.03984531,
             -0.03931376, -0.0388847, -0.03888507, -0.03908662, -0.03877577,
             -0.03830952, -0.03802713, -0.03773521, -0.03752388, -0.03743759,
             -0.03714113, -0.03668387, -0.0363703, -0.03642288, -0.03633051,
             -0.03574618, -0.03486536, -0.03357797, -0.03209969, -0.0306837,
             -0.02963987, -0.029102, -0.0291513, -0.02932013, -0.02912619,
             -0.02869407, -0.02801974, -0.02732363, -0.02690451, -0.02676622,
             -0.0267323, -0.02664896, -0.02661708, -0.02637166, -0.02577496,
             -0.02490428, -0.02410813, -0.02340367, -0.02283356, -0.02246305,
             -0.0224229, -0.0225435, -0.02295603, -0.02324663, -0.02310005,
             -0.02266893, -0.02221522, -0.02168056, -0.02129419, -0.02064909,
             -0.02007801, -0.01979083, -0.01979541, -0.01978879, -0.01954269,
             -0.0191623, -0.01879572, -0.01849678, -0.01810297, -0.01769666,
             -0.01753802, -0.01794351, -0.01871307, -0.01930005, -0.01933,
             -0.01901017, -0.01873486, -0.01861838, -0.01870777, -0.01879,
             -0.01904219, -0.01945078, -0.0200607, -0.02076936, -0.02100213,
             -0.02071439, -0.02052113, -0.02076313, -0.02128468, -0.02175631,
             -0.02206387, -0.02201054, -0.02172142, -0.02143092, -0.02133647,
             -0.02144956, -0.02176286, -0.02212579, -0.02243861, -0.02278316,
             -0.02304113, -0.02313356, -0.02349275, -0.02417028, -0.0245954,
             -0.0244062, -0.02388557, -0.02374682, -0.02401071, -0.02431126,
             -0.02433125, -0.02427656, -0.02430442, -0.02424977, -0.02401619,
             -0.02402294, -0.02415424, -0.02413262, -0.02404076, -0.02397651,
             -0.0243893, -0.0253322, -0.02664395, -0.0278802, -0.02877936,
             -0.02927182, -0.02937318, -0.02926277, -0.02931632, -0.02957945,
             -0.02982133, -0.03023224, -0.03060406, -0.03066011, -0.03070932,
             -0.03116429, -0.03179009, -0.03198094, -0.03149462, -0.03082037,
             -0.03041594, -0.0303307, -0.03028465, -0.03052841, -0.0311837,
             -0.03199307, -0.03262025, -0.03345083, -0.03442665, -0.03521313,
             -0.0356433, -0.03606037, -0.03677406, -0.03735165, -0.03746578,
             -0.03744154, -0.03752143, -0.03780898, -0.03837639, -0.03903232,
             -0.03911629, -0.03857567, -0.03816592, -0.03819285, -0.03818405,
             -0.03801684, -0.03788493, -0.03823232, -0.03906142, -0.04023251,
             -0.04112434, -0.04188011, -0.04254759, -0.043, -0.04340181,
             -0.04412687, -0.04484482, -0.04577669, -0.04700832, -0.04781373,
             -0.04842662, -0.04923723, -0.05007637, -0.05037817, -0.05009794,
             -0.04994083, -0.05012712, -0.05094001, -0.05216065, -0.05350458,
             -0.05469781, -0.05566309, -0.05641011, -0.05688106, -0.05730818,
             -0.05759156, -0.05763771, -0.05760073, -0.05766117, -0.05794587,
             -0.05816696, -0.0584046, -0.05905105, -0.06014331, -0.06142231,
             -0.06270788, -0.06388225, -0.06426245, -0.06386721, -0.0634656,
             -0.06358049, -0.06442514, -0.06570047, -0.06694328, -0.0682621,
             -0.06897846, -0.06896583, -0.06854621, -0.06797142, -0.06763755,
             -0.06784024, -0.06844314, -0.06918567, -0.07021928, -0.07148473,
             -0.07232504, -0.07272276, -0.07287021, -0.07289836, -0.07271531,
             -0.07239956, -0.07214086, -0.07170078, -0.07081195, -0.06955202,
             -0.06825156, -0.06690167, -0.06617102, -0.06683291, -0.06887539,
             -0.07089424, -0.07174837, -0.07150888, -0.07070378, -0.06960066,
             -0.06842496, -0.06777666, -0.06728403, -0.06681262, -0.06679066]]

        results = np.array(results)

        # compare results obtained using this library. There are slight
        # variations due to the fact that we are in two different packages
        for i in range(n_components):
            if np.sign(fpca.components_.data_matrix[i][0]) != np.sign(
                    results[i][0]):
                results[i, :] *= -1
        np.testing.assert_allclose(
            fpca.components_.data_matrix.reshape(
                fpca.components_.data_matrix.shape[:-1]),
            results,
            rtol=1e-6)


if __name__ == '__main__':
    unittest.main()
