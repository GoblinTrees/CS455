# this is a repo for the tango's poses
import random


def fiveStep(startDict: dict, endDict: dict) -> list:
    steps = []
    # add the first step
    steps.append(startDict)

    # for each value in dict, take the difference between the two values, divide it by 5, and assign the dict to iteration

    for i in range(5):  # 5 steps in between
        intermediate_step = {}
        for key in startDict:
            # Calculate the difference between start and end values
            diff = endDict[key] - startDict[key]
            # Divide the difference by 5 to get the increment
            increment = diff / 5
            # Calculate the value for the intermediate step
            intermediate_value = startDict[key] + (increment * i)
            # Round to the nearest integer (assuming motor values are integers)
            intermediate_step[key] = round(intermediate_value)
        # Append the intermediate step to the steps list
        steps.append(intermediate_step)

    # finally, iterate through the list and append each entry into the steps list

    # add the final step
    steps.append(endDict)
    return steps


def tenStep(startDict: dict, endDict: dict) -> list:
    steps = []
    # add the first step
    steps.append(startDict)

    # for each value in dict, take the difference between the two values, divide it by 5, and assign the dict to iteration

    for i in range(1, 10):  # 5 steps in between
        intermediate_step = {}
        for key in startDict:
            # Calculate the difference between start and end values
            diff = endDict[key] - startDict[key]
            # Divide the difference by 5 to get the increment
            increment = diff / 10
            # Calculate the value for the intermediate step
            intermediate_value = startDict[key] + (increment * i)
            # Round to the nearest integer (assuming motor values are integers)
            intermediate_step[key] = round(intermediate_value)
        # Append the intermediate step to the steps list
        steps.append(intermediate_step)

    # finally, iterate through the list and append each entry into the steps list

    # add the final step
    steps.append(endDict)
    return steps


def nStep(startDict: dict, endDict: dict, numStep: int) -> list:
    steps = []
    # add the first step
    steps.append(startDict)

    # for each value in dict, take the difference between the two values, divide it by 5, and assign the dict to iteration

    for i in range(1, numStep):  # 5 steps in between
        intermediate_step = {}
        for key in startDict:
            # Calculate the difference between start and end values
            diff = endDict[key] - startDict[key]
            # Divide the difference by numStep to get the increment
            increment = diff / numStep
            # Calculate the value for the intermediate step
            intermediate_value = startDict[key] + (increment * i)
            # Round to the nearest integer (assuming motor values are integers)
            intermediate_step[key] = round(intermediate_value)
        # Append the intermediate step to the steps list
        steps.append(intermediate_step)

    # finally, iterate through the list and append each entry into the steps list

    # add the final step
    steps.append(endDict)
    return steps


def get_random_pose_key(dictionary):
    if not isinstance(dictionary, dict):
        raise TypeError("Input must be a dictionary")
    if not dictionary:
        raise ValueError("Dictionary is empty")

    return random.choice(list(dictionary.keys()))


poses = {
    'neutral': {
        "Headtilt": 6000,
        "Headturn": 6000,
        "Lshoulder": 6000,
        "Lbicep": 6000,
        "Lelbow": 6000,
        "Lwrist": 6000,
        "Lclaw": 6000,
        "RShoulder": 6000,
        "Rbicep": 6600,
        "Relbow": 6000,
        "Rwrist": 6000,
        "Rclaw": 6000,
        "Waist": 6000,
        "L_Motors": 6000,
        "R_Motors": 6000,
    },
    'rwave': {
        "Headtilt": 6000,
        "Headturn": 6000,
        "Lshoulder": 6000,
        "Lbicep": 6000,
        "Lelbow": 6000,
        "Lwrist": 6000,
        "Lclaw": 6000,
        "RShoulder": 8200,
        "Rbicep": 9000,
        "Relbow": 9000,
        "Rwrist": 6000,
        "Rclaw": 6000,
        "Waist": 6000,
        "L_Motors": 6000,
        "R_Motors": 6000,
    },
    'fist_pump': {
        "Headtilt": 3000,
        "Headturn": 5000,
        "Lshoulder": 6000,
        "Lbicep": 6200,
        "Lelbow": 5000,
        "Lwrist": 6000,
        "Lclaw": 6400,
        "RShoulder": 6000,
        "Rbicep": 6600,
        "Relbow": 8400,
        "Rwrist": 6000,
        "Rclaw": 9000,
        "Waist": 6000,
        "L_Motors": 6000,
        "R_Motors": 6000,
    },
    'superhero': {
        "Headtilt": 7200,
        "Headturn": 6000,
        "Lshoulder": 7200,
        "Lbicep": 3400,
        "Lelbow": 3000,
        "Lwrist": 6000,
        "Lclaw": 6000,
        "RShoulder": 9000,
        "Rbicep": 6200,
        "Relbow": 6000,
        "Rwrist": 6000,
        "Rclaw": 6000,
        "Waist": 6000,
        "L_Motors": 6000,
        "R_Motors": 6000,
    },
    'cover face': {
        "Headtilt": 3000,
        "Headturn": 6000,
        "Lshoulder": 3000,
        "Lbicep": 8400,
        "Lelbow": 7600,
        "Lwrist": 6000,
        "Lclaw": 7800,
        "RShoulder": 9000,
        "Rbicep": 4400,
        "Relbow": 7400,
        "Rwrist": 8400,
        "Rclaw": 9000,
        "Waist": 6000,
        "L_Motors": 6000,
        "R_Motors": 6000,
    }, 'fight': {
        "Headtilt": 4800,
        "Headturn": 6000,
        "Lshoulder": 3800,
        "Lbicep": 7200,
        "Lelbow": 6800,
        "Lwrist": 6000,
        "Lclaw": 6000,
        "RShoulder": 7200,
        "Rbicep": 4600,
        "Relbow": 9000,
        "Rwrist": 9000,
        "Rclaw": 6000,
        "Waist": 4000,
        "L_Motors": 6000,
        "R_Motors": 6000,
    },
}
standard = {
    'raise_right_arm': {
        "Headtilt": 6000,
        "Headturn": 6000,
        "Lshoulder": 6000,
        "Lbicep": 6000,
        "Lelbow": 6000,
        "Lwrist": 6000,
        "Lclaw": 6000,
        "RShoulder": 9000,
        "Rbicep": 7200,
        "Relbow": 9000,
        "Rwrist": 6200,
        "Rclaw": 3000,
        "Waist": 6000,
        "L_Motors": 6000,
        "R_Motors": 6000,
    },
    'lower_right_arm': {
        "Headtilt": 6000,
        "Headturn": 6000,
        "Lshoulder": 6000,
        "Lbicep": 6000,
        "Lelbow": 6000,
        "Lwrist": 6000,
        "Lclaw": 6000,
        "RShoulder": 3000,
        "Rbicep": 7200,
        "Relbow": 3000,
        "Rwrist": 9000,
        "Rclaw": 9000,
        "Waist": 6000,
        "L_Motors": 6000,
        "R_Motors": 6000,
    },
    'raise_left_arm': {
        "Headtilt": 6000,
        "Headturn": 6000,
        "Rshoulder": 6000,
        "Rbicep": 6000,
        "Relbow": 6000,
        "Rwrist": 6000,
        "Rclaw": 6000,
        "LShoulder": 9000,
        "Lbicep": 7200,
        "Lelbow": 9000,
        "Lwrist": 6200,
        "Lclaw": 3000,
        "Waist": 6000,
        "L_Motors": 6000,
        "R_Motors": 6000,
    },
    'lower_left_arm': {
        "Headtilt": 6000,
        "Headturn": 6000,
        "Rshoulder": 6000,
        "Rbicep": 6000,
        "Relbow": 6000,
        "Rwrist": 6000,
        "Rclaw": 6000,
        "LShoulder": 3000,
        "Lbicep": 7200,
        "Lelbow": 3000,
        "Lwrist": 9000,
        "Lclaw": 9000,
        "Waist": 6000,
        "L_Motors": 6000,
        "R_Motors": 6000,
    },
    'cross_arms': {
        "Headtilt": 5600,
        "Headturn": 6000,
        "Lshoulder": 4600,
        "Lbicep": 9000,
        "Lelbow": 5600,
        "Lwrist": 6000,
        "Lclaw": 6000,
        "RShoulder": 7800,
        "Rbicep": 3000,
        "Relbow": 6000,
        "Rwrist": 6000,
        "Rclaw": 6000,
        "Waist": 6000,
        "L_Motors": 6000,
        "R_Motors": 6000,
    },
    'spread_arms': {
        "Headtilt": 6000,
        "Headturn": 6000,
        "Lshoulder": 3000,
        "Lbicep": 3000,
        "Lelbow": 9000,
        "Lwrist": 9000,
        "Lclaw": 6000,
        "RShoulder": 9000,
        "Rbicep": 9000,
        "Relbow": 8400,
        "Rwrist": 9000,
        "Rclaw": 3000,
        "Waist": 6000,
        "L_Motors": 6000,
        "R_Motors": 6000,
    },
    'clap_hands': {
        "Headtilt": 6000,
        "Headturn": 6000,
        "Lshoulder": 4400,
        "Lbicep": 9000,
        "Lelbow": 9000,
        "Lwrist": 9000,
        "Lclaw": 3000,
        "RShoulder": 7000,
        "Rbicep": 3000,
        "Relbow": 8400,
        "Rwrist": 9000,
        "Rclaw": 3000,
        "Waist": 6000,
        "L_Motors": 6000,
        "R_Motors": 6000,
    },
    'point_right': {
        "Headtilt": 5400,
        "Headturn": 3000,
        "Lshoulder": 5400,
        "Lbicep": 6000,
        "Lelbow": 6000,
        "Lwrist": 6000,
        "Lclaw": 6000,
        "RShoulder": 9000,
        "Rbicep": 9000,
        "Relbow": 6000,
        "Rwrist": 6000,
        "Rclaw": 6000,
        "Waist": 9000,
        "L_Motors": 6000,
        "R_Motors": 6000,
    },
    'point_left': {
        "Headtilt": 6000,
        "Headturn": 3000,
        "Lshoulder": 3000,
        "Lbicep": 3000,
        "Lelbow": 6000,
        "Lwrist": 6000,
        "Lclaw": 6000,
        "RShoulder": 6000,
        "Rbicep": 6600,
        "Relbow": 6000,
        "Rwrist": 6000,
        "Rclaw": 6000,
        "Waist": 6000,
        "L_Motors": 6000,
        "R_Motors": 6000,
    },
    'look_left': {
        "Headtilt": 6000,
        "Headturn": 9000,
        "Lshoulder": 6000,
        "Lbicep": 6000,
        "Lelbow": 6000,
        "Lwrist": 6000,
        "Lclaw": 6000,
        "RShoulder": 6000,
        "Rbicep": 6600,
        "Relbow": 6000,
        "Rwrist": 6000,
        "Rclaw": 6000,
        "Waist": 6000,
        "L_Motors": 6000,
        "R_Motors": 6000,
    },
    'look_right': {
        "Headtilt": 6000,
        "Headturn": 3000,
        "Lshoulder": 6000,
        "Lbicep": 6000,
        "Lelbow": 6000,
        "Lwrist": 6000,
        "Lclaw": 6000,
        "RShoulder": 6000,
        "Rbicep": 6600,
        "Relbow": 6000,
        "Rwrist": 6000,
        "Rclaw": 6000,
        "Waist": 6000,
        "L_Motors": 6000,
        "R_Motors": 6000,
    },
    'tilt_head_up': {
        "Headtilt": 7400,
        "Headturn": 6000,
        "Lshoulder": 6000,
        "Lbicep": 6000,
        "Lelbow": 6000,
        "Lwrist": 6000,
        "Lclaw": 6000,
        "RShoulder": 6000,
        "Rbicep": 6600,
        "Relbow": 6000,
        "Rwrist": 6000,
        "Rclaw": 6000,
        "Waist": 6000,
        "L_Motors": 6000,
        "R_Motors": 6000,
    },
    'tilt_head_down': {
        "Headtilt": 4000,
        "Headturn": 6000,
        "Lshoulder": 6000,
        "Lbicep": 6000,
        "Lelbow": 6000,
        "Lwrist": 6000,
        "Lclaw": 6000,
        "RShoulder": 6000,
        "Rbicep": 6600,
        "Relbow": 6000,
        "Rwrist": 6000,
        "Rclaw": 6000,
        "Waist": 6000,
        "L_Motors": 6000,
        "R_Motors": 6000,
    },
}

all_poses = {}
all_poses.update(standard)
all_poses.update(poses)

if __name__ == "__main__":
    # Test with 'standard' dictionary
    random_pose = get_random_pose_key(standard)
    print("Random pose from 'standard':", random_pose)

    # Test with 'poses' dictionary
    random_pose = get_random_pose_key(poses)
    print("Random pose from 'poses':", random_pose)

    # Test with 'all_poses' dictionary
    random_pose = get_random_pose_key(all_poses)
    print("Random pose from 'all_poses':", random_pose)
