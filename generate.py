from training import TrainModel
import argparse
parser = argparse.ArgumentParser(description='generate model')
parser.add_argument('--length',type=int)
parser.add_argument('--model',type=str)
parser.add_argument('--prefix',type=str)
args = parser.parse_args()
length = args.length
model = args.model
prefix = args.prefix
generate_model = TrainModel()
result = generate_model.generator(length, prefix, model)
print(result)
