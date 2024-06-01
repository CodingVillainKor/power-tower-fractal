import torch
_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MAX_ITER = 500
ESCAPE_RADIUS = 1e+10

def compute_tetration_divergence_torch(n, x0, y0, eps=5e-3, max_iter=MAX_ITER, escape_radius=ESCAPE_RADIUS):
    nx, ny = n, int(n*(9/16))
    eps_y = eps * (9/16)
    x = torch.linspace(x0 - eps, x0 + eps, nx, dtype=torch.float64).to(_device)
    y = torch.linspace(y0 - eps_y, y0 + eps_y, ny, dtype=torch.float64).to(_device)
    c = x[:, None] + 1j * y[None, :]
    z = c
    divergence_map = torch.zeros_like(c, dtype=bool)
    for _ in range(max_iter):
        powered = c ** z
        z = powered
        divergence_map |= (z.abs() > escape_radius)
    
    numpy_map = divergence_map.cpu().detach().numpy().astype(int).T * 255
    return numpy_map