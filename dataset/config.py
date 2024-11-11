jobs_config = {
    "num_jobs": 1000,
    "max_deadline": 2000,
    "max_task_per_depth": 2,
    "max_depth": 5,
    "task": {
        # input_size ,output_size ,computational_load in MB --> * 10^6
        "input_size": [1, 1001],
        "output_size": [1, 1001],
        "computational_load": [1, 1001],
        "safe_measurement": [0.5, 0.5],
        "task_kinds": [1, 2, 3, 4]
    },
    "max_num_parents_dag": 2,
    "min_num_nodes_dag": 4,
    "max_num_nodes_dag": 16
}

devices_config = {
    "iot": {
        "num_devices": 100,
        "num_cores": [4, 8, 16],
        "voltage_frequencies": [
            (10e6, 1.8),
            (20e6, 2.3),
            (40e6, 2.7),
            (80e6, 4.0),
            (160e6, 5.0),
        ],
        "isl": (0.1, 0.2),
        # capacitance in nano-Farad --> * 1e-9
        "capacitance": (0.2, 0.3),
        # powerIdle in micro-Watt --> * 1e-6
        "powerIdle": [800, 900, 1000],
        # battery_capacity in Watt-second
        "battery_capacity": (36, 41),
        "safe": (0.25, 0.75),
        "num_acceptable_task": [3, 4],
    },
    "mec": {
        "num_devices": 50,
        "num_cores": [16, 32, 64],
        "voltage_frequencies": [
            (600 * 1e6, 0.8),
            (750 * 1e6, 0.825),
            (1000 * 1e6, 1.0),
            (1500 * 1e6, 1.2),
        ],
        "isl": -1,
        # capacitance in nano-Farad --> * 1e-9
        "capacitance": (1.5, 2),
        # powerIdle in micro-Watt --> * 1e-6
        "powerIdle": [550000, 650000, 750000],
        "battery_capacity": -1,
        "safe": (0.5, 0.5),
        "num_acceptable_task": [3, 4],

    },
    "cloud": {
        "num_devices": 1,
        "num_cores": 128,
        "voltage_frequencies": ((2.8e9, 13.85), (3.9e9, 24.28)),
        "isl": -1,
        "capacitance": (3, 5),
        "powerIdle": [0],
        "battery_capacity": -1,
        "safe": (1, 0),
        "num_acceptable_task": [3, 4],  
    },
}

learning_config = {
    "num_epoch": 100000,
    ###### TREE #######
    "tree": "ddt",  # ddt

    #    ddt :  ddt 
    #    soft-ddt :  soft tree
    #    clustree : clustree 

    "tree_max_depth": 3,

    ###### REWARD,ALPHA,BETA #######
    "rewardSetup": 5,

    #   1 : -1 * (alpha * e + beta * t)
    #   2 : 1 / (alpha * e + beta * t)
    #   3 : -np.exp(alpha * e) - np.exp(beta * t)
    #   4 : -np.exp(alpha * e + beta * t)
    #   5 : np.exp(-1 * (alpha * e + beta * t))
    #   6 : -np.log(alpha * e + beta * t)
    #   7 : -((alpha * e + beta * t) ** 2)

    "alpha": 1,  # energy coefficient in the reward
    "beta": 1,  # time coefficient in the reward

    ###### PUNISH #######
    "increasing_punish": False,
    "init_punish": -10,
    "punish_epsilon": -0.001,

    ###### EXPLORE #######
    "should_explore": False,
    "explore_epsilon": 1e-5,

    "drain_battery": True,

    ###### INPUT & OUTPUT #######
    "onehot_kind": True,  # one-hotting the task kind
    "regularize_input": True,  # regularize the task/device features to feed the tree
    "regularize_output": False,  # regularize t,e for the reward
    'pe_num_features': 2,

    ###### ALGORITHM #######

    "learning_algorithm": "ppo",
    #   policy-grad
    #   a2c
    #   ppo

    "ppo_epsilon": 0.8,

    "critic_hidden_layer_num": 1,
    "critic_hidden_layer_dim": 256,

    "discount_factor": 0.0,  # 0: reward , 0.99:return

    "scalability": True,
    "add_device_iterations": 0.0001,
    "remove_device_iterations": 0.0001,

    "utilization": True,
    "alpha_diversity": 1,
    "alpha_gin": 1,
    "max_lambda": 10,

    "transmission_calc_type": 1,
    #   0: predecessor
    #   1: tems

    ###### PATHS #######
    "result_summery_path": './results/summery.csv',
    "result_plot_path": './results/result.png',
    "checkpoint_file_path": "./results/checkpoints/model.pth"
}

# generate random Processing element attributes based on the bounds and ranges defined in the config

#   frequency in KHZ
#   voltage in Volt
#   capacitance in nano-Farad
#   powerIdle in Watt
#   ISL in percentage
#   battery capacity in W*micro-second : 36000 Ws - Equivalent to 36000*10^3 W * millisecond, 10Wh or