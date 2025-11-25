import pandas as pd
import numpy as np
import torch
from torch_geometric.data import Data, Dataset, DataLoader
from torch_geometric.nn import GraphConv, global_mean_pool
from torch.nn import Linear, Module, MSELoss
from torch.optim import AdamW
from sklearn.model_selection import KFold
import os
from sklearn.metrics import mean_squared_log_error


# Load data
train_df = pd.read_csv("./data/train.csv")
test_df = pd.read_csv("./data/test.csv")


# Function to load geometry data
def load_geometry(id, folder="./data/train/"):
    id = int(id)  # Ensure id is an integer
    path = os.path.join(folder, str(id), "geometry.xyz")
    if not os.path.exists(path):  # Check if file exists
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, "r") as f:
        lines = f.readlines()
    # Skip lines that start with '#'
    lines = [line for line in lines if not line.strip().startswith("#")]
    num_atoms = int(lines[0].strip())
    atoms = lines[2 : num_atoms + 2]
    positions = []
    atom_types = []
    for atom in atoms:
        parts = atom.split()
        atom_types.append(parts[0])
        positions.append([float(x) for x in parts[1:]])
    return np.array(positions), atom_types


# Create a PyTorch Geometric dataset
class MaterialDataset(Dataset):
    def __init__(self, df, folder):
        self.df = df
        self.folder = folder
        super(MaterialDataset, self).__init__()

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        id = self.df.iloc[idx]["id"]
        try:
            positions, atom_types = load_geometry(id, self.folder)
        except (FileNotFoundError, ValueError) as e:
            print(e)
            return None  # Return None if file not found or parsing error
        atom_type_map = {"Al": 0, "Ga": 1, "In": 2, "O": 3}
        x = torch.tensor(
            [atom_type_map.get(atom, 3) for atom in atom_types], dtype=torch.long
        )
        pos = torch.tensor(positions, dtype=torch.float)
        dist = torch.cdist(pos, pos)
        edge_index = torch.nonzero(dist < 2.0, as_tuple=False).T
        edge_attr = dist[edge_index[0], edge_index[1]]
        if "formation_energy_ev_natom" in self.df.columns:
            y = torch.tensor(
                [
                    self.df.iloc[idx]["formation_energy_ev_natom"],
                    self.df.iloc[idx]["bandgap_energy_ev"],
                ],
                dtype=torch.float,
            )
        else:
            y = None
        data = Data(x=x, edge_index=edge_index, edge_attr=edge_attr, pos=pos, y=y)
        return data


train_dataset = MaterialDataset(train_df, "./data/train/")
test_dataset = MaterialDataset(test_df, "./data/test/")

# Filter out None values from dataset
train_dataset = [data for data in train_dataset if data is not None]
test_dataset = [data for data in test_dataset if data is not None]


# Model
class GNN(Module):
    def __init__(self):
        super(GNN, self).__init__()
        self.conv1 = GraphConv(4, 128)
        self.conv2 = GraphConv(128, 128)
        self.lin = Linear(128, 2)

    def forward(self, data):
        x, edge_index, edge_attr = data.x, data.edge_index, data.edge_attr
        x = torch.nn.functional.relu(self.conv1(x, edge_index))
        x = torch.nn.functional.relu(self.conv2(x, edge_index))
        x = global_mean_pool(
            x, torch.zeros(x.size(0), dtype=torch.long, device=x.device)
        )
        x = self.lin(x)
        return x


# Training and evaluation
def train(model, loader, optimizer, criterion):
    model.train()
    total_loss = 0
    for data in loader:
        data = data.to("cuda")
        optimizer.zero_grad()
        out = model(data)
        loss = criterion(out, data.y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * data.num_graphs
    return total_loss / len(loader_loader.dataset)


def evaluate(model, loader, criterion):
    model.eval()
    total_loss = 0
    with torch.no_grad():
        for data in loader:
            data = data.to("cuda")
            out = model(data)
            loss = criterion(out, data.y)
            total_loss += loss.item() * data.num_graphs
    return total_loss / len(loader.dataset)


kf = KFold(n_splits=5, shuffle=True)
rmsles = []

for fold, (train_idx, val_idx) in enumerate(kf.split(train_dataset)):
    train_loader = DataLoader(
        [train_dataset[i] for i in train_idx], batch_size=32, shuffle=True
    )
    val_loader = DataLoader([train_dataset[i] for i in val_idx], batch_size=32)
    model = GNN().to("cuda")
    optimizer = AdamW(model.parameters(), lr=0.001)
    criterion = MSELoss()
    for epoch in range(100):
        train(model, train_loader, optimizer, criterion)
        val_loss = evaluate(model, val_loader, criterion)
    rmsle = np.sqrt(
        mean_squared_log_error(
            np.exp(val_loader.dataset.y.cpu().numpy()),
            np.exp(model(val_loader.dataset.to("cuda")).detach().cpu().numpy()),
        )
    )
    rmsles.append(rmsle)
    print(f"Fold {fold+1}, RMSLE: {rmsle}")

print(f"Average RMSLE: {np.mean(rmsles)}")

# Make predictions on test set
test_loader = DataLoader(test_dataset, batch_size=32)
model.eval()
predictions = []
with torch.no_grad():
    for data in test_loader:
        data = data.to("cuda")
        out = model(data)
        predictions.extend(out.cpu().numpy())

submission_df = pd.DataFrame(
    predictions, columns=["formation_energy_ev_natom", "bandgap_energy_ev"]
)
submission_df["id"] = test_df["id"]
submission_df = submission_df[["id", "formation_energy_ev_natom", "bandgap_energy_ev"]]
submission_df.to_csv("./submission.csv", index=False)
