import os


def blood_distribution(blood_units: dict[str: int], patients: dict[str: int]) -> int:
    # the idea is to assign from most restrictive to least restrictive
    # so, first assign O-, then O+, then A-, then A+, etc.

    blood_types = ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"]
    max_blood_recipients = 0

    for blood_type in blood_types:
        # we have more than enough exact blood for this group
        if blood_units[blood_type] >= patients[blood_type]:
            max_blood_recipients += patients[blood_type]
            blood_units[blood_type] -= patients[blood_type]
            patients[blood_type] -= patients[blood_type]

        # we don't have enough exact blood matches and need to look for sum more
        else:
            blood_groups_to_check = allowed_blood_groups(blood_type)

            for other_blood_group in blood_groups_to_check:
                if patients[blood_type] <= 0:
                    break

                if blood_units[other_blood_group] > 0:
                    diff = min(blood_units[other_blood_group], patients[blood_type])
                    max_blood_recipients += diff
                    blood_units[other_blood_group] -= diff
                    patients[blood_type] -= diff

    return max_blood_recipients 


def allowed_blood_groups(blood_group):
    allowed_mapping = {
        "O+": ["O+", "O-"],
        "O-": ["O-"],
        "A-": ["A-", "O-"],
        "A+": ["A+", "A-", "O-", "O+"],
        "B+": ["B+", "B-", "O+", "O-"],
        "B-": ["B-", "O-"],
        "AB+": ["AB+", "AB-", "O+", "O-", "A+", "A-", "B+", "B-"],
        "AB-": ["AB-", "A-", "B-", "O-"],
    }
    return allowed_mapping[blood_group]


def process_input(input_string):
    blood_units, patients = input_string.strip().split("\n")
    blood_units = list(map(int, blood_units.split()))
    patients = list(map(int, patients.split()))

    blood_groups = ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"]
    blood_dict = dict(zip(blood_groups, blood_units))

    patients_dict = dict(zip(blood_groups, patients))

    return blood_dict, patients_dict


def run_test(input_file, output_file):
    """
    Copied from previous projects, acts a basic test harness
    against the provided .in and .out test cases
    """
    with open(input_file, "r") as f:
        input_data = f.read().strip()

    with open(output_file, "r") as f:
        expected_output = f.read().strip()

    (blood, patients) = process_input(input_data)

    result = blood_distribution(blood, patients)

    if result == int(expected_output):
        print(f"Test PASSED: {input_file}")
    else:
        print(f"Test FAILED:     {input_file}")
        print("Expected output:", expected_output)
        print("Actual output:  ", result)
    print()


# runs the tests
test_directory = "blood_distribution_tests"

for filename in os.listdir(test_directory):
    if filename.endswith(".in"):
        input_file = os.path.join(test_directory, filename)
        output_file = os.path.join(test_directory, filename[:-3] + ".out")
        run_test(input_file, output_file)
