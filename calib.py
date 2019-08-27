import sys
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
    calibrated_image_matrix = image_matrix * alpha

    return calibrated_image_matrix


def usage_exit():
    print('Run with one of the following usages:')
    print('1. calib.py calib image_filename calibration_filename')
    print('2. calib.py cloud original_udm_filename product_udm_filename')
    sys.exit(2)


def main(argv):
    if (len(argv) < 3):
        print('not enough params')
        usage_exit()

    if (argv[0] == 'calib'):
        # calibrate image by vector
        image = np.array(json.loads(open(argv[1], 'r').read()))
        calib_filename = argv[2]
        calibrated_image_matrix = apply_calibration(calib_filename, image)
        print('calibrated_image_matrix', calibrated_image_matrix.shape, '\n',calibrated_image_matrix)

    elif (argv[0] == 'cloud'):
        # correct cloud udm
        udm_orig = np.array(json.loads(open(argv[1], 'r').read()))
        udm_prod = np.array(json.loads(open(argv[2], 'r').read()))
        corrected_cloud_udm = copy_cloud_mask(udm_orig, udm_prod)
        print('corrected_cloud_udm', corrected_cloud_udm.shape, '\n',corrected_cloud_udm)

    else:
        # error
        print('unknown operator', argv[1])
        usage_exit()


if __name__ == "__main__":
    main(sys.argv[1:])
