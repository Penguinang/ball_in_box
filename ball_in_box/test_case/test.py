from ball_in_box.ballinbox import ball_in_box
from ball_in_box.area_sum import area_sum
from ball_in_box import validate as val

def test():
    test_case = [
        [(0.5, 0.5),(0.5, -0.3)],
        [(0.15, 0.05),(-0.5, -0.33),(-0.245, -0.05),(-0.15, -0.33)],
        [(0.1, -0.5),(-0.5, -0.3),(-0.89, 0.90),(-0.01, 0.009)]        
    ]
    pass_count = 0
    total_count = len(test_case)

    for case in test_case:
        num_of_circle = 5
        circles = ball_in_box(num_of_circle, case)

        if num_of_circle == len(circles) and val.validate(circles, case):
            area = area_sum(circles)
            print("Total area: {}".format(area))
            pass_count += 1
        else:
            print("Error: no good circles.")

    print("Total test case number: %d"%total_count)
    print("Pass test case number: %d"%pass_count)
    print("Pass rate %f"%(pass_count / total_count))

if __name__ == "__main__":
    test()