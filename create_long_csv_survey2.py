import pandas as pd
import json
import numpy as np


# nested json
inputFname = './data/qualitysurvey_data_20participants.csv'
outputFname = "./data/generated/aestheticRatings_v1.csv"


def get_model_emo(fn):
    fnn = fn.split(".")[0]
    # gpt3 filenames were not the same as the rest
    if fnn.startswith("gpt3"):
        elems = fnn.split("-")
        gmodel = "gpt3"
        emo = elems[-2].strip().split(" ")[-1]
        context = elems[-2].strip().split(" ")[5]
    else:
        elems = fnn.split("-")
        gmodel = elems[0]
        emo = elems[-2].split(" ")[-1]        
        context = elems[-2].split(" ")[1]
    return (gmodel,emo,context)


df = pd.read_csv(inputFname)

all_dfs = []
for testIndx in range(df.shape[0]):
    p_json = df['jspsych_data_all'][testIndx]
    ddict = json.loads(p_json)
    exp_trials = ddict['trials'][8:194]

    data_stimFilename = [x['stimulus'].split("/")[-1] for x in exp_trials]
    data_rt = [int(x['rt']) for x in exp_trials]
    n = len(data_rt)
    data_rating = [int(x['response'])+1 for x in exp_trials] # ONLY DIFFERENCE from survey 1 : change in rating scale
    data_trialIndex = [int(x['trial_index']) for x in exp_trials]
    data_timeElapsed = [f"{x['time_elapsed']/1000:.1f}" for x in exp_trials]
    data_age = [int(ddict['trials'][2]['response']['input_age'])] * n
    data_gender = [str(ddict['trials'][2]['response']['input_gender'])] * n
    data_pid = [df['PROLIFIC_PID'][testIndx]]*n
    
    df_p = pd.DataFrame(list(zip(data_pid, data_age, data_gender, data_trialIndex, data_stimFilename, data_rt, data_timeElapsed, data_rating)), columns=["participantID", "age", "gender", "trial_index", "stimulus_filename", "RT(ms)", "total_time_elapsed(s)", "rating"])
    all_dfs.append(df_p)


df_final = pd.concat(all_dfs)

model_emo = np.array([get_model_emo(x) for x in df_final['stimulus_filename']])
df_final['model'] = model_emo[:,0]
df_final['emotion'] = model_emo[:,1]
df_final['context'] = model_emo[:,2]
# remove the attention check trials
df_final = df_final[df_final['model']!='attentionCheck']
df_final.to_csv(outputFname, index=False)
