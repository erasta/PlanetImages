import json
import numpy as np

def copy_cloud_mask(original_udm, product_udm):
    cloud_bit_pos = 1
    cloud_bit_mask = 1 << cloud_bit_pos

    # take just the cloud bit from orig UDM
    orig_just_cloud = np.bitwise_and(original_udm, cloud_bit_mask)

    # remove just the cloud bit from prod UDM
    prod_without_cloud = np.bitwise_and(product_udm, 255 ^ cloud_bit_mask)

    # put the orig UDM cloud bit unto prod UDM
    return np.bitwise_or(prod_without_cloud, orig_just_cloud)


def apply_calibration(calibration_filename, image_matrix):
    # reading the json file contents
    calib_json = json.loads(open(calibration_filename, 'r').read())
    calib = calib_json['calibration_info']
    calib_space = calib['calibration_spacing']
    calib_vec = np.array(calib['calibration_vector'])

    # interpolating the calibration vector to fit the image size
    xp = np.arange(0, len(calib_vec) * calib_space, calib_space)
    x = np.linspace(0, len(calib_vec) + 1, image_matrix.shape[1])
    alpha = np.interp(x, xp, calib_vec)

    # calibrating the image
    calibrated_image_matrix = im * alpha

    return calibrated_image_matrix


im = np.array(json.loads(open('data/im2.json', 'r').read()))
print('im', im.shape, '\n',im)
# udm_prod = np.array(json.loads(open('data/udm_prod.json', 'r').read()))
# udm_orig = np.array(json.loads(open('data/udm_orig.json', 'r').read()))
# print(copy_cloud_mask(udm_orig, udm_prod))
out = apply_calibration('data/c.json', im)
print('out', out.shape, '\n',out)

