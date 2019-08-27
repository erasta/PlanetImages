import json
import numpy as np

def copy_cloud_mask(original_udm, product_udm):
    prod_without_cloud = np.bitwise_and(product_udm, 253) # 253 = all the 8 bits are lit except bit 1
    orig_just_cloud = np.bitwise_and(original_udm, 2)     # 2   = all the 8 bits are shut except bit 1
    return np.bitwise_or(prod_without_cloud, orig_just_cloud)


def apply_calibration(calibration_filename, image_matrix):
    calib = json.loads(open(calibration_filename, 'r').read())['calibration_info']
    calib_space = calib['calibration_spacing']
    calib_vec = np.array(calib['calibration_vector'])
    xp = np.arange(0, len(calib_vec) * calib_space, calib_space)
    x = np.linspace(0, len(calib_vec) + 1, image_matrix.shape[1])
    alpha = np.interp(x, xp, calib_vec)
    calibrated_image_matrix = im * alpha
    return calibrated_image_matrix


im = np.array(json.loads(open('im2.json', 'r').read()))
print('im', im.shape, '\n',im)
# print(scipy.linalg.sqrtm(ro_sqr))
# udm_prod = np.array(json.loads(open('udm_prod.json', 'r').read()))
# udm_orig = np.array(json.loads(open('udm_orig.json', 'r').read()))
# print(copy_cloud_mask(udm_orig, udm_prod))
out = apply_calibration('c.json', im)
print('out', out.shape, '\n',out)

