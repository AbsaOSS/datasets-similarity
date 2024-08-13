"""File to generate report from test results"""
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


def compute_avg(test_results: dict) -> dict:
    """
    Compute average similarity for each test type
    :param test_results: dict of test results
    :return: dict of average results
    """
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


def make_plot(result: dict, file_name: str) -> bool:
    """
    Make plot from results
    :param result: dict of test results
    :param file_name: name of the file to save plot
    :return: always True
    """

    col_first = list()
    col_second = list()
    first_second = list()

    for key in result.keys():
        col_first.append(result[key][0])
        col_second.append(result[key][1])
        first_second.append(result[key][2])

    bar_width = 0.25
    br1 = np.arange(len(col_first))
    br2 = [x + bar_width for x in br1]
    br3 = [x + bar_width for x in br2]

    st.bar_chart(data=result.values(),
                 x_label='Function type', y_label='Time in seconds')
    plt.bar(br1, col_first, color='r', width=bar_width,
            edgecolor='grey', label='First half')
    plt.bar(br2, col_second, color='g', width=bar_width,
            edgecolor='grey', label='Second half')
    plt.bar(br3, first_second, color='b', width=bar_width,
            edgecolor='grey', label='First second')

    plt.xlabel('Function type', fontweight='bold', fontsize=15)
    plt.ylabel('Similarity', fontweight='bold', fontsize=15)
    plt.xticks([r + bar_width for r in range(len(col_first))],
               result.keys())

    plt.legend()
    plt.savefig(f"files/{file_name}_plot.png")
    plt.clf()
    return True


def generate_stability_report(test_results: dict, file_name: str) -> bool:
    """
    Generate report from stability test results
    :param test_results: dict of test results
    :param file_name: name of the file to save report
    :return: always True
    """
    st.title('Stability test')
    # result = compute_avg(test_results)
    # make_plot(result, file_name)
    result = {}
    len_column = 0
    first = True
    for column in test_results.keys():
        if first:
            for test_type in test_results[column].keys():
                result[test_type] = 0
            first = False
        len_column += 1



    with (open(f"files/{file_name}.md", "w")as f):
        f.write("# Stability test\n\n")
        for column in test_results.keys():
            for test_type in test_results[column].keys():
                if test_results[column][test_type][0]:
                    result[test_type] += 1

        for i in result:
            f.write(f"## {i}\n")
            f.write(f"**SCORE:** {result[i]}\n\n")
            f.write(f"**PERCENTAGE:** {round((result[i]/len_column)*100)}%\n\n")

    print(f"REPORT GENERATED: {file_name}.md")
    return True


def generate_partial_column_report(test_results: dict, file_name: str) -> bool:
    """
    Generate report from partial test results
    :param test_results: dict of test results
    :param file_name: name of the file to save report
    :return: always True
    """
    st.title('Partial column test')
    result = compute_avg(test_results)
    make_plot(result, file_name)

    with open(f"files/{file_name}.md", "w") as f:
        f.write(f"![{file_name}_plot.png]({file_name}_plot.png)\n")
        for fun in result:
            f.write(f"## {fun}\n")
            f.write(f"**SCORE:** {round(result[fun][0] + result[fun][1] + result[fun][2], 3)}\n\n"
                    f"Average similarity for whole column and first half: {round(result[fun][0], 3)}\n"
                    f"Average similarity for whole column and second half: {round(result[fun][1], 3)}\n"
                    f"Average similarity for first half and second half: {round(result[fun][2], 3)}\n\n")
        f.write("---\n")
        for column in test_results.keys():
            f.write(f"## --- Start Column: {column} ---\n")
            for test_type in test_results[column].keys():
                f.write(f"### {test_type}\n")
                # f.write(f"{test_results[column][test_type][1]}\n")
                f.write(f"For {column}:\n - whole column and first half: {(test_results[column][test_type][1])[0]}\n "
                        f"- whole column and second half: {(test_results[column][test_type][1])[1]}\n - first half"
                        f" and second half: {(test_results[column][test_type][1])[2]}\n\n")
            f.write("\n")
    print(f"REPORT GENERATED: {file_name}.md")
    return True

def generate_time_report(test_results: dict, file_name: str):
    """
    Generate report from time test results
    :param test_results: dict of test results
    :param file_name: name of the file to save report
    """
    # st.title('Time test')

    result = {}
    for column in test_results.keys():
        for test_type in test_results[column].keys():
            result[test_type] = 0 if test_type not in result.keys() else result[test_type]
            result[test_type] += test_results[column][test_type][1]
    for res in result:
        result[res] = result[res] / len(test_results.keys())
        print(f"{res}: {result[res]}")

    # st.bar_chart(data=result.values(),
    #              x_label='Function type', y_label='Time in seconds')

    plt.bar(result.keys(), result.values())

    plt.xlabel('Function type', fontweight='bold', fontsize=15)
    plt.ylabel('Time in seconds', fontweight='bold', fontsize=15)

    plt.savefig(f"files/{file_name}_plot.png")
    plt.clf()


def similar_and_not_similar_file(file_name: str, test_results: dict, columns_to_test: list):
    """
    Generates two files similar and not_similar
    files contains list of columns for each column that are similar/not similar
    """
    with open(f"files/{file_name}similar.md", "w") as f_sim:
        with open(f"files/{file_name}not_similar.md", "w") as f_not:
            for function in test_results.keys():
                f_sim.write(f"## Function: {function} \n")
                f_not.write(f"## Function: {function} \n")
                written_column = []
                for column in test_results[function].keys():
                    if column[0] not in columns_to_test or column[1] not in columns_to_test:
                        continue
                    if column[0] not in written_column:
                        f_sim.write(f"\n### {column[0]}: \n")
                        f_not.write(f"\n### {column[0]}: \n")
                        written_column.append(column[0])
                    if test_results[function][column] > 0.5:
                        f_sim.write(f"{column[1]} ({test_results[function][column]}),  ")
                    else:

                        f_not.write(f"{column[1]} ({test_results[function][column]}),  ")
                f_sim.write("\n")
                f_not.write("\n")
            f_sim.write("\n")
            f_not.write("\n")
def generate_sim_report(test_results: dict, file_name: str):
    columns_to_test = ["reg_state1", "reg_city1", "country5", "country7", "Star46", "Star16",
                       "make3", "car_name4", "condition5", "date_added7", "fuel_type4", "fuel3",
                       "flight1", "tail_number1"]
    values = {
        "reg_state1": {
            "reg_city1": {"relationship": "YES", "value": 0.7},
            "country5": {"relationship": "YES", "value": 0.51},
            "country7": {"relationship": "YES", "value": 0.51},
            "condition5": {"relationship": "NO", "value": 0.35},
            "date_added7": {"relationship": "NO", "value": 0.35},
            "flight1": {"relationship": "NO", "value": 0.4},
            "tail_number1": {"relationship": "NO", "value": 0.4}
        },
        "reg_city1": {
            "reg_state1": {"relationship": "YES", "value": 0.7},
            "country5": {"relationship": "YES", "value": 0.51},
            "country7": {"relationship": "YES", "value": 0.51},
            "condition5": {"relationship": "NO", "value": 0.35},
            "date_added7": {"relationship": "NO", "value": 0.35},
            "flight1": {"relationship": "NO", "value": 0.4},
            "tail_number1": {"relationship": "NO", "value": 0.4}
        },
        "country5": {
            "reg_state1": {"relationship": "YES", "value": 0.51},
            "reg_city1": {"relationship": "YES", "value": 0.51},
            "country7": {"relationship": "YES", "value": 0.65},
            "condition5": {"relationship": "NO", "value": 0.35},
            "date_added7": {"relationship": "NO", "value": 0.35},
            "flight1": {"relationship": "NO", "value": 0.4},
            "tail_number1": {"relationship": "NO", "value": 0.4}
        },
        "country7": {
            "reg_state1": {"relationship": "YES", "value": 0.51},
            "reg_city1": {"relationship": "YES", "value": 0.51},
            "country5": {"relationship": "YES", "value": 0.65},
            "condition5": {"relationship": "NO", "value": 0.35},
            "date_added7": {"relationship": "NO", "value": 0.35},
            "flight1": {"relationship": "NO", "value": 0.4},
            "tail_number1": {"relationship": "NO", "value": 0.4}
        },
        "star46": {
            "star16": {"relationship": "YES", "value": 0.75},
            "condition5": {"relationship": "NO", "value": 0.35},
            "date_added7": {"relationship": "NO", "value": 0.35},
            "flight1": {"relationship": "NO", "value": 0.35},
            "tail_number1": {"relationship": "NO", "value": 0.35}
        },
        "star16": {
            "star46": {"relationship": "YES", "value": 0.75},
            "condition5": {"relationship": "NO", "value": 0.35},
            "date_added7": {"relationship": "NO", "value": 0.35},
            "flight1": {"relationship": "NO", "value": 0.35},
            "tail_number1": {"relationship": "NO", "value": 0.35}
        },
        "make3": {
            "car_name4": {"relationship": "YES", "value": 0.6},
            "condition5": {"relationship": "NO", "value": 0.45},
            "date_added7": {"relationship": "NO", "value": 0.45},
            "flight1": {"relationship": "NO", "value": 0.45},
            "tail_number1": {"relationship": "NO", "value": 0.45}
        },
        "car_name4": {
            "make3": {"relationship": "YES", "value": 0.6},
            "condition5": {"relationship": "NO", "value": 0.35},
            "date_added7": {"relationship": "NO", "value": 0.35},
            "flight1": {"relationship": "NO", "value": 0.35},
            "tail_number1": {"relationship": "NO", "value": 0.35}
        },
        "condition5": {
            "date_added7": {"relationship": "YES", "value": 0.6},
            "reg_city1": {"relationship": "NO", "value": 0.35},
            "reg_state1": {"relationship": "NO", "value": 0.35},
            "country5": {"relationship": "NO", "value": 0.35},
            "country7": {"relationship": "NO", "value": 0.35},
            "Star46": {"relationship": "NO", "value": 0.35},
            "Star16": {"relationship": "NO", "value": 0.35},
            "make3": {"relationship": "NO", "value": 0.4},
            "car_name4": {"relationship": "NO", "value": 0.35},
            "fuel_type4": {"relationship": "NO", "value": 0.35},
            "fuel3": {"relationship": "NO", "value": 0.35},
            "flight1": {"relationship": "NO", "value": 0.4},
            "tail_number1": {"relationship": "NO", "value": 0.4}
        },
        "date_added7": {
            "condition5": {"relationship": "YES", "value": 0.6},
            "reg_city1": {"relationship": "NO", "value": 0.35},
            "reg_state1": {"relationship": "NO", "value": 0.35},
            "country5": {"relationship": "NO", "value": 0.35},
            "country7": {"relationship": "NO", "value": 0.35},
            "Star46": {"relationship": "NO", "value": 0.35},
            "Star16": {"relationship": "NO", "value": 0.35},
            "make3": {"relationship": "NO", "value": 0.4},
            "car_name4": {"relationship": "NO", "value": 0.35},
            "fuel_type4": {"relationship": "NO", "value": 0.35},
            "fuel3": {"relationship": "NO", "value": 0.35},
            "flight1": {"relationship": "NO", "value": 0.4},
            "tail_number1": {"relationship": "NO", "value": 0.4}
        },
        "fuel_type4": {
            "fuel3": {"relationship": "YES", "value": 0.7},
            "flight1": {"relationship": "NO", "value": 0.35},
            "condition5": {"relationship": "NO", "value": 0.35},
            "tail_number1": {"relationship": "NO", "value": 0.35},
            "date_added7": {"relationship": "NO", "value": 0.35}
        },
        "fuel3": {
            "fuel_type4": {"relationship": "YES", "value": 0.7},
            "flight1": {"relationship": "NO", "value": 0.35},
            "condition5": {"relationship": "NO", "value": 0.35},
            "tail_number1": {"relationship": "NO", "value": 0.35},
            "date_added7": {"relationship": "NO", "value": 0.35}
        },
        "flight1": {
            "tail_number1": {"relationship": "YES", "value": 0.7}
        },
        "tail_number1": {
            "flight1": {"relationship": "YES", "value": 0.7}
        }
    }

    similar_and_not_similar_file(file_name, test_results, columns_to_test)

    with open(f"files/{file_name}similar_and_not.md", "w") as f:
        for function in test_results.keys():
            score = 0
            sim_score = 0
            not_score = 0
            count = 0
            for column in test_results[function].keys():
                if column[0] not in columns_to_test or column[1] not in columns_to_test:
                    continue
                test_res = test_results[function][column]
                if column[0] == column[1]:
                    if test_res == 1:
                        score += 1
                    else:
                        score -= 1
                        print("in score -1")
                    continue
                if column[0] not in values.keys() or column[1] not in values[column[0]].keys():
                    continue
                wanted = values[column[0]][column[1]]["value"]
                wanted_sim = True if values[column[0]][column[1]]["relationship"] == "YES" else False
                if wanted_sim and (wanted - 0.1 <= test_res or wanted + 0.2 >= test_res):
                    score += 1
                    sim_score += 1
                elif not wanted_sim and (wanted - 0.2 >= test_res or wanted + 0.1 <= test_res):
                    score += 1
                    not_score += 1
                else:
                    score -= 1
                    count += 1
            f.write(f"## Function: {function}\n\n"
                    f"  **SCORE** {score}\n\n"
                    f" \n similar score **{sim_score}**,"
                    f" \n not similar score **{not_score}**,"
                    f" \n max score **{count + sim_score + not_score}**,"
                    f" \n bad **{count}**\n\n")




