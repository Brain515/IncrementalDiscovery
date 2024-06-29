import time
import os
import csv
# import pandas as pd
# from pm4py.algo.discovery.alpha import algorithm as alpha_miner
# from pm4py.algo.discovery.alpha.variants import classic as ca
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.visualization.dfg import visualizer as dfg_visualization
from pm4py.objects.conversion.dfg import converter as dfg_mining
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
# from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.evaluation.precision import algorithm as precision_evaluator
from pm4py.algo.evaluation.replay_fitness import algorithm as replay_fitness_evaluator
# from pm4py.algo.discovery.heuristics.algorithm import CLASSIC
# import pm4py
import pm4py.algo.discovery.inductive.algorithm
import psutil
# from pm4py.algo.discovery.inductive.variants.im_d import dfg_based
# from pm4py.visualization.process_tree import visualizer as pt_visualizer

csv_file = r'C:\Users\lenovo\Desktop\output.csv'
data = [['New-CoSeLog-Algorithm', 'Time', 'Memory', 'Precision', 'Fitness', 'F-value']]

#----传统方法

def alpha_flow():
    def show_info():
        return psutil.virtual_memory().used >> 20
    start_mem = show_info()  # 开始内存
    start = time.time()  # 开始时间
    log_folder = "D:\\BPI-Month\\CoSeLog\\Adding_Logs_For_Traditional_Discovery"
    logs = []
    for log_file in os.listdir(log_folder):
        if log_file.endswith(".xes"):
            log_path = os.path.join(log_folder, log_file)
            log = xes_importer.apply(log_path)
            logs.append(log)
            dfg = dfg_discovery.apply(log)
            net, im, fm = pm4py.algo.discovery.alpha.algorithm.apply_dfg(dfg)
    gviz = pn_visualizer.apply(net, im, fm)
    pn_visualizer.view(gviz)
    end = time.time()  # 结束时间
    end_mem = show_info()  # 结束内存
    print("程序运行时间：%.2f秒" % (end - start))  # 27.41
    print(f'一共占用{end_mem - start_mem}MB')  # 467
    last_log = logs[-1]
    prec = precision_evaluator.apply(last_log, net, im, fm, variant=precision_evaluator.Variants.ETCONFORMANCE_TOKEN)
    fitness = replay_fitness_evaluator.apply(last_log, net, im, fm, variant=replay_fitness_evaluator.Variants.TOKEN_BASED)
    f_mea = (2 * fitness['average_trace_fitness'] * prec) / (fitness['average_trace_fitness'] + prec)
    print(prec)  # 0.099
    print(fitness)  # 0.189
    print(f_mea)  # 0.131
    data.append(['alpha', round(end - start, 2), end_mem - start_mem, round(prec, 2), round(fitness['average_trace_fitness'], 2),
                 round(f_mea, 2)])

def IM_flow():
    def show_info():
        return psutil.virtual_memory().used >> 20
    start_mem = show_info()  # 开始内存
    start = time.time()  # 开始时间
    log_folder = "D:\\BPI-Month\\CoSeLog\\Adding_Logs_For_Traditional_Discovery"
    logs = []
    for log_file in os.listdir(log_folder):
        if log_file.endswith(".xes"):
            log_path = os.path.join(log_folder, log_file)
            log = xes_importer.apply(log_path)
            logs.append(log)
            dfg = dfg_discovery.apply(log)
            net, im, fm = dfg_mining.apply(dfg)
    gviz = pn_visualizer.apply(net, im, fm)
    pn_visualizer.view(gviz)
    end = time.time()  # 结束时间
    end_mem = show_info()  # 结束内存
    print("程序运行时间：%.2f秒" % (end - start))  # 24.93
    print(f'一共占用{end_mem - start_mem}MB')  # 513
    last_log = logs[-1]
    prec = precision_evaluator.apply(last_log, net, im, fm, variant=precision_evaluator.Variants.ETCONFORMANCE_TOKEN)
    fitness = replay_fitness_evaluator.apply(last_log, net, im, fm, variant=replay_fitness_evaluator.Variants.TOKEN_BASED)
    f_mea = (2 * fitness['average_trace_fitness'] * prec) / (fitness['average_trace_fitness'] + prec)
    print(prec)  # 0.34
    print(fitness)  # 1
    print(f_mea)  # 0.56
    data.append(['IM', round(end - start, 2), end_mem - start_mem, round(prec, 2), round(fitness['average_trace_fitness'], 2), round(f_mea, 2)])

def HM_flow():
    def show_info():
        return psutil.virtual_memory().used >> 20
    start_mem = show_info()  # 开始内存
    start = time.time()  # 开始时间
    log_folder = "D:\\BPI-Month\\CoSeLog\\Adding_Logs_For_Traditional_Discovery"
    logs = []
    for log_file in os.listdir(log_folder):
        if log_file.endswith(".xes"):
            log_path = os.path.join(log_folder, log_file)
            log = xes_importer.apply(log_path)
            logs.append(log)
            dfg = dfg_discovery.apply(log)
            net, im, fm = heuristics_miner.apply_dfg(dfg, parameters={heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.99})
    gviz = pn_visualizer.apply(net, im, fm)
    pn_visualizer.view(gviz)
    end = time.time()  # 结束时间
    end_mem = show_info()  # 结束内存
    print("程序运行时间：%.2f秒" % (end - start))  # 24.93
    print(f'一共占用{end_mem - start_mem}MB')  # 513
    last_log = logs[-1]
    prec = precision_evaluator.apply(last_log, net, im, fm, variant=precision_evaluator.Variants.ETCONFORMANCE_TOKEN)
    fitness = replay_fitness_evaluator.apply(last_log, net, im, fm, variant=replay_fitness_evaluator.Variants.TOKEN_BASED)
    f_mea = (2 * fitness['average_trace_fitness'] * prec) / (fitness['average_trace_fitness'] + prec)
    print(prec)
    print(fitness)
    print(f_mea)
    data.append(['HM', round(end - start, 2), end_mem - start_mem, round(prec, 2), round(fitness['average_trace_fitness'], 2), round(f_mea, 2)])

def IMd_flow():
    def show_info():
        return psutil.virtual_memory().used >> 20
    start_mem = show_info()  # 开始内存
    start = time.time()  # 开始时间
    log_folder = "D:\\BPI-Month\\CoSeLog\\Adding_Logs_For_Traditional_Discovery"
    logs = []
    for log_file in os.listdir(log_folder):
        if log_file.endswith(".xes"):
            log_path = os.path.join(log_folder, log_file)
            log = xes_importer.apply(log_path)
            logs.append(log)
            dfg = dfg_discovery.apply(log)
            net, im, fm = pm4py.algo.discovery.inductive.variants.im_d.dfg_based.apply_dfg(dfg)
    gviz = pn_visualizer.apply(net, im, fm)
    pn_visualizer.view(gviz)
    end = time.time()  # 结束时间
    end_mem = show_info()  # 结束内存
    print("程序运行时间：%.2f秒" % (end - start))  # 24.93
    print(f'一共占用{end_mem - start_mem}MB')  # 513
    last_log = logs[-1]
    prec = precision_evaluator.apply(last_log, net, im, fm, variant=precision_evaluator.Variants.ETCONFORMANCE_TOKEN)
    fitness = replay_fitness_evaluator.apply(last_log, net, im, fm, variant=replay_fitness_evaluator.Variants.TOKEN_BASED)
    f_mea = (2 * fitness['average_trace_fitness'] * prec) / (fitness['average_trace_fitness'] + prec)
    print(prec)
    print(fitness)
    print(f_mea)
    data.append(['IMd', round(end - start, 2), end_mem - start_mem, round(prec, 2), round(fitness['average_trace_fitness'], 2), round(f_mea, 2)])


#----IPDF框架内容

def IPDF_alpha_flow():
    def show_info():
        return psutil.virtual_memory().used >> 20
    start_mem = show_info()  # 开始内存
    start = time.time()  # 开始时间
    log_folder = "D:\\BPI-Month\\CoSeLog"
    logs = []
    dfg1 = None
    for i, file_name in enumerate(os.listdir(log_folder)):
        if file_name.endswith(".xes"):
            log_path = os.path.join(log_folder, file_name)
            log = xes_importer.apply(log_path)
            logs.append(log)
            dfg = dfg_discovery.apply(log)
            if dfg1 is None:
                dfg1 = dfg
            else:
                dfg1.update(dfg)
            # 对于倒数第二个日志，记录当前的DFG，并可视化
            if i == len(os.listdir(log_folder)) - 2:
                gviz = dfg_visualization.apply(dfg1, variant=dfg_visualization.Variants.FREQUENCY)
                dfg_visualization.view(gviz)
    net, im, fm = pm4py.algo.discovery.alpha.algorithm.apply_dfg(dfg1)
    gviz = pn_visualizer.apply(net, im, fm)
    pn_visualizer.view(gviz)
    end = time.time()  # 结束时间
    end_mem = show_info()  # 结束内存
    print("程序运行时间：%.2f秒" % (end - start))  # 27.41
    print(f'一共占用{end_mem - start_mem}MB')  # 467
    log = xes_importer.apply(
        os.path.join("D:\BPI-Month\CoSeLog", "Adding_Logs_For_Traditional_Discovery", "14For10-1.xes"))
    prec = precision_evaluator.apply(log, net, im, fm, variant=precision_evaluator.Variants.ETCONFORMANCE_TOKEN)
    fitness = replay_fitness_evaluator.apply(log, net, im, fm, variant=replay_fitness_evaluator.Variants.TOKEN_BASED)
    f_mea = (2 * fitness['average_trace_fitness'] * prec) / (fitness['average_trace_fitness'] + prec)
    print(prec)  # 0.099
    print(fitness)  # 0.189
    print(f_mea)  # 0.131
    data.append(['IPDF_alpha', round(end - start, 2), end_mem - start_mem, round(prec, 2), round(fitness['average_trace_fitness'], 2),
                 round(f_mea, 2)])

def IPDF_IM_flow():
    def show_info():
        return psutil.virtual_memory().used >> 20
    start_mem = show_info()  # 开始内存
    start = time.time()  # 开始时间
    log_folder = "D:\\BPI-Month\\CoSeLog"
    logs = []
    dfg1 = None
    for i, file_name in enumerate(os.listdir(log_folder)):
        if file_name.endswith(".xes"):
            log_path = os.path.join(log_folder, file_name)
            log = xes_importer.apply(log_path)
            logs.append(log)
            dfg = dfg_discovery.apply(log)
            if dfg1 is None:
                dfg1 = dfg
            else:
                dfg1.update(dfg)
            # 对于倒数第二个日志，记录当前的DFG，并可视化
            if i == len(os.listdir(log_folder)) - 2:
                gviz = dfg_visualization.apply(dfg1, variant=dfg_visualization.Variants.FREQUENCY)
                dfg_visualization.view(gviz)
    net, im, fm = dfg_mining.apply(dfg1)
    gviz = pn_visualizer.apply(net, im, fm)
    pn_visualizer.view(gviz)
    end = time.time()  # 结束时间
    end_mem = show_info()  # 结束内存
    print("程序运行时间：%.2f秒" % (end - start))  # 27.41
    print(f'一共占用{end_mem - start_mem}MB')  # 467
    log = xes_importer.apply(
        os.path.join("D:\BPI-Month\CoSeLog", "Adding_Logs_For_Traditional_Discovery", "14For10-1.xes"))
    prec = precision_evaluator.apply(log, net, im, fm, variant=precision_evaluator.Variants.ETCONFORMANCE_TOKEN)
    fitness = replay_fitness_evaluator.apply(log, net, im, fm, variant=replay_fitness_evaluator.Variants.TOKEN_BASED)
    f_mea = (2 * fitness['average_trace_fitness'] * prec) / (fitness['average_trace_fitness'] + prec)
    print(prec)  # 0.099
    print(fitness)  # 0.189
    print(f_mea)  # 0.131
    data.append(['IPDF_IM', round(end - start, 2), end_mem - start_mem, round(prec, 2), round(fitness['average_trace_fitness'], 2),
                 round(f_mea, 2)])

def IPDF_HM_flow():
    def show_info():
        return psutil.virtual_memory().used >> 20
    start_mem = show_info()  # 开始内存
    start = time.time()  # 开始时间
    log_folder = "D:\\BPI-Month\\CoSeLog"
    logs = []
    dfg1 = None
    for i, file_name in enumerate(os.listdir(log_folder)):
        if file_name.endswith(".xes"):
            log_path = os.path.join(log_folder, file_name)
            log = xes_importer.apply(log_path)
            logs.append(log)
            dfg = dfg_discovery.apply(log)
            if dfg1 is None:
                dfg1 = dfg
            else:
                dfg1.update(dfg)
            # 对于倒数第二个日志，记录当前的DFG，并可视化
            if i == len(os.listdir(log_folder)) - 2:
                gviz = dfg_visualization.apply(dfg1, variant=dfg_visualization.Variants.FREQUENCY)
                dfg_visualization.view(gviz)
    net, im, fm = heuristics_miner.apply_dfg(dfg1, parameters={heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.99})
    gviz = pn_visualizer.apply(net, im, fm)
    pn_visualizer.view(gviz)
    end = time.time()  # 结束时间
    end_mem = show_info()  # 结束内存
    print("程序运行时间：%.2f秒" % (end - start))  # 27.41
    print(f'一共占用{end_mem - start_mem}MB')  # 467
    log = xes_importer.apply(
        os.path.join("D:\BPI-Month\CoSeLog", "Adding_Logs_For_Traditional_Discovery", "14For10-1.xes"))
    prec = precision_evaluator.apply(log, net, im, fm, variant=precision_evaluator.Variants.ETCONFORMANCE_TOKEN)
    fitness = replay_fitness_evaluator.apply(log, net, im, fm, variant=replay_fitness_evaluator.Variants.TOKEN_BASED)
    f_mea = (2 * fitness['average_trace_fitness'] * prec) / (fitness['average_trace_fitness'] + prec)
    print(prec)  # 0.099
    print(fitness)  # 0.189
    print(f_mea)  # 0.131
    data.append(['IPDF_HM', round(end - start, 2), end_mem - start_mem, round(prec, 2), round(fitness['average_trace_fitness'], 2),
                 round(f_mea, 2)])

def IPDF_IMd_flow():
    def show_info():
        return psutil.virtual_memory().used >> 20
    start_mem = show_info()  # 开始内存
    start = time.time()  # 开始时间
    log_folder = "D:\\BPI-Month\\CoSeLog"
    logs = []
    dfg1 = None
    for i, file_name in enumerate(os.listdir(log_folder)):
        if file_name.endswith(".xes"):
            log_path = os.path.join(log_folder, file_name)
            log = xes_importer.apply(log_path)
            logs.append(log)
            dfg = dfg_discovery.apply(log)
            if dfg1 is None:
                dfg1 = dfg
            else:
                dfg1.update(dfg)
            # 对于倒数第二个日志，记录当前的DFG，并可视化
            if i == len(os.listdir(log_folder)) - 2:
                gviz = dfg_visualization.apply(dfg1, variant=dfg_visualization.Variants.FREQUENCY)
                dfg_visualization.view(gviz)
    net, im, fm = pm4py.algo.discovery.inductive.variants.im_d.dfg_based.apply_dfg(dfg1)
    gviz = pn_visualizer.apply(net, im, fm)
    pn_visualizer.view(gviz)
    end = time.time()  # 结束时间
    end_mem = show_info()  # 结束内存
    print("程序运行时间：%.2f秒" % (end - start))  # 27.41
    print(f'一共占用{end_mem - start_mem}MB')  # 467
    log = xes_importer.apply(
        os.path.join("D:\BPI-Month\CoSeLog", "Adding_Logs_For_Traditional_Discovery", "14For10-1.xes"))
    prec = precision_evaluator.apply(log, net, im, fm, variant=precision_evaluator.Variants.ETCONFORMANCE_TOKEN)
    fitness = replay_fitness_evaluator.apply(log, net, im, fm, variant=replay_fitness_evaluator.Variants.TOKEN_BASED)
    f_mea = (2 * fitness['average_trace_fitness'] * prec) / (fitness['average_trace_fitness'] + prec)
    print(prec)  # 0.099
    print(fitness)  # 0.189
    print(f_mea)  # 0.131
    data.append(['IPDF_IMd', round(end - start, 2), end_mem - start_mem, round(prec, 2), round(fitness['average_trace_fitness'], 2),
                 round(f_mea, 2)])
def main():
    #----传统方法
    alpha_flow()
    time.sleep(60)
    IM_flow()
    time.sleep(80)
    HM_flow()
    time.sleep(80)
    IMd_flow()
    #----IPDF框架
    IPDF_alpha_flow()
    time.sleep(60)
    IPDF_IM_flow()
    time.sleep(60)
    IPDF_HM_flow()
    time.sleep(80)
    IPDF_IMd_flow()
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

if __name__ == "__main__":
    main()
