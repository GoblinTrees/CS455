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
    'wave': {
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
    'fist_pump': {
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
    'superhero': {
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
    }, 'cover face': {
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
    }, 'fight': {
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
        "RShoulder": 6000,
        "Rbicep": 6600,
        "Relbow": 6000,
        "Rwrist": 6000,
        "Rclaw": 6000,
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
        "RShoulder": 6000,
        "Rbicep": 6600,
        "Relbow": 6000,
        "Rwrist": 6000,
        "Rclaw": 6000,
        "Waist": 6000,
        "L_Motors": 6000,
        "R_Motors": 6000,
    },
    'raise_left_arm': {
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
    'lower_left_arm': {
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
    'cross_arms': {
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
    'spread_arms': {
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
    'clap_hands': {
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
    'point_right': {
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
    'point_left': {
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
    'fold_arms': {
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
    'look_left': {
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
    'look_right': {
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
    'tilt_head_up': {
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
    'tilt_head_down': {
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
