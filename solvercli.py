def cli():
    print("原神稻妻关灯谜题求解器2.0")
    modular = int(input("请输入 模数："))
    init_status_str = input(f"请输入 初始状态（一串1-{modular}的正整数）：")  # 123
    block_count = len(init_status_str)
    target_status_str = input(f"请输入 目标状态（一个1-{modular}的正整数）：")  # 2，都亮2个灯，可留空。
    patterns_str = []
    for current_block_index in range(block_count):
        current_str = input(f"请输入第{current_block_index + 1}个方块的影响模式：（{block_count}个1-{modular}的正整数）")
        patterns_str.append(current_str)
    return modular, block_count, init_status_str, target_status_str, patterns_str  # 获得用户输入的信息。


def single_calculate(modular, patterns, start, end):  # 模数、变化样式、初始状态，最后状态
    from sympy import Matrix
    from diophantine import solve

    A_mat = []
    B_vet = []
    for index, current_pattern in enumerate(patterns):
        extra_list = [0] * len(patterns[0])
        extra_list[index] = -modular
        A_mat.append(current_pattern + extra_list)
        B_vet.append(end[index] - start[index])
    return solve(Matrix(A_mat), Matrix(B_vet))


# 处理求解结果，返回所有可能的解（拨动次数）
def process_solution(solution, modular):
    if len(solution) > 0:
        block_count = int(len(solution[0]) / 2)
        all_primitive_solutions = [list(single_solution)[:block_count] for single_solution in solution]
        return [[(x if x >= 0 else x + modular) for x in current_solution] for current_solution in all_primitive_solutions]  # 如果某个值小于0，则加模
    else:
        return []


def get_solution(modular, block_count, init_status_str, target_status_str, patterns_str):
    pattern_list = [[int(x) for x in single_pattern_string] for single_pattern_string in patterns_str]  # patterns don't need minus 1
    start_list = [int(x) - 1 for x in init_status_str]
    solutions = []
    if target_status_str == "":
        for end_status in range(modular):  # 比如用户模4，则0123都可能是最后的情况
            solutions += process_solution(single_calculate(modular, pattern_list, start_list, [end_status] * block_count), modular)
    else:
        solutions = process_solution(single_calculate(modular, pattern_list, start_list, [int(target_status_str) - 1] * block_count), modular)
        # solution是二维数组，记录了所有的可能的解。
    return solutions


def main():
    modular, block_count, init_status_str, target_status_str, patterns_str = cli()
    solutions = get_solution(modular, block_count, init_status_str, target_status_str, patterns_str)
    if len(solutions) == 0:
        print("无解")
    else:
        solutions.sort(key=sum)
        print("\n")
        print("\n".join(["".join([str(x) for x in t]) for t in solutions]))


if __name__ == "__main__":
    main()
