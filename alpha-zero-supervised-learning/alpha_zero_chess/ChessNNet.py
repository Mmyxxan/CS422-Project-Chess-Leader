import os
import torch
import torch.optim as optim
import numpy as np
from tqdm import tqdm
from .NNet import NNet
from .utils import AverageMeter

class ChessNNet:
    def __init__(self, args):
        self.args = args
        self.nnet = NNet()

        model_folder = self.args.get('best_model_folder')
        model_filename = self.args.get('best_model_filename')
        if model_folder and model_filename:
            self.load_checkpoint(model_folder, model_filename)
        
        if self.args['cuda']:
            self.nnet.cuda()
        self.optimizer = optim.Adam(self.nnet.parameters(), lr=self.args.get("lr", 0.0001))

    def train(self, train_loader, val_loader=None):
        best_val_loss = float('inf')

        for epoch in range(self.args['epochs']):
            print(f"\nEpoch {epoch + 1}/{self.args['epochs']}")
            self.nnet.train()

            pi_losses = AverageMeter()
            v_losses = AverageMeter()
            t = tqdm(train_loader, desc="Training", leave=False)

            for batch in t:
                boards, policy_targets, value_targets = batch
                boards = boards.float()
                policy_targets = policy_targets.long()
                value_targets = value_targets.float()

                if self.args['cuda']:
                    boards = boards.cuda()
                    policy_targets = policy_targets.cuda()
                    value_targets = value_targets.cuda()

                out_pi, out_v = self.nnet(boards)

                l_pi = self.nnet.cross_entropy_loss(out_pi, policy_targets)
                l_v = self.nnet.mse_loss(out_v.squeeze(), value_targets)

                loss = l_pi + l_v

                pi_losses.update(l_pi.item(), boards.size(0))
                v_losses.update(l_v.item(), boards.size(0))

                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                t.set_postfix(loss_pi=pi_losses.avg, loss_v=v_losses.avg)

            # Save checkpoint after epoch
            checkpoint_name = f"checkpoint_epoch_{epoch + 1}.pth"
            self.save_checkpoint(self.args['folder'], checkpoint_name)

            # Evaluate on validation set if provided
            if val_loader:
                val_loss = self.evaluate(val_loader)
                print(f"Validation loss: {val_loss:.4f}")
                if val_loss < best_val_loss:
                    best_val_loss = val_loss
                    self.save_checkpoint(self.args['folder'], "best_model.pth")
                    print("✅ Saved new best model.")

    def evaluate(self, val_loader):
        self.nnet.eval()
        total_loss = 0
        total_batches = 0

        with torch.no_grad():
            for batch in val_loader:
                boards, policy_targets, value_targets = batch
                boards = boards.float()
                policy_targets = policy_targets.long()
                value_targets = value_targets.float()

                if self.args['cuda']:
                    boards = boards.cuda()
                    policy_targets = policy_targets.cuda()
                    value_targets = value_targets.cuda()

                out_pi, out_v = self.nnet(boards)

                l_pi = self.nnet.cross_entropy_loss(out_pi, policy_targets)
                l_v = self.nnet.mse_loss(out_v.squeeze(), value_targets)

                total_loss += (l_pi + l_v).item()
                total_batches += 1

        return total_loss / total_batches

    def predict(self, board_tensor, policy_mask=None):
        """
        Predict policy and value for a single board with optional legal move mask.

        Args:
            board_tensor (Tensor): shape (16, 8, 8)
            policy_mask (Tensor or None): shape (4672,) or (73, 8, 8)

        Returns:
            policy_logits (np.array): masked softmax policy
            value (float): predicted board value
        """
        self.nnet.eval()

        x = board_tensor.unsqueeze(0).float()
        if self.args['cuda']:
            x = x.cuda()

        with torch.no_grad():
            policy_logits, value = self.nnet(x)  # raw logits

            if policy_mask is not None:
                policy_logits = policy_logits.view(policy_logits.shape[0], -1)
                policy_mask = torch.tensor(policy_mask, dtype=torch.float32)
                policy_mask = policy_mask.view(1, -1)
                policy_exp = torch.exp(policy_logits)
                policy_exp *= policy_mask
                policy_sum = torch.sum(policy_exp, dim=1, keepdim=True)
                policy_softmax = policy_exp / (policy_sum + 1e-8)  # avoid div by 0
                # policy_softmax = policy_exp / policy_sum
                return policy_softmax.squeeze(0).cpu().numpy(), value.item()
            else:
                return torch.softmax(policy_logits, dim=1).squeeze(0).cpu().numpy(), value.item()

    def save_checkpoint(self, folder, filename):
        filepath = os.path.join(folder, filename)
        os.makedirs(folder, exist_ok=True)
        torch.save({'state_dict': self.nnet.state_dict()}, filepath)
        print(f"✅ Model saved to {filepath}")

    def load_checkpoint(self, folder, filename):
        filepath = os.path.join(folder, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"No model found at {filepath}")
        checkpoint = torch.load(filepath, map_location='cuda' if self.args['cuda'] else 'cpu')
        self.nnet.load_state_dict(checkpoint['state_dict'])
        # self.nnet.load_state_dict(checkpoint)
        print(f"✅ Model loaded from {filepath}")
