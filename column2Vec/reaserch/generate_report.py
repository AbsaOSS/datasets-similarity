import numpy as np


def compute_avg(test_results: dict):
    result = {}
    for column in test_results.keys():
        for test_type in test_results[column].keys():
            if test_results[column][test_type][0]:
                result[test_type] = [0, 0, 0] if test_type not in result.keys() else result[test_type]
                result[test_type][0] += 1
                result[test_type][1] += 1
                result[test_type][2] += 1
            else:
                result[test_type] = [0, 0, 0] if test_type not in result.keys() else result[test_type]
                result[test_type][0] += test_results[column][test_type][1][0]
                result[test_type][1] += test_results[column][test_type][1][1]
                result[test_type][2] += test_results[column][test_type][1][2]

    for res in result:
        result[res][0] = result[res][0] / len(test_results.keys())
        result[res][1] = result[res][1] / len(test_results.keys())
        result[res][2] = result[res][2] / len(test_results.keys())
    return result

def make_plot(result: dict, file_name: str):
    import matplotlib.pyplot as plt
    col_first = list()
    col_second = list()
    first_second = list()

    for key in result.keys():
        col_first.append(result[key][0])
        col_second.append(result[key][1])
        first_second.append(result[key][2])

    barWidth = 0.25
    fig = plt.subplots(figsize=(12, 8))
    br1 = np.arange(len(col_first))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]

    plt.bar(br1, col_first, color='r', width=barWidth,
            edgecolor='grey', label='First half')
    plt.bar(br2, col_second, color='g', width=barWidth,
            edgecolor='grey', label='Second half')
    plt.bar(br3, first_second, color='b', width=barWidth,
            edgecolor='grey', label='First second')

    plt.xlabel('Function type', fontweight='bold', fontsize=15)
    plt.ylabel('Similarity', fontweight='bold', fontsize=15)
    plt.xticks([r + barWidth for r in range(len(col_first))],
               result.keys())

    plt.legend()
    plt.savefig(f"{file_name}_plot.png")
    return True

def generate_report( test_results: dict, file_name: str):
    result = compute_avg(test_results)
    make_plot(result, file_name)

    with open(f"{file_name}.md", "w") as f:
        f.write(f"![{file_name}_plot.png]({file_name}_plot.png)\n")
        for column in test_results.keys():
            f.write(f"## --- Start Column: {column} ---\n")
            for test_type in test_results[column].keys():
                f.write(f"### {test_type}\n")
                # f.write(f"{test_results[column][test_type][1]}\n")
                f.write(f"For {column}:\n - whole column and first half: {test_results[column][test_type][1][0]}\n "
                f"- whole column and second half: {test_results[column][test_type][1][1]}\n - first half"
                f" and second half: {test_results[column][test_type][1][2]}\n\n")
            f.write("\n")
    print(f"REPORT GENERATED: {file_name}.md")
    return True

def generate_time_report( test_results: dict, file_name: str):
    result = {}
    for column in test_results.keys():
        for test_type in test_results[column].keys():
            result[test_type] = 0 if test_type not in result.keys() else result[test_type]
            result[test_type] += test_results[column][test_type][1]
    for res in result:
        result[res] = result[res] / len(test_results.keys())

    make_plot(result, file_name)

    with open(f"{file_name}.md", "w") as f:
        f.write(f"![{file_name}_plot.png]({file_name}_plot.png)\n")
        for column in test_results.keys():
            f.write(f"## --- Start Column: {column} ---\n")
            for test_type in test_results[column].keys():
                f.write(f"### {test_type}\n")
                # f.write(f"{test_results[column][test_type][1]}\n")
                f.write(f"For {column}:\n - whole column and first half: {test_results[column][test_type][1][0]}\n "
                f"- whole column and second half: {test_results[column][test_type][1][1]}\n - first half"
                f" and second half: {test_results[column][test_type][1][2]}\n\n")
            f.write("\n")
    print(f"REPORT GENERATED: {file_name}.md")
    return True
