'''
Mode 0 is for using Plansformer fine-tuned model on 4 domains - bw, gr, hn, dl directly
for inference on a problem set without any continual training.
'''
#import pwd
from torch import cuda
device = 'cuda' if cuda.is_available() else 'cpu'

#imports
import torch
import torch.nn.functional as F
import re
import Planners.New_PlansformerS1.prompt_gen as pg

#imports
from transformers import RobertaTokenizer, T5ForConditionalGeneration

def solve(domain, problem, mode):
    #path to plansformer model files
    model_path = "Planners/New_PlansformerS1/mode"+ str(mode) +"_model_files"

    #using plansformer's tokenizer and model weights
    tokenizer = RobertaTokenizer.from_pretrained(model_path, local_files_only = True)
    model = T5ForConditionalGeneration.from_pretrained(model_path, local_files_only = True)
    model = model.to(device)
    #input problem/task
    instance_prompt = pg.get_prompt(domain,problem)

    #print(f"Instance prompt: {instance_prompt}")

    #tokenizing the input and passing it to the model
    input_ids = tokenizer.encode(instance_prompt, return_tensors='pt').to(device, dtype = torch.long)
    generated_ids = model.generate(
        input_ids, num_beams = 2, max_length=input_ids.shape[-1] + 2,
        repetition_penalty = 2.5, length_penalty = 1.0,
        early_stopping=False, do_sample = True, return_dict_in_generate=True, output_scores=True, return_legacy_cache=True)

    #obtaining the predicted plan from Plansformer for given input
    predicted_plan = [tokenizer.decode(g, skip_special_tokens=True) for g in generated_ids.sequences]
    gen_sequences = generated_ids.sequences[:1,1:]
    probs = torch.stack(generated_ids.scores, dim=1).softmax(-1)
    if probs.shape[0] > 1:
        probs = probs[:1]
    gen_probs = torch.gather(probs, 2, gen_sequences[:, :, None]).squeeze(-1)
    return torch.mean(gen_probs), predicted_plan