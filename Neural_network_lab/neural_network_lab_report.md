# Laboratory – Neural Models: Learning, Depth, Activations, and Output Layers

## Task 1: Problem Specification & Linear Separability

**1. Input, Output and Examples**
* **Input space $\mathcal{X}$**: $\{0, 1\}^2$
* **Output space $\mathcal{Y}$**: $\{0, 1\}$
* **Examples**: $((0,0), 0)$, $((0,1), 1)$, $((1,0), 1)$, $((1,1), 0)$

**2. Sketch of XOR points**
(Refer to the generated `xor_problem_plot.png` for a visualization of the input points colored by class).

**3. Linear Separability Explanation**
A single straight decision boundary cannot separate the two classes because points belonging to the same class lie on opposite diagonals (e.g., $(0,0)$ and $(1,1)$ vs. $(1,0)$ and $(0,1)$). No single line can isolate the two blue points from the two red points.

**4. Prediction for linear model**
If we train a single affine transformation followed by a sigmoid output, the network will fail to converge to an optimal solution. It will likely predict a probability near 0.5 for all inputs, as it cannot learn the non-linear boundary required for XOR.

## Task 2: Model Design and Validation Criteria

**1. Why is the hidden nonlinearity scientifically necessary here?**
Without a non-linear activation in the hidden layer, the entire network (two linear layers) collapses into a single affine transformation. A linear transformation cannot represent XOR logic.

**2. Why is sigmoid plus binary cross-entropy a sensible pairing?**
Sigmoid naturally scales the logit output into a probability space between 0 and 1, perfectly matching our binary $\{0,1\}$ target. Binary cross-entropy heavily penalizes confident but incorrect predictions, providing a robust gradient for updating the model weights.

**3. Validation Criteria**
Successful learning requires:
1. Final loss converging to a value very close to zero.
2. All four thresholded predictions matching the labeled dataset exactly.
3. The gradient at early steps being non-zero to show that a learning signal is actively propagating.

## Task 4: Execute, Test, and Diagnose

**Part A & D: Activation Experiment & Results**

| Hidden activation | Final loss | 4/4 correct? | Early $\|\nabla_W(1) L\|_2$ |
| :--- | :--- | :--- | :--- |
| Sigmoid | 0.0153 | Yes | 0.0044 |
| Tanh | 0.0017 | Yes | 0.0168 |
| ReLU | 0.3467 | No | 0.0706 |

*(Refer to `activation_loss_curves.png` for the training progression).*

**Part B: Backpropagation Check**
The tensor `parameter.grad` in PyTorch represents the partial derivative of the loss $L$ with respect to the specific weight matrix, $\frac{\partial L}{\partial W^{(1)}}$. Because we pass the full batch of four examples at once and take the mean loss, the gradient is the average of the individual gradients for each of the four examples.

**Part C: Symmetry Experiment**
When all weights were initialized to zero, the hidden layer gradient at Epoch 5 was:
```
[[0. 0.]
 [0. 0.]]
```
Because the weights are exactly identical (zero), both hidden units compute the exact same output for any given input, and thus receive identical error gradients during backpropagation. The symmetry is never broken, effectively reducing the hidden layer to a single unit.

## Task 5: Multiclass Extension

**Output Design & Validations:**
1. **Shape of final weight matrix**: `[3, 2]` (3 outputs, 2 inputs from the hidden layer).
2. **Number of logits per example**: 3.
3. **Why softmax probabilities sum to one**: Softmax exponentiates the logits (making them positive) and divides each by the sum of all exponentiated logits, producing a valid probability distribution.
4. **Why stable implementations subtract max logit**: Subtracting the maximum logit before exponentiating prevents numerical overflow (e.g., `exp(1000)` = infinity), while preserving the relative probabilities since $e^{x-c}/ \sum e^{y-c}$ factors out $e^{-c}$.

**Results:**
* **Predictions**: `[0, 1, 1, 2]` (Correctly matches classes)
* **Prob sum for first example**: 1.0000

## Reflection Questions

1. **Depth vs Nonlinearity**: Depth alone is insufficient to solve XOR without non-linearity. A deep affine network collapses to a linear classifier, while a non-linear activation transforms the 2D plane so that a linear output layer can easily separate the XOR classes.
2. **Backpropagation signal**: The early gradient norm was non-zero and the final loss converged. If the gradient had just been randomly non-zero without direction, the final predictions would not have been 4/4 correct. 
3. **Identical weight init**: Identical weights mean the hidden units always perform the exact same computation and receive the exact same derivative updates. They are permanently locked together.
4. **Hidden activation and gradients**: Sigmoid suffered from a relatively small gradient (0.0044) due to saturation mechanics. Tanh had a stronger gradient (0.0168) because it maps between -1 and 1 and is steeper at the origin. ReLU can suffer from "dead" units if inputs push it negative early on, turning the gradient completely to zero.
5. **Output layer and loss**: The output layer determines the mathematical codomain of the network's prediction (e.g. $[0,1]$ for binary, real numbers for regression). The loss function defines the penalty for diverging from the target in that specific space. 
6. **LLM as assistant**: The LLM significantly improved productivity by rapidly generating boilerplate PyTorch setup (initialization, training loop, plotting). However, human verification was essential to ensure the exact architecture (2-2-1) and loss combination were applied as mathematically requested by the lab.
7. **Scale-up testing**: Tracking loss convergence, verifying final predicted outputs against a test set, and logging gradient norms are inexpensive and essential at scale. Exhaustive finite-difference gradient checking, symmetry verifications on specific weights, and printing entire weight matrices become impossible.
