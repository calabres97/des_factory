#Practica 1 metodos de simulacion

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

def next_crash_time(mean=2.798378171,std=0.20142525174966558):
    '''Returns next crashing time from a normal distribution

    Default values for mean and standard deviation(std) are derived from E6.fallos.txt file
    '''
    return np.random.normal(mean,std)

def worker_performance(t,ini,final,T):
    '''Return the workers performance constant that varies lineally in time
    t: instant
    '''
    return ini+t*(final-ini)/T

def next_fix_time(t, initial_performance, final_performance, T):
    '''Return the fix time from an exponential distribution
    '''
    lam=worker_performance(t,initial_performance,final_performance,T)
    return np.random.exponential(1/lam)


def upload_times(vector,step):
    '''Return the vectors substracting the time step
    '''
    for i in range(len(vector)):
        vector[i]-=step
    return vector


def obtain_gaussian_parameters(filename):
    '''Return the mean and the standard deviation from a list of values in a file
    '''
    values=[]
    with open(filename) as filex:
        for line in filex:
            values+=[float(line.strip())] 

    mean=np.mean(values)
    std=np.std(values)
    return (mean,std)


def simulation(gmean, gstd, T=1000, n_active_machines=10, n_workers=3, n_reserve=4, 
                initial_performance=0.55, final_performance=1.65):

    working_machines=n_active_machines
    reserve_machines=n_reserve
    fixing_machines=0
    waiting_machines=0

    function_time=0
    f_times=[[],[]]
    crash_times=[]
    
    for _ in range(working_machines):
        crash_times+=[next_crash_time(gmean,gstd)]

    fix_times=[T]*n_workers
    all_working_time=0
    all_times=[[],[]]

    t=0
    step=0
    left=T
    verb=False
    while left>0 and t<=T:
        if verb:
            print('Left: ',left)
            print('Step: ',step)
            print('Machines: ',working_machines, reserve_machines, fixing_machines, waiting_machines)
            print('Crash times: ', crash_times)
            print('Fix times: ', fix_times)
            print('Function time: ', function_time)
            print('All workers fixing: ', all_working_time)
            input()
        
        mins=[T-t, min(fix_times), min(crash_times)]
        step=min(mins)
        action=mins.index(step)
            
        fix_times=upload_times(fix_times,step)
        crash_times=upload_times(crash_times,step)
        t+=step
        left-=step

        if working_machines==n_active_machines:
            function_time+=step
            f_times[0].append(t)
            f_times[1].append(function_time)
        if not (left) in fix_times:
            all_working_time+=step
            all_times[0].append(t)
            all_times[1].append(all_working_time)
                
        if action==0:
            break
        elif action==1:
            ifix=fix_times.index(0)
            if waiting_machines>0:
                waiting_machines-=1
                fix_times[ifix]=next_fix_time(t, initial_performance, final_performance, T)
            else:
                fixing_machines-=1
                fix_times[ifix]=left
                
            if working_machines==n_active_machines:
                reserve_machines+=1
            else:
                working_machines+=1
                icrash=crash_times.index(left)
                crash_times[icrash]=next_crash_time(gmean,gstd)
            
        elif action==2:
            icrash=crash_times.index(0)
            if reserve_machines>0:
                reserve_machines-=1
                crash_times[icrash]=next_crash_time(gmean,gstd)
            else:
                working_machines-=1
                crash_times[icrash]=left

            if fixing_machines<n_workers:
                fixing_machines+=1
                ifix=fix_times.index(left)
                fix_times[ifix]=next_fix_time(t, initial_performance, final_performance, T)
            else:
                waiting_machines+=1

    
    props_function = function_time/T
    props_allfixing = all_working_time/T

    return props_function, props_allfixing

    
if __name__ == "__main__":

    gmean,gstd=obtain_gaussian_parameters('E6.fallos.txt')

    mean_function = []
    mean_fixing = []

    props_function=[]
    props_allfixing=[]
    for rep in range(200):
        x, y = simulation(gmean, gstd)
        props_function.append(x)
        props_allfixing.append(y)

    mean_function.append(np.mean(props_function))
    mean_fixing.append(np.mean(props_allfixing))

    plt.hist(props_function, color='r', alpha=0.5, label='Functioning')
    plt.hist(props_allfixing, alpha=0.5, label='All fixing')
    plt.xticks(np.arange(0, 1, 0.1))
    plt.title('Times proportion histogram standard simulation')
    plt.xlabel('Time proportion')
    plt.ylabel('Number of simulations')
    plt.legend(loc='upper center')
    plt.show()

    props_function=[]
    props_allfixing=[]
    for rep in range(200):
        x, y = simulation(gmean, gstd, n_workers=4)
        props_function.append(x)
        props_allfixing.append(y)

    mean_function.append(np.mean(props_function))
    mean_fixing.append(np.mean(props_allfixing))

    plt.hist(props_function, color='r', alpha=0.5,label='Functioning',)
    plt.hist(props_allfixing, alpha=0.5, label='All fixing')
    plt.xticks(np.arange(0, 1, 0.1))
    plt.title('Times proportion histogram 4 workers')
    plt.xlabel('Time proportion')
    plt.ylabel('Number of simulations')
    plt.legend(loc='upper center')
    plt.show()

    props_function=[]
    props_allfixing=[]
    for rep in range(200):
        x, y = simulation(gmean, gstd, n_reserve=5)
        props_function.append(x)
        props_allfixing.append(y)

    mean_function.append(np.mean(props_function))
    mean_fixing.append(np.mean(props_allfixing))

    plt.hist(props_function, color='r', alpha=0.5, label='Functioning')
    plt.hist(props_allfixing, alpha=0.5, label='All fixing')
    plt.xticks(np.arange(0, 1, 0.1))
    plt.title('Times proportion histogram 5 reserve machines')
    plt.legend(loc='upper center')
    plt.show()

    for mean in mean_function:
        print("Percentage function: " + str(mean))

    print("--------------")

    for mean in mean_fixing:
        print("Percentage fixing: " + str(mean))