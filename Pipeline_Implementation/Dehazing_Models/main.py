# import os
# import torch
# import argparse
# from torch.backends import cudnn
# from models.FSNet import build_net
# from train import _train
# from eval import _eval

# def main(args):
#     # CUDNN
#     cudnn.benchmark = True

#     if not os.path.exists('results/'):
#         os.makedirs(args.model_save_dir)
#     if not os.path.exists('results/' + args.model_name + '/'):
#         os.makedirs('results/' + args.model_name + '/')
#     if not os.path.exists(args.model_save_dir):
#         os.makedirs(args.model_save_dir)
#     if not os.path.exists(args.result_dir):
#         os.makedirs(args.result_dir)

#     model = build_net()
#     print(model)

#     if torch.cuda.is_available():
#         model.cuda()
#     if args.mode == 'train':
#         _train(model, args)

#     elif args.mode == 'test':
#         _eval(model, args)


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()

#     # Directories
#     parser.add_argument('--model_name', default='FSNet',type=str)
#     parser.add_argument('--data_dir', type=str, default='')
#     parser.add_argument('--mode', default='test', choices=['train', 'test'], type=str)

#     # Train
#     parser.add_argument('--batch_size', type=int, default=8)
#     parser.add_argument('--learning_rate', type=float, default=1e-4)
#     parser.add_argument('--weight_decay', type=float, default=0)
#     parser.add_argument('--num_epoch', type=int, default=30)
#     parser.add_argument('--print_freq', type=int, default=100)
#     parser.add_argument('--num_worker', type=int, default=8)
#     parser.add_argument('--save_freq', type=int, default=1)
#     parser.add_argument('--valid_freq', type=int, default=1)
#     parser.add_argument('--resume', type=str, default='')


#     # Test
#     parser.add_argument('--test_model', type=str, default='')
#     parser.add_argument('--save_image', type=bool, default=False, choices=[True, False])

#     args = parser.parse_args()
#     args.model_save_dir = os.path.join('results/', 'FSNet', 'ots/')
#     args.result_dir = os.path.join('results/', args.model_name, 'test')
#     if not os.path.exists(args.model_save_dir):
#         os.makedirs(args.model_save_dir)
#     command = 'cp ' + 'models/layers.py ' + args.model_save_dir
#     os.system(command)
#     command = 'cp ' + 'models/FSNet.py ' + args.model_save_dir
#     os.system(command)
#     command = 'cp ' + 'train.py ' + args.model_save_dir
#     os.system(command)
#     command = 'cp ' + 'main.py ' + args.model_save_dir
#     os.system(command)
#     print(args)
#     main(args)



import os
import torch
from torch.backends import cudnn
from Pipeline_Implementation.Dehazing_Models.models.FSNet import build_net
from Pipeline_Implementation.Dehazing_Models.train import _train
from Pipeline_Implementation.Dehazing_Models.eval import _eval

class Arguments:
    def __init__(self):
        # Hardcoded arguments
        self.current_file_dir = os.path.dirname(__file__)
        self.model_name = 'FSNet'
        self.data_dir = f'{self.current_file_dir}/reside-outdoor'
        self.mode = 'test'
        # self.batch_size = 8
        # self.learning_rate = 1e-4
        # self.weight_decay = 0
        # self.num_epoch = 30
        # self.print_freq = 100
        # self.num_worker = 8
        # self.save_freq = 1
        # self.valid_freq = 1
        # self.resume = ''

        self.test_model = f'{self.current_file_dir}/ots.pkl'
        self.save_image = True

        # Paths
        self.model_save_dir = os.path.join(self.current_file_dir, 'results/', self.model_name, 'ots/')
        self.result_dir = os.path.join(self.current_file_dir, 'results/')

def main(args):
    # CUDNN
    cudnn.benchmark = True

    # Ensure directories exist
    # if not os.path.exists('results/'):
    #     os.makedirs(args.model_save_dir)
    # if not os.path.exists('results/' + args.model_name + '/'):
    #     os.makedirs('results/' + args.model_name + '/')
    # if not os.path.exists(args.model_save_dir):
    #     os.makedirs(args.model_save_dir)
    # if not os.path.exists(args.result_dir):
    #     os.makedirs(args.result_dir)

    # Build and print the model
    model = build_net()
    # print(model)

    if torch.cuda.is_available():
        model.cuda()

    if args.mode == 'train':
        _train(model, args)
    elif args.mode == 'test':
        _eval(model, args)

# if __name__ == '__main__':
#     # Initialize hardcoded arguments
#     args = Arguments()

#     # Copy important files to the model save directory
#     # os.makedirs(args.model_save_dir, exist_ok=True)
#     # os.system(f'cp models/layers.py {args.model_save_dir}')
#     # os.system(f'cp models/FSNet.py {args.model_save_dir}')
#     # os.system(f'cp train.py {args.model_save_dir}')
#     # os.system(f'cp main.py {args.model_save_dir}')

#     # Print arguments and run main function
#     # print(args.__dict__)
#     main(args)


