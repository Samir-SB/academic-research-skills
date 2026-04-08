# Selection Formulas

Here are the exact formulas used in your pipeline, written clearly and in research-ready form.

## 📡 1. Capacity Formula (Shannon Capacity)

The capacity is derived from the Shannon-Hartley Theorem:

$$C = \log_2(1 + \text{SNR})$$

**Where:**
- $C$: channel capacity (bits/s/Hz)
- $\text{SNR}$: signal-to-noise ratio

**In your implementation:**

$$C = \log_2(1 + \text{SNR}(d))$$

So capacity is distance-dependent through SNR.

## 📶 2. STR (Signal Transmission Reward)

This is your custom reward function based on distance:

$$\text{STR}(d) = \begin{cases} 1 & \text{if } d \leq R_c \\ e^{-k(d - R_c)} & \text{if } d > R_c \end{cases}$$

**Where:**
- $d$: distance between user and provider
- $R_c$: coverage radius (e.g., 200–300 m)
- $k$: decay factor controlling how fast signal drops

## 🔁 3. Extended Reward Logic

From your code and description:

$$R = \begin{cases} 1 & \text{if } C > 0 \\ -1 & \text{if } C = 0 \end{cases}$$
