#!/usr/bin/env python
#Practica 1 metodos de simulacion

import numpy as np
import matplotlib.pyplot as plt
from sys import argv

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

def next_fix_time(t):
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

def previous_events(event,interval):
    '''Return the ponderated average of the values of the times in the interval 
    event: [[times],[values]]
    interval: [t0,t1]
    '''
    av=0
    it=0
    while event[0][it]<interval[0]:
        it+=1

    prev_t=interval[0]
    value=event[1][it-1]
    while event[0][it]<=interval[1]:
        step=event[0][it]-prev_t
        av+=step*value
        
        value=event[1][it]
        prev_t=event[0][it]
        it+=1
        
    step=interval[1]-prev_t
    av+=step*value

    return av/(interval[1]-interval[0])
            

def plot_average(events, step, T):
    '''Plot the average of the values of a list of lists, with time step
    events: list of events: [[[times],[values]],[]]
    '''
    sol=[]
    interval=[0,0]
    for t in range(step,T,step):
        if t % 100 ==0:
            print('Processed {} / {}'.format(t,T))
        interval[0]=t-step
        interval[1]=t
        
        av=0
        for event in events:
            av+=previous_events(event,interval)
            
        sol.append(av/len(events))
        
    return sol
            
            
##########################################################
#Gaussian parameters
gmean,gstd=obtain_gaussian_parameters('E6.fallos.txt')

np.random.seed(44)

#Total time of the simulation
T=1000
if len(argv)>1:
    nreps=int(argv[1])
else:
    nreps=200

#Hyperparameters
alternative_implement=True

n_active_machines=10
if len(argv)>2:
    n_workers=int(argv[2])
else:
    n_workers=3
    
if len(argv)>3:
    n_reserve=int(argv[3])
else:
    n_reserve=5

if len(argv)>4:
    animated_plot= argv[4].lower()=='true'
else:
    animated_plot=False

print('Numero de repeticiones: {}\nNumero de trabajadores: {}\n\
Numero de maquinas de reserva: {}\nPlot animado: {} \n\
Implementación Alternativa: {}\n'\
      .format(nreps,n_workers,n_reserve,animated_plot,alternative_implement))

#Intial values for workers
initial_performance=0.55
final_performance=1.65

props_function=[]
props_allfixing=[]

events_fixing=[]
events_functioning=[]
for rep in range(nreps):
    if (rep+1)%10==0:
        print('Repetition {} / {}'.format(rep+1,nreps))
    #Intial values for the machines
    working_machines=n_active_machines
    reserve_machines=n_reserve
    fixing_machines=0
    waiting_machines=0

    #Crashing
    function_time=0
    f_times=[[0],[0]]
    crash_times=[]
    for i in range(working_machines):
        crash_times+=[next_crash_time(gmean,gstd)]

    #Fixing
    #When a worker time is empty, it will be equal to T-t(left)
    fix_times=[T]*n_workers
    all_working_time=0
    all_times=[[0],[0]]

    on_f=[[0],[1]]
    on_all=[[0],[0]]

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

        #Uploading stadistics
        
        if working_machines==n_active_machines:
            f_times[0].append(t)
            all_times[0].append(t)
            function_time+=step
            f_times[1].append(function_time/T)
            all_times[1].append(all_times[1][-1])
            on_f[0].append(t)
            on_f[1].append(1)
        else:
            on_f[0].append(t)
            on_f[1].append(0)
        
        if not (left) in fix_times:
            f_times[0].append(t)
            all_times[0].append(t)
            #If all workers are working
            all_working_time+=step
            all_times[1].append(all_working_time/T)
            f_times[1].append(f_times[1][-1])
            on_all[0].append(t)
            on_all[1].append(1)
        else:
            on_all[0].append(t)
            on_all[1].append(0)

        #Uploading machine states
##        print('\nWorking: {}\nReserve: {}\nFixing: {}\nWaiting: {}'\
##              .format(working_machines,reserve_machines,fixing_machines,waiting_machines))
##        print('\nAction: ',action)
        if action==0:
            #Time will be out before any other event
            break
        elif action==1:
            #Next event is a fixed machine
            #print('Fixed machine')
            ifix=fix_times.index(0)
            if waiting_machines>0:
                waiting_machines-=1
                fix_times[ifix]=next_fix_time(t)
            else:
                fixing_machines-=1
                fix_times[ifix]=left

            if alternative_implement:
                reserve_machines+=1  
                if working_machines + reserve_machines < n_active_machines:
                    pass
                else:
                    while True:
                        try:
                            icrash=crash_times.index(left)
                            crash_times[icrash]=next_crash_time(gmean,gstd)
                            working_machines+=1
                            reserve_machines-=1
                        except:
                            break
            else:
                if working_machines==n_active_machines:
                    reserve_machines+=1
                else:
                    working_machines+=1
                    icrash=crash_times.index(left)
                    crash_times[icrash]=next_crash_time(gmean,gstd)
            
        elif action==2:
            #print('Crashed machine')
            #Next event is a crashed machine
            icrash=crash_times.index(0)
            if alternative_implement:
                working_machines-=1
                if reserve_machines + working_machines >= n_active_machines:
                    reserve_machines-=1
                    working_machines+=1
                    crash_times[icrash]=next_crash_time(gmean,gstd)
                else:
                    crash_times[icrash]=left
            else:
                if reserve_machines>0:
                    reserve_machines-=1
                    crash_times[icrash]=next_crash_time(gmean,gstd)
                else:
                    working_machines-=1
                    crash_times[icrash]=left

            if fixing_machines<n_workers:
                fixing_machines+=1
                ifix=fix_times.index(left)
                fix_times[ifix]=next_fix_time(t)
            else:
                waiting_machines+=1

##        print('\nWorking: {}\nReserve: {}\nFixing: {}\nWaiting: {}'\
##              .format(working_machines,reserve_machines,fixing_machines,waiting_machines))
##        input()

        

    
    props_function+=[function_time/T]
    props_allfixing+=[all_working_time/T]

    events_fixing.append(on_all)
    events_functioning.append(on_f)

    states_plot=False
    if states_plot:
        #Plot de tiempos de on/off (all working si o no) para cada repeticion
        plt.plot(on_f[0],on_f[1],lw=0.2,label='Functioning')
        plt.plot(on_all[0],np.array(on_all[1])+1.5,'r',lw=0.2,label='Fixing')
        plt.title('Functioning and fixing times through simulation')
        plt.legend(loc='upper left')
        plt.ylim(-0.5, 3.5)
        plt.xlim(0, T)
        plt.draw()
        plt.pause(0.0001)
        plt.savefig('Simulation_states_{}.png'.format(rep))
        input()
        plt.clf()

average_plot=False
if average_plot: 
    #Plot media para todas las repeticiones de tiempos de on/off (all working si o no)
    sol_fix=plot_average(events_fixing,1,T)
    sol_fun=plot_average(events_functioning,1,T)
    plt.plot(sol_fun,lw=0.2,label='Funcionando')
    plt.plot(sol_fix,'r',lw=0.2,label='Todos reparando')
    plt.xlabel('Tiempo de simulación (horas)')
    plt.ylabel('Proporción de tiempo funcionando / todos reparando')
    plt.legend(loc='best')
    plt.title('Proporciones de funcionando y todos reparando\n(Promediado en {} repeticiones)'\
              .format(nreps))
    plt.draw()
    plt.pause(2)
    plt.savefig('proportion_all_amp.png')
    plt.clf()
    #input()


#Plot de tiempos acumulados de la ultima repeticion
#Animated plot
#animated_plot=False
generate_plot=False
if generate_plot:
    if animated_plot:
        for i in range(1,max(len(all_times[0]),len(f_times[0])),20):
            plt.clf()
            plt.plot(f_times[0][:i], f_times[1][:i], 'r-',label='Functioning')
            plt.ylim(0, 1)
            plt.xlim(0, T)
            plt.plot(all_times[0][:i], all_times[1][:i], 'b-',label='Fixing')
            plt.title('Functioning and fixing times through simulation')
            plt.legend(loc='upper left')
            plt.draw()
            plt.pause(0.0001)
    #Normal plot
    else:
        #Realmente aqui solo estamos mostrando la ultima de las repeticiones de la
        #simulacion, como es asincrono no se como hacer una media
        plt.plot(f_times[0], f_times[1], 'r-',label='Functioning')
        plt.plot(all_times[0], all_times[1], 'b-',label='Fixing')
        plt.title('Functioning and fixing times through simulation')
        plt.legend(loc='upper left')
        plt.ylim(0, 1)
        plt.xlim(0, T)
        plt.draw()
        plt.pause(0.0001)
        plt.savefig('cumulative_proportions.png')
    input()
    plt.clf()

#Histograma de todos reparando y funcionando para todas las repeticiones
histogram=True
if histogram:
    plt.hist(props_function,color='r',alpha=0.5,label='Funcionando')
    plt.hist(props_allfixing,alpha=0.5, label='Todos reparando')
    plt.title('Histograma de proporción de tiempo (en {} repeticiones)'.format(nreps))
    plt.xlabel('Porporción de tiempo')
    plt.ylabel('Número de repticiones')
    plt.legend(loc='upper left')
    plt.xlim(0, 1)

    print('Proporción de tiempo funcionando: ', np.mean(props_function))
    print('Proporción de tiempo funcionando (STD): ', np.std(props_function))
    
    print('Proporción de tiempo arreglando: ', np.mean(props_allfixing))
    print('Proporción de tiempo arreglando (STD): ', np.std(props_allfixing))

    plt.draw()
    plt.pause(2)
    plt.savefig('histogram_proportions_amp.png')
    #input()
    plt.clf()

plt.close()


