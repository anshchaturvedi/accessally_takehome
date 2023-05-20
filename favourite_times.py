from collections import defaultdict
import os


def get_hours_in_d_range(d: int) -> dict:
    hours_minutes_mapping = defaultdict(list)

    for hour in range(12, 25):
        finished = False
        for minute in range(0, 60):
            hour = hour if hour <= 12 else hour - 12
            hours_minutes_mapping[hour].append(f"{minute:02d}")
            d -= 1
            if d < 0:
                finished = True
                break
        if finished:
            break

    return hours_minutes_mapping


def get_all_arithmetic_sequences(d: int) -> int:
    count = 0
    all_times = get_hours_in_d_range(d)
    if d < 60:
        count += get_all_arithmetic_sequences_for_hour(12, all_times[12])
    else:
        count += get_all_arithmetic_sequences_for_hour(12, all_times[12])

        for i in range(0, 12):
            if i in all_times:
                count += get_all_arithmetic_sequences_for_hour(i, all_times[i])

    return count


def get_all_arithmetic_sequences_for_hour(hour: int, minutes) -> int:
    nums = []
    count = 0
    if hour >= 10:
        nums.append(hour // 10)
        nums.append(hour % 10)
    else:
        nums.append(hour)

    for minute in minutes:
        for digit in minute:
            nums.append(int(digit))

        if is_arithmetic_sequence(nums):
            count += 1

        # clear minutes
        nums.pop()
        nums.pop()

    # return result
    return count


def is_arithmetic_sequence(nums: list[int]) -> bool:
    if len(nums) == 3:
        return nums[2] - nums[1] == nums[1] - nums[0]
    elif len(nums) == 4:
        return nums[3] - nums[2] == nums[2] - nums[1] == nums[1] - nums[0]
    else:
        return False


def favourite_times(d: int) -> int:
    # keeps track of whether the duration will cause us to loop back to 12:00
    # if yes, then we can optimize and not have to recalculate
    full_loop = 12 * 60
    num_loops, remainder_duration = None, None

    # if d > (12*60) then we are just looping back again, instead of recalculating
    # all the arithmetic sequences again, we can just do `d = d mod full_loop`

    if d > full_loop:
        num_loops = d // full_loop
        remainder_duration = d % full_loop

    # if there are loops, we calculate all the arithmetic sequences the first time
    ans = 0
    if num_loops:
        ans += get_all_arithmetic_sequences(720) * num_loops
        ans += get_all_arithmetic_sequences(remainder_duration)
    else:
        ans += get_all_arithmetic_sequences(d)

    return ans


def run_test(input_file, output_file):
    """
    Copied from previous projects, acts a basic test harness
    against the provided .in and .out test cases
    """
    with open(input_file, "r") as f:
        input_data = f.read().strip()

    with open(output_file, "r") as f:
        expected_output = f.read().strip()

    result = favourite_times(int(input_data))

    if result == int(expected_output):
        print(f"Test PASSED: {input_file}")
    else:
        print(f"Test FAILED:     {input_file}")
        print("Expected output:", expected_output)
        print("Actual output:  ", result)
    print()


# runs the tests
test_directory = "favourite_times_tests"

for filename in os.listdir(test_directory):
    if filename.endswith(".in"):
        input_file = os.path.join(test_directory, filename)
        output_file = os.path.join(test_directory, filename[:-3] + ".out")
        run_test(input_file, output_file)
