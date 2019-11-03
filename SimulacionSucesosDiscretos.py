#Practica 1 metodos de simulacion

import numpy as np
import matplotlib.pyplot as plt

def next_crash_time(mean=2.798378171, std=0.20142525174966558):
    '''Returns next crashing time from a normal distribution

    Default values for mean and standard deviation(std) are derived from E6.fallos.txt file
    '''
    return np.random.normal(mean,std)

def worker_performance(t, ini, final, T):
    '''Return the workers performance constant that varies lineally in time
    t: instant
    '''
    return ini + t * (final - ini) / T

def next_fix_time(t, initial_performance, final_performance, sim_time):
    '''Return the fix time from an exponential distribution
    '''
    lam=worker_performance(t, initial_performance, final_performance, sim_time)
    return np.random.exponential(1 / lam)
    
def upload_times(vector, step):
    '''Return the vectors substracting the time step
    '''
    for i in range(len(vector)):
        vector[i] -= step
    return vector

def obtain_gaussian_parameters(filename):
    '''Return the mean and the standard deviation from a list of values in a file
    '''
    values=[]
    with open(filename) as filex:
        for line in filex:
            values += [float(line.strip())] 

    mean=np.mean(values)
    std=np.std(values)
    return (mean, std)

def simulation(file, sim_time=1000, active_machines=10, workers=3, reserve=4, 
                initial_performance=0.55, final_performance=1.65, verbose=False):

    gmean, gstd = obtain_gaussian_parameters(file)

    #Intial values for the machines
    working_machines = active_machines
    reserve_machines = reserve
    fixing_machines = 0
    waiting_machines = 0

    #Crashing
    function_time = 0
    f_times = [[],[]]
    crash_times = []
    for i in range(working_machines):
        crash_times += [next_crash_time(gmean, gstd)]

    #Fixing
    #When a worker time is empty, it will be equal to T-t(left)
    fix_times = [sim_time] * workers
    all_working_time = 0
    all_times = [[],[]]

    t = 0
    step = 0
    left = sim_time

    props_function = []
    props_allfixing = []
    while left > 0 and t <= sim_time:
        if verbose:
            print('Left: ', left)
            print('Step: ', step)
            print('Machines: ', working_machines, reserve_machines, fixing_machines, waiting_machines)
            print('Crash times: ', crash_times)
            print('Fix times: ', fix_times)
            print('Function time: ', function_time)
            print('All workers fixing: ', all_working_time)
            input()
        
        mins = [sim_time - t, min(fix_times), min(crash_times)]
        step = min(mins)
        action = mins.index(step)
            
        fix_times = upload_times(fix_times,step)
        crash_times = upload_times(crash_times,step)
        t += step
        left -= step

        #Uploading stadistics
        if working_machines == active_machines:
            function_time += step
            f_times[0].append(t)
            f_times[1].append(function_time)
        if not (left) in fix_times:
            #If all workers are working
            all_working_time+=step
            all_times[0].append(t)
            all_times[1].append(all_working_time)
                
        if action == 0:
            #Time will be out before any other event
            break
        elif action == 1:
            #Next event is a fixed machine
            #print('Fixed machine')
            ifix = fix_times.index(0)
            if waiting_machines > 0:
                waiting_machines -= 1
                fix_times[ifix] = next_fix_time(t, initial_performance, final_performance, t)
            else:
                fixing_machines -= 1
                fix_times[ifix] = left
                
            if working_machines == active_machines:
                reserve_machines += 1
            else:
                working_machines += 1
                icrash = crash_times.index(left)
                crash_times[icrash] = next_crash_time(gmean,gstd)
            
        elif action == 2:
            #print('Crashed machine')
            #Next event is a crashed machine
            icrash = crash_times.index(0)
            if reserve_machines > 0:
                reserve_machines -= 1
                crash_times[icrash] = next_crash_time(gmean,gstd)
            else:
                working_machines -= 1
                crash_times[icrash] = left

            if fixing_machines < workers:
                fixing_machines += 1
                ifix = fix_times.index(left)
                fix_times[ifix] = next_fix_time(t, initial_performance, final_performance, t)
            else:
                waiting_machines += 1

        props_function += [function_time / sim_time]
        props_allfixing += [all_working_time / sim_time]

    return props_function, props_allfixing
'''
    plt.hist(props_function, color='r', alpha=0.5, label='Functioning')
    plt.hist(props_allfixing, alpha=0.5, label='All fixing')
    plt.title('Times proportion histogram')
    plt.legend(loc='upper center')

    plt.show()

    print('Proportion of functioning time: ', np.mean(props_function))
    print('Proportion of all fixing time: ', np.mean(props_allfixing))

    #Realmente aqui solo estamos mostrando la ultima de las repeticiones de la
    #simulacion, como es asincrono no se como hacer una media
    plt.plot(f_times[0], f_times[1], 'r-',label='Functioning')
    plt.plot(all_times[0], all_times[1], 'b-',label='Fixing')
    plt.title('Functioning and fixing times through simulation')
    plt.legend(loc='upper left')
    plt.show()

    return

'''

if __name__ == "__main__":

    props_function_hist = []
    props_allfixing_hist = []

    for rep in range(200):
        props_function, props_allfixing = simulation('E6.fallos.txt')
        props_function_hist += [props_function]
        props_allfixing_hist += props_allfixing

    plt.hist(props_function, color='r', alpha=0.5, label='Functioning')
    plt.hist(props_allfixing, alpha=0.5, label='All fixing')
    plt.title('Times proportion histogram')
    plt.legend(loc='upper center')

    plt.show()

    print('Proportion of functioning time: ', np.mean(props_function))
    print('Proportion of all fixing time: ', np.mean(props_allfixing))
'''
    #Realmente aqui solo estamos mostrando la ultima de las repeticiones de la
    #simulacion, como es asincrono no se como hacer una media
    plt.plot(f_times[0], f_times[1], 'r-',label='Functioning')
    plt.plot(all_times[0], all_times[1], 'b-',label='Fixing')
    plt.title('Functioning and fixing times through simulation')
    plt.legend(loc='upper left')
    plt.show()
'''