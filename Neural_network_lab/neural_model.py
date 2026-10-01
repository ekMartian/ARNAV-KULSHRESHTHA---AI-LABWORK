import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

def generate_xor_plot():
    fig, ax = plt.subplots(figsize=(5, 5))
    x_coords = [0, 0, 1, 1]
    y_coords = [0, 1, 0, 1]
    labels = [0, 1, 1, 0]
    colors = ['red' if l == 1 else 'blue' for l in labels]
    markers = ['x' if l == 1 else 'o' for l in labels]
    for i in range(4):
        ax.scatter(x_coords[i], y_coords[i], color=colors[i], marker=markers[i], s=100)
    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_title("XOR Problem")
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    plt.grid(True)
    plt.savefig('xor_problem_plot.png')
    plt.close()

def run_binary_xor():
    X = torch.tensor([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
    y = torch.tensor([[0.], [1.], [1.], [0.]])
    activations = [('Sigmoid', nn.Sigmoid()), ('Tanh', nn.Tanh()), ('ReLU', nn.ReLU())]
    plt.figure(figsize=(6, 4))
    results = {}
    for name, act in activations:
        torch.manual_seed(42)
        model = nn.Sequential(nn.Linear(2, 2), act, nn.Linear(2, 1))
        criterion = nn.BCEWithLogitsLoss()
        optimizer = optim.SGD(model.parameters(), lr=1.0)
        losses = []
        early_grad_norm = 0.0
        for epoch in range(2000):
            optimizer.zero_grad()
            logits = model(X)
            loss = criterion(logits, y)
            loss.backward()
            if epoch == 10:
                early_grad_norm = torch.norm(model[0].weight.grad).item()
            optimizer.step()
            if epoch % 50 == 0:
                losses.append(loss.item())
        plt.plot(range(0, 2000, 50), losses, label=name)
        logits = model(X)
        probs = torch.sigmoid(logits)
        preds = (probs > 0.5).float()
        final_loss = criterion(logits, y).item()
        results[name] = {
            'final_loss': final_loss,
            'correct': (preds == y).all().item(),
            'early_grad_norm': early_grad_norm
        }
    plt.title("Activation Loss Curves")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
    plt.grid(True)
    plt.savefig('activation_loss_curves.png')
    plt.close()
    torch.manual_seed(42)
    model = nn.Sequential(nn.Linear(2, 2), nn.Sigmoid(), nn.Linear(2, 1))
    for param in model.parameters():
        nn.init.zeros_(param)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.SGD(model.parameters(), lr=1.0)
    for epoch in range(5):
        optimizer.zero_grad()
        logits = model(X)
        loss = criterion(logits, y)
        loss.backward()
        optimizer.step()
    sym_weights = model[0].weight.detach().numpy().copy()
    results['Symmetry'] = sym_weights
    return results

def run_multiclass_xor():
    X = torch.tensor([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
    y = torch.tensor([0, 1, 1, 2])
    torch.manual_seed(42)
    model = nn.Sequential(
        nn.Linear(2, 2),
        nn.Sigmoid(),
        nn.Linear(2, 3)
    )
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=1.0)
    for epoch in range(2000):
        optimizer.zero_grad()
        logits = model(X)
        loss = criterion(logits, y)
        loss.backward()
        optimizer.step()
    logits = model(X)
    probs = torch.softmax(logits, dim=1)
    preds = torch.argmax(probs, dim=1)
    return {
        'probs': probs.detach().numpy(),
        'preds': preds.detach().numpy(),
        'weights_shape': list(model[2].weight.shape)
    }

if __name__ == '__main__':
    generate_xor_plot()
    bin_res = run_binary_xor()
    multi_res = run_multiclass_xor()
    print("--- Binary XOR Results ---")
    for act in ['Sigmoid', 'Tanh', 'ReLU']:
        print(f"{act}: Final Loss: {bin_res[act]['final_loss']:.4f}, All Correct: {bin_res[act]['correct']}, Early Grad Norm: {bin_res[act]['early_grad_norm']:.4f}")
    print("\n--- Symmetry Weights (Epoch 5) ---")
    print(bin_res['Symmetry'])
    print("\n--- Multiclass XOR Results ---")
    print(f"Predictions: {multi_res['preds']}")
    print(f"Probabilities (Example 0): {multi_res['probs'][0]}")
    print(f"Sum of probabilities (Example 0): {multi_res['probs'][0].sum():.4f}")
    print(f"Final Weight Matrix Shape: {multi_res['weights_shape']}")
