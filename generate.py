import numpy as np
from collections import defaultdict
import json


camera_idx_to_name = {
    0: '54138969',
    1: '55011271',
    2: '58860488',
    3: '60457274'
}


def get_camera_parameters(metadata, camera, subject):
    # some black magic with indexes
    metadata_slice = np.zeros(15)
    start = 6 * (camera * 11 + (subject - 1))

    metadata_slice[:6] = metadata[start:start + 6]
    metadata_slice[6:] = metadata[265 + camera * 9 - 1:265 + (camera + 1) * 9 - 1]

    # extrinsics
    x, y, z = -metadata_slice[0], metadata_slice[1], -metadata_slice[2]
    c = np.cos(x)
    c2 = np.cos(y)
    c3 = np.cos(z)

    s1 = np.sin(x)
    s2 = np.sin(y)
    s3 = np.sin(z)

    R_x = np.array([
        [1, 0, 0],
        [0, np.cos(x), np.sin(x)],
        [0, -np.sin(x), np.cos(x)]
    ])

    R_y = np.array([
        [np.cos(y), 0, np.sin(y)],
        [0, 1, 0],
        [-np.sin(y), 0, np.cos(y)]
    ])

    R_z = np.array([
        [np.cos(z), np.sin(z), 0],
        [-np.sin(z), np.cos(z), 0],
        [0, 0, 1]
    ])

    R = R_x @ R_y @ R_z
    
    t = metadata_slice[3:6].reshape(-1, 1)
    t = -R @ t
    
    R = R.tolist()
    t = t.tolist()

    # intrinsics
    fx, fy = metadata_slice[6:8]
    cx, cy = metadata_slice[8:10]
    calibration_matrix = [
        [fx, 0.0, cx],
        [0.0, fy, cy],
        [0.0, 0.0, 1.0]
    ]

    k1, k2, k3 = metadata_slice[10:13]
    p1, p2 = metadata_slice[13:15]
    distortion = [k1, k2, p1, p2, k3]
    
    return R, t, calibration_matrix, distortion


def main():
    metadata = np.load("metadata.npy")
    camera_parameters = defaultdict(lambda: defaultdict(dict))

    for camera in range(4):
        for subject in range(1, 11 + 1):
            R, t, calibration_matrix, distortion = get_camera_parameters(metadata, camera, subject)
            camera_name = camera_idx_to_name[camera]

            # intrinsic parameters are the same for all subjects
            if subject == 1:
                camera_parameters['intrinsics'][camera_name] = {
                    'calibration_matrix': calibration_matrix,
                    'distortion': distortion
                }

            # extrinsics
            camera_parameters['extrinsics']['S{}'.format(subject)][camera_name] = {
                'R': R,
                't': t
            }
            
    with open('camera-parameters.json', 'w') as fout:
        json.dump(camera_parameters, fout, indent=2)
        
    print('Success!')


if __name__ == '__main__':
    main()