# End-functionalized Plots

This project implements the singly and doubly end-functionalized linear-polymer equations from equations (3), (4), (9), and (10) of the supplied Gorbunov paper.

## Files

- `end_functionalized_plots.ipynb`: explained calculation and plots.
- `end_functionalized_plots.py`: standalone Python version.
- `singly_doubly_functionalized_K_vs_g.png`: partition coefficient versus pore-size ratio.
- `singly_doubly_functionalized_K_vs_N.png`: partition coefficient versus chain length.
- `requirements.txt`: Python packages used by the project.

## Run

From the repository root:

```bash
cd "End-functionalized Plots"
python3 -m pip install -r requirements.txt
python3 end_functionalized_plots.py
```

Open the notebook in VS Code and run its cells from top to bottom.

## Model

For a singly end-functionalized chain:

$$K^{(1)}=K^{(0)}+q_a p_a$$

For a doubly end-functionalized chain:

$$K^{(2)}=K^{(0)}+q_a p_a+q_b p_b+q_aq_b p_{ab}$$

For end-functionalized linear chains, the paper gives:

$$p_a=U_1(\lambda,g)=\sum_{k\ odd}\frac{2\lambda}{\lambda+\lambda^2+\alpha_k^2}e^{-\alpha_k^2g^2}$$

$$p_{ab}=U_2(\lambda,g)=\sum_{k\ odd}\frac{2\alpha_k^2}{\lambda+\lambda^2+\alpha_k^2}e^{-\alpha_k^2g^2}$$

where $q_a$ and $q_b$ are reduced end-group interaction parameters and $g=R_G/R_P$ is the polymer-to-pore size ratio.
