# Problem Formulation - Reservoir Optimization

## Mathematical Formulation

### Decision Variables
- Q[t]: Water release rate at day t (m³/s), for t = 1, 2, ..., 7

### Parameters
- V_0: Initial storage = 500,000 m³
- V_min: Minimum storage = 100,000 m³
- V_max: Maximum storage = 1,000,000 m³
- Q_eco: Minimum ecological release = 10 m³/s
- Q_max: Maximum release = 100 m³/s
- I[t]: Inflow forecast = [15, 12, 10, 8, 12, 15, 18] m³/s
- P[t]: Hydropower price = [0.08, 0.08, 0.08, 0.08, 0.10, 0.12, 0.10] $/kWh
- Δt: Time step = 86,400 s (1 day)

### Objective Function
Maximize total hydropower revenue:
```
max J = Σ (Q[t] × P[t] × Δt)  for t = 1 to 7
```

### Constraints

**1. Storage Bounds:**
```
V_min ≤ V[t] ≤ V_max   for t = 1 to 7
```

**2. Release Bounds:**
```
Q_eco ≤ Q[t] ≤ Q_max   for t = 1 to 7
```

**3. Mass Balance:**
```
V[t+1] = V[t] + (I[t] - Q[t]) × Δt   for t = 1 to 7
```

**4. Initial Condition:**
```
V[1] = V_0
```

### Implementation Notes
- Converted to minimization problem by negating objective
- Used scipy.optimize.minimize with SLSQP method
- Applied tolerance buffer (TOL=500) to handle floating-point precision
- All constraints enforced as inequality constraints