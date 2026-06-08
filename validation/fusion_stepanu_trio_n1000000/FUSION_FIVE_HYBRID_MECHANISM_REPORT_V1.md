# Fusion Five-Hybrid Mechanism Report V1

## Core Finding

The Symbiotic Five-Hybrid fusion controller is not primarily an armor-based controller.

The dominant mechanism is the Corridor Risk Field:

State + Memory + Trend -> Corridor Risk -> Executive Intervention -> Recovery -> Persistence

## Tested Layers

### 1. Armor OFF
Result: no major degradation.

Conclusion: V91 armor is a last-resort safety layer, not the main driver.

### 2. Ignition OFF
Result: no major degradation.

Conclusion: ignition recovery is auxiliary, not the main driver.

### 3. Corridor Trigger OFF
Result: unsafe_time increased strongly.

Conclusion: corridor trigger is the main active mechanism.

## Corridor Anatomy

Baseline:

corridor_risk =
0.45*(1-CM) + 0.35*(ELI/60) + 0.20*short_mem

Component removal test:

- no_CM worsened unsafe_time
- no_ELI worsened unsafe_time
- no_short_mem worsened unsafe_time

Conclusion:

The risk field is not a single-indicator system. It is a combined state-memory-trend estimator.

## Weight Sweep

Best unsafe_time was obtained by ELI-heavy 0.30 / 0.50 / 0.20.

However, historical current weights 0.45 / 0.35 / 0.20 remain very close to optimum and provide better energy/yield balance.

## ELI Boost Test

Extreme ELI weighting degraded performance.

ELI-only performed worst among tested ELI-heavy variants.

Conclusion:

ELI is valuable as persistence memory, but it must be fused with CM and short-term trend.

## Final Interpretation

Five-Hybrid is best described as:

State estimator: CM
Memory estimator: ELI
Trend estimator: short_mem
Decision layer: Corridor Risk Field
Executive layer: soft corridor intervention + rare armor

## Practical Conclusion

The strongest mechanism identified today is:

Corridor Risk Field = State + Memory + Trend

This supports the broader Recovery/Persistence framework:

Memory -> Build-up -> Detection -> Intervention -> Recovery -> Persistence

